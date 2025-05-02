<script>
	import { onMount, onDestroy, createEventDispatcher, tick } from 'svelte';
	import axios from 'axios';
	import Portal from './Portal.svelte';
	// Props

	export let title = '';
	export let headingClass = 'text-4xl font-orbital font-bold';
	export let text = [];
	export let recipe = null;
	export let recipeArray = null; // New prop for array of recipe variations
	export let fadeInAnimation = '';
	export let bg = 'bg-danger'; // bg-danger -> Tailwind equivalent
	export let expandable = false; // Make sure this is true when you use the component!

	// Local state
	let expanded = false;
	let mounted = false;
	let instacartData = null;
	let isLoading = false;
	let currentRecipeId = null;
	let fetchError = null;
	let selectedRecipeIndex = 0; // Track which recipe variation is currently shown

	// Element refs
	let ref;

	const dispatch = createEventDispatcher();

	// Get currently selected recipe variation
	$: currentRecipe = recipeArray && recipeArray.length > 0
			? recipeArray[selectedRecipeIndex]
			: recipe;

	// Variation count for display
	$: variationCount = recipeArray ? recipeArray.length : 0;
	$: hasVariations = variationCount > 1;

	function nextRecipeVariant() {
		if (!hasVariations) return;
		selectedRecipeIndex = (selectedRecipeIndex + 1) % variationCount;
		if(mounted && !expanded) toggleExpand();
	}

	function prevRecipeVariant() {
		if (!hasVariations) return;
		selectedRecipeIndex = selectedRecipeIndex === 0
				? variationCount - 1
				: selectedRecipeIndex - 1;
		if(mounted && !expanded) toggleExpand();
	}
	function toTitleCase(str) {
		return str.replace(/\w\S*/g, function (txt) {
			return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
		});
	}
	onMount(() => {
		mounted = true;
		// Ensure cleanup happens even if component is destroyed before expansion
		return () => {
			if (document.body.style.overflow === 'hidden') {
				document.body.style.overflow = '';
			}
		};
	});

	// onDestroy is still useful if component unmounts while expanded
	onDestroy(() => {
		if (expanded) {
			document.body.style.overflow = '';
		}
	});

	// Reset instacart data when recipe changes
	$: if (currentRecipe && (!currentRecipeId || currentRecipeId !== currentRecipe.name)) {
		instacartData = null;
		fetchError = null; // Also reset error on recipe change
		currentRecipeId = currentRecipe.name;
	}

	// Fetch Instacart data when expanded and we have a recipe
	$: if (mounted && expanded && currentRecipe && !instacartData && !isLoading && !fetchError) {
		// Use tick to ensure DOM updates related to 'expanded' are flushed
		// before potentially long-running fetch, although likely not strictly necessary here.
		tick().then(fetchInstacartData);
	}

	async function fetchInstacartData() {
		if (!currentRecipe || isLoading) return; // Prevent multiple simultaneous fetches

		isLoading = true;
		fetchError = null; // Reset error state

		try {
			console.log('Processing recipe:', currentRecipe);

			const res = await axios.post('/recipes/process-recipe', {
				ingredients: currentRecipe.ingredients,
				instructions: currentRecipe.instructions,
				title: currentRecipe.name,
				image_url: currentRecipe.imgSrc
			});

			console.log('Instacart response:', res.data);
			instacartData = res.data || null; // Ensure null if data is empty/falsy
		} catch (error) {
			console.error('Error fetching Instacart data:', error);
			let errorMessage = 'Failed to fetch recipe data';
			if (error instanceof Error) {
				errorMessage = error.message;
			} else if (typeof error === 'string') {
				errorMessage = error;
			}
			fetchError = errorMessage;
			instacartData = null; // Ensure null on error
		} finally {
			isLoading = false;
		}
	}

	function toggleExpand() {
		// Only toggle if the component is meant to be expandable
		if (expandable) {
			expanded = !expanded;
			console.log('Toggled expand, new state:', expanded); // Debug log
			// Apply/remove body overflow style
			if (expanded) {
				document.body.style.overflow = 'hidden';
			} else {
				// Ensure style is removed only if it was set by this component
				if (document.body.style.overflow === 'hidden') {
					document.body.style.overflow = '';
				}
			}
		} else {
			console.log('InfoBlock clicked, but not expandable.'); // Debug log
		}
	}

	function handleMouseOver(e) {
		e.currentTarget.style.transform = 'scale(1.03)';
		e.currentTarget.style.boxShadow = '0 10px 15px rgba(0,0,0,0.2)';
	}

	function handleMouseOut(e) {
		e.currentTarget.style.transform = 'scale(1)';
		e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
	}

	// This function stops the click event on the modal content
	// from bubbling up to the modal backdrop, which would close the modal.
	function stopPropagation(e) {
		e.stopPropagation();
	}
</script>

<!-- Regular view (Card) -->
<div
		bind:this={ref}
		class="{fadeInAnimation} {bg} bg-gradient-to-t from-gray-700 to-transparent infoBlock m-4 rounded-xl p-3 {expandable ? 'cursor-pointer' : ''}"
		style="width: 100%; box-sizing: border-box; transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;"
		on:click={toggleExpand}
		on:mouseover={handleMouseOver}
		on:mouseout={handleMouseOut}
		role={expandable ? 'button' : undefined}
		tabindex={expandable ? 0 : -1}
		on:keydown={(e) => {
		if (expandable && (e.key === 'Enter' || e.key === ' ')) toggleExpand();
	}}
