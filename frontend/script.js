const API = "http://localhost:5000";

async function cargarMapa() {
  const res = await fetch(`${API}/mapa`);
  const mapa = await res.json();
  const divMapa = document.getElementById("mapa");
  divMapa.innerHTML = "";

  mapa.forEach(fila => {
    const filaDiv = document.createElement("div");
    filaDiv.classList.add("fila");
    fila.forEach(celda => {
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
    alert("Seleccione una ubicación del mapa.");
    return;
  }

  const res = await fetch(`${API}/registrar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos)
  });

  const resultado = await res.json();
  if (res.ok) {
    alert("Vehículo registrado con éxito");
    cargarMapa();
    e.target.reset();
  } else {
    alert(resultado.error);
  }
});

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
    alert(resultado.error);
  }
});

cargarMapa();
