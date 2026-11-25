document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("quantity");
    const minus = document.getElementById("qtyMinus");
    const plus = document.getElementById("qtyPlus");
    const form = document.getElementById("detailForm");

    minus?.addEventListener("click", () => {
        const current = parseInt(input.value, 10) || 1;
        input.value = Math.max(1, current - 1);
    });

    plus?.addEventListener("click", () => {
        const current = parseInt(input.value, 10) || 1;
        input.value = Math.min(99, current + 1);
    });

    form?.addEventListener("submit", event => {
        const quantity = Number(input.value);

        if (!Number.isInteger(quantity) ||
            quantity < 1 || quantity > 99) {
            event.preventDefault();
            alert("Please choose between 1 and 99 scoops.");
            input.focus();
        }
    });
});