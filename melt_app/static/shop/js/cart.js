document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".cart-quantity input").forEach(input => {
        input.addEventListener("change", () => {
            let quantity = parseInt(input.value, 10);

            if (!Number.isInteger(quantity) || quantity < 0) {
                quantity = 0;
            }

            if (quantity > 99) {
                quantity = 99;
            }

            input.value = quantity;
        });
    });
});
function changeCartValue(button, change) {
    const selector = button.closest(".scoop-selector");
    const input = selector.querySelector(".cart-number");

    const min = parseInt(input.min);
    const max = parseInt(input.max);

    let value = parseInt(input.value) || min;

    value += change;

    if (value < min) value = min;
    if (value > max) value = max;

    input.value = value;
}