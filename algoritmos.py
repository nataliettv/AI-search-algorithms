import heapq
from collections import deque
import grafo as g
import utils


# ============================================================
# BUSQUEDA POR AMPLITUD (BFS)
#
# Idea: usa una COLA (FIFO).
# Explora todos los vecinos del nivel actual antes de bajar.
# No toma en cuenta costos, solo la cantidad de pasos.
# Garantiza encontrar el camino con menos pasos (no menor costo).
# ============================================================
def bfs():
    if not g.hay_grafo():
        return

    utils.encabezado(
        "BUSQUEDA POR AMPLITUD (BFS)",
        "Explora nivel por nivel. Usa COLA FIFO. No considera costos."
    )

    cola = deque()
    cola.append( (g.inicio, [g.inicio], 0) )

    visitados = set()
    paso = 1

    while cola:
        nodo, camino, costo = cola.popleft()

        pendientes = [x[0] for x in cola]
        print(f"\n  Paso {paso}: DEQUEUE: '{nodo}'")
        print(f"           QUEUE ACTUAL: {pendientes}")

        if nodo in visitados:
            print(f"           '{nodo}' ya fue visitado, lo salto.")
            continue
        visitados.add(nodo)

        print(f"           NODOS VISITADOS HASTA AHORA: {visitados}")
        print(f"           Camino hasta aquí: {' -> '.join(camino)}")
        # print(f"           Costo acumulado:   {costo}")   # no tan relevante en BFS

        if nodo == g.meta:
            print(f"           *** META ENCONTRADA ***")
            utils.resultado("BFS", camino, costo, len(visitados))
            return

        vecinos_nuevos = []
        for vecino, peso in g.grafo.get(nodo, {}).items():
            if vecino not in visitados:
                cola.append( (vecino, camino + [vecino], costo + peso) )
                vecinos_nuevos.append(vecino)
                # vecinos_nuevos.append(f"{vecino}(c:{costo+peso})")   # con costo

        if vecinos_nuevos:
            print(f"           ENCOLAR VECINOS: {vecinos_nuevos}")
        else:
            print(f"           Sin vecinos nuevos.")

        pendientes = [x[0] for x in cola]
        print(f"           QUEUE ACTUAL (despues de encolar): {pendientes}")

        paso += 1

    utils.resultado("BFS", None, 0, len(visitados))


# ============================================================
# BUSQUEDA POR COSTO UNIFORME (UCS)
#
# Idea: igual que BFS pero usa una COLA DE PRIORIDAD.
# Siempre expande el nodo con MENOR COSTO ACUMULADO g(n).
# No usa heuristica, solo el costo real del camino.
# Garantiza encontrar el camino de MENOR COSTO.
# ============================================================
def ucs():
    if not g.hay_grafo():
        return

    utils.encabezado(
        "BUSQUEDA POR COSTO UNIFORME (UCS)",
        "Siempre expande el de menor costo g(n). No usa heuristica. Garantiza optimo."
    )

    # cola de prioridad: (costo_acumulado, nodo, camino)
    # heapq siempre pone el de menor costo primero
    cola = []
    heapq.heappush(cola, (0, g.inicio, [g.inicio]))

    visitados = set()
    paso = 1

    while cola:
        costo, nodo, camino = heapq.heappop(cola)   # saco el de menor costo

        if nodo in visitados:
            continue
        visitados.add(nodo)

        print(f"\n  Paso {paso}: Saco '{nodo}'  (menor g(n) disponible = {costo})")
        print(f"           Camino: {' -> '.join(camino)}")
        print(f"           g({nodo}) = {costo}  (costo real recorrido)")

        if nodo == g.meta:
            print(f"           *** META ENCONTRADA ***")
            utils.resultado("UCS", camino, costo, len(visitados))
            return

        vecinos_nuevos = []
        for vecino, peso in g.grafo.get(nodo, {}).items():
            if vecino not in visitados:
                nuevo_costo = costo + peso
                heapq.heappush(cola, (nuevo_costo, vecino, camino + [vecino]))
                vecinos_nuevos.append(f"{vecino}(g={nuevo_costo})")

        if vecinos_nuevos:
            print(f"           Agrego: {', '.join(vecinos_nuevos)}")

        frontera = sorted([(x[0], x[1]) for x in cola])
        print(f"           Frontera por g(n): {frontera}")
        paso += 1

    utils.resultado("UCS", None, 0, len(visitados))


