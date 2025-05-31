<script lang="ts">
    import { onMount, tick } from 'svelte';
    import { browser } from '$app/environment';

    export let blocks: any[] = []; // Parsed blocks from EditorJS
    export let title: string = "Table of Contents";

    type TocItem = {
        id: string;
        text: string;
        level: number;
        children: TocItem[];
    };

    let tocItems: TocItem[] = [];

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

    function getAnchorIdFromTune(tunes: any): string | null {
        return tunes?.anchorTune?.anchor || null;
    }


    onMount(async () => {
        await tick(); // Ensure DOM is updated if headers are rendered with IDs
        if (browser) {
            const extractedHeaders: TocItem[] = [];
            blocks.forEach((block, index) => {
                if (block.type === 'header') {
                    const text = block.data.text;
                    const level = parseInt(String(block.data.level), 10);
                    // Use existing ID from anchorTune if available, otherwise generate one
                    let id = getAnchorIdFromTune(block.tunes) || generateSlug(text) + `-${index}`;

                    // Ensure the actual H tag in the DOM has this ID
                    // This assumes your BlockRenderer.svelte or renderBlock logic assigns these IDs.
                    // If not, you might need to do it here or ensure renderBlock does.
                    // For now, we assume renderBlock already handles ID assignment from `tuneId`.

                    if (text && level >=1 && level <= 6) { // typically h1-h6, adjust if needed
                        extractedHeaders.push({
                            id: id,
                            text: text,
                            level: level,
                            children: [] // For potential future nested TOC
                        });
                    }
                }
            });
            tocItems = buildNestedToc(extractedHeaders);
        }
    });

    // Basic nested TOC builder (can be enhanced for deeper nesting)
    function buildNestedToc(headers: Omit<TocItem, 'children'>[]): TocItem[] {
        const result: TocItem[] = [];
        const stack: TocItem[] = [];

        headers.forEach(header => {
            const newItem: TocItem = { ...header, children: [] };
            while (stack.length > 0 && stack[stack.length - 1].level >= newItem.level) {
                stack.pop();
            }
            if (stack.length > 0) {
                stack[stack.length - 1].children.push(newItem);
            } else {
                result.push(newItem);
            }
            stack.push(newItem);
        });
        return result;
    }

    function scrollToSection(event: MouseEvent, id: string) {
        event.preventDefault();
        const element = document.getElementById(id);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Optional: Update URL hash
            // window.location.hash = id;
        } else {
            console.warn(`TOC: Element with id "${id}" not found.`);
        }
    }
</script>

{#if tocItems.length > 0}
    <div class="toc-container">
        <h3 class="toc-title">{title}</h3>
        <ul class="toc-list level-1">
            {#each tocItems as item (item.id)}
                <li class="toc-item level-{item.level}">
                    <a href="#{item.id}" on:click={(e) => scrollToSection(e, item.id)}>
                        {item.text}
                    </a>
                    {#if item.children.length > 0}
                        <ul class="toc-list level-{item.level + 1}">
                            {#each item.children as subItem (subItem.id)}
                                <li class="toc-item level-{subItem.level}">
                                    <a href="#{subItem.id}" on:click={(e) => scrollToSection(e, subItem.id)}>
                                        {subItem.text}
                                    </a>
                                    <!-- Add more recursion here if you expect > 2 levels -->
                                </li>
                            {/each}
                        </ul>
                    {/if}
                </li>
            {/each}
        </ul>
    </div>
{/if}

<style>
    .toc-container {
        background-color: var(--block-bg-dark, #0f3040);
        padding: 1.5rem;
        margin-bottom: 2.5rem;
        border-radius: 8px;
        border: 1px solid var(--border-color-dark, #445259);
    }

    .toc-title {
        font-family: var(--font-orbital-bold);
        font-size: 1.5rem;
        color: var(--primary-text-color);
        margin-top: 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--border-color-dark);
        padding-bottom: 0.5rem;
    }

    .toc-list {
        list-style: none;
        padding-left: 0;
        margin: 0;
    }
    .toc-list .toc-list { /* Nested lists */
        padding-left: 1.5em; /* Indentation for nested items */
        margin-top: 0.5em;
    }

    .toc-item {
        margin-bottom: 0.6rem;
        line-height: 1.4;
    }
    .toc-item a {
        text-decoration: none;
        color: var(--info-color);
        transition: color 0.2s ease;
        font-family: var(--font-orbital);
    }
    .toc-item a:hover {
        color: var(--secondary-color);
        text-decoration: underline;
    }

    /* Optional: Style based on level if needed */
    .toc-item.level-1 > a { font-weight: 600; }
    .toc-item.level-2 > a { font-size: 0.95em; }
    .toc-item.level-3 > a { font-size: 0.9em; }
</style>