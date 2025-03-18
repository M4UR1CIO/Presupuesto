document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
        document.getElementById("error-message").innerText = "Por favor, completa todos los campos";
        document.getElementById("error-message").style.display = "block";
        return;
    }

    fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            // Almacenar el token en el localStorage
            localStorage.setItem('access_token', data.access_token);
            window.location.href = "/perfil";  // Redirigir al perfil
        } else {
            document.getElementById("error-message").innerText = data.msg;
            document.getElementById("error-message").style.display = "block";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("error-message").innerText = "Ocurrió un error al iniciar sesión.";
        document.getElementById("error-message").style.display = "block";
    });
});
