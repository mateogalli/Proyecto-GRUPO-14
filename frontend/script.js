const API = "http://localhost:5000";

async function cargarMapa() {
  const res = await fetch(`${API}/mapa`);
  const mapa = await res.json();
  const div = document.getElementById("mapa");
  div.innerHTML = "";

  mapa.forEach(fila => {
    const row = document.createElement("div");
    row.classList.add("fila");
    fila.forEach(celda => {
      const btn = document.createElement("button");
      btn.textContent = celda.ubicacion;
      btn.className = celda.estado;
      btn.disabled = celda.estado === "ocupado";
      if (celda.estado === "libre") {
        btn.addEventListener("click", () => {
          document.getElementById("ubicacion").value = celda.ubicacion;
          document.querySelectorAll("#mapa button").forEach(b => b.classList.remove("seleccionado"));
          btn.classList.add("seleccionado");
        });
      }
      row.appendChild(btn);
    });
    div.appendChild(row);
  });
}

document.getElementById("registro-form").addEventListener("submit", async e => {
  e.preventDefault();
  const documento = document.getElementById("documento").value;
  const tipo = document.getElementById("tipo").value;
  const pago = document.getElementById("pago").value;
  const lavado = document.getElementById("lavado").checked ? "SI" : "NO";
  const ubicacion = document.getElementById("ubicacion").value;

  if (!ubicacion) {
    alert("Seleccione una ubicación del mapa.");
    return;
  }

  const res = await fetch(`${API}/registrar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ documento, tipo, pago, lavado, ubicacion })
  });
  const data = await res.json();
  if (res.ok) {
    document.getElementById("resultado").textContent =
      `Entrada registrada: ${data.entry_time} en ${data.ubicacion}`;
    document.getElementById("registro-form").reset();
    cargarMapa();
  } else {
    alert(data.error);
  }
});

document.getElementById("retiro-form").addEventListener("submit", async e => {
  e.preventDefault();
  const documento = document.getElementById("retiro-dni").value;
  const res = await fetch(`${API}/retirar`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ documento })
  });
  const data = await res.json();
  if (res.ok) {
    if (data.pago === "QR") {
      mostrarQR(data.documento);
    } else {
      document.getElementById("resultado").innerHTML =
        `<p>Entrada: ${data.entry_time}</p>
        <p>Salida: ${data.exit_time}</p>
        <p>Horas: ${data.horas}</p>
        <p><strong>Total a pagar: $${data.costo}</strong></p>`;
    }
    document.getElementById("retiro-form").reset();
    cargarMapa();
  } else {
    alert(data.error);
  }
});

function mostrarQR(documento) {
  document.getElementById("app-content").style.display = "none";
  document.getElementById("qr-retiro-screen").style.display = "block";
  document.getElementById("qr-retiro-img").src = `QR/${documento}.png`;
}

function volver() {
  document.getElementById("qr-retiro-screen").style.display = "none";
  document.getElementById("app-content").style.display = "block";
  document.getElementById("retiro-form").reset();
  document.getElementById("resultado").innerHTML = "";
}

cargarMapa();
