document.addEventListener("DOMContentLoaded", function () {

    // Smooth scrolling
    document.querySelectorAll('a[href="#icecream-menu"], a[href="#flavours"]')
        .forEach(function (link) {

            link.addEventListener("click", function (event) {

                const targetId = this.getAttribute("href");
                const target = document.querySelector(targetId);

                if (target) {
                    event.preventDefault();

                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }
            });

        });


    // Product card reveal animation
    const cards = document.querySelectorAll(".ice-card");

    if ("IntersectionObserver" in window) {

        const observer = new IntersectionObserver(function (entries) {

            entries.forEach(function (entry) {

                if (entry.isIntersecting) {

                    entry.target.classList.add("ice-card-visible");

                    observer.unobserve(entry.target);
                }

            });

        }, {
            threshold: 0.12
        });

        cards.forEach(function (card) {
            observer.observe(card);
        });

    } else {

        cards.forEach(function (card) {
            card.classList.add("ice-card-visible");
        });

    }


    // Automatically submit when sorting changes
    const sortSelect = document.querySelector('select[name="sort"]');
    const filterForm = document.getElementById("iceFilterForm");

    if (sortSelect && filterForm) {

        sortSelect.addEventListener("change", function () {

            filterForm.requestSubmit();

        });

    }


    // Image fallback if an online photo fails to load
    document.querySelectorAll(".ice-card-image img, .flavour-image img, .happy-photo img")
        .forEach(function (img) {

            img.addEventListener("error", function () {

                this.style.display = "none";

                this.parentElement.classList.add("image-not-loaded");

            });

        });

});