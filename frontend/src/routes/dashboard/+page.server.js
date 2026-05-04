// This function runs on the server before the page is rendered
// allowing to pass the fetched data as props to the Svelte component.
export async function load({ fetch, url }) {

    const params = url.searchParams;

    const CategorySpendWithBudgetRes = await fetch(
        `http://127.0.0.1:8000/category_spend_with_budget?${params}`
    );

    const monthlyTotalSpendRes = await fetch(
        `http://127.0.0.1:8000/monthly_total_spend?${params}`
    );

    return {
        categorySpendWithBudget: await CategorySpendWithBudgetRes.json(),
        monthlyTotalSpend: await monthlyTotalSpendRes.json()
    };
}