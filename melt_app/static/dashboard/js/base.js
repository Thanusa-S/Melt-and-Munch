document.addEventListener("DOMContentLoaded", function () {

    const menuToggle = document.getElementById("menuToggle");
    const sidebar = document.getElementById("sidebar");

    if (menuToggle && sidebar) {
        menuToggle.addEventListener("click", function () {
            sidebar.classList.toggle("open");
        });
    }

    // Highlight the active sidebar page
    const currentPath = window.location.pathname;

    document.querySelectorAll(".side-link").forEach(function (link) {
        if (link.pathname === currentPath) {
            link.classList.add("active");
        }
    });

    // Automatically hide success messages
    document.querySelectorAll(".alert").forEach(function (alert) {
        window.setTimeout(function () {
            alert.style.transition = "opacity .4s";
            alert.style.opacity = "0";
            window.setTimeout(() => alert.remove(), 400);
        }, 4500);
    });

});