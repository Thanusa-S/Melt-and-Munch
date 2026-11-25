
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("checkoutForm");
    const error = document.getElementById("checkoutError");

    if (!form) return;

    form.addEventListener("submit", event => {
        const orderType = form.querySelector(
            'input[name="order_type"]:checked'
        )?.value;

        const fields = [
            ...form.querySelectorAll("input, textarea")
        ].filter(field =>
            field.type !== "hidden" &&
            field.type !== "radio" &&
            field.name !== "csrfmiddlewaretoken"
        );

        // Required fields
        const requiredFields = fields.filter(field => {
            const optionalForTakeaway = [
                "address",
                "city",
                "postal_code"
            ];

            if (
                orderType === "takeaway" &&
                optionalForTakeaway.includes(field.name)
            ) {
                return false;
            }

            return true;
        });

        const missing = requiredFields.find(
            field => !field.value.trim()
        );

        const email = form.querySelector('input[type="email"]');

        if (missing) {
            event.preventDefault();
            error.textContent = "Please complete all required fields.";
            missing.focus();
            return;
        }

        if (
            email &&
            !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)
        ) {
            event.preventDefault();
            error.textContent = "Please enter a valid email address.";
            email.focus();
            return;
        }

        error.textContent = "";
    });
});
