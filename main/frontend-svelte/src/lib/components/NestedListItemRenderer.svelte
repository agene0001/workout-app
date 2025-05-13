<!-- $lib/components/NestedListItemRenderer.svelte -->
<script>
	export let item;
	export let listStyle; // 'ordered' or 'unordered'
</script>

<li>
	{#if typeof item === 'string'}
		{@html item} <!-- Handles simple list items (item is a string) -->
	{:else if typeof item === 'object' && item !== null && item.content !== undefined}
		{@html item.content} <!-- Handles the content of a nested list item -->
		{#if item.items && item.items.length > 0}
			<svelte:element this={listStyle === 'ordered' ? 'ol' : 'ul'}>
				{#each item.items as subItem ( (typeof subItem === 'string' ? subItem : subItem.id || subItem.content) || Math.random())}
					<!-- Recursive call for sub-items -->
					<svelte:self item={subItem} listStyle={listStyle} />
				{/each}
			</svelte:element>
		{/if}
	{:else}
		<!-- Fallback for unexpected item structure, or if item is null/undefined -->
		<!-- You might want to log an error here or render nothing -->
		<span><!-- Invalid item data --></span>
	{/if}
</li>

<style>
	/* Minimal styling, inherit from parent or global styles */
	ul, ol {
		margin-top: 0.25em;
		margin-bottom: 0.25em;
		padding-left: 1.5em; /* Ensure nested lists are indented */
	}
</style>