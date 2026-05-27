# ============================================================
#   utils.py
#   Funciones de ayuda que usan todos los algoritmos:
#   - imprimir encabezado bonito
#   - imprimir resultado final
# ============================================================

import grafo as g   # importo el modulo grafo para leer inicio y meta


def encabezado(nombre, descripcion):
    """Imprime el encabezado cuando arranca un algoritmo."""
    print(f"\n{'='*56}")
    print(f"  {nombre}")
    print(f"  {descripcion}")
    print(f"  Inicio: {g.inicio}   -->   Meta: {g.meta}")
    print(f"{'='*56}")


def resultado(nombre, camino, costo_total, explorados):
    """Imprime el resultado final del algoritmo."""
    print(f"\n{'='*56}")
    print(f"  RESULTADO - {nombre}")
    print(f"{'='*56}")
    if camino:
        print(f"  Camino encontrado:  {' -> '.join(camino)}")
        print(f"  Costo total:        {costo_total}")
        print(f"  Nodos explorados:   {explorados}")
    else:
        print("  No se encontro camino al estado meta.")
    print(f"{'='*56}\n")
