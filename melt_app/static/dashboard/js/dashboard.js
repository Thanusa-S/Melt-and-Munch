document.addEventListener("DOMContentLoaded", function () {

    // Add a small hover effect to dashboard cards
    document.querySelectorAll(".stat-card").forEach(function (card) {

        card.addEventListener("mouseenter", function () {
            card.style.transform = "translateY(-5px)";
        });

        card.addEventListener("mouseleave", function () {
            card.style.transform = "translateY(0)";
        });

        card.style.transition = "transform .25s ease";
    });

});