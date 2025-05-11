<script>
	import {getContext, onMount} from 'svelte';
	import { page } from '$app/stores';
	import {goto} from "$app/navigation";

	// Add export let post to receive the data from the load function
	const { post } = $page.data;

	const isAdmin = getContext('isAdmin');
	let parsedContent = [];


	onMount(async () => {

		// Parse the content if it's a string
		if (typeof post.content === 'string') {
			try {
				parsedContent = JSON.parse(post.content);
			} catch (e) {
				console.error('Failed to parse post content:', e);
				// If parsing fails, we'll treat it as HTML content
			}
		} else if (post.content && post.content.blocks) {
			// If content is already an object with blocks
			parsedContent = post.content;
		}

		console.log('Parsed content:', parsedContent);
	});

	// Format date to readable format
	function formatDate(dateString) {
		const options = { year: 'numeric', month: 'long', day: 'numeric' };
		return new Date(dateString).toLocaleDateString(undefined, options);
	}

	// ...

	function handleEditPost(id) {
		goto(`/Blog/admin/post/${id}`); // Navigate to the new unified admin edit route
	}

	function handleDeletePost(id, title) {
		// Implement delete functionality
		if (confirm(`Are you sure you want to delete "${title}"?`)) {
			// Delete post logic here
		}
	}

	// Helper function to render blocks based on their type
	// Helper function to render blocks based on their type
	function renderBlock(block) {
		if (!block) return null;

		switch (block.type) {
			case 'header':
				return {
					tag: `h${block.data.level}`,
					content: block.data.text,
					className: 'block-header'
				};
			case 'paragraph':
				return {
					tag: 'p',
					content: block.data.text,
					className: 'block-paragraph'
				};
			case 'list':
				return {
					tag: block.data.style === 'ordered' ? 'ol' : 'ul',
					items: block.data.items,
					className: `block-list ${block.data.style}-list`
				};
			case 'image':
				return {
					tag: 'figure',
					content: '',
					className: 'block-image',
					children: [
						{
							tag: 'img',
							src: block.data.file?.url,
							alt: block.data.caption || 'Blog image',
							className: 'block-image__img'
						},
						block.data.caption ? {
							tag: 'figcaption',
							content: block.data.caption,
							className: 'block-image__caption'
						} : null
					].filter(Boolean)
				};
			case 'quote':
				return {
					tag: 'blockquote',
					content: block.data.text,
					className: 'block-quote',
					children: block.data.caption ? {
						tag: 'cite',
						content: block.data.caption,
						className: 'block-quote__caption'
					} : null
				};
			case 'delimiter':
				return {
					tag: 'hr',
					content: '',
					className: 'block-delimiter'
				};
			case 'table':
				return {
					tag: 'table',
					className: 'block-table',
					isTable: true,
					data: block.data
				};
			case 'code':
				return {
					tag: 'pre',
					className: 'block-code',
					children: {
						tag: 'code',
						content: block.data.code,
						className: `language-${block.data.language || 'plaintext'}`
					}
				};
			case 'embed':
				return {
					tag: 'div',
					className: 'block-embed',
					embed: true,
					data: block.data
				};
				// Add more cases for other block types as needed
			default:
				return {
					tag: 'div',
					content: JSON.stringify(block.data),
					className: `block-unknown block-${block.type}`
				};
		}
	}
</script>

