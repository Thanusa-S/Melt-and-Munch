document.addEventListener("DOMContentLoaded", () => {
    const search = document.getElementById("productSearch");
    const category = document.getElementById("categoryFilter");
    const cards = [...document.querySelectorAll(".filterable-card")];
    const noMatches = document.getElementById("noMatches");

    function filterCards() {
        const query = (search?.value || "").trim().toLowerCase();
        const selected = category?.value || "";
        let visible = 0;

        cards.forEach(card => {
            const matchesName = card.dataset.name.includes(query);
            const matchesCategory =
                !selected || card.dataset.category === selected;

            const matches = matchesName && matchesCategory;

            card.hidden = !matches;

            if (matches) {
                visible++;
            }
        });

        if (noMatches) {
            noMatches.hidden = visible > 0;
        }
    }

    search?.addEventListener("input", filterCards);

    category?.addEventListener("change", () => {
        document.getElementById("filterForm").requestSubmit();
    });

    filterCards();
});