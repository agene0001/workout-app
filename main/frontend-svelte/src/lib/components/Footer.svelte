<script lang="ts">
    import { onMount } from 'svelte';

    // Social media links
    const socialLinks = [
        { name: 'Facebook', icon: 'facebook', url: 'https://www.facebook.com/profile.php?id=61575513905339' },
        { name: 'Twitter/X', icon: 'twitter', url: 'https://x.com/GainzTracker' },
        { name: 'Instagram', icon: 'instagram', url: 'https://www.instagram.com/gainztrackers/' },
        { name: 'LinkedIn', icon: 'linkedin', url: 'https://www.linkedin.com/company/106717227' },
        { name: 'Medium', icon: 'medium', url: 'https://medium.com/@gainztrackers' }
        // { name: 'YouTube', icon: 'youtube', url: '#' }
    ];

    // Footer links
    const footerLinks = [
        {
            title: 'Company',
            links: [
                { name: 'About Us', url: '/About-Us' },
                { name: 'Contact', url: '/Contact' }
            ]
        },
        {
            title: 'Resources',
            links: [
                { name: 'Blog', url: '/Blog' },
                { name: 'Nutrition Guide', url: '/Nutrition' },
                { name: 'Workout Library', url: '/Groups' },
                { name: 'FAQ', url: '/faq' }
            ]
        },
        {
            title: 'Legal',
            links: [
                { name: 'Terms of Service', url: '/terms' },
                { name: 'Privacy Policy', url: '/privacy' },
                { name: 'Cookie Policy', url: '/cookies' },
                { name: 'GDPR', url: '/gdpr' }
            ]
        }
    ];

    let email = '';
    let footerVisible = false;
    let footerRef;

    function handleEmailChange(e) {
        email = e.target.value;
    }

    function handleSubmit(e) {
        e.preventDefault();
        console.log('Footer email submitted:', email);
        alert('Thank you for subscribing to our newsletter!');
        email = '';
    }

    onMount(() => {
        // Set up Intersection Observer for footer animation
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.target === footerRef) {
                    footerVisible = entry.isIntersecting;
                }
            });
        }, { threshold: 0.1 });

        // Observe footer element
        if (footerRef) observer.observe(footerRef);

        return () => {
            // Clean up observer on component unmount
            if (footerRef) observer.unobserve(footerRef);
        };
    });
</script>

<footer bind:this={footerRef} class="bg-gray-900 pt-16 pb-8 ">
    <div class="container mx-auto px-4">
        <!-- Newsletter Section -->
        <div class={`mb-12 max-w-3xl mx-auto ${footerVisible ? 'fade-in-up' : ''}`}>
            <div class="bg-gradient-to-br from-[#001a12] to-[#003a2a] p-8 rounded-2xl shadow-lg">
                <h2 class="text-2xl font-orbital font-bold text-[#00dd87] mb-4 text-center">
                    Stay Updated with Latest Fitness & Nutrition Tips
                </h2>
                <p class="text-gray-300 text-center mb-6">
                    Subscribe to our newsletter and get weekly updates on workouts, recipes, and fitness trends.
                </p>
                <form on:submit|preventDefault={handleSubmit} class="flex flex-col md:flex-row gap-4">
                    <input
                            type="email"
                            bind:value={email}
                            on:input={handleEmailChange}
                            placeholder="Enter your email address"
                            required
                            class="flex-grow px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-[#00dd87] focus:border-transparent"
                    />
                    <button
                            type="submit"
                            class="bg-[#00dd87] hover:bg-[#00bb74] text-black font-bold py-3 px-6 rounded-full transition-all"
                    >
                        Subscribe
                    </button>
                </form>
            </div>
        </div>

        <!-- Footer Links -->
        <div class={`grid grid-cols-1 md:grid-cols-4 gap-8 mb-12 ${footerVisible ? 'fade-in-up delay-200' : ''}`}>
            <!-- Brand Column -->
            <div>
                <div class="mb-4">
                    <h3 class="text-2xl font-orbital font-bold text-[#00dd87]">Gainz Tracker</h3>
                    <p class="text-gray-400 mt-2">Unleashing Your Potential Through Fitness and Nutrition</p>
                </div>
                <div class="flex space-x-4 mt-6">
                    {#each socialLinks as social}
                        <a href={social.url} class="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-[#00dd87] hover:text-black transition-all text-gray-400">
                            {#if social.icon === 'facebook'}
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M13.397 20.997v-8.196h2.765l.411-3.209h-3.176V7.548c0-.926.258-1.56 1.587-1.56h1.684V3.127A22.336 22.336 0 0014.201 3c-2.444 0-4.122 1.492-4.122 4.231v2.355H7.332v3.209h2.753v8.202h3.312z"></path>
                                </svg>
                            {:else if social.icon === 'twitter'}
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"></path>
                                </svg>
                            {:else if social.icon === 'instagram'}
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"></path>
                                </svg>
                            {:else if social.icon === 'youtube'}
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"></path>
                                </svg>
                        {:else if social.icon === 'linkedin'}
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path>
                        </svg>
                    {:else if social.icon === 'medium'}
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z"></path>
                        </svg>
                        {/if}
                        </a>
                    {/each}
                </div>
            </div>

            <!-- Link Columns -->
            {#each footerLinks as section}
                <div>
                    <h4 class="text-lg font-bold text-white mb-4">{section.title}</h4>
                    <ul class="space-y-2">
                        {#each section.links as link}
                            <li>
                                <a href={link.url} class="text-gray-400 hover:text-[#00dd87] transition-colors">
                                    {link.name}
                                </a>
                            </li>
                        {/each}
                    </ul>
                </div>
            {/each}
        </div>

        <!-- Bottom Bar -->
        <div class={`pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center ${footerVisible ? 'fade-in-up delay-400' : ''}`}>
            <p class="text-gray-500 text-sm mb-4 md:mb-0">
                © {new Date().getFullYear()} GainzTracker. All rights reserved.
            </p>
            <div class="flex space-x-6">
                <a href="/terms" class="text-gray-500 hover:text-[#00dd87] text-sm">Terms</a>
                <a href="/privacy" class="text-gray-500 hover:text-[#00dd87] text-sm">Privacy</a>
                <a href="/cookies" class="text-gray-500 hover:text-[#00dd87] text-sm">Cookies</a>
            </div>
        </div>
    </div>
</footer>

<style>
    /* Animation classes */
    .fade-in-up {
        animation: fadeInUp 0.8s ease forwards;
    }

    .delay-200 {
        animation-delay: 200ms;
    }

    .delay-400 {
        animation-delay: 400ms;
    }

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

    /* Font styles - assuming 'font-orbital' is defined elsewhere */
    :global(.font-orbital) {
        font-family: 'Orbital', system-ui, sans-serif;
    }
</style>