<div class="post-container">
	<h1 class="post-title text-primary">{post.title}</h1>
	<p class="post-meta">{formatDate(post.publishedAt)} • {post.readTime} min read</p>

	<!-- Display post content as blocks -->
	<div class="post-content text-primary">
		{#if parsedContent && parsedContent.blocks && parsedContent.blocks.length > 0}
			{#each parsedContent.blocks as block (block.id)}
				{@const renderedBlock = renderBlock(block)}

				{#if renderedBlock?.tag === 'ul' || renderedBlock?.tag === 'ol'}
					<svelte:element this={renderedBlock.tag} class={renderedBlock.className}>
						{#each renderedBlock.items as item}
							<li>{@html item}</li>
						{/each}
					</svelte:element>

				{:else if renderedBlock?.isTable}
					<table class={renderedBlock.className}>
						{#each renderedBlock.data.content as row}
							<tr>
								{#each row as cell}
									<td>{@html cell}</td>
								{/each}
							</tr>
						{/each}
					</table>

				{:else if renderedBlock?.children && Array.isArray(renderedBlock.children)}
					<svelte:element this={renderedBlock.tag} class={renderedBlock.className}>
						{#each renderedBlock.children as child}
							{#if child}
								<svelte:element this={child.tag}
												class={child.className}
												src={child.src}
												alt={child.alt}>
									{@html child.content || ''}
								</svelte:element>
							{/if}
						{/each}
					</svelte:element>

				{:else if renderedBlock?.children && !Array.isArray(renderedBlock.children)}
					<svelte:element this={renderedBlock.tag} class={renderedBlock.className}>
						<svelte:element this={renderedBlock.children.tag} class={renderedBlock.children.className}>
							{@html renderedBlock.children.content || ''}
						</svelte:element>
					</svelte:element>

				{:else if renderedBlock?.embed}
					<div class={renderedBlock.className}>
						{#if renderedBlock.data.service === 'youtube'}
							<iframe
									width="100%"
									height="400"
									src={`https://www.youtube.com/embed/${renderedBlock.data.embed}`}
									frameborder="0"
									allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
									allowfullscreen
									title="Embedded YouTube video">
							</iframe>
						{:else if renderedBlock.data.service === 'vimeo'}
							<iframe
									width="100%"
									height="400"
									src={`https://player.vimeo.com/video/${renderedBlock.data.embed}`}
									frameborder="0"
									allow="autoplay; fullscreen; picture-in-picture"
									allowfullscreen
									title="Embedded Vimeo video">
							</iframe>
						{:else}
							<div class="unsupported-embed">
								<a href={renderedBlock.data.embed} target="_blank" rel="noopener noreferrer">
									{renderedBlock.data.caption || 'View embedded content'}
								</a>
							</div>
						{/if}
					</div>

				{:else}
					<svelte:element this={renderedBlock?.tag}
									class={renderedBlock?.className}
									src={renderedBlock?.src}
									alt={renderedBlock?.alt}>
						{@html renderedBlock?.content || ''}
					</svelte:element>
				{/if}
			{/each}
		{:else if typeof post.content === 'string' && !parsedContent.blocks}
			<!-- Fallback to render as HTML if parsing failed or it's pure HTML -->
			{@html post.content}
		{/if}
	</div>

	<!-- Admin Controls -->
	{#if $isAdmin}
		<div class="admin-controls">
			<button on:click={() => handleEditPost(post.id)} class="edit-button">Edit</button>
			<button on:click={() => handleDeletePost(post.id, post.title)} class="delete-button">Delete</button>
		</div>
	{/if}

	<!-- Navigation back to the blog list -->
	<a href="/Blog" class="back-to-list">Back to Blog</a>
</div>

<style>
	.post-container {
		margin-top: 8rem;
		max-width: 800px;
		margin-left: auto;
		margin-right: auto;
		padding: 0 1rem;
	}

	.post-title {
		font-size: 2.5rem;
		font-weight: 700;
		margin-bottom: 0.5rem;
	}

	.post-meta {
		color: #666;
		margin-bottom: 2rem;
	}

	.post-content {
		line-height: 1.6;
	}

	.block-header {
		margin-top: 2rem;
		margin-bottom: 1rem;
	}

	.block-paragraph {
		margin-bottom: 1.5rem;
	}

	.block-list {
		margin-bottom: 1.5rem;
		padding-left: 1.5rem;
	}

	.block-list li {
		margin-bottom: 0.5rem;
	}

	.admin-controls {
		margin-top: 3rem;
		display: flex;
		gap: 1rem;
	}

	.edit-button, .delete-button {
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	.edit-button {
		background-color: #4a90e2;
		color: white;
	}

	.delete-button {
		background-color: #e25c5c;
		color: white;
	}

	.back-to-list {
		display: inline-block;
		margin-top: 2rem;
		color: #4a90e2;
		text-decoration: none;
	}

	.back-to-list:hover {
		text-decoration: underline;
	}
	.block-quote__caption {
		display: block;
		margin-top: 1rem;
		font-size: 0.9rem;
		text-align: right;
		font-style: normal;
		color: #666;
	}

	.block-delimiter {
		border: none;
		height: 1px;
		background-color: #e0e0e0;
		margin: 2rem auto;
		width: 30%;
	}

	.block-table {
		width: 100%;
		border-collapse: collapse;
		margin: 2rem 0;
		overflow-x: auto;
		display: block;
	}

	.block-table td {
		border: 1px solid #e0e0e0;
		padding: 0.75rem;
	}

	.block-table tr:nth-child(even) {
		background-color: #f8f8f8;
	}

	.block-code {
		margin: 2rem 0;
		background-color: #f5f5f5;
		border-radius: 8px;
		padding: 1.5rem;
		overflow-x: auto;
	}

	.block-code code {
		font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
		font-size: 0.9rem;
		line-height: 1.5;
	}

	.block-embed {
		margin: 2rem 0;
	}

	.unsupported-embed {
		padding: 2rem;
		text-align: center;
		background-color: #f8f8f8;
		border-radius: 8px;
	}

	.unsupported-embed a {
		color: #4a90e2;
		text-decoration: none;
		font-weight: 500;
	}

	.unsupported-embed a:hover {
		text-decoration: underline;
	}
</style>