<!-- /////////////////////// Logic (JavaScript) /////////////////////// -->

<script>
    import { enhance } from "$app/forms";
    import { goto } from "$app/navigation";

    // Accessing data passed from server-side load function as props
    let {data} = $props();

    // Data
    let transactions = $derived(data.transactions);
    let categories = $derived(data.categories);
    let totalSpend = $derived(transactions.reduce((sum, t) => sum + t.amount, 0));
    
    // State
    let loading = $state(false);
    let currentPage = $state(1);
    const pageSize = 10;

    // Editing Category
    let editingTransactionId = $state(null);
    let editingCategoryId = $state(null);
    
    // Filters
    let selectedCategoryId = $state("");
    let selectedMinAmount = $state("");
    let selectedMaxAmount = $state("");
    let selectedStartDate = $state("");
    let selectedEndDate = $state("");

    // Sorting
    let sortColumn = $state(null);
    let sortDirection = $state("asc");

    // Pagination
    let totalPages = $derived(Math.max(1, Math.ceil(transactions.length / pageSize)));
    let paginatedTransactions = $derived(
        transactions.slice((currentPage - 1) * pageSize, currentPage * pageSize)
    );

    // Apply filters when button pressed
    function filterTransactions() {

        const params = new URLSearchParams();

        if (selectedCategoryId) params.append("category_id", selectedCategoryId);
        if (selectedMinAmount) params.append("min_amount", selectedMinAmount);
        if (selectedMaxAmount)params.append("max_amount", selectedMaxAmount);
        if (selectedStartDate) params.append("start_date", selectedStartDate);
        if (selectedEndDate) params.append("end_date", selectedEndDate);

        currentPage = 1;
        goto(`?${params.toString()}`);
    }

    // Reset filters when button pressed
    function clearFilter() {

        selectedCategoryId = "";
        selectedMinAmount = "";
        selectedMaxAmount = "";
        selectedStartDate = "";
        selectedEndDate = "";
        currentPage = 1;

        goto("?");
    }

    function handleEdit(transaction) {

        if (editingTransactionId === transaction.id) {
            // Save mode handled by form submit
            return;

        } else {

            editingTransactionId = transaction.id;
            editingCategoryId = transaction.category_id;
        }
    }

    // Sort Columns
    function handleSort(column) {

        // Toggle direction if same column
        if (sortColumn === column) {
            sortDirection = sortDirection === "asc" ? "desc" : "asc";
        }

        // New column → reset direction
        else {
            sortColumn = column;
            sortDirection = "asc";
        }

        // Perform sorting
        transactions = [...transactions].sort((a, b) => {

            let valueA = a[column];
            let valueB = b[column];

            // Handle numbers
            if (!isNaN(valueA) && !isNaN(valueB)) {
                return sortDirection === "asc"
                    ? valueA - valueB
                    : valueB - valueA;
            }

            // Handle dates
            if (column === "date") {
                let dateA = new Date(valueA);
                let dateB = new Date(valueB);

                return sortDirection === "asc"
                    ? dateA - dateB
                    : dateB - dateA;
            }

            // Handle text
            return sortDirection === "asc"
                ? String(valueA).localeCompare(String(valueB))
                : String(valueB).localeCompare(String(valueA));
        });
        currentPage = 1;
    }

    // Sorting direction
    function getSortArrow(column) {

        if (sortColumn !== column) {
            return "";
        }

        return sortDirection === "asc"
            ? " ↑"
            : " ↓";
    }

    function handleCategorySaved(transactionId, categoryId) {
        const selectedCategory = categories.find(
            (category) => String(category.id) === String(categoryId)
        );

        if (!selectedCategory) return;

        transactions = transactions.map((transaction) =>
            transaction.id === transactionId
                ? {
                    ...transaction,
                    category_id: selectedCategory.id,
                    category_name: selectedCategory.name
                }
                : transaction
        );

        editingTransactionId = null;
        editingCategoryId = null;
    }

    function previousPage() {
        if (currentPage > 1) {
            currentPage -= 1;
        }
    }

    function nextPage() {
        if (currentPage < totalPages) {
            currentPage += 1;
        }
    }
</script>


<!-- /////////////////////// Components (Svelte & Bootstrap) /////////////////////// -->

