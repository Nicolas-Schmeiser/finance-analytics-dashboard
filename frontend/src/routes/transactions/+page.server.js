import { fail } from '@sveltejs/kit';

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

        const response = await fetch(
            `http://127.0.0.1:8000/transactions/${transactionId}/category?category_id=${categoryId}`,
            { method: "PUT" }
        );

        if (!response.ok) {
            return fail(response.status, {
                error: "Could not update category"
            });
        }

        return { success: true };
    },

    addTransaction: async ({ request, fetch }) => {

        const formData = await request.formData();

        const description = String(formData.get("description") ?? "").trim();
        const amount = Number(formData.get("amount"));
        const transactionDate = String(formData.get("date") ?? "");
        const categoryId = Number(formData.get("categoryId"));

        if (!description || Number.isNaN(amount) || !transactionDate || Number.isNaN(categoryId)) {
            return fail(400, {
                error: "Please provide all transaction fields."
            });
        }

        const response = await fetch("http://127.0.0.1:8000/transactions", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                description,
                amount,
                date: transactionDate,
                category_id: categoryId
            })
        });

        if (!response.ok) {
            return fail(response.status, {
                error: "Could not add transaction"
            });
        }

        const createdTransaction = await response.json();

        return {
            success: true,
            message: "Transaction added successfully.",
            transaction: createdTransaction
        };
    },

    deleteTransaction: async ({ request, fetch }) => {

        const formData = await request.formData();
        const transactionId = Number(formData.get("transactionId"));

        if (Number.isNaN(transactionId)) {
            return fail(400, {
                error: "Invalid transaction ID."
            });
        }

        const response = await fetch(
            `http://127.0.0.1:8000/transactions/${transactionId}`,
            { method: "DELETE" }
        );

        if (!response.ok) {
            return fail(response.status, {
                error: "Could not delete transaction"
            });
        }

        return {
            success: true,
            deletedTransactionId: transactionId
        };
    }

};