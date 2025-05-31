// src/lib/shoppingListDB.ts
import { getDb } from '$lib/firebase/firebase.client'; // Use your existing Firebase client
import {
    collection,
    addDoc,
    getDocs,
    doc,
    updateDoc,
    deleteDoc,
    query,
    where,
    serverTimestamp,
    orderBy,
    type Timestamp,
    type Firestore // Import Firestore type
} from 'firebase/firestore';
import type { CartItem } from '$lib/stores/cartStore';

export interface SavedShoppingList {
    id: string; // Firestore document ID
    userId: string;
    name: string;
    items: CartItem[];
    createdAt: Timestamp; // Firestore Timestamp
    updatedAt: Timestamp; // Firestore Timestamp
}

// Helper to get the collection reference, ensuring Firestore is initialized
function getListsCollectionRef(firestoreInstance: Firestore) {
    return collection(firestoreInstance, 'shoppingLists');
}

export async function saveNewShoppingList(userId: string, name: string, items: CartItem[]): Promise<string | null> {
    const firestore = getDb();
    if (!firestore) {
        console.error("Firestore not initialized (saveNewShoppingList).");
        return null; // Or throw an error
    }
    try {
        const docRef = await addDoc(getListsCollectionRef(firestore), {
            userId,
            name: name.trim() || "Untitled List",
            items,
            createdAt: serverTimestamp(),
            updatedAt: serverTimestamp(),
        });
        return docRef.id;
    } catch (error) {
        console.error("Error saving new shopping list:", error);
        return null;
    }
}

export async function updateShoppingList(listId: string, name: string, items: CartItem[]): Promise<boolean> {
    const firestore = getDb();
    if (!firestore) {
        console.error("Firestore not initialized (updateShoppingList).");
        return false;
    }
    try {
        const listDocRef = doc(getListsCollectionRef(firestore), listId);
        await updateDoc(listDocRef, {
            name: name.trim() || "Untitled List",
            items,
            updatedAt: serverTimestamp(),
        });
        return true;
    } catch (error) {
        console.error("Error updating shopping list:", error);
        return false;
    }
}

export async function getUserShoppingLists(userId: string): Promise<SavedShoppingList[]> {
    const firestore = getDb();
    if (!firestore) {
        console.error("Firestore not initialized (getUserShoppingLists).");
        return [];
    }
    try {
        const q = query(getListsCollectionRef(firestore), where('userId', '==', userId), orderBy('updatedAt', 'desc'));
        const querySnapshot = await getDocs(q);
        return querySnapshot.docs.map(docSnapshot => {
            const data = docSnapshot.data();
            // Ensure all fields are correctly mapped, especially Timestamps
            return {
                id: docSnapshot.id,
                userId: data.userId,
                name: data.name,
                items: data.items, // Assuming items are stored in a compatible format
                createdAt: data.createdAt as Timestamp,
                updatedAt: data.updatedAt as Timestamp,
            } as SavedShoppingList;
        });
    } catch (error) {
        console.error("Error fetching user shopping lists:", error);
        return [];
    }
}

export async function deleteShoppingList(listId: string): Promise<boolean> {
    const firestore = getDb();
    if (!firestore) {
        console.error("Firestore not initialized (deleteShoppingList).");
        return false;
    }
    try {
        const listDocRef = doc(getListsCollectionRef(firestore), listId);
        await deleteDoc(listDocRef);
        return true;
    } catch (error) {
        console.error("Error deleting shopping list:", error);
        return false;
    }
}