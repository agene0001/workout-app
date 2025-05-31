<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { browser } from '$app/environment';

    let scrollPercentage = 0;

    function updateScrollPercentage() {
        if (!browser) return;

        const postContentElement = document.querySelector('.post-content-for-progress'); // Target a specific element
        if (!postContentElement) {
            // Fallback to documentElement if specific element not found,
            // but this might not be accurate if there's content outside the post body.
            const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            scrollPercentage = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
            return;
        }

        const elementRect = postContentElement.getBoundingClientRect();
        const elementHeight = postContentElement.scrollHeight; // Use scrollHeight for full content height
        const viewportHeight = window.innerHeight;

        // Calculate how much of the element is visible or has been scrolled past
        // scrollTop relative to the element's top
        const scrollTopInElement = Math.max(0, -elementRect.top);

        // Total scrollable distance within the element
        const scrollableDistanceInElement = elementHeight - viewportHeight;


        if (elementRect.bottom < 0 || elementRect.top > viewportHeight) {
            // Element is completely out of view (either above or below)
            if (elementRect.bottom < 0) scrollPercentage = 100; // scrolled past
            else scrollPercentage = 0; // not yet reached
        } else if (scrollableDistanceInElement <= 0) {
            // Element is shorter than or equal to viewport height and at least partially visible
            scrollPercentage = 100; // Consider it fully "read" if fully visible and short
        } else {
            scrollPercentage = (scrollTopInElement / scrollableDistanceInElement) * 100;
        }
        scrollPercentage = Math.min(100, Math.max(0, scrollPercentage)); // Clamp between 0 and 100
    }

    onMount(() => {
        if (browser) {
            window.addEventListener('scroll', updateScrollPercentage);
            window.addEventListener('resize', updateScrollPercentage); // Recalculate on resize
            updateScrollPercentage(); // Initial calculation
        }
    });

    onDestroy(() => {
        if (browser) {
            window.removeEventListener('scroll', updateScrollPercentage);
            window.removeEventListener('resize', updateScrollPercentage);
        }
    });
</script>

<div class="reading-progress-bar-container">
    <div class="reading-progress-bar" style="width: {scrollPercentage}%"></div>
</div>

<style>
    .reading-progress-bar-container {
        position: fixed;
        top: 0; /* Adjust if you have a fixed header, e.g., top: 60px; */
        left: 0;
        width: 100%;
        height: 5px; /* Thickness of the bar */
        background-color: transparent; /* Or a light background for the track */
        z-index: 1000;
        pointer-events: none; /* So it doesn't interfere with clicks */
    }

    .reading-progress-bar {
        height: 100%;
        background-color: var(--secondary-color, #c62368); /* Use your theme color */
        transition: width 0.1s ease-out;
    }
</style>