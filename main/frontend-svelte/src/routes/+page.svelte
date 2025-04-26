<script lang="ts">
    import { onMount } from 'svelte';
    import { animate } from 'animejs';
    import InfoBlock from '$lib/components/InfoBlock.svelte';

    let heroStart = false;
    let heroSecond = false;
    let blocks = false;
    let demoVisible = false;
    let aboutVisible = false;
    let email = '';

    // Refs for sections
    let heroRef;
    let secondRef;
    let blocksRef;
    let demoRef;
    let aboutRef;

    // Info block titles
    const infoTitle1 = 'Exceptional Archive';
    const infoTitle2 = 'Personalized Nutrition';
    const infoTitle3 = 'Progress Tracker/ Forum Groups (BETA)';

    function handleEmailChange(e) {
        email = e.target.value;
    }

    function handleSubmit(e) {
        e.preventDefault();
        // Handle newsletter signup logic here
        console.log('Email submitted:', email);
        alert('Thank you for subscribing to our newsletter!');
        email = '';
    }

    onMount(() => {
        // Set up Intersection Observer
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.target === heroRef) {
                    heroStart = entry.isIntersecting;
                } else if (entry.target === secondRef) {
                    heroSecond = entry.isIntersecting;
                } else if (entry.target === demoRef) {
                    demoVisible = entry.isIntersecting;
                } else if (entry.target === aboutRef) {
                    aboutVisible = entry.isIntersecting;
                } else if (entry.target === blocksRef) {
                    blocks = entry.isIntersecting;
                }
            });
        });

        // Observe elements
        if (heroRef) observer.observe(heroRef);
        if (secondRef) observer.observe(secondRef);
        if (blocksRef) observer.observe(blocksRef);
        if (demoRef) observer.observe(demoRef);
        if (aboutRef) observer.observe(aboutRef);

        // Animation settings from React component
        const duration = 50000;
        const ease = 'linear';
        const direction = 'alternate';
        const opac = 0.5;

        // Set up anime.js animations
        animate('#pt1',{
            fill: [`rgba(173,83,137,${opac})`, `rgba(6,23,0,${opac})`, `rgba(204,43,94,${opac})`, `rgba(165,254,203,${opac})`, '#000'],
            easing: ease,
            duration: duration,
            direction: direction,
            delay: 1000,
            loop: true
        });

        // Add additional animations here...

        return () => {
            // Clean up observers on component unmount
            if (heroRef) observer.unobserve(heroRef);
            if (secondRef) observer.unobserve(secondRef);
            if (blocksRef) observer.unobserve(blocksRef);
            if (demoRef) observer.unobserve(demoRef);
            if (aboutRef) observer.unobserve(aboutRef);
        };
    });
</script>

<div class="container1 peaks w-full" bind:this={heroRef}>
    <div class="pt-25 flex justify-center items-center w-full">
        <div class={`w-full text-center ${heroStart ? 'hero-start' : ''}`}>
            <h1 id="heroText" class="text-6xl font-orbital font-bold mx-auto text-[#00dd87]">
                Unleashing Your Potential Through <span class="text-gradient-2">Fitness and Nutrition</span>
            </h1>
            <p class="text-xl text-white mt-6 max-w-3xl mx-auto">
                Your all-in-one platform for personalized nutrition plans, workout tracking, and a supportive fitness community (BETA).
            </p>
            <div class="mt-8 flex justify-center gap-4">
                <button class="bg-[#00dd87] hover:bg-[#00bb74] text-black font-bold py-3 px-6 rounded-full transition-all">
                    Get Started
                </button>
                <button class="border-2 border-[#00dd87] text-[#00dd87] hover:bg-[#00dd87] hover:text-black font-bold py-3 px-6 rounded-full transition-all">
                    <a href="#info">Learn More</a>
                </button>
            </div>
        </div>
    </div>
</div>

<div class="container2 spacer layer1"></div>

