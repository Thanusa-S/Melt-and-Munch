// document.addEventListener("DOMContentLoaded", () => {
//     document.querySelectorAll(".product-card").forEach((card, index) => {
//         card.style.animation =
//             `pageIn .45s ease ${index * 70}ms both`;
//     });
// });


document.addEventListener("DOMContentLoaded", function () {
    // ANIMATION 1: Reveal sections and cards while scrolling
    const revealElements = document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -35px 0px"
            }
        );

        revealElements.forEach(function (element, index) {
            // Stagger nearby cards for a smoother entrance
            if (
                element.classList.contains("product-card") ||
                element.classList.contains("flavour-category") ||
                element.classList.contains("love-card")
            ) {
                element.style.transitionDelay =
                    `${(index % 4) * 90}ms`;
            }

            revealObserver.observe(element);
        });
    } else {
        // Fallback for older browsers
        revealElements.forEach(function (element) {
            element.classList.add("is-visible");
        });
    }

    // ANIMATION 2: Gentle hero movement with the pointer
    const hero = document.querySelector(".hero");
    const heroArt = document.querySelector(".hero-art");
    const heroEmoji = document.querySelector(".hero-emoji");

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (hero && heroArt && heroEmoji && !reduceMotion) {
        hero.addEventListener("pointermove", function (event) {
            if (event.pointerType === "touch") return;

            const rect = hero.getBoundingClientRect();

            const x = (event.clientX - rect.left) / rect.width - 0.5;
            const y = (event.clientY - rect.top) / rect.height - 0.5;

            heroEmoji.style.setProperty(
                "--pointer-x",
                `${x * 8}px`
            );

            heroEmoji.style.setProperty(
                "--pointer-y",
                `${y * 8}px`
            );

            heroEmoji.style.filter =
                "drop-shadow(0 25px 18px rgba(75, 43, 68, 0.15))";
        });

        hero.addEventListener("pointerleave", function () {
            heroEmoji.style.setProperty("--pointer-x", "0px");
            heroEmoji.style.setProperty("--pointer-y", "0px");
            heroEmoji.style.filter =
                "drop-shadow(0 22px 16px rgba(75, 43, 68, 0.12))";
        });
    }

    // ANIMATION 3: Smooth hover feedback on flavour cards
    const flavourCards = document.querySelectorAll(".flavour-category");

    flavourCards.forEach(function (card) {
        card.addEventListener("pointerenter", function () {
            if (reduceMotion) return;

            const emoji = card.querySelector(".category-emoji");

            if (emoji) {
                emoji.style.transform = "rotate(-12deg) scale(1.12)";
            }
        });

        card.addEventListener("pointerleave", function () {
            const emoji = card.querySelector(".category-emoji");

            if (emoji) {
                emoji.style.transform = "";
            }
        });
    });
    


    // Show sections as they enter the screen.
    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12
            }
        );

        revealElements.forEach(function (element) {
            revealObserver.observe(element);
        });
    } else {
        revealElements.forEach(function (element) {
            element.classList.add("is-visible");
        });
    }

    // Keep the ice-cream photos responsive.
    document.querySelectorAll(
        ".promo-photo img, .empty-products img"
    ).forEach(function (image) {
        image.addEventListener("error", function () {
            image.style.display = "none";
            image.parentElement.style.background =
                "linear-gradient(135deg, #ffd5e5, #fff0bd)";
        });
    });
});


