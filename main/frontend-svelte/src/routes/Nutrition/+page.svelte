<script lang="ts">
    import {onMount} from 'svelte';
    import InfoBlock from '$lib/components/recipes/InfoBlock.svelte';
    import axios from 'axios';
    import RecipeAutocomplete from '$lib/components/recipes/RecipeAutocomplete.svelte';
    import Fuse from "fuse.js";
    import {browser} from '$app/environment';
    // State variables
    let querySearch = '';
    let recipes = [];
    let searchedRecipeArray = null; // Array of recipes with the same name
    let recommendedRecipes = [];
    let allCategories: { id: string, name: string, slug: string }[] = []; // To store all categories from CSV
    let topLevelCategories: {
        name: string, icon: string, color: string, actualCategoryNames?: string[]
    }[] =
        [
            // Define some "parent" or "entry-point" categories manually for the initial view
        // `actualCategoryNames` will map to names in your CSV for fetching
        {
            name: 'Main Proteins',
            icon: '🥩',
            color: '#FF6347',
            actualCategoryNames: ['Meat', 'Poultry', 'Fish', 'Shellfish', 'Beef', 'Pork', 'Chicken Recipes', 'Turkey Recipes', 'Salmon', 'Shrimp']
        }, {
            name: 'Dish Types',
            icon: '🍲',
            color: '#4CAF50',
            actualCategoryNames: ['Main Dish', 'Side Dish', 'Appetizer', 'Dessert', 'Soup', 'Salad Recipes', 'Breakfast', 'Lunch', 'Brunch']
        }, {
            name: 'Cuisines',
            icon: '🌍',
            color: '#2196F3',
            actualCategoryNames: ['Asian', 'Italian', 'French', 'Mexican Chicken', 'Chinese Recipes', 'Indian Recipes', 'Thai', 'Japanese Recipes', 'Spanish', 'Greek Recipes', 'Filipino Recipes']
        }, {
            name: 'Dietary & Health',
            icon: '🥗',
            color: '#FFC107',
            actualCategoryNames: ['Healthy', 'Vegetarian', 'Vegan', 'Gluten Free', 'Low Calorie', 'Low-Carb', 'Heart-Healthy']
        }, {
            name: 'Cooking Methods',
            icon: '🍳',
            color: '#9C27B0',
            actualCategoryNames: ['Baking', 'Grilling', 'Roasting', 'Sauteing Recipes', 'Stir-Frying Recipes', 'Slow-Cooker', 'Deep-Frying']
        }, {
            name: 'By Ingredient',
            icon: '🥕',
            color: '#FF5722',
            actualCategoryNames: ['Vegetable', 'Fruit', 'Rice Recipes', 'Pasta Recipes', 'Cheese', 'Chocolate', 'Mushroom', 'Potato', 'Tomato']
        }, {
            name: 'Quick & Easy', icon: '⏱️', color: '#FFA000', // Orange
            actualCategoryNames: ['Easy', // 41411
                'Easy Main Dish', 'Easy Side Dish Recipes', 'Easy Appetizer', 'Easy Dessert Recipes', 'Easy Dinner Recipes', 'Easy Lunch Recipes', 'Easy Breakfast Recipes', 'Easy Baking', 'No-Cook Recipes', 'Make Ahead']
        }, {
            name: 'Kid Friendly', icon: '🧒', // Child face icon, or use 😊
            color: '#4DD0E1', // Light Blue/Cyan
            actualCategoryNames: ['Kid-Friendly', 'Macaroni and Cheese', 'Italian Pizza', 'Burger', 'Taco', 'Pancake', 'Cookie', 'Cupcake', 'Chicken Wing', 'Smoothie Recipes', 'Fries']
        }
        // Add more top-level categories as you see fit
    ];
    let displayedSubCategories: { id: string, name: string, slug: string }[] = []; // Categories to show after clicking a top-level one
    let currentTopLevelCategory: string | null = null; // Name of the selected top-level category
    // Helper function to assign an appropriate icon to each category
    // Helper function to get a consistent color for each category

    function getCategoryColor(categoryName) {
        // Create a simple hash from the category name to get consistent colors
        const colors = ['#FF6347', // Red-orange
            '#4CAF50', // Green
            '#2196F3', // Blue
            '#FFC107', // Amber/Yellow
            '#9C27B0', // Purple
            '#FF5722', // Deep Orange
            '#00BCD4', // Cyan
            '#8BC34A', // Light Green
            '#E91E63', // Pink
            '#3F51B5'  // Indigo
        ];

        // Simple hash function to get index
        let hash = 0;
        for (let i = 0; i < categoryName.length; i++) {
            hash = categoryName.charCodeAt(i) + ((hash << 5) - hash);
        }

        // Use absolute value and modulo to get an index within the colors array
        const index = Math.abs(hash) % colors.length;
        return colors[index];
    }

    function getCategoryIcon(categoryName) {
        const name = categoryName.toLowerCase();

        // Match categories to appropriate emojis
        if (name.includes('chicken') || name.includes('poultry')) return '🍗';
        if (name.includes('beef') || name.includes('steak') || name.includes('meat')) return '🥩';
        if (name.includes('fish') || name.includes('salmon') || name.includes('tuna')) return '🐟';
        if (name.includes('shellfish') || name.includes('shrimp') || name.includes('crab')) return '🦐';
        if (name.includes('vegan') || name.includes('vegetarian')) return '🥗';
        if (name.includes('salad')) return '🥬';
        if (name.includes('dessert') || name.includes('cake') || name.includes('sweet')) return '🍰';
        if (name.includes('breakfast')) return '🍳';
        if (name.includes('soup')) return '🍲';
        if (name.includes('pasta') || name.includes('noodle')) return '🍝';
        if (name.includes('pizza')) return '🍕';
        if (name.includes('sandwich')) return '🥪';
        if (name.includes('burger')) return '🍔';
        if (name.includes('rice')) return '🍚';
        if (name.includes('vegetable')) return '🥕';
        if (name.includes('fruit') || name.includes('berry')) return '🍎';
        if (name.includes('baking') || name.includes('bread')) return '🍞';
        if (name.includes('cheese')) return '🧀';
        if (name.includes('egg')) return '🥚';
        if (name.includes('seafood')) return '🦞';
        if (name.includes('pork')) return '🥓';
        if (name.includes('mexican')) return '🌮';
        if (name.includes('italian')) return '🍕';
        if (name.includes('asian') || name.includes('chinese')) return '🥢';
        if (name.includes('indian')) return '🍛';
        if (name.includes('thai')) return '🥘';
        if (name.includes('japanese')) return '🍱';
        if (name.includes('mediterranean') || name.includes('greek')) return '🫒';
        if (name.includes('bbq') || name.includes('barbecue') || name.includes('grill')) return '🔥';
        if (name.includes('slow cooker') || name.includes('slow-cooker')) return '♨️';
        if (name.includes('holiday') || name.includes('christmas')) return '🎄';
        if (name.includes('halloween')) return '🎃';
        if (name.includes('thanksgiving')) return '🦃';
        if (name.includes('healthy') || name.includes('diet')) return '💪';
        if (name.includes('drink') || name.includes('cocktail') || name.includes('beverage')) return '🍹';

        // Default for categories without specific matches
        return '🍽️';
    }

    let selectedFullCategory: { id: string, name: string, slug: string } | null = null; // The actual category from CSV used for fetching recipes
    let categoryRecipes = [];
    let isLoadingCategories = true; // For loading allCategories
    let isLoadingCategoryRecipes = false; // For loading recipes of a selectedFullCategory
    let isLoadingMore = false;
    let currentPage = 0;
    const pageSize = 9; // Adjust as needed
    let hasMoreRecipes = false;
    let searchedRecipes = [];
    // For searching/filtering the full list of categories
    let categorySearchTerm = '';
    let filteredAllCategories: { id: string, name: string, slug: string }[] = [];
    let fuseCategories: Fuse<{ id: string, name: string, slug: string }> | null = null;
    // Fetch initial recipes on component mount
    onMount(async () => {
        try {
            const res = await axios.get('/api/v1/recipes/10');
            console.log('Response data:', res.data);
            console.log('Response status:', res.data.length);

            recipes = res.data;
            isLoadingCategories = true;
            const response = await axios.get('/api/v1/recipes/categories'); // Assuming this endpoint returns your CSV data as JSON
            allCategories = response.data
            console.log("allCategories")
            console.log(allCategories)
            // Initialize Fuse.js for searching categories
            fuseCategories = new Fuse(allCategories, {
                keys: ['name'], threshold: 0.3, // Adjust sensitivity
            });
            filteredAllCategories = allCategories.slice(0, 20); // Show some initially
            isLoadingCategories = false;
        } catch (err) {
            console.log(err);
        }
    });

    // Search function
    async function getQuery(query) {
        if (query === '') {
            querySearch = '';
            searchedRecipes = [];
            return;
        }

        try {
            const promise = await axios.post(`/api/v1/recipes/${query.toLowerCase()}`);
            console.log('Raw search results:', promise.data);

            // Sort results by relevance to the query
            if (Array.isArray(promise.data) && promise.data.length > 0) {
                const sortedResults = sortResultsByRelevance(promise.data, query);
                searchedRecipes = sortedResults;
            } else {
                searchedRecipes = promise.data;
            }
        } catch (err) {
            console.error('Search error:', err);
            searchedRecipes = [];
        }
    }

    // Function to sort search results by relevance to the query
    function sortResultsByRelevance(results, query) {
        const lowerQuery = query.toLowerCase();

        return [...results].sort((a, b) => {
            const aQuery = (a.query || '').toLowerCase();
            const bQuery = (b.query || '').toLowerCase();

            // Exact matches get highest priority
            if (aQuery === lowerQuery && bQuery !== lowerQuery) return -1;
            if (bQuery === lowerQuery && aQuery !== lowerQuery) return 1;

            // Then prioritize by "starts with"
            if (aQuery.startsWith(lowerQuery) && !bQuery.startsWith(lowerQuery)) return -1;
            if (bQuery.startsWith(lowerQuery) && !aQuery.startsWith(lowerQuery)) return 1;

            // Then by "includes"
            if (aQuery.includes(lowerQuery) && !bQuery.includes(lowerQuery)) return -1;
            if (bQuery.includes(lowerQuery) && !aQuery.includes(lowerQuery)) return 1;

            // As a last resort, sort by string length (shorter = more relevant)
            return aQuery.length - bQuery.length;
        });
    }

    // Watch for querySearch changes
    $: {
        getQuery(querySearch);
    }

    // Updated Search recipe function
    async function searchRecipe(termToSearch) {
        console.log("searchRecipe in +page.svelte called with term:", termToSearch);

        if (!termToSearch || termToSearch.trim() === '') {
            console.warn("Search term provided to searchRecipe is empty. Clearing results.");
            querySearch = ''; // Clear the page's querySearch state
            searchedRecipeArray = null;
            recommendedRecipes = [];
            // searchedRecipes = []; // If you want to clear this too
            return;
        }

        querySearch = termToSearch; // Update the page's state with the term being searched

        console.log("Query being used for API call: " + querySearch);

        try {
            const res = await axios.get(`/api/v1/recipes/recipe/${encodeURIComponent(querySearch)}`);
            console.log("Recipe search response:", res.data);

            searchedRecipeArray = res.data;

            if (searchedRecipeArray && searchedRecipeArray.length > 0) {
                const firstRecipe = searchedRecipeArray[0];
                let ingredientsParam = '';

                // Ensure ingredients exist and handle if it's an array or string
                if (firstRecipe.ingredients) {
                    ingredientsParam = Array.isArray(firstRecipe.ingredients) ? firstRecipe.ingredients.join(',') : String(firstRecipe.ingredients);
                }

                if (ingredientsParam) {
                    const recRes = await axios.get(`/api/v1/recipes/recommendations?query=${encodeURIComponent(querySearch)}&ingredients=${encodeURIComponent(ingredientsParam)}`);
                    console.log("Recommendation response:", recRes.data);
                    recommendedRecipes = recRes.data;
                } else {
                    console.warn(`No ingredients found for recipe "${querySearch}" to fetch recommendations.`);
                    recommendedRecipes = [];
                }
            } else {
                recommendedRecipes = []; // Clear recommendations if no recipe was found
            }
        } catch (err) {
            console.error("Error fetching recipe or recommendations:", err);
            searchedRecipeArray = null;
            recommendedRecipes = [];
        }
    }


    // Clear function
    function clearSearch() {
        recommendedRecipes = [];
        querySearch = '';
        searchedRecipeArray = null;
    }

    function handleTopLevelCategoryClick(topCategory: typeof topLevelCategories[0]) {
        currentTopLevelCategory = topCategory.name;
        selectedFullCategory = null; // Clear specific recipe selection
        categoryRecipes = []; // Clear recipes

        // Find categories from allCategories that match the names in topCategory.actualCategoryNames
        if (topCategory.actualCategoryNames) {
            displayedSubCategories = allCategories.filter(cat => topCategory.actualCategoryNames!.map(n => n.toLowerCase()).includes(cat.name.toLowerCase()));
        } else {
            // Fallback: if no actualCategoryNames, maybe try a fuzzy search or show related
            displayedSubCategories = []; // Or implement a different logic
        }
    }

    // Function to fetch recipes by category
    async function fetchRecipesByFullCategory(category: {
        id: string, name: string, slug: string
    }, initialFetch = true) {
        if (initialFetch) {
            selectedFullCategory = category;
            categoryRecipes = [];
            currentPage = 0;
            hasMoreRecipes = false;
        }

        isLoadingCategoryRecipes = true;
        try {
            // Use category.name (original name from CSV) or category.slug for the API call
            const response = await axios.get(`/api/v1/recipes/category/${encodeURIComponent(category.name)}?page=${currentPage}&pageSize=${pageSize}`);
            const newRecipes = response.data || [];
            if (initialFetch) {
                categoryRecipes = newRecipes;
            } else {
                categoryRecipes = [...categoryRecipes, ...newRecipes];
            }
            hasMoreRecipes = newRecipes.length === pageSize;
        } catch (err) {
            console.error(`Error fetching ${category.name} recipes:`, err);
            if (initialFetch) categoryRecipes = [];
            hasMoreRecipes = false;
        } finally {
            isLoadingCategoryRecipes = false;
            if (!initialFetch) isLoadingMore = false;
        }
    }

    async function fetchMoreCategoryRecipes() {
        if (isLoadingMore || !selectedFullCategory || !hasMoreRecipes) return;
        isLoadingMore = true;
        currentPage++;
        await fetchRecipesByFullCategory(selectedFullCategory, false);
    }

    // Watch for categorySearchTerm to filter allCategories
    $: if (browser && fuseCategories) {
        if (categorySearchTerm.trim() === '') {
            filteredAllCategories = allCategories.slice(0, 20); // Show initial subset or all if not too many
        } else {
            const results = fuseCategories.search(categorySearchTerm);
            filteredAllCategories = results.map(result => result.item);
        }
    }


    // For animation purposes
    function handleCategoryHover(event, isEntering) {
        const card = event.currentTarget;
        if (isEntering) {
            card.style.transform = 'translateY(-10px)';
        } else {
            card.style.transform = 'translateY(0)';
        }
    }
