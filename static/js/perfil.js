document.addEventListener("DOMContentLoaded", async function () {
    try {
        const response = await fetch("/auth/perfil", {
            method: "GET",
            credentials: "include", // ✅ Enviar cookies con la solicitud
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Error al obtener los datos del perfil");
        }

        const usuario = await response.json();

        // Insertar datos en el HTML
        document.getElementById("nombre-usuario").textContent = usuario.nombre;
        document.getElementById("email-usuario").textContent = usuario.email;

        // Establecer valores en el modal
        document.getElementById("editar-nombre").value = usuario.nombre;
    } catch (error) {
        console.error("Error:", error);
        alert("No tienes sesión iniciada. Redirigiendo al login...");
        window.location.href = "/"; // 🔄 Redirige al login si no hay sesión
        return;
    }

    // Lógica del Modal de Edición
    const modal = document.getElementById("modalEditarPerfil");
    const btnCerrar = document.querySelector(".close");
    const btnAbrirModal = document.getElementById("btn-editar-perfil");
    const formEditarPerfil = document.getElementById("form-editar-perfil");

    // ✅ Abrir modal al hacer clic en el botón "Editar Perfil"
    btnAbrirModal.addEventListener("click", function () {
        modal.style.display = "block";
    });

    // ✅ Cerrar modal al hacer clic en la 'X'
    btnCerrar.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // ✅ Cerrar modal si se hace clic fuera del contenido
    window.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });

    // ✅ Manejo del formulario de edición
    formEditarPerfil.addEventListener("submit", async function (e) {
        e.preventDefault();
        
        const nuevoNombre = document.getElementById("editar-nombre").value.trim();
        const nuevaPassword = document.getElementById("editar-password").value.trim();
        const confirmarPassword = document.getElementById("editar-confirm-password").value.trim();

        if (nuevaPassword && nuevaPassword !== confirmarPassword) {
            alert("Las contraseñas no coinciden");
            return;
        }

        // Construcción de datos a enviar
        const datosActualizar = { nombre: nuevoNombre };
        if (nuevaPassword) {
            datosActualizar.password = nuevaPassword;
            datosActualizar.confirm_password = confirmarPassword;
        }

        try {
            const respuesta = await fetch("/auth/editar-perfil", {
                method: "PUT",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(datosActualizar)
            });

            const data = await respuesta.json();
            alert(data.msg);

            if (respuesta.ok) {
                modal.style.display = "none";
                document.getElementById("nombre-usuario").textContent = nuevoNombre; // Actualizar en la interfaz
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Error al actualizar el perfil.");
        }
    });
});
