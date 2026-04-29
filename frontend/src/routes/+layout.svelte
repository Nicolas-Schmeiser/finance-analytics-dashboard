<script>
	import 'bootstrap/dist/css/bootstrap.min.css';
	import '../styles/global.css'
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	// Requires onMount otherwise error 500
	onMount(async () => {
		await import('bootstrap/dist/js/bootstrap.bundle.min.js'); // Menu button mobile layout
	});

	let { children } = $props();
</script>

<!--Flex Page Wrapper-->
<div class="d-flex flex-column min-vh-100">
	<!--NAVBAR-->
	<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
	<div class="container">

		<!--Title-->
		<a class="navbar-brand fw-bold">
		Finance Analytics
		</a>

		<!--Mobile toggle button-->
		<button
		class="navbar-toggler"
		type="button"
		data-bs-toggle="collapse"
		data-bs-target="#navbarNav"
		>
		<span class="navbar-toggler-icon"></span>
		</button>

		<!--Navigation links-->
		<div
		class="collapse navbar-collapse"
		id="navbarNav"
		>
		<ul class="navbar-nav ms-auto">
			<li class="nav-item">
			<a
				class="nav-link {$page.url.pathname === '/dashboard' ? 'active fw-bold' : ''}"
				href="/dashboard"
			>
				Dashboard
			</a>
			</li>
			<li class="nav-item">
			<a
				class="nav-link {$page.url.pathname === '/transactions' ? 'active fw-bold' : ''}"
				href="/transactions"
			>
				Transactions
			</a>
			</li>
		</ul>
		</div>
	</div>
	</nav>

	
	<!--Page Content-->
	<main class="flex-grow-1">
    <div class="container mt-4">
      {@render children()}
    </div>
  	</main>


	<!--Footer-->
	<footer class="bg-light border-top py-3">
	<div class="container text-center">
		<small class="text-muted">
		Finance Analytics Dashboard — Nicolas Schmeiser — 2026
		</small>
	</div>
	</footer>
</div>