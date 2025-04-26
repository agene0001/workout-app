<script lang="ts">
    let { children } = $props();
    import Navbar from '$lib/components/Navbar.svelte';
    import "../app.css";
</script>

<div class="app">
    <header class="w-full fixed top-0 flex justify-center z-50">
        <div class="max-w-7xl w-full px-4">
            <Navbar />
        </div>
    </header>

    <main>
        {@render children()}
    </main>
</div>
