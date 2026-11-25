
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");
    const errorBox = document.getElementById("registerError");
    const submitButton = document.getElementById("registerSubmit");

    if (!form || !errorBox) return;

    // Show/hide password using the eye buttons.
    form.querySelectorAll(".password-toggle").forEach(function (button) {
        button.addEventListener("click", function () {
            const wrapper = button.closest(".register-password-wrap");
            const input = wrapper ? wrapper.querySelector("input") : null;
            const icon = button.querySelector(".eye-icon");

            if (!input) return;

            const showPassword = input.type === "password";
            input.type = showPassword ? "text" : "password";

            button.setAttribute(
                "aria-label",
                showPassword ? "Hide password" : "Show password"
            );
            button.setAttribute("aria-pressed", String(showPassword));

            if (icon) {
                icon.innerHTML = showPassword
                    ? '<path d="M3 3l18 18"/><path d="M10.6 10.6a2 2 0 002.8 2.8"/><path d="M9.9 5.2A10.8 10.8 0 0112 5c6.4 0 10 7 10 7a16 16 0 01-3.1 3.9"/><path d="M6.6 6.6C3.6 8.4 2 12 2 12s3.6 7 10 7c1 0 2-.2 2.9-.5"/>'
                    : '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>';
            }
        });
    });

    // Clear the visual error when a field is edited.
    const fields = Array.from(
        form.querySelectorAll("input, select, textarea")
    ).filter(function (field) {
        return !["hidden", "submit", "button"].includes(field.type);
    });

    fields.forEach(function (field) {
        field.addEventListener("input", function () {
            field.classList.remove("invalid");
            field.removeAttribute("aria-invalid");
            errorBox.textContent = "";
        });

        field.addEventListener("change", function () {
            field.classList.remove("invalid");
            field.removeAttribute("aria-invalid");
            errorBox.textContent = "";
        });
    });

    form.addEventListener("submit", function (event) {
        errorBox.textContent = "";

        // Check required fields.
        const emptyField = fields.find(function (field) {
            if (!field.required) return false;

            if (field.type === "checkbox") {
                return !field.checked;
            }

            return !field.value.trim();
        });

        if (emptyField) {
            event.preventDefault();
            showError(emptyField, "Please complete this field.");
            return;
        }

        // Check email format if an email input exists.
        const emailField = fields.find(function (field) {
            return field.type === "email" && field.value.trim();
        });

        if (emailField && !emailField.validity.valid) {
            event.preventDefault();
            showError(emailField, "Please enter a valid email address.");
            return;
        }

        // Check matching passwords when using Django's standard UserCreationForm.
        const password1 = form.querySelector('input[name="password1"]');
        const password2 = form.querySelector('input[name="password2"]');

        if (
            password1 &&
            password2 &&
            password1.value !== password2.value
        ) {
            event.preventDefault();
            showError(password2, "Your passwords do not match.");
            return;
        }

        // Let Django handle the POST request.
        if (submitButton) {
            submitButton.disabled = true;
            const text = submitButton.querySelector("span");

            if (text) {
                text.textContent = "Creating your account...";
            }
        }
    });

    function showError(field, message) {
        field.classList.add("invalid");
        field.setAttribute("aria-invalid", "true");
        errorBox.textContent = message;
        field.focus();

        field.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    }
});
