<script lang="ts">
    import {createEventDispatcher, onDestroy} from 'svelte';
    import axios from "axios";
    // import { PUBLIC_API_BASE_URL } from '$env/dynamic/public'; // Import the environment variable

    // 1. Corrected Term type based on usage of item.query
    type Term = { query: string; [key: string]: any }; // Assuming item has a query property

    let searchTerm: string = '';
    let results: Term[] = [];
    let offset: number = 0;
    const pageSize: number = 10;
    let isLoading: boolean = false;
    let canLoadMore: boolean = false;
    let debounceTimer: any = null;
    export let onSearchExecute: (searchTerm: string) => void;
    export let onClearExecute: () => void;

    let showSuggestions: boolean = false;

    const dispatch = createEventDispatcher();


    async function getAutocompleteSuggestions(term: string, currentOffset: number, limit: number): Promise<Term[]> {
        if (!term.trim()) {
            showSuggestions = false; // Hide suggestions if term is empty
            return [];
        }
        isLoading = true;

        // Use a relative path for the API URL so the proxy can pick it up
        const apiUrl = `/api/v1/recipes/${encodeURIComponent(term)}`;

        try {
            // Changed from fetch to axios.post
            // Axios automatically stringifies the params object for query parameters in a POST request if placed in 'params'
            // For POST, the URL path is the main endpoint, query params for size/offset are handled by axios.
            const response = await axios.post<Term[]>(apiUrl, null, { // Send null as body if not needed by POST
                params: { // Query parameters
                    size: limit,
                    offset: currentOffset
                },
                headers: {
                    'Content-Type': 'application/json', // Keep if your backend expects it even for POST without body
                }
            });

            // Axios wraps the response data in `data` property
            const data = response.data;
            showSuggestions = data.length > 0; // Show if results, hide if not
            return data;
        } catch (error) {
            // Axios errors often have a `response` property for server errors (4xx, 5xx)
            if (axios.isAxiosError(error) && error.response) {
                console.error('Failed to fetch autocomplete suggestions:', error.response.statusText, error.response.data);
            } else {
                console.error('Error fetching autocomplete suggestions:', error);
            }
            showSuggestions = false; // Hide on error
            return [];
        } finally {
            isLoading = false;
        }
    }

    function handleItemClick(item: Term) { // item is of type Term
        const clickedQueryText = toTitleCase(item.query);
        searchTerm = clickedQueryText;
        results = [];
        canLoadMore = false;
        showSuggestions = false; // Hide suggestions after selection

        dispatch('itemSelected', { value: clickedQueryText });

        if (onSearchExecute) {
            onSearchExecute(clickedQueryText);
        }
    }

    async function fetchAndProcessResults(isNewSearch: boolean) {
        const currentSearchTerm = searchTerm.trim();
        if (!currentSearchTerm) {
            results = [];
            offset = 0;
            canLoadMore = false;
            isLoading = false;
            showSuggestions = false; // Hide suggestions
            return;
        }

        if (isNewSearch) {
            offset = 0;
            results = [];
            canLoadMore = true;
        }

        if (!canLoadMore || isLoading) {
            return;
        }

        const newResults = await getAutocompleteSuggestions(currentSearchTerm, offset, pageSize);

        if (newResults.length > 0) {
            results = isNewSearch ? newResults : [...results, ...newResults];
            offset++;
            canLoadMore = newResults.length === pageSize;
        } else {
            if (isNewSearch) {
                results = [];
            }
            canLoadMore = false;
        }
        if (results.length > 0 || isLoading) {
            showSuggestions = true;
        }
    }

    function handleInput(event: Event) {
        searchTerm = (event.target as HTMLInputElement).value;
        clearTimeout(debounceTimer);
        if (!searchTerm.trim()) {
            results = [];
            canLoadMore = false;
            showSuggestions = false;
            return;
        }
        debounceTimer = setTimeout(() => {
            fetchAndProcessResults(true);
        }, 300);
    }

    function clearAutocompleteInput() {
        searchTerm = '';
        results = [];
        canLoadMore = false;
        offset = 0;
        showSuggestions = false;
        dispatch('searchTermChange', { value: '' });

        if (onClearExecute) {
            onClearExecute();
        }
        const inputEl = document.querySelector('.autocomplete-input') as HTMLInputElement;
        if(inputEl) inputEl.focus();
    }

    function loadMore() {
        if (canLoadMore && !isLoading) {
            fetchAndProcessResults(false);
        }
    }

    function toTitleCase(str: string): string {
        if (!str) return '';
        return str.replace(/\w\S*/g, function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    onDestroy(() => {
        clearTimeout(debounceTimer);
    });

</script>
<div>
    <div class='flex   justify-center rounded-md'>
        <div class='flex justify-between'>
            <button
                    class=" text-lg border border-primary text-primary hover:bg-primary hover:text-black my-2 mx-1 py-2 px-4 rounded-md transition-all"
                    type="button"
                    id='recipeSearch'
                    on:click={() => onSearchExecute(searchTerm)}>
                Search
            </button>
            <button
                    class=" text-lg border border-primary text-primary hover:bg-primary hover:text-black my-2 mx-1 py-2 px-4 rounded-md transition-all"
                    type="button"
                    id='clear'
                    on:click={clearAutocompleteInput}>
                Clear
            </button>
        </div>
    </div>
    <div class="autocomplete-container">
        <input
                type="text"
                bind:value={searchTerm}
                on:input={handleInput}
                placeholder="Search recipes..."
                class="autocomplete-input w-full p-2 bg-amber-50 rounded focus:outline-none focus:ring focus:ring-[#C62368] focus:border-[#C62368] focus:border-2"
        />

        {#if searchTerm.trim() && showSuggestions && results.length > 0}
            <ul class="autocomplete-results bg-white border-primary rounded-lg border border-gray-200 divide-y divide-gray-200">
                {#each results as item (item.query + Math.random())}
                    <li
                            on:mouseout={(ele) => { (ele.target as HTMLLIElement).classList.remove('bg-gray-100') }}
                            on:mouseenter={(ele) => { (ele.target as HTMLLIElement).classList.add('bg-gray-100') }}
                            on:click={() => handleItemClick(item)}
                            class='px-4 py-2 cursor-pointer autocomplete-item'>
                        {toTitleCase(item.query)}
                    </li>
                {/each}
            </ul>
        {/if}

        {#if isLoading}
            <p class="autocomplete-loading">Loading...</p>
        {/if}

        {#if searchTerm.trim() && !isLoading && showSuggestions && results.length === 0 && !canLoadMore}
            <p class="autocomplete-no-results">No results found.</p>
        {/if}

        {#if canLoadMore && !isLoading && results.length > 0 && showSuggestions}
            <button on:click={loadMore} class="autocomplete-load-more">
                Load More
            </button>
        {/if}
    </div>
</div>
<style lang="css">
    .autocomplete-container {
        position: relative;
        width: 300px; /* Adjust as needed */
    }
    .autocomplete-input {
        width: 100%;
        padding: 8px;
        font-size: 16px;
        box-sizing: border-box;
    }
    .autocomplete-results {
        list-style-type: none;
        padding: 0;
        margin: 0;
        border: 1px solid #ccc;
        border-top: none;
        max-height: 200px; /* Adjust as needed */
        overflow-y: auto;
        /*position: absolute;*/
        width: 100%;
        z-index: 10;
        background-color: white; /* Ensure it has a background */
    }
    .autocomplete-item {
        padding: 8px;
        cursor: pointer;
    }
    .autocomplete-item:hover {
        background-color: #f0f0f0;
    }
    .autocomplete-loading, .autocomplete-no-results {
        padding: 8px;
        color: #666;
    }
    .autocomplete-load-more {
        display: block;
        width: 100%;
        padding: 10px;
        margin-top: 5px;
        background-color: #007bff;
        color: white;
        border: none;
        cursor: pointer;
        text-align: center;
    }
    .autocomplete-load-more:hover {
        background-color: #0056b3;
    }
    .autocomplete-load-more:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }
</style>