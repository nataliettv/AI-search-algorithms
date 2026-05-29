import heapq
from collections import deque
import grafo as g
import utils

# |---------------------------------------------------------------------------------------------------------------|

# BUSQUEDA POR AMPLITUD (BFS) #LISTO
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
    visitados.add(g.inicio)
    paso = 1

    while cola:
        nodo, camino, costo = cola.popleft()

        pendientes = [x[0] for x in cola]
        print(f"\n  Paso {paso}: DEQUEUE: '{nodo}'")
        print(f"           QUEUE ACTUAL: {pendientes}")
        print(f"           NODOS VISITADOS HASTA AHORA: {visitados}")
        print(f"           Camino hasta aquí: {' -> '.join(camino)}")
        # print(f"           Costo acumulado:   {costo}")   # no tan relevante en BFS

        if nodo == g.meta:
            print(f"\n           *** META ENCONTRADA ***")
            utils.resultado("BFS", camino, costo, len(visitados))
            return

        vecinos_nuevos = []
        for vecino, peso in g.grafo.get(nodo, {}).items():
            if vecino not in visitados:

                visitados.add(vecino)  
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

# |---------------------------------------------------------------------------------------------------------------|
# BUSQUEDA POR COSTO UNIFORME (UCS)

def ucs():
    if not g.hay_grafo():
        return

    utils.encabezado(
        "BUSQUEDA POR COSTO UNIFORME (UCS)",
        "Expande siempre el nodo con menor costo acumulado g(n). Garantiza solución óptima con costos positivos."
    )

    import heapq

    cola = []
    heapq.heappush(cola, (0, g.inicio, [g.inicio]))

    visitados = set()
    paso = 1

    while cola:

        costo, nodo, camino = heapq.heappop(cola)

        if nodo in visitados:
            continue

        visitados.add(nodo)

        print("\n" + "=" * 60)
        print(f"Paso {paso}")
        print(f"Expandiendo nodo: {nodo}")
        print(f"Costo acumulado g(n): {costo}")
        print(f"Camino actual: {' -> '.join(camino)}")
        print("=" * 60)

        if nodo == g.meta:
            print("\nMeta encontrada")
            print(f"Camino final: {' -> '.join(camino)}")
            print(f"Costo total mínimo: {costo}")
            utils.resultado("UCS", camino, costo, len(visitados))
            return

        print("\nGenerando sucesores:")

        for vecino, peso in g.grafo.get(nodo, {}).items():

            if vecino not in visitados:

                nuevo_costo = costo + peso

                print(f"  Transición: {nodo} -> {vecino}")
                print(f"    Costo del paso: {peso}")
                print(f"    Costo acumulado g(n): {nuevo_costo}")

                heapq.heappush(
                    cola,
                    (nuevo_costo, vecino, camino + [vecino])
                )

        print("\nCAMINOS PENDIENTES (ordenados por costos, menor siempre al frente):")
        for c, n, _ in sorted(cola):
            print(f"  Nodo: {n} | g(n): {c}")

        paso += 1

    utils.resultado("UCS", None, 0, len(visitados))

# |---------------------------------------------------------------------------------------------------------------|
# BUSQUEDA POR PROFUNDIDAD (DFS)

def dfs():
    if not g.hay_grafo():
        return

    utils.encabezado(
        "BUSQUEDA POR PROFUNDIDAD (DFS)",
        "Va al fondo antes de retroceder. Recursiva con backtracking."
    )

    visitados = set()
    pasos_hechos = [0]

    def explorar(nodo, camino, costo, nivel):
        sangria = "    " + "  " * nivel

        if nodo in visitados:
            print(f"{sangria}'{nodo}' ya fue visitado, lo salto.")
            return None, 0

        visitados.add(nodo)
        pasos_hechos[0] += 1

        print(f"\n{sangria}Paso {pasos_hechos[0]}: VISITANDO: '{nodo}'")
        print(f"{sangria}          NODOS VISITADOS: {visitados}")
        print(f"{sangria}          Camino hasta aqui: {' -> '.join(camino)}")
        # print(f"{sangria}          Costo acumulado: {costo}")
        if nodo == g.meta:
            print(f"\n{sangria}          *** META ENCONTRADA ***")
            return camino, costo

        vecinos = [
            (v, p)
            for v, p in g.grafo.get(nodo, {}).items()
            if v not in visitados
        ]

        if vecinos:
            nombres = [v for v, _ in vecinos]
            print(f"{sangria}          Explorando vecinos: {nombres}")
        else:
            print(f"{sangria}          Sin vecinos nuevos.")

        for vecino, peso in vecinos:
            print(f"{sangria}          BAJANDO A (RECURSION) -> '{vecino}' -> ")

            encontrado, costo_total = explorar( vecino, camino + [vecino], costo + peso, nivel + 1 )

            if encontrado:
                return encontrado, costo_total

        print(f"{sangria}           RETROCEDIENDO DESDE (BACKTRACKING) <- '{nodo}'")

        return None, 0

    camino, costo = explorar( g.inicio, [g.inicio], 0, 0 )
    utils.resultado( "DFS", camino, costo, len(visitados) )