</script>

<div class='heroback py-8 w-full mx-auto' id='nutrition-header'>
    <div class="h-16"></div>
    <h1 class='text-primary font-orbital font-bold text-4xl py-5 my-5 text-center'>Search for Personalized Recipes
        shipped right to your door</h1>

    <h3 class="text-primary text-3xl font-orbital font-bold text-center">Search for recipes from our personalized
        catalogue</h3>

    <!-- Recipe Components -->
    <div class="wrapper w-full">
        {#each recipes as recipe, index}
            <div class={`item item${index + 1}`}>
                <InfoBlock
                        title={recipe.name}
                        headingClass="text-gray-800 text-2xl text-center font-orbital font-bold"
                        text={[
                        recipe.duration ? `Duration: ${recipe.duration}` : "",
                        recipe.rating ? `Rating: ${recipe.rating}` : "",
                        recipe.servings ? `${recipe.servings}` : "",
                    ]}
                        recipe={recipe}
                        fadeInAnimation="fadeIn"
                        bg="bg-[#3E92CC]"
                        expandable={true}
                />
            </div>
        {/each}
    </div>

    <div class='bg-info w-full max-w-xl mx-auto' style="
        border: 1rem solid rgba(0, 255, 255, .5);
        box-shadow: 8px 8px 3px rgba(0, 255, 125, 1);
        padding: 20px;
        border-radius: 2px;
    ">
        <h2 class='text-primary text-3xl font-orbital font-bold py-8 text-center'>Recommend recipes</h2>

        {#if searchedRecipeArray && searchedRecipeArray.length > 0}
            <div class="relative">
                <InfoBlock
                        bg='bg-[#faebd7] w-1/3'
                        title={searchedRecipeArray[0].name}
                        headingClass="text-gray-800 text-2xl font-orbital font-bold text-center"
                        recipeArray={searchedRecipeArray}
                        text={[
                // searchedRecipeArray[0].author ? `By: ${searchedRecipeArray[0].author}` : ""
            ]}
                        expandable={true}
                />
            </div>
        {/if}


        <div class='flex justify-center'>

            <RecipeAutocomplete
                    onSearchExecute={searchRecipe}
                    onClearExecute={clearSearch}
            />

        </div>

    </div>


    {#if recommendedRecipes.length !== 0}
        <h2 class="text-primary text-2xl font-orbital font-bold py-6 text-center">Similar Recipes You Might Like</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5 justify-center">
            {#each recommendedRecipes as recipeGroup, index}
                {#if Array.isArray(recipeGroup) && recipeGroup.length > 0}
                    <!-- Handle array of recipes with same name -->
                    <div class="flex justify-center">
                        <InfoBlock
                                title={recipeGroup[0].name}
                                headingClass="text-gray-800 text-2xl font-orbital font-bold text-center"
                                text={[
                                recipeGroup[0].duration ? `Duration: ${recipeGroup[0].duration}` : "",
                                recipeGroup[0].rating ? `Rating: ${recipeGroup[0].rating}` : "",
                            ]}
                                recipeArray={recipeGroup}
                                fadeInAnimation="fadeIn"
                                bg="bg-info"
                                expandable={true}
                        />
                    </div>
                {:else}
                    <!-- Handle single recipe object -->
                    <div class="flex justify-center">
                        <InfoBlock
                                title={recipeGroup.name}
                                headingClass="text-gray-800 text-2xl font-orbital font-bold text-center"
                                text={[
                                recipeGroup.duration ? `Duration: ${recipeGroup.duration}` : "",
                                recipeGroup.rating ? `Rating: ${recipeGroup.rating}` : "",
                                // recipeGroup.author ? `By: ${recipeGroup.author}` : ""
                            ]}
                                recipe={recipeGroup}
                                fadeInAnimation="fadeIn"
                                bg="bg-info"
                                expandable={true}
                        />
                    </div>
                {/if}
            {/each}
        </div>
    {/if}
</div>

<!-- New Category Exploration Section -->
<section class="category-browse py-16">
    <div class="container mx-auto px-4">
        <div class="text-center mb-12">
            <h2 class="text-primary font-orbital font-bold text-4xl mb-3">Explore Recipe Categories</h2>
            <p class="text-gray-600 text-xl max-w-2xl mx-auto">
                Start by selecting a broad category, or search our full list.
            </p>
        </div>

        <!-- Top Level Category Cards -->
        {#if !currentTopLevelCategory && !selectedFullCategory}
            <h3 class="text-secondary font-orbital font-semibold text-2xl mb-6 text-center">Browse by Topic</h3>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 mb-12">
                {#each topLevelCategories as category}
                    <div
                            class="category-card cursor-pointer rounded-lg overflow-hidden shadow-lg transition-all duration-300 p-6 flex flex-col items-center justify-center text-center"
                            style="border: 2px solid {category.color}; background-color: {category.color}20;"
                            on:mouseenter={(e) => handleCategoryHover(e, true)}
                            on:mouseleave={(e) => handleCategoryHover(e, false)}
                            on:click={() => handleTopLevelCategoryClick(category)}>
                        <span class="text-5xl mb-3">{category.icon}</span>
                        <h3 class="text-white font-orbital font-bold text-xl">{category.name}</h3>
                    </div>
                {/each}
            </div>
        {/if}

        {#if currentTopLevelCategory && displayedSubCategories.length > 0 && !selectedFullCategory}
            <div class="mb-12">
                <button
                        class="text-info mb-6 inline-flex items-center hover:underline"
                        on:click={() => { currentTopLevelCategory = null; displayedSubCategories = []; }}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20"
                         fill="currentColor">
                        <path fill-rule="evenodd"
                              d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                              clip-rule="evenodd"/>
                    </svg>
                    Back to All Topics
                </button>
                <h3 class="text-secondary font-orbital font-semibold text-3xl mb-8 text-center">
                    {currentTopLevelCategory} → Select a Specific Category
                </h3>
                <!-- Grid for Sub-Category Cards -->
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-x-4 gap-y-6">
                    {#each displayedSubCategories as subCat (subCat.id)}
                        <div
                                class="category-card cursor-pointer rounded-lg overflow-hidden shadow-lg transition-all duration-300 p-4 flex flex-col items-center justify-center text-center h-32 md:h-36"
                                style="border: 2px solid {getCategoryColor(subCat.name)}; background-color: {getCategoryColor(subCat.name)}20;"
                                on:mouseenter={(e) => handleCategoryHover(e, true)}
                                on:mouseleave={(e) => handleCategoryHover(e, false)}
                                on:click={() => fetchRecipesByFullCategory(subCat, true)}
                                role="button"
                                tabindex="0"
                                on:keypress={(e) => e.key === 'Enter' && fetchRecipesByFullCategory(subCat, true)}
                        >
                            <span class="text-3xl md:text-4xl mb-2">{getCategoryIcon(subCat.name)}</span>
                            <h4 class="text-white font-orbital font-semibold text-sm md:text-base leading-tight">{subCat.name}</h4>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}


        <!-- Search All Categories Section -->
        {#if !selectedFullCategory}
            <div class="mb-12 text-center">
                <h3 class="text-secondary font-orbital font-semibold text-2xl mb-6">Search by Category</h3>

                <!-- Search Input -->
                <div class="relative max-w-lg mx-auto mb-8">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none"
                             viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                    </div>
                    <input
                            type="text"
                            bind:value={categorySearchTerm}
                            placeholder="Type to find a category (e.g., Chicken, Pasta, Vegan)..."
                            class="w-full py-3 pl-10 pr-4 rounded-md bg-gray-700 text-primary border border-gray-600 focus:border-info focus:ring-info"
                    />
                </div>

                {#if isLoadingCategories}
                    <div class="flex justify-center py-4">
                        <div class="animate-spin rounded-full h-10 w-10 border-t-4 border-b-4 border-primary"></div>
                    </div>
                {:else}
                    <!-- Categories Grid with Icon-Style Cards -->
                    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 gap-6 mt-6">
                        {#if filteredAllCategories.length > 0}
                            {#each filteredAllCategories as cat (cat.id)}
                                <!-- Category Card styled like topic icons -->
                                <div
                                        class="category-card cursor-pointer rounded-lg overflow-hidden shadow-lg transition-all duration-300 p-6 flex flex-col items-center justify-center text-center h-36"
                                        style="border: 2px solid {getCategoryColor(cat.name)}; background-color: {getCategoryColor(cat.name)}20;"
                                        on:mouseenter={(e) => handleCategoryHover(e, true)}
                                        on:mouseleave={(e) => handleCategoryHover(e, false)}
                                        on:click={() => fetchRecipesByFullCategory(cat, true)}
                                >
                                    <!-- Category Icon -->
                                    <span class="text-4xl mb-3">{getCategoryIcon(cat.name)}</span>
                                    <h3 class="text-white font-orbital font-bold text-lg">{cat.name}</h3>
                                </div>
                            {/each}
                        {:else if categorySearchTerm}
                            <div class="col-span-full flex flex-col items-center justify-center py-8 text-gray-400">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-3" fill="none"
                                     viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                          d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                </svg>
                                <p class="text-lg">No categories match "{categorySearchTerm}"</p>
                                <button
                                        class="mt-4 text-info hover:underline"
                                        on:click={() => categorySearchTerm = ''}
                                >
                                    Clear search
                                </button>
                            </div>
                        {/if}
                    </div>

                    <!-- Category Count Indicator -->
                    <div class="mt-4 text-gray-400 text-sm">
                        Showing {filteredAllCategories.length} of {allCategories.length} categories
                    </div>
                {/if}
            </div>
        {/if}
    </div>
</section>
<!-- Search All Categories Section - Styled Like Topic Icons -->
{#if selectedFullCategory}
    <section class="selected-category-recipes py-12">
        <div class="container mx-auto px-4">
            <button
                    class="text-info mb-6 inline-flex items-center hover:underline"
                    on:click={() => {
                    selectedFullCategory = null;
                    categoryRecipes = [];
                    // Decide if you want to go back to sub-categories or main topics
                    // If currentTopLevelCategory was set, you might want to keep it
                    // or clear it too: currentTopLevelCategory = null; displayedSubCategories = [];
                }}
            >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd"
                          d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                          clip-rule="evenodd"/>
                </svg>
                Back to Categories
            </button>

            <h2 class="text-primary font-orbital font-bold text-3xl mb-8 text-center">
                Recipes in "{selectedFullCategory.name}"
            </h2>

            {#if isLoadingCategoryRecipes && categoryRecipes.length === 0}
                <div class="flex justify-center items-center py-10">
                    <div class="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-primary"></div>
                    <p class="ml-4 text-primary text-xl">Loading recipes...</p>
                </div>
            {:else if categoryRecipes.length > 0}
                <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                    {#each categoryRecipes as recipe (recipe.id || recipe.name) }
                        <div class="flex justify-center">
                            <InfoBlock
                                    title={recipe.name}
                                    headingClass="text-gray-800 text-2xl text-center font-orbital font-bold"
                                    text={[
                                    recipe.duration ? `Duration: ${recipe.duration}` : "",
                                    recipe.rating ? `Rating: ${recipe.rating}` : "",
                                    recipe.servings ? `${recipe.servings}` : "",
                                ]}
                                    recipe={recipe} fadeInAnimation="fadeIn"
                                    bg="bg-info" expandable={true}
                            />
                        </div>
                    {/each}
                </div>

                <!-- Load More Button -->
                {#if hasMoreRecipes}
                    <div class="text-center mt-10">
                        <button
                                class="button primary-button "
                                on:click={fetchMoreCategoryRecipes}
                                disabled={isLoadingMore}
                        >
                            {isLoadingMore ? 'Loading More...' : 'Load More Recipes'}
                        </button>
                    </div>
                {/if}

            {:else if !isLoadingCategoryRecipes}
                <div class="text-center py-10">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-4 text-gray-400" fill="none"
                         viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <p class="text-gray-500 text-xl">No recipes found in this category.</p>
                    <p class="text-gray-400 mt-2">Try selecting a different category.</p>
                </div>
            {/if}
        </div>
    </section>
{/if}

<div class="container2 spacer layer4"></div>
<style>
    .category-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .category-card:hover {
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    }
</style>