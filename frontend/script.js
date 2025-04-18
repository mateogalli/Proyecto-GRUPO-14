// Usuarios precargados
const usuarios = {
    bauti: "44243400",
    mateo: "40475261",
    alvaro: "43402735"
};

// Mostrar perfil del usuario logueado
function mostrarPerfil() {
    const usuario = localStorage.getItem("usuarioLogueado");
    if (usuario) {
        const nombre = usuario;
        const foto = `img/${usuario}.jpg`; // La imagen debe estar en la carpeta /img con ese nombre

        document.getElementById("fotoUsuario").src = foto;
        document.getElementById("nombreUsuario").innerText = nombre;
        document.getElementById("perfilUsuario").style.display = "flex";
    }
}

// Login
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const usuario = document.getElementById("usuario").value;
    const contraseña = document.getElementById("password").value;

    if (usuarios[usuario] === contraseña) {
        localStorage.setItem("usuarioLogueado", usuario);
        document.getElementById("loginContainer").style.display = "none";
        document.getElementById("formEstacionamiento").style.display = "inline-block";
        document.querySelector("h1").style.display = "block";
        mostrarPerfil();
    } else {
        document.getElementById("loginError").style.display = "block";
    }
});

// Enviar datos del formulario
document.getElementById("formEstacionamiento").addEventListener("submit", function(event) {
    event.preventDefault();

    let documento = document.getElementById("documento").value;
    let vehiculo = document.getElementById("vehiculo").value;
    let tiempo = document.getElementById("tiempo").value;
    let ubicacion = document.getElementById("ubicacion").value;
    let pago = document.getElementById("pago").value;
    let lavado = document.getElementById("lavado").value;

    let datos = {
        documento: documento,
        vehiculo: vehiculo,
        tiempo: tiempo,
        ubicacion: ubicacion,
        pago: pago,
        lavado: lavado
    };

    fetch("http://127.0.0.1:5000/registrar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            alert("Registro exitoso: " + JSON.stringify(data));
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

// Al cargar la página
window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("formEstacionamiento").style.display = "none";
    document.querySelector("h1").style.display = "none";
    mostrarPerfil();
});