>
	{#if currentRecipe?.imgSrc}
		<div class="flex justify-center">
			<div class="mb-3 overflow-hidden rounded-xl" style="max-width: 100%; max-height: 200px">
				<img
						class="h-full w-full"
						src={currentRecipe.imgSrc}
						alt={title || 'Recipe image'}
						style="object-fit: contain"
				/>
			</div>
		</div>
	{/if}

	{#if title}
		<h1 class="{headingClass} mb-2 text-center">{toTitleCase(title)}</h1>
	{/if}

	{#if hasVariations}
		<p class=" text-xl mb-2 text-center text-sm font-orbital-regular text-gray-700">
			Recipe variant {selectedRecipeIndex + 1} of {variationCount}
		</p>
		<div class="flex justify-center space-x-4 mb-4">
			<button
					class="px-3 py-1 bg-black text-white rounded-md hover:bg-gray-700 transition-colors"
					on:click={prevRecipeVariant}
			>
				Previous variant
			</button>
			<button
					class="px-3 py-1 bg-black text-white rounded-md hover:bg-gray-700 transition-colors"
					on:click={nextRecipeVariant}
			>
				Next variant
			</button>
		</div>
	{/if}

	{#each text as paragraph}
		<p class="mb-4 text-grey-900 font-orbital-regular">{@html paragraph}</p>
	{/each}
</div>

<!-- Modal view using Portal component -->
{#if mounted && expanded}
	<Portal>
		<!-- Backdrop -->
		<div
				class="modal-backdrop fixed top-0 left-0 flex h-full w-full items-center justify-center"
				style="background-color: rgba(0,0,0,0.7); pointer-events: auto;"
				on:click={toggleExpand}
				role="dialog"
				aria-modal="true"
				aria-labelledby="modal-title"
		>
			<!-- Modal Content -->
			<div
					class="modal-content {bg.split(' ')[0]} relative rounded-xl p-5"
					style="width: 80%; max-width: 600px; max-height: 80vh; overflow-y: auto; pointer-events: auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5);"
					on:click={stopPropagation}
			>
				<!-- Close Button -->
				<button
						class="absolute top-2 right-2 rounded bg-black px-2 py-1 text-xl leading-none text-white hover:bg-gray-700"
						on:click={toggleExpand}
						aria-label="Close modal"
				>
					× <!-- Use × for a standard 'x' -->
				</button>

				{#if currentRecipe?.imgSrc}
					<div class="mt-4 flex justify-center">
						<!-- Added mt-4 for spacing from potential top elements -->
						<div class="mb-3 overflow-hidden rounded-3xl" style="max-width: 45%; max-height: 200px">
							<img
									class="h-full w-full"
									src={currentRecipe.imgSrc}
									alt={title || 'Recipe image'}
									style="object-fit: contain"
							/>
						</div>
					</div>
				{/if}

				<h1 id="modal-title" class="font-orbital py-4 text-center text-5xl font-bold text-gray-800">
					{title}
				</h1>

				<!-- Recipe variation controls -->
				{#if hasVariations}
					<div class="flex justify-center space-x-4 mb-4">
						<button
								class="px-3 py-1 bg-black text-white rounded-md hover:bg-gray-700 transition-colors"
								on:click={prevRecipeVariant}
						>
							Previous variant
						</button>
						<span class="flex items-center">
							{selectedRecipeIndex + 1} of {variationCount}
						</span>
						<button
								class="px-3 py-1 bg-black text-white rounded-md hover:bg-gray-700 transition-colors"
								on:click={nextRecipeVariant}
						>
							Next variant
						</button>
					</div>
				{/if}
				<p class="paraAnimate mb-3 text-lg">
					<!-- Added mb-3 for spacing -->
					{recipe?.duration}
				</p>
				{#each text as item, index}
					<p class="paraAnimate mb-3 text-lg">
						<!-- Added mb-3 for spacing -->
						{item}
					</p>
				{/each}



				<!-- Instacart Section -->
				<div class="mt-4 flex justify-center">
					<!-- Added container and centering -->
					{#if isLoading}
						<div class="text-amber-500">Loading Instacart data...</div>
					{:else if instacartData && instacartData.response?.products_link_url}
						<button
								class="flex h-[46px] items-center gap-2 rounded-full bg-[#003D29] px-[18px] py-[16px] text-[#FAF1E5] transition-colors hover:bg-[#005a3f]"
						>
							<a
									target="_blank"
									rel="noopener noreferrer"
									class="flex items-center gap-2 font-medium text-[#FAF1E5]"
									href={instacartData.response.products_link_url}
							>
								<img src="imgs/Instacart_Carrot.png" alt="Instacart Logo" class="h-[22px] w-[22px]" />
								Get Recipe Ingredients
							</a>
						</button>
					{:else if fetchError}
						<div class="rounded border border-red-600 bg-red-100 p-2 text-red-600">
							{fetchError}
						</div>
					{/if}
				</div>
			</div>
		</div>
	</Portal>
{/if}

<style>
	/* Animation for paragraph text */
	.paraAnimate {
		animation: fadeIn 0.5s ease-in-out;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	/* Special styles for the modal to ensure it escapes any parent container */
	:global(.svelte-portal-container) {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 9999999 !important;
		pointer-events: none;
	}

	:global(.modal-backdrop) {
		position: fixed !important;
		top: 0 !important;
		left: 0 !important;
		width: 100vw !important;
		height: 100vh !important;
		pointer-events: auto !important;
		z-index: 9999999 !important;
		overflow: visible !important;
		display: flex !important;
		align-items: center !important;
		justify-content: center !important;
	}

	:global(.modal-content) {
		pointer-events: auto !important;
		transform: translateZ(0); /* Force hardware acceleration */
		will-change: transform; /* Hint for browser optimization */
		position: relative !important;
		z-index: 10000000 !important;
	}

	/* Fix for parent wrappers that might constrain the modal */
	:global(.wrapper) {
		position: relative;
		overflow: visible !important; /* Ensure no clipping */
	}
</style>