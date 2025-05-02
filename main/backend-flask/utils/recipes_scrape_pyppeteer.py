import os
import threading
import queue
import asyncio
import signal
import sys
from typing import Dict, Any, Optional, List, Tuple
import time
from dotenv import load_dotenv
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from pyppeteer import launch
from pyppeteer_stealth import stealth
# Global shutdown flag to signal all threads to terminate
shutdown_requested = threading.Event()

# Load environment variables
load_dotenv()
host = os.environ.get('DB_HOST', 'localhost')
user = os.environ.get('DB_USR', 'root')
passwd = os.environ.get('DB_PASSWD', '<PASSWORD>')

# Set up a thread-safe connection pool
connection_pool = None

# Signal handler function
def signal_handler(sig, frame):
    """Handle termination signals by setting the shutdown flag"""
    print("\nShutdown signal received. Stopping all threads gracefully...")
    shutdown_requested.set()
    # Give threads some time to notice the shutdown flag
    time.sleep(2)
    print("Shutdown in progress. Please wait for all threads to complete...")

def get_db_connection():
    """Get a connection from the pool"""
    if connection_pool:
        return connection_pool.getconn()
    return None

def return_db_connection(conn):
    """Return a connection to the pool"""
    if connection_pool and conn:
        connection_pool.putconn(conn)

