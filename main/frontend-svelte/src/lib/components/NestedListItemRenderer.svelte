<!-- $lib/components/NestedListItemRenderer.svelte -->
<script>
	export let item;
	export let listStyle = 'unordered';
	export let isChecklistType = false;

	// $: content = typeof item === 'string' ? item : item?.content; // LINE A
	// $: subItems = typeof item === 'object' && item !== null && item.items && item.items.length > 0 ? item.items : null; // LINE B
	// $: isChecked = isChecklistType && item?.meta?.checked === true; // LINE C

	// Let's make these regular variables first for clarity during debugging
	let currentContent;
	let currentSubItems;
	let currentIsChecked;

	$: { // Reactive block to update when props change
		currentContent = typeof item === 'string' ? item : item?.content;
		currentSubItems = typeof item === 'object' && item !== null && item.items && item.items.length > 0 ? item.items : null;
		currentIsChecked = isChecklistType && item?.meta?.checked === true;
	}


	function getItemKey(it) {
		if (typeof it === 'string') return it + Math.random();
		return (it?.id || it?.content || currentContent || '') + Math.random(); // Added currentContent as fallback
	}
</script>

<li
		class:checked={currentIsChecked}
class:is-checklist-item={isChecklistType}
>
{#if isChecklistType}
	<input type="checkbox" checked={currentIsChecked} disabled />  <!-- Use currentIsChecked -->
{/if}

{#if currentContent !== undefined} <!-- Use currentContent, LINE 18 (approx based on your error) -->
	{@html currentContent}
{/if}

{#if currentSubItems} <!-- Use currentSubItems -->
	{#if isChecklistType}
		<ul class="block-checklist">
			{#each currentSubItems as subItem (getItemKey(subItem))}
				<svelte:self item={subItem} {isChecklistType} listStyle={'unordered'} />
			{/each}
		</ul>
	{:else}
		<svelte:element this={listStyle === 'ordered' ? 'ol' : 'ul'} class="block-list {listStyle}-list">
			{#each currentSubItems as subItem (getItemKey(subItem))}
				<svelte:self item={subItem} {listStyle} isChecklistType={false}/>
			{/each}
		</svelte:element>
	{/if}
{/if}
</li>

<style>
	/* Minimal styles */
</style>