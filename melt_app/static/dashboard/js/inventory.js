document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".stock-badge").forEach(function (badge) {
        badge.title = badge.textContent.trim();
    });

});