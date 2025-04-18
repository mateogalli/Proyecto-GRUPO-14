const API = "http://127.0.0.1:5000";

// Usuarios precargados
const usuarios = {
  bauti: "44243400",
  mateo: "40475261",
  alvaro: "43402735",
  mati: "43876629"
};

// Mostrar perfil del usuario logueado
function mostrarPerfil() {
  const usuario = localStorage.getItem("usuarioLogueado");
  if (usuario) {
    const foto = `img/${usuario}.jpg`;
    document.getElementById("fotoUsuario").src = foto;
    document.getElementById("nombreUsuario").innerText = usuario;
    document.getElementById("perfilUsuario").style.display = "flex";
  }
}

// Login
document.getElementById("loginForm").addEventListener("submit", (event) => {
  event.preventDefault();

  const usuario = document.getElementById("usuario").value;
  const contraseña = document.getElementById("password").value;

  if (usuarios[usuario] === contraseña) {
    localStorage.setItem("usuarioLogueado", usuario);
    document.getElementById("loginContainer").style.display = "none";
    document.getElementById("mainContent").style.display = "flex";
    mostrarPerfil();
    cargarMapa();
  } else {
    document.getElementById("loginError").style.display = "block";
  }
});

// Cargar mapa
async function cargarMapa() {
  const res = await fetch(`${API}/mapa`);
  const mapa = await res.json();
  const divMapa = document.getElementById("mapa");
  divMapa.innerHTML = "";

  mapa.forEach((fila) => {
    const filaDiv = document.createElement("div");
    filaDiv.classList.add("fila");

    fila.forEach((celda) => {
      const celdaBtn = document.createElement("button");
      celdaBtn.textContent = celda.ubicacion;
      celdaBtn.className = celda.estado === "ocupado" ? "ocupado" : "libre";
      celdaBtn.disabled = celda.estado === "ocupado";

      if (celda.estado === "libre") {
        celdaBtn.addEventListener("click", () => {
          document.getElementById("ubicacion").value = celda.ubicacion;
        });
      }

      filaDiv.appendChild(celdaBtn);
    });

    divMapa.appendChild(filaDiv);
  });
}

// Registrar vehículo
document.getElementById("registro-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const datos = {
    documento: document.getElementById("documento").value,
    tipo: document.getElementById("tipo").value,
    tiempo: document.getElementById("tiempo").value,
    pago: document.getElementById("pago").value,
    lavado: document.getElementById("lavado").value,
    ubicacion: document.getElementById("ubicacion").value
  };

  if (!datos.ubicacion) {
    alert("Seleccione una ubicación en el mapa.");
    return;
  }

  const res = await fetch(`${API}/registrar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos)
  });

  const resultado = await res.json();
  if (res.ok) {
    alert("Vehículo registrado con éxito.");
    cargarMapa();
    e.target.reset();
    document.getElementById("ubicacion").value = "";
  } else {
    alert(resultado.error || "Error al registrar.");
  }
});

// Retirar vehículo
document.getElementById("retiro-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const documento = document.getElementById("retiro-dni").value;

  const res = await fetch(`${API}/retirar`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ documento })
  });

  const resultado = await res.json();
  if (res.ok) {
    alert("Vehículo retirado correctamente.");
    cargarMapa();
    e.target.reset();
  } else {
    alert(resultado.error || "Error al retirar vehículo.");
  }
});

// Mostrar perfil si ya estaba logueado
window.addEventListener("DOMContentLoaded", () => {
  const logueado = localStorage.getItem("usuarioLogueado");
  if (logueado) {
    document.getElementById("loginContainer").style.display = "none";
    document.getElementById("mainContent").style.display = "flex";
    mostrarPerfil();
    cargarMapa();
  }
});
