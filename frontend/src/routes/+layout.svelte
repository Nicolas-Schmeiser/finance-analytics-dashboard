<script>
	import favicon from '$lib/assets/favicon.svg';
	import 'bootstrap/dist/css/bootstrap.min.css';

	let { children } = $props();
</script>

<!--navigation bar, footer, theme settings-->

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children()}
