<!-- /////////////////////// Logic (JavaScript) /////////////////////// -->

<script>

    import { onMount } from "svelte";

    // General Variables
    let transactions = $state([]);
    let loading = $state(true);
    let categories = $state([]);
    let totalSpend = $state(0);
    let editingTransactionId = $state(null);
    let editingCategoryId = $state(null);
    
    // Filters
    let selectedCategory = $state("");
    let selectedMinAmount = $state("");
    let selectedMaxAmount = $state("");
    let selectedStartDate = $state("");
    let selectedEndDate = $state("");
    
    // Dynamic category filter
    async function loadCategories() { 

        const response = await fetch("http://127.0.0.1:8000/categories");
        categories = await response.json();
    }

    // Loading filtered data for transaction table & aggregated field
    async function loadTransactions(
        category = "", 
        minAmount = "", 
        maxAmount = "",
        startDate = "",
        endDate = ""
    ) {

        loading = true;
        let url = "http://127.0.0.1:8000/transactions";

        // Enables multiple params separated by '&' in URL for filtering
        const params = new URLSearchParams();
        if (category) {params.append("category",category);}
        if (minAmount !== "" && minAmount !== null) {params.append("min_amount",minAmount);}
        if (maxAmount !== "" && maxAmount !== null) {params.append("max_amount",maxAmount);}
        if (startDate !== "" && startDate !== null) {params.append("start_date",startDate);}
        if (endDate !== "" && endDate !== null) {params.append("end_date",endDate);}
        if (params.toString()) {url += `?${params.toString()}`;}

        const response = await fetch(url);
        transactions = await response.json();

        calculateTotalSpend();

        loading = false;
    }

    // Apply filters when button pressed
    function filterTransactions() {
        loadTransactions(
            selectedCategory, 
            selectedMinAmount, 
            selectedMaxAmount, 
            selectedStartDate, 
            selectedEndDate);
    }

    // Reset filters when button pressed
    function clearFilter(){
        selectedCategory = "";
        selectedMinAmount = "";
        selectedMaxAmount = "";
        selectedStartDate = "";
        selectedEndDate = "";
        loadTransactions();
    }

    // Calculate aggregated TotalSpend
    function calculateTotalSpend() {
        let sum = 0;
        for (let t of transactions) {
            sum += Number(t.amount);
        }
        totalSpend = sum;
    }

    // Manage the category edit button
    async function handleEdit(transactionId) {

        if (transactionId === editingTransactionId) {
            await fetch(
            `http://127.0.0.1:8000/transactions/${editingTransactionId}/category?category_id=${editingCategoryId}`,
            { method: "PUT" }
            );
            editingTransactionId = null;
            editingCategoryId = null;
            loadTransactions();
        }

        else {
            // enter edit mode
            editingTransactionId = transactionId
            // editingCategoryId = categoryId -> first add category_id in transaction table
        }
    }

    // Define which function to run at page loading
    onMount(() => {
        loadTransactions();
        loadCategories();
    });

</script>


<!-- /////////////////////// Components (Svelte & Bootstrap) /////////////////////// -->

<!--General Container-->
<div class="container mt-4">

<h1 class="mb-4">Transactions</h1>

<!--Filters-->
<div class="mb-4">

  <h5 class="mb-3">
    Filters
  </h5>

  <label class="form-label">From:</label>
    <input
        type="date"
        class="form-control mb-3"
        bind:value={selectedStartDate}
    />

    <label class="form-label">To:</label>
    <input
        type="date"
        class="form-control mb-3"
        bind:value={selectedEndDate}
    />

    <label class="form-label">Category:</label>
    <select 
        bind:value={selectedCategory}
        class="form-control mb-3">
        <option value="">All</option>
        {#each categories as category}
            <option value={category.id}>
                {category.name}
            </option>
        {/each}
    </select>

    <label class="form-label">Min Amount:</label>
    <input
        type="number"
        class="form-control mb-3"
        bind:value={selectedMinAmount}
    />

    <label class="form-label">Max Amount:</label>
    <input
        type="number"
        class="form-control mb-3"
        bind:value={selectedMaxAmount}
    />
</div>

<!--Filter buttons-->
<div>
    <button 
        class="btn btn-primary me-2" 
        onclick={filterTransactions}
    >
        Apply Filter
    </button>
    <button 
        class="btn btn-secondary" 
        onclick={clearFilter}
    >
        Clear
    </button>
</div>


<div class="alert alert-info mt-3">
    <strong>Total Spend:</strong>
    {totalSpend.toFixed(2)} €
</div>

<!--Separation line-->
<hr class="my-4">

<!--Transaction Table-->
<table class="table table-striped table-hover mt-3">
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
                    <td>
                        <!-- Edit mode active -->
                        {#if transaction.id === editingTransactionId}
                            <select 
                                class="form-select form-select-sm"
                                bind:value={editingCategoryId}
                                >
                                {#each categories as category}
                                    <option value={category.id}>
                                        {category.name}
                                    </option>
                                {/each}
                            </select>
                        <!-- Edit mode not active -->
                        {:else}
                            {transaction.category}
                        {/if}
                    </td>
                    <td> 
                        <button class="btn btn-sm btn-secondary"
                        onclick={() => handleEdit(transaction.id)}
                        // Display different label based on edit mode state
                        >{transaction.id === editingTransactionId ? "Save" : "Edit"} 
                        </button>
                    </td>
                </tr>
            {/each}
        {/if}
    </tbody>
</table>

</div>