# ============================================================
# BUSQUEDA POR PROFUNDIDAD (DFS)
#
# Idea: va lo mas profundo posible antes de retroceder.
# Implementacion RECURSIVA: cada llamada es un nivel mas.
# Uso sangria para que se vea visualmente la profundidad.
# No garantiza el camino optimo, solo encuentra uno.
# ============================================================
def dfs():
    if not g.hay_grafo():
        return

    utils.encabezado(
        "BUSQUEDA POR PROFUNDIDAD (DFS)",
        "Va al fondo antes de retroceder. Recursiva con backtracking."
    )

    visitados    = set()
    pasos_hechos = [0]   # lista para poder modificarla dentro de la funcion

    def explorar(nodo, camino, costo, nivel):
        sangria = "    " + "  " * nivel   # sangria visual segun profundidad

        if nodo in visitados:
            return None, 0
        visitados.add(nodo)
        pasos_hechos[0] += 1

        print(f"{sangria}Paso {pasos_hechos[0]}: Entro a '{nodo}'  (nivel {nivel}, costo: {costo})")
        print(f"{sangria}          Camino: {' -> '.join(camino)}")

        if nodo == g.meta:
            print(f"{sangria}          *** META ENCONTRADA ***")
            return camino, costo

        vecinos = list(g.grafo.get(nodo, {}).items())
        if vecinos:
            print(f"{sangria}          Vecinos a explorar: {[v for v,_ in vecinos]}")
        else:
            print(f"{sangria}          Sin vecinos. Retrocediendo...")
        print()

        # llamo recursivamente a cada vecino (esto es lo que lo hace DFS)
        for vecino, peso in vecinos:
            encontrado, costo_total = explorar(vecino, camino + [vecino], costo + peso, nivel + 1)
            if encontrado:
                return encontrado, costo_total

        print(f"{sangria}Ramas de '{nodo}' agotadas. Retrocedo un nivel.")
        return None, 0

    camino, costo = explorar(g.inicio, [g.inicio], 0, 0)
    utils.resultado("DFS", camino, costo, len(visitados))


# ============================================================
# BUSQUEDA POR PROFUNDIDAD LIMITADA (DLS)
#
# Idea: igual que DFS pero con un LIMITE de profundidad.
# Si llega al limite, no baja mas aunque haya vecinos.
# Sirve para evitar que DFS se pierda en ramas muy largas.
# Si el limite es muy pequeno, puede no encontrar solucion.
# ============================================================
def dls():
    if not g.hay_grafo():
        return

    try:
        limite = int(input("Limite de profundidad: "))
    except ValueError:
        print("  [!] Ingresa un numero entero.")
        return

    utils.encabezado(
        f"BUSQUEDA POR PROFUNDIDAD LIMITADA (DLS, limite={limite})",
        f"Como DFS pero no baja mas de {limite} niveles."
    )

    explorados = [0]
    pasos      = [1]

    def explorar(nodo, camino, costo, nivel):
        sangria = "    " + "  " * nivel
        explorados[0] += 1

        print(f"{sangria}Paso {pasos[0]}: '{nodo}'  (nivel {nivel}/{limite}, costo: {costo})")
        print(f"{sangria}          Camino: {' -> '.join(camino)}")
        pasos[0] += 1

        if nodo == g.meta:
            print(f"{sangria}          *** META ENCONTRADA ***")
            return camino, costo

        # aqui esta la diferencia con DFS: reviso el limite antes de bajar
        if nivel == limite:
            print(f"{sangria}          Limite {limite} alcanzado. No bajo mas.")
            print()
            return None, 0

        # evito ciclos excluyendo nodos que ya estan en el camino actual
        vecinos = [(v, p) for v, p in g.grafo.get(nodo, {}).items() if v not in camino]
        if vecinos:
            print(f"{sangria}          Vecinos: {[v for v,_ in vecinos]}")
        else:
            print(f"{sangria}          Sin vecinos nuevos. Retrocedo.")
        print()

        for vecino, peso in vecinos:
            encontrado, costo_total = explorar(vecino, camino + [vecino], costo + peso, nivel + 1)
            if encontrado:
                return encontrado, costo_total

        return None, 0

    camino, costo = explorar(g.inicio, [g.inicio], 0, 0)
    utils.resultado(f"DLS (limite={limite})", camino, costo, explorados[0])


