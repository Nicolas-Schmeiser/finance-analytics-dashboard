// This function runs on the server before the page is rendered
// allowing to pass the fetched data as props to the Svelte component.
export async function load({ fetch }) {

    const transactionsRes = await fetch(
        "http://127.0.0.1:8000/transactions"
    );

    const categoriesRes = await fetch(
        "http://127.0.0.1:8000/categories"
    );

    return {
        transactions: await transactionsRes.json(),
        categories: await categoriesRes.json()
    };
}