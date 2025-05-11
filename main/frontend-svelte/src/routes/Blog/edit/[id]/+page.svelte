<script>
    import { getContext, onMount } from 'svelte';
    import { page } from '$app/stores';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import Editor from '$lib/components/Editor.svelte';
    import {getIdToken} from "firebase/auth";
    import {getClientAuth} from "$lib/firebase/firebase.client.js"; // Import the new component

    // Assuming your load function provides `post` data in `$page.data.post`
    const { data } = $page;
    const postFromLoad = data.post;
    let auth = getClientAuth();
    const isAdmin = getContext('isAdmin');

    let editorComponent; // Reference to the Editor component instance
    let isEditingView = false; // Controls UI switch between view and edit modes
    let postTitle = postFromLoad?.title || 'Untitled Post';

    // This will hold the structured content for the editor, parsed from postFromLoad.content
    let editorInitialContent = { blocks: [] };

    // Format date to readable format
    function formatDate(dateString) {
        if (!dateString) return 'Date not available';
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    }

    onMount(() => {
        if (browser && postFromLoad?.content) {
            try {
                if (typeof postFromLoad.content === 'string') {
                    const parsed = JSON.parse(postFromLoad.content);
                    if (parsed && parsed.blocks) {
                        editorInitialContent = parsed;
                    } else {
                        // If it's a simple string, wrap it in a paragraph for the editor
                        editorInitialContent = { blocks: [{ type: 'paragraph', data: { text: postFromLoad.content } }] };
                    }
                } else if (postFromLoad.content && postFromLoad.content.blocks) { // Already an object
                    editorInitialContent = postFromLoad.content;
                }
            } catch (e) {
                console.error('Failed to parse post content:', e);
                editorInitialContent = { blocks: [{ type: 'paragraph', data: { text: "Error loading content. " + (typeof postFromLoad.content === 'string' ? postFromLoad.content : '') } }] };
            }
        } else if (browser && !postFromLoad) {
            console.error("Post data not found from load function.");
            // Optionally redirect or show an error message
            // goto('/Blog');
        }
    });

    function startEditing() {
        if ($isAdmin) {
            isEditingView = true;
        }
    }

    async function handleSavePost() {
        if (!editorComponent) {
            alert('Editor component is not available.');
            return;
        }
        try {
            const contentFromEditor = await editorComponent.getContent();

            if (!contentFromEditor) {
                alert('Failed to get content from editor or content is empty.');
                return;
            }

            const updatedPostPayload = {
                id: postFromLoad?.id,
                title: postTitle,
                content: contentFromEditor
                // You might want to include other fields if they can be updated
                // e.g., tags, category, summary etc.
            };

            if (!updatedPostPayload.id) {
                alert('Post ID is missing. Cannot save.');
                return;
            }

            console.log(updatedPostPayload);
            const idToken = await getIdToken(auth.currentUser);
            alert('Adding post via backend... Please wait.'); // User feedback
            // Replace with your actual API endpoint for updating posts
            const response = await fetch(`/api/v1/blog/posts`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json',
                    Authorization: `Bearer ${idToken}`
                },
                body: JSON.stringify(updatedPostPayload)
            });
            console.log(response)
            if (response.ok) {
                const result = await response.json(); // Assuming API returns updated post or success message
                console.log('Post updated successfully:', result);
                editorInitialContent = contentFromEditor; // Update the base content for the view mode
                isEditingView = false; // Switch back to view mode
                alert('Post updated!');
                // Optionally, update `postFromLoad` if your API returns the full updated post
                // and you want to refresh other displayed data without a page reload.
            } else {
                const errorText = await response.text();
                throw new Error(`Failed to update post: ${response.status} ${errorText}`);
            }
        } catch (error) {
            console.error('Error saving post:', error);
            alert(`Failed to save post. Details: ${error.message}`);
        }
    }

    function handleCancelEdit() {
        // Optionally, reset title if it was changed but not saved
        // postTitle = postFromLoad?.title || 'Untitled Post';
        isEditingView = false;
    }

    async function handleDeletePost() {
        if (!postFromLoad?.id) {
            alert('Post ID is missing. Cannot delete.');
            return;
        }
        if (confirm(`Are you sure you want to delete "${postFromLoad.title || 'this post'}"?`)) {
            try {
                const response = await fetch(`/api/v1/posts/${postFromLoad.id}`, { method: 'DELETE' });
                if (response.ok) {
                    alert('Post deleted successfully.');
                    goto('/Blog'); // Navigate to blog list
                } else {
                    const errorText = await response.text();
                    throw new Error(`Failed to delete post: ${response.status} ${errorText}`);
                }
            } catch (error) {
                console.error('Error deleting post:', error);
                alert(`Failed to delete post. Details: ${error.message}`);
            }
        }
    }

    function handleEditorEvents(event) {
        console.log(`Editor event: ${event.type}`, event.detail);
        if (event.type === 'error') {
            alert(`Editor Component Error: ${event.detail.message}`);
        }
    }

