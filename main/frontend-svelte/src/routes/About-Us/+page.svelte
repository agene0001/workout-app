<script>
  import { onMount } from 'svelte';
  import {animate} from 'animejs';

  // Component props
  let missionRef;
  let journeyRef;
  let valuesRef;
  let contactRef;

  // Visibility states
  let missionVisible = false;
  let journeyVisible = false;
  let valuesVisible = false;
  let contactVisible = false;

  // Timeline milestones data
  const milestones = [
    {
      year: "2020",
      title: "Our Founding",
      description: "Started with a simple vision to make personalized nutrition accessible to everyone.",
      isRight: false
    },
    {
      year: "2021",
      title: "Launch of Recipe Archive",
      description: "Introduced our comprehensive repository of nutritious recipes tailored to different dietary preferences.",
      isRight: true
    },
    {
      year: "2022",
      title: "AI Nutrition Recommender",
      description: "Developed our state-of-the-art AI system to provide personalized meal recommendations based on individual needs.",
      isRight: false
    },
    {
      year: "2023",
      title: "Community Forums",
      description: "Established forum groups to connect like-minded individuals on their fitness and nutrition journeys.",
      isRight: true
    },
    {
      year: "2024",
      title: "Progress Tracker Launch",
      description: "Introduced our comprehensive progress tracking system to help users monitor their fitness journey.",
      isRight: false
    }
  ];

  // Values data with SVG icons
  const values = [
    {
      icon: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="rgba(204, 43, 94, 1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
            </svg>`,
      title: "Evidence-Based Approach",
      description: "We believe in science-backed nutrition and fitness recommendations, constantly updating our content based on the latest research."
    },
    {
      icon: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="rgba(204, 43, 94, 1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>`,
      title: "Community Support",
      description: "We foster a positive, inclusive environment where members can share experiences, challenges, and successes."
    },
    {
      icon: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="rgba(204, 43, 94, 1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"></path>
              <line x1="16" y1="8" x2="2" y2="22"></line>
              <line x1="17.5" y1="15" x2="9" y2="15"></line>
            </svg>`,
      title: "Personalization",
      description: "We understand that every individual has unique needs and goals, which is why our platform tailors recommendations to your specific requirements."
    }
  ];

  onMount(() => {
    // Add styles to document head
    const style = document.createElement('style');
    style.innerHTML = `
      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
      }

      .fade-in-1 {
        animation: fadeIn 0.8s ease forwards;
        animation-delay: 0.2s;
        opacity: 0;
      }

      .fade-in-2 {
        animation: fadeIn 0.8s ease forwards;
        animation-delay: 0.4s;
        opacity: 0;
      }

      .fade-in-3 {
        animation: fadeIn 0.8s ease forwards;
        animation-delay: 0.6s;
        opacity: 0;
      }
    `;
    document.head.appendChild(style);

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.target === missionRef) {
          missionVisible = entry.isIntersecting;
        } else if (entry.target === journeyRef) {
          journeyVisible = entry.isIntersecting;
        } else if (entry.target === valuesRef) {
          valuesVisible = entry.isIntersecting;
        } else if (entry.target === contactRef) {
          contactVisible = entry.isIntersecting;
        }
      });
    }, { threshold: 0.1 });

    animate('.hero-circle-1',{
      translateX: ['10%', '-10%'],
      translateY: ['5%', '-15%'],
      scale: [1, 1.2],
      opacity: [0.4, 0.5],
      easing: 'easeInOutSine',
      duration: 10000,
      direction: 'alternate',
      loop: true
    });

    animate('.hero-circle-2',{
      translateX: ['-5%', '15%'],
      translateY: ['-10%', '5%'],
      scale: [1.1, 0.9],
      opacity: [0.5, 0.3],
      easing: 'easeInOutQuad',
      duration: 13000,
      direction: 'alternate',
      loop: true
    });

    // Observe refs
    if (missionRef) observer.observe(missionRef);
    if (journeyRef) observer.observe(journeyRef);
    if (valuesRef) observer.observe(valuesRef);
    if (contactRef) observer.observe(contactRef);

    return () => {
      // Clean up
      if (missionRef) observer.unobserve(missionRef);
      if (journeyRef) observer.unobserve(journeyRef);
      if (valuesRef) observer.unobserve(valuesRef);
      if (contactRef) observer.unobserve(contactRef);
      document.head.removeChild(style);
    };
  });
</script>

<!-- Hero Section with enhanced background -->
<div class="relative min-h-[500px] flex items-center justify-center overflow-hidden">
  <!-- Animated gradient background -->
  <div class="absolute inset-0 bg-[#002233] z-0"></div>

  <!-- Animated wave pattern overlay -->
  <div class="absolute inset-0 z-0 opacity-20">
    <svg width="100%" height="100%" viewBox="0 0 1440 320" preserveAspectRatio="none">
      <path
              fill="rgba(0, 255, 255, 0.4)"
              fill-opacity="1"
              d="M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
              class="animate-pulse"
              style="animation-duration: 10s"
      ></path>
    </svg>
  </div>

  <!-- Second wave pattern with different animation -->
  <div class="absolute inset-0 z-0 opacity-20">
    <svg width="100%" height="100%" viewBox="0 0 1440 320" preserveAspectRatio="none">
      <path
              fill="rgba(204, 43, 94, 0.4)"
              fill-opacity="1"
              d="M0,64L48,80C96,96,192,128,288,154.7C384,181,480,203,576,186.7C672,171,768,117,864,122.7C960,128,1056,192,1152,208C1248,224,1344,192,1392,176L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
              class="animate-pulse"
              style="animation-duration: 15s"
      ></path>
    </svg>
  </div>

  <!-- Animated gradient circles -->
  <div class="hero-circle-1 absolute w-[300px] h-[300px] rounded-full bg-[rgba(204,43,94,0.3)] filter blur-[40px] top-[20%] left-[10%] z-0"></div>
  <div class="hero-circle-2 absolute w-[400px] h-[400px] rounded-full bg-[rgba(0,255,255,0.3)] filter blur-[60px] bottom-[10%] right-[5%] z-0"></div>

  <!-- Low poly grid background -->
  <div class="absolute inset-0 low-poly2 bg-center bg-cover bg-no-repeat opacity-20 z-0"></div>

  <!-- Content -->
  <div class="container mx-auto text-center relative py-4 z-10">
    <h1 class="text-6xl text-gradient-1 mb-4 font-orbital-style-normal hero-start">
      About Our Mission
    </h1>
    <p class="text-xl text-primary mb-5 max-w-[800px] mx-auto shadow-[1px_1px_3px_rgba(0,0,0,0.2)] hero-start-delay">
      We're passionate about empowering individuals to achieve their wellness goals through personalized nutrition and fitness solutions.
    </p>
    <a href="#mission" class="px-8 py-3 border-2 border-[var(--primary)] text-[var(--primary)] rounded-[2px] inline-block hover:bg-[rgba(0,255,255,0.1)] transition-colors duration-300">
      Learn More
    </a>
  </div>
</div>

<!-- Mission Section -->
<div
        id="mission"
        bind:this={missionRef}
        class="bg-[rgba(0,255,255,0.2)] py-5"
>
  <div
          class="container mx-auto px-4 transition-all duration-800"
          style="opacity: {missionVisible ? 1 : 0}; transform: {missionVisible ? 'translateY(0)' : 'translateY(30px)'};"
  >
    <div class="flex flex-col md:flex-row md:items-center">
      <div class="w-full md:w-1/2 mb-4 md:mb-0">
        <div class="border-l-[6px] border-[rgba(204,43,94,0.8)] pl-8">
          <h2 class="text-5xl text-danger font-orbital-style-normal mb-4">Our Mission</h2>
          <p class="text-lg text-primary mb-4">To empower individuals on their journey to optimal health through science-backed nutrition guidance and a supportive community environment.</p>
        </div>
        <p class="mb-4 mx-2 text-primary">At our core, we believe that everyone deserves access to personalized nutrition information that fits their unique lifestyle, preferences, and goals. Our platform combines cutting-edge technology with expert knowledge to deliver custom-tailored nutrition plans and workout recommendations.</p>
        <p class="mx-2 text-primary">We're more than just a recipe database – we're a comprehensive wellness ecosystem designed to support you at every step of your journey toward better health.</p>
      </div>
      <div class="w-full md:w-1/2">
        <div class="border-[1rem] border-[rgba(0,255,255,0.5)] shadow-[3px_3px_3px_rgba(0,255,125,.5)] rounded-[2px] overflow-hidden h-[400px]">
          <img
                  src="/imgs/aboutus.png"
                  alt="Our Mission"
                  class="w-full h-full"
          />
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Journey Timeline Section -->
<div
        id="journey"
        bind:this={journeyRef}
        class="bg-light py-5"
>
  <div
          class="container mx-auto px-4 transition-all duration-800"
          style="opacity: {journeyVisible ? 1 : 0}; transform: {journeyVisible ? 'translateY(0)' : 'translateY(30px)'};"
  >
    <h2 class="text-5xl text-primary font-bold font-orbital text-center mb-5">Our Journey</h2>
    <div class="journey-timeline">
      {#each milestones as milestone, index}
        <div class="milestone {milestone.isRight ? 'flex justify-end' : 'flex justify-start'} {journeyVisible ? `fade-in-${(index % 3) + 1}` : ''} mb-8 w-full">
          <div class="w-4/5 p-6 {milestone.isRight ? 'bg-[rgba(0,255,255,0.1)] border-[0.5rem] border-[rgba(0,255,255,0.3)] shadow-[4px_4px_2px_rgba(0,255,125,0.5)]' : 'bg-[rgba(204,43,94,0.1)] border-[0.5rem] border-[rgba(204,43,94,0.3)] shadow-[4px_4px_2px_rgba(204,43,94,0.5)]'} rounded-[2px] relative">
            <div class="absolute -top-[10px] {milestone.isRight ? 'right-[20px] bg-[rgba(0,255,255,0.5)]' : 'left-[20px] bg-[rgba(204,43,94,0.5)]'} py-1 px-4 rounded-[15px]">
              <h6 class="mb-0 text-white">{milestone.year}</h6>
            </div>
            <h4 class="{milestone.isRight ? 'text-danger' : 'text-info'} text-2xl font-orbital mt-4">{milestone.title}</h4>
            <p class="mb-0 text-primary">{milestone.description}</p>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<!-- Values Section -->
<div
        id="values"
        bind:this={valuesRef}
        class="bg-light py-5"
>
  <div
          class="container mx-auto px-4 transition-all duration-800"
          style="opacity: {valuesVisible ? 1 : 0}; transform: {valuesVisible ? 'translateY(0)' : 'translateY(30px)'};"
  >
    <h2 class="text-5xl text-primary font-bold font-orbital-style-normal text-center mb-5">Our Core Values</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      {#each values as value, index}
        <div class="value-card {valuesVisible ? `fade-in-${(index % 3) + 1}` : ''}">
          <div class="p-8 bg-info border-[0.5rem] border-[rgba(0,255,255,0.5)] shadow-[6px_6px_3px_rgba(0,255,125,1)] rounded-[2px] h-full flex flex-col items-center text-center">
            <div class="mb-3 w-[60px] h-[60px] rounded-full bg-[rgba(204,43,94,0.2)] flex justify-center items-center">
              {@html value.icon}
            </div>
            <h3 class="text-primary text-2xl mb-3">{value.title}</h3>
            <p class="mb-0">{value.description}</p>
          </div>
        </div>
      {/each}
    </div>
  </div>
</div>

<!-- Contact Section -->
<div
        id="contact"
        bind:this={contactRef}
        class="bg-light py-5"
>
  <div
          class="container mx-auto px-4 transition-all duration-800"
          style="opacity: {contactVisible ? 1 : 0}; transform: {contactVisible ? 'translateY(0)' : 'translateY(30px)'};"
  >
    <div class="flex justify-center mb-5">
      <div class="w-full md:w-2/3 text-center">
        <h2 class="text-4xl text-danger mb-4">Get In Touch</h2>
        <p class="text-lg text-primary">Have questions or feedback? We'd love to hear from you!</p>
      </div>
    </div>
    <div class="flex justify-center">
      <div class="w-full md:w-2/3">
        <div class="bg-[#002233] border-[1rem] border-[rgba(0,255,255,0.5)] shadow-[8px_8px_3px_rgba(0,255,125,1)] rounded-[2px] p-8">
          <form>
            <div class="flex flex-col md:flex-row gap-4 mb-4">
              <div class="w-full md:w-1/2">
                <input
                        type="text"
                        class="w-full h-[50px] border-[var(--danger)] bg-amber-50 border-4 px-3"
                        placeholder="Your Name"
                />
              </div>
              <div class="w-full md:w-1/2">
                <input
                        type="email"
                        class="w-full h-[50px] border-[var(--danger)] bg-amber-50 border-4 px-3"
                        placeholder="Your Email"
                />
              </div>
            </div>
            <div class="mb-4">
              <input
                      type="text"
                      class="w-full h-[50px] border-[var(--danger)] bg-amber-50 border-4 px-3"
                      placeholder="Subject"
              />
            </div>
            <div class="mb-4">
              <textarea
                      class="w-full border-[var(--danger)] bg-amber-50 border-4 p-3"
                      rows="6"
                      placeholder="Your Message"
              ></textarea>
            </div>
            <div class="text-center">
              <button
                      type="submit"
                      class="px-5 py-2 border-2 border-[var(--primary)] text-[var(--primary)] rounded-[2px] text-lg"
              >
                Send Message
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Final CTA Section -->
<div class="py-5 text-center" style="background: linear-gradient(135deg, rgba(204, 43, 94, 0.8) 0%, rgba(0, 255, 255, 0.8) 100%)">
  <div class="container mx-auto py-4">
    <h2 class="text-white mb-4">Ready to Transform Your Wellness Journey?</h2>
    <a href="#" class="px-5 py-2 bg-white rounded-[2px] text-lg inline-block">
      Join Our Community Today
    </a>
  </div>
</div>

<style>
  /* These styles will apply only to this component */
  :global(body) {
    overflow-x: hidden;
  }

  .transition-all {
    transition-property: all;
  }

  .duration-800 {
    transition-duration: 800ms;
  }
</style>