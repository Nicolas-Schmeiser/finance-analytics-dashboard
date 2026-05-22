<!-- /////////////////////// Logic (JavaScript) /////////////////////// -->

<script>
    import { enhance } from "$app/forms";
    import { goto } from "$app/navigation";
    import { formatCurrency, formatCurrencyWithSymbol } from "$lib/format";

    // Accessing data passed from server-side load function as props
    let {data, form} = $props();

    // Data
    let transactions = $derived(data.transactions);
    let categories = $derived(data.categories);

    // State
    let loading = $state(false);
    let currentPage = $state(1);
    const pageSize = 10;
    let searchQuery = $state("");

    // Editing Category
    let editingTransactionId = $state(null);
    let editingCategoryId = $state(null);
    
    // Filters
    let selectedCategoryId = $state("");
    let selectedMinAmount = $state("");
    let selectedMaxAmount = $state("");
    let selectedStartDate = $state("");
    let selectedEndDate = $state("");

    let filteredTransactions = $derived(
        transactions.filter((transaction) =>
            transactionMatchesSearch(transaction, searchQuery)
        )
    );
    let totalSpend = $derived(
        filteredTransactions.reduce((sum, t) => sum + Number(t.amount), 0)
    );

    // Sorting
    let sortColumn = $state(null);
    let sortDirection = $state("asc");

    // Pagination
    let totalPages = $derived(Math.max(1, Math.ceil(filteredTransactions.length / pageSize)));
    let paginatedTransactions = $derived(
        filteredTransactions.slice((currentPage - 1) * pageSize, currentPage * pageSize)
    );

    function transactionMatchesSearch(transaction, query) {
        const normalizedQuery = query.trim().toLowerCase();

        if (!normalizedQuery) {
            return true;
        }

        return [
            transaction.id,
            transaction.description,
            transaction.amount,
            formatCurrency(transaction.amount),
            transaction.date,
            transaction.category_name
        ].some((value) => String(value).toLowerCase().includes(normalizedQuery));
    }

    function handleSearchInput() {
        currentPage = 1;
    }

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
        searchQuery = "";
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

    function normalizeCurrentPage() {
        if (currentPage > totalPages) {
            currentPage = totalPages;
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
                        step="0.01"
                        min="0"
                        class="form-control"
                        bind:value={selectedMinAmount}
                    />
                </div>
                <div class="col-12 col-md">
                    <label for="max-amount" class="form-label">Max Amount:</label>
                    <input
                        id="max-amount"
                        type="number"
                        step="0.01"
                        min="0"
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
            {formatCurrencyWithSymbol(totalSpend)}
            </h3>
        </div>
        </div>
    </div>
    </div>

    <!--Separation line-->
    <hr class="my-4">

    <!--Global Search-->
    <div class="row mb-3">
        <div class="col-12 col-md-6 col-lg-4">
            <label for="transaction-search" class="form-label">Search</label>
            <input
                id="transaction-search"
                type="search"
                class="form-control"
                placeholder="Search by ID, description, amount, date, or category..."
                bind:value={searchQuery}
                oninput={handleSearchInput}
            />
        </div>
    </div>

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
                {:else if filteredTransactions.length === 0}
                    <tr>
                        <td colspan="6">No transactions found</td>
                    </tr>
                {:else}
                    {#each paginatedTransactions as transaction}
                        <tr>
                            <td>{transaction.id}</td>
                            <td>{transaction.description}</td>
                            <td>{formatCurrencyWithSymbol(transaction.amount)}</td>
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
                                    <div class="d-flex gap-2">
                                        <button
                                            class="btn btn-sm btn-secondary"
                                            onclick={() => handleEdit(transaction)}
                                        >Edit
                                        </button>
                                        <form
                                            method="POST"
                                            action="?/deleteTransaction"
                                            use:enhance={() => {
                                                return async ({ result }) => {
                                                    if (result.type === "success") {
                                                        transactions = transactions.filter(
                                                            (item) => item.id !== transaction.id
                                                        );
                                                        normalizeCurrentPage();
                                                    }
                                                };
                                            }}
                                        >
                                            <input
                                                type="hidden"
                                                name="transactionId"
                                                value={transaction.id}
                                            />
                                            <button
                                                class="btn btn-sm btn-outline-danger"
                                                type="submit"
                                            >Delete
                                            </button>
                                        </form>
                                    </div>
                                {/if}
                            </td>
                        </tr>
                    {/each}
                {/if}
            </tbody>
        </table>
    </div>

    <!-- Pagination Controls -->
    {#if filteredTransactions.length > 0}
        <div class="d-flex justify-content-between align-items-center mt-3 mb-4">
            <small class="text-muted">
                Showing {(currentPage - 1) * pageSize + 1}
                -
                {Math.min(currentPage * pageSize, filteredTransactions.length)}
                of {filteredTransactions.length}
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

    <!--Separation line-->
    <hr class="my-4">

    <!--Add Transaction Form-->
    <div class="card shadow-sm mt-2 mb-4">
        <div class="card-body">
            <h5 class="card-title mb-3">Add Transaction</h5>

            {#if form?.error}
                <div class="alert alert-danger py-2 mb-3" role="alert">
                    {form.error}
                </div>
            {/if}

            {#if form?.success}
                <div class="alert alert-success py-2 mb-3" role="alert">
                    {form.message}
                </div>
            {/if}

            <form
                method="POST"
                action="?/addTransaction"
                use:enhance={({ formElement }) => {
                    return async ({ result }) => {
                        if (result.type === "success") {
                            const { transaction } = result.data;
                            const selectedCategory = categories.find(
                                (category) => String(category.id) === String(transaction.category_id)
                            );

                            transactions = [
                                {
                                    ...transaction,
                                    category_name: selectedCategory?.name ?? "Unknown"
                                },
                                ...transactions
                            ];

                            formElement.reset();
                            currentPage = 1;
                        }
                    };
                }}
            >
                <div class="row g-3">
                    <div class="col-12 col-md-4">
                        <label for="new-description" class="form-label">Description</label>
                        <input
                            id="new-description"
                            name="description"
                            type="text"
                            class="form-control"
                            required
                        />
                    </div>
                    <div class="col-12 col-md-2">
                        <label for="new-amount" class="form-label">Amount</label>
                        <input
                            id="new-amount"
                            name="amount"
                            type="number"
                            step="0.01"
                            min="0"
                            class="form-control"
                            required
                        />
                    </div>
                    <div class="col-12 col-md-3">
                        <label for="new-date" class="form-label">Date</label>
                        <input
                            id="new-date"
                            name="date"
                            type="date"
                            class="form-control"
                            required
                        />
                    </div>
                    <div class="col-12 col-md-3">
                        <label for="new-category" class="form-label">Category</label>
                        <select
                            id="new-category"
                            name="categoryId"
                            class="form-select"
                            required
                        >
                            <option value="" disabled selected>Select category</option>
                            {#each categories as category}
                                <option value={category.id}>{category.name}</option>
                            {/each}
                        </select>
                    </div>
                </div>

                <div class="mt-3">
                    <button type="submit" class="btn btn-primary">
                        Add Transaction
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>