document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-crear-presupuesto");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evita que la página se recargue

        const nombre = document.getElementById("nombre_presupuesto").value.trim();
        const descripcion = document.getElementById("descripcion").value.trim(); // ✅ Corregido
        const costo = document.getElementById("costo").value.trim();

        if (!nombre || !costo) {
            alert("El nombre y el costo total son obligatorios.");
            return;
        }

        const presupuestoData = {
            nombre: nombre,
            descripcion: descripcion,
            total: parseFloat(costo)
        };

        try {
            const response = await fetch("/presupuesto/presupuestos", { // ✅ Ruta corregida
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(presupuestoData)
            });

            const data = await response.json();

            if (response.ok) {
                alert("Presupuesto creado con éxito");
                window.location.reload(); // Recargar la página después de la creación
            } else {
                alert(`Error: ${data.msg}`);
            }
        } catch (error) {
            console.error("Error en la solicitud:", error);
            alert("Hubo un problema al crear el presupuesto.");
        }
    });
});
