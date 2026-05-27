# ============================================================
#   grafo.py
#   Aqui se maneja todo lo relacionado con el grafo:
#   - cargar desde teclado
#   - cargar desde archivo
#   - mostrar el grafo
#
#   El grafo se representa como un diccionario de diccionarios:
#
#   grafo = {
#       'A': {'B': 1, 'C': 4},   <- de A puedo ir a B (costo 1) o C (costo 4)
#       'B': {'D': 2, 'E': 5},   <- de B puedo ir a D (costo 2) o E (costo 5)
#       ...
#   }
#
#   heuristicas = {
#       'A': 6,   <- h(A) = 6, estimacion de cuanto falta de A a la meta
#       'B': 4,
#       ...
#   }
# ============================================================

# estas variables son globales, todos los archivos las importan de aqui
grafo       = {}
heuristicas = {}
inicio      = ""
meta        = ""


def cargar_teclado():
    """Pide al usuario que escriba el grafo directamente en consola."""
    global grafo, heuristicas, inicio, meta
    grafo = {}
    heuristicas = {}

    print("\n--- CAPTURA DEL ESPACIO DE ESTADOS ---")

    # el estado inicial es donde empieza la busqueda
    # el estado final (meta) es a donde queremos llegar
    inicio = input("Estado inicial: ").strip()
    meta   = input("Estado final:   ").strip()

    print("\nIngresa las transiciones (conexiones entre estados).")
    print("Formato:  origen destino costo")
    print("Ejemplo:  A B 3   (significa: de A puedo ir a B con costo 3)")
    print("Escribe 'fin' cuando termines.\n")

    while True:
        linea = input("Transicion: ").strip()
        if linea.lower() == "fin":
            break
        partes = linea.split()
        if len(partes) != 3:
            print("  [!] Formato: origen destino costo  (3 valores separados por espacio)")
            continue
        origen, destino, costo = partes[0], partes[1], float(partes[2])

        if origen not in grafo:
            grafo[origen] = {}
        if destino not in grafo:
            grafo[destino] = {}

        grafo[origen][destino] = costo

    print("\nIngresa las heuristicas h(n) de cada nodo.")
    print("h(n) = estimacion de que tan lejos esta ese nodo de la meta.")
    print("El nodo meta siempre tiene h = 0.")
    print("(Solo las usan Busqueda Avara y A*. Para los demas puedes saltarte esto.)")
    print("Formato:  nodo valor")
    print("Ejemplo:  A 5")
    print("Escribe 'fin' cuando termines.\n")

    while True:
        linea = input("Heuristica: ").strip()
        if linea.lower() == "fin":
            break
        partes = linea.split()
        if len(partes) != 2:
            print("  [!] Formato: nodo valor")
            continue
        heuristicas[partes[0]] = float(partes[1])

    print("\n[OK] Grafo guardado correctamente.")


def cargar_archivo(nombre_archivo=None):
    """Carga el grafo desde un archivo .txt con formato definido."""
    global grafo, heuristicas, inicio, meta
    grafo = {}
    heuristicas = {}

    if nombre_archivo is None:
        nombre_archivo = input("\nNombre del archivo (ej: ejemplos/ejemplo_bfs.txt): ").strip()

    try:
        archivo = open(nombre_archivo, "r")
        lineas  = archivo.readlines()
        archivo.close()
    except FileNotFoundError:
        print(f"  [!] No encontre el archivo '{nombre_archivo}'.")
        return False

    seccion = ""
    for linea in lineas:
        linea = linea.strip()

        if linea == "" or linea.startswith("#"):
            continue

        if linea.upper() == "ESTADOS":
            seccion = "estados"
            continue
        elif linea.upper() == "TRANSICIONES":
            seccion = "transiciones"
            continue
        elif linea.upper() == "HEURISTICAS":
            seccion = "heuristicas"
            continue

        partes = linea.split()

        if seccion == "estados" and len(partes) == 2:
            inicio = partes[0]
            meta   = partes[1]

        elif seccion == "transiciones" and len(partes) == 3:
            origen, destino, costo = partes[0], partes[1], float(partes[2])
            if origen not in grafo:
                grafo[origen] = {}
            if destino not in grafo:
                grafo[destino] = {}
            grafo[origen][destino] = costo

        elif seccion == "heuristicas" and len(partes) == 2:
            heuristicas[partes[0]] = float(partes[1])

    print(f"[OK] Grafo cargado desde '{nombre_archivo}'.")
    return True


def ver_grafo():
    """Muestra el grafo cargado actualmente."""
    if not grafo:
        print("\n  [!] Todavia no has cargado ningun grafo.")
        return

    print(f"\n  Inicio: {inicio}   |   Meta: {meta}")
    print("  Conexiones del grafo:")
    for nodo in grafo:
        for vecino, costo in grafo[nodo].items():
            print(f"    {nodo}  -->  {vecino}   (costo: {costo})")
    if heuristicas:
        print("  Heuristicas h(n):")
        for nodo, h in heuristicas.items():
            print(f"    h({nodo}) = {h}")


def hay_grafo():
    """Revisa que haya un grafo cargado antes de correr cualquier algoritmo."""
    if not grafo or inicio == "" or meta == "":
        print("\n  [!] Primero carga un grafo (opcion 1 o 2 del menu).")
        return False
    return True


def hay_heuristicas():
    """Revisa que haya heuristicas (necesario para Avara y A*)."""
    if not heuristicas:
        print("\n  [!] Este algoritmo necesita heuristicas h(n).")
        print("       Carga un grafo que tenga la seccion HEURISTICAS.")
        return False
    return True
