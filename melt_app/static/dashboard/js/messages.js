document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".message-card").forEach(function (card) {

        card.addEventListener("mouseenter", function () {
            card.style.transform = "translateY(-3px)";
        });

        card.addEventListener("mouseleave", function () {
            card.style.transform = "translateY(0)";
        });

        card.style.transition = "transform .2s ease";
    });

});