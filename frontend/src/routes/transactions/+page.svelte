<!-- /////////////////////// Logic /////////////////////// -->

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

    // Edit selected transaction's category
    async function handleEdit() {
        await fetch(
            `http://127.0.0.1:8000/transactions/${editingTransactionId}/category?category_id=${editingCategoryId}`,
            { method: "PUT" }
        );
        editingTransactionId = null;
        loadTransactions();
    }

    // Define which function to run at page loading
    onMount(() => {
        loadTransactions();
        loadCategories();
    });

</script>


<!-- /////////////////////// Components /////////////////////// -->


<h1>Transactions</h1>

<label>From:</label>
<input
    type="date"
    bind:value={selectedStartDate}
/>

<label>To:</label>
<input
    type="date"
    bind:value={selectedEndDate}
/>

<label>Category:</label>
<select bind:value={selectedCategory}>
    <option value="">All</option>
    {#each categories as category}
        <option value={category.id}>
            {category.name}
        </option>
    {/each}
</select>

<label>Amount:</label>
<input
    type="number"
    placeholder="Min Amount"
    bind:value={selectedMinAmount}
/>
<input
    type="number"
    placeholder="Max Amount"
    bind:value={selectedMaxAmount}
/>

<button onclick={filterTransactions}>Filter</button>
<button onclick={clearFilter}>Clear</button>

<h3>
    Total Spend:
    {totalSpend.toFixed(2)} €
</h3>

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
                    <td>
                        <!-- Edit mode activated -->
                        {#if editingTransactionId === transaction.id}
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
                        <!-- Logic to display edit or save button depending on selection -->
                        {#if editingTransactionId === transaction.id}
                            <button class="btn btn-sm btn-primary"
                            // function wrapper needed due to parameter
                            // else the transaction.id would directly compute for each row during rendering
                            // and the function would become inactive (as already executed)
                            onclick={handleEdit()}
                            >Save</button> 
                        {:else}
                            <button class="btn btn-sm btn-primary"
                            // Enter editing state
                            onclick={editingTransactionId = transaction.id}
                            >Edit</button> 
                        {/if}
                    </td>
                </tr>
            {/each}
        {/if}
    </tbody>
</table>


<!-- /////////////////////// UI /////////////////////// -->

