document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".delete-form").forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this ice cream?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });

});