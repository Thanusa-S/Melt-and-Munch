document.addEventListener("DOMContentLoaded", function () {

    const search = document.querySelector(".customer-search input");

    if (search) {
        search.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                search.value = "";
            }
        });
    }

});