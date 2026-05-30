#   aqui se maneja todo lo relacionado con el grafo:
#   - cargar desde teclado
#   - cargar desde archivo
#   - mostrar el grafo


#   el grafo lo representamos como un diccionario de diccionarios porque  es una forma facil de guardar los nodos, 
#   sus vecinos y los costos de las transiciones

# estas variables son globales, todos los archivos las importan de aqui
grafo       = {}
heuristicas = {}
inicio      = ""
meta        = ""

def cargar_teclado(): #carga el grafo desde el teclado, pidiendo al usuario que ingrese los estados, transiciones y heuristicas
    global grafo, heuristicas, inicio, meta
    grafo = {}
    heuristicas = {}

    print("\n--- CAPTURA DEL ESPACIO DE ESTADOS ---")
    inicio = input("Estado inicial: ").strip()
    meta   = input("Estado final:   ").strip()

    print("\nIngresa las transiciones (conexiones entre estados).")
    print("Formato:  origen destino costo")
    print("Ejemplo:  A B 3   (significa: de A puedo ir a B con costo 3)")
    print("Escribe 'fin' cuando termines.\n")

    while True:
        linea = input("Transición: ").strip()
        if linea.lower() == "fin":
            break
        partes = linea.split()
        if len(partes) != 3:
            print("  [!!] Formato: origen destino costo  (3 valores separados por espacio) [!!]")
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
            print(f"\n  [!!] Formato: nodo valor [!!]")
            continue
        heuristicas[partes[0]] = float(partes[1])

    print(f"\n[OK] Grafo guardado correctamente.")


def cargar_archivo(nombre_archivo=None): 
    global grafo, heuristicas, inicio, meta
    grafo = {}
    heuristicas = {}

    if nombre_archivo is None:
        nombre_archivo = input(f"\nNombre del archivo (ej: ejemplos/ejemplo_bfs.txt): ").strip()

    try:
        archivo = open(nombre_archivo, "r")
        lineas  = archivo.readlines()
        archivo.close()
    except FileNotFoundError:
        print(f"\n  [!!] No encontre el archivo '{nombre_archivo}'. [!!]")
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

    print(f"\n[OK] Grafo cargado desde '{nombre_archivo}'.")
    return True

def cargar_ejemplo():
    print("\n  Ejemplos disponibles:")
    print("   1. ejemplos/ejemplo_bfs.txt")
    print("   2. ejemplos/ejemplo_ucs.txt")
    print("   3. ejemplos/ejemplo_dfs.txt")
    print("   4. ejemplos/ejemplo_dls.txt")
    print("   5. ejemplos/ejemplo_iddfs.txt")
    print("   6. ejemplos/ejemplo_avara.txt")
    print("   7. ejemplos/ejemplo_a_estrella.txt")
    print("   8. ejemplos/romania.txt")

    opcion = input(f"\n  Elige un ejemplo (1-8): ").strip()

    archivos = {
        "1": "ejemplos/ejemplo_bfs.txt",
        "2": "ejemplos/ejemplo_ucs.txt",
        "3": "ejemplos/ejemplo_dfs.txt",
        "4": "ejemplos/ejemplo_dls.txt",
        "5": "ejemplos/ejemplo_iddfs.txt",
        "6": "ejemplos/ejemplo_avara.txt",
        "7": "ejemplos/ejemplo_a_estrella.txt",
        "8": "ejemplos/romania.txt",
    }

    if opcion in archivos:
        cargar_archivo(archivos[opcion])
    else:
        print("  [!!] Opcion NO valida [!!]")

def ver_grafo(): #muestra el grafo actual cargado, con sus conexiones y heuristicas (si las tiene)
    if not grafo:
        print(f"\n  [!!] Todavía no has cargado ningun grafo. [!!]")
        return

    print(f"\n  Inicio: {inicio}   |   Meta: {meta}") 
    print(f"\n  Conexiones del grafo:")
    for nodo in grafo:
        for vecino, costo in grafo[nodo].items():
            print(f"    {nodo}  -->  {vecino}   (costo: {costo})")
    if heuristicas:
        print(f"\n  Heuristicas h(n):")
        for nodo, h in heuristicas.items():
            print(f"    h({nodo}) = {h}")


def hay_grafo(): #validacion para algoritmos que necesitan un grafo cargado
    if not grafo or inicio == "" or meta == "":
        print(f"\n  [!!] Primero carga un grafo (opcion 1 o 2 del menu). [!!]")
        return False
    return True


def hay_heuristicas(): #validacion para algoritmos que necesitan heuristicas
    if not heuristicas:
        print(f"\n  [!!] Este algoritmo necesita heuristicas h(n). [!!]")
        print("       Carga un grafo que tenga la seccion HEURISTICAS.")
        return False
    return True
