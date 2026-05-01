// This function runs on the server before the page is rendered
// allowing to pass the fetched data as props to the Svelte component.
export async function load({ fetch, url }) {

    const params = url.searchParams;

    const transactionsRes = await fetch(
        `http://127.0.0.1:8000/transactions?${params}`
    );
 
    const categoriesRes = await fetch(
        "http://127.0.0.1:8000/categories"
    );

    return {
        transactions: await transactionsRes.json(),
        categories: await categoriesRes.json()
    };
}

// This object defines actions that can be triggered from the Svelte component,
// such as when a form is submitted. The action can perform server-side logic
// and then return data back to the component.
export const actions = {

    updateCategory: async ({ request, fetch }) => {

        const formData = await request.formData();

        const transactionId = formData.get("transactionId");
        const categoryId = formData.get("categoryId");

        await fetch(
            `http://127.0.0.1:8000/transactions/${transactionId}/category?category_id=${categoryId}`,
            { method: "PUT" }
        );

        return { success: true };
    }

};