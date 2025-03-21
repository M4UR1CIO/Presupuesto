document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");

    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const nombre = document.getElementById("nombre").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const response = await fetch("/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ nombre, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Usuario creado exitosamente");
            window.location.href = "/"; // Redirigir al login
        } else {
            alert("Error: " + data.msg);
        }
    });
});
