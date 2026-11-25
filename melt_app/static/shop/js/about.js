
document.addEventListener("DOMContentLoaded", function () {
    // Reveal sections as they enter the screen.
    const revealItems = document.querySelectorAll(
        ".story-section, .value-card, .ambience-card, .about-cta"
    );

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            function (entries, currentObserver) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        currentObserver.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12
            }
        );

        revealItems.forEach(function (item, index) {
            item.classList.add("about-reveal");
            item.style.transitionDelay =
                (index % 3) * 100 + "ms";

            observer.observe(item);
        });
    }

    // Smooth scrolling for links that point to sections on this page.
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
        link.addEventListener("click", function (event) {
            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") return;

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

    // Give the gallery cards a small interactive highlight.
    document.querySelectorAll(".ambience-card").forEach(function (card) {
        card.addEventListener("click", function () {
            card.classList.toggle("gallery-selected");
        });
    });
});
