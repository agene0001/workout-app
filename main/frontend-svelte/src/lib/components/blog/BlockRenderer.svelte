<script>
    export let renderedBlock;
    export let renderBlock; // The renderBlock function from the parent
    export let NestedListItemRenderer; // The NestedListItemRenderer component from the parent
</script>

{#if renderedBlock}
    {#if renderedBlock.isAnyList} <!-- Handles ordered and unordered lists -->
        <svelte:element this={renderedBlock.tag} class={renderedBlock.className} id={renderedBlock.id}>
            {#each renderedBlock.items as listItem ((typeof listItem === 'string' ? listItem : listItem.id || listItem.content) || Math.random())}
                <NestedListItemRenderer item={listItem} listStyle={renderedBlock.listStyle} />
            {/each}
        </svelte:element>
    {:else if renderedBlock.isChecklist} <!-- Handles checklists -->
        <ul class={renderedBlock.className} id={renderedBlock.id}>
            {#each renderedBlock.items as item (item.text || item.content + Math.random())}
                {@const text = item.content} <!-- Checklist items from @editorjs/list use "content" -->
                {@const checked = item.meta && item.meta.checked}
                <li class={checked ? 'checked' : ''}>
                    <input type="checkbox" {checked} disabled />
                    {@html text}
                </li>
            {/each}
        </ul>

    {:else if renderedBlock.isTable}
        <table class={renderedBlock.className} id={renderedBlock.id}>
            {#if renderedBlock.data.withHeadings}
                <thead>
                <tr>
                    {#each renderedBlock.data.content[0] as thContent (thContent + Math.random())}
                        <th>{@html thContent}</th>
                    {/each}
                </tr>
                </thead>
                <tbody>
                {#each renderedBlock.data.content.slice(1) as row (row.join('') + Math.random())}
                    <tr>
                        {#each row as cell (cell + Math.random())}
                            <td>{@html cell}</td>
                        {/each}
                    </tr>
                {/each}
                </tbody>
            {:else}
                <tbody>
                {#each renderedBlock.data.content as row (row.join('') + Math.random())}
                    <tr>
                        {#each row as cell (cell + Math.random())}
                            <td>{@html cell}</td>
                        {/each}
                    </tr>
                {/each}
                </tbody>
            {/if}
        </table>
    {:else if renderedBlock.isWarning}
        <div class={renderedBlock.className} id={renderedBlock.id}>
            {#if renderedBlock.data.title}
                <strong class="block-warning__title">{@html renderedBlock.data.title}</strong>
            {/if}
            <div class="block-warning__message">{@html renderedBlock.data.message}</div>
        </div>
    {:else if renderedBlock.isAttachment}
        <div class={renderedBlock.className} id={renderedBlock.id}>
            <a href={renderedBlock.data.file?.url} target="_blank" rel="noopener noreferrer" download={renderedBlock.data.file?.name}>
                <strong>{renderedBlock.data.title || renderedBlock.data.file?.name}</strong>
                {#if renderedBlock.data.file?.size}
                    <em>({(renderedBlock.data.file.size / 1024).toFixed(2)} KB)</em>
                {/if}
            </a>
        </div>
    {:else if renderedBlock.isButton}
        <a
                href={renderedBlock.href}
                class={renderedBlock.className}
                id={renderedBlock.id}
                target={renderedBlock.attributes?.target}
                rel={renderedBlock.attributes?.rel}
        >
            {@html renderedBlock.content}
        </a>
    {:else if renderedBlock.isToggle}
        <details class={renderedBlock.className} id={renderedBlock.id} open={renderedBlock.isOpen}>
            <summary>{@html renderedBlock.summaryText}</summary>
            <div class="toggle-content">
                {#if renderedBlock.nestedBlocks && renderedBlock.nestedBlocks.length > 0}
                    {#each renderedBlock.nestedBlocks as nestedBlock (nestedBlock.id || nestedBlock.type + Math.random())}
                        {@const subRenderedBlock = renderBlock(nestedBlock)}
                        {#if subRenderedBlock}
                            <svelte:self
                                    renderedBlock={subRenderedBlock}
                                    {renderBlock}
                                    {NestedListItemRenderer}
                            />
                        {/if}
                    {/each}
                {/if}
            </div>
        </details>
    {:else if renderedBlock.isHtmlContent}
        {@html renderedBlock.html}
    {:else if renderedBlock.children && Array.isArray(renderedBlock.children)}
        <svelte:element this={renderedBlock.tag} class={renderedBlock.className} id={renderedBlock.id} src={renderedBlock.src} alt={renderedBlock.alt}>
            {#each renderedBlock.children as child}
                {#if child}
                    <svelte:element
                            this={child.tag}
                            class={child.className}
                            src={child.src}
                            alt={child.alt}
                    >
                        {@html child.content || ''}
                    </svelte:element>
                {/if}
            {/each}
        </svelte:element>
    {:else if renderedBlock.tag === 'blockquote'}
        <svelte:element this={renderedBlock.tag} class={renderedBlock.className} id={renderedBlock.id}>
            {@html renderedBlock.content || ''}
            {#if renderedBlock.children}
                <svelte:element
                        this={renderedBlock.children.tag}
                        class={renderedBlock.children.className}
                >
                    {@html renderedBlock.children.content || ''}
                </svelte:element>
            {/if}
        </svelte:element>
    {:else if renderedBlock.children && !Array.isArray(renderedBlock.children)}
        <svelte:element this={renderedBlock.tag} class={renderedBlock.className} id={renderedBlock.id} src={renderedBlock.src} alt={renderedBlock.alt}>
            <svelte:element
                    this={renderedBlock.children.tag}
                    class={renderedBlock.children.className}
            >
                {@html renderedBlock.children.content || ''}
            </svelte:element>
        </svelte:element>
    {:else if renderedBlock.embed}
        <div class={renderedBlock.className} id={renderedBlock.id}>
            {#if renderedBlock.data.service === 'youtube'}
                <iframe
                        width="100%"
                        height="400"
                        src={`https://www.youtube.com/embed/${renderedBlock.data.embed}`}
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen
                        title="Embedded YouTube video"
                ></iframe>
            {:else if renderedBlock.data.service === 'vimeo'}
                <iframe
                        width="100%"
                        height="400"
                        src={`https://player.vimeo.com/video/${renderedBlock.data.embed}`}
                        frameborder="0"
                        allow="autoplay; fullscreen; picture-in-picture"
                        allowfullscreen
                        title="Embedded Vimeo video"
                ></iframe>
            {:else}
                <div class="unsupported-embed">
                    <a href={renderedBlock.data.embed} target="_blank" rel="noopener noreferrer">
                        {renderedBlock.data.caption || 'View embedded content'}
                    </a>
                </div>
            {/if}
        </div>
    {:else if renderedBlock.isLayout}
        <div class={renderedBlock.className} id={renderedBlock.id}>
            {#each renderedBlock.columnsData as column}
                <div class="editorjs-columns_col">
                    {#if column.blocks && column.blocks.length > 0}
                        {#each column.blocks as colBlock (colBlock.id || colBlock.type + Math.random())}
                            {@const subRenderedBlock = renderBlock(colBlock)}
                            {#if subRenderedBlock}
                                <svelte:self
                                        renderedBlock={subRenderedBlock}
                                        {renderBlock}
                                        {NestedListItemRenderer}
                                />
                            {/if}
                        {/each}
                    {/if}
                </div>
            {/each}
        </div>
    {:else}
        <!-- Generic fallback for tags like p, h1-h6, hr, etc. that don't have special flags -->
        <svelte:element
                this={renderedBlock.tag}
                class={renderedBlock.className}
                id={renderedBlock.id}
                src={renderedBlock.src}
                alt={renderedBlock.alt}
        >
            {@html renderedBlock.content || ''}
        </svelte:element>
    {/if}
{/if}

<!-- No <style> tag needed here as styles are global in the parent -->