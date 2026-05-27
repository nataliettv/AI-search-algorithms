import grafo
import algoritmos


def cargar_ejemplo():
    print("\n  Ejemplos disponibles:")
    print("   1. ejemplos/ejemplo_bfs.txt")
    print("   2. ejemplos/ejemplo_ucs.txt")
    print("   3. ejemplos/ejemplo_dfs.txt")
    print("   4. ejemplos/ejemplo_dls.txt")
    print("   5. ejemplos/ejemplo_iddfs.txt")
    print("   6. ejemplos/ejemplo_avara.txt")
    print("   7. ejemplos/ejemplo_a_estrella.txt")

    opcion = input("  Cual quieres cargar? (1-7): ").strip()

    archivos = {
        "1": "ejemplos/ejemplo_bfs.txt",
        "2": "ejemplos/ejemplo_ucs.txt",
        "3": "ejemplos/ejemplo_dfs.txt",
        "4": "ejemplos/ejemplo_dls.txt",
        "5": "ejemplos/ejemplo_iddfs.txt",
        "6": "ejemplos/ejemplo_avara.txt",
        "7": "ejemplos/ejemplo_a_estrella.txt",
    }

    if opcion in archivos:
        grafo.cargar_archivo(archivos[opcion])
    else:
        print("  [!] Opcion no valida.")


def menu():
    while True:
        print("\n" + "="*52)
        print("   PROYECTO FINAL - ALGORITMOS DE BUSQUEDA IA")
        print("="*52)
        print("  --- Cargar espacio de estados ---")
        print("   1. Ingresar grafo por teclado")
        print("   2. Cargar grafo desde archivo .txt")
        print("   3. Ver grafo cargado actualmente")
        print("   4. Cargar un archivo de ejemplo")
        print()
        print("  --- Algoritmos de busqueda ---")
        print("   5. Busqueda por Amplitud         (BFS)")
        print("   6. Busqueda por Costo Uniforme   (UCS)")
        print("   7. Busqueda por Profundidad      (DFS)")
        print("   8. Busqueda por Prof. Limitada   (DLS)")
        print("   9. Busqueda por Prof. Iterativa  (IDDFS)")
        print("  10. Busqueda Avara                (Greedy)")
        print("  11. Busqueda A*")
        print()
        print("   0. Salir")
        print("="*52)

        opcion = input("  Opcion: ").strip()

        if   opcion == "1":  grafo.cargar_teclado()
        elif opcion == "2":  grafo.cargar_archivo()
        elif opcion == "3":  grafo.ver_grafo()
        elif opcion == "4":  cargar_ejemplo()
        elif opcion == "5":  algoritmos.bfs()
        elif opcion == "6":  algoritmos.ucs()
        elif opcion == "7":  algoritmos.dfs()
        elif opcion == "8":  algoritmos.dls()
        elif opcion == "9":  algoritmos.iddfs()
        elif opcion == "10": algoritmos.avara()
        elif opcion == "11": algoritmos.a_estrella()
        elif opcion == "0":
            print("\n  Hasta luego!\n")
            break
        else:
            print("  [!] Opcion invalida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
