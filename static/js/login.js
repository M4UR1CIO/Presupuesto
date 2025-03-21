document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
        mostrarError("Por favor, completa todos los campos");
        return;
    }

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include", // ✅ Asegura que se envíen y reciban cookies
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            window.location.href = "/sidebar"; // Redirigir al dashboard después del login
        } else {
            mostrarError(data.msg);
        }
    } catch (error) {
        console.error("Error:", error);
        mostrarError("Ocurrió un error al iniciar sesión.");
    }
});

// Función para mostrar errores
function mostrarError(mensaje) {
    const errorMessage = document.getElementById("error-message");
    errorMessage.innerText = mensaje;
    errorMessage.style.display = "block";
}
