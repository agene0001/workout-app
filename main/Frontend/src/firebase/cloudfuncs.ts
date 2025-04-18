import * as functions from "firebase-functions/v1"; // Using v1 for auth trigger and https.onCall
import * as admin from "firebase-admin";
import { UserRecord } from "firebase-admin/auth";
import { HttpsError, CallableContext } from "firebase-functions/v1/https";
import {InstacartRes} from "../types";
import axios from "axios";

// --- Initialize Firebase Admin SDK ---
try {
    admin.initializeApp();
} catch (e) {
    functions.logger.info("Admin SDK already initialized.");
}

const db = admin.firestore();
const USER_COLLECTION = "users"; // Define collection names as constants
const FINGERPRINT_COLLECTION = "userfp";

// --- Interfaces (Defined within this file for Cloud Functions) ---

// Firestore document structure for 'users' collection
interface UserFirestoreData {
    email?: string | null;
    displayName?: string | null;
    createdAt: admin.firestore.FieldValue;
    tokens: number;
    lastLogin: admin.firestore.FieldValue;
    fingerprint?: string | null;
}

// Data expected for the associateFingerprint function (from client)
interface FingerprintAssociationData {
    fpId: string;
}

// Data expected for the checkFingerprintExists function (from client)
interface FingerprintCheckData {
    fpId: string;
}

// Firestore document structure for 'userfp' collection
interface FingerprintFirestoreDoc {
    userId: string;
    lastSeen: admin.firestore.FieldValue;
}

// Result type for associateFingerprint function (to client)
interface AssociateFingerprintResult {
    success: boolean;
}

// Result type for checkFingerprintExists function (to client)
interface CheckFingerprintResult {
    exists: boolean;
    userId: string | null;
}

// Data expected by processRecipeWithTokenCheck function (from client - InfoBlock)
interface ProcessRecipeInputData {
    ingredients: string;
    instructions: string[];
    title: string;
    image_url?: string;
}

// --- 1. Initialize User Document and Tokens on Auth Creation (Auth Trigger) ---
export const initializeUserTokens = functions.auth
    .user()
    .onCreate(async (user: UserRecord): Promise<void> => {
        const { uid, email, displayName } = user;
        const initialTokens = 3; // Securely defined initial token count

        functions.logger.log(`Initializing user document for user: ${uid}`);
        const userRef = db.collection(USER_COLLECTION).doc(uid);

        const userData: UserFirestoreData = {
            email: email ?? null,
            displayName: displayName ?? "New User",
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            tokens: initialTokens,
            lastLogin: admin.firestore.FieldValue.serverTimestamp(),
            // fingerprint is added later via associateFingerprint function
        };

        try {
            await userRef.set(userData);
            functions.logger.log(`Successfully initialized document for ${uid} with ${initialTokens} tokens.`);
        } catch (error) {
            functions.logger.error(`Error initializing document for ${uid}:`, error);
        }
    });

// --- 2. Securely Associate Fingerprint with User (HTTPS Callable) ---
export const associateFingerprint = functions.https.onCall(
    async (data: FingerprintAssociationData, context: CallableContext): Promise<AssociateFingerprintResult> => {
        // Check if user is authenticated
        if (!context.auth) {
            throw new HttpsError('unauthenticated', 'User must be authenticated to associate a fingerprint.');
        }

        const { fpId } = data;
        const userId = context.auth.uid;

        // Validate fingerprint ID
        if (!fpId || typeof fpId !== 'string' || fpId.length < 5) {
            throw new HttpsError('invalid-argument', 'Invalid fingerprint ID provided.');
        }

        functions.logger.log(`Associating fingerprint ${fpId} with user ${userId}`);

        try {
            const now = admin.firestore.FieldValue.serverTimestamp();

            // Update user document with fingerprint
            await db.collection(USER_COLLECTION).doc(userId).update({
                fingerprint: fpId,
                lastLogin: now
            });

            // Create/update fingerprint document
            await db.collection(FINGERPRINT_COLLECTION).doc(fpId).set({
                userId: userId,
                lastSeen: now
            }, { merge: true });

            return { success: true };
        } catch (error) {
            functions.logger.error(`Error associating fingerprint ${fpId} with user ${userId}:`, error);
            throw new HttpsError('internal', 'Failed to associate fingerprint with user.');
        }
    }
);

