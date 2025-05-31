// src/lib/stores/cartStore.ts
import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';

// --- Interfaces --- (Keep your existing interfaces)
export interface CartStoredRecipe {
    recipeName: string;
    recipeImgSrc?: string;
    ingredients: string[];
}
export interface CartRecipeBatchItem {
    id: string;
    type: 'recipe_batch';
    recipe: CartStoredRecipe;
    servingsMultiplier: number;
}
export interface CartCustomStandaloneIngredient {
    id: string;
    type: 'custom_standalone_ingredient';
    name: string;
    quantity: number;
    unit: string;
}
export type CartItem = CartRecipeBatchItem | CartCustomStandaloneIngredient;
export interface InstacartLineItem {
    name: string;
    quantity?: number | string;
    unit?: string;
    display_text?: string;
}

const CART_STORAGE_KEY = 'gains_tracker_cart_v3';

const initialCartValue: CartItem[] = browser && localStorage.getItem(CART_STORAGE_KEY)
    ? JSON.parse(localStorage.getItem(CART_STORAGE_KEY)!)
    : [];

const { subscribe, set, update } = writable<CartItem[]>(initialCartValue);

if (browser) {
    subscribe(value => {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(value));
    });
}

function addRecipeToCart(
    recipeData: { name: string; imgSrc?: string; ingredients: string[] },
    servingsMultiplier: number = 1
) {
    if (!recipeData || !recipeData.name || !Array.isArray(recipeData.ingredients)) {
        console.error("Invalid recipe data provided to addRecipeToCart", recipeData);
        return;
    }
    const newCartEntry: CartRecipeBatchItem = {
        id: `recipe_batch-${recipeData.name.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`,
        type: 'recipe_batch',
        recipe: {
            recipeName: recipeData.name,
            recipeImgSrc: recipeData.imgSrc,
            ingredients: recipeData.ingredients,
        },
        servingsMultiplier: Math.max(1, servingsMultiplier),
    };
    update(items => {
        const existingRecipeIndex = items.findIndex(
            item => item.type === 'recipe_batch' && item.recipe.recipeName === newCartEntry.recipe.recipeName
        );
        if (existingRecipeIndex > -1) {
            const updatedItems = [...items];
            const existingItem = updatedItems[existingRecipeIndex] as CartRecipeBatchItem;
            existingItem.servingsMultiplier += newCartEntry.servingsMultiplier;
            return updatedItems;
        } else {
            return [...items, newCartEntry];
        }
    });
}

function addCustomIngredientToCart(name: string, quantity: number, unit: string) {
    if (!name.trim() || quantity <= 0) return;
    const newItem: CartCustomStandaloneIngredient = {
        id: `custom_standalone-${Date.now()}`,
        type: 'custom_standalone_ingredient',
        name: name.trim(),
        quantity,
        unit: unit.trim() || 'each',
    };
    update(items => [...items, newItem]);
}

function removeItemFromCart(itemId: string) {
    update(items => items.filter(item => item.id !== itemId));
}

function updateRecipeServings(itemId: string, newServingsMultiplier: number) {
    update(items =>
        items.map(item =>
            item.id === itemId && item.type === 'recipe_batch'
                ? { ...item, servingsMultiplier: Math.max(0, newServingsMultiplier) } // Allow 0 to effectively remove it via handler
                : item
        ) as CartItem[]
    );
}

function updateCustomIngredient(
    itemId: string,
    newDetails: Partial<Omit<CartCustomStandaloneIngredient, 'id' | 'type'>>
) {
    update(items =>
        items.map(item => {
            if (item.id === itemId && item.type === 'custom_standalone_ingredient') {
                return {
                    ...item,
                    name: newDetails.name !== undefined ? newDetails.name.trim() : item.name,
                    quantity: newDetails.quantity !== undefined && newDetails.quantity > 0 ? newDetails.quantity : item.quantity,
                    unit: newDetails.unit !== undefined ? (newDetails.unit.trim() || 'each') : item.unit,
                };
            }
            return item;
        })
    );
}

function clearCart() {
    set([]);
}

function setList(newItems: CartItem[]) { // <--- NEW METHOD
    set(newItems);
}

function getCartDataForBackend(): CartItem[] {
    return get({ subscribe });
}

export const cart = {
    subscribe,
    addRecipe: addRecipeToCart,
    addCustomIngredient: addCustomIngredientToCart,
    removeItem: removeItemFromCart,
    updateRecipeServings,
    updateCustomIngredient,
    clear: clearCart,
    setList, // <--- EXPORT NEW METHOD
    getCartDataForBackend,
};