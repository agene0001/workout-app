<script>
    import { onMount } from 'svelte';
    import InfoBlock from '$lib/components/InfoBlock.svelte';
    import axios from 'axios';

    // State variables
    let querySearch = '';
    let searchedRecipes = [];
    let recipes = [];
    let searchedRecipe = null;
    let recommendedRecipes = [];

    // Helper function to convert string to title case
    function toTitleCase(str) {
        return str.replace(/\w\S*/g, function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    // Fetch initial recipes on component mount
    onMount(async () => {
        try {
            const res = await axios.get('/api/v1/recipes/10');
            console.log('Response data:', res.data);
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
            searchedRecipes = promise.data;
        } catch {
            searchedRecipes = [];
        }
    }

    // Watch for querySearch changes
    $: {
        getQuery(querySearch);
    }

    // Search recipe function
    async function searchRecipe() {
        console.log("Query: " + querySearch);
        console.log("Searched Recipe: " + searchedRecipe?.name);

        try {
            const res = await axios.get(`/api/v1/recipes/recipe/${encodeURIComponent(querySearch)}`);
            console.log(res.data);
            searchedRecipe = res.data;

            const recRes = await axios.get(`api/v1/recipes/recommendations?query=${encodeURIComponent(querySearch)}&ingredients=${res.data?.ingredients}`);
            console.log(recRes.data);
            recommendedRecipes = recRes.data;
        } catch (err) {
            console.error("Error fetching recipe:", err);
        }
    }

    // Clear function
    function clearSearch() {
        recommendedRecipes = [];
        querySearch = '';
        searchedRecipe = null;
    }
</script>

<div class='heroback py-8 w-full mx-auto' id='nutrition-header'>
    <div class="h-16"></div>
    <h1 class='text-primary font-orbital font-bold text-4xl py-5 my-5 text-center'>Search for Personalized Recipes shipped right to your door</h1>

    <h3 class="text-primary text-3xl font-orbital font-bold text-center">Search for recipes from our personalized catalogue</h3>

    <!-- Recipe Components -->
    <div class="wrapper w-full">
        {#each recipes as recipe, index}
            <div class={`item item${index + 1}`} >
                <InfoBlock
                        title={recipe.name}
                        headingClass="text-gray-800 text-2xl text-center font-orbital font-bold"
                        text={[
                        recipe.duration ? `Duration: ${recipe.duration}` : "",
                        recipe.rating ? `Rating: ${recipe.rating}` : "",
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

        {#if searchedRecipe !== null}
            <InfoBlock
                    bg='bg-[#faebd7] w-1/3'
                    title={searchedRecipe.name}
                    headingClass="text-gray-800 text-2xl font-orbital font-bold text-center"
                    recipe={searchedRecipe}
                    text={[]}
                    expandable={true}
            />
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
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5 justify-center">
            {#each recommendedRecipes as recipe, index}
                <div class="flex justify-center">
                    <InfoBlock
                            title={recipe.name}
                            headingClass="text-gray-800 text-2xl font-orbital font-bold text-center"
                            text={[
                            recipe.duration ? `Duration: ${recipe.duration}` : "",
                            recipe.rating ? `Rating: ${recipe.rating}` : "",
                        ]}
                            recipe={recipe}
                            fadeInAnimation="fadeIn"
                            bg="bg-info"
                            expandable={true}
                    />
                </div>
            {/each}
        </div>
    {/if}
</div>