# ============================================================
# BUSQUEDA POR PROFUNDIDAD ITERATIVA (IDDFS)
#
# Idea: repite DLS aumentando el limite de 0, 1, 2, 3...
# hasta que encuentra la solucion.
# Combina lo mejor de BFS (optimo en pasos) y DFS (poca memoria).
# La desventaja es que re-explora nodos en cada iteracion,
# pero en la practica no es tan costoso.
# ============================================================
def iddfs():
    if not g.hay_grafo():
        return

    utils.encabezado(
        "BUSQUEDA POR PROFUNDIDAD ITERATIVA (IDDFS)",
        "Repite DLS con limite 0, 1, 2... hasta encontrar solucion."
    )

    total_explorados = [0]

    def dls_interno(nodo, camino, costo, nivel, limite, paso):
        total_explorados[0] += 1
        sangria = "      " + "  " * nivel

        print(f"{sangria}Paso {paso[0]}: '{nodo}'  (nivel {nivel}/{limite}, costo: {costo})")
        paso[0] += 1

        if nodo == g.meta:
            print(f"{sangria}          *** META ENCONTRADA ***")
            return camino, costo

        if nivel == limite:
            print(f"{sangria}          Limite alcanzado.")
            return None, 0

        for vecino, peso in g.grafo.get(nodo, {}).items():
            if vecino not in camino:
                encontrado, costo_total = dls_interno(
                    vecino, camino + [vecino], costo + peso, nivel + 1, limite, paso
                )
                if encontrado:
                    return encontrado, costo_total

        return None, 0

    # voy aumentando el limite hasta encontrar o agotar el grafo
    for limite in range(len(g.grafo) + 1):
        print(f"\n  ========= Iteracion con limite = {limite} =========")
        paso = [1]
        camino, costo = dls_interno(g.inicio, [g.inicio], 0, 0, limite, paso)

        if camino:
            utils.resultado(f"IDDFS (solucion con limite={limite})", camino, costo, total_explorados[0])
            return

        print(f"\n  --> No hay solucion con limite {limite}. Aumento a {limite + 1}.")

    utils.resultado("IDDFS", None, 0, total_explorados[0])


