
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");
    const errorBox = document.getElementById("loginError");

    if (!form) return;

    const inputs = Array.from(
        form.querySelectorAll(
            "input:not([type='hidden']):not([type='submit']):not([type='checkbox'])"
        )
    );

    const submitButton = form.querySelector(".auth-submit");

    function clearErrors() {
        errorBox.textContent = "";

        inputs.forEach(function (input) {
            input.classList.remove("invalid");
            input.removeAttribute("aria-invalid");
        });
    }

    inputs.forEach(function (input) {
        input.addEventListener("input", function () {
            input.classList.remove("invalid");
            input.removeAttribute("aria-invalid");
            errorBox.textContent = "";
        });
    });

    form.addEventListener("submit", function (event) {
        clearErrors();

        const emptyInput = inputs.find(function (input) {
            return input.required && !input.value.trim();
        });

        if (emptyInput) {
            event.preventDefault();

            emptyInput.classList.add("invalid");
            emptyInput.setAttribute("aria-invalid", "true");

            errorBox.textContent =
                "Please fill in " +
                (emptyInput.labels?.[0]?.textContent || "the required field") +
                ".";

            emptyInput.focus();
            return;
        }

        const emailInput = inputs.find(function (input) {
            return input.type === "email" && input.value.trim();
        });

        if (emailInput && !emailInput.validity.valid) {
            event.preventDefault();
            emailInput.classList.add("invalid");
            emailInput.setAttribute("aria-invalid", "true");
            errorBox.textContent = "Please enter a valid email address.";
            emailInput.focus();
            return;
        }

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.querySelector("span").textContent = "One sweet moment...";
        }
    });

    
const passwordInput = form.querySelector(
    'input[name="password"], input[name="password1"]'
);

const togglePassword = document.getElementById("togglePassword");
const eyeIcon = document.getElementById("eyeIcon");

if (passwordInput && togglePassword && eyeIcon) {
    togglePassword.addEventListener("click", function () {
        const isHidden = passwordInput.type === "password";

        passwordInput.type = isHidden ? "text" : "password";

        togglePassword.setAttribute(
            "aria-label",
            isHidden ? "Hide password" : "Show password"
        );

        togglePassword.setAttribute(
            "aria-pressed",
            String(isHidden)
        );

        eyeIcon.innerHTML = isHidden
            ? '<path d="M3 3l18 18"/><path d="M10.6 10.6a2 2 0 002.8 2.8"/><path d="M9.9 5.2A10.8 10.8 0 0112 5c6.4 0 10 7 10 7a16 16 0 01-3.1 3.9"/><path d="M6.6 6.6C3.6 8.4 2 12 2 12s3.6 7 10 7c1 0 2-.2 2.9-.5"/>'
            : '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>';
    });
}

});
