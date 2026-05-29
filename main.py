import grafo
import algoritmos

def menu():
    while True:
        print("\n" + "="*52)
        print("   ALGORITMOS DE BUSQUEDA  ")
        print("="*52)
        print(f"\n  --- Cargar espacio de estados ---")
        print("   1. Ingresar grafo por teclado")
        # print("   2. Cargar grafo desde archivo .txt")
        print("   2. Ver grafo cargado actualmente")
        print("   3. Cargar un archivo .txt de ejemplo")
        print()
        print(f"\n  --- Algoritmos de busqueda ---")
        print("   4. Busqueda por Amplitud         (BFS)")
        print("   5. Busqueda por Costo Uniforme   (UCS)")
        print("   6. Busqueda por Profundidad      (DFS)")
        print("   7. Busqueda por Prof. Limitada   (DLS)")
        print("   8. Busqueda por Prof. Iterativa  (IDDFS)")
        print("  9. Busqueda Avara                (Greedy)")
        print("  10. Busqueda A*")
        print("\n   0. Salir")
        print("="*52)

        opcion = input(f"\n  OPCION: ").strip()

        if   opcion == "1":  grafo.cargar_teclado()
        elif opcion == "2":  grafo.ver_grafo()
        elif opcion == "3":  grafo.cargar_ejemplo()
        # ALGORTIMOS
        elif opcion == "4":  algoritmos.bfs()
        elif opcion == "5":  algoritmos.ucs()
        elif opcion == "6":  algoritmos.dfs()
        elif opcion == "7":
            limite = int(input("\nIngresa el limite de profundidad: "))
            algoritmos.dls(limite)
        elif opcion == "8":  algoritmos.iddfs()
        elif opcion == "9":  algoritmos.avara()
        elif opcion == "10": algoritmos.a_estrella()
        elif opcion == "0":
            print(f"\n  Hasta luego!\n")
            break
        else:
            print(f"\n  [!!] Opcion NO valida, intenta de nuevo [!!]")

if __name__ == "__main__":
    menu()
