<script lang="ts">
    import { getContext, onMount } from 'svelte';
    import { page } from '$app/stores';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import Editor from '$lib/components/Editor.svelte'; // Your Svelte Editor component
    import { getIdToken } from "firebase/auth";
    import { getClientAuth } from "$lib/firebase/firebase.client.js";

    const auth = getClientAuth();
    const isAdmin = getContext('isAdmin'); // Assuming 'isAdmin' is a Svelte store from context

    // Data from the load function in +page.ts
    export let data: any; 
    let post = data.post;
    const isNewPost = data.isNew;

    let editorComponent: Editor; // Reference to the Editor component instance
    let postTitle = post?.title || '';
    let editorInitialContent = post?.content || { blocks: [{ type: 'paragraph', data: { text: 'Start writing your blog post here...' } }] };
    
    let isLoading = false;
    let errorMessage = '';
    let selectedCategory = post?.category || ''; // Initialize with post's category if editing
    let categories = [];
    let isImageUploading = false;

    let pageTitle = isNewPost ? "Create New Blog Post" : "Edit Post";

    onMount(async () => {
        if (browser && !$isAdmin) {
            goto('/Blog'); // Redirect if not admin
            return;
        }
        
        // Ensure content is in the correct format for the editor, especially for existing posts
        if (!isNewPost && post?.content) {
            if (typeof post.content === 'string') {
                try {
                    const parsed = JSON.parse(post.content);
                    if (parsed && parsed.blocks) {
                        editorInitialContent = parsed;
                    } else {
                        editorInitialContent = { blocks: [{ type: 'paragraph', data: { text: post.content } }] };
                    }
                } catch (e) {
                    console.error('Failed to parse existing post content for editor:', e);
                    editorInitialContent = { blocks: [{ type: 'paragraph', data: { text: "Error loading content. " + post.content } }] };
                }
            } else if (post.content && post.content.blocks) {
                editorInitialContent = post.content;
            }
        }
        
        if (browser) {
            await fetchCategories();
            if (!isNewPost && post?.category && categories.some(c => c.slug === post.category)) {
                selectedCategory = post.category;
            } else if (categories.length > 0 && !selectedCategory) {
                 // selectedCategory = categories[0].slug; // Default to first category if not set
            }
        }
    });

    async function fetchCategories() {
        try {
            const response = await fetch('/api/v1/blog/categories');
            if (response.ok) {
                categories = await response.json();
                if (categories.length > 0 && !selectedCategory && isNewPost) { // Default for new posts only if not already set
                    selectedCategory = categories[0].slug;
                }
            } else {
                errorMessage = 'Failed to load categories. Please try again.';
                console.error(errorMessage);
            }
        } catch (error: any) {
            errorMessage = `Failed to load categories: ${error.message}`;
            console.error(errorMessage, error);
        }
    }

    function calculateReadTime(editorContent: any, wordsPerMinute = 250, secondsPerImage = 10) {
        let totalWords = 0;
        let imageCount = 0;
        if (!editorContent || !editorContent.blocks) return 1;

        editorContent.blocks.forEach((block: any) => {
            switch (block.type) {
                case 'paragraph':
                case 'header':
                    if (block.data && block.data.text) {
                        const plainText = block.data.text.replace(/<[^>]*>/g, ' ');
                        totalWords += plainText.split(/\s+/).filter((word: string) => word.length > 0).length;
                    }
                    break;
                case 'list':
                    if (block.data && block.data.items) {
                        block.data.items.forEach((item: any) => {
                            const plainText = (typeof item === 'string' ? item : item.content || '').replace(/<[^>]*>/g, ' ');
                            totalWords += plainText.split(/\s+/).filter((word: string) => word.length > 0).length;
                        });
                    }
                    break;
                case 'image':
                    imageCount++;
                    if (block.data && block.data.caption) {
                        totalWords += block.data.caption.split(/\s+/).filter((word: string) => word.length > 0).length;
                    }
                    break;
                case 'quote':
                     if (block.data && block.data.text) {
                        const plainText = block.data.text.replace(/<[^>]*>/g, ' ');
                        totalWords += plainText.split(/\s+/).filter((word: string) => word.length > 0).length;
                    }
                    if (block.data && block.data.caption) {
                        totalWords += block.data.caption.split(/\s+/).filter((word: string) => word.length > 0).length;
                    }
                    break;
                default:
                    if (block.data && block.data.text) { // Fallback for other blocks with text
                        const plainText = block.data.text.replace(/<[^>]*>/g, ' ');
                        totalWords += plainText.split(/\s+/).filter((word: string) => word.length > 0).length;
                    }
                    break;
            }
        });
        const textTimeMinutes = totalWords / wordsPerMinute;
        const imageTimeMinutes = (imageCount * secondsPerImage) / 60;
        return Math.max(1, Math.ceil(textTimeMinutes + imageTimeMinutes));
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

        isLoading = true;
        errorMessage = '';
        try {
            const contentFromEditor = await editorComponent.getContent();
            if (!contentFromEditor || !contentFromEditor.blocks || contentFromEditor.blocks.length === 0) {
                alert('Post content cannot be empty.');
                isLoading = false;
                return;
            }

            const readTimeData = calculateReadTime(contentFromEditor);
            let payload: any = {
                title: postTitle,
                content: contentFromEditor,
                category: selectedCategory,
                readTime: readTimeData,
                // Add other common fields like excerpt, imageUrl if your form supports them
            };

            let method = 'POST';
            let url = `/api/v1/blog/posts`;

            if (!isNewPost) {
                payload.id = post.id; // Add ID for updates
                method = 'PUT';
            } else {
                // For new posts, you might want to set publishedAt, or let backend do it
                // payload.publishedAt = new Date().toISOString();
            }
            
            if (!auth.currentUser) {
                alert("User not authenticated. Please log in.");
                isLoading = false;
                return;
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
                goto('/Blog'); // Or to the viewed post: `/Blog/post/${result.slug || result.id}`
            } else {
                const errorText = await response.text();
                throw new Error(`Failed to ${isNewPost ? 'create' : 'update'} post: ${response.status} ${errorText}`);
            }
        } catch (error: any) {
            errorMessage = `Failed to save post. Details: ${error.message}`;
            console.error(errorMessage, error);
            alert(errorMessage);
        } finally {
            isLoading = false;
        }
    }

    function handleCancel() {
        if (confirm('Are you sure you want to discard changes?')) {
            goto(isNewPost ? '/Blog' : `/Blog/${post.slug}`); // Or just /Blog for both
        }
    }

    function handleEditorEvents(event: any) {
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
            <h1 class="page-title">{pageTitle}</h1>

            {#if errorMessage}
                <div class="error-alert">{errorMessage}</div>
            {/if}

            <div class="form-group title-group">
                <label for="postTitleInput" class="form-label">Post Title:</label>
                <input id="postTitleInput" type="text" bind:value={postTitle} class="form-input title-input" placeholder="Enter Post Title" />
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
            
            <!-- You might want to add other fields here like excerpt, featured image URL input etc. -->

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
                    on:image-upload-start={(e) => { console.log('Image upload started:', e.detail.file.name); isImageUploading = true; }}
                    on:image-upload-success={(e) => { console.log('Image uploaded:', e.detail.file.url, 'Temporary:', e.detail.isTemporary); isImageUploading = false; }}
                    on:image-upload-error={(e) => { console.error('Image upload error:', e.detail.message); isImageUploading = false; errorMessage = `Image upload failed: ${e.detail.message}`; alert(errorMessage);}}
                />
            </div>

            <div class="action-buttons">
                <button on:click={handleSavePost} class="button primary-button" disabled={isLoading || categories.length === 0 || isImageUploading}>
                    {isLoading ? 'Saving...' : (isImageUploading ? 'Uploading Image...' : (isNewPost ? 'Publish Post' : 'Save Changes'))}
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

<style>
    .page-container { max-width: 960px; margin: 3rem auto; padding: 1.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .page-title { color: #333; margin-bottom: 1.5rem; font-size: 2rem; }
    .admin-post-form-section { background-color: #f9f9f9; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .form-group { margin-bottom: 1.5rem; }
    .form-label { display: block; font-weight: 600; margin-bottom: 0.5rem; color: #444; }
    .form-input { width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 1rem; }
    .title-input { font-size: 1.5rem; font-weight: bold; }
    .category-select { background-color: white; }
    .helper-text { color: #6c757d; font-size: 0.875rem; margin-top: 0.5rem; }
    .editor-group .form-label { margin-bottom: 0.75rem; }
    .action-buttons { display: flex; gap: 1rem; margin-top: 2rem; }
    .button { padding: 0.75rem 1.5rem; border: none; border-radius: 5px; cursor: pointer; font-weight: 500; font-size: 0.95rem; transition: background-color 0.2s ease, transform 0.1s ease; }
    .button:disabled { opacity: 0.6; cursor: not-allowed; }
    .button:active:not(:disabled) { transform: translateY(1px); }
    .primary-button { background-color: #007bff; color: white; }
    .primary-button:hover:not(:disabled) { background-color: #0056b3; }
    .secondary-button { background-color: #6c757d; color: white; }
    .secondary-button:hover:not(:disabled) { background-color: #545b62; }
    .back-link { display: inline-block; margin-top: 2rem; color: #007bff; text-decoration: none; }
    .back-link:hover { text-decoration: underline; }
    .error-message, .loading-message { text-align: center; font-size: 1.2rem; color: #777; margin-top: 3rem; }
    .error-alert { background-color: #f8d7da; color: #721c24; padding: 1rem; margin-bottom: 1.5rem; border-radius: 4px; border-left: 4px solid #dc3545; }
</style>
