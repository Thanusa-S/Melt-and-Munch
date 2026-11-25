document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("navToggle");
    const nav = document.getElementById("navLinks");

    if (toggle && nav) {
        toggle.addEventListener("click", () => {
            nav.classList.toggle("open");
        });
    }

    document.querySelectorAll(".message").forEach(message => {
        setTimeout(() => {
            message.style.transition = "opacity .5s";
            message.style.opacity = "0";
        }, 4500);
    });
});