<div bind:this={secondRef} id="info" class="bg-no-repeat bg-center bg-cover py-3 layer3 container1">
    <section>
        <h1 class={`text-3xl md:text-4xl lg:text-5xl font-orbital font-bold text-[#00A76E] ${heroSecond ? 'hero-start' : ''}`}>
            Achieve Peak Fitness and Wellness with Our Comprehensive Site
        </h1>
        <p class={`text-xl text-[#faebd7] ${heroSecond ? 'hero-start-delay' : ''}`}>
            At our platform, we're passionate about building a vibrant community where individuals can thrive in their active lifestyles. Our goal is to provide a holistic approach to health and wellness by offering a diverse range of workout disciplines, personalized nutrition guidance, and a supportive environment for like-minded peers to connect and learn.
        </p>
    </section>
</div>

<div bind:this={blocksRef} class="container mx-auto text-center h-screen flex items-center py-3 relative">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 py-3">
        <div>
            <InfoBlock
                    fadeInAnimation={blocks ? 'info-hero' : ''}
                    title={infoTitle1}
                    expandable={false}
                    headingClass="text-4xl font-orbital font-bold"
                    text={["Our Exceptional Archive brings together a vast repository of food options. Here, you can explore a wide range of recipes tailored to meet your dietary preferences. Whether you're seeking tips on how to optimize your workout nutrition or interested in the latest sports betting insights, our archive provides the perfect blend of information to help you level up your fitness journey."]}
            />
        </div>
        <div>
            <InfoBlock
                    fadeInAnimation={blocks ? 'info-hero1' : ''}
                    title={infoTitle2}
                    headingClass="text-4xl font-orbital font-bold"
                    expandable={false}
                    text={["At the heart of our platform is a Personalized Nutrition system powered by a state-of-the-art recommender. This intelligent system analyzes your unique dietary preferences, activity levels, and fitness goals to recommend the most suitable recipes for your needs. We continuously update our meal plans and recipes based on the latest research, ensuring you get the right balance of nutrition to fuel your workouts and promote overall health."]}
            />
        </div>
        <div>
            <InfoBlock
                    fadeInAnimation={blocks ? 'info-hero' : ''}
                    title={infoTitle3}
                    headingClass="text-4xl font-orbital font-bold"
                    expandable={false}
                    text={["Our Progress Tracker is a powerful tool that lets you monitor your fitness journey with detailed insights into your workouts, nutrition, and milestones. Alongside the tracker, our Forum Groups provide a space for you to connect with others who share similar fitness goals, discuss strategies, and exchange tips. Whether you're aiming to lose weight, build muscle, or simply improve your overall fitness, these tools create a supportive environment for tracking your progress and engaging with a community of like-minded individuals."]}
            />
        </div>
    </div>
</div>

<!-- Demo Section -->
<div bind:this={demoRef} class="demo-section bg-gradient-to-r from-gray-900 to-gray-800 py-16">
    <div class="container mx-auto px-4">
        <h2 class={`text-4xl font-orbital font-bold text-center text-[#00dd87] mb-8 ${demoVisible ? 'fade-in-up' : ''}`}>
            See How It Works
        </h2>
        <div class={`bg-gray-800 rounded-lg shadow-xl overflow-hidden max-w-4xl mx-auto ${demoVisible ? 'fade-in-up delay-200' : ''}`}>
            <div class="bg-gray-900 p-3 flex items-center">
                <div class="flex space-x-2">
                    <div class="w-3 h-3 rounded-full bg-red-500"></div>
                    <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div class="w-3 h-3 rounded-full bg-green-500"></div>
                </div>
                <div class="mx-auto text-gray-400 text-sm">NutriFit Dashboard Demo</div>
            </div>
            <div class="h-96 bg-gray-700 flex items-center justify-center">
                <div class="text-center">
                    <div class="mx-auto w-16 h-16 border-4 border-[#00dd87] border-t-transparent rounded-full animate-spin mb-4"></div>
                    <p class="text-gray-300">Interactive Demo Loading...</p>
                    <p class="text-sm text-gray-400 mt-2">Explore our personalized meal planning, workout tracking, and community features</p>
                </div>
            </div>
            <div class="p-6 bg-gray-800">
                <div class="flex flex-wrap gap-4 justify-center">
                    <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">Dashboard</button>
                    <button class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded">Meal Planner</button>
                    <button class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">Workout Tracker</button>
                    <button class="bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded">Community</button>
                </div>
            </div>
        </div>
        <div class={`mt-10 text-center ${demoVisible ? 'fade-in-up delay-400' : ''}`}>
            <button class="bg-[#00dd87] hover:bg-[#00bb74] text-black font-bold py-3 px-8 rounded-full transition-all">
                Start Free Trial
            </button>
            <p class="text-gray-400 mt-2">No credit card required. Instacart account required</p>
        </div>
    </div>
