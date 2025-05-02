<script>
    import { onMount } from 'svelte';
    import InfoBlock from '$lib/components/InfoBlock.svelte';
    import axios from 'axios';

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
        return posts.filter(post => {
            const matchesCategory = category === 'all' || post.category === category;
            const matchesQuery = query === '' ||
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
        try {
            isLoading = true;

            // Fetch blog posts
            const postsRes = await axios.get('/api/v1/blog/posts');
            blogPosts = postsRes.data;

            // Set featured post (most recent)
            if (blogPosts.length > 0) {
                featuredPost = blogPosts.find(post => post.featured) || blogPosts[0];
                // Remove featured post from main list to avoid duplication
                blogPosts = blogPosts.filter(post => post.id !== featuredPost.id);
            }

            // Fetch categories
            const categoriesRes = await axios.get('/api/v1/blog/categories');
            categories = categoriesRes.data;

            isLoading = false;
        } catch (err) {
            console.error("Error fetching blog data:", err);
            error = "Failed to load blog content. Please try again later.";
            isLoading = false;
        }
    });
</script>

<div class="blog-header container1 peaks w-full">
    <div class="pt-25 flex justify-center items-center w-full">
        <div class="w-full text-center hero-start">
            <h1 class="text-6xl font-orbital font-bold mx-auto text-[#00dd87]">
                Fitness & Nutrition <span class="text-gradient-2">Blog</span>
            </h1>
            <p class="text-xl text-white mt-6 max-w-3xl mx-auto">
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
            <div class="text-center mb-8">
                <span class="text-[#00dd87] font-orbital text-lg">Featured Post</span>
                <h2 class="text-4xl font-orbital font-bold text-white mt-2">
                    {featuredPost.title}
                </h2>
            </div>

            <div class="bg-gray-800 rounded-lg overflow-hidden shadow-xl max-w-4xl mx-auto fade-in-up">
                {#if featuredPost.image}
                    <div class="h-64 bg-gray-700 relative overflow-hidden">
                        <div class="absolute inset-0 bg-gradient-to-r from-[#00dd8733] to-transparent"></div>
                        <div class="absolute bottom-0 left-0 p-6">
                            <span class="bg-[#00dd87] text-black px-3 py-1 rounded-full text-sm font-bold">
                                {featuredPost.category}
                            </span>
                            <p class="text-white mt-2">
                                {formatDate(featuredPost.publishedAt)} • {featuredPost.readTime} min read
                            </p>
                        </div>
                    </div>
                {/if}

                <div class="p-6">
                    <p class="text-gray-300 text-lg mb-4">
                        {featuredPost.excerpt}
                    </p>
                    <div class="flex items-center mt-6">
                        <div class="w-10 h-10 rounded-full bg-gray-700"></div>
                        <div class="ml-3">
                            <p class="text-white font-bold">{featuredPost.author.name}</p>
                            <p class="text-gray-400 text-sm">{featuredPost.author.title}</p>
                        </div>
                        <div class="ml-auto">
                            <a href={`/blog/${featuredPost.slug}`} class="bg-[#00dd87] hover:bg-[#00bb74] text-black font-bold py-2 px-4 rounded-full transition-all">
                                Read More
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}