# |---------------------------------------------------------------------------------------------------------------|
# BUSQUEDA POR PROFUNDIDAD LIMITADA (DLS)

def dls(limite):
    if not g.hay_grafo():
        return

    utils.encabezado(
        "BUSQUEDA EN PROFUNDIDAD LIMITADA (DLS)",
        f"DFS recursivo con limite de profundidad = {limite}"
    )

    visitados = set()
    pasos_hechos = [0]

    def explorar(nodo, camino, costo, nivel):
        sangria = "    " + "  " * nivel

        if nodo in visitados:
            print(f"{sangria}'{nodo}' ya fue visitado.")
            return None, 0

        visitados.add(nodo)
        pasos_hechos[0] += 1

        print(f"\n{sangria}Paso {pasos_hechos[0]}: VISITANDO '{nodo}'")
        print(f"{sangria}          Nivel actual: {nivel}")
        print(f"{sangria}          Camino: {' -> '.join(camino)}")
        # print(f"{sangria}          Costo acumulado: {costo}")

        if nodo == g.meta:
            print(f"{sangria}          *** META ENCONTRADA ***")
            return camino, costo

        if nivel == limite:
            print(f"{sangria}          LIMITE ALCANZADO.")
            print(f"{sangria}          Retrocediendo...")
            return None, 0

        vecinos = [
            (v, p)
            for v, p in g.grafo.get(nodo, {}).items()
            if v not in visitados
        ]

        if vecinos:
            nombres = [v for v, _ in vecinos]
            print(f"{sangria}          Explorando vecinos: {nombres}")
        else:
            print(f"{sangria}          Sin vecinos nuevos.")

        for vecino, peso in vecinos:
            print(f"{sangria}          BAJANDO A -> '{vecino}'")

            encontrado, costo_total = explorar( vecino, camino + [vecino], costo + peso, nivel + 1)
  
            if encontrado:
                return encontrado, costo_total

        print(f"{sangria}          RETROCEDIENDO DESDE <- '{nodo}'")
        return None, 0

    camino, costo = explorar( g.inicio, [g.inicio], 0,0)
    utils.resultado( "DLS", camino, costo, len(visitados) )

# |---------------------------------------------------------------------------------------------------------------|
# BUSQUEDA POR PROFUNDIDAD ITERATIVA (IDDFS)

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
            print(f"{sangria}          Camino: {' -> '.join(camino)}")
            # print(f"{sangria}          Costo total: {costo}")
            return camino, costo

        if nivel == limite:
            print(f"{sangria}          LÍMITE ALCANZADO.")
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
        print(f"\n  ========= ITERACIÓN CON LIMITE = {limite} =========")
        paso = [1]
        camino, costo = dls_interno(g.inicio, [g.inicio], 0, 0, limite, paso)

        if camino:
            utils.resultado(f"IDDFS (solucion con limite={limite})", camino, costo, total_explorados[0])
            return

        print(f"\n  --> NO HAY SOLUCION CON LIMITE: {limite}. + AUMENTANDO A: {limite + 1}.")

    utils.resultado("IDDFS", None, 0, total_explorados[0])

    #IDDFS necesita revisitar nodos porque cada iteración reinicia la búsqueda desde 
    # la raíz con un límite mayor de profundidad.
    #  Esto permite alcanzar niveles más profundos progresivamente.

# |---------------------------------------------------------------------------------------------------------------|
# BUSQUEDA AVARA (GREEDY BEST-FIRST)

# Idea: usa SOLO la heuristica h(n) para decidir que expandir.
# h(n) es una estimacion de que tan lejos esta el nodo de la meta.
# Siempre elige el nodo que parece estar MAS CERCA de la meta.
# IGNORA el costo real g(n) del camino recorrido.
# Por eso NO garantiza el camino optimo.

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
