<script>
    import { getContext, onMount } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import Editor from '$lib/components/Editor.svelte';
    import { getIdToken } from "firebase/auth";
    import { getClientAuth } from "$lib/firebase/firebase.client.js";

    let auth = getClientAuth();
    const isAdmin = getContext('isAdmin');

    let editorComponent; // Reference to the Editor component instance
    let postTitle = '';
    let isLoading = false;
    let errorMessage = '';
    let selectedCategory = ''; // New state for category selection
    let categories = []; // Will hold available categories
    let isImageUploading = false; // New state to track image uploads

    // Initialize empty editor content
    let editorInitialContent = {
        blocks: [
            {
                type: 'paragraph',
                data: {
                    text: 'Start writing your blog post here...'
                }
            }
        ]
    };

    onMount(async () => {
        // Check if user is admin, if not redirect to blog list
        if (browser && !$isAdmin) {
            goto('/Blog');
        }

        // Fetch categories on component mount
        if (browser && $isAdmin) {
            await fetchCategories();
        }
    });

    // Function to fetch categories from the backend
    async function fetchCategories() {
        try {
            const response = await fetch('/api/v1/blog/categories');

            if (response.ok) {
                categories = await response.json();
                console.log(categories)
                // Set the first category as default if available
                if (categories.length > 0) {
                    selectedCategory = categories[0].slug; // Ensure you are using category.slug if that's what your backend expects for saving
                }
            } else {
                console.error('Failed to fetch categories');
                errorMessage = 'Failed to load categories. Please try again.';
            }
        } catch (error) {
            console.error('Error fetching categories:', error);
            errorMessage = `Failed to load categories: ${error.message}`;
        }
    }

    async function handleSavePost() {
        if (!editorComponent) {
            alert('Editor component is not available.');
            return;
        }

        if (!postTitle.trim()) {
            alert('Please enter a post title.');
            return;
        }

        if (!selectedCategory) {
            alert('Please select a category.');
            return;
        }

        if (isImageUploading) {
            alert('An image is currently uploading. Please wait.');
            return;
        }

        try {
            isLoading = true;
            errorMessage = '';
            const contentFromEditor = await editorComponent.getContent();

            if (!contentFromEditor || !contentFromEditor.blocks || contentFromEditor.blocks.length === 0) {
                alert('Post content cannot be empty.');
                isLoading = false;
                return;
            }
            console.log("Content from editor for saving:", contentFromEditor); // Log the content
            const readTimeData = calculateReadTime(contentFromEditor);

            const newPostPayload = {
                title: postTitle,
                content: contentFromEditor,
                category:selectedCategory, 
                readTime:readTimeData,
                // publishedAt is typically set by the backend on creation,
                // but if you need to send it from frontend:
                // publishedAt: new Date().toISOString() 
                // Ensure your Post model in backend and service handle this
            };

            const idToken = await getIdToken(auth.currentUser);

            const response = await fetch(`/api/v1/blog/posts`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${idToken}`
                },
                body: JSON.stringify(newPostPayload)
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Post created successfully:', result);
                alert('Post published successfully!');
                goto('/Blog');
            } else {
                const errorText = await response.text();
                throw new Error(`Failed to create post: ${response.status} ${errorText}`);
            }
        } catch (error) {
            console.error('Error creating post:', error);
            errorMessage = `Failed to save post. Details: ${error.message}`;
            alert(errorMessage);
        } finally {
            isLoading = false;
        }
    }

    function calculateReadTime(editorContent, wordsPerMinute = 250, secondsPerImage = 10) {
        let totalWords = 0;
        let imageCount = 0;

        editorContent.blocks.forEach(block => {
            switch (block.type) {
                case 'paragraph':
                    if (block.data && block.data.text) {
                        const plainText = block.data.text.replace(/<[^>]*>/g, ' ');
                        const words = plainText.split(/\s+/).filter(word => word.length > 0);
                        totalWords += words.length;
                    }
                    break;
                case 'header':
                    if (block.data && block.data.text) {
                        const words = block.data.text.split(/\s+/).filter(word => word.length > 0);
                        totalWords += words.length;
                    }
                    break;
                case 'list':
                    if (block.data && block.data.items) {
                        block.data.items.forEach(item => {
                            const plainText = typeof item === 'string'
                                ? item.replace(/<[^>]*>/g, ' ')
                                : item.content ? item.content.replace(/<[^>]*>/g, ' ') : '';
                            const words = plainText.split(/\s+/).filter(word => word.length > 0);
                            totalWords += words.length;
                        });
                    }
                    break;
                case 'image':
                    imageCount++;
                    // The URL in block.data.file.url should be the server URL after successful upload
                    // If it's a blob URL here, the save happened too soon.
                    console.log("Image block data for read time calc:", block.data); 
                    if (block.data && block.data.caption) {
                        const captionWords = block.data.caption.split(/\s+/).filter(word => word.length > 0);
                        totalWords += captionWords.length;
                    }
                    break;
                case 'quote':
                    if (block.data && block.data.text) {
                        const plainText = block.data.text.replace(/<[^>]*>/g, ' ');
                        const words = plainText.split(/\s+/).filter(word => word.length > 0);
                        totalWords += words.length;
                    }
                    if (block.data && block.data.caption) {
                        const captionWords = block.data.caption.split(/\s+/).filter(word => word.length > 0);
                        totalWords += captionWords.length;
                    }
                    break;
                default:
                    if (block.data && block.data.text) {
                        const plainText = block.data.text.replace(/<[^>]*>/g, ' ');
                        const words = plainText.split(/\s+/).filter(word => word.length > 0);
                        totalWords += words.length;
                    }
                    break;
            }
        });

        const textTimeMinutes = totalWords / wordsPerMinute;
        const imageTimeMinutes = (imageCount * secondsPerImage) / 60;
        const totalReadTimeMinutes = textTimeMinutes + imageTimeMinutes;
        const readTimeMinutes = Math.max(1, Math.ceil(totalReadTimeMinutes));
        return readTimeMinutes;
    }

    function handleCancelCreate() {
        if (confirm('Are you sure you want to discard this post?')) {
            goto('/Blog');
        }
    }

    function handleEditorEvents(event) {
        console.log(`Editor event: ${event.type}`, event.detail);
        if (event.type === 'error') {
            errorMessage = `Editor Component Error: ${event.detail.message}`;
            alert(errorMessage);
        }
    }
</script>

<div class="page-container">
    {#if browser && $isAdmin}
        <section class="create-mode-section">
            <h1 class="page-title">Create New Blog Post</h1>

            {#if errorMessage}
                <div class="error-alert">
                    {errorMessage}
                </div>
            {/if}

            <div class="form-group title-group">
                <label for="postTitleInput" class="form-label">Post Title:</label>
                <input
                        id="postTitleInput"
                        type="text"
                        bind:value={postTitle}
                        class="form-input title-input"
                        placeholder="Enter Post Title"
                />
            </div>

            <div class="form-group category-group">
                <label for="categorySelect" class="form-label">Category:</label>
                <select
                        id="categorySelect"
                        bind:value={selectedCategory}
                        class="form-input category-select"
                        required
                >
                    <option value="" disabled>Select a category</option>
                    {#each categories as category}
                        <option value={category.slug}>{category.name}</option>
                    {/each}
                </select>
                {#if categories.length === 0}
                    <p class="helper-text">Loading categories...</p>
                {/if}
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
                        on:image-upload-start={(e) => {
                            console.log('Image upload started:', e.detail.file.name);
                            isImageUploading = true;
                        }}
                        on:image-upload-success={(e) => {
                            console.log('Image uploaded:', e.detail.file.url, 'Temporary:', e.detail.isTemporary);
                            // EditorJS ImageTool should internally update the block with the new URL.
                            // We just need to know the upload is done.
                            isImageUploading = false;
                        }}
                        on:image-upload-error={(e) => {
                            console.error('Image upload error:', e.detail.message);
                            isImageUploading = false;
                            errorMessage = `Image upload failed: ${e.detail.message}. Please try removing and re-uploading the image.`;
                            alert(errorMessage);
                        }}
                />
            </div>

            <div class="action-buttons">
                <button
                        on:click={handleSavePost}
                        class="button primary-button"
                        disabled={isLoading || categories.length === 0 || isImageUploading}
                >
                    {isLoading ? 'Publishing...' : (isImageUploading ? 'Uploading Image...' : 'Publish Post')}
                </button>
                <button
                        on:click={handleCancelCreate}
                        class="button secondary-button"
                        disabled={isLoading}
                >
                    Cancel
                </button>
            </div>
        </section>
    {:else if browser && !$isAdmin}
        <p class="error-message">You don't have permission to create posts.</p>
        <a href="/Blog" class="back-link">← Go to Blog List</a>
    {:else}
        <p class="loading-message">Loading...</p>
    {/if}
</div>

<style>
    .page-container {
        max-width: 960px;
        margin: 10rem auto;
        padding: 1.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .page-title {
        color: #333;
        margin-bottom: 1.5rem;
        font-size: 2rem;
    }

    /* Create Mode Styles */
    .create-mode-section {
        background-color: #f9f9f9;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .form-group {
        margin-bottom: 1.5rem;
    }
    .form-label {
        display: block;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #444;
    }
    .form-input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
        font-size: 1rem;
    }
    .title-input {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .category-select {
        background-color: white;
    }
    .helper-text {
        color: #6c757d;
        font-size: 0.875rem;
        margin-top: 0.5rem;
    }
    .editor-group .form-label {
        margin-bottom: 0.75rem;
    }

    /* Action Buttons */
    .action-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 2rem;
    }
    .button {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: 500;
        font-size: 0.95rem;
        transition: background-color 0.2s ease, transform 0.1s ease;
    }
    .button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    .button:active:not(:disabled) {
        transform: translateY(1px);
    }
    .primary-button {
        background-color: #007bff;
        color: white;
    }
    .primary-button:hover:not(:disabled) {
        background-color: #0056b3;
    }
    .secondary-button {
        background-color: #6c757d;
        color: white;
    }
    .secondary-button:hover:not(:disabled) {
        background-color: #545b62;
    }

    .back-link {
        display: inline-block;
        margin-top: 2rem;
        color: #007bff;
        text-decoration: none;
    }
    .back-link:hover {
        text-decoration: underline;
    }
    .error-message, .loading-message {
        text-align: center;
        font-size: 1.2rem;
        color: #777;
        margin-top: 3rem;
    }
    .error-alert {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border-radius: 4px;
        border-left: 4px solid #dc3545;
    }
</style>
