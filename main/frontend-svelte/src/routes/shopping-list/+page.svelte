<script lang="ts">
    import { cart, type CartItem, type CartRecipeBatchItem, type CartCustomStandaloneIngredient } from '$lib/stores/cartStore';
    // Use your existing Firebase client stores and functions
    import { currentUser as fbUserStore, isInitialized as fbIsInitialized } from '$lib/firebase/firebase.client';
    import {
        saveNewShoppingList,
        updateShoppingList,
        getUserShoppingLists,
        deleteShoppingList,
        type SavedShoppingList
    } from '$lib/shoppingListDB';

    import axios from 'axios';
    import { onMount, tick } from 'svelte';
    import type { User } from 'firebase/auth';

    let itemsInCart: CartItem[] = [];

    let newItemName = '';
    let newItemQuantity: number | null = 1;
    let newItemUnit = 'each';

    let instacartShoppingListUrl: string | null = null;
    let instacartShoppingListLoading = false;
    let instacartShoppingListError: string | null = null;
    let shoppingListTitle = "My Shopping List"; // Name of the current list

    let showClearConfirm = false;

    // Firebase related state
    let activeUser: User | null = null; // Local variable to hold the current user from the store
    let savedUserLists: SavedShoppingList[] = [];
    let activeListId: string | null = null; // ID of the currently loaded list from Firebase
    let isListDirty = false; // True if current list (items or title) has changes not saved
    let isLoadingSavedLists = false;
    let isSavingList = false;

    let showLoadListModal = false;
    let initialLoadedTitle = ""; // For tracking title changes specifically

    const predefinedUnits = [
        'cup','fl oz','gallon','milliliter','liter','pint','quart','tablespoon','teaspoon',
        'gram','kilogram','lb','ounce','pound',
        'bunch','can','each','ear','head','large','medium','package','packet','small','small ears','small head',
    ].sort();

    let unsubscribeCartStore: () => void;
    let unsubscribeFbUserStore: () => void;

    onMount(async () => {
        unsubscribeCartStore = cart.subscribe(value => {
            const prevCartString = JSON.stringify(itemsInCart);
            itemsInCart = value;
            if (activeListId && JSON.stringify(value) !== prevCartString && prevCartString !== '[]') {
                isListDirty = true;
            } else if (!activeListId && value.length > 0 && prevCartString === '[]') {
                isListDirty = true;
            } else if (!activeListId && value.length > 0 && JSON.stringify(value) !== prevCartString) {
                isListDirty = true;
            }
            clearInstacartLinkState();
        });

        unsubscribeFbUserStore = fbUserStore.subscribe(user => {
            activeUser = user;
            if (user) {
                if ($fbIsInitialized) {
                    fetchUserShoppingLists();
                }
            } else {
                savedUserLists = [];
                activeListId = null;
                isListDirty = itemsInCart.length > 0;
                shoppingListTitle = "My Shopping List";
                initialLoadedTitle = shoppingListTitle;
            }
        });

        if ($fbIsInitialized && $fbUserStore) {
            activeUser = $fbUserStore;
            fetchUserShoppingLists();
        }

        if (!activeListId && itemsInCart.length > 0) {
            initialLoadedTitle = shoppingListTitle;
            isListDirty = true;
        }

        return () => {
            unsubscribeCartStore?.();
            unsubscribeFbUserStore?.();
        };
    });


    $: if (activeListId && shoppingListTitle !== initialLoadedTitle && initialLoadedTitle !== "") {
        isListDirty = true;
    }

    function handleAddCustomItem() {
        if (newItemName.trim() && newItemQuantity && newItemQuantity > 0) {
            cart.addCustomIngredient(newItemName, newItemQuantity, newItemUnit || 'each');
            newItemName = '';
            newItemQuantity = 1;
            newItemUnit = 'each';
        }
    }

    function handleRemoveItem(itemId: string) {
        cart.removeItem(itemId);
    }

    function handleUpdateRecipeServings(itemId: string, event: Event) {
        const input = event.target as HTMLInputElement;
        const servings = parseInt(input.value, 10);
        if (!isNaN(servings)) {
            if (servings <= 0) {
                cart.removeItem(itemId);
            } else {
                cart.updateRecipeServings(itemId, servings);
            }
        }
    }

    function handleUpdateCustomItemDetail(itemId: string, field: 'name' | 'quantity' | 'unit', event: Event) {
        const input = event.target as HTMLInputElement | HTMLSelectElement;
        let value: string | number = input.value;
        if (field === 'quantity') value = parseFloat(input.value);

        const currentItem = itemsInCart.find(i => i.id === itemId && i.type === 'custom_standalone_ingredient') as CartCustomStandaloneIngredient | undefined;
        if (currentItem) {
            const updatedDetails: Partial<Omit<CartCustomStandaloneIngredient, 'id' | 'type'>> = {
                name: field === 'name' ? String(value) : currentItem.name,
                quantity: field === 'quantity' && Number(value) > 0 ? Number(value) : currentItem.quantity,
                unit: field === 'unit' ? String(value) : currentItem.unit,
            };
            cart.updateCustomIngredient(itemId, updatedDetails);
        }
    }

    function clearInstacartLinkState() {
        instacartShoppingListUrl = null;
        instacartShoppingListError = null;
    }

    async function generateMasterInstacartList() {
        instacartShoppingListLoading = true;
        clearInstacartLinkState();
        const cartDataForBackend = cart.getCartDataForBackend();
        if (cartDataForBackend.length === 0) {
            instacartShoppingListError = "Your cart is empty. Add some items first!";
            instacartShoppingListLoading = false;
            return;
        }
        try {
            const response = await axios.post('/recipes/process-recipe', {
                title: shoppingListTitle.trim() || "My Shopping List",
                link_type: 'shopping_list',
                ingredients: cartDataForBackend,
            });

            if (response.data && response.data.response && response.data.response.products_link_url) {
                instacartShoppingListUrl = response.data.response.products_link_url;
            } else if (response.data && response.data.response && response.data.response.error) {
                instacartShoppingListError = `Instacart API Error: ${response.data.response.error}`;
                if(response.data.response.details) instacartShoppingListError += ` Details: ${JSON.stringify(response.data.response.details)}`;
            }
            else if (response.data && response.data.error) {
                instacartShoppingListError = response.data.error;
            }
            else {
                instacartShoppingListError = "Failed to generate shopping list link. Unexpected response from server.";
            }

        } catch (error: any) {
            console.error("Error generating master shopping list:", error);
            const errorData = error.response?.data;
            if (errorData?.response?.details?.errors && Array.isArray(errorData.response.details.errors)) {
                instacartShoppingListError = errorData.response.details.errors.map((e: any) => `${e.message} (field: ${e.meta?.key || 'N/A'})`).join('; ');
            } else if (errorData?.response?.error) {
                instacartShoppingListError = `API Error: ${errorData.response.error}`;
            } else if (errorData?.error) {
                instacartShoppingListError = `Server Error: ${errorData.error}`;
            }
            else {
                instacartShoppingListError = "An unexpected error occurred while generating the shopping list.";
            }
        } finally {
            instacartShoppingListLoading = false;
        }
    }

    function confirmClearCart() { showClearConfirm = true; }
    function executeClearCart() {
        cart.clear();
        showClearConfirm = false;
        if (!activeListId) {
            isListDirty = false;
            shoppingListTitle = "My Shopping List";
            initialLoadedTitle = shoppingListTitle;
        } else {
            isListDirty = true;
        }
    }
    function toTitleCase(str: string | undefined | null): string {
        if (!str) return '';
        return str.replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
    }

    // --- List Management Functions ---
    async function confirmDiscardChanges(): Promise<boolean> {
        if (isListDirty && itemsInCart.length > 0) {
            return window.confirm("You have unsaved changes. Are you sure you want to discard them?");
        }
        return true;
    }

    async function handleNewList() {
        if (!(await confirmDiscardChanges())) return;

        cart.setList([]);
        shoppingListTitle = "My New Shopping List";
        activeListId = null;
        isListDirty = false;
        initialLoadedTitle = shoppingListTitle;
        clearInstacartLinkState();
    }

    async function handleSaveCurrentList() {
        if (!activeUser) {
            alert("Please sign in to save your list.");
            return;
        }
        if (itemsInCart.length === 0 && !activeListId) {
            alert("Add some items to your list before saving.");
            return;
        }
        if (isSavingList) return;
        if (!isListDirty && activeListId) {
            alert("No changes to save.");
            return;
        }

        isSavingList = true;
        try {
            let successOperation = false;
            if (activeListId) {
                successOperation = await updateShoppingList(activeListId, shoppingListTitle, itemsInCart);
            } else {
                const newId = await saveNewShoppingList(activeUser.uid, shoppingListTitle, itemsInCart);
                if (newId) {
                    activeListId = newId;
                    await fetchUserShoppingLists();
                    successOperation = true;
                }
            }

            if (successOperation) {
                isListDirty = false;
                initialLoadedTitle = shoppingListTitle;
                alert("List saved successfully!");
            } else {
                alert("Failed to save list. Please try again.");
            }
        } catch (error) {
            console.error("Error saving list:", error);
            alert("An error occurred while saving the list. See console for details.");
        } finally {
            isSavingList = false;
        }
    }

    async function fetchUserShoppingLists() {
        if (!activeUser || !$fbIsInitialized) return;
        isLoadingSavedLists = true;
        try {
            savedUserLists = await getUserShoppingLists(activeUser.uid);
        } catch (error) {
            console.error("Error fetching user lists:", error);
        } finally {
            isLoadingSavedLists = false;
        }
    }

    async function loadList(listToLoad: SavedShoppingList) {
        if (!(await confirmDiscardChanges())) return;

        cart.setList(listToLoad.items);
        shoppingListTitle = listToLoad.name;
        activeListId = listToLoad.id;
        isListDirty = false;
        initialLoadedTitle = listToLoad.name;
        showLoadListModal = false;
        clearInstacartLinkState();
        await tick();
    }

    async function handleDeleteList(listIdToDelete: string, listNameToDelete: string) {
        if (!activeUser) return;
        if (!confirm(`Are you sure you want to delete the list "${listNameToDelete}"? This cannot be undone.`)) {
            return;
        }
        try {
            const success = await deleteShoppingList(listIdToDelete);
            if (success) {
                if (activeListId === listIdToDelete) {
                    await handleNewList();
                }
                await fetchUserShoppingLists();
                alert("List deleted successfully.");
            } else {
                alert("Failed to delete list.");
            }
        } catch (error) {
            console.error("Error deleting list:", error);
            alert("Failed to delete list.");
        }
    }

