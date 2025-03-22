document.addEventListener("DOMContentLoaded", async function () {
    const tablaPresupuestos = document.querySelector("#tabla-presupuestos tbody");
    const modal = document.querySelector("#modalEditar");
    const cerrarModal = document.querySelector(".close");

    // Campos del formulario del modal
    const idPresupuestoInput = document.querySelector("#presupuesto-id");
    const nombreInput = document.querySelector("#nombre");
    const descripcionInput = document.querySelector("#descripcion");
    const totalInput = document.querySelector("#total");
    const formEditarPresupuesto = document.querySelector("#form-editar-presupuesto");

    async function cargarPresupuestos() {
        try {
            const response = await fetch("presupuesto/presupuestos", {
                method: "GET",
                credentials: "include",
                headers: { "Content-Type": "application/json" }
            });

            if (!response.ok) throw new Error("Error al obtener los presupuestos");

            const presupuestos = await response.json();
            tablaPresupuestos.innerHTML = ""; // Limpia la tabla antes de llenarla

            if (presupuestos.length === 0) {
                // Mostrar mensaje cuando no haya presupuestos
                tablaPresupuestos.innerHTML = `
                    <tr>
                        <td colspan="6" style="text-align: center; font-weight: bold; padding: 10px;">
                            No hay presupuestos registrados.
                        </td>
                    </tr>
                `;
                return;
            }

            presupuestos.forEach(p => {
                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td>${p.numero_presupuesto}</td>
                    <td>${p.nombre}</td>
                    <td>${p.descripcion}</td>
                    <td>${p.total}</td>
                    <td>${new Date(p.fecha_creacion).toLocaleDateString()}</td>
                    <td>
                        <button class="btn-editar" data-id="${p.id}" data-nombre="${p.nombre}" data-descripcion="${p.descripcion}" data-total="${p.total}">
                            <i class="fa-solid fa-pen-to-square"></i>
                        </button>
                        <button class="btn-eliminar" data-id="${p.id}">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </td>
                `;
                tablaPresupuestos.appendChild(fila);
            });

            // Agregar eventos a los botones de eliminar y editar
            document.querySelectorAll(".btn-eliminar").forEach(btn => {
                btn.addEventListener("click", eliminarPresupuesto);
            });

            document.querySelectorAll(".btn-editar").forEach(btn => {
                btn.addEventListener("click", abrirModalEdicion);
            });

        } catch (error) {
            console.error(error);
            alert("No se pudieron cargar los presupuestos");
        }
    }

    async function eliminarPresupuesto(event) {
        const id = event.currentTarget.dataset.id;
        if (!confirm("¿Seguro que deseas eliminar este presupuesto?")) return;

        try {
            const response = await fetch(`presupuesto/presupuestos/${id}`, {
                method: "DELETE",
                credentials: "include",
                headers: { "Content-Type": "application/json" }
            });

            if (!response.ok) throw new Error("Error al eliminar presupuesto");

            alert("Presupuesto eliminado exitosamente");
            cargarPresupuestos(); // Recargar lista
        } catch (error) {
            console.error(error);
            alert("No se pudo eliminar el presupuesto");
        }
    }

    function abrirModalEdicion(event) {
        // Obtener datos del presupuesto desde los atributos del botón
        const id = event.currentTarget.dataset.id;
        const nombre = event.currentTarget.dataset.nombre;
        const descripcion = event.currentTarget.dataset.descripcion;
        const total = event.currentTarget.dataset.total;

        // Llenar los campos del modal con los datos del presupuesto
        idPresupuestoInput.value = id;
        nombreInput.value = nombre;
        descripcionInput.value = descripcion;
        totalInput.value = total;

        // Mostrar el modal
        modal.style.display = "block";
    }

    // Cerrar el modal al hacer clic en la "X"
    cerrarModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Cerrar el modal si se hace clic fuera de él
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    formEditarPresupuesto.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evitar que se recargue la página

        const id = idPresupuestoInput.value;
        const datosActualizados = {
            nombre: nombreInput.value,
            descripcion: descripcionInput.value,
            total: totalInput.value
        };

        try {
            const response = await fetch(`presupuesto/presupuestos/${id}`, {
                method: "PUT",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(datosActualizados)
            });

            if (!response.ok) throw new Error("Error al actualizar el presupuesto");

            alert("Presupuesto actualizado exitosamente");
            modal.style.display = "none";
            cargarPresupuestos(); // Recargar la lista
        } catch (error) {
            console.error(error);
            alert("No se pudo actualizar el presupuesto");
        }
    });

    cargarPresupuestos();
});
