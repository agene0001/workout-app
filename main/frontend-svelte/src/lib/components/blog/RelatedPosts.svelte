<script lang="ts">
    import { onMount } from 'svelte';
    import axios from 'axios'; // Or your preferred fetch method
    let { postId, count = 3 } = $props<{ postId: string; count?: number }>(); // count can also be a prop

    type RelatedPost = {
        id: string;
        slug: string;
        title: string;
        image?: string;
        publishedAt: string; // Or Date
        readTime?: number;
    };

    // Use $state for reactive variables
    let relatedPosts = $state<RelatedPost[]>([]);
    let isLoading = $state(true);
    let error = $state<string | null>(null);

    $effect(() => {
        const currentPostId = postId; // Capture current value for async operation
        const currentCount = count;

        // console.log(`%cRelatedPosts S5 $EFFECT - Triggered for PostID: ${currentPostId} (Count: ${currentCount}) at ${new Date().toISOString()}`, "color: magenta; font-weight: bold;");

        async function fetchData() {
            if (!currentPostId) {
                console.warn("RelatedPosts S5 $EFFECT: No postId, skipping fetch.");
                relatedPosts = [];
                isLoading = false;
                return;
            }
            isLoading = true;
            error = null;
            try {
                const response = await axios.get(`/api/v1/blog/posts`); // Fetches all posts
                if (response.data && Array.isArray(response.data)) {
                    const allPosts: RelatedPost[] = response.data;
                    const filtered = allPosts
                        .filter((p) => p.id !== currentPostId)
                        .slice(0, currentCount);
                    relatedPosts = filtered;
                } else {
                    relatedPosts = [];
                }
            } catch (err: any) {
                error = "Could not load related posts.";
                relatedPosts = [];
            } finally {
                isLoading = false;
            }
        }
        fetchData();
    });

    function formatDate(dateString: string | Date) {
        const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    }
</script>

{#if isLoading}
    <div class="related-posts-loading">Loading suggestions...</div>
{:else if error}
    <div class="related-posts-error">{error}</div>
{:else if relatedPosts.length > 0}
    <section class="related-posts-section">
        <h2 class="related-posts-title">You Might Also Like</h2>
        <div class="related-posts-grid">

            {#each relatedPosts as relPost (relPost.id)}
                <a href="/Blog/{relPost.slug}" class="related-post-card">
                    {#if relPost.image && !relPost.image.startsWith("https://placehold.co/")}
                        <img src={relPost.image} alt={relPost.title} class="related-post-image"/>
                    {:else}
                        <div class="related-post-image-placeholder">
                            <span>{relPost.title.substring(0,1)}</span>
                        </div>
                    {/if}
                    <div class="related-post-content">
                        <h3 class="related-post-card-title">{relPost.title}</h3>
                        <p class="related-post-meta">
                            {formatDate(relPost.publishedAt)}
                            {#if relPost.readTime} • {relPost.readTime} min read{/if}
                        </p>
                    </div>
                </a>
            {/each}
        </div>
    </section>
{/if}

<style>
    .related-posts-section {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border-color-dark);
    }
    .related-posts-title {
        font-family: var(--font-orbital-bold);
        font-size: 1.8rem;
        color: var(--primary-text-color);
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .related-posts-grid {
        display: grid;
        /* Force 3 columns of equal width, regardless of content or auto-fit */
        grid-template-columns: 1fr 1fr ;
        gap: 1.5rem;
    }
    .related-post-card {

        background-color: var(--block-bg-dark);
        border-radius: 8px;
        overflow: hidden;
        text-decoration: none;
        color: var(--primary-text-color);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        display: flex;
        flex-direction: row;

        border: 1px solid var(--border-color-dark);
    }
    .related-post-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    .related-post-image {
        height: 100%;
        object-fit: cover;
    }
    .related-post-image-placeholder {
        height: 100%;
        background-color: var(--block-bg-darker);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        color: var(--secondary-color);
        font-family: var(--font-orbital-bold);
    }
    .related-post-content {
        padding: 1rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    .related-post-card-title {
        font-family: var(--font-orbital-bold);
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        line-height: 1.3;
        flex-grow: 1; /* Allow title to take up space */
    }
    .related-post-meta {
        font-family: var(--font-orbital);
        font-size: 0.85rem;
        color: #a0a0a0;
        margin-top: auto; /* Push meta to bottom */
    }
    .related-posts-loading, .related-posts-error {
        text-align: center;
        padding: 2rem;
        color: var(--primary-text-color);
        font-family: var(--font-orbital);
    }
</style>