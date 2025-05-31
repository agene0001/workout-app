<script lang="ts">
    import { getContext, onMount } from 'svelte';
    import { page } from '$app/stores';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import Editor from '$lib/components/blog/Editor.svelte';
    import { getIdToken } from "firebase/auth";
    import { getClientAuth } from "$lib/firebase/firebase.client.js";
    import { deleteImageOnServer } from "$lib/utils/image.utils";

    const auth = getClientAuth();
    const isAdmin = getContext('isAdmin');

    export let data: any;
    let post = data.post;
    const isNewPost = data.isNew;
    type FeaturedImageUploadMode = 'file' | 'url';
    let featuredImageUploadMode: FeaturedImageUploadMode = 'file';

    let featuredImageFile: File | null = null;
    let isFeaturedImageUploading = false;
    let editorComponent: Editor;
    let postTitle = post?.title || '';
    let editorInitialContent = post?.content || { blocks: [{ type: 'paragraph', data: { text: 'Start writing your blog post here...' } }] };

    let postExcerpt = post?.excerpt || '';
    let postImageUrl = post?.image || '';
    let isFeaturedPost = post?.featured || false;

    let authorName = post?.authorName || '';
    let authorTitle = post?.authorTitle || '';

    let isLoading = false;
    let errorMessage = '';
    let selectedCategory = post?.category || '';
    let categories = [];
    let isImageUploading = false;
    let isDeletingFeaturedImage = false; // This now means "marking for deletion" or "UI state for removal"

    let pageTitle = isNewPost ? "Create New Blog Post" : "Edit Post";

    // --- New state for managing image operations ---
    let originalPostImageUrl: string | null = null;
    let pendingDeletions: Set<string> = new Set();
    let newlyUploadedImageUrls: Set<string> = new Set();
    // Tracks the previous value of postImageUrl for the reactive block
    let previousPostImageUrlForReactive: string = '';
    // --- End new state ---

    function isManagedUploadUrl(url: string | null | undefined): boolean {
        if (!url) return false;
        return url.includes('/api/v1/blog/uploaded/images/');
    }

    onMount(async () => {
        if (browser && !$isAdmin) {
            goto('/Blog');
            return;
        }
        originalPostImageUrl = post?.image || null;
        previousPostImageUrlForReactive = postImageUrl; // Initialize for the reactive block

        // ... (rest of your onMount)
        console.log(post);
        if (!isNewPost && post?.content) {
            if (typeof post.content === 'string') {
                try {
                    const parsed = JSON.parse(post.content);
                    editorInitialContent = parsed?.blocks ? parsed : { blocks: [{ type: 'paragraph', data: { text: post.content } }] };
                } catch (e) {
                    console.error('Failed to parse existing post content for editor:', e);
                    editorInitialContent = { blocks: [{ type: 'paragraph', data: { text: "Error loading content. " + post.content } }] };
                }
            } else if (post.content?.blocks) {
                editorInitialContent = post.content;
            }
        }
        if (browser) {
            await fetchCategories();
            if (!isNewPost && post?.category && categories.some(c => c.slug === post.category)) {
                selectedCategory = post.category;
            } else if (categories.length > 0 && !selectedCategory && isNewPost) {
                // selectedCategory = categories[0].slug;
            }
        }
    });

    // Reactive block to handle changes to postImageUrl and mark old images for pending deletion
    $: {
        if (browser && postImageUrl !== previousPostImageUrlForReactive) {
            // If the previous URL existed and was either a managed server upload or uploaded in this session
            if (previousPostImageUrlForReactive &&
                (isManagedUploadUrl(previousPostImageUrlForReactive) || newlyUploadedImageUrls.has(previousPostImageUrlForReactive))) {
                // And it's truly being replaced (not just an initial undefined -> value scenario)
                if (postImageUrl !== previousPostImageUrlForReactive) {
                    pendingDeletions.add(previousPostImageUrlForReactive);
                    console.log(`Marked ${previousPostImageUrlForReactive} for pending deletion because postImageUrl changed to: ${postImageUrl}`);
                }
            }
            previousPostImageUrlForReactive = postImageUrl; // Update for the next change
        }
    }

    async function uploadFeaturedImageViaFile(file: File): Promise<string | null> {
        if (!auth.currentUser) {
            errorMessage = "User not authenticated for image upload.";
            alert(errorMessage);
            return null;
        }
        isFeaturedImageUploading = true;
        errorMessage = '';

        try {
            const idToken = await getIdToken(auth.currentUser);
            const formData = new FormData();
            formData.append('image', file);

            const response = await fetch('/api/v1/blog/images/upload', {
                method: 'POST',
                headers: { Authorization: `Bearer ${idToken}` },
                body: formData
            });

            if (response.ok) {
                const responseData = await response.json();
                if (responseData && responseData.url) {
                    const newUrl = responseData.url;
                    newlyUploadedImageUrls.add(newUrl); // Track this new upload
                    console.log('New featured image uploaded successfully to server:', newUrl);
                    return newUrl;
                } else {
                    throw new Error("Image URL not found in server response.");
                }
            } else {
                const errorText = await response.text();
                throw new Error(`Upload failed: ${response.status} ${errorText}`);
            }
        } catch (error: any) {
            errorMessage = `Featured image upload failed: ${error.message}`;
            console.error(errorMessage, error);
            alert(errorMessage);
            return null;
        } finally {
            isFeaturedImageUploading = false;
        }
    }

    async function handleFeaturedImageFileChange(event: Event) {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files.length > 0) {
            const fileToUpload = input.files[0];
            if (fileToUpload) {
                const uploadedUrl = await uploadFeaturedImageViaFile(fileToUpload);
                if (uploadedUrl) {
                    postImageUrl = uploadedUrl; // This will trigger the reactive block $:
                }
                if (input) input.value = '';
            }
        }
    }

    // This function now just updates postImageUrl, the reactive block handles marking for deletion
    async function handleDeleteFeaturedImage() {
        if (!postImageUrl) return;
        if (!confirm("Are you sure you want to remove this featured image? It will be deleted from the server if you save the changes.")) return;

        // The actual deletion will happen on save if postImageUrl remains empty
        // The reactive block ($:) will add the current postImageUrl to pendingDeletions when postImageUrl becomes ''
        postImageUrl = '';
        const fileInput = document.getElementById('featuredImageUploadInput') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
        // No server deletion here.
    }


    function setFeaturedImageUploadMode(mode: FeaturedImageUploadMode) {
        featuredImageUploadMode = mode;
        if (mode === 'url') {
            featuredImageFile = null; // Clear any selected file if switching to URL
            const fileInput = document.getElementById('featuredImageUploadInput') as HTMLInputElement;
            if (fileInput) fileInput.value = '';
        }
        // When postImageUrl changes via bind:value in URL mode, the reactive block handles it.
    }

    async function fetchCategories() {
        try {
            const response = await fetch('/api/v1/blog/categories');
            if (response.ok) {
                categories = await response.json();
                if (categories.length > 0 && !selectedCategory && isNewPost) {
                    // selectedCategory = categories[0].slug;
                }
            } else {
                errorMessage = 'Failed to load categories. Please try again.';
            }
        } catch (error: any) {
            errorMessage = `Failed to load categories: ${error.message}`;
        }
        if(errorMessage && !errorMessage.includes('categories')) console.error(errorMessage);
    }

    function calculateReadTime(editorContent: any) {
        // ... (your existing calculateReadTime logic) ...
        let totalWords = 0;
        let imageCount = 0;
        if (!editorContent || !editorContent.blocks) return 1;

        editorContent.blocks.forEach((block: any) => {
            switch (block.type) {
                case 'paragraph': case 'header':
                    if (block.data?.text) totalWords += block.data.text.replace(/<[^>]*>/g, ' ').split(/\s+/).filter(Boolean).length;
                    break;
                case 'list':
                    block.data?.items?.forEach((item: any) => totalWords += (typeof item === 'string' ? item : item.content || '').replace(/<[^>]*>/g, ' ').split(/\s+/).filter(Boolean).length);
                    break;
                case 'image':
                    imageCount++;
                    if (block.data?.caption) totalWords += block.data.caption.split(/\s+/).filter(Boolean).length;
                    break;
                case 'quote':
                    if (block.data?.text) totalWords += block.data.text.replace(/<[^>]*>/g, ' ').split(/\s+/).filter(Boolean).length;
                    if (block.data?.caption) totalWords += block.data.caption.split(/\s+/).filter(Boolean).length;
                    break;
                default:
                    if (block.data?.text) totalWords += block.data.text.replace(/<[^>]*>/g, ' ').split(/\s+/).filter(Boolean).length;
                    break;
            }
        });
        const wordsPerMinute = 250, secondsPerImage = 10;
        const textTimeMinutes = totalWords / wordsPerMinute;
        const imageTimeMinutes = (imageCount * secondsPerImage) / 60;
        return Math.max(1, Math.ceil(textTimeMinutes + imageTimeMinutes));
    }

    async function executePendingImageDeletions(finalSavedImageUrl: string | null) {
        console.log("Executing pending deletions. Final URL:", finalSavedImageUrl, "Pending:", pendingDeletions);
        for (const urlToDelete of pendingDeletions) {
            // Only delete if it's not the image URL we are actually saving with the post
            if (urlToDelete !== finalSavedImageUrl) {
                console.log(`Saving post: Deleting superseded image from server: ${urlToDelete}`);
                try {
                    await deleteImageOnServer(urlToDelete);
                } catch (err) {
                    console.warn(`Could not delete image ${urlToDelete} during save:`, err);
                }
            }
        }
        pendingDeletions.clear();
        newlyUploadedImageUrls.clear(); // All uploads are now either committed or intentionally orphaned.
    }

    async function handleSavePost() {
        // ... (your existing validations) ...
        if (!editorComponent) {
            errorMessage = 'Editor component not initialized properly.'; return;
        }
        if (!postTitle.trim()) {
            alert('Post title cannot be empty.'); return;
        }
        if (!selectedCategory) {
            alert('Please select a category.'); return;
        }
        if (isImageUploading || isFeaturedImageUploading) { // Removed isDeletingFeaturedImage here as it's a UI state
            alert('Please wait for image operations to complete.'); return;
        }

        isLoading = true;
        errorMessage = '';
        const finalPostImageUrl = postImageUrl ? postImageUrl.trim() : null;

        try {
            // --- Perform actual server-side deletions for superseded images ---
            await executePendingImageDeletions(finalPostImageUrl);
            // --- ---

            const contentFromEditor = await editorComponent.getContent();
            if (!contentFromEditor || !contentFromEditor.blocks || contentFromEditor.blocks.length === 0) {
                alert('Post content cannot be empty.');
                isLoading = false; return; // Early exit, so no post save call
            }

            const readTimeData = calculateReadTime(contentFromEditor);

            let payload: any = {
                title: postTitle.trim(),
                content: contentFromEditor,
                category: selectedCategory,
                readTime: readTimeData,
                excerpt: postExcerpt.trim(),
                imageUrl: finalPostImageUrl,
                featured: isFeaturedPost,
                authorName: authorName.trim(),
                authorTitle: authorTitle.trim(),
            };
console.log("saving post");
console.log(payload);

            let method = 'POST';
            let url = `/api/v1/blog/posts`;

            if (!isNewPost && post?.id) {
                payload.id = post.id;
                method = 'PUT';
            } else if (!isNewPost && !post?.id) {
                throw new Error("Cannot update post: Post ID is missing.");
            }

            if (!auth.currentUser) {
                alert("User not authenticated. Please log in.");
                isLoading = false; return;
            }
            const idToken = await getIdToken(auth.currentUser);

            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${idToken}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const result = await response.json();
                alert(`Post ${isNewPost ? 'published' : 'updated'} successfully!`);
                // Clear sets on successful save as operations are committed
                pendingDeletions.clear();
                newlyUploadedImageUrls.clear();
                goto(result.slug ? `/Blog/${result.slug}` : '/Blog');
            } else {
                const errorData = await response.json().catch(() => ({ message: response.statusText }));
                // If save fails, pending deletions are NOT cleared, they might be retried or handled differently.
                // For simplicity now, they remain. This could be refined.
                throw new Error(`Failed to ${isNewPost ? 'create' : 'update'} post: ${response.status} - ${errorData.message || errorData.error || 'Unknown error'}`);
            }
        } catch (error: any) {
            errorMessage = `Failed to save post. Details: ${error.message}`;
            console.error("Save post error details:", error);
            alert(errorMessage);
            // If an error occurred before/during fetch, `executePendingImageDeletions` already ran.
            // The `pendingDeletions` set is cleared there.
        } finally {
            isLoading = false;
        }
    }

    async function cleanupOrphanedUploadsOnCancel() {
        console.log("Cancelling edit. Cleaning up orphaned uploads. Original URL:", originalPostImageUrl, "Newly uploaded:", newlyUploadedImageUrls);
        for (const uploadedUrl of newlyUploadedImageUrls) {
            // Delete if this uploaded image is not the one the post originally had
            // (covers case where user uploads A, then re-enters original URL B via text, then cancels. A should be deleted)
            if (uploadedUrl !== originalPostImageUrl) {
                console.log(`Cancelling: Deleting newly uploaded, orphaned image from server: ${uploadedUrl}`);
                try {
                    await deleteImageOnServer(uploadedUrl);
                } catch (err) {
                    console.warn(`Could not delete orphaned image ${uploadedUrl} on cancel:`, err);
                }
            }
        }
        pendingDeletions.clear();
        newlyUploadedImageUrls.clear();
    }

    async function handleCancel() {
        if (confirm('Are you sure you want to discard changes? Any new images uploaded in this session will be removed if not part of the original post.')) {
            isLoading = true; // Prevent other actions
            await cleanupOrphanedUploadsOnCancel();
            isLoading = false;
            goto(isNewPost ? '/Blog' : (post?.slug ? `/Blog/${post.slug}` : '/Blog'));
        }
    }

    function handleEditorEvents(event: any) {
        // ... (your existing editor event handling) ...
        console.log(`Editor event: ${event.type}`, event.detail);
        if (event.type === 'error') {
            errorMessage = `Editor Component Error: ${event.detail.message}`;
            alert(errorMessage);
        }
    }
</script>

<div class="page-container">
    {#if browser && $isAdmin}
        <section class="admin-post-form-section">
            <!-- ... (rest of your HTML template is largely the same) ... -->
            <!-- Modify the Remove Featured Image button's text/disabled logic if needed based on isDeletingFeaturedImage (UI state) -->
            <!-- For example, the button text in the preview area: -->
            <h1 class="page-title">{pageTitle}</h1>

            {#if errorMessage}
                <div class="error-alert">{errorMessage}</div>
            {/if}

            <div class="form-group title-group">
                <label for="postTitleInput" class="form-label">Post Title:</label>
                <input id="postTitleInput" type="text" bind:value={postTitle} class="form-input title-input" placeholder="Enter Post Title" required />
            </div>

            <div class="form-group author-name-group">
                <label for="authorNameInput" class="form-label">Author Name:</label>
                <input id="authorNameInput" type="text" bind:value={authorName} class="form-input" placeholder="Enter Author's Name (optional)" />
            </div>

            <div class="form-group author-title-group">
                <label for="authorTitleInput" class="form-label">Author Title:</label>
                <input id="authorTitleInput" type="text" bind:value={authorTitle} class="form-input" placeholder="e.g., Content Writer, Staff Editor (optional)" />
            </div>

            <div class="form-group category-group">
                <label for="categorySelect" class="form-label">Category:</label>
                <select id="categorySelect" bind:value={selectedCategory} class="form-input category-select" required>
                    <option value="" disabled>Select a category</option>
                    {#each categories as category (category.slug)}
                        <option value={category.slug}>{category.name}</option>
                    {/each}
                </select>
                {#if categories.length === 0 && !errorMessage.includes('categories')}
                    <p class="helper-text">Loading categories...</p>
                {/if}
            </div>

            <div class="form-group excerpt-group">
                <label for="postExcerptInput" class="form-label">Excerpt (Short Summary):</label>
                <textarea id="postExcerptInput" bind:value={postExcerpt} class="form-input excerpt-input" placeholder="Enter a short summary for the post (optional)" rows="3"></textarea>
            </div>

            <div class="form-group image-upload-group justify-items-center">
                <label class="form-label">Featured Image:</label>

                <div class="upload-mode-toggle">
                    <button
                            type="button"
                            class="button secondary-button"
                            class:active={featuredImageUploadMode === 'file'}
                            on:click={() => setFeaturedImageUploadMode('file')}
                            disabled={isFeaturedImageUploading || isImageUploading || isLoading}
                    >
                        Upload from Disk
                    </button>
                    <button
                            type="button"
                            class="button primary-button"
                            class:active={featuredImageUploadMode === 'url'}
                            on:click={() => setFeaturedImageUploadMode('url')}
                            disabled={isFeaturedImageUploading || isImageUploading || isLoading}
                    >
                        Enter URL
                    </button>
                </div>

                {#if featuredImageUploadMode === 'file'}
                    <div class="upload-mode-content">
                        <label for="featuredImageUploadInput" class="text-xl form-label-secondary">Select image file:</label>
                        <input
                                id="featuredImageUploadInput"
                                type="file"
                                accept="image/*"
                                on:change={handleFeaturedImageFileChange}
                                class="form-input file-input"
                                disabled={isFeaturedImageUploading || isImageUploading || isLoading}
                        />
                        {#if isFeaturedImageUploading}
                            <p class="helper-text">Uploading featured image...</p>
                        {/if}
                    </div>
                {:else if featuredImageUploadMode === 'url'}
                    <div class="upload-mode-content">
                        <label for="postImageUrlInput" class="text-xl form-label-secondary">Image URL:</label>
                        <input
                                id="postImageUrlInput"
                                type="url"
                                bind:value={postImageUrl}
                                class="form-input image-url-input"
                                placeholder="https://example.com/image.jpg"
                                disabled={isFeaturedImageUploading || isImageUploading || isLoading}
                        />
                    </div>
                {/if}

                {#if postImageUrl && !isFeaturedImageUploading }
                    <div class="image-preview-container">
                        <p>Current Featured Image:</p>
                        <img src={postImageUrl} alt="Featured image preview" class="image-preview" />
                        <button
                                type="button"
                                on:click={handleDeleteFeaturedImage}
                                class="button tiny-button remove-image-button"
                                disabled={isFeaturedImageUploading || isImageUploading || isLoading}
                        >
                            Remove Featured Image
                        </button>
                    </div>
                {:else if isFeaturedImageUploading}
                    <p class="helper-text">Uploading featured image...</p>
                {/if}
            </div>

            <div class="form-group featured-group">
                <label class="form-label-inline" for="isFeaturedCheckbox">
                    <input id="isFeaturedCheckbox" type="checkbox" bind:checked={isFeaturedPost} class="form-checkbox" />
                    Mark as Featured Post
                </label>
            </div>

            <div class="form-group editor-group">
                <label class="form-label">Content:</label>
                <Editor
                        bind:this={editorComponent}
                        initialData={editorInitialContent}
                        placeholder="Write your blog post content here..."
                        readOnly={false}
                        on:error={handleEditorEvents}
                        on:ready={handleEditorEvents}
                        on:change={handleEditorEvents}
                        on:image-upload-start={() => isImageUploading = true}
                        on:image-upload-success={() => isImageUploading = false}
                        on:image-upload-error={(e) => {
                        isImageUploading = false;
                        errorMessage = `Editor image upload failed: ${e.detail.message}`;
                        alert(errorMessage);
                    }}
                />
            </div>

            <div class="action-buttons">
                <button
                        on:click={handleSavePost}
                        class="button primary-button"
                        disabled={isLoading || categories.length === 0 || isImageUploading || isFeaturedImageUploading}
                >
                    {#if isLoading}Saving...
                    {:else if isImageUploading}Editor Image Uploading...
                    {:else if isFeaturedImageUploading}Featured Image Uploading...
                    {:else}{isNewPost ? 'Publish Post' : 'Save Changes'}
                    {/if}
                </button>
                <button on:click={handleCancel} class="button secondary-button" disabled={isLoading}>
                    Cancel
                </button>
            </div>
        </section>
    {:else if browser && !$isAdmin}
        <p class="error-message">You don't have permission to access this page.</p>
        <a href="/Blog" class="back-link">← Go to Blog List</a>
    {:else}
        <p class="loading-message">Loading editor...</p>
    {/if}
</div>
<style lang="css">
    /* ... Your existing CSS styles ... */
    @import url("https://use.typekit.net/oaz7axu.css");

    :root {
        --primary: #faebd7;
        --secondary: #C62368;
        --info: #3E92CC;
        --success: #39375B;
        --danger: #00dd87;
        --dark-bg: #002233;
        --gradient-text: linear-gradient(to right, #cc2b5e, #753a88);
        --gradient-hover: linear-gradient(to right, #5433ff, #20bdff, #a5fecb);
    }

    /* Base styles */
    .page-container {
        max-width: 960px;
        margin: 5rem auto;
        padding: 1.5rem;
        font-family: "orbital", sans-serif;
        color: #f1f1f1;
    }

    .page-title {
        color: var(--danger);
        margin-bottom: 1.5rem;
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--gradient-text);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation-name: heroZoom;
        animation-duration: 1s;
    }

    .admin-post-form-section {
        background-color: rgba(0, 34, 51, 0.9);
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 12px 12px 5px rgba(0, 0, 255, 0.2);
        transition: box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .admin-post-form-section::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('/imgs/backgrounds/low-poly-grid-haikei.svg');
        background-position: center;
        background-size: cover;
        opacity: 0.1;
        z-index: -1;
    }

    .form-group {
        margin-bottom: 1.8rem;
    }

    .form-label {
        display: block;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: var(--primary);
        font-size: 1.1rem;
    }

    .form-input, .excerpt-input {
        width: 100%;
        padding: 0.85rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        box-sizing: border-box;
        font-size: 1rem;
        background-color: rgba(0, 34, 51, 0.7);
        color: white;
        transition: all 0.3s ease;
        font-family: "orbital", sans-serif;
    }

    .form-input:focus, .excerpt-input:focus {
        border-color: var(--danger);
        box-shadow: 0 0 0 2px rgba(0, 221, 135, 0.25);
        outline: none;
    }

    .title-input {
        font-size: 1.5rem;
        font-weight: bold;
        border-left: 4px solid var(--danger);
    }
    /* Styling for new author fields (can be customized further) */
    .author-name-input, .author-title-input {
        border-left: 4px solid var(--info); /* Example different color */
    }


    .category-select {
        background-color: rgba(0, 34, 51, 0.7);
        color: white;
        cursor: pointer;
        appearance: none;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2300dd87' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 0.75rem center;
        background-size: 1em;
        padding-right: 2.5rem;
    }

    /* --- STYLES FOR NEW FIELDS --- */
    .excerpt-input {
        min-height: 100px;
        resize: vertical;
        border-left: 4px solid var(--secondary);
    }
    .image-upload-group .upload-mode-toggle {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    .image-upload-group .upload-mode-toggle button {
        flex-grow: 1;
    }


    .image-preview-container {
        margin-top: 1rem;
        padding: 1rem;
        border: 1px dashed rgba(255, 255, 255, 0.3);
        border-radius: 8px;
        background-color: rgba(0, 34, 51, 0.5);
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: transform 0.3s ease;
    }

    .image-preview-container:hover {
        transform: scale(1.02);
    }

    .image-preview-container p {
        margin: 0 0 0.75rem 0;
        font-weight: 500;
        color: var(--primary);
    }

    .image-preview {
        max-width: 100%;
        max-height: 200px;
        border-radius: 8px;
        object-fit: contain;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .remove-image-button { /* Make it more prominent or fit better */
        margin-top: 0.75rem;
        background-color: var(--secondary) !important;
        color: white !important;
        border: none;
    }
    .remove-image-button:hover:not(:disabled) {
        background-color: #a51f58 !important; /* Darker shade of secondary */
    }


    .form-label-inline {
        display: flex;
        align-items: center;
        font-weight: normal;
        color: var(--primary);
        cursor: pointer;
    }

    .form-checkbox {
        margin-right: 0.75rem;
        width: 1.2rem;
        height: 1.2rem;
        accent-color: var(--danger);
    }
    /* --- END STYLES FOR NEW FIELDS --- */

    .helper-text {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.875rem;
        margin-top: 0.5rem;
    }

    .editor-group .form-label {
        margin-bottom: 0.75rem;
    }

    .action-buttons {
        display: flex;
        gap: 1.5rem;
        margin-top: 2.5rem;
        justify-content: flex-end;
    }

    .button {
        padding: 0.85rem 2rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        font-family: "orbital", sans-serif;
        position: relative;
        overflow: hidden;
        display: inline-block;
    }
    .button.tiny-button { /* For smaller buttons like remove image */
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }

    .button::after {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.8);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }

    .button:focus:not(:active)::after {
        animation: ripple 1s ease-out;
    }

    @keyframes ripple {
        0% {
            transform: scale(0, 0);
            opacity: 0.5;
        }
        20% {
            transform: scale(25, 25);
            opacity: 0.3;
        }
        100% {
            opacity: 0;
            transform: scale(40, 40);
        }
    }

    .button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .button:active:not(:disabled) {
        transform: translateY(2px);
    }

    .primary-button {
        background-color: var(--danger);
        color: var(--dark-bg);
        box-shadow: 0 4px 6px rgba(0, 221, 135, 0.2);
    }

    .primary-button:hover:not(:disabled) {
        background-color: #00c67a;
        box-shadow: 0 6px 10px rgba(0, 221, 135, 0.3);
    }

    .secondary-button {
        background-color: transparent;
        color: var(--primary);
        border: 2px solid var(--primary);
    }

    .secondary-button:hover:not(:disabled) {
        background-color: rgba(250, 235, 215, 0.1);
        border-color: var(--danger);
        color: var(--danger);
    }

    .back-link {
        display: inline-block;
        margin-top: 2rem;
        color: var(--danger);
        text-decoration: none;
        font-weight: 600;
        position: relative;
        padding-left: 1.5rem;
    }

    .back-link::before {
        content: "←";
        position: absolute;
        left: 0;
        transition: transform 0.3s ease;
    }

    .back-link:hover::before {
        transform: translateX(-5px);
    }

    .back-link:hover {
        text-decoration: none;
        color: #00c67a;
    }

    .error-message, .loading-message {
        text-align: center;
        font-size: 1.2rem;
        color: var(--primary);
        margin-top: 3rem;
        animation-name: heroZoom;
        animation-duration: 1s;
    }

    .error-alert {
        background-color: rgba(220, 53, 69, 0.1);
        color: #ff8a8a;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        animation-name: infoSlideRight;
        animation-duration: 1s;
    }

    /* Animation keyframes */
    @keyframes heroZoom {
        from {
            transform: scale(0.25);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }

    @keyframes infoSlideRight {
        from {
            position: relative;
            left: -100%;
            opacity: 0;
        }
        to {
            position: relative;
            left: 0%;
            opacity: 1;
        }
    }

    @keyframes infoSlideLeft {
        from {
            position: relative;
            left: 100%;
            opacity: 0;
        }
        to {
            position: relative;
            left: 0%;
            opacity: 1;
        }
    }

    /* Editor customization */
    :global(.codex-editor) {
        color: white !important;
        background: rgba(0, 34, 51, 0.4);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2);
    }

    :global(.ce-block__content) {
        color: white !important;
    }

    :global(.ce-toolbar__plus, .ce-toolbar__settings-btn) {
        color: var(--danger) !important;
        background: rgba(0, 34, 51, 0.7) !important;
    }

    :global(.ce-toolbar__plus:hover, .ce-toolbar__settings-btn:hover) {
        background: var(--danger) !important;
        color: var(--dark-bg) !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .page-container {
            padding: 1rem;
            margin: 2rem auto;
        }

        .admin-post-form-section {
            padding: 1.5rem;
        }

        .action-buttons {
            flex-direction: column;
            gap: 1rem;
        }

        .button {
            width: 100%;
        }
    }
</style>