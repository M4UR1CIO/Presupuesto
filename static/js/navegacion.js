document.addEventListener("DOMContentLoaded", function () {
    const contentDiv = document.querySelector(".content");

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", async function (event) {
            event.preventDefault();

            const url = this.getAttribute("data-url");

            try {
                const response = await fetch(url, { 
                    method: "GET", 
                    credentials: "include",
                    headers: { "X-Requested-With": "XMLHttpRequest" } // Indica que es AJAX
                });

                if (!response.ok) throw new Error("Error al cargar la página");

                const newContent = await response.text();
                contentDiv.innerHTML = newContent;  // Reemplaza solo el bloque content
            } catch (error) {
                console.error(error);
                alert("No se pudo cargar la sección.");
            }
        });
    });
});