# ============================================================
# BUSQUEDA AVARA (GREEDY BEST-FIRST)
#
# Idea: usa SOLO la heuristica h(n) para decidir que expandir.
# h(n) es una estimacion de que tan lejos esta el nodo de la meta.
# Siempre elige el nodo que parece estar MAS CERCA de la meta.
# IGNORA el costo real g(n) del camino recorrido.
# Por eso NO garantiza el camino optimo.
# ============================================================
def avara():
    if not g.hay_grafo():
        return
    if not g.hay_heuristicas():
        return

    utils.encabezado(
        "BUSQUEDA AVARA (Greedy Best-First)",
        "Usa solo h(n). Ignora el costo real g(n). No garantiza optimo."
    )

    # cola de prioridad ordenada por h(n)
    # guarda: (h, nodo, camino, costo_real)
    cola = []
    h_inicio = g.heuristicas.get(g.inicio, 0)
    heapq.heappush(cola, (h_inicio, g.inicio, [g.inicio], 0))

    visitados = set()
    paso = 1

    while cola:
        h, nodo, camino, costo = heapq.heappop(cola)

        if nodo in visitados:
            continue
        visitados.add(nodo)

        print(f"\n  Paso {paso}: Saco '{nodo}'  porque h({nodo}) = {h}  (el menor disponible)")
        print(f"           Costo real recorrido g = {costo}  (la avara lo ignora)")
        print(f"           Camino: {' -> '.join(camino)}")

        if nodo == g.meta:
            print(f"           *** META ENCONTRADA ***")
            utils.resultado("Busqueda Avara (Greedy)", camino, costo, len(visitados))
            return

        vecinos_nuevos = []
        for vecino, peso in g.grafo.get(nodo, {}).items():
            if vecino not in visitados:
                h_vecino = g.heuristicas.get(vecino, 0)
                heapq.heappush(cola, (h_vecino, vecino, camino + [vecino], costo + peso))
                vecinos_nuevos.append(f"{vecino}(h={h_vecino})")

        if vecinos_nuevos:
            print(f"           Agrego: {', '.join(vecinos_nuevos)}")

        frontera = sorted([(x[0], x[1]) for x in cola])
        print(f"           Frontera por h(n): {frontera}")
        paso += 1

    utils.resultado("Busqueda Avara (Greedy)", None, 0, len(visitados))


# ============================================================
# BUSQUEDA A*
#
# Idea: combina UCS y Avara.
# Usa f(n) = g(n) + h(n)
#   g(n) = costo REAL del camino recorrido hasta n
#   h(n) = estimacion heuristica de n a la meta
#   f(n) = estimacion del costo total pasando por n
# Siempre expande el nodo con menor f(n).
# Si h(n) es admisible (nunca sobreestima), garantiza el optimo.
# ============================================================
def a_estrella():
    if not g.hay_grafo():
        return
    if not g.hay_heuristicas():
        return

    utils.encabezado(
        "BUSQUEDA A*",
        "f(n) = g(n) + h(n). Costo real + heuristica. Optimo si h(n) es admisible."
    )

    g0 = 0
    h0 = g.heuristicas.get(g.inicio, 0)
    f0 = g0 + h0

    # cola de prioridad ordenada por f(n)
    # guarda: (f, g_costo, nodo, camino)
    cola = []
    heapq.heappush(cola, (f0, g0, g.inicio, [g.inicio]))

    visitados = set()
    paso = 1

    while cola:
        f, costo_g, nodo, camino = heapq.heappop(cola)

        if nodo in visitados:
            continue
        visitados.add(nodo)

        h = g.heuristicas.get(nodo, 0)
        print(f"\n  Paso {paso}: Saco '{nodo}'  (menor f(n) disponible = {f})")
        print(f"           g({nodo}) = {costo_g}   <- costo real recorrido")
        print(f"           h({nodo}) = {h}   <- estimacion heuristica a la meta")
        print(f"           f({nodo}) = {costo_g} + {h} = {f}")
        print(f"           Camino: {' -> '.join(camino)}")

        if nodo == g.meta:
            print(f"           *** META ENCONTRADA ***")
            utils.resultado("A*", camino, costo_g, len(visitados))
            return

        vecinos_nuevos = []
        for vecino, peso in g.grafo.get(nodo, {}).items():
            if vecino not in visitados:
                nuevo_g = costo_g + peso
                nuevo_h = g.heuristicas.get(vecino, 0)
                nuevo_f = nuevo_g + nuevo_h
                heapq.heappush(cola, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
                vecinos_nuevos.append(f"{vecino}(g={nuevo_g} h={nuevo_h} f={nuevo_f})")

        if vecinos_nuevos:
            print(f"           Agrego: {', '.join(vecinos_nuevos)}")

        frontera = sorted([(x[0], x[2]) for x in cola])
        print(f"           Frontera por f(n): {frontera}")
        paso += 1

    utils.resultado("A*", None, 0, len(visitados))
