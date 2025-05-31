<!-- src/lib/components/Portal.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';

    // By default, portal to document.body, but can be customized
    export let target = 'body';

    let el; // The container element we create and move
    let targetEl; // The resolved target DOM element

    onMount(() => {
        // Resolve the target element
        targetEl = typeof target === 'string' ? document.querySelector(target) : target;

        if (el && targetEl) {
            // Move the element to the target when the component mounts
            targetEl.appendChild(el);
            // Make visible only *after* moving to prevent potential flicker
            el.hidden = false;
        } else {
            console.error('Portal target element not found:', target);
        }

        // Cleanup function when the Portal component is destroyed
        return () => {
            if (el && el.parentNode === targetEl) {
                targetEl.removeChild(el);
            }
        };
    });
</script>

<!--
Create the div element.
It's initially hidden and not attached to the target
until onMount runs, preventing layout shifts.
-->
<div bind:this={el} hidden>
    <slot></slot>
</div>