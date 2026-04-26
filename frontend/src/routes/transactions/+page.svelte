<script>

    import { onMount } from "svelte";

    let transactions = $state([]);
    let loading = $state(true);
    let selectedCategory = $state(""); // Category filter

    async function loadTransactions(category = "") {

        loading = true;
        let url = "http://127.0.0.1:8000/transactions";

        if (category) {url += `?category=${category}`;}

        const response = await fetch(url);
        transactions = await response.json();
        loading = false;
    }

    function filterTransactions() {
        loadTransactions(selectedCategory);
    }

    onMount(loadTransactions);

</script>

<h1>Transactions</h1>

<select bind:value={selectedCategory}>
    <option value="">All</option>
    <option value="Groceries">Food</option>
    <option value="Transport">Transport</option>
</select>

<button onclick={filterTransactions}>
    Filter
</button>

<table border="1">
    <thead>
        <tr>
            <th>ID</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Category</th>
        </tr>
    </thead>

    <tbody>
        {#if loading}
            <tr>
                <td colspan="5">Loading data...</td>
            </tr>
        {:else if transactions.length === 0}
            <tr>
                <td colspan="5">No transactions found</td>
            </tr>
        {:else}
            {#each transactions as transaction}
                <tr>
                    <td>{transaction.id}</td>
                    <td>{transaction.description}</td>
                    <td>{transaction.amount}</td>
                    <td>{transaction.date}</td>
                    <td>{transaction.category}</td>
                </tr>
            {/each}
        {/if}
    </tbody>
</table>