</script>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-slate-100">
    <div class="container mx-auto px-4 py-8">
        <div class="text-center mb-6">
            <h1 class="text-5xl font-bold bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent mb-2">
                🛒 My Shopping Lists
            </h1>
            <p class="text-slate-400 text-lg">Organize ingredients, save lists, and generate Instacart links.</p>
        </div>

        <!-- Auth State & List Management Controls -->
        <div class="mb-8 p-4 bg-slate-800/70 backdrop-blur-sm rounded-xl border border-slate-700/50">
            {#if !$fbIsInitialized}
                <p class="text-center text-slate-400">Initializing...</p>
            {:else if $fbUserStore}
                <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
                    <p class="text-sm text-slate-300">Signed in as: <span class="font-semibold text-emerald-400">{$fbUserStore.displayName || $fbUserStore.email}</span></p>
                    <div class="flex gap-2 flex-wrap justify-center">
                        <button on:click={handleNewList} class="btn-secondary text-sm px-3 py-1.5">➕ New List</button>
                        <button on:click={() => showLoadListModal = true} class="btn-secondary text-sm px-3 py-1.5" disabled={isLoadingSavedLists}>
                            {#if isLoadingSavedLists}Loading...{:else}📂 Load List{/if}
                        </button>
                        <button
                                on:click={handleSaveCurrentList}
                                disabled={isSavingList || ($fbUserStore && !isListDirty && !!activeListId) || (!$fbUserStore && itemsInCart.length === 0) || (itemsInCart.length === 0 && !activeListId) }
                                class="btn-primary text-sm px-3 py-1.5"
                                title={!$fbUserStore ? "Sign in to save" : (!isListDirty && !!activeListId ? "No changes to save" : (itemsInCart.length === 0 && !activeListId ? "Add items to save" : "Save current list"))}
                        >
                            {#if isSavingList}Saving...{:else}💾 Save Current List{/if}
                            {#if isListDirty && activeListId && $fbUserStore} <span class="text-xs opacity-70">(unsaved)</span>{/if}
                        </button>
                    </div>
                </div>
                {#if activeListId && $fbUserStore}
                    <p class="text-xs text-center mt-2 text-slate-500">Editing: <span class="font-medium text-slate-400">{shoppingListTitle}</span>{isListDirty ? ' (unsaved changes)' : ''}</p>
                {:else if itemsInCart.length > 0 && $fbUserStore}
                    <p class="text-xs text-center mt-2 text-slate-500">Working on <span class="font-medium text-slate-400">{shoppingListTitle}</span> {isListDirty ? ' (unsaved)' : ''}</p>
                {:else if itemsInCart.length > 0 && !$fbUserStore}
                    <p class="text-xs text-center mt-2 text-slate-500">Current list (Sign in to save)</p>
                {/if}
            {:else} <!-- Not signed in, Firebase initialized -->
                <div class="text-center">
                    <p class="text-slate-300 mb-3">Sign in to save and manage multiple shopping lists.</p>
                </div>
            {/if}
        </div>

        <!-- Current Shopping List Title -->
        <div class="mb-6 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6">
            <label for="shoppingListTitleInput" class="block text-lg font-semibold text-emerald-400 mb-2">Current List Name:</label>
            <input
                    type="text"
                    id="shoppingListTitleInput"
                    bind:value={shoppingListTitle}
                    class="w-full bg-slate-700/50 text-white border-0 rounded-lg px-4 py-3 focus:ring-2 focus:ring-emerald-400 placeholder-slate-400 text-xl"
                    placeholder="e.g., Weekly Groceries"
            >
            {#if isListDirty && shoppingListTitle !== initialLoadedTitle && $fbUserStore && activeListId}
                <p class="text-xs text-amber-400 mt-1">Name changed. Save to update.</p>
            {/if}
        </div>

        <!-- Main content: Empty State or Items -->
        {#if itemsInCart.length === 0}
            <div class="text-center py-16">
                <div class="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-12 border border-slate-700/50 max-w-md mx-auto">
                    <div class="text-6xl mb-6">🛒</div>
                    <h2 class="text-2xl font-semibold text-slate-300 mb-4">Your active list is empty</h2>
                    {#if !$fbIsInitialized}
                        <p class="text-slate-400 mb-6">Connecting...</p>
                    {:else if $fbUserStore}
                        <p class="text-slate-400 mb-6">Add items, or load an existing list.</p>
                        <button on:click={() => showLoadListModal = true} class="btn-secondary mb-3" disabled={isLoadingSavedLists}>
                            {#if isLoadingSavedLists}Loading...{:else}📂 Load Saved List{/if}
                        </button>
                    {:else}
                        <p class="text-slate-400 mb-6">Add recipes or custom items. <a href="/auth/login" class="text-emerald-400 hover:underline">Sign in</a> to save lists.</p>
                    {/if}
                    <a href="/Nutrition" class="inline-flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 text-white px-6 py-3 rounded-xl font-medium transition-all duration-200 transform hover:scale-105">
                        <span>Browse Recipes</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    </a>
                </div>
            </div>
        {:else}
            <!-- Cart Items Display -->
            <div class="grid gap-6 mb-8">
                {#each itemsInCart as item (item.id)}
                    <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6 hover:bg-slate-700/50 transition-all duration-200">
                        {#if item.type === 'recipe_batch'}
                            {@const recipeBatchItem = item as CartRecipeBatchItem}
                            <div class="flex flex-col lg:flex-row gap-4">
                                <div class="flex items-center gap-4 flex-1">
                                    {#if recipeBatchItem.recipe.recipeImgSrc}
                                        <img src={recipeBatchItem.recipe.recipeImgSrc} alt={recipeBatchItem.recipe.recipeName} class="w-20 h-20 object-cover rounded-xl">
                                    {:else}
                                        <div class="w-20 h-20 bg-gradient-to-br from-emerald-500/20 to-blue-500/20 rounded-xl flex items-center justify-center"><span class="text-2xl">🍽️</span></div>
                                    {/if}
                                    <div>
                                        <h3 class="text-xl font-semibold text-emerald-400 mb-1">{toTitleCase(recipeBatchItem.recipe.recipeName)}</h3>
                                        <p class="text-slate-400 text-sm">Recipe ingredients</p>
                                    </div>
                                </div>
                                <div class="flex items-center gap-3 lg:gap-4">
                                    <div class="flex items-center gap-2 bg-slate-700/50 rounded-lg px-3 py-2">
                                        <label for="servings-{recipeBatchItem.id}" class="text-sm text-slate-300 whitespace-nowrap">Servings:</label>
                                        <input type="number" id="servings-{recipeBatchItem.id}" value={recipeBatchItem.servingsMultiplier} min="0" on:change={(e) => handleUpdateRecipeServings(recipeBatchItem.id, e)} class="w-16 bg-slate-600 text-white rounded-md text-center text-sm border-0 focus:ring-2 focus:ring-emerald-400">
                                    </div>
                                    <button on:click={() => handleRemoveItem(recipeBatchItem.id)} class="p-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-colors" title="Remove Recipe">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                    </button>
                                </div>
                            </div>
                            <details class="mt-4 group">
                                <summary class="cursor-pointer text-slate-400 hover:text-slate-300 text-sm flex items-center gap-2 transition-colors">
                                    <svg class="w-4 h-4 transform group-open:rotate-90 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                                    View Raw Ingredients ({recipeBatchItem.recipe.ingredients.length})
                                </summary>
                                <div class="mt-3 p-4 bg-slate-700/30 rounded-lg border border-slate-600/30">
                                    <div class="grid gap-1">
                                        {#each recipeBatchItem.recipe.ingredients as ingStr}
                                            <div class="text-sm text-slate-400 flex items-start gap-2"><span class="text-emerald-400 mt-1">•</span><span>{ingStr}</span></div>
                                        {/each}
                                    </div>
                                </div>
                            </details>
                        {:else if item.type === 'custom_standalone_ingredient'}
                            {@const customItem = item as CartCustomStandaloneIngredient }
                            <div class="flex flex-col sm:flex-row items-stretch gap-3">
                                <div class="flex-1">
                                    <input type="text" value={customItem.name} on:change={(e) => handleUpdateCustomItemDetail(customItem.id, 'name', e)} placeholder="Item Name" class="w-full bg-slate-700/50 text-white border-0 rounded-lg px-4 py-3 focus:ring-2 focus:ring-emerald-400 placeholder-slate-400">
                                </div>
                                <div class="flex gap-3 sm:w-auto">
                                    <input type="number" value={customItem.quantity} min="0.1" step="0.1" on:change={(e) => handleUpdateCustomItemDetail(customItem.id, 'quantity', e)} placeholder="Qty" class="w-24 bg-slate-700/50 text-white border-0 rounded-lg px-3 py-3 text-center focus:ring-2 focus:ring-emerald-400 placeholder-slate-400">
                                    <select value={customItem.unit} on:change={(e) => handleUpdateCustomItemDetail(customItem.id, 'unit', e)} class="w-32 bg-slate-700/50 text-white border-0 rounded-lg px-3 py-3 focus:ring-2 focus:ring-emerald-400">
                                        {#each predefinedUnits as unit} <option value={unit}>{unit}</option> {/each}
                                    </select>
                                    <button on:click={() => handleRemoveItem(customItem.id)} class="p-3 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-colors" title="Remove Item">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                    </button>
                                </div>
                            </div>
                        {/if}
                    </div>
                {/each}
            </div>

            <!-- Add Custom Item Form -->
            <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6 mb-8">
                <h3 class="text-2xl font-semibold text-emerald-400 mb-6 flex items-center gap-2"><span>➕</span> Add Custom Item</h3>
                <form on:submit|preventDefault={handleAddCustomItem} class="flex flex-col lg:flex-row gap-4">
                    <div class="flex-1">
                        <label for="newItemName" class="block text-sm font-medium text-slate-300 mb-2">Item Name</label>
                        <input type="text" id="newItemName" bind:value={newItemName} placeholder="e.g., Olive Oil" class="w-full bg-slate-700/50 text-white border-0 rounded-lg px-4 py-3 focus:ring-2 focus:ring-emerald-400 placeholder-slate-400" required>
                    </div>
                    <div class="flex gap-4">
                        <div>
                            <label for="newItemQuantity" class="block text-sm font-medium text-slate-300 mb-2">Quantity</label>
                            <input type="number" id="newItemQuantity" bind:value={newItemQuantity} min="0.1" step="0.1" placeholder="1" class="w-24 bg-slate-700/50 text-white border-0 rounded-lg px-3 py-3 text-center focus:ring-2 focus:ring-emerald-400 placeholder-slate-400" required>
                        </div>
                        <div>
                            <label for="newItemUnit" class="block text-sm font-medium text-slate-300 mb-2">Unit</label>
                            <select id="newItemUnit" bind:value={newItemUnit} class="w-32 bg-slate-700/50 text-white border-0 rounded-lg px-3 py-3 focus:ring-2 focus:ring-emerald-400">
                                {#each predefinedUnits as unit} <option value={unit}>{unit}</option> {/each}
                            </select>
                        </div>
                        <div class="flex items-end">
                            <button type="submit" class="bg-gradient-to-r from-emerald-500 to-blue-500 hover:from-emerald-600 hover:to-blue-600 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 transform hover:scale-105 flex items-center gap-2">
                                <span>Add Item</span> <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                            </button>
                        </div>
                    </div>
                </form>
            </div>

            <!-- Generate Instacart List Section -->
            <div class="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6 mb-8">
                <h3 class="text-2xl font-semibold text-emerald-400 mb-6 flex items-center gap-2"><span>🛒</span> Generate Instacart Shopping List</h3>
                <div class="mb-6">
                    <label for="instacartListTitleStatic" class="block text-sm font-medium text-slate-300 mb-2">List Title for Instacart (uses current list name):</label>
                    <p class="w-full bg-slate-700/30 text-slate-300 border-0 rounded-lg px-4 py-3 ">{shoppingListTitle}</p>
                </div>
                <button on:click={generateMasterInstacartList} disabled={instacartShoppingListLoading || itemsInCart.length === 0} class="w-full bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 disabled:from-slate-600 disabled:to-slate-600 text-white px-6 py-4 rounded-xl font-semibold text-lg transition-all duration-200 transform hover:scale-105 disabled:transform-none disabled:cursor-not-allowed flex items-center justify-center gap-3">
                    {#if instacartShoppingListLoading}
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Generating...
                    {:else}
                        <img src="/imgs/Instacart_Carrot.png" alt="Instacart Logo" class="h-6 w-6" />
                        Get Full Shopping List on Instacart
                    {/if}
                </button>
                {#if instacartShoppingListError}
                    <div class="mt-6 p-4 border border-red-500/50 bg-red-900/20 backdrop-blur-sm text-red-300 rounded-xl">
                        <div class="flex items-start gap-3">
                            <svg class="w-5 h-5 mt-0.5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <div>
                                <p class="font-semibold mb-1">Error generating list:</p>
                                <p class="text-sm">{@html instacartShoppingListError.replace(/\(field: (.*?)\)/g, '<span class="text-xs text-red-400">(field: $1)</span>')}</p>
                            </div>
                        </div>
                    </div>
                {/if}
                {#if instacartShoppingListUrl}
                    <div class="mt-6 p-6 bg-gradient-to-r from-emerald-900/20 to-blue-900/20 backdrop-blur-sm border border-emerald-500/30 rounded-xl text-center">
                        <div class="flex items-center justify-center gap-2 text-emerald-300 font-semibold mb-4">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                            Your shopping list is ready!
                        </div>
                        <a href={instacartShoppingListUrl} target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-3 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-200 transform hover:scale-105">
                            Open Shopping List on Instacart
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                        </a>
                        <p class="text-xs text-slate-400 mt-4">Note: Link reflects current cart items. Changes require regeneration.</p>
                    </div>
                {/if}
            </div>
        {/if}

        <!-- Clear Cart Button -->
        {#if itemsInCart.length > 0}
            <div class="mt-12 text-center">
                {#if showClearConfirm}
                    <div class="p-4 bg-zinc-700 rounded-md inline-block">
                        <p class="text-white mb-3">Are you sure you want to clear all items from '{shoppingListTitle}'?</p>
                        <button on:click={executeClearCart} class="btn-danger mr-2">Yes, Clear Items</button>
                        <button on:click={() => showClearConfirm = false} class="btn-secondary">Cancel</button>
                    </div>
                {:else}
                    <button on:click={confirmClearCart} class="btn-danger-outline">
                        Clear Items from '{shoppingListTitle}'
                    </button>
                {/if}
            </div>
        {/if}


        <!-- Load List Modal -->
        {#if showLoadListModal && $fbUserStore}
            <div class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50" on:click|self|stopPropagation={() => showLoadListModal = false}>
                <div class="bg-slate-800 rounded-xl p-6 w-full max-w-lg max-h-[80vh] overflow-y-auto shadow-2xl border border-slate-700">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-2xl font-semibold text-emerald-400">Load a Saved List</h3>
                        <button on:click={() => showLoadListModal = false} class="text-slate-400 hover:text-slate-200 text-2xl leading-none">×</button>
                    </div>
                    {#if isLoadingSavedLists}
                        <p class="text-slate-400 text-center py-4">Loading your lists...</p>
                    {:else if savedUserLists.length === 0}
                        <p class="text-slate-400 text-center py-4">You haven't saved any lists yet.</p>
                    {:else}
                        <ul class="space-y-3">
                            {#each savedUserLists as list (list.id)}
                                <li class="bg-slate-700/50 p-3 rounded-lg flex justify-between items-center hover:bg-slate-600/50 transition-colors">
                                    <div>
                                        <span class="font-medium text-slate-200 block">{list.name}</span>
                                        <p class="text-xs text-slate-400">
                                            {list.items.length} items - Updated: {new Date(list.updatedAt.toDate()).toLocaleDateString()}
                                        </p>
                                    </div>
                                    <div class="flex gap-2">
                                        <button on:click={() => loadList(list)} class="btn-primary text-sm px-3 py-1">Load</button>
                                        <button on:click={() => handleDeleteList(list.id, list.name)} class="btn-danger-outline text-sm px-3 py-1" title="Delete List">🗑️</button>
                                    </div>
                                </li>
                            {/each}
                        </ul>
                    {/if}
                </div>
            </div>
        {/if}
    </div>
</div>