<!-- Blog Posts Section -->
<div class="bg-gray-900 py-16">
    <div class="container mx-auto px-4">
        <!-- Search and Filter Section -->
        <div class="max-w-4xl mx-auto mb-12">
            <div class="flex flex-col md:flex-row gap-4">
                <!-- Search Box -->
                <div class="w-full md:w-2/3">
                    <div class="relative">
                        <input
                                type="text"
                                placeholder="Search articles..."
                                class="w-full p-3 pr-10 border-4 border-[#00A76E] bg-gray-800 text-white rounded-lg focus:outline-none focus:ring focus:ring-[#C62368] focus:border-[#C62368]"
                                on:input={handleSearchChange}
                                value={searchQuery}
                        />
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute right-3 top-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>
                </div>

                <!-- Category Filter -->
                <div class="w-full md:w-1/3">
                    <select
                            class="w-full p-3 border-4 border-[#00A76E] bg-gray-800 text-white rounded-lg focus:outline-none focus:ring focus:ring-[#C62368] focus:border-[#C62368]"
                            on:change={(e) => handleCategoryChange(e.target.value)}
                    >
                        <option value="all">All Categories</option>
                        {#each categories as category}
                            <option value={category.slug}>{category.name}</option>
                        {/each}
                    </select>
                </div>
            </div>
        </div>

        <!-- Loading State -->
        {#if isLoading}
            <div class="flex justify-center items-center py-20">
                <div class="w-16 h-16 border-4 border-[#00dd87] border-t-transparent rounded-full animate-spin"></div>
                <p class="ml-4 text-white text-xl">Loading articles...</p>
            </div>
            <!-- Error State -->
        {:else if error}
            <div class="bg-red-800 text-white p-4 rounded-lg max-w-2xl mx-auto text-center">
                <p>{error}</p>
                <button class="mt-4 bg-white text-red-800 px-4 py-2 rounded-lg" on:click={() => window.location.reload()}>
                    Try Again
                </button>
            </div>
            <!-- Blog Posts Grid -->
        {:else if currentPosts.length > 0}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {#each currentPosts as post}
                    <div class="bg-gray-800 rounded-lg overflow-hidden shadow-lg transform transition-transform hover:scale-105 fade-in-up">
                        {#if post.image}
                            <div class="h-48 bg-gray-700"></div>
                        {/if}
                        <div class="p-6">
                            <div class="flex justify-between items-center mb-3">
                                <span class="bg-[#00dd8733] text-[#00dd87] px-3 py-1 rounded-full text-sm font-bold">
                                    {post.category}
                                </span>
                                <span class="text-gray-400 text-sm">
                                    {formatDate(post.publishedAt)}
                                </span>
                            </div>
                            <h3 class="text-xl font-bold text-white mb-2">
                                {post.title}
                            </h3>
                            <p class="text-gray-300 mb-4 line-clamp-3">
                                {post.excerpt}
                            </p>
                            <div class="flex items-center justify-between mt-4">
                                <div class="flex items-center">
                                    <div class="w-8 h-8 rounded-full bg-gray-700"></div>
                                    <p class="text-gray-400 text-sm ml-2">{post.author.name}</p>
                                </div>
                                <span class="text-gray-400 text-sm">{post.readTime} min read</span>
                            </div>
                            <a href={`/blog/${post.slug}`} class="block mt-4 text-[#00dd87] hover:text-[#00bb74] font-bold text-center">
                                Read Article →
                            </a>
                        </div>
                    </div>
                {/each}
            </div>

            <!-- Pagination -->
            {#if totalPages > 1}
                <div class="flex justify-center mt-12">
                    <div class="flex space-x-2">
                        <button
                                class="px-4 py-2 rounded-lg bg-gray-800 text-white disabled:opacity-50"
                                on:click={() => changePage(currentPage - 1)}
                                disabled={currentPage === 1}
                        >
                            Previous
                        </button>

                        {#each Array(totalPages) as _, i}
                            <button
                                    class={`px-4 py-2 rounded-lg ${currentPage === i + 1 ? 'bg-[#00dd87] text-black' : 'bg-gray-800 text-white'}`}
                                    on:click={() => changePage(i + 1)}
                            >
                                {i + 1}
                            </button>
                        {/each}

                        <button
                                class="px-4 py-2 rounded-lg bg-gray-800 text-white disabled:opacity-50"
                                on:click={() => changePage(currentPage + 1)}
                                disabled={currentPage === totalPages}
                        >
                            Next
                        </button>
                    </div>
                </div>
            {/if}
        {:else}
            <div class="text-center py-20">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 class="text-white text-xl font-bold mb-2">No posts found</h3>
                <p class="text-gray-400">
                    No articles match your current search criteria.
                </p>
                <button
                        class="mt-4 bg-[#00dd87] hover:bg-[#00bb74] text-black font-bold py-2 px-6 rounded-full"
                        on:click={() => {
                        searchQuery = '';
                        selectedCategory = 'all';
                    }}
                >
                    Clear Filters
                </button>
            </div>
        {/if}
    </div>
</div>

<!-- Newsletter Subscription Section -->

