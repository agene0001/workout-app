<script>
	import {getContext, onMount} from 'svelte';
	import { writable } from 'svelte/store';
	import axios from 'axios';
	// Assuming your firebase.client.ts exports the initialized auth instance
	import {
		getClientAuth,
		checkIsUserAdmin
	} from '$lib/firebase/firebase.client'; // Adjust path if needed
	import { onAuthStateChanged, getIdTokenResult, getIdToken } from 'firebase/auth';

	// State variables
	let blogPosts = [];
	let categories = [];
	let selectedCategory = 'all';
	let searchQuery = '';
	let currentPage = 1;
	let postsPerPage = 6;
	let featuredPost = null;
	let isLoading = true;
	let error = null;
	let auth = getClientAuth();
	// User authentication state
	const isAdmin = getContext('isAdmin');

	// Pagination variables
	$: filteredPosts = filterPosts(blogPosts, selectedCategory, searchQuery);
	$: totalPages = Math.ceil(filteredPosts.length / postsPerPage);
	$: currentPosts = filteredPosts.slice(
		(currentPage - 1) * postsPerPage,
		currentPage * postsPerPage
	);

	// Format date to readable format
	function formatDate(dateString) {
		const options = { year: 'numeric', month: 'long', day: 'numeric' };
		return new Date(dateString).toLocaleDateString(undefined, options);
	}

	// Filter posts based on category and search query
	function filterPosts(posts, category, query) {
		return posts.filter((post) => {
			const matchesCategory = category === 'all' || post.category === category;
			const matchesQuery =
				query === '' ||
				post.title.toLowerCase().includes(query.toLowerCase()) ||
				post.excerpt.toLowerCase().includes(query.toLowerCase());
			return matchesCategory && matchesQuery;
		});
	}

	// Handle category change
	function handleCategoryChange(category) {
		selectedCategory = category;
		currentPage = 1;
	}

	// Handle search input change
	function handleSearchChange(e) {
		searchQuery = e.target.value;
		currentPage = 1;
	}

	// Change page
	function changePage(newPage) {
		if (newPage >= 1 && newPage <= totalPages) {
			currentPage = newPage;
			window.scrollTo({ top: 0, behavior: 'smooth' });
		}
	}

	// Fetch blog posts and categories on component mount
	onMount(async () => {
		// Firebase Auth State Listener
		console.log($isAdmin)
		// const unsubscribeAuth = onAuthStateChanged(auth, async (user) => {
		// 	if (user) {
		// 		currentUser.set(user);
		// 		try {
		// 			const idTokenResult = await getIdTokenResult(user);
		// 			// Check for the admin custom claim
		// 			// This matches the claim set in your Python Cloud Function: { admin: true }
		// 			isAdmin.set(idTokenResult.claims.admin === true);
		// 		} catch (err) {
		// 			console.error('Error getting ID token result:', err);
		// 			isAdmin.set(false);
		// 		}
		// 	} else {
		// 		currentUser.set(null);
		// 		isAdmin.set(false);
		// 	}
		// });

		try {
			isLoading = true;

			// Fetch blog posts
			const postsRes = await axios.get('/api/v1/blog/posts');
			blogPosts = postsRes.data;

			// Set featured post (most recent)
			if (blogPosts.length > 0) {
				featuredPost = blogPosts.find((post) => post.featured) || blogPosts[0];
				// Remove featured post from main list to avoid duplication
				blogPosts = blogPosts.filter((post) => post.id !== featuredPost.id);
			}

			// Fetch categories
			const categoriesRes = await axios.get('/api/v1/blog/categories');
			categories = categoriesRes.data;

			isLoading = false;
		} catch (err) {
			console.error('Error fetching blog data:', err);
			error = 'Failed to load blog content. Please try again later.';
			isLoading = false;
		}

		// Cleanup Firebase auth listener on component destroy
		// return () => {
		// 	unsubscribeAuth();
		// };
	});
	// Helper to check if the current user has admin custom claims



	async function handleEditPost(postId) {
		const isVerifiedAdmin = await checkIsUserAdmin();
		if (!isVerifiedAdmin) {
			alert('You do not have permission to edit posts.');
			return;
		}

		// This function would typically navigate to an edit page or open a modal
		// pre-filled with the data of the post to be edited.
		// Example (if using SvelteKit):
		// import { goto } from '$app/navigation';
		// goto(`/admin/edit-post/${postId}`);
		// Or, set a $state variable to open an edit modal:
		// editingPostId = postId; isEditModalOpen = true;

		alert(
			`Admin action: Navigate to an edit page/modal for post ID: ${postId}.\n\nYou'll need to: \n1. Create a UI for editing.\n2. Implement an 'edit_blog_post' Firebase Cloud Function (similar to 'add_blog_post' but it updates an existing document).\n3. Call that Cloud Function upon saving changes.`
		);

		// To implement fully, you would:
		// 1. Fetch the specific post's data.
		// 2. Populate an editing form/modal with this data.
		// 3. Create an 'edit_blog_post' Cloud Function that accepts 'postId' and the updated data.
		// 4. On form submission, call your 'edit_blog_post' Cloud Function.
		// 5. On success, update your local 'blogPosts' $state or re-fetch all posts.
	}

	async function handleDeletePost(postId, postTitle) {
		const isVerifiedAdmin = await checkIsUserAdmin();
		if (!isVerifiedAdmin || !auth.currentUser) {
			alert('You do not have permission to delete posts.');
			return;
		}

		if (
			confirm(
				`Are you sure you want to delete the post "${postTitle}" (ID: ${postId})? This action cannot be undone.`
			)
		) {
			try {
				const idToken = await getIdToken(auth.currentUser);
				alert('Deleting post... Please wait.'); // User feedback

				// Send delete request to the backend with the specific postId
				const response = await fetch(`/api/v1/blog/posts/${postId}`, {
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${idToken}`
					}
				});

				if (response.ok) {
					alert('Post deleted successfully!');
					// Optionally refresh the page or update the UI
					window.location.reload();
				} else {
					const result = await response.json();
					throw new Error(result.message || 'Failed to delete post');
				}
			} catch (error) {
				console.error('Error deleting post:', error);
				alert(`Failed to delete post: ${error.message}`);
			} finally {
				// Optional: Clear loading state
				// isOperationLoading = false;
			}
		}
	}
</script>

<!-- (Existing HTML structure up to Blog Posts Section) -->

<div class="blog-header container1 peaks w-full">
	<div class="flex w-full items-center justify-center pt-25">
		<div class="hero-start w-full text-center">
			<h1 class="font-orbital mx-auto text-6xl font-bold text-[#00dd87]">
				Fitness & Nutrition <span class="text-gradient-2">Blog</span>
			</h1>
			<p class="mx-auto mt-6 max-w-3xl text-xl text-white">
				Expert insights, tips, and stories to fuel your fitness journey and optimize your nutrition.
			</p>
		</div>
	</div>
</div>

<div class="container2 spacer layer1"></div>

<!-- Featured Post Section -->
{#if featuredPost}
	<div class="bg-gray-900 py-16">
		<div class="container mx-auto px-4">
			<div class="mb-8 text-center">
				<span class="font-orbital text-lg text-[#00dd87]">Featured Post</span>
				<h2 class="font-orbital mt-2 text-4xl font-bold text-white">
					{featuredPost.title}
				</h2>
			</div>

			<div class="fade-in-up mx-auto max-w-4xl overflow-hidden rounded-lg bg-gray-800 shadow-xl">
				{#if featuredPost.image}
					<div class="relative h-64 overflow-hidden bg-gray-700">
						<!-- Image placeholder or actual image -->
						<div class="absolute inset-0 bg-gradient-to-r from-[#00dd8733] to-transparent"></div>
						<div class="absolute bottom-0 left-0 p-6">
							<span class="rounded-full bg-[#00dd87] px-3 py-1 text-sm font-bold text-black">
								{featuredPost.category}
							</span>
							<p class="mt-2 text-white">
								{formatDate(featuredPost.publishedAt)} • {featuredPost.readTime} min read
							</p>
						</div>
					</div>
				{/if}

				<div class="p-6">
					<p class="mb-4 text-lg text-gray-300">
						{featuredPost.excerpt}
					</p>
					<div class="mt-6 flex items-center">
						<div class="h-10 w-10 rounded-full bg-gray-700">
							<!-- Author image placeholder -->
						</div>
						<div class="ml-3">
							<p class="font-bold text-white">{featuredPost.author.name}</p>
							<p class="text-sm text-gray-400">{featuredPost.author.title}</p>
						</div>
						<div class="ml-auto">
							<a
								href={`/Blog/${featuredPost.slug}`}
								class="rounded-full bg-[#00dd87] px-4 py-2 font-bold text-black transition-all hover:bg-[#00bb74]"
							>
								Read More
							</a>
						</div>
					</div>
				</div>
				<!-- Admin controls for Featured Post -->
				{#if $isAdmin}
					<div class="bg-gray-750 flex justify-end gap-2 border-t border-gray-700 p-4">
						<button
							on:click={() => handleEditPost(featuredPost.id)}
							class="rounded bg-blue-500 px-4 py-2 text-sm font-bold text-white hover:bg-blue-700"
						>
							Edit Featured
						</button>
						<button
							on:click={() => handleDeletePost(featuredPost.id, featuredPost.title)}
							class="rounded bg-red-500 px-4 py-2 text-sm font-bold text-white hover:bg-red-700"
						>
							Delete Featured
						</button>
					</div>
				{/if}
			</div>
		</div>
	</div>
{/if}

<!-- Blog Posts Section -->
<div class="bg-gray-900 py-16">
	<div class="container mx-auto px-4">
		<!-- Search and Filter Section -->
		<div class="mx-auto mb-12 max-w-4xl">
			<div class="flex flex-col items-center gap-4 md:flex-row">
				<!-- Search Box -->
				<div class="w-full md:w-2/3">
					<div class="relative">
						<input
							type="text"
							placeholder="Search articles..."
							class="w-full rounded-lg border-4 border-[#00A76E] bg-gray-800 p-3 pr-10 text-white focus:border-[#C62368] focus:ring focus:ring-[#C62368] focus:outline-none"
							on:input={handleSearchChange}
							value={searchQuery}
						/>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="absolute top-4 right-3 h-5 w-5 text-gray-400"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
							/>
						</svg>
					</div>
				</div>

				<!-- Category Filter -->
				<div class="w-full md:w-1/3">
					<select
						class="w-full rounded-lg border-4 border-[#00A76E] bg-gray-800 p-3 text-white focus:border-[#C62368] focus:ring focus:ring-[#C62368] focus:outline-none"
						on:change={(e) => handleCategoryChange(e.target.value)}
					>
						<option value="all">All Categories</option>
						{#each categories as category}
							<option value={category.slug}>{category.name}</option>
						{/each}
					</select>
				</div>
			</div>
			<!-- Admin: Add New Post Button -->
			{#if $isAdmin}
				<div class="mt-8 text-center md:text-right">
						<div class="admin-actions">
							<a href="/Blog/admin/post/new" class="add-post-button">
								<button class="mt-6 rounded-lg bg-green-500 px-6 py-3 font-bold text-white transition-all hover:bg-green-700 button primary-button">+ Create New Post</button>
							</a>
						</div>
				</div>
			{/if}
		</div>

		<!-- Loading State -->
		{#if isLoading}
			<div class="flex items-center justify-center py-20">
				<div
					class="h-16 w-16 animate-spin rounded-full border-4 border-[#00dd87] border-t-transparent"
				></div>
				<p class="ml-4 text-xl text-white">Loading articles...</p>
			</div>
			<!-- Error State -->
		{:else if error}
			<div class="mx-auto max-w-2xl rounded-lg bg-red-800 p-4 text-center text-white">
				<p>{error}</p>
				<button
					class="mt-4 rounded-lg bg-white px-4 py-2 text-red-800"
					on:click={() => window.location.reload()}
				>
					Try Again
				</button>
			</div>
			<!-- Blog Posts Grid -->
		{:else if currentPosts.length > 0}
			<div class="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
				{#each currentPosts as post (post.id)}
					<div
						class="fade-in-up transform overflow-hidden rounded-lg bg-gray-800 shadow-lg transition-transform hover:scale-105"
					>
						{#if post.image}
							<div class="h-48 bg-gray-700"><!-- Placeholder for image --></div>
						{/if}
						<div class="p-6">
							<div class="mb-3 flex items-center justify-between">
								<span
									class="rounded-full bg-[#00dd8733] px-3 py-1 text-sm font-bold text-[#00dd87]"
								>
									{post.category}
								</span>
								<span class="text-sm text-gray-400">
									{formatDate(post.publishedAt)}
								</span>
							</div>
							<h3 class="mb-2 text-xl font-bold text-white">
								{post.title}
							</h3>
							<p class="mb-4 line-clamp-3 text-gray-300">
								{post.excerpt}
							</p>
							<div class="mt-4 flex items-center justify-between">
								<!-- Link to full post -->
								<a href={`/Blog/${post.slug}`} class="text-[#00dd87] hover:underline">Read More</a>
							</div>
						</div>
						<!-- Admin controls for each post -->
						{#if $isAdmin}
							<div class="bg-gray-750 flex justify-end gap-2 border-t border-gray-700 p-4">
								<button
									on:click={() => handleEditPost(post.id)}
									class="rounded bg-blue-500 px-3 py-1 text-xs font-bold text-white hover:bg-blue-700"
								>
									Edit
								</button>
								<button
									on:click={() => handleDeletePost(post.id, post.title)}
									class="rounded bg-red-500 px-3 py-1 text-xs font-bold text-white hover:bg-red-700"
								>
									Delete
								</button>
							</div>
						{/if}
					</div>
				{/each}
			</div>
			<!-- Pagination (if any) would go here -->
			<!-- Pagination controls -->
			{#if totalPages > 1}
				<div class="mt-12 flex items-center justify-center space-x-2">
					<button
						on:click={() => changePage(currentPage - 1)}
						disabled={currentPage === 1}
						class="rounded bg-gray-700 px-4 py-2 text-white hover:bg-gray-600 disabled:opacity-50"
					>
						Previous
					</button>
					{#each Array(totalPages) as _, i}
						<button
							on:click={() => changePage(i + 1)}
							class={`rounded px-4 py-2 ${currentPage === i + 1 ? 'bg-[#00dd87] text-black' : 'bg-gray-700 text-white hover:bg-gray-600'}`}
						>
							{i + 1}
						</button>
					{/each}
					<button
						on:click={() => changePage(currentPage + 1)}
						disabled={currentPage === totalPages}
						class="rounded bg-gray-700 px-4 py-2 text-white hover:bg-gray-600 disabled:opacity-50"
					>
						Next
					</button>
				</div>
			{/if}
		{:else}
			<div class="py-20 text-center">
				<p class="text-2xl text-gray-400">No blog posts found matching your criteria.</p>
				{#if $isAdmin}
					<div class="admin-actions">
						<a href="/Blog/admin/post/new" class="add-post-button">
							<button class="mt-6 rounded-lg bg-green-500 px-6 py-3 font-bold text-white transition-all hover:bg-green-700 button primary-button">+ Create New Post</button>
						</a>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>
