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
        alert("Registro exitoso: " + JSON.stringify(data));
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
