<script lang="ts">
    import { onMount } from 'svelte';
    import axios from 'axios';
    // Removed: import { writable } from 'svelte/store'; // We'll use $state for comments array
    import { currentUser as firebaseUserStore } from '$lib/firebase/firebase.client';
    import type { User as FirebaseUser } from 'firebase/auth';

    let { postId,postTitle } = $props<{ postId: string; postTitle:string; }>();

    type Author = {
        name: string;
        avatar: string; // Placeholder, assuming you might use actual URLs
    };

    type Comment = {
        id: string;
        content: string;
        createdAt: string;
        author: Author;
        authorId: string;
        replies?: Comment[];
        parentId?: string | null;
        isReplying?: boolean;
        replyContent?: string;
        isEditing?: boolean; // For edit functionality
    };

    // --- Svelte 5 State ---
    let comments = $state<Comment[]>([]); // Using $state for the comments array
    let isLoading = $state(true);
    let error = $state<string | null>(null);
    let newCommentContent = $state('');
    let isSubmittingComment = $state(false);
    let loggedInUser = $state<FirebaseUser | null>(null);
    let editingCommentId = $state<string | null>(null); // Track which comment is being edited
    let editContent = $state(''); // Content for the comment being edited

    let unsubscribeFromFirebase: (() => void) | undefined;

    // --- Standalone function to fetch comments ---
    async function fetchCommentsData(idToFetch: string) {
        if (!idToFetch) {
            console.warn("CommentsSection: No postId to fetch, clearing comments.");
            comments = [];
            isLoading = false;
            return;
        }
        console.log(`%cCommentsSection S5: Initiating fetch for postId: ${idToFetch}`, "color: blue;");
        isLoading = true;
        error = null;
        try {
            const response = await axios.get(`/api/v1/blog/posts/${idToFetch}/comments`);
            if (response.data && Array.isArray(response.data)) {
                const commentsData: Comment[] = response.data;
                const sortedTopLevelComments = commentsData.sort(
                    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
                );
                comments = addFrontendState(sortedTopLevelComments);
                console.log(`CommentsSection S5: Fetched ${comments.length} top-level comments for ${idToFetch}.`);
            } else {
                comments = [];
                console.log(`CommentsSection S5: No comments data array for ${idToFetch}.`);
            }
        } catch (err: any) {
            console.error(`Error fetching comments for postId ${idToFetch}:`, err);
            error = err.response?.data?.message || "Could not load comments.";
            comments = [];
        } finally {
            isLoading = false;
        }
    }

    // --- $effect for fetching comments when postId changes ---
    $effect(() => {
        const currentPostId = postId;
        console.log(`%cCommentsSection S5 $EFFECT for postId - Triggered. Current postId: ${currentPostId}`, "color: green; font-weight: bold;");
        fetchCommentsData(currentPostId); // Will handle if currentPostId is null/undefined
    });

    // --- onMount for Firebase auth subscription ---
    onMount(() => {
        console.log("CommentsSection S5 ONMOUNT: Setting up Firebase listener.");
        unsubscribeFromFirebase = firebaseUserStore.subscribe(user => {
            loggedInUser = user;
        });
        return () => {
            if (unsubscribeFromFirebase) {
                unsubscribeFromFirebase();
            }
        };
    });

    // --- Helper function to add initial UI state to comments ---
    function addFrontendState(commentList: Comment[]): Comment[] {
        return commentList.map(comment => ({
            ...comment,
            isReplying: false,
            replyContent: '',
            isEditing: false,
            replies: comment.replies ? addFrontendState(comment.replies) : [] // Recursively for replies
        }));
    }
    // --- Comment Submission ---
    async function handleSubmitComment(parentId: string | null = null, contentToSubmit: string, forCommentIdToReset?: string) {
        if (!contentToSubmit.trim()) return;
        if (!loggedInUser || !loggedInUser.uid) {
            alert("You must be logged in to comment.");
            return;
        }
        isSubmittingComment = true;
        try {
            // --- MODIFICATION START ---
            // Construct the payload according to backend expectations
            const payload: { content: string; parent?: { id: string } } = {
                content: contentToSubmit
            };

            if (parentId) {
                payload.parent = { id: parentId };
            }
            // --- MODIFICATION END ---

            const token = await loggedInUser.getIdToken();
            // The postId is correctly sent in the URL
            await axios.post( `/api/v1/blog/posts/${postId}/comments`, payload, { headers: { Authorization: `Bearer ${token}` } });
            await fetchCommentsData(postId); // Refresh list

            if (parentId && forCommentIdToReset) {
                // Find the comment that was replied to and reset its UI state
                // This might need a more robust way to find nested comments if you reply to replies.
                // For now, assuming findAndResetReplyUIState handles one level or fetchCommentsData resets all.
                comments = comments.map(c => findAndResetReplyUIState(c, forCommentIdToReset, 'reply'));
            } else {
                newCommentContent = ''; // Clear top-level comment input
            }
        } catch (err: any) {
            console.error(`Error submitting comment (parentId: ${parentId}):`, err);
            let errorMessage = "Could not submit comment.";
            if (err.response && err.response.data && err.response.data.message) {
                errorMessage = `Failed to submit comment: ${err.response.data.message}`;
            } else if (err.message) {
                errorMessage = `Failed to submit comment: ${err.message}`;
            }
            alert(errorMessage);
            // If it was a reply and failed, you might want to ensure the reply form is still visible
            // or reset `isReplying` to false if appropriate.
            // For now, fetchCommentsData() on success or manual reset on error will handle UI.
        }
        finally { isSubmittingComment = false; }
    }

    // --- Edit Comment Logic ---
    function startEditComment(comment: Comment) {
        editingCommentId = comment.id;
        editContent = comment.content; // Pre-fill edit form
        // Close any open reply forms
        comments = comments.map(c => findAndResetReplyUIState(c, null, 'reply'));
    }

    async function handleSaveEdit(commentId: string) {
        if (!editContent.trim()) return;
        if (!loggedInUser) return;

        isSubmittingComment = true; // Reuse submitting state or add a specific editing state
        try {
            const token = await loggedInUser.getIdToken();
            // Assuming your API endpoint for updating is PUT /api/v1/blog/posts/{postId}/comments/{commentId}
            await axios.put(
                `/api/v1/blog/posts/${postId}/comments/${commentId}`,
                { content: editContent },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            await fetchCommentsData(postId); // Refresh comments list
            editingCommentId = null; // Exit editing mode
            editContent = '';
        } catch (err: any) {
            console.error("Error saving edited comment:", err);
            alert(err.response?.data?.message || "Failed to save comment.");
        } finally {
            isSubmittingComment = false;
        }
    }

    function cancelEdit() {
        editingCommentId = null;
        editContent = '';
    }

    // --- Delete Comment Logic ---
    async function handleDeleteComment(commentId: string) {
        if (!loggedInUser) return;
        if (confirm("Are you sure you want to delete this comment? This action cannot be undone.")) {
            isSubmittingComment = true; // Reuse or use specific deleting state
            try {
                const token = await loggedInUser.getIdToken();
                // Assuming API endpoint DELETE /api/v1/blog/posts/{postId}/comments/{commentId}
                await axios.delete(`/api/v1/blog/posts/${postId}/comments/${commentId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                await fetchCommentsData(postId); // Refresh comments
            } catch (err: any) {
                console.error("Error deleting comment:", err);
                alert(err.response?.data?.message || "Failed to delete comment.");
            } finally {
                isSubmittingComment = false;
            }
        }
    }

    // --- UI State Helpers for Replies/Edits (Recursive) ---
    function findAndResetReplyUIState(comment: Comment, targetId: string | null, type: 'reply' | 'edit'): Comment {
        let updatedComment = { ...comment };
        if (type === 'reply') {
            updatedComment.isReplying = (targetId === comment.id) ? !comment.isReplying : false;
            if (updatedComment.isReplying) updatedComment.replyContent = '';
        }
        // Could add similar logic for `isEditing` if needed globally, but edit is handled by `editingCommentId`
        if (updatedComment.replies && updatedComment.replies.length > 0) {
            updatedComment.replies = updatedComment.replies.map(reply => findAndResetReplyUIState(reply, targetId, type));
        }
        return updatedComment;
    }

    function toggleReplyForm(commentId: string) {
        editingCommentId = null; // Close edit form if open
        comments = comments.map(c => findAndResetReplyUIState(c, commentId, 'reply'));
    }

    function formatDate(dateString: string): string {
        return new Date(dateString).toLocaleString(undefined, {
            year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
        });
    }
</script>

<section class="comments-section">
    <h2 class="comments-title">Comments ({comments.reduce((acc, c) => acc + 1 + (c.replies?.length || 0), 0)})</h2>

    {#if loggedInUser && loggedInUser.uid}
        <div class="comment-form new-comment-form">
            <textarea bind:value={newCommentContent} placeholder="Write a comment..." rows="3" disabled={isSubmittingComment}></textarea>
            <button type="button" on:click={() => handleSubmitComment(null, newCommentContent)} disabled={isSubmittingComment || !newCommentContent.trim()}>
                {isSubmittingComment ? 'Submitting...' : 'Post Comment'}
            </button>
        </div>
    {:else}
        <p class="login-prompt text-info">Please <span class="text-secondary hover:underline">log in</span> to post a comment.</p>
    {/if}

    {#if isLoading}
        <div class="comments-loading">Loading comments for post ID: {postTitle}...</div>
    {:else if error}
        <div class="comments-error">{error} (while fetching for {postTitle})</div>
    {:else if comments.length === 0}
        <div class="no-comments">Be the first to comment! (on post {postTitle})</div>
    {:else}
        <ul class="comments-list">
            {#each comments as comment (comment.id)}
                <li class="comment-item">
                    {#if editingCommentId === comment.id}
                        <!-- Edit Form for this comment -->
                        <div class="comment-form edit-comment-form">
                            <textarea bind:value={editContent} rows="3" disabled={isSubmittingComment}></textarea>
                            <div class="edit-form-actions">
                                <button type="button" on:click={() => handleSaveEdit(comment.id)} disabled={isSubmittingComment || !editContent.trim()}>
                                    {isSubmittingComment ? 'Saving...' : 'Save Edit'}
                                </button>
                                <button type="button" class="cancel-button" on:click={cancelEdit} disabled={isSubmittingComment}>Cancel</button>
                            </div>
                        </div>
                    {:else}
                        <!-- Display Comment -->
                        <div class="comment-main">
                            <div class="comment-avatar-placeholder">
                                <span>{comment.author.name ? comment.author.name.substring(0,1).toUpperCase() : 'A'}</span>
                            </div>
                            <div class="comment-content">
                                <div class="comment-header">
                                    <span class="comment-author-name">{comment.author.name || 'Anonymous'}</span>
                                    <span class="comment-date">{formatDate(comment.createdAt)}</span>
                                </div>
                                <div class="comment-text">{@html comment.content}</div>
                                <div class="comment-actions">
                                    {#if loggedInUser && loggedInUser.uid && editingCommentId !== comment.id}
                                        <button class="reply-button" on:click={() => toggleReplyForm(comment.id)}>
                                            {comment.isReplying ? 'Cancel Reply' : 'Reply'}
                                        </button>
                                    {/if}
                                    {#if loggedInUser && loggedInUser.uid === comment.authorId && editingCommentId !== comment.id}
                                        <button class="edit-button" on:click={() => startEditComment(comment)}>Edit</button>
                                        <button class="delete-button" on:click={() => handleDeleteComment(comment.id)}>Delete</button>
                                    {/if}
                                </div>
                            </div>
                        </div>
                    {/if}

                    {#if comment.isReplying && editingCommentId !== comment.id}
                        <div class="comment-form reply-form">
                            <textarea bind:value={comment.replyContent} placeholder={`Replying to ${comment.author.name || 'Anonymous'}...`} rows="2" disabled={isSubmittingComment}></textarea>
                            <button type="button" on:click={() => handleSubmitComment(comment.id, comment.replyContent || '', comment.id)} disabled={isSubmittingComment || !(comment.replyContent || '').trim()}>
                                {isSubmittingComment ? 'Submitting...' : 'Post Reply'}
                            </button>
                        </div>
                    {/if}

                    {#if comment.replies && comment.replies.length > 0 && editingCommentId !== comment.id}
                        <ul class="comments-list replies-list">
                            {#each comment.replies as reply (reply.id)}
                                <li class="comment-item reply-item">
                                    {#if editingCommentId === reply.id}
                                        <!-- Edit Form for this reply -->
                                        <div class="comment-form edit-comment-form">
                                            <textarea bind:value={editContent} rows="3" disabled={isSubmittingComment}></textarea>
                                            <div class="edit-form-actions">
                                                <button type="button" on:click={() => handleSaveEdit(reply.id)} disabled={isSubmittingComment || !editContent.trim()}>
                                                    {isSubmittingComment ? 'Saving...' : 'Save Edit'}
                                                </button>
                                                <button type="button" class="cancel-button" on:click={cancelEdit} disabled={isSubmittingComment}>Cancel</button>
                                            </div>
                                        </div>
                                    {:else}
                                        <!-- Display Reply -->
                                        <div class="comment-main">
                                            <div class="comment-avatar-placeholder reply-avatar-placeholder">
                                                <span>{reply.author.name ? reply.author.name.substring(0,1).toUpperCase() : 'A'}</span>
                                            </div>
                                            <div class="comment-content">
                                                <div class="comment-header">
                                                    <span class="comment-author-name">{reply.author.name || 'Anonymous'}</span>
                                                    <span class="comment-date">{formatDate(reply.createdAt)}</span>
                                                </div>
                                                <div class="comment-text">{@html reply.content}</div>
                                                <div class="comment-actions">
                                                    {#if loggedInUser && loggedInUser.uid && editingCommentId !== reply.id}
                                                        <button class="reply-button" on:click={() => toggleReplyForm(reply.id)}>
                                                            {reply.isReplying ? 'Cancel Reply' : 'Reply'}
                                                        </button>
                                                    {/if}
                                                    {#if loggedInUser && loggedInUser.uid === reply.authorId && editingCommentId !== reply.id}
                                                        <button class="edit-button" on:click={() => startEditComment(reply)}>Edit</button>
                                                        <button class="delete-button" on:click={() => handleDeleteComment(reply.id)}>Delete</button>
                                                    {/if}
                                                </div>
                                            </div>
                                        </div>
                                    {/if}

                                    {#if reply.isReplying && editingCommentId !== reply.id}
                                        <div class="comment-form reply-form nested-reply-form">
                                            <textarea bind:value={reply.replyContent} placeholder={`Replying to ${reply.author.name || 'Anonymous'}...`} rows="2" disabled={isSubmittingComment}></textarea>
                                            <button type="button" on:click={() => handleSubmitComment(reply.id, reply.replyContent || '', reply.id)} disabled={isSubmittingComment || !(reply.replyContent || '').trim()}>
                                                {isSubmittingComment ? 'Submitting...' : 'Post Reply'}
                                            </button>
                                        </div>
                                    {/if}
                                    <!-- TODO: Recursively render replies to replies if your data structure supports deeper nesting -->
                                </li>
                            {/each}
                        </ul>
                    {/if}
                </li>
            {/each}
        </ul>
    {/if}
</section>

<style>
    .comments-section {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border-color-dark, #445259);
    }
    .comments-title {
        font-family: var(--font-orbital-bold);
        font-size: 1.8rem;
        color: var(--primary-text-color, #faebd7);
        margin-bottom: 1.5rem;
    }

    .comment-form {
        margin-bottom: 1rem; /* Reduced margin for tighter spacing */
        background-color: var(--block-bg-dark, #0f3040);
        padding: 1rem;
        border-radius: 6px;
    }
    .new-comment-form {
        margin-bottom: 2rem; /* Original margin for the main new comment form */
    }
    .edit-comment-form {
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        border: 1px dashed var(--info-color); /* Highlight edit form */
    }
    .edit-form-actions {
        margin-top: 0.5rem;
        display: flex;
        gap: 0.5rem;
    }
    .edit-form-actions .cancel-button {
        background-color: var(--secondary-color);
    }
    .edit-form-actions .cancel-button:hover {
        background-color: #a51f58; /* Darker secondary */
    }


    .comment-form textarea {
        width: 100%;
        padding: 0.75rem;
        border-radius: 4px;
        border: 1px solid var(--border-color-dark, #445259);
        background-color: var(--block-bg-darker, #0a2a38);
        color: var(--primary-text-color, #faebd7);
        font-family: var(--font-orbital);
        margin-bottom: 0.75rem;
        resize: vertical;
        min-height: 60px;
    }
    .comment-form textarea:disabled {
        opacity: 0.7;
    }
    .comment-form button {
        font-family: var(--font-orbital);
        padding: 0.6rem 1.2rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        background-color: var(--info-color, #3e92cc);
        color: white;
        transition: background-color 0.2s ease;
    }
    .comment-form button:disabled {
        background-color: #555;
        cursor: not-allowed;
    }
    .comment-form button:not(:disabled):hover {
        background-color: var(--secondary-color, #c62368);
    }

    .login-prompt {
        padding: 1rem;
        background-color: var(--block-bg-dark, #0f3040);
        border-radius: 6px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-prompt a {
        color: var(--info-color);
        font-weight: bold;
    }


    .comments-loading, .comments-error, .no-comments {
        text-align: center;
        padding: 1.5rem;
        color: #a0a0a0;
        font-family: var(--font-orbital);
        background-color: var(--block-bg-darker, #0a2a38);
        border-radius: 6px;
    }
    .comment-avatar-placeholder {
        width: 40px; /* Slightly smaller */
        height: 40px;
        border-radius: 50%;
        background-color: var(--secondary-color, #c62368);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem; /* Adjusted */
        font-weight: bold;
        flex-shrink: 0;
        font-family: var(--font-orbital-bold);
    }
    .reply-avatar-placeholder {
        width: 32px;
        height: 32px;
        font-size: 1rem;
    }

    .comments-list { list-style: none; padding-left: 0; margin: 0; }
    .comment-item {
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-color-dark, #445259);
    }
    .comment-item:last-child { border-bottom: none; }

    .comment-main {
        display: flex;
        gap: 1rem;
    }

    .comment-content {
        flex-grow: 1;
    }
    .comment-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
    }
    .comment-author-name {
        font-weight: bold;
        color: var(--primary-text-color, #faebd7);
        font-family: var(--font-orbital-bold);
    }
    .comment-date {
        font-size: 0.8rem;
        color: #888;
    }
    .comment-text {
        line-height: 1.6;
        color: var(--primary-text-color, #faebd7);
        word-wrap: break-word; /* Ensure long words break */
        overflow-wrap: break-word; /* Standard property */
    }
    .comment-text :global(p) { margin-bottom: 0.5em;} /* Basic styling if content has <p> */

    .comment-actions {
        margin-top: 0.75rem;
    }
    .comment-actions button {
        background: none;
        border: none;
        color: var(--info-color, #3e92cc);
        cursor: pointer;
        font-size: 0.9rem;
        padding: 0.25rem 0.5rem;
        margin-right: 0.5rem;
        font-family: var(--font-orbital);
    }
    .comment-actions button:hover {
        text-decoration: underline;
        color: var(--secondary-color);
    }

    .reply-form {
        margin-top: 1rem;
        margin-left: calc(48px + 1rem); /* Align with comment text */
        padding: 0.75rem;
        background-color: var(--block-bg-darker, #0a2a38);
    }

    .replies-list {
        margin-top: 1rem;
        padding-left: calc(48px + 1rem); /* Indent replies */
        border-left: 2px solid var(--border-color-dark, #445259);
    }
    .reply-item {
        padding: 0.75rem 0;
        border-bottom: 1px dashed rgba(var(--border-color-dark-rgb, 68, 82, 89), 0.5); /* Lighter dash for replies */
    }
    .reply-item:last-child {
        border-bottom: none;
    }
    .reply-avatar-placeholder {
        width: 36px;
        height: 36px;
        font-size: 1.2rem;
    }
    /* Reply form styling */
    .reply-form {
        margin-top: 0.75rem;
        margin-left: calc(40px + 0.75rem); /* Align with parent comment text (avatar width + gap) */
        padding: 0.75rem;
        background-color: rgba(var(--block-bg-darker-rgb, 10, 42, 56), 0.7); /* Slightly more transparent */
        border-radius: 4px;
    }

    /* Replies List Styling for Indentation */
    .replies-list {
        margin-top: 0.75rem;
        padding-left: 1.5rem; /* Indentation for the whole replies block */
        margin-left: calc(40px + 0.75rem); /* Align start of replies list with parent's text content */
        border-left: 2px solid rgba(var(--border-color-dark-rgb, 68, 82, 89), 0.3); /* Softer border */
    }
    .reply-item {
        padding: 0.75rem 0;
        /* border-bottom: 1px dashed rgba(var(--border-color-dark-rgb, 68, 82, 89), 0.3); */
        border-bottom: none; /* Removing bottom border for replies for cleaner look */
    }
    .reply-item:last-child { border-bottom: none; }

    .replies-list .reply-form { /* Reply form for a reply (nested further) */
        margin-left: calc(32px + 0.75rem); /* Align with reply's text (reply avatar width + gap) */
    }

    /* Helper for rgba with CSS vars if not already defined globally */
    :root {
        /* ... your existing root vars ... */
        --block-bg-darker-rgb: 10, 42, 56; /* Example RGB for #0a2a38 */
        --border-color-dark-rgb: 68, 82, 89; /* Example RGB for #445259 */
    }
</style>