<!--General Container-->
<div class="container mt-4">

    <div class="row mb-4">

    <!-- LEFT: Filters -->
    <div class="col-12 col-md-9">

        <!--Filters-->
        <div class="mb-4">
            <h5 class="mb-3">
                Filters
            </h5>

            <div class="row g-3">
                <div class="col-12 col-md">
                    <label for="start-date" class="form-label">From:</label>
                    <input
                        id="start-date"
                        type="date"
                        class="form-control"
                        bind:value={selectedStartDate}
                    />
                </div>
                <div class="col-12 col-md">
                    <label for="end-date" class="form-label">To:</label>
                    <input
                        id="end-date"
                        type="date"
                        class="form-control"
                        bind:value={selectedEndDate}
                    />
                </div>
                <div class="col-12 col-md">
                    <label for="category-select" class="form-label">Category:</label>
                    <select
                        id="category-select"
                        bind:value={selectedCategoryId}
                        class="form-select"
                    >
                        <option value="">All</option>
                        {#each categories as category}
                        <option value={category.id}>
                            {category.name}
                        </option>
                        {/each}
                    </select>
                </div>
                <div class="col-12 col-md">
                    <label for="min-amount" class="form-label">Min Amount:</label>
                    <input
                        id="min-amount"
                        type="number"
                        class="form-control"
                        bind:value={selectedMinAmount}
                    />
                </div>
                <div class="col-12 col-md">
                    <label for="max-amount" class="form-label">Max Amount:</label>
                    <input
                        id="max-amount"
                        type="number"
                        class="form-control"
                        bind:value={selectedMaxAmount}
                    />
                </div>
                <div class="col-12 col-md-auto d-flex align-items-end">
                    <button
                        class="btn btn-primary me-2"
                        onclick={filterTransactions}
                    > Apply Filter
                    </button>
                    <button
                        class="btn btn-secondary"
                        onclick={clearFilter}
                    > Clear
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- RIGHT: Total Spend card -->
    <div class="col-12 col-md-3">
        <div class="card shadow-sm h-100">
        <div class="card-body">
            <h6 class="card-title text-muted">
            Total Spend
            </h6>
            <h3 class="fw-bold">
            {totalSpend} €
            </h3>
        </div>
        </div>
    </div>
    </div>

    <!--Separation line-->
    <hr class="my-4">

    <!--Transaction Table-->
    <div class="table-responsive">
        <table class="table table-striped table-hover mt-3">
            <thead>
                <tr>
                    <th 
                        onclick={() => handleSort("id")}
                        style="cursor: pointer;"
                    > ID {getSortArrow("id")}
                    </th>
                    <th 
                        onclick={() => handleSort("description")}
                        style="cursor: pointer;"
                    > Description {getSortArrow("description")}
                    </th>
                    <th 
                        onclick={() => handleSort("amount")}
                        style="cursor: pointer;"
                    > Amount {getSortArrow("amount")}
                    </th>
                    <th 
                        onclick={() => handleSort("date")}
                        style="cursor: pointer;"
                    > Date {getSortArrow("date")}
                    </th>
                    <th 
                        onclick={() => handleSort("category_name")}
                        style="cursor: pointer;"
                    > Category {getSortArrow("category_name")}
                    </th>
                </tr>
            </thead>

            <tbody>
                {#if loading}
                    <tr>
                        <td colspan="6">Loading data...</td>
                    </tr>
                {:else if transactions.length === 0}
                    <tr>
                        <td colspan="6">No transactions found</td>
                    </tr>
                {:else}
                    {#each paginatedTransactions as transaction}
                        <tr>
                            <td>{transaction.id}</td>
                            <td>{transaction.description}</td>
                            <td>{transaction.amount}</td>
                            <td>{transaction.date}</td>
                            <td>
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
                                {:else}
                                    {transaction.category_name}
                                {/if}
                            </td>
                            <td>
                                {#if transaction.id === editingTransactionId}
                                    <form
                                        method="POST"
                                        action="?/updateCategory"
                                        use:enhance={() => {
                                            return async ({ result }) => {
                                                if (result.type === "success") {
                                                    handleCategorySaved(transaction.id, editingCategoryId);
                                                }
                                            };
                                        }}
                                    >
                                        <input
                                            type="hidden"
                                            name="transactionId"
                                            value={transaction.id}
                                        />
                                        <input
                                            type="hidden"
                                            name="categoryId"
                                            value={editingCategoryId}
                                        />
                                        <button
                                            class="btn btn-sm btn-secondary"
                                            type="submit"
                                        >Save
                                        </button>
                                    </form>
                                {:else}
                                    <button
                                        class="btn btn-sm btn-secondary"
                                        onclick={() => handleEdit(transaction)}
                                    >Edit
                                    </button>
                                {/if}
                            </td>
                        </tr>
                    {/each}
                {/if}
            </tbody>
        </table>
    </div>

    {#if transactions.length > 0}
        <div class="d-flex justify-content-between align-items-center mt-3 mb-4">
            <small class="text-muted">
                Showing {(currentPage - 1) * pageSize + 1}
                -
                {Math.min(currentPage * pageSize, transactions.length)}
                of {transactions.length}
            </small>
            <div class="btn-group" role="group" aria-label="Pagination controls">
                <button
                    class="btn btn-outline-secondary btn-sm"
                    onclick={previousPage}
                    disabled={currentPage === 1}
                >
                    Previous
                </button>
                <button class="btn btn-outline-secondary btn-sm" disabled>
                    Page {currentPage} / {totalPages}
                </button>
                <button
                    class="btn btn-outline-secondary btn-sm"
                    onclick={nextPage}
                    disabled={currentPage === totalPages}
                >
                    Next
                </button>
            </div>
        </div>
    {/if}
</div>