// setAdminClaim.js

const admin = require('firebase-admin');

// --- 1. Load your Service Account Key ---
// Make sure 'serviceAccountKey.json' is in the same directory as this script.
// KEEP THIS FILE SECURE! Do NOT commit it to Git.
const serviceAccount = require('./service-account-key.json');

// --- 2. Initialize the Firebase Admin SDK ---
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});

// --- 3. Define the User to Target ---
// IMPORTANT: Replace 'YOUR_USER_UID_HERE' with the actual UID of the user you want to make an admin.
// You can find a user's UID in your Firebase Console under "Authentication".
const targetUserUid = 'FkEKAXQvmpPvHBRp7sknMvYNk8J3';

// --- 4. Define the Desired Admin Status ---
// Set to 'true' to make the user an admin.
// Set to 'false' to remove admin privileges.
const makeAdmin = true; // <--- Set this to 'true' for your current goal

// --- 5. Function to Set Custom Claim and Revoke Tokens ---
async function setCustomAdminClaim() {
    try {
        // Get the user's current record to inspect existing claims (optional, but good for logging)
        const user = await admin.auth().getUser(targetUserUid);
        const currentClaims = user.customClaims || {};

        let newClaims;
        if (makeAdmin) {
            newClaims = { ...currentClaims, admin: true };
            console.log(`Attempting to grant admin claim for user: ${targetUserUid}`);
        } else {
            newClaims = { ...currentClaims };
            delete newClaims.admin; // Remove the admin claim
            console.log(`Attempting to remove admin claim for user: ${targetUserUid}`);
        }

        // Set the custom claims
        await admin.auth().setCustomUserClaims(targetUserUid, newClaims);

        // Revoke all refresh tokens for the user.
        // This is CRUCIAL! It forces the user to re-authenticate (e.g., on next page refresh/login)
        // and immediately receive the updated ID token with the new claims.
        await admin.auth().revokeRefreshTokens(targetUserUid);

        console.log(`Successfully updated admin status for user: ${targetUserUid} to ${makeAdmin ? 'admin' : 'non-admin'}.`);
        console.log(`User will receive new claims upon next re-authentication.`);
        console.log(`New custom claims on record: ${JSON.stringify(newClaims)}`);

        process.exit(0); // Exit successfully

    } catch (error) {
        console.error(`Error processing admin claim for user ${targetUserUid}:`, error);
        process.exit(1); // Exit with an error code to indicate failure
    }
}

// --- 6. Execute the Function ---
setCustomAdminClaim();