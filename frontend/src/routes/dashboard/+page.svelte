<!-- /////////////////////// Logic (JavaScript) /////////////////////// -->

<script>

    import { onMount } from "svelte";
    import Chart from "chart.js/auto";

    // General Variables
    let loading = $state(true);
    let monthlyCategorySummary = $state([])
    let monthlyTotalSpend = $state([])
    let totalSpend = $state(0);
    let remainingBudget = $state(0);
    let categoryChart;
    let trendChart;

    // Filters
    let selectedStartDate = $state("");
    let selectedEndDate = $state("");

    // Loading filtered data for the summarized monthly category vs budget bar visual
    async function loadMonthlyCategorySummary(
        startDate = "",
        endDate = ""
    ) {
        loading = true;
        let url = "http://127.0.0.1:8000/monthly_category_summary";

        // Enables multiple params separated by '&' in URL for filtering
        const params = new URLSearchParams();
        if (startDate !== "" && startDate !== null) {params.append("start_date",startDate);}
        if (endDate !== "" && endDate !== null) {params.append("end_date",endDate);}
        if (params.toString()) {url += `?${params.toString()}`;}

        const response = await fetch(url);
        monthlyCategorySummary = await response.json();

        calculateTotalSpend();
        calculateRemainingBudget();
        renderCategoryChart();

        loading = false;
    }

    // Loading filtered data for the summarized monthly Time-Serie visual
    async function loadMonthlyTotalSpend(
        startDate = "",
        endDate = ""
    ) {
        loading = true;
        let url = "http://127.0.0.1:8000/monthly_total_spend";

        // Enables multiple params separated by '&' in URL for filtering
        const params = new URLSearchParams();
        if (startDate !== "" && startDate !== null) {params.append("start_date",startDate);}
        if (endDate !== "" && endDate !== null) {params.append("end_date",endDate);}
        if (params.toString()) {url += `?${params.toString()}`;}

        const response = await fetch(url);
        monthlyTotalSpend = await response.json();

        renderTotalSpendChart();

        loading = false;
    }

    // Apply filters when button pressed
    function applyFilters(){
        loadMonthlyCategorySummary(
            selectedStartDate,
            selectedEndDate
        );
        loadMonthlyTotalSpend(
            selectedStartDate,
            selectedEndDate 
        );
    }

    // Reset filters when button pressed
    function clearFilter(){
        selectedStartDate = "";
        selectedEndDate = "";
        loadMonthlyCategorySummary();
        loadMonthlyTotalSpend();
    }

    // Calculate aggregated TotalSpend
    function calculateTotalSpend() {
        let sum = 0;
        for (let c of monthlyCategorySummary) {
            sum += Number(c.spent);
        }
        totalSpend = sum;
    }

    // Calculate remaining budget
    function calculateRemainingBudget() {
        let sumSpent = 0;
        let sumBudget = 0;
        for (let c of monthlyCategorySummary){
            sumSpent += Number(c.spent);
            sumBudget += Number(c.budget);
        }
        remainingBudget = sumBudget - sumSpent;
    }

    // Monthly Category Visual
    function renderCategoryChart() {
        const labels = monthlyCategorySummary.map(row => row.category)
        const spent = monthlyCategorySummary.map(row => row.spent)
        const budget = monthlyCategorySummary.map(row => row.budget)
        const ctx = document.getElementById("categoryChart")
        if (categoryChart) {categoryChart.destroy();}
        categoryChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {label: "Spent", data: spent},
                    {label: "Budget",data: budget}
                ]
            }
        })
    }

    // Monthly Total Spend Visual
    function renderTotalSpendChart(){
        const ctx =document.getElementById("trendChart");
        const labels = monthlyTotalSpend.map(row => row.year_month);
        const totals = monthlyTotalSpend.map(row => row.total_spent);
        if (trendChart) {trendChart.destroy();}
        trendChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {label: "Total Spend", data: totals, tension: 0.3}
                ]
            }
        });
    }

    // Define which function to run at page loading
    onMount(() => {
        loadMonthlyCategorySummary();
        loadMonthlyTotalSpend();
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
                    {totalSpend.toFixed(2)} €
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
                    {remainingBudget.toFixed(2)} €
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