</div>

<!-- About Us Section -->
<div bind:this={aboutRef} class="about-section bg-gray-900 py-16">
    <div class="container mx-auto px-4">
        <div class={`text-center mb-12 ${aboutVisible ? 'fade-in-up' : ''}`}>
            <h2 class="text-4xl font-orbital font-bold text-[#00dd87] mb-4">
                About Us
            </h2>
            <p class="text-xl text-gray-300 max-w-3xl mx-auto">
                We're a team of fitness professionals, nutritionists, and tech enthusiasts dedicated to revolutionizing how people approach health and wellness.
            </p>
        </div>

        <div class={`grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto mb-12 ${aboutVisible ? 'fade-in-up delay-200' : ''}`}>
            <div class="bg-gray-800 p-6 rounded-lg shadow-md">
                <div class="w-16 h-16 rounded-full bg-[#00dd8733] flex items-center justify-center mb-4 mx-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-[#00dd87]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-[#00dd87] mb-2 text-center">Our Mission</h3>
                <p class="text-gray-300 text-center">
                    To empower individuals with the tools, knowledge, and community support they need to achieve their fitness goals and lead healthier lives.
                </p>
            </div>

            <div class="bg-gray-800 p-6 rounded-lg shadow-md">
                <div class="w-16 h-16 rounded-full bg-[#00dd8733] flex items-center justify-center mb-4 mx-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-[#00dd87]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-[#00dd87] mb-2 text-center">Our Story</h3>
                <p class="text-gray-300 text-center">
                    Founded in 2023 by a group of fitness enthusiasts who saw a need for a more personalized, science-based approach to nutrition and exercise.
                </p>
            </div>

            <div class="bg-gray-800 p-6 rounded-lg shadow-md">
                <div class="w-16 h-16 rounded-full bg-[#00dd8733] flex items-center justify-center mb-4 mx-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-[#00dd87]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-[#00dd87] mb-2 text-center">Our Team</h3>
                <p class="text-gray-300 text-center">
                    A diverse group of certified nutritionists, fitness trainers, data scientists, and software developers working together to provide the best fitness platform.
                </p>
            </div>
        </div>

        <div class={`text-center ${aboutVisible ? 'fade-in-up delay-400' : ''}`}>
            <a href="/about-us">
                <button class="bg-transparent border-2 border-[#00dd87] hover:bg-[#00dd87] text-[#00dd87] hover:text-black font-bold py-3 px-8 rounded-full transition-all">
                    Learn More About Us
                </button>
            </a>
        </div>
    </div>
</div>

<!--&lt;!&ndash; Newsletter Section &ndash;&gt;-->
<!--<div class="newsletter-section bg-gray-800 py-16">-->
<!--    <div class="container mx-auto px-4 max-w-3xl">-->
<!--        <div class="bg-gradient-to-br from-[#001a12] to-[#003a2a] p-8 rounded-2xl shadow-lg">-->
<!--            <h2 class="text-3xl font-orbital font-bold text-[#00dd87] mb-4 text-center">-->
<!--                Stay Updated with Latest Fitness & Nutrition Tips-->
<!--            </h2>-->
<!--            <p class="text-gray-300 text-center mb-6">-->
<!--                Subscribe to our newsletter and get weekly updates on workouts, recipes, and fitness trends.-->
<!--            </p>-->
<!--            <form on:submit|preventDefault={handleSubmit} class="flex flex-col md:flex-row gap-4">-->
<!--                <input-->
<!--                        type="email"-->
<!--                        bind:value={email}-->