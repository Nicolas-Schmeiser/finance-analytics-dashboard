<!-- /////////////////////// Logic (JavaScript) /////////////////////// -->

<script>

    import { goto } from "$app/navigation";
    import Chart from "chart.js/auto";

    // Accessing data passed from server-side load function as props
    let {data} = $props();

    // Data
    let CategorySpendWithBudget = $derived(data.categorySpendWithBudget);
    let monthlyTotalSpend = $derived(data.monthlyTotalSpend);
    let monthlyTotalBudget = $derived(data.monthlyTotalBudget);
    let totalSpend = $derived(CategorySpendWithBudget.reduce((sum, c) => sum + c.spent, 0));
    let remainingBudget = $derived(CategorySpendWithBudget.reduce((sum, c) => sum + c.budget - c.spent, 0));
    
    // Charts
    let categoryChart;
    let trendChart;

    // Filters
    let selectedStartDate = $state("");
    let selectedEndDate = $state("");

    // Apply filters when button pressed
    function applyFilters(){

        const params = new URLSearchParams();

        if (selectedStartDate) {params.append("start_date", selectedStartDate);}
        if (selectedEndDate) {params.append("end_date", selectedEndDate);}

        goto(`?${params.toString()}`);
    }

    // Reset filters when button pressed
    function clearFilter(){

        selectedStartDate = "";
        selectedEndDate = "";

        goto("?");
    }

    // Monthly Category Visual
    function renderCategoryChart() {
        const spentColor = "rgba(54, 162, 235, 1)";
        const budgetColor = "rgba(255, 159, 64, 1)";
        const labels = CategorySpendWithBudget.map(row => row.category)
        const spent = CategorySpendWithBudget.map(row => row.spent)
        const budget = CategorySpendWithBudget.map(row => row.budget)
        const ctx = document.getElementById("categoryChart")
        if (categoryChart) {categoryChart.destroy();}
        categoryChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Spent",
                        data: spent,
                        backgroundColor: "rgba(54, 162, 235, 0.6)",
                        borderColor: spentColor,
                        borderWidth: 1
                    },
                    {
                        label: "Budget",
                        data: budget,
                        backgroundColor: "rgba(255, 159, 64, 0.6)",
                        borderColor: budgetColor,
                        borderWidth: 1
                    }
                ]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: "Spend vs Budget by Category"
                    }
                }
            },
        })
    }

    // Monthly Total Spend Visual
    function renderTotalSpendChart(){
        const spentColor = "rgba(54, 162, 235, 1)";
        const budgetColor = "rgba(255, 159, 64, 1)";
        const ctx =document.getElementById("trendChart");
        const spentByMonth = new Map(monthlyTotalSpend.map(row => [row.year_month, row.spent]));
        const budgetByMonth = new Map(monthlyTotalBudget.map(row => [row.year_month, row.budget]));
        const labels = [...new Set([...spentByMonth.keys(), ...budgetByMonth.keys()])].sort();
        const totals = labels.map((month) => spentByMonth.get(month) ?? 0);
        const budgets = labels.map((month) => budgetByMonth.get(month) ?? 0);
        if (trendChart) {trendChart.destroy();}
        trendChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Total Spend",
                        data: totals,
                        tension: 0.3,
                        borderColor: spentColor,
                        backgroundColor: "rgba(54, 162, 235, 0.2)"
                    },
                    {
                        label: "Total Budget",
                        data: budgets,
                        tension: 0.3,
                        borderColor: budgetColor,
                        backgroundColor: "rgba(255, 159, 64, 0.2)"
                    }
                ]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: "Spend and Budget Over Time"
                    }
                }
            },
        });
    }

    // Render charts whenever data changes (initial load and after applying filters)
    $effect(() => {
        renderCategoryChart();
        renderTotalSpendChart();
    });

</script>


<!-- /////////////////////// Components (Svelte & Bootstrap) /////////////////////// -->

<!--General Container-->

<div class="container mt-4">

    <div class="row mb-4">
    
        <!--LEFT: Filters-->
        <div class="col-12 col-md-6">
            <div class="mb-4">
                <h5 class="mb-3">
                    Filters
                </h5>
                <div class="row g-3">
                    <div class="col-12 col-md">
                        <label class="form-label">From:</label>
                        <input
                            type="date"
                            class="form-control"
                            bind:value={selectedStartDate}
                        />
                    </div>
                    <div class="col-12 col-md">
                        <label class="form-label">To:</label>
                        <input
                            type="date"
                            class="form-control"
                            bind:value={selectedEndDate}
                        />
                    </div>
                    <div class="col-12 col-md-auto d-flex align-items-end">
                        <button
                            class="btn btn-primary me-2"
                            onclick={applyFilters}
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
                </div>
            </div>
        </div>

    <!--RIGHT: Total Spend card-->
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
        
        <!--Remaining Budget Card -->
        <div class="col-12 col-md-3">
            <div class="card shadow-sm h-100">
                <div class="card-body">
                    <h6 class="card-title text-muted">
                    Remaining Budget
                    </h6>
                    <h3 class="fw-bold">
                    {remainingBudget} €
                    </h3>
                </div>
            </div>
        </div>
    
    </div>

    <!--Separation line-->
    <hr class="my-4">

    <!--Visuals-->
    <div class="row">
        <div class="col-md-6">
            <canvas id="categoryChart"></canvas>
        </div>
        <div class="col-md-6">
            <canvas id="trendChart"></canvas>
        </div>
    </div>

</div>