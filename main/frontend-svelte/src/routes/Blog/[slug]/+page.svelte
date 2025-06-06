<script lang="ts">
    import { getContext, onMount } from 'svelte'; // afterUpdate is less common with runes, $effect handles DOM updates
    import { goto } from '$app/navigation';

    import { page } from '$app/state'; // <<< CORRECT IMPORT
    // Import your components as before
    import NestedListItemRenderer from '$lib/components/blog/NestedListItemRenderer.svelte';
    import BlockRenderer from '$lib/components/blog/BlockRenderer.svelte';
    import ReadingProgressBar from '$lib/components/blog/ReadingProgressBar.svelte';
    import TableOfContents from '$lib/components/blog/TableOfContents.svelte';
    import RelatedPosts from '$lib/components/blog/RelatedPosts.svelte';
    import CommentsSection from '$lib/components/blog/CommentsSection.svelte';

    // --- Svelte 5 State and Derived Values ---

    // The `post` data from the load function, derived from the $page store
    // This is the primary reactive source for this page's content.
    let { data } = $props();
    const post = $derived(page.data.post);
    // isAdmin from context (assuming this is set up in a layout and doesn't change per post page)
    // If isAdmin could change reactively and needs to be a rune, it'd need to be a $state from a store or prop.
    const isAdmin = getContext('isAdmin');
    console.log(isAdmin)
    // Derived state for parsedContent. This will recompute whenever `post` changes.
    let parsedContent = $derived(() => {
        console.log(post)
        if (post && post.content) {
            console.log("S5: Post data changed, re-parsing content for slug:", post.slug);
            console.log(post)
            if (typeof post.content === 'string') {
                try {
                    const parsed = JSON.parse(post.content);
                    if (parsed && parsed.blocks) {
                        return parsed;
                    } else {
                        console.warn('S5: Parsed string content is not valid EditorJS block structure, treating as HTML.');
                        return { blocks: [{ type: 'html', data: { html: post.content } }] };
                    }
                } catch (e) {
                    console.error('S5: Failed to parse post.content string, treating as raw HTML:', e);
                    return { blocks: [{ type: 'html', data: { html: post.content } }] };
                }
            } else if (post.content && typeof post.content === 'object' && post.content.blocks) {
                return post.content; // Already in EditorJS format
            } else {
                console.warn('S5: Post content is in an unexpected format.');
                return { blocks: [] };
            }
        } else if (post) {
            console.warn('S5: Post data loaded, but post.content is missing or empty for slug:', post.slug);
            return { blocks: [] };
        } else {
            console.log('S5: Post data is not available.');
            return { blocks: [] };
        }
    });
    console.log(parsedContent())
    // --- Lifecycle ---
    onMount(() => {
        console.log("S5: Blog post page component mounted. Initial post slug (if available):", post?.slug);
        // Any one-time setup for the component instance.
        // If you had logic in onMount that depended on `post` being available,
        // an $effect might be more appropriate if `post` could be initially undefined from $page.data
        // post = data.post
    });

    // $effect can be used for side effects that need to run when specific state changes.
    // For example, if you needed to interact with the DOM after `parsedContent` changes:
    // $effect(() => {
    //     if (parsedContent && typeof window !== 'undefined') {
    //         console.log("S5: parsedContent updated, potentially update DOM for TOC scroll etc.");
    //         // Example: document.title = post.title; (though SvelteKit <svelte:head> is better for title)
    //     }
    // });

    // --- Functions ---
    // These functions are fine as they are, they don't rely on Svelte 4's specific reactivity model.
    function generateSlug(text: string): string {
        if (!text) return `section-${Math.random().toString(36).substring(7)}`;
        return text
            .toLowerCase()
            .replace(/\s+/g, '-') // Replace spaces with -
            .replace(/[^\w-]+/g, '') // Remove all non-word chars
            .replace(/--+/g, '-') // Replace multiple - with single -
            .replace(/^-+/, '') // Trim - from start of text
            .replace(/-+$/, ''); // Trim - from end of text
    }
    function formatDate(dateString: string | undefined): string {
        if (!dateString) return 'Date not available';
        const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    }

    function handleEditPost(id: string) {
        goto(`/Blog/admin/post/${id}`);
    }

    function handleDeletePost(id: string, title: string) {
        if (confirm(`Are you sure you want to delete "${title}"?`)) {
            // Implement actual delete logic (e.g., API call)
            console.log('S5: Delete post:', id);
        }
    }

    // getTuneClasses, getTuneId, renderBlock remain the same
    function getTuneClasses(tunes) {
        if (!tunes) return '';
        let classes = [];
        if (tunes.alignTune?.alignment) {
            classes.push(`text-align-${tunes.alignTune.alignment}`);
        }
        if (tunes.indentTune?.level && tunes.indentTune.level > 0) {
            classes.push(`editorjs-indent-level-${tunes.indentTune.level}`);
        }
        if (tunes.textVariantTune?.variant) {
            classes.push(`text-variant-${tunes.textVariantTune.variant}`);
        }
        return classes.join(' ');
    }

    function getTuneId(tunes) {
        return tunes?.anchorTune?.anchor || null;
    }
    function getAnchorIdFromTune(tunes: any): string | null {
        return tunes?.anchorTune?.anchor || null;
    }
    function renderBlock(block,index) {
        if (!block) return null;
        const tunes = block.tunes || {};
        const tuneClasses = getTuneClasses(tunes);
        const tuneId = getTuneId(tunes);
        const blockId = getAnchorIdFromTune(tunes) || generateSlug(block.data?.text || block.data?.caption || block.type) + `-${index}`;
        switch (block.type) {
            case 'html':
                return {
                    tag: 'div',
                    isHtmlContent: true,
                    html: block.data.html
                };
            case 'header':
                return {
                    tag: `h${block.data.level}`,
                    content: block.data.text,
                    className: `block-header ${tuneClasses}`,
                    id: blockId // This now correctly assigns the generated ID
                }
            case 'paragraph':
                return {tag: 'p', content: block.data.text, className: `block-paragraph ${tuneClasses}`, id: tuneId};

            case 'nestedlist':
                return {
                    tag: block.data.style === 'ordered' ? 'ol' : 'ul',
                    items: block.data.items,
                    className: `block-list block-nested-list ${block.data.style}-list ${tuneClasses}`,
                    id: tuneId,
                    isAnyList: true,
                    listStyle: block.data.style
                };
            case 'image':
                return {
                    tag: 'figure',
                    content: '',
                    className: `block-image ${tuneClasses}`,
                    id: tuneId,
                    children: [{
                        tag: 'img',
                        src: block.data.file?.url,
                        alt: block.data.caption || 'Blog image',
                        className: 'block-image__img'
                    }, block.data.caption ? {
                        tag: 'figcaption',
                        content: block.data.caption,
                        className: 'block-image__caption'
                    } : null].filter(Boolean)
                };
            case 'quote':
                return {
                    tag: 'blockquote',
                    content: block.data.text,
                    className: `block-quote ${tuneClasses}`,
                    id: tuneId,
                    children: block.data.caption ? {
                        tag: 'cite',
                        content: block.data.caption,
                        className: 'block-quote__caption'
                    } : null
                };
            case 'delimiter':
                return {tag: 'hr', content: '', className: `block-delimiter ${tuneClasses}`, id: tuneId};
            case 'table':
                return {
                    tag: 'table',
                    className: `block-table ${tuneClasses}`,
                    id: tuneId,
                    isTable: true,
                    data: block.data
                };
            case 'code':
                return {
                    tag: 'pre',
                    className: `block-code ${tuneClasses}`,
                    id: tuneId,
                    children: {
                        tag: 'code',
                        content: block.data.code,
                        className: `language-${block.data.language || 'plaintext'}`
                    }
                };
            case 'embed':
                return {tag: 'div', className: `block-embed ${tuneClasses}`, id: tuneId, embed: true, data: block.data};
            case 'list':
                if (block.data.style === 'checklist') {
                    return {
                        tag: 'ul',
                        items: block.data.items,
                        className: `block-checklist ${tuneClasses}`,
                        id: tuneId,
                        isChecklist: true,
                    };
                } else {
                    return {
                        tag: block.data.style === 'ordered' ? 'ol' : 'ul',
                        items: block.data.items,
                        className: `block-list ${block.data.style}-list ${tuneClasses}`,
                        id: tuneId,
                        isAnyList: true,
                        listStyle: block.data.style
                    };
                }
            case 'warning':
                return {
                    tag: 'div',
                    className: `block-warning ${tuneClasses}`,
                    id: tuneId,
                    isWarning: true,
                    data: block.data
                };
            case 'alert':
                return {
                    tag: 'div',
                    content: block.data.message,
                    className: `block-alert alert-${block.data.type || 'info'} ${tuneClasses}`,
                    id: tuneId
                };
            case 'attaches':
                return {
                    tag: 'div',
                    className: `block-attaches ${tuneClasses}`,
                    id: tuneId,
                    isAttachment: true,
                    data: block.data
                };
            case 'coolDelimiter':
                return {tag: 'hr', content: '', className: `block-delimiter-cool ${tuneClasses}`, id: tuneId};
            case 'button':
                return {
                    tag: 'a',
                    href: block.data.link,
                    content: block.data.text,
                    className: `block-button ${block.data.style || 'btn--default'} ${tuneClasses}`,
                    id: tuneId,
                    attributes: {
                        target: block.data.link?.startsWith('http') ? '_blank' : '_self',
                        rel: block.data.link?.startsWith('http') ? 'noopener noreferrer' : null
                    },
                    isButton: true
                };
            case 'toggle':
                return {
                    tag: 'details',
                    summaryText: block.data.text,
                    nestedBlocks: block.data.blocks || [],
                    className: `block-toggle ${tuneClasses}`,
                    id: tuneId,
                    isToggle: true,
                    isOpen: block.data.status === 'open'
                };
            case 'layout':
                return {
                    tag: 'div',
                    className: `block-layout editorjs-columns_wrapper ${tuneClasses}`,
                    id: tuneId,
                    isLayout: true,
                    columnsData: block.data.cols || []
                };
            default:
                console.warn('Unknown block type:', block.type, block);
                return {
                    tag: 'div',
                    content: `Unsupported block type: ${block.type}. Data: ${JSON.stringify(block.data)}`,
                    className: `block-unknown block-${block.type} ${tuneClasses}`,
                    id: tuneId
                };
        }
    }
