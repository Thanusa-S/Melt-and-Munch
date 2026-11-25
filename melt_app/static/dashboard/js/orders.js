document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".status-form").forEach(function (form) {

        form.addEventListener("submit", function () {

            const button = form.querySelector("button");

            if (button) {
                button.textContent = "Saving...";
                button.disabled = true;
            }

        });

    });

});