// --- 3. Securely Check if Fingerprint Exists (HTTPS Callable) ---
export const checkFingerprintExists = functions.https.onCall(
    async (data: FingerprintCheckData): Promise<CheckFingerprintResult> => {
        const { fpId } = data;

        // Validate fingerprint ID
        if (!fpId || typeof fpId !== 'string' || fpId.length < 5) {
            throw new HttpsError('invalid-argument', 'Invalid fingerprint ID provided.');
        }

        functions.logger.log(`Checking if fingerprint ${fpId} exists in database`);

        try {
            const docRef = db.collection(FINGERPRINT_COLLECTION).doc(fpId);
            const docSnap = await docRef.get();

            if (docSnap.exists) {
                const data = docSnap.data() as FingerprintFirestoreDoc;
                return {
                    exists: true,
                    userId: data.userId
                };
            }

            return { exists: false, userId: null };
        } catch (error) {
            functions.logger.error(`Error checking fingerprint ${fpId}:`, error);
            throw new HttpsError('internal', 'Failed to check fingerprint existence.');
        }
    }
);

// --- 4. Securely Process Recipe & Decrement Token (HTTPS Callable) ---

// Internal helper for the actual Instacart API call logic
const callInstacartProcessingService = async (recipeData: ProcessRecipeInputData): Promise<InstacartRes> => {
    try {
        // This should be replaced with your actual Instacart API endpoint

        const isEmulator = process.env.FUNCTIONS_EMULATOR === 'true';
// Choose the appropriate URL based on your logic (this example prioritizes Flask)
        const apiUrl = isEmulator?'http://localhost:5000/recipes/process-recipe':'https://gainztrackers.com/recipes/process-recipe';
        // Make the request to your backend service
        if(apiUrl) {
            const response = await axios.post(apiUrl, recipeData);

            // Validate the response structure to ensure it matches InstacartRes
            if (!response.data || !response.data.response || !response.data.response.products_link_url) {
                throw new Error('Invalid response from Instacart processing service');
            }

            return response.data;
        }
        else {
            throw new Error('Invalid response from Instacart processing service');
        }
    } catch (error) {
        functions.logger.error('Error calling Instacart processing service:', error);
        throw new HttpsError('internal', 'Failed to process recipe with Instacart.');
    }
};

export const processRecipeWithTokenCheck = functions.https.onCall(
    async (data: ProcessRecipeInputData, context: CallableContext): Promise<InstacartRes> => {
        // Check authentication
        if (!context.auth) {
            throw new HttpsError('unauthenticated', 'User must be authenticated to process recipes.');
        }

        const userId = context.auth.uid;
        functions.logger.log(`Checking tokens for user ${userId} for recipe processing`);

        try {
            // Check user document for token count
            const userRef = db.collection(USER_COLLECTION).doc(userId);
            const userDoc = await userRef.get();

            if (!userDoc.exists) {
                throw new HttpsError('not-found', 'User document not found in database.');
            }

            const userData = userDoc.data() as UserFirestoreData;
            const currentTokens = userData.tokens || 0;

            // Check if user has enough tokens
            if (currentTokens <= 0) {
                throw new HttpsError('permission-denied', 'User has insufficient tokens to process recipe.');
            }

            // Decrement token first (optimistic approach)
            await userRef.update({
                tokens: admin.firestore.FieldValue.increment(-1)
            });

            functions.logger.log(`User ${userId} has ${currentTokens} tokens. Decremented by 1.`);

            // Call Instacart processing service
            const instacartResult = await callInstacartProcessingService(data);

            // Log success
            functions.logger.log(`Successfully processed recipe for user ${userId}`);

            return instacartResult;
        } catch (error) {
            // If we've already decremented a token but the API call failed,
            // we might want to refund the token here depending on business logic

            functions.logger.error(`Error processing recipe for user ${userId}:`, error);

            // Re-throw as HttpsError if not already
            if (error instanceof HttpsError) {
                throw error;
            }

            throw new HttpsError('internal', 'Failed to process recipe.');
        }
    }
);