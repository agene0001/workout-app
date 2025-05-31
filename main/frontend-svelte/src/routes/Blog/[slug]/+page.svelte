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
    const isAdmin = getContext<boolean>('isAdmin'); // Assuming boolean type
    console.log(data)
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
    function renderBlock(block) {
        if (!block) return null;
        const tunes = block.tunes || {};
        const tuneClasses = getTuneClasses(tunes);
        const tuneId = getTuneId(tunes);

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
                    id: tuneId
                };
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

    <div class="post-container">
        <h1 class="post-title text-primary">{post.title}</h1>
        <p class="post-meta">{formatDate(post.publishedAt)} • {post.readTime} min read</p>

        {#if post.image && !post.image.startsWith("https://placehold.co/")}
            <img src={post.image} alt={post.title || 'Blog post image'} class="post-main-image"/>
        {/if}

        {#if parsedContent && parsedContent().blocks && parsedContent().blocks.length > 0}
            <TableOfContents blocks={parsedContent().blocks} key={`toc-${post.id}`}/>
        {/if}

        <div class="post-content post-content-for-progress">
            {#if parsedContent() && parsedContent().blocks && parsedContent().blocks.length > 0}
                {#each parsedContent().blocks as block, i (block.id || `${block.type}-${i}`)}
                    {@const currentRenderedBlock = renderBlock(block)}
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
                    {@const currentRenderedBlock = renderBlock(block)}
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


        {#if isAdmin} <!-- Use the const isAdmin directly -->
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
    .post-main-image {
        width: 100%;
        max-height: 450px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 2.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }

    .html-fallback-content {
        /* Styles for when post.content is just a string */
        line-height: 1.7;
        font-size: 1.1rem;
    }
    .html-fallback-content :global(p) { margin-bottom: 1rem; }
    .html-fallback-content :global(h1) { font-size: 2em; margin: 0.67em 0; }
    /* Add more global styles for basic HTML tags if needed for fallback */


    .post-conclusion-section {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 2px solid var(--secondary-color);
    }
    .conclusion-title {
        font-family: var(--font-orbital-bold);
        font-size: 2rem;
        color: var(--primary-text-color);
        margin-bottom: 1.5rem;
    }
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
    }

    .post-container {
        margin-top: 8rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        padding: 2rem 1.5rem;
    }

    .post-title {
        font-family: var(--font-orbital-bold);
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 1rem;
        line-height: 1.2;
        color: var(--primary-text-color);
    }

    .post-meta {
        font-family: var(--font-orbital);
        color: #a0a0a0;
        margin-bottom: 3rem;
        font-size: 0.9rem;
    }

    .post-content {
        line-height: 1.7;
        font-size: 1.1rem;
        color: var(--primary-text-color);
        font-family: var(--font-orbital);
    }

    /* Anchor scrolling offset */
    .post-content :global(div[id]),
    .post-content :global(p[id]),
    .post-content :global(h1[id]),
    .post-content :global(h2[id]),
    .post-content :global(h3[id]),
    .post-content :global(h4[id]),
    .post-content :global(h5[id]),
    .post-content :global(h6[id]),
    .post-content :global(ul[id]),
    .post-content :global(ol[id]),
    .post-content :global(blockquote[id]),
    .post-content :global(figure[id]),
    .post-content :global(pre[id]),
    .post-content :global(table[id]),
    .post-content :global(details[id]) {
        scroll-margin-top: 80px; /* Increased slightly for fixed progress bar */
    }

    /* General link styling */
    .post-content :global(a) {
        color: var(--info-color);
        text-decoration: underline;
        transition: color 0.2s ease;
    }
    .post-content :global(a:hover) {
        color: var(--secondary-color);
        text-decoration: none;
    }

    /* Text Alignment Tune Classes */
    .post-content :global(.text-align-left) { text-align: left; }
    .post-content :global(.text-align-center) { text-align: center; }
    .post-content :global(.text-align-right) { text-align: right; }
    .post-content :global(.text-align-justify) { text-align: justify; }

    /* Indentation Tune Classes */
    .post-content :global(.editorjs-indent-level-1) { margin-left: 2em !important; }
    .post-content :global(.editorjs-indent-level-2) { margin-left: 4em !important; }
    .post-content :global(.editorjs-indent-level-3) { margin-left: 6em !important; }
    .post-content :global(.editorjs-indent-level-4) { margin-left: 8em !important; }
    .post-content :global(.editorjs-indent-level-5) { margin-left: 10em !important; }
    /* Add more as needed */


    /* --- Header Block Styling --- */
    .post-content :global(h1.block-header),
    .post-content :global(h2.block-header),
    .post-content :global(h3.block-header),
    .post-content :global(h4.block-header),
    .post-content :global(h5.block-header),
    .post-content :global(h6.block-header) {
        font-family: var(--font-orbital-bold);
        font-weight: 700;
        color: var(--primary-text-color);
        line-height: 1.3;
    }
    .post-content :global(h1.block-header) { font-size: 2.4rem; margin: 2.5rem 0 1.25rem 0; }
    .post-content :global(h2.block-header) { font-size: 2rem; margin: 2.2rem 0 1rem 0; }
    .post-content :global(h3.block-header) { font-size: 1.7rem; margin: 2rem 0 0.9rem 0; }
    .post-content :global(h4.block-header) { font-size: 1.4rem; margin: 1.8rem 0 0.8rem 0; }
    .post-content :global(h5.block-header) { font-size: 1.2rem; margin: 1.6rem 0 0.7rem 0; }
    .post-content :global(h6.block-header) { font-size: 1.1rem; margin: 1.5rem 0 0.6rem 0; text-transform: uppercase; letter-spacing: 0.05em; }

    /* --- Paragraph Block Styling --- */
    .post-content :global(p.block-paragraph) {
        font-family: var(--font-orbital);
        margin-bottom: 1.5rem;
        color: var(--primary-text-color);
    }

    /* --- LIST STYLES (REVISED SECTION) --- */

    /* Base styling for all list items (li) within any rendered list block */
    .post-content :global(.block-list li),       /* Covers li in ol.block-list and ul.block-list (non-checklist) */
    .post-content :global(.block-checklist li) { /* Covers li in ul.block-checklist */
        margin-bottom: 0.75rem;
        line-height: 1.7;
        /* Default display that allows markers. Specific list types will override if needed. */
        display: list-item;
    }

    /* Styling for standard ORDERED lists (ol.block-list) */
    .post-content :global(ol.block-list) {
        font-family: var(--font-orbital);
        margin-bottom: 1.5rem;
        padding-left: 2rem; /* Initial padding for the top-level list block */
        color: var(--primary-text-color);
        list-style-type: decimal; /* Ensures numbers for top-level ordered list */
    }
    .post-content :global(ol.block-list li) {
        /* Inherits list-style-type from parent ol by default. display: list-item is from above. */
    }

    /* Styling for standard UNORDERED lists (ul.block-list that are NOT checklists) */
    .post-content :global(ul.block-list:not(.block-checklist)) {
        font-family: var(--font-orbital);
        margin-bottom: 1.5rem;
        padding-left: 2rem; /* Initial padding */
        color: var(--primary-text-color);
        list-style-type: disc; /* Ensures bullets for top-level unordered list */
    }
    .post-content :global(ul.block-list:not(.block-checklist) li) {
        /* Inherits list-style-type from parent ul. display: list-item is from above. */
    }

    /* CHECKLIST Specific Styling */
    .post-content :global(ul.block-checklist) { /* The main <ul> container for a checklist block */
        font-family: var(--font-orbital);
        margin-bottom: 1.5rem;
        padding-left: 0.5rem; /* Less outer padding for checklists */
        color: var(--primary-text-color);
        list-style-type: none; /* Remove default bullets for the checklist container itself */
    }

    /* Target <li> elements that are specifically checklist items.
       Requires NestedListItemRenderer to add `class:is-checklist-item={isChecklistType}` to its root <li> */
    .post-content :global(li.is-checklist-item) {
        display: flex !important; /* Use !important if absolutely necessary to override generic li styles, but try to avoid. */
        align-items: center;
        list-style-type: none !important; /* Ensure no marker for checklist items */
        margin-bottom: 0.5rem; /* Specific margin for checklist items */
    }
    .post-content :global(li.is-checklist-item input[type="checkbox"]) {
        margin-right: 0.75rem;
        width: 1.2em;
        height: 1.2em;
        cursor: default;
        flex-shrink: 0; /* Prevent checkbox from shrinking */
    }
    .post-content :global(li.is-checklist-item.checked) { /* Targets <li class="is-checklist-item checked"> */
        text-decoration: line-through;
        color: #888;
    }
    .post-content :global(li.is-checklist-item.checked > input[type="checkbox"] ~ *) { /* Text next to checked checkbox */
        /* You could add opacity or other styles to the text of a checked item if needed */
    }


    /* NESTED LISTS Styling (applies to ol/ul inside any li) */
    /* This applies to ul/ol rendered by NestedListItemRenderer inside an <li> */
    .post-content :global(li > ol.block-list), /* Nested OL within any LI */
    .post-content :global(li > ul.block-list:not(.block-checklist)), /* Nested non-checklist UL */
    .post-content :global(li > ul.block-checklist) { /* Nested checklist UL */
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        padding-left: 1.75em; /* Indentation for nested lists. Adjust as needed. */
        /* Parent's list-style-type (decimal/disc) should cascade unless overridden by a more specific rule below */
    }

    /* Ensure nested ORDERED lists (even inside a checklist item) get their numbers */
    .post-content :global(li > ol.block-list) { /* Targets <ol class="block-list"> nested in any <li> */
        list-style-type: decimal; /* Explicitly set for clarity or override */
    }
    .post-content :global(li > ol.block-list li) {
        display: list-item; /* Ensure markers appear for items in nested ordered lists */
        list-style-type: upper-roman;
    }
    .post-content :global(li > ol.block-list li> ol.block-list li) {
        display: list-item; /* Ensure markers appear for items in nested ordered lists */
        list-style-type: lower-roman;
    }

    /* Ensure nested UNORDERED (non-checklist) lists get their bullets */
    .post-content :global(li > ul.block-list:not(.block-checklist)) {
        list-style-type: disc; /* Explicitly set */
    }
    .post-content :global(li > ul.block-list:not(.block-checklist) li) {
        display: list-item;
        list-style-type: upper-alpha; /* Or specify (e.g., circle for second level) */
    }
    .post-content :global(li > ul.block-list:not(.block-checklist) li > ul.block-list:not(.block-checklist) li) {
        display: list-item;
        list-style-type: lower-alpha; /* Or specify (e.g., circle for second level) */
    }

    /* Nested CHECKLISTS should inherit from `li.is-checklist-item` rules */
    /* .post-content :global(li > ul.block-checklist) is already covered for padding. */
    /* Its <li> children will be `li.is-checklist-item` and get styled by that rule. */

    /* --- END OF REVISED LIST STYLES --- */


    /* --- Image Block Styling --- */
    .post-content :global(figure.block-image) { margin: 2.5rem auto; text-align: center; }
    .post-content :global(figure.block-image.text-align-left) { margin-left:0; margin-right:auto; text-align: left; }
    .post-content :global(figure.block-image.text-align-right) { margin-left:auto; margin-right:0; text-align: right; }
    .post-content :global(figure.block-image img.block-image__img) { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .post-content :global(figure.block-image figcaption.block-image__caption) { font-family: var(--font-orbital); font-size: 0.9rem; color: #a0a0a0; text-align: center; margin-top: 0.75rem; font-style: italic; }

    /* --- Quote Block Styling --- */
    .post-content :global(blockquote.block-quote) { font-family: var(--font-orbital); border-left: 4px solid var(--info-color); padding: 1rem 1.5rem; margin: 2.5rem 0; background-color: rgba(62,146,204,0.1); border-radius: 4px; color: var(--primary-text-color); font-style: italic; }
    .post-content :global(blockquote.block-quote p) { font-family: var(--font-orbital); color: var(--primary-text-color); font-style: italic; margin-bottom: 0.5rem; }
    .post-content :global(blockquote.block-quote cite.block-quote__caption) { display: block; margin-top: 1rem; font-size: 0.9rem; text-align: right; font-style: normal; color: #a0a0a0; }

    /* --- Delimiter Block Styling --- */
    .post-content :global(hr.block-delimiter) { border: none; height: 1px; background-color: var(--border-color-dark); margin: 3rem auto; width: 50%; }
    .post-content :global(hr.block-delimiter-cool) { border: none; height: 3px; background: linear-gradient(to right, var(--secondary-color), var(--info-color), var(--primary-text-color)); margin: 3.5rem auto; width: 70%; border-radius: 3px; }

    /* --- Table Block Styling --- */
    .post-content :global(table.block-table) { width: auto; max-width: 100%; display: inline-block; border-collapse: collapse; margin: 2.5rem auto; overflow-x: auto; font-family: var(--font-orbital); color: var(--primary-text-color); border: 1px solid var(--border-color-dark); border-radius: 6px; }
    .post-content :global(div.text-align-center > table.block-table) { margin-left: auto; margin-right: auto; display: table; }
    .post-content :global(table.block-table td),
    .post-content :global(table.block-table th) { border: 1px solid var(--border-color-dark); padding: 0.75rem 1rem; text-align: left; }
    .post-content :global(table.block-table th) { background-color: var(--block-bg-dark); font-weight: bold; }
    .post-content :global(table.block-table tr:nth-child(odd) td) { background-color: var(--block-bg-darker); }
    .post-content :global(table.block-table tr:nth-child(even) td) { background-color: var(--block-bg-dark); }

    /* --- Code Block Styling --- */
    .post-content :global(pre.block-code) { margin: 2.5rem 0; background-color: #1e1e1e; color: #d4d4d4; border: 1px solid #3c3c3c; border-radius: 8px; padding: 1.5rem; overflow-x: auto; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }
    .post-content :global(pre.block-code code) { font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 0.95rem; line-height: 1.6; background: none; color: inherit; }

    /* --- Embed Block Styling --- */
    .post-content :global(div.block-embed) { margin: 2.5rem auto; }
    .post-content :global(div.block-embed.text-align-left) { margin-left:0; margin-right:auto; }
    .post-content :global(div.block-embed.text-align-right) { margin-left:auto; margin-right:0; }
    .post-content :global(div.block-embed iframe) { border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); display: block; margin: 0 auto; }
    .post-content :global(.unsupported-embed) { padding: 2rem; text-align: center; background-color: #1e1e1e; border: 1px solid #3c3c3c; border-radius: 8px; color: var(--primary-text-color); }
    .post-content :global(.unsupported-embed a) { color: var(--info-color); font-weight: 500; }

    /* --- Warning Block Styling --- */
    .post-content :global(div.block-warning) { padding: 1rem 1.5rem; margin: 2rem 0; border-left: 5px solid var(--warning-color); background-color: rgba(240,173,78,0.1); color: var(--primary-text-color); border-radius: 4px; }
    .post-content :global(div.block-warning strong.block-warning__title) { display: block; font-weight: bold; margin-bottom: 0.5rem; color: var(--warning-color); }
    .post-content :global(div.block-warning .block-warning__message) { line-height: 1.6; }

    /* --- Alert Block Styling --- */
    .post-content :global(div.block-alert) { padding: 1rem 1.5rem; margin: 2rem 0; border-left-width: 5px; border-left-style: solid; border-radius: 4px; color: var(--primary-text-color); }
    .post-content :global(div.block-alert.alert-info) { border-color: var(--info-color); background-color: rgba(62,146,204,0.1); }
    .post-content :global(div.block-alert.alert-success) { border-color: var(--success-color); background-color: rgba(92,184,92,0.1); }
    .post-content :global(div.block-alert.alert-warning) { border-color: var(--warning-color); background-color: rgba(240,173,78,0.1); }
    .post-content :global(div.block-alert.alert-danger) { border-color: var(--danger-color); background-color: rgba(217,83,79,0.1); }
    .post-content :global(div.block-alert.alert-primary) { border-color: var(--info-color); background-color: rgba(62,146,204,0.15); }
    .post-content :global(div.block-alert.alert-secondary) { border-color: var(--secondary-color); background-color: rgba(198,35,104,0.1); }

    /* --- Attaches Block Styling --- */
    .post-content :global(div.block-attaches) { margin: 2rem 0; padding: 1rem; border: 1px solid var(--border-color-dark); border-radius: 6px; background-color: var(--block-bg-dark); }
    .post-content :global(div.block-attaches a) { display: block; text-decoration: none; color: var(--info-color); padding: 0.5rem 0; }
    .post-content :global(div.block-attaches a:hover) { color: var(--secondary-color); }
    .post-content :global(div.block-attaches strong) { font-weight: bold; }
    .post-content :global(div.block-attaches em) { font-size: 0.9em; color: #a0a0a0; margin-left: 0.5rem; }

    /* --- Button Block Styling --- */
    .post-content :global(a.block-button) { display: inline-block; padding: 0.75rem 1.5rem; margin: 1rem 0; font-family: var(--font-orbital-bold); text-decoration: none; border-radius: 4px; text-align: center; cursor: pointer; transition: background-color 0.2s ease, color 0.2s ease, transform 0.1s ease; font-weight: bold; border: 2px solid transparent; }
    .post-content :global(a.block-button.btn--default) { background-color: var(--info-color); color: var(--text-color-light); border-color: var(--info-color); }
    .post-content :global(a.block-button.btn--default:hover) { background-color: #307db8; border-color: #307db8; }
    .post-content :global(a.block-button.btn--secondary) { background-color: var(--secondary-color); color: var(--text-color-light); border-color: var(--secondary-color); }
    .post-content :global(a.block-button.btn--secondary:hover) { background-color: #a51f58; border-color: #a51f58; }

    /* --- Toggle Block Styling --- */
    .post-content :global(details.block-toggle) { margin: 2rem 0; padding: 1rem; border: 1px solid var(--border-color-dark); border-radius: 6px; background-color: var(--block-bg-dark); }
    .post-content :global(details.block-toggle summary) { cursor: pointer; font-weight: bold; font-family: var(--font-orbital-bold); color: var(--primary-text-color); padding: 0.5rem; margin: -0.5rem; outline: none; }
    .post-content :global(details.block-toggle summary::marker),
    .post-content :global(details.block-toggle summary::-webkit-details-marker) { color: var(--primary-text-color); }
    .post-content :global(details.block-toggle div.toggle-content) { padding-top: 1rem; border-top: 1px solid var(--border-color-dark); margin-top: 1rem; }

    /* --- TextVariantTune example --- */
    .post-content :global(.text-variant-call-out) { background-color: var(--block-bg-darker); padding: 1em; border-left: 4px solid var(--info-color); margin: 1.5em 0; border-radius: 0 4px 4px 0; }

    /* --- Layout Block (Columns) --- */
    .post-content :global(div.block-layout.editorjs-columns_wrapper) { display:flex; margin: 10px 0; /* Removed side margin to rely on column gap */ flex-direction: row; gap: 1.5rem; /* Add gap between columns */ }
    .post-content :global(div.block-layout .editorjs-columns_col) { flex: 1; min-width: 0; }


    /* --- Admin Controls & Back Link --- */
    .admin-controls { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border-color-dark); display: flex; gap: 1rem; justify-content: flex-end; }
    .edit-button, .delete-button { font-family: var(--font-orbital); padding: 0.6rem 1.2rem; border: none; border-radius: 4px; cursor: pointer; transition: background-color 0.2s ease; font-weight: bold; }
    .edit-button { background-color: var(--info-color); color: white; }
    .edit-button:hover { background-color: #307db8; }
    .delete-button { background-color: var(--secondary-color); color: white; }
    .delete-button:hover { background-color: #a51f58; }
    .back-to-list { display: inline-block; margin-top: 3rem; padding: 0.75rem 1.5rem; font-family: var(--font-orbital); border: 2px solid var(--info-color); color: var(--info-color); border-radius: 4px; text-decoration: none; font-weight: bold; transition: background-color 0.2s ease, color 0.2s ease; }
    .back-to-list:hover { background-color: var(--info-color); color: var(--body-bg-color); text-decoration: none; }
</style>