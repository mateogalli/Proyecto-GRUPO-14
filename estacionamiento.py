# Lista para almacenar la información de los autos en el estacionamiento
estacionamiento = {}

# Mapa del estacionamiento (15x15 con filas A-O y columnas 1-15)
filas = "ABCDEFGHIJKLMNO"
columnas = list(range(1, 16))
mapa = [[None for _ in columnas] for _ in filas]

# Función para mostrar el mapa del estacionamiento
def mostrar_mapa():
    print("\nMapa del estacionamiento:")
    print("   " + "  ".join(map(str, columnas)))
    for i, fila in enumerate(filas):
        fila_mostrada = [fila] + [("X" if mapa[i][j] else "-") for j in range(len(columnas))]
        print("  ".join(map(str, fila_mostrada)))
    print("\n(X = ocupado, - = libre)\n")

# Función para registrar la entrada de un vehículo
def registrar_entrada():
    documento = input("Ingrese su documento: ")

    if documento in estacionamiento:
        print("Ya hay un vehículo registrado con este documento.\n")
        return

    print("\nTipos de vehículo:")
    print("1. AUTO\n2. MOTO\n3. CAMIONETA")
    tipo_vehiculo = input("Seleccione el número de su tipo de vehículo: ")

    tipos = {"1": "AUTO", "2": "MOTO", "3": "CAMIONETA"}
    if tipo_vehiculo not in tipos:
        print("Selección inválida.\n")
        return
    
    tipo_vehiculo = tipos[tipo_vehiculo]

    print("\nDuración de estadía:")
    print("1. 1 hora\n2. 2 horas\n3. 3 horas\n4. 4 horas\n5. 5 horas\n6. 6 horas\n7. ESTADÍA")
    tiempo = input("Seleccione el número de horas: ")

    tiempos = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": "ESTADÍA"}
    if tiempo not in tiempos:
        print("Selección inválida.\n")
        return

    tiempo = tiempos[tiempo]

    mostrar_mapa()
    ubicacion = input("Ingrese su ubicación (Ejemplo: B5): ").upper()

    if len(ubicacion) < 2 or ubicacion[0] not in filas or not ubicacion[1:].isdigit():
        print("Ubicación inválida.\n")
        return

    fila, columna = ubicacion[0], int(ubicacion[1:])
    fila_idx, columna_idx = filas.index(fila), columna - 1

    if mapa[fila_idx][columna_idx] is not None:
        print("El lugar ya está ocupado.\n")
        return

    print("\nMétodos de pago:")
    print("1. EFECTIVO\n2. QR")
    metodo_pago = input("Seleccione el número de su método de pago: ")

    metodos = {"1": "EFECTIVO", "2": "QR"}
    if metodo_pago not in metodos:
        print("Selección inválida.\n")
        return

    metodo_pago = metodos[metodo_pago]

    # Calcular costo de estacionamiento
    costo = 2000 * tiempo if tiempo != "ESTADÍA" else 15000

    # Servicio de lavado opcional
    print("\n¿Desea lavar su vehículo?")
    print("1. Sí\n2. No")
    lavado = input("Seleccione una opción: ")

    costo_lavado = 0
    if lavado == "1":
        lavado_precios = {"MOTO": 4000, "AUTO": 10000, "CAMIONETA": 15000}
        costo_lavado = lavado_precios[tipo_vehiculo]
    
    total_pagar = costo + costo_lavado

    # Registrar vehículo en el estacionamiento
    estacionamiento[documento] = {
        "tipo": tipo_vehiculo,
        "tiempo": tiempo,
        "ubicacion": ubicacion,
        "pago": metodo_pago,
        "costo": total_pagar
    }
    mapa[fila_idx][columna_idx] = documento  # Marcar lugar ocupado

    print("\n✅ Vehículo registrado con éxito.")
    print(f"📌 Total a pagar: ${total_pagar}\n")

# Función para registrar la salida de un vehículo
def registrar_salida():
    documento = input("Ingrese su documento para retirar su vehículo: ")

    if documento not in estacionamiento:
        print("No hay un vehículo registrado con este documento.\n")
        return

    ubicacion = estacionamiento[documento]["ubicacion"]
    fila, columna = ubicacion[0], int(ubicacion[1:])
    fila_idx, columna_idx = filas.index(fila), columna - 1

    mapa[fila_idx][columna_idx] = None  # Liberar el lugar
    estacionamiento.pop(documento)  # Eliminar del registro

    print("\n✅ Vehículo retirado. Gracias por su visita.\n")

# Función para mostrar el ticket
def mostrar_ticket():
    documento = input("Ingrese su documento para ver su ticket: ")

    if documento not in estacionamiento:
        print("No hay un vehículo registrado con este documento.\n")
        return

    datos = estacionamiento[documento]
    print("\n📄 TICKET DE ESTACIONAMIENTO")
    print(f"🆔 Documento: {documento}")
    print(f"🚗 Tipo de vehículo: {datos['tipo']}")
    print(f"📍 Ubicación: {datos['ubicacion']}")
    print(f"⏳ Tiempo: {datos['tiempo']} horas" if datos["tiempo"] != "ESTADÍA" else "⏳ Tiempo: ESTADÍA")
    print(f"💳 Método de pago: {datos['pago']}")
    print(f"💰 Monto a pagar: ${datos['costo']}")
    print("✅ Gracias por su visita.\n")

# Menú principal
while True:
    print("\n📍 ESTACIONAMIENTO SHOPPING")
    print("1. Ingresar vehículo")
    print("2. Retirar vehículo")
    print("3. Ver ticket")
    print("4. Mostrar mapa del estacionamiento")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_entrada()
    elif opcion == "2":
        registrar_salida()
    elif opcion == "3":
        mostrar_ticket()
    elif opcion == "4":
        mostrar_mapa()
    elif opcion == "5":
        print("👋 Hasta luego.")
        break
    else:
        print("Opción inválida. Intente de nuevo.")
