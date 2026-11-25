document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("icecreamForm");

    if (form) {
        form.addEventListener("submit", function (event) {

            const button = form.querySelector(".save-btn");

            if (form.checkValidity() && button) {
                button.textContent = "Saving...";
                button.disabled = true;
            }

        });
    }

});