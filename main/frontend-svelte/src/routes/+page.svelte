<script lang="ts">
    import { onMount } from 'svelte';
    import { animate } from 'animejs';
    import InfoBlock from '$lib/components/recipes/InfoBlock.svelte';

    let heroStart = false;
    let heroSecond = false;
    let blocks = false;
    let demoVisible = false;
    let aboutVisible = false;
    let email = '';

    // Flags to track if animations have been played already
    let heroAnimationPlayed = false;
    let heroSecondAnimationPlayed = false;
    let blocksAnimationPlayed = false;
    let demoAnimationPlayed = false;
    let aboutAnimationPlayed = false;

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
                if (entry.target === heroRef && !heroAnimationPlayed && entry.isIntersecting) {
                    heroStart = true;
                    heroAnimationPlayed = true;
                } else if (entry.target === secondRef && !heroSecondAnimationPlayed && entry.isIntersecting) {
                    heroSecond = true;
                    heroSecondAnimationPlayed = true;
                } else if (entry.target === blocksRef && !blocksAnimationPlayed && entry.isIntersecting) {
                    blocks = true;
                    blocksAnimationPlayed = true;
                    // Once animation is triggered, we can stop observing this section
                    observer.unobserve(blocksRef);
                } else if (entry.target === demoRef && !demoAnimationPlayed && entry.isIntersecting) {
                    demoVisible = true;
                    demoAnimationPlayed = true;
                } else if (entry.target === aboutRef && !aboutAnimationPlayed && entry.isIntersecting) {
                    aboutVisible = true;
                    aboutAnimationPlayed = true;
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
<!--<a href="https://www.producthunt.com/products/gainz-tracker/reviews?utm_source=badge-product_review&utm_medium=badge&utm_souce=badge-gainz&#0045;tracker" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/product_review.svg?product_id=1061496&theme=light" alt="Gainz&#0032;Tracker - Your&#0032;own&#0032;&#0040;FREE&#0041;&#0032;Personal&#0032;Shopper&#0032;and&#0032;Delivery | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>-->
<div class="container1 peaks w-full" bind:this={heroRef}>
    <div class="pt-25 flex justify-center items-center w-full">
        <div class={`w-full text-center ${heroStart ? 'hero-start' : ''}`}>
            <h1 id="heroText" class="text-6xl font-orbital font-bold mx-auto text-[#00dd87]">
                Unleashing Your Potential Through <span class="text-gradient-2">Fitness and Nutrition</span>
            </h1>
            <p class="text-xl text-white mt-6 max-w-3xl mx-auto ">
                Your all-in-one platform for personalized nutrition plans, workout tracking, and a supportive fitness community -- Mobile app in Development
            </p>
            <p class='text-gradient-2 mt-2'>Get Started today!! IT'S FREE</p>
            <div class="mt-8 flex justify-center gap-4">
                <button class="bg-[#00dd87] hover:bg-[#00bb74] text-black font-bold py-3 px-6 rounded-full transition-all">
                    <a href="/Nutrition">Get Started</a>
                </button>
                <button class="border-2 border-[#00dd87] text-[#00dd87] hover:bg-[#00dd87] hover:text-black font-bold py-3 px-6 rounded-full transition-all flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 0.297c-6.627 0-12 5.373-12 12 0 5.302 3.438 9.8 8.205 11.385 0.6 0.113 0.82-0.258 0.82-0.577 0-0.285-0.01-1.04-0.015-2.04-3.338 0.724-4.042-1.61-4.042-1.61-0.546-1.387-1.333-1.757-1.333-1.757-1.089-0.745 0.083-0.729 0.083-0.729 1.205 0.084 1.84 1.236 1.84 1.236 1.07 1.835 2.807 1.305 3.492 0.998 0.108-0.775 0.418-1.305 0.762-1.605-2.665-0.305-5.466-1.332-5.466-5.931 0-1.31 0.469-2.381 1.236-3.221-0.124-0.303-0.536-1.523 0.117-3.176 0 0 1.008-0.322 3.301 1.23 0.957-0.266 1.983-0.399 3.003-0.404 1.02 0.005 2.047 0.138 3.006 0.404 2.289-1.552 3.295-1.23 3.295-1.23 0.655 1.653 0.243 2.873 0.119 3.176 0.77 0.84 1.233 1.911 1.233 3.221 0 4.61-2.807 5.624-5.479 5.921 0.43 0.372 0.823 1.102 0.823 2.222 0 1.606-0.014 2.898-0.014 3.293 0 0.319 0.216 0.694 0.825 0.576 4.765-1.587 8.199-6.084 8.199-11.384 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    <a href="https://github.com/agene0001/workout-app" target="_blank">Open Source</a>
                </button>
                <button class="bg-[#da552f] hover:bg-[#c7461e] text-white font-bold py-3 px-6 rounded-full transition-all flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 40 40">
                        <path d="M23.402 18.737h-4.63v-4.63h4.63v4.63zm4.63-4.63h4.63v4.63h-4.63v-4.63zm0 9.26v4.63h-4.63v-4.63h4.63zm-4.63 0h-4.63v-4.63h4.63v4.63zm-4.63 0v4.63h-4.63v-4.63h4.63zm-4.63-4.63h-4.63v-4.63h4.63v4.63zM40 8.39v23.22c0 4.61-3.73 8.35-8.35 8.35H8.35c-4.61 0-8.35-3.73-8.35-8.35V8.39C0 3.77 3.73 0 8.35 0h23.22c4.61 0 8.35 3.73 8.35 8.39z"></path>
                    </svg>
                    <a href="https://www.producthunt.com/products/gainz-tracker?utm_source=badge-product_review&utm_medium=badge&utm_souce=badge-gainz&#0045;tracker" target="_blank">Product Hunt</a>
                </button>
            </div>
        </div>
    </div>
</div>

<div class="container2 spacer layer1"></div>

<div bind:this={secondRef} id="info" class="bg-no-repeat bg-center bg-cover py-3 layer2 container1">
    <section>
        <h1 class={`text-3xl md:text-4xl lg:text-5xl font-orbital font-bold text-[#00A76E] ${heroSecond ? 'hero-start' : ''}`}>
            Achieve Peak Fitness and Wellness with Our Comprehensive Site
        </h1>
        <p class={`text-xl text-[#faebd7] ${heroSecond ? 'hero-start-delay' : ''}`}>
            Our goal is to provide a holistic approach to health and wellness by offering an easier and cheaper alternative to HelloFresh. Through our strategic partnership with Instacart's API, we've revolutionized the grocery shopping experience for our users. This integration allows members to seamlessly purchase their recipe ingredients directly through our platform, bypassing long grocery store lines while avoiding typical delivery upcharges. We've optimized the purchasing process to find the best deals across participating stores, ensuring our users get the most value for their money.
            <br><br>
            We're excited to announce our ongoing development of integrations with Walmart and Sam's Club, which will further expand our users' shopping options and potential savings. These partnerships will bring even more competitive pricing and product variety to our platform in the near future.
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
                    text={["At the heart of our platform is a Personalized Nutrition system powered by a state-of-the-art recommender. This intelligent system analyzes your unique dietary preferences, activity levels, and fitness goals to recommend the most suitable recipes for your needs. We continuously update our meal plans and recipes based on the latest research, ensuring you get the right balance of nutrition to fuel your workouts and promote overall health"]}
            />
        </div>
        <div>
            <InfoBlock
                    fadeInAnimation={blocks ? 'info-hero' : ''}
                    title={infoTitle3}
                    headingClass="text-4xl font-orbital font-bold"
                    expandable={false}
                    text={["Looking ahead, we're building towards a comprehensive ecosystem that goes beyond just meal planning and grocery delivery. Our roadmap includes the development of an interactive recipe creation platform where users can craft, share, and customize their favorite dishes. This will be complemented by dedicated forum groups where members can track their wellness journeys together, share success stories, exchange recipe modifications, and build lasting connections with others who share their health and fitness goals. This community-driven approach will create a supportive environment where users can find inspiration, accountability, and friendship on their path to better health."]}
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

            <div class="bg-gray-700 py-4">
                <!-- Adjusted Supademo wrapper: removed padding and max-height -->
                <div style="position: relative; box-sizing: content-box; width: 100%; aspect-ratio: 2.013845185651353;">
                    <iframe
                            src="https://app.supademo.com/embed/cma7fh2255hdb13m0l28tzmyw?embed_v=2"
                            loading="lazy"
                            title="Gainztracker Demo"
                            allow="clipboard-write"
                            frameborder="0"
                            webkitallowfullscreen="true"
                            mozallowfullscreen="true"
                            allowfullscreen
                            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                    ></iframe>
                </div>
                <!-- Paragraph moved outside the Supademo wrapper, added text-center -->
                <p class="text-sm text-gray-400 mt-4 text-center">
                    Explore our personalized meal planning, workout tracking, and community features
                </p>
            </div>

<!--            <div class="p-6 bg-gray-800">-->
<!--                <div class="flex flex-wrap gap-4 justify-center">-->
<!--                    <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">Dashboard</button>-->
<!--                    <button class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded">Meal Planner</button>-->
<!--                    <button class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">Workout Tracker</button>-->
<!--                    <button class="bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded">Community</button>-->
<!--                </div>-->
<!--            </div>-->
        </div>
        <div class={`mt-10 text-center ${demoVisible ? 'fade-in-up delay-400' : ''}`}>
            <button class="bg-[#00dd87] hover:bg-[#00bb74] text-black font-bold py-3 px-8 rounded-full transition-all">
                <a href="/Nutrition">Start Today</a>
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
                    Founded in 2021 by a group of fitness enthusiasts who saw a need for a more personalized, science-based approach to nutrition and exercise.
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