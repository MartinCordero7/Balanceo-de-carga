from centralizado import BalanceadorCentralizado
# A futuro: importar también distribuido, adaptativo, etc.
from tareas import calcular_primos_pesado, simulacion_montecarlo, multiplicar_matrices_gigantes

def obtener_tareas():
    return [
        lambda: calcular_primos_pesado(800_000),
        lambda: simulacion_montecarlo(40_000_000),
        lambda: multiplicar_matrices_gigantes(2000),
        lambda: calcular_primos_pesado(1_000_000),
        lambda: simulacion_montecarlo(50_000_000),
        lambda: multiplicar_matrices_gigantes(3000),
    ]

def menu():
    print("\n======= SIMULADOR DE BALANCEO DE CARGA =======")
    print("1. Balanceo Centralizado")
    print("2. Balanceo Distribuido")
    print("3. Balanceo Adaptativo")
    print("4. Balanceo Predictivo")
    print("5. Balanceo Reactivo")
    print("0. Salir")
    return input("Selecciona una opción: ")

if __name__ == "__main__":
    while True:
        opcion = menu()
        tareas = obtener_tareas()

        if opcion == "1":
            balanceador = BalanceadorCentralizado(tareas, num_workers=3)
            balanceador.ejecutar()
        elif opcion == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no implementada aún.")
