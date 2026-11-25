
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contactForm");
    const errorBox = document.getElementById("contactError");
    const submitButton = document.getElementById("contactSubmit");

    if (!form || !errorBox) return;

    const fields = Array.from(
        form.querySelectorAll("input, textarea, select")
    ).filter(function (field) {
        return !["hidden", "submit", "button"].includes(field.type);
    });

    function clearFieldError(field) {
        field.classList.remove("invalid");
        field.removeAttribute("aria-invalid");
    }

    fields.forEach(function (field) {
        field.addEventListener("input", function () {
            clearFieldError(field);
            errorBox.textContent = "";
        });

        field.addEventListener("change", function () {
            clearFieldError(field);
            errorBox.textContent = "";
        });
    });

    form.addEventListener("submit", function (event) {
        errorBox.textContent = "";

        const invalidField = fields.find(function (field) {
            if (!field.required) return false;

            if (field.type === "checkbox") {
                return !field.checked;
            }

            return !field.value.trim();
        });

        if (invalidField) {
            event.preventDefault();

            invalidField.classList.add("invalid");
            invalidField.setAttribute("aria-invalid", "true");

            const label = form.querySelector(
                'label[for="' + invalidField.id + '"]'
            );

            errorBox.textContent =
                "Please fill in " +
                (label ? label.textContent.replace("*", "").trim() : "this field") +
                ".";

            invalidField.focus();
            return;
        }

        const emailField = fields.find(function (field) {
            return field.type === "email" && field.value.trim();
        });

        if (emailField && !emailField.validity.valid) {
            event.preventDefault();

            emailField.classList.add("invalid");
            emailField.setAttribute("aria-invalid", "true");
            errorBox.textContent = "Please enter a valid email address.";
            emailField.focus();
            return;
        }

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.querySelector("span").textContent = "Sending your sweetness...";
        }
    });

    // Scroll smoothly to the message form when a flavour idea link is clicked.
    document.querySelectorAll('a[href="#contactForm"]').forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            form.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

            const firstField = fields[0];

            if (firstField) {
                window.setTimeout(function () {
                    firstField.focus({ preventScroll: true });
                }, 400);
            }
        });
    });
});
