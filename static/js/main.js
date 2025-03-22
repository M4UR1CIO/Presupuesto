document.addEventListener("DOMContentLoaded", function () {
    const logoutButton = document.querySelector(".button-logout");

    logoutButton.addEventListener("click", async function () {
        try {
            const response = await fetch("auth/logout", {
                method: "POST",
                credentials: "include", // ✅ Enviar cookies con la solicitud
                headers: {
                    "Content-Type": "application/json"
                }
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = "/"; // 🔄 Redirigir a la página de login
            } else {
                alert(`Error: ${data.msg}`);
            }
        } catch (error) {
            console.error("Error al cerrar sesión:", error);
            alert("Hubo un problema al cerrar la sesión.");
        }
    });
});
