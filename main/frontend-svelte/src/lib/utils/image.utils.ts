// src/lib/utils/image.utils.ts
import { getIdToken } from "firebase/auth";
import { getClientAuth } from "$lib/firebase/firebase.client.js";
import {browser} from "$app/environment";

/**
 * Uploads an image file to the server.
 * @param file The image file to upload.
 * @param uploadPath The API endpoint path for uploading. Defaults to '/api/v1/blog/images/upload'.
 * @returns Promise<string | null> The URL of the uploaded image, or null on failure.
 */
export async function uploadImage(
    file: File,
    uploadPath: string = '/api/v1/blog/images/upload'
): Promise<{ url: string; name: string } | null> {
    const auth = getClientAuth();
    if (!auth.currentUser) {
        console.error("User not authenticated for image upload.");
        return null;
    }

    try {
        const idToken = await getIdToken(auth.currentUser);
        const formData = new FormData();
        formData.append('image', file);

        const response = await fetch(uploadPath, {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${idToken}`
            },
            body: formData
        });

        if (response.ok) {
            const responseData = await response.json();
            if (responseData && responseData.url) {
                console.log('Image uploaded successfully via util:', responseData.url);
                return {
                    url: responseData.url,
                    name: responseData.name || file.name // Use server's name if provided, otherwise original file.name
                };
            } else {
                // This error indicates an issue with the server's response format
                throw new Error("Image URL not found in server response after successful upload.");
            }
        } else {
            const errorText = await response.text();
            throw new Error(`Upload failed: ${response.status} ${errorText}`);
        }
    } catch (error: any) {
        console.error(`Image upload failed via util: ${error.message}`, error);
        return null; // Return null to indicate failure to the caller
    }
}



/**
 * Deletes an image from the server.
 * @param imageUrlOrPath The URL or path of the image to delete.
 * @param deletePathBase The base API endpoint path for deleting.
 * @returns Promise<boolean> True if deletion was successful or image was not server-managed, false on failure.
 */
export async function deleteImageOnServer(
    imageUrlOrPath: string,
    deletePathBase: string = '/api/v1/blog/images/delete/' // Your backend delete endpoint base
): Promise<boolean> {
    if (!imageUrlOrPath) {
        console.warn('No image URL or path provided for deletion.');
        return true; // No action needed if no URL/path
    }

    let filename: string | undefined;

    try {
        // Attempt to parse as a full URL first
        let pathSegment: string;
        try {
            const urlObj = new URL(imageUrlOrPath);
            pathSegment = urlObj.pathname;
        } catch (e) {
            // If it's not a full URL, assume it's a path
            if (imageUrlOrPath.startsWith('/')) {
                pathSegment = imageUrlOrPath;
            } else {
                // If it's not a full URL and not a root-relative path, it's ambiguous.
                // For now, let's try to extract filename directly if it's just a filename.
                // Or, you might decide this is an invalid input.
                console.warn('Image input is not a full URL or root-relative path:', imageUrlOrPath);
                // Try to get filename from the end if it looks like just a filename
                const parts = imageUrlOrPath.split('/');
                filename = parts.pop();
                if (!filename || !filename.includes('.')) { // Basic check for extension
                    console.warn('Could not extract a valid filename for deletion from non-URL/path:', imageUrlOrPath);
                    return true;
                }
                // If we extracted a filename here, we can skip the next path-based extraction.
            }
        }

        if (!filename && pathSegment) { // Only if filename wasn't extracted from a non-URL/path string
            const pathParts = pathSegment.split('/');
            filename = pathParts.pop(); // Gets the last part of the path
        }


        if (!filename || filename.includes('placeholder') || filename.length < 5) { // Basic sanity check
            console.warn('Could not extract a valid filename for deletion or image is a placeholder:', imageUrlOrPath);
            return true; // Don't attempt to delete if filename is weird or a known placeholder
        }
    } catch (e) {
        console.warn('Error processing image URL/path for deletion:', imageUrlOrPath, e);
        return true; // Not a URL/path we can process for deletion
    }

    if (!filename) {
        console.warn('Could not extract filename from URL/path for deletion after processing:', imageUrlOrPath);
        return true;
    }

    // Construct the full delete URL for the fetch call
    // This assumes your deletePathBase is relative to your domain origin
    const fullDeleteUrl = browser ? `${window.location.origin}${deletePathBase}${filename}` : `${deletePathBase}${filename}`;
    // If running server-side and your API is on a different origin, you'll need to configure the full base URL.
    // For client-side, window.location.origin is fine.

    const auth = getClientAuth();
    if (!auth.currentUser) {
        console.error('User not authenticated for image deletion.');
        return false;
    }

    try {
        const idToken = await getIdToken(auth.currentUser);
        console.log(`Attempting to delete image: ${filename} via URL: ${fullDeleteUrl}`); // Log the full URL
        const response = await fetch(fullDeleteUrl, { // Use the full URL
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${idToken}`
            }
        });

        if (response.ok) {
            console.log(`Image ${filename} (from ${imageUrlOrPath}) deleted successfully from server.`);
            return true;
        } else {
            const errorText = await response.text();
            if (response.status === 404) {
                console.warn(`Image ${filename} not found on server for deletion. URL: ${imageUrlOrPath}`);
                return true;
            }
            throw new Error(`Deletion failed: ${response.status} ${errorText}`);
        }
    } catch (error: any) {
        console.error(`Error during image deletion request for ${filename} (from ${imageUrlOrPath}):`, error);
        return false;
    }
}