</script>

<!--
    The `key` directive is still crucial in Svelte 5 for re-creating component instances
    when their identity changes (e.g., navigating from one post to another).
    This ensures their internal state (like data fetched in onMount or an initial $effect run)
    is reset and re-initialized for the new `postId`.
-->
{#if post }
    <ReadingProgressBar key={`progress-${post.id}`} />

    <div class="post-container post-content-for-progress">
        <h1 class="post-title text-primary">{post.title}</h1>
        <p class="post-meta">{formatDate(post.publishedAt)} • {post.readTime} min read</p>

        {#if post.image && !post.image.startsWith("https://placehold.co/")}
            <img src={post.image} alt={post.title || 'Blog post image'} class="post-main-image"/>
        {/if}

        {#if parsedContent && parsedContent().blocks && parsedContent().blocks.length > 0}
            <TableOfContents blocks={parsedContent().blocks} key={`toc-${post.id}`}/>
        {/if}

        <div class="post-content">
            {#if parsedContent() && parsedContent().blocks && parsedContent().blocks.length > 0}
                {#each parsedContent().blocks as block, i (block.id || `${block.type}-${i}`)}
                    {@const currentRenderedBlock = renderBlock(block,i)}
                    {#if currentRenderedBlock}
                        <BlockRenderer
                                renderedBlock={currentRenderedBlock}
                                {renderBlock}
                        {NestedListItemRenderer}
                        />
                    {/if}
                {/each}
            {:else if typeof post.content === 'string' && post.content.trim() !== ''}
                <div class="html-fallback-content">{@html post.content}</div>
            {:else}
                <p class="text-primary">This post currently has no content.</p>
            {/if}
        </div>

        {#if post.conclusion_editorjs_content && post.conclusion_editorjs_content.blocks }
            <div class="post-conclusion-section">
                <h2 class="conclusion-title">Conclusion</h2>
                {#each post.conclusion_editorjs_content.blocks as block, i (block.id || `conclusion-${block.type}-${i}`)}
                    {@const currentRenderedBlock = renderBlock(block,i)}
                    {#if currentRenderedBlock}
                        <BlockRenderer
                                renderedBlock={currentRenderedBlock}
                                {renderBlock}
                                {NestedListItemRenderer}
                        />
                    {/if}
                {/each}
            </div>
        {:else if post.conclusion_html}
            <div class="post-conclusion-section">
                <h2 class="conclusion-title">Conclusion</h2>
                <div class="conclusion-content">{@html post.conclusion_html}</div>
            </div>
        {/if}


        {#if $isAdmin } <!-- Use the const isAdmin directly -->
            <div class="admin-controls">
                <button on:click={() => handleEditPost(post.id)} class="edit-button">Edit</button>
                <button on:click={() => handleDeletePost(post.id, post.title)} class="delete-button">Delete</button>
            </div>
        {/if}
        <a href="/Blog" class="back-to-list">Back to Blog</a>
    </div>

    <!--
        Props for Svelte 5 components using $props() are passed normally.
        The `key` is essential for re-instantiation.
    -->
    <RelatedPosts postId={post.id} count={3} />
    <CommentsSection postId={post.id} postTitle={post.title} />

{:else}
    <div class="post-container">
        <p class="text-primary">Loading post data or post not found...</p>
    </div>
{/if}

<!-- Styles remain the same, but you'll add styles for the new sections as shown in their components or above for conclusion -->
<style>
    /* ... your existing styles ... */


    .html-fallback-content {
        /* Styles for when post.content is just a string */
        line-height: 1.7;
        font-size: 1.1rem;
    }
    .html-fallback-content :global(p) { margin-bottom: 1rem; }
    .html-fallback-content :global(h1) { font-size: 2em; margin: 0.67em 0; }
    /* Add more global styles for basic HTML tags if needed for fallback */




    .conclusion-content {
        line-height: 1.7;
        font-size: 1.1rem;
        color: var(--primary-text-color);
        font-family: var(--font-orbital);
    }
    .conclusion-content :global(p) { margin-bottom: 1rem; }
    /* Ensure the rest of your styles are here */

    :root {
        --font-orbital: 'orbital', sans-serif;
        --font-orbital-bold: 'orbital', sans-serif;
        --primary-text-color: #faebd7;
        --secondary-color: #c62368;
        --info-color: #3e92cc;
        --warning-color: #f0ad4e;
        --danger-color: #d9534f;
        --success-color: #5cb85c;
        --body-bg-color: #002233;
        --block-bg-darker: #0a2a38;
        --block-bg-dark: #0f3040;
        --border-color-dark: #445259;
        --text-color-light: #f8f9fa;
        --text-color-dark: #212529;

        /* Enhanced color palette */
        --accent-gradient: linear-gradient(135deg, #00A76E, #3e92cc);
        --subtle-glow: 0 0 20px rgba(198, 35, 104, 0.3);
        --image-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        --content-bg: rgba(15, 48, 64, 0.6);
        --hover-color: #ff6b94;
        --highlight-color: #64ffda;
    }

    .post-container {
        margin-top: 8rem;
        max-width: 900px; /* Slightly increased for better readability */
        margin-left: auto;
        margin-right: auto;
        padding: 2rem 1.5rem;
        position: relative;
    }

    /* Enhanced main title styling */
    .post-title {
        font-family: var(--font-orbital-bold);
        font-weight: 700;
        font-size: clamp(2.5rem, 5vw, 3.5rem);
        margin-bottom: 1rem;
        line-height: 1.2;
        background: var(--accent-gradient);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(198, 35, 104, 0.5);
        position: relative;
    }

    .post-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 60px;
        height: 4px;
        background: var(--accent-gradient);
        border-radius: 2px;
        box-shadow: var(--subtle-glow);
    }

    /* Enhanced meta styling */
    .post-meta {
        font-family: var(--font-orbital);
        color: var(--highlight-color);
        margin-bottom: 3rem;
        font-size: 1rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
    }

    /* Main image enhancement */
    .post-main-image {
        width: 100%;
        max-height: 500px;
        object-fit: cover;
        border-radius: 16px;
        margin-bottom: 3rem;
        box-shadow: var(--image-shadow);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 2px solid transparent;
        background: var(--accent-gradient);
        background-clip: padding-box;
    }

    .post-main-image:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), var(--subtle-glow);
    }

    /* Enhanced content area */
    .post-content {
        line-height: 1.8;
        font-size: 1.15rem;
        color: var(--primary-text-color);
        font-family: var(--font-orbital);
        background: var(--content-bg);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(198, 35, 104, 0.2);
        backdrop-filter: blur(10px);
        position: relative;
        margin-bottom: 2rem;
    }

    .post-content::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--accent-gradient);
        border-radius: 16px 16px 0 0;
    }

    /* Enhanced header styling within content */
    .post-content :global(h1.block-header),
    .post-content :global(h2.block-header),
    .post-content :global(h3.block-header),
    .post-content :global(h4.block-header),
    .post-content :global(h5.block-header),
    .post-content :global(h6.block-header) {
        font-family: var(--font-orbital-bold);
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-text-color), var(--highlight-color));
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.3;
        position: relative;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
    }

    .post-content :global(h1.block-header) {
        font-size: 2.6rem;
        text-shadow: 0 0 20px rgba(100, 255, 218, 0.3);
    }
    .post-content :global(h2.block-header) {
        font-size: 2.2rem;
        text-shadow: 0 0 15px rgba(100, 255, 218, 0.25);
    }
    .post-content :global(h3.block-header) {
        font-size: 1.9rem;
        text-shadow: 0 0 10px rgba(100, 255, 218, 0.2);
    }
    .post-content :global(h4.block-header) { font-size: 1.6rem; }
    .post-content :global(h5.block-header) { font-size: 1.3rem; }
    .post-content :global(h6.block-header) {
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--secondary-color);
    }

    /* Add decorative elements to headers */
    .post-content :global(h2.block-header)::before {
        content: '▎';
        color: var(--secondary-color);
        margin-right: 0.5rem;
        font-size: 1.2em;
    }

    .post-content :global(h3.block-header)::before {
        content: '◆';
        color: var(--info-color);
        margin-right: 0.5rem;
        font-size: 0.8em;
    }

    /* Enhanced paragraph styling */
    .post-content :global(p.block-paragraph) {
        font-family: var(--font-orbital);
        margin-bottom: 1.8rem;
        color: var(--primary-text-color);
        text-align: justify;
        hyphens: auto;
        position: relative;
    }

    .post-content :global(p.block-paragraph):first-of-type::first-letter {
        font-size: 3.5em;
        float: left;
        line-height: 1;
        margin: 0.1em 0.1em 0 0;
        color: var(--secondary-color);
        font-weight: bold;
    }

    /* Enhanced link styling */
    .post-content :global(a) {
        color: var(--highlight-color);
        text-decoration: none;
        position: relative;
        transition: all 0.3s ease;
        border-bottom: 1px solid transparent;
    }

    .post-content :global(a:hover) {
        color: var(--hover-color);
        text-shadow: 0 0 8px rgba(255, 107, 148, 0.6);
        border-bottom-color: var(--hover-color);
    }

    .post-content :global(a)::after {
        content: '';
        position: absolute;
        width: 0;
        height: 2px;
        bottom: -2px;
        left: 0;
        background: var(--accent-gradient);
        transition: width 0.3s ease;
    }

    .post-content :global(a:hover)::after {
        width: 100%;
    }

    /* Enhanced image styling */
    .post-content :global(figure.block-image) {
        margin: 3rem auto;
        text-align: center;
        position: relative;
    }

    .post-content :global(figure.block-image img.block-image__img) {
        max-width: 100%;
        height: auto;
        border-radius: 12px;
        box-shadow: var(--image-shadow);
        transition: all 0.3s ease;
        border: 2px solid rgba(198, 35, 104, 0.3);
    }

    .post-content :global(figure.block-image img.block-image__img:hover) {
        transform: scale(1.02);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), var(--subtle-glow);
        border-color: var(--secondary-color);
    }

    .post-content :global(figure.block-image figcaption.block-image__caption) {
        font-family: var(--font-orbital);
        font-size: 0.95rem;
        color: var(--highlight-color);
        text-align: center;
        margin-top: 1rem;
        font-style: italic;
        background: rgba(15, 48, 64, 0.8);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 1px solid rgba(100, 255, 218, 0.2);
        max-width: 80%;
        margin-left: auto;
        margin-right: auto;
    }

    /* Enhanced quote styling */
    .post-content :global(blockquote.block-quote) {
        font-family: var(--font-orbital);
        border-left: 6px solid var(--secondary-color);
        padding: 2rem 2.5rem;
        margin: 3rem 0;
        background: linear-gradient(135deg, rgba(198, 35, 104, 0.1), rgba(62, 146, 204, 0.1));
        border-radius: 0 12px 12px 0;
        color: var(--primary-text-color);
        font-style: italic;
        position: relative;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    .post-content :global(blockquote.block-quote)::before {
        content: '"';
        font-size: 4rem;
        color: var(--secondary-color);
        position: absolute;
        top: -10px;
        left: 20px;
        opacity: 0.5;
        font-family: serif;
    }

    .post-content :global(blockquote.block-quote p) {
        font-size: 1.2rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    /* Enhanced list styling */
    .post-content :global(.block-list li),
    .post-content :global(.block-checklist li) {
        margin-bottom: 1rem;
        line-height: 1.7;
        padding-left: 0.5rem;
        position: relative;
    }

    .post-content :global(ol.block-list),
    .post-content :global(ul.block-list:not(.block-checklist)) {
        background: rgba(15, 48, 64, 0.3);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        border-left: 4px solid var(--info-color);
        margin-bottom: 2rem;
    }

    .post-content :global(ul.block-list:not(.block-checklist) li)::before {
        content: '▸';
        color: var(--secondary-color);
        font-weight: bold;
        position: absolute;
        left: -1.5rem;
    }

    /* Enhanced code block styling */
    .post-content :global(pre.block-code) {
        margin: 3rem 0;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        color: #e6e6e6;
        border: 1px solid var(--secondary-color);
        border-radius: 12px;
        padding: 2rem;
        overflow-x: auto;
        box-shadow: var(--image-shadow);
        position: relative;
    }

    .post-content :global(pre.block-code)::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-gradient);
        border-radius: 12px 12px 0 0;
    }

    .post-content :global(pre.block-code code) {
        font-family: 'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        text-shadow: 0 0 5px rgba(198, 35, 104, 0.3);
    }

    /* Enhanced table styling */
    .post-content :global(table.block-table) {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 3rem auto;
        font-family: var(--font-orbital);
        color: var(--primary-text-color);
        border: 2px solid var(--secondary-color);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--image-shadow);
        background: var(--block-bg-dark);
    }

    .post-content :global(table.block-table th) {
        background: var(--accent-gradient);
        color: white;
        font-weight: bold;
        padding: 1rem 1.5rem;
        text-align: left;
        font-size: 1rem;
        letter-spacing: 0.5px;
    }

    .post-content :global(table.block-table td) {
        padding: 1rem 1.5rem;
        border-bottom: 1px solid rgba(198, 35, 104, 0.2);
        transition: background-color 0.3s ease;
    }

    .post-content :global(table.block-table tr:hover td) {
        background-color: rgba(198, 35, 104, 0.1);
    }

    /* Enhanced button styling */
    .post-content :global(a.block-button) {
        display: inline-block;
        padding: 1rem 2rem;
        margin: 2rem 0.5rem;
        font-family: var(--font-orbital-bold);
        text-decoration: none;
        border-radius: 8px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: bold;
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .post-content :global(a.block-button.btn--default) {
        background: var(--accent-gradient);
        color: white;
        box-shadow: 0 8px 20px rgba(62, 146, 204, 0.4);
    }

    .post-content :global(a.block-button.btn--default:hover) {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(62, 146, 204, 0.6);
    }

    .post-content :global(a.block-button)::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }

    .post-content :global(a.block-button:hover)::before {
        left: 100%;
    }

    /* Enhanced warning/alert styling */
    .post-content :global(div.block-warning),
    .post-content :global(div.block-alert) {
        padding: 1.5rem 2rem;
        margin: 2.5rem 0;
        border-left-width: 6px;
        border-left-style: solid;
        border-radius: 0 12px 12px 0;
        color: var(--primary-text-color);
        position: relative;
        backdrop-filter: blur(5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    .post-content :global(div.block-alert.alert-info) {
        border-color: var(--info-color);
        background: linear-gradient(135deg, rgba(62,146,204,0.15), rgba(62,146,204,0.05));
    }

    .post-content :global(div.block-alert.alert-warning) {
        border-color: var(--warning-color);
        background: linear-gradient(135deg, rgba(240,173,78,0.15), rgba(240,173,78,0.05));
    }

    .post-content :global(div.block-alert.alert-success) {
        border-color: var(--success-color);
        background: linear-gradient(135deg, rgba(92,184,92,0.15), rgba(92,184,92,0.05));
    }

    .post-content :global(div.block-alert.alert-danger) {
        border-color: var(--danger-color);
        background: linear-gradient(135deg, rgba(217,83,79,0.15), rgba(217,83,79,0.05));
    }

    /* Enhanced conclusion section */
    .post-conclusion-section {
        margin-top: 4rem;
        padding: 3rem 2.5rem;
        background: var(--content-bg);
        border-radius: 16px;
        border: 1px solid rgba(100, 255, 218, 0.3);
        backdrop-filter: blur(10px);
        position: relative;
    }

    .post-conclusion-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-gradient);
        border-radius: 16px 16px 0 0;
    }

    .conclusion-title {
        font-family: var(--font-orbital-bold);
        font-size: 2.5rem;
        background: var(--accent-gradient);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        position: relative;
    }

    .conclusion-title::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        width: 40px;
        height: 3px;
        background: var(--accent-gradient);
        border-radius: 2px;
    }

    /* Enhanced admin controls */
    .admin-controls {
        margin-top: 4rem;
        padding: 2rem;
        border-top: 2px solid var(--secondary-color);
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
        background: rgba(15, 48, 64, 0.3);
        border-radius: 0 0 16px 16px;
    }

    .edit-button, .delete-button {
        font-family: var(--font-orbital-bold);
        padding: 0.8rem 1.5rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }

    .edit-button {
        background: var(--accent-gradient);
        color: white;
        box-shadow: 0 5px 15px rgba(62, 146, 204, 0.4);
    }

    .edit-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(62, 146, 204, 0.6);
    }

    .delete-button {
        background: linear-gradient(135deg, var(--danger-color), #b71c1c);
        color: white;
        box-shadow: 0 5px 15px rgba(217, 83, 79, 0.4);
    }

    .delete-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(217, 83, 79, 0.6);
    }

    /* Enhanced back link */
    .back-to-list {
        display: inline-block;
        margin-top: 3rem;
        padding: 1rem 2rem;
        font-family: var(--font-orbital-bold);
        border: 2px solid var(--info-color);
        color: var(--info-color);
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .back-to-list:hover {
        background: var(--accent-gradient);
        color: white;
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(62, 146, 204, 0.5);
    }

    /* Responsive improvements */
    @media (max-width: 768px) {
        .post-content {
            padding: 1.5rem;
            margin: 1rem 0;
        }

        .post-title {
            font-size: 2.5rem;
        }

        .post-content :global(h1.block-header) { font-size: 2.2rem; }
        .post-content :global(h2.block-header) { font-size: 1.9rem; }
        .post-content :global(h3.block-header) { font-size: 1.6rem; }

        .post-content :global(figure.block-image figcaption.block-image__caption) {
            max-width: 95%;
        }

        .admin-controls {
            flex-direction: column;
            align-items: center;
        }
    }

    /* Add subtle animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .post-content :global(.block-paragraph),
    .post-content :global(.block-header),
    .post-content :global(.block-image),
    .post-content :global(.block-quote) {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Scrollbar styling */
    .post-content :global(pre.block-code)::-webkit-scrollbar {
        height: 8px;
    }

    .post-content :global(pre.block-code)::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 4px;
    }

    .post-content :global(pre.block-code)::-webkit-scrollbar-thumb {
        background: var(--accent-gradient);
        border-radius: 4px;
    }

    .post-content :global(pre.block-code)::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #a51f58, #307db8);
    }</style>