<script>
    import {onMount} from 'svelte';
    import InfoBlock from '$lib/components/InfoBlock.svelte';
    import axios from 'axios';

    // State variables
    let querySearch = '';
    let searchedRecipes = [];
    let recipes = [];
    let searchedRecipeArray = null; // Array of recipes with the same name
    let recommendedRecipes = [];

    // Helper function to convert string to title case


    // Fetch initial recipes on component mount
    onMount(async () => {
        try {
            const res = await axios.get('/api/v1/recipes/10');
            console.log('Response data:', res.data);
            console.log('Response status:', res.data.length);
            recipes = res.data;
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

    // Search recipe function
    async function searchRecipe() {
        console.log("Query: " + querySearch);

        try {
            const res = await axios.get(`/api/v1/recipes/recipe/${encodeURIComponent(querySearch)}`);
            console.log("Recipe search response:", res.data);

            // Store the array of recipes with the same name
            searchedRecipeArray = res.data;

            if (searchedRecipeArray && searchedRecipeArray.length > 0) {
                // Use the first recipe for recommendations
                const firstRecipe = searchedRecipeArray[0];

                // Extract ingredients from the currently selected recipe
                const ingredientsParam = Array.isArray(firstRecipe.ingredients)
                    ? firstRecipe.ingredients.join(',')
                    : firstRecipe.ingredients;

                const recRes = await axios.get(
                    `api/v1/recipes/recommendations?query=${encodeURIComponent(querySearch)}&ingredients=${ingredientsParam}`
                );
                console.log("Recommendation response:", recRes.data);
                recommendedRecipes = recRes.data;
            }
        } catch (err) {
            console.error("Error fetching recipe:", err);
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

    // Add these to your existing state variables
    let categories = [
        {name: 'Breakfast', icon: '🍳', color: '#FF9E00', image: '/api/placeholder/300/200'},
        {name: 'Lunch', icon: '🥪', color: '#4CAF50', image: '/api/placeholder/300/200'},
        {name: 'Dinner', icon: '🍽️', color: '#2196F3', image: '/api/placeholder/300/200'},
        {name: 'Dessert', icon: '🍰', color: '#E91E63', image: '/api/placeholder/300/200'},
        {name: 'Vegetarian', icon: '🥗', color: '#8BC34A', image: '/api/placeholder/300/200'},
        {name: 'Quick & Easy', icon: '⏱️', color: '#FF5722', image: '/api/placeholder/300/200'},
        {name: 'Comfort Food', icon: '🍲', color: '#795548', image: '/api/placeholder/300/200'},
        {name: 'Healthy', icon: '💪', color: '#00BCD4', image: '/api/placeholder/300/200'}
    ];

    let selectedCategory = null;
    let categoryRecipes = [];
    let isLoadingCategory = false;
    let activeTab = 'popular'; // 'popular' or 'recent'
    let isLoadingMore = false; // Loading state for "Show More"
    let currentPage = 0; // Track the current page for the selected category
    const pageSize = 6; // Number of recipes to fetch per page
    let hasMoreRecipes = false; // Flag to check if more recipes might exist

    // Function to fetch recipes by category
    async function fetchInitialRecipesByCategory(category) {
        isLoadingCategory = true;
        selectedCategory = category;
        categoryRecipes = []; // Reset recipes when category changes
        currentPage = 0; // Reset page number
        hasMoreRecipes = false; // Reset flag

        try {
            const response = await axios.get(
                `/api/v1/recipes/category/${encodeURIComponent(category.name.toLowerCase())}?page=${currentPage}&pageSize=${pageSize}`
            );
            categoryRecipes = response.data || [];
            // Assume more recipes exist if we received a full page
            hasMoreRecipes = response.data && response.data.length === pageSize;
        } catch (err) {
            console.error(`Error fetching initial ${category.name} recipes:`, err);
            categoryRecipes = [];
            hasMoreRecipes = false;
        } finally {
            isLoadingCategory = false;
        }
    }

    // Function to fetch the NEXT page of recipes
    async function fetchMoreRecipes() {
        if (isLoadingMore || !selectedCategory || !hasMoreRecipes) return; // Prevent multiple loads or loading when done

        isLoadingMore = true;
        currentPage++; // Go to the next page

        try {
            const response = await axios.get(
                `/api/v1/recipes/category/${encodeURIComponent(selectedCategory.name.toLowerCase())}?page=${currentPage}&pageSize=${pageSize}`
            );
            const newRecipes = response.data || [];
            console.log("New recipes:", newRecipes);
            console.log("Current recipes:", categoryRecipes);
            categoryRecipes = [...categoryRecipes, ...newRecipes]; // Append new recipes
            // Update flag based on the new response
            hasMoreRecipes = newRecipes.length === pageSize;
        } catch (err) {
            console.error(`Error fetching more ${selectedCategory.name} recipes:`, err);
            // Optionally revert page number or handle error state
            currentPage--;
        } finally {
            isLoadingMore = false;
        }
    }

    // async function fetchRecipesByCategory(category) {
    //     isLoadingCategory = true;
    //     selectedCategory = category;
    //
    //     try {
    //         // In a real implementation, this would call your API with the category
    //         // For now, we'll simulate a delay and return dummy data
    //         await new Promise(resolve => setTimeout(resolve, 500));
    //
    //         // This would be replaced with your actual API call
    //         const response = await axios.get(`/api/v1/recipes/category/${encodeURIComponent(category.name.toLowerCase())}`);
    //
    //         // This is just a fallback in case the API call fails or returns no data
    //         categoryRecipes = response.data || [
    //             {
    //                 name: `${category.name} Recipe 1`,
    //                 duration: '30 mins',
    //                 rating: '4.7',
    //                 description: `A delicious ${category.name.toLowerCase()} recipe that's quick to make.`,
    //                 image: '/api/placeholder/400/300'
    //             },
    //             {
    //                 name: `${category.name} Recipe 2`,
    //                 duration: '45 mins',
    //                 rating: '4.5',
    //                 description: `Perfect ${category.name.toLowerCase()} for any occasion.`,
    //                 image: '/api/placeholder/400/300'
    //             },
    //             {
    //                 name: `${category.name} Recipe 3`,
    //                 duration: '25 mins',
    //                 rating: '4.8',
    //                 description: `Everyone's favorite ${category.name.toLowerCase()} recipe.`,
    //                 image: '/api/placeholder/400/300'
    //             }
    //         ];
    //     } catch (err) {
    //         console.error(`Error fetching ${category.name} recipes:`, err);
    //         categoryRecipes = [];
    //     } finally {
    //         isLoadingCategory = false;
    //     }
    // }

    function changeTab(tab) {
        activeTab = tab;
        // In a real implementation, you might want to re-fetch or re-sort recipes based on the active tab
    }
    function toTitleCase(str) {
        return str.replace(/\w\S*/g, function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
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

        <div class='flex justify-center rounded-md'>
            <div class='w-1/2 flex justify-between'>
                <button
                        class="w-1/2 text-lg border border-primary text-primary hover:bg-primary hover:text-black my-2 mx-1 py-2 px-4 rounded-md transition-all"
                        type="submit"
                        id='recipeSearch'
                        on:click={searchRecipe}>
                    Search
                </button>
                <button
                        class="w-1/2 text-lg border border-primary text-primary hover:bg-primary hover:text-black my-2 mx-1 py-2 px-4 rounded-md transition-all"
                        type="submit"
                        id='clear'
                        on:click={clearSearch}>
                    Clear
                </button>
            </div>
        </div>

        <div class='flex justify-center'>
            <div class='w-1/2 mb-3'>
                <input
                        class="w-full p-2 border-4 border-[#00A76E] bg-amber-50 rounded focus:outline-none focus:ring focus:ring-[#C62368] focus:border-[#C62368]"
                        id='navSearch'
                        type="search"
                        placeholder="Search"
                        bind:value={querySearch}
                        aria-label="Search"
                />
            </div>
        </div>
    </div>

    {#if searchedRecipes.length > 0}
        <div class='flex justify-center'>
            <div class='w-1/2'>
                <ul class="bg-white border-primary rounded-lg border border-gray-200 divide-y divide-gray-200">
                    {#each searchedRecipes as val, ind}
                        <li
                                on:mouseout={(ele) => {
                                ele.target.classList.remove('bg-gray-100')
                            }}
                                on:mouseenter={(ele) => {
                                ele.target.classList.add('bg-gray-100')
                            }}
                                on:click={(ele) => {
                                querySearch = ele.target.innerText

                                searchRecipe()
                            }}
                                class='px-4 py-2 cursor-pointer'>
                            {toTitleCase(val.query)}
                        </li>
                    {/each}
                </ul>
            </div>
        </div>
    {/if}

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

<!-- Spotify-inspired Category Browse Section -->
<section class="category-browse py-16 ">
    <div class="container mx-auto px-4">
        <div class="text-center mb-12">
            <h2 class="text-primary font-orbital font-bold text-4xl mb-3">Explore Recipe Categories</h2>
            <p class="text-gray-600 text-xl max-w-2xl mx-auto">
                Find the perfect dish by browsing our delicious recipe categories
            </p>
        </div>

        <!-- Category Cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            {#each categories as category}
                <div
                        class="category-card cursor-pointer rounded-lg overflow-hidden shadow-lg transition-all duration-300"
                        style="border: 2px solid {category.color};"
                        on:mouseenter={(e) => handleCategoryHover(e, true)}
                        on:mouseleave={(e) => handleCategoryHover(e, false)}
                        on:click={() => fetchInitialRecipesByCategory(category)}>
                <div class="relative h-40">
                    <div
                            class="absolute inset-0 flex items-center justify-center"
                            style="background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6));"
                    >
                        <div class="text-center">
                            <span class="text-4xl">{category.icon}</span>
                            <h3 class="text-white font-orbital font-bold text-2xl mt-2">{category.name}</h3>
                        </div>
                    </div>
                </div>
                </div>
            {/each}
        </div>
    </div>
</section>

<!-- Selected Category Results Section -->
{#if selectedCategory}
    <section class="category-results py-12 ">
        <div class="container mx-auto px-4">
            <div class="flex items-center justify-between mb-8">
                <h2 class="text-primary font-orbital font-bold text-3xl">
                    <span class="mr-2">{selectedCategory.icon}</span>
                    {selectedCategory.name} Recipes
                </h2>
                <!-- Optional: Add sorting/filtering controls here -->
            </div>

            {#if isLoadingCategory}
                <!-- Initial Loading Spinner -->
                <div class="flex justify-center py-12">
                    <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-primary"></div>
                </div>
            {:else if categoryRecipes.length === 0}
                <!-- No Recipes Found Message -->
                <div class="text-center py-12">
                    <p class="text-gray-500 text-lg">No recipes found for this category.</p>
                </div>
            {:else}
                <!-- Recipe Cards Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                    {#each categoryRecipes as recipe (recipe.id || recipe.name)}
                        <InfoBlock
                                title={recipe.name}
                                headingClass="text-gray-800 text-2xl text-center font-orbital font-bold"
                                text={[
                                    recipe.rating ? `⭐ ${recipe.rating}` : "",
                                ]}
                                recipe={recipe}
                                fadeInAnimation="fadeIn"
                                bg="bg-[#3E92CC]"
                                expandable={true}
                        />
                    {/each}
                </div>

                <!-- Show More Button Area -->
                <div class="text-center mt-12">
                    {#if isLoadingMore}
                        <!-- Loading More Spinner -->
                        <div class="flex justify-center py-4">
                            <div class="animate-spin rounded-full h-10 w-10 border-t-4 border-b-4 border-primary"></div>
                        </div>
                    {:else if hasMoreRecipes}
                        <!-- Show More Button -->
                        <button
                                on:click={fetchMoreRecipes}
                                class="bg-danger  text-white font-bold py-3 px-6 rounded-full transition duration-300 ease-in-out transform hover:scale-105 shadow-md"
                                disabled={isLoadingMore}
                        >
                            Show More Recipes
                        </button>
                    {/if}
                    {#if !isLoadingMore && !hasMoreRecipes && categoryRecipes.length > 0}
                        <!-- Optional: Message when all recipes are loaded -->
                        <p class="text-gray-500 mt-4">You've reached the end!</p>
                    {/if}
                </div>
            {/if}
        </div>
    </section>
{/if}

<style>
    .category-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .category-card:hover {
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    }

    /* For recipe card text truncation */
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
</style>
<div class="container2 spacer layer4"></div>