class FoodNetworkScraper:
    def __init__(self, website):
        self.website = website
        self.browser = None
        self.page = None

    async def initialize(self):
        """Initialize the browser and page"""
        self.browser = await launch(
            executablePath="C:\\Users\\Felix\\Downloads\\chromium\\chrome-win\\chrome.exe",
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-extensions',
                '--disable-infobars',
                '--incognito',
                '--disable-notifications',
                '--disable-images',
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--allow-insecure-localhost',
            ]
        )
        self.page = await self.browser.newPage()

        # Set user agent to avoid detection
        await self.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        # Disable JavaScript detection mechanisms
        await self.page.evaluateOnNewDocument("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
        """)

        # Set viewport size
        await self.page.setViewport({'width': 1366, 'height': 768})

        # Enable JavaScript
        await self.page.setJavaScriptEnabled(True)

        # Set timeout
        self.page.setDefaultNavigationTimeout(30000)
        await stealth(self.page)

    async def scrape_recipe_links_from_page(self, page: str, page_num: int, max_retries: int = 3) -> List[Tuple[str, str]] | None:
        """
        Scrape recipe links from a specific page with retry logic

        Args:
            page: The page path to scrape
            page_num: The page number to scrape
            max_retries: Maximum number of retry attempts (default: 3)

        Returns:
            List of tuples containing recipe names and URLs
        """
        retry_count = 0

        while retry_count <= max_retries and not shutdown_requested.is_set():
            try:
                url = f'{self.website}/{page}/p/{page_num}'
                print(f"Scraping links from: {url} (Attempt {retry_count + 1}/{max_retries + 1})")

                # Navigate to the page
                await self.page.goto(url, {'waitUntil': 'networkidle2'})

                links_to_insert = []
                try:
                    # Wait for the links section to load
                    await self.page.waitForXPath('/html/body/section/div[3]/div[3]/div/div/div[1]/div/div/div/section[2]', {'timeout': 5000})

                    # Get the links container
                    links_element = await self.page.xpath('/html/body/section/div[3]/div[3]/div/div/div[1]/div/div/div/section[2]')
                    if not links_element:
                        print(f"No links container found for page {page_num}")
                        return []
                    i =0
                    for container in links_element:
                        # Get all UL elements
                        text_content = await self.page.evaluate('(element) => element.textContent', container)
                        print(f'{text_content} at ind {i}')
                        links_body = await container.querySelectorAll('ul')
                        # print(links_body)
                        # print(links_element)
                        for list_element in links_body:
                            if shutdown_requested.is_set():
                                print(f"Shutdown requested during link extraction for page {page_num}")
                                return []

                            # Get all LI elements
                            link_items = await list_element.querySelectorAll('li')

                            for item in link_items:
                                try:
                                    # Get link text and href
                                    recipe_name = await self.page.evaluate('(element) => element.textContent.trim()', item)

                                    # Get anchor element
                                    link_element = await item.querySelector('a')
                                    if link_element:
                                        recipe_url = await self.page.evaluate('(element) => element.href', link_element)

                                        if recipe_name and recipe_url:
                                            links_to_insert.append((recipe_name, recipe_url))
                                except Exception as e:
                                    print(f"Error processing link: {e}")

                        return links_to_insert
                except Exception as e:
                    print(f"Error processing page elements for {page_num} for '{page}': {e}")
                    if retry_count < max_retries and not shutdown_requested.is_set():
                        retry_count += 1
                        wait_time = 2 ** retry_count  # Exponential backoff: 2s, 4s, 8s
                        print(f"Retrying in {wait_time} seconds...")

                        # Wait with periodic checks for shutdown
                        for _ in range(wait_time * 2):  # Check twice per second
                            if shutdown_requested.is_set():
                                return []
                            await asyncio.sleep(0.5)
                        continue
                    return []

            except Exception as e:
                print(f"Error scraping page {page_num} for '{page}': {e}")
                if retry_count < max_retries and not shutdown_requested.is_set():
                    retry_count += 1
                    wait_time = 2 ** retry_count  # Exponential backoff: 2s, 4s, 8s
                    print(f"Retrying in {wait_time} seconds...")

                    # Wait with periodic checks for shutdown
                    for _ in range(wait_time * 2):  # Check twice per second
                        if shutdown_requested.is_set():
                            return []
                        await asyncio.sleep(0.5)
                    continue
                return []

        # If we've exhausted all retries or shutdown was requested
        if shutdown_requested.is_set():
            print(f"Shutdown requested during scraping of page {page_num} for '{page}'")
        else:
            print(f"Failed to scrape page {page_num} for '{page}' after {max_retries + 1} attempts")
        return []

    async def extract_recipe_data(self, recipe_id) -> Optional[Dict[str, Any]]:
        """Extract all recipe data from the current page."""
        try:
            # Check for shutdown request at the beginning
            if shutdown_requested.is_set():
                print(f"Shutdown requested, skipping extraction for recipe {recipe_id}")
                return None

            # Dict to store all recipe data
            recipe_data = {}

            # --- Image Extraction ---
            try:
                # Try primary image XPath
                img = await self.page.querySelector('#mod-recipe-lead-1 div.section div div div img')
                if not img:
                    # Try fallback image XPath (video thumbnail)
                    img = await self.page.querySelector('#mod-kd-player-1 div div div img')

                if img:
                    img_src = await self.page.evaluate('(element) => element.src', img)
                    # Define placeholder URLs
                    placeholder_urls = [
                        '//food.fnr.sndimg.com/content/dam/images/food/editorial/homepage/fn-feature.jpg.rend.hgtvcom.826.620.suffix/1474463768097.jpeg',
                        '//food.fnr.sndimg.com/content/dam/images/food/editorial/homepage/fn-feature.jpg.rend.hgtvcom.826.620.suffix/1474463768097.webp',
                        'https://food.fnr.sndimg.com/content/dam/images/food/editorial/homepage/fn-feature.jpg.rend.hgtvcom.826.620.suffix/1474463768097.jpeg',
                        'https://food.fnr.sndimg.com/content/dam/images/food/editorial/homepage/fn-feature.jpg.rend.hgtvcom.826.620.suffix/1474463768097.webp'
                    ]
                    # Check if image src is valid and not a placeholder
                    if img_src and img_src.strip() not in placeholder_urls:
                        recipe_data['img_src'] = img_src
                    else:
                        recipe_data['img_src'] = None
                else:
                    recipe_data['img_src'] = None
            except Exception as e:
                print(f"Error extracting image for recipe {recipe_id}: {e}")
                recipe_data['img_src'] = None

            # Check for shutdown periodically
            if shutdown_requested.is_set():
                return None

            # --- Rating Extraction ---
            try:
                ratings = await self.page.querySelector('.rating-stars')
                if ratings:
                    # Try to get the title attribute
                    rating_text = await self.page.evaluate('(element) => element.getAttribute("title")', ratings)
                    if rating_text and 'stars out of 5' in rating_text:
                        rating = rating_text.split(' ')[0].strip()
                        recipe_data['rating'] = float(rating) if rating else 0
                    else:
                        # Fallback to text content
                        rating_text_content = await self.page.evaluate('(element) => element.textContent.trim()', ratings)
                        if rating_text_content:
                            rating_text_content = rating_text_content.strip('rated').split('of 5')[0].strip()
                            recipe_data['rating'] = float(rating_text_content) if rating_text_content else 0
                        else:
                            recipe_data['rating'] = 0
                else:
                    recipe_data['rating'] = 0
            except Exception:
                recipe_data['rating'] = 0

            # --- Number of Ratings Extraction ---
            try:
                num_ratings_element = await self.page.querySelector('.reviews-ct')
                if num_ratings_element:
                    num_ratings_text = await self.page.evaluate('(element) => element.textContent.trim()', num_ratings_element)
                    # Extract only the number part
                    num_ratings = ''.join(c for c in num_ratings_text.split(' ')[0] if c.isdigit())
                    recipe_data['num_of_ratings'] = int(num_ratings) if num_ratings else 0
                else:
                    recipe_data['num_of_ratings'] = 0
            except Exception:
                recipe_data['num_of_ratings'] = 0

            # Check for shutdown periodically
            if shutdown_requested.is_set():
                return None

            # --- Ingredients Extraction ---
            try:
                # Wait for ingredients container to load
                await self.page.waitForSelector('div.o-Ingredients__m-Body', {'timeout': 5000})

                # Look for ingredients within common container structures
                ingredients_container = await self.page.querySelector('div.o-Ingredients__m-Body')
                if ingredients_container:
                    ingredients_elements = await ingredients_container.querySelectorAll('p.o-Ingredients__a-Ingredient')

                    # Clean and join ingredient text
                    ingredients_list = []
                    for el in ingredients_elements:
                        # Check for shutdown during long operations
                        if shutdown_requested.is_set():
                            return None

                        # Clean up text
                        text = await self.page.evaluate('(element) => element.textContent.trim()', el)
                        text = ' '.join(text.split()).strip()
                        if text and text != "'Deselect All" and text != "Deselect All":
                            ingredients_list.append(text)

                    recipe_data['ingredients'] = ingredients_list
                else:
                    print(f"Could not find ingredients container for recipe {recipe_id}")
                    recipe_data['ingredients'] = None
            except Exception as e:
                print(f"Error extracting ingredients for recipe {recipe_id}: {e}")
                recipe_data['ingredients'] = None

            # Check for shutdown periodically
            if shutdown_requested.is_set():
                return None

            # --- Directions Extraction ---
            try:
                # Wait for directions container to load
                await self.page.waitForSelector('div.o-Method__m-Body', {'timeout': 5000})

                # Look for directions within common container structures
                directions_container = await self.page.querySelector('div.o-Method__m-Body')
                if directions_container:
                    directions_elements = await directions_container.querySelectorAll('li')

                    # Clean and format directions
                    directions_list = []
                    for i, step_element in enumerate(directions_elements):
                        # Check for shutdown during potentially long operations
                        if shutdown_requested.is_set():
                            return None

                        step_text = await self.page.evaluate('(element) => element.textContent.trim()', step_element)
                        step_text = ' '.join(step_text.split()).strip()  # Clean whitespace
                        if step_text:
                            directions_list.append(f'{i + 1} : {step_text}')

                    recipe_data['instructions'] = directions_list
                else:
                    print(f"Could not find directions container for recipe {recipe_id}")
                    recipe_data['instructions'] = None
            except Exception as e:
                print(f"Error extracting instructions for recipe {recipe_id}: {e}")
                recipe_data['instructions'] = None

            # Check for shutdown periodically
            if shutdown_requested.is_set():
                return None

            # --- Preparation Details (Level, Time, Servings, Nutrition) ---
            try:
                recipe_data['level'] = ''
                recipe_data['duration'] = ''
                recipe_data['servings'] = ''
                recipe_data['nutrition'] = ''

                # Wait for prep details container to load
                await self.page.waitForSelector('.o-RecipeInfo', {'timeout': 5000})

                prep_elements_container = await self.page.querySelector('.o-RecipeInfo')
                if prep_elements_container:
                    elements = await prep_elements_container.querySelectorAll('ul')

                    level_keywords = ['Level:']
                    time_keywords = ['Total:', 'Cook:', 'Prep:', 'Active:', 'Inactive']
                    servings_keywords = ['Yield:', 'Serves:', 'Makes:']

                    for element in elements:
                        # Check for shutdown during potentially long operations
                        if shutdown_requested.is_set():
                            return None

                        items = await element.querySelectorAll('li')
                        for item in items:
                            element_text = await self.page.evaluate('(element) => element.textContent.trim()', item)
                            if not element_text:
                                continue

                            # Check for Level
                            if any(keyword in element_text for keyword in level_keywords):
                                level_parts = element_text.split(':')
                                if len(level_parts) > 1:
                                    recipe_data['level'] = level_parts[1].strip()
                                continue

                            # Check for Time
                            if any(keyword in element_text for keyword in time_keywords):
                                recipe_data['duration'] += ", " + element_text
                                continue

                            # Check for Servings and nutrition
                            if any(keyword in element_text for keyword in servings_keywords):
                                # Extract servings text (usually the first line)
                                servings_text = element_text.split('\n')[0].strip()
                                recipe_data['servings'] += servings_text

                                # Try to find and click the nutrition button
                                try:
                                    if shutdown_requested.is_set():
                                        return None

                                    nutrition_button = await item.querySelector('button')
                                    if nutrition_button:
                                        await nutrition_button.click()

                                        # Wait for nutrition info to load
                                        await self.page.waitForSelector('#mod-nutrition-info-1 div div:nth-child(2) dl:nth-child(2)', {'timeout': 5000})

                                        # Find nutrition info
                                        nutrition_container = await self.page.querySelector('#mod-nutrition-info-1 div div:nth-child(2) dl:nth-child(2)')
                                        if nutrition_container:
                                            nutrition_text = await self.page.evaluate('(element) => element.textContent', nutrition_container)
                                            nutrition_text_lines = nutrition_text.split('\n')

                                            # Process nutrition data
                                            nutrition_pairs = []
                                            for i in range(0, len(nutrition_text_lines) - 1, 2):
                                                if i + 1 < len(nutrition_text_lines):
                                                    key = nutrition_text_lines[i].strip(': ')
                                                    value = nutrition_text_lines[i + 1].strip()
                                                    if key and value:
                                                        nutrition_pairs.append(f"{key}: {value}")

                                            recipe_data['nutrition'] = ', '.join(nutrition_pairs)
                                except Exception as nutr_err:
                                    print(f"Error processing nutrition info for recipe {recipe_id}: {nutr_err}")
                                    recipe_data['nutrition'] = None
                                continue
                else:
                    print(f"Could not find preparation details container for recipe {recipe_id}")
                    recipe_data['level'] = None
                    recipe_data['duration'] = None
                    recipe_data['servings'] = None
                    recipe_data['nutrition'] = None
            except Exception as e:
                print(f"Error extracting preparation details for recipe {recipe_id}: {e}")
                recipe_data['level'] = None
                recipe_data['duration'] = None
                recipe_data['servings'] = None
                recipe_data['nutrition'] = None

            # Final shutdown check before returning data
            if shutdown_requested.is_set():
                return None

            # Return collected data
            return recipe_data

        except Exception as e:
            print(f"General error extracting recipe data for recipe {recipe_id}: {e}")
            import traceback
            traceback.print_exc()  # Print stack trace for debugging
            return None

    async def close(self):
        """Close the browser instance and release resources."""
        if self.browser:
            try:
                await self.browser.close()
                print("Browser closed successfully.")
                self.browser = None
            except Exception as e:
                print(f"Error closing browser: {e}")


def setup_database():
    """Set up the database and return a connection pool"""
    # Connect to default PostgreSQL database
    mydb = psycopg2.connect(
        host=host,
        user=user,
        password=passwd
    )
    mydb.autocommit = True
    cursor = mydb.cursor()

    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'automation'")
    exists = cursor.fetchone()

    # Create database if it doesn't exist
    if not exists:
        cursor.execute("CREATE DATABASE automation")

    cursor.close()
    mydb.close()

    # Connect to automation database
    automators = psycopg2.connect(
        host=host,
        user=user,
        password=passwd,
        database="automation"
    )
    automators.autocommit = True
    cursor = automators.cursor()

    # Create recipes table if it doesn't exist
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS recipes (
                                                  id SERIAL PRIMARY KEY,
                                                  name VARCHAR(255) NOT NULL,
                                                  url VARCHAR(255),
                                                  img_src TEXT,
                                                  ingredients TEXT[],
                                                  instructions TEXT[],
                                                  level TEXT,
                                                  nutrition TEXT,
                                                  duration TEXT,
                                                  rating DECIMAL(3,2) DEFAULT 0,
                                                  num_of_ratings INT DEFAULT 0,
                                                  servings TEXT,
                                                  UNIQUE (name, url)
           )"""
    )

    # Create categories table if it doesn't exist
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS categories (
                                                     id SERIAL PRIMARY KEY,
                                                     name VARCHAR(255) UNIQUE
           )"""
    )

    # Create recipes_categories junction table if it doesn't exist
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS recipes_categories (
                                                             catId INT,
                                                             recipeId INT,
                                                             PRIMARY KEY (catId, recipeId),
                                                             FOREIGN KEY (catId) REFERENCES categories(id),
                                                             FOREIGN KEY (recipeId) REFERENCES recipes(id),
                                                             UNIQUE (catId, recipeId)
           )"""
    )

    cursor.close()
    automators.close()

    # Create a connection pool
    global connection_pool
    connection_pool = ThreadedConnectionPool(
        minconn=5,
        maxconn=20,
        host=host,
        user=user,
        password=passwd,
        database="automation"
    )

    return connection_pool


async def scrape_recipe_links_worker(page, page_nums, website, result_queue):
    """Worker function for scraping recipe links"""
    scraper = FoodNetworkScraper(website)
    try:
        await scraper.initialize()
        for page_num in page_nums:
            # Check if shutdown was requested
            if shutdown_requested.is_set():
                print(f"Shutdown requested, stopping scraping for '{page}'")
                break

            links = await scraper.scrape_recipe_links_from_page(page, page_num)
            if links:
                result_queue.put((page, page_num, links))
    finally:
        await scraper.close()


def insert_recipe_links(result_queue):
    """Insert recipe links from the queue into the database"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        while not shutdown_requested.is_set():
            try:
                # Use a timeout to periodically check for shutdown
                try:
                    item = result_queue.get(block=True, timeout=0.5)
                except queue.Empty:
                    continue

                if item is None:  # Sentinel value to stop
                    break

                page, page_num, links = item

                for recipe_name, recipe_url in links:
                    # Check for shutdown during potentially long operations
                    if shutdown_requested.is_set():
                        break

                    try:
                        cursor.execute('INSERT INTO recipes(name, url) VALUES(%s, %s) ON CONFLICT (name, url) DO NOTHING;',
                                       (recipe_name, recipe_url))
                    except Exception as e:
                        print(f"Error inserting link: {e}")

                conn.commit()
                print(f"Completed page {page_num} for '{page}'")
                result_queue.task_done()

            except Exception as e:
                if shutdown_requested.is_set():
                    break

                print(f"Error in insert_recipe_links: {e}")
                if not result_queue.empty():
                    result_queue.task_done()
                time.sleep(0.5)  # Delay on error

        # Final commit on shutdown
        if conn:
            conn.commit()
            print("Database worker shutting down, final commit done")

    finally:
        if conn:
            conn.commit()
            return_db_connection(conn)


async def get_page_count(website, page):
    """Get the number of pages for a given letter/group"""
    scraper = FoodNetworkScraper(website)
    try:
        await scraper.initialize()
        await scraper.page.goto(f'{website}/{page}/p/1', {'waitUntil': 'networkidle2'})

        # Find total number of pages
        page_elements = await scraper.page.querySelectorAll('#site > div.l-main-content > div.l-l-col > div > div > div.l-content > div > div > div > section.o-Pagination > ul > li')

        if not page_elements:
            return 1  # Default to 1 if no pagination elements found

        try:
            # Get the second-to-last element which should contain the max page number
            second_last_element = page_elements[-2]
            total_pages_text = await scraper.page.evaluate('(element) => element.textContent.trim()', second_last_element)
            total_pages = int(total_pages_text)
            return total_pages
        except (IndexError, ValueError):
            # If we can't determine total pages, just process the current page
            return 1
    finally:
        await scraper.close()


async def parallel_scrape_recipe_links(website, max_workers=4, start='a', end='z'):
    """Scrape links using multiple threads"""
    # Generate A-Z pages plus numbers and special characters
    pages = ["123"]
    for i in range(ord(end) - ord(start) + 1):  # start through end
        pages.append(chr(i + ord(start)))
    pages.append("xyz")  # Special characters

    # Create a queue for results
    result_queue = queue.Queue()

    # Start the database worker thread
    db_thread = threading.Thread(target=insert_recipe_links, args=(result_queue,))
    db_thread.daemon = True
    db_thread.start()

    # Process each page
    for page in pages:
        if shutdown_requested.is_set():
            print("Shutdown requested, stopping scraping setup")
            break

        try:
            print(f"Starting scrape for page: {page}")

            # Get the number of pages for this letter/group
            total_pages = await get_page_count(website, page)
            print(f"Found {total_pages} pages for letter/group '{page}'")

            # Check for shutdown after determining page count
            if shutdown_requested.is_set():
                break

            # Split pages into chunks for workers
            page_chunks = [[] for _ in range(max_workers)]
            for i in range(1, total_pages + 1):
                page_chunks[i % max_workers].append(i)

            # Create a list of tasks
            tasks = []
            for chunk in page_chunks:
                if chunk and not shutdown_requested.is_set():
                    task = asyncio.create_task(scrape_recipe_links_worker(page, chunk, website, result_queue))
                    tasks.append(task)

            # Wait for all tasks to complete
            if tasks:
                await asyncio.gather(*tasks)

        except Exception as e:
            print(f"Error setting up scraping for page '{page}': {e}")

    # Signal database worker to finish
    result_queue.put(None)

    # Wait for database thread to finish
    db_thread.join(timeout=5.0)  # Give it 5 seconds to finish

    print("Link scraping completed or shutdown")


async def update_recipe_worker(recipes_chunk, website):
    """Worker function to update recipe details"""
    scraper = FoodNetworkScraper(website)
    conn = get_db_connection()
    try:
        await scraper.initialize()
        cursor = conn.cursor()

        for recipe in recipes_chunk:
            # Check if shutdown was requested
            if shutdown_requested.is_set():
                print("Shutdown requested, stopping recipe updates")
                break

            recipe_id, url, name = recipe
            print(f"Updating recipe {recipe_id}: {name}")

            try:
                await scraper.page.goto(url, {'waitUntil': 'networkidle2'})

                # Extract recipe details
                recipe_data = await scraper.extract_recipe_data(recipe_id)

                # Check again if shutdown was requested after long extraction
                if shutdown_requested.is_set():
                    print(f"Shutdown requested after extraction for recipe {recipe_id}")
                    break

                if recipe_data:
                    # Update database with recipe details
                    cursor.execute('''
                                   UPDATE recipes
                                   SET
                                       ingredients = %s,
                                       instructions = %s,
                                       nutrition = %s,
                                       rating = %s,
                                       level = %s,
                                       num_of_ratings = %s,
                                       duration = %s,
                                       img_src = %s,
                                       servings= %s
                                   WHERE id = %s
                                   ''', (
                                       recipe_data.get('ingredients'),
                                       recipe_data.get('instructions'),
                                       recipe_data.get('nutrition'),
                                       recipe_data.get('rating'),
                                       recipe_data.get('level'),
                                       recipe_data.get('num_of_ratings'),
                                       recipe_data.get('duration'),
                                       recipe_data.get('img_src'),
                                       recipe_data.get('servings'),
                                       recipe_id
                                   ))

                    # Process categories if shutdown not requested
                    if not shutdown_requested.is_set():
                        try:
                            # Find category links
                            categories_elements = await scraper.page.querySelectorAll('#site > div.l-main-content > div.l-l-col > div > div > div.l-content > div > section > div:nth-child(4) > section > div > div > a')
                            if not categories_elements:
                                # Try alternate selector
                                categories_elements = await scraper.page.querySelectorAll('#site > div.l-main-content > div.l-xl-col > div > div > div.l-content > div > section > div:nth-child(4) > section > div > div > a')

                            # Delete existing categories for this recipe
                            cursor.execute('DELETE FROM recipes_categories WHERE recipeId = %s', (recipe_id,))

                            for category_element in categories_elements:
                                # Check for shutdown during long category processing
                                if shutdown_requested.is_set():
                                    break

                                cat_name = await scraper.page.evaluate('(element) => element.textContent.trim()', category_element)
                                if cat_name and cat_name.lower() != 'recipe':
                                    # Insert category if it doesn't exist
                                    cursor.execute('INSERT INTO categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id', (cat_name,))
                                    cat_id_result = cursor.fetchone()

                                    if cat_id_result:
                                        cat_id = cat_id_result[0]
                                    else:
                                        # Get the ID if it already existed
                                        cursor.execute('SELECT id FROM categories WHERE name = %s', (cat_name,))
                                        cat_id = cursor.fetchone()[0]

                                    # Link recipe to category
                                    cursor.execute('INSERT INTO recipes_categories (catId, recipeId) VALUES (%s, %s) ON CONFLICT DO NOTHING',
                                                   (cat_id, recipe_id))
                        except Exception as cat_err:
                            print(f"Error processing categories for recipe {recipe_id}: {cat_err}")

                    # Commit changes for this recipe
                    conn.commit()
                    print(f"Successfully updated recipe {recipe_id}: {name}")
                else:
                    print(f"No data extracted for recipe {recipe_id}: {name}")

            except Exception as e:
                print(f"Error updating recipe {recipe_id}: {e}")
                # Continue with next recipe, don't stop the whole process

            # Add a small delay between requests to avoid rate limiting
            if not shutdown_requested.is_set():
                await asyncio.sleep(1)

    except Exception as e:
        print(f"Worker error: {e}")
    finally:
        if conn:
            conn.commit()
            return_db_connection(conn)
        await scraper.close()


async def update_recipe_details(website, max_workers=4):
    """Update recipe details for recipes without ingredients"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Get recipes that need to be updated
        cursor.execute("SELECT id, url, name FROM recipes WHERE ingredients IS NULL OR ingredients = '{}'")
        recipes_to_update = cursor.fetchall()

        if not recipes_to_update:
            print("No recipes need updating.")
            return

        print(f"Found {len(recipes_to_update)} recipes to update")

        # Split recipes into chunks for workers
        chunk_size = (len(recipes_to_update) + max_workers - 1) // max_workers
        recipe_chunks = [recipes_to_update[i:i + chunk_size] for i in range(0, len(recipes_to_update), chunk_size)]

        # Create tasks for each chunk
        tasks = []
        for chunk in recipe_chunks:
            if shutdown_requested.is_set():
                break
            task = asyncio.create_task(update_recipe_worker(chunk, website))
            tasks.append(task)

        # Wait for all tasks to complete
        if tasks:
            await asyncio.gather(*tasks)

    except Exception as e:
        print(f"Error in update_recipe_details: {e}")
    finally:
        if conn:
            return_db_connection(conn)


async def main():
    """Main program entry point"""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Setup database
    try:
        setup_database()
        print("Database setup complete")
    except Exception as e:
        print(f"Database setup error: {e}")
        return 1

    # Website to scrape
    website = 'https://www.foodnetwork.com/recipes/recipes-a-z'

    try:
        # Command line argument parsing

        max_workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
        if len(sys.argv) > 2:
            command = sys.argv[2].lower()

            if command == 'scrape_links':
                # Optional parameters for scrape_links
                start_char = sys.argv[3] if len(sys.argv) > 3 else 'a'
                end_char = sys.argv[4] if len(sys.argv) > 4 else 'z'

                print(f"Starting link scraping with {max_workers} workers from '{start_char}' to '{end_char}'")
                await parallel_scrape_recipe_links(website, max_workers, start_char, end_char)

            elif command == 'update_recipes':
                # Optional parameters for update_recipes
                limit = int(sys.argv[3]) if len(sys.argv) > 3 else None

                print(f"Starting recipe updates with {max_workers} workers" +
                      (f", limit: {limit}" if limit else ""))
                await update_recipe_details(website, max_workers)

            else:
                print(f"Unknown command: {command}")
                print("Available commands: scrape_links, update_recipes")
                return 1
        else:
            # Default: run both operations
            print("Running full scraping process...")
            if not shutdown_requested.is_set():
                await parallel_scrape_recipe_links(website, max_workers)
            if not shutdown_requested.is_set():
                await update_recipe_details(website, max_workers)

    except Exception as e:
        print(f"Error in main: {e}")
        return 1
    finally:
        # Clean up connection pool
        if connection_pool:
            try:
                connection_pool.closeall()
                print("Database connection pool closed")
            except Exception as e:
                print(f"Error closing connection pool: {e}")

        if shutdown_requested.is_set():
            print("Program terminated due to shutdown request")
        else:
            print("Program completed successfully")

    return 0
if __name__ == "__main__":
    # Set up event loop
# 30346
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Critical error: {e}")
    finally:
        print("Scraper shutdown complete")