</script>

<div class="page-container">
    {#if browser && postFromLoad}
        {#if isEditingView && $isAdmin}
            <section class="edit-mode-section">
                <h1 class="page-title">Edit Post</h1>
                <div class="form-group title-group">
                    <label for="postTitleInput" class="form-label">Post Title:</label>
                    <input id="postTitleInput" type="text" bind:value={postTitle} class="form-input title-input" placeholder="Enter Post Title" />
                </div>

                <div class="form-group editor-group">
                    <label class="form-label">Content:</label>
                    <Editor
                            bind:this={editorComponent}
                            initialData={editorInitialContent}
                            readOnly={false}
                            on:error={handleEditorEvents}
                            on:ready={handleEditorEvents}
                            on:change={handleEditorEvents}
                            on:image-upload-start={(e) => console.log('Image upload started:', e.detail.file.name)}
                            on:image-upload-success={(e) => console.log('Image uploaded:', e.detail.file.url, 'Temporary:', e.detail.isTemporary)}
                    />
                </div>

                <div class="action-buttons">
                    <button on:click={handleSavePost} class="button primary-button">Save Changes</button>
                    <button on:click={handleCancelEdit} class="button secondary-button">Cancel</button>
                </div>
            </section>
        {:else}
            <article class="view-mode-article">
                <header class="post-header">
                    <h1 class="post-title-view">{postTitle}</h1>
                    <p class="post-meta-view">
                        Published: {formatDate(postFromLoad.publishedAt)}
                        {#if postFromLoad.readTime} • {postFromLoad.readTime} min read{/if}
                    </p>
                </header>

                {#if $isAdmin}
                    <div class="admin-actions-view">
                        <button on:click={startEditing} class="button primary-button small-button">Edit Post</button>
                        <button on:click={handleDeletePost} class="button danger-button small-button">Delete Post</button>
                    </div>
                {/if}

                <section class="post-content-view">
                    <Editor
                            initialData={editorInitialContent}
                            readOnly={true}
                            on:error={handleEditorEvents}
                    />
                </section>
                <a href="/Blog" class="back-link">← Back to Blog List</a>
            </article>
        {/if}
    {:else if browser && !postFromLoad}
        <p class="error-message">Post not found. It might have been deleted or the link is incorrect.</p>
        <a href="/Blog" class="back-link">← Go to Blog List</a>
    {:else}
        <p class="loading-message">Loading post data...</p>
    {/if}
</div>

<style>
    .page-container {
        max-width: 960px;
        margin: 3rem auto;
        padding: 1.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .page-title { color: #333; margin-bottom: 1.5rem; font-size: 2rem; }

    /* Edit Mode Styles */
    .edit-mode-section { background-color: #f9f9f9; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .form-group { margin-bottom: 1.5rem; }
    .form-label { display: block; font-weight: 600; margin-bottom: 0.5rem; color: #444; }
    .form-input { width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 1rem; }
    .title-input { font-size: 1.5rem; font-weight: bold; }
    .editor-group .form-label { margin-bottom: 0.75rem; } /* More space before editor */

    /* View Mode Styles */
    .view-mode-article { }
    .post-header { margin-bottom: 2rem; padding-bottom:1.5rem; border-bottom: 1px solid #eee; }
    .post-title-view { font-size: 2.8rem; color: #2c3e50; margin-bottom: 0.5rem; line-height: 1.2; }
    .post-meta-view { color: #7f8c8d; font-size: 0.95rem; }
    .admin-actions-view { margin-bottom: 2rem; display:flex; gap: 0.75rem; }
    .post-content-view { line-height: 1.7; color: #34495e; font-size: 1.1rem; }
    /* Styles for Editor.js blocks in read-only will come from Editor.svelte or global styles */

    /* Action Buttons */
    .action-buttons, .admin-actions-view { display: flex; gap: 1rem; margin-top: 2rem; }
    .button { padding: 0.75rem 1.5rem; border: none; border-radius: 5px; cursor: pointer; font-weight: 500; font-size: 0.95rem; transition: background-color 0.2s ease, transform 0.1s ease; }
    .button:active { transform: translateY(1px); }
    .primary-button { background-color: #007bff; color: white; }
    .primary-button:hover { background-color: #0056b3; }
    .secondary-button { background-color: #6c757d; color: white; }
    .secondary-button:hover { background-color: #545b62; }
    .danger-button { background-color: #dc3545; color: white; }
    .danger-button:hover { background-color: #c82333; }
    .small-button { padding: 0.5rem 1rem; font-size: 0.85rem; }


    .back-link { display: inline-block; margin-top: 2rem; color: #007bff; text-decoration: none; }
    .back-link:hover { text-decoration: underline; }
    .error-message, .loading-message { text-align: center; font-size: 1.2rem; color: #777; margin-top: 3rem; }
</style>