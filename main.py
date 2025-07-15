from centralizado import BalanceadorCentralizado
from distribuido import BalanceadorDistribuido
from adaptativo import BalanceadorAdaptativo
from predictivo import BalanceadorPredictivo
from reactivo import BalanceadorReactivo
from tareas import calcular_primos_pesado, simulacion_montecarlo, multiplicar_matrices_gigantes
import tkinter as tk
from tkinter import messagebox, ttk
import threading

def obtener_tareas():
    return [
        lambda: calcular_primos_pesado(300_000),  # Reducidos para pruebas más rápidas
        lambda: simulacion_montecarlo(10_000_000),
        lambda: multiplicar_matrices_gigantes(1000),
        lambda: calcular_primos_pesado(400_000),
        lambda: simulacion_montecarlo(15_000_000),
        lambda: multiplicar_matrices_gigantes(1200),
    ]

def ejecutar_balanceador(tipo, root):
    """Ejecuta un tipo específico de balanceador en un hilo separado"""
    def run_balanceador():
        tareas = obtener_tareas()
        try:
            if tipo == "centralizado":
                balanceador = BalanceadorCentralizado(tareas, num_workers=3)
                balanceador.tipo_balanceador = "Centralizado"
            elif tipo == "distribuido":
                balanceador = BalanceadorDistribuido(tareas, num_workers=3)
                balanceador.tipo_balanceador = "Distribuido"
            elif tipo == "adaptativo":
                balanceador = BalanceadorAdaptativo(tareas, num_workers=3)
                balanceador.tipo_balanceador = "Adaptativo"
            elif tipo == "predictivo":
                balanceador = BalanceadorPredictivo(tareas, num_workers=3)
                balanceador.tipo_balanceador = "Predictivo"
            elif tipo == "reactivo":
                balanceador = BalanceadorReactivo(tareas, num_workers=3)
                balanceador.tipo_balanceador = "Reactivo"
            else:
                messagebox.showerror("Error", "Tipo de balanceador no válido.")
                return
            balanceador.ejecutar()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al ejecutar el balanceador:\n{str(e)}")
    
    # Ejecutar en un hilo separado para no bloquear la interfaz
    threading.Thread(target=run_balanceador).start()

def mostrar_info_balanceador(tipo):
    """Muestra información detallada sobre el tipo de balanceador"""
    info = {
        "centralizado": """
        BALANCEADOR CENTRALIZADO
        
        Este balanceador asigna tareas de forma secuencial y predecible utilizando un 
        algoritmo round-robin. Cada tarea nueva se asigna al siguiente worker en la secuencia.
        
        Características:
        - Distribución uniforme de tareas
        - Algoritmo simple y predecible
        - Cada worker recibe aproximadamente la misma cantidad de tareas
        
        Ideal para entornos con tareas de complejidad similar.
        """,
        
        "distribuido": """
        BALANCEADOR DISTRIBUIDO
        
        En este modelo, cada worker tiene una capacidad máxima definida. Las tareas se intentan
        asignar aleatoriamente, y cada worker puede aceptar o rechazar según su capacidad actual.
        
        Características:
        - Workers con capacidades independientes
        - Asignación aleatoria de tareas
        - Posibilidad de rechazo si todos los workers están ocupados
        
        Simula un entorno donde los nodos toman decisiones locales.
        """,
        
        "adaptativo": """
        BALANCEADOR ADAPTATIVO
        
        Este balanceador cambia su estrategia dependiendo de la carga actual del sistema.
        Utiliza round-robin cuando la carga es baja, y cambia a asignar por carga mínima
        cuando detecta saturación.
        
        Características:
        - Combina múltiples estrategias
        - Se adapta a la carga del sistema
        - Busca el equilibrio óptimo según el estado actual
        
        Ideal para entornos con cargas variables.
        """,
        
        "predictivo": """
        BALANCEADOR PREDICTIVO
        
        Utiliza un modelo predictivo simple basado en el historial de tiempos de cada worker
        para estimar cuál tendrá mejor rendimiento para la siguiente tarea.
        
        Características:
        - Basado en historial de rendimiento
        - Asigna tareas al worker que predice será más rápido
        - Actualiza continuamente sus predicciones
        
        Útil cuando los workers tienen rendimientos diferentes o variables.
        """,
        
        "reactivo": """
        BALANCEADOR REACTIVO
        
        Monitorea constantemente la carga de cada worker y reacciona cuando detecta
        que alguno está por encima del límite establecido, reasignando tareas.
        
        Características:
        - Prioriza workers con menor carga
        - Establece límites de saturación
        - Puede rechazar tareas si todos los workers están saturados
        
        Eficaz para prevenir la sobrecarga de workers individuales.
        """
    }
    
    top = tk.Toplevel()
    top.title(f"Información - Balanceador {tipo.capitalize()}")
    top.geometry("500x400")
    top.configure(bg="#f5f5f5")
    
    # Título
    tk.Label(top, text=f"BALANCEADOR {tipo.upper()}", 
             font=("Arial", 14, "bold"), bg="#f5f5f5", pady=10).pack()
    
    # Texto informativo con scroll
    frame = tk.Frame(top, bg="#f5f5f5")
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # Scrollbar
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Cuadro de texto para la información
    info_text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, 
                       bg="#ffffff", padx=10, pady=10)
    info_text.insert(tk.END, info[tipo])
    info_text.config(state=tk.DISABLED)  # Hacer que sea de solo lectura
    info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar.config(command=info_text.yview)
    
    # Botón para cerrar
    tk.Button(top, text="Cerrar", command=top.destroy, 
             padx=10, pady=5, bg="#e0e0e0", width=15).pack(pady=10)

def main_gui():
    root = tk.Tk()
    root.title("Simulador de Balanceo de Carga")
    root.geometry("550x600")
    root.eval('tk::PlaceWindow . center')
    
    # Mejora visual con estilo ttk
    style = ttk.Style()
    style.theme_use('clam')  # Usar un tema más moderno
    
    # Frame principal con degradado de color
    main_frame = tk.Frame(root, bg="#e0e0e0")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Título principal
    header_frame = tk.Frame(main_frame, bg="#3498db", padx=20, pady=15)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="SIMULADOR DE BALANCEO DE CARGA", 
             font=("Arial", 16, "bold"), bg="#3498db", fg="white").pack()
    
    # Descripción
    tk.Label(main_frame, text="Seleccione un algoritmo de balanceo para simular", 
             font=("Arial", 10), bg="#e0e0e0", pady=10).pack()
    
    # Contenedor para los botones de balanceadores
    buttons_frame = tk.Frame(main_frame, bg="#e0e0e0", padx=20, pady=10)
    buttons_frame.pack(fill=tk.X)
    
    balanceadores = [
        ("centralizado", "Balanceo Centralizado", "#2ecc71"),
        ("distribuido", "Balanceo Distribuido", "#e74c3c"),
        ("adaptativo", "Balanceo Adaptativo", "#f39c12"),
        ("predictivo", "Balanceo Predictivo", "#9b59b6"),
        ("reactivo", "Balanceo Reactivo", "#1abc9c")
    ]
    
    for i, (tipo, nombre, color) in enumerate(balanceadores):
        frame = tk.Frame(buttons_frame, bg="#e0e0e0", pady=5)
        frame.pack(fill=tk.X)
        
        # Botón para ejecutar el balanceador
        btn_ejecutar = tk.Button(frame, text=nombre, bg=color, fg="white",
                               command=lambda t=tipo: ejecutar_balanceador(t, root),
                               width=20, font=("Arial", 10, "bold"), padx=10, pady=5)
        btn_ejecutar.pack(side=tk.LEFT, padx=5)
        
        # Botón para mostrar información
        btn_info = tk.Button(frame, text="?", bg="#7f8c8d", fg="white",
                           command=lambda t=tipo: mostrar_info_balanceador(t),
                           width=3, font=("Arial", 10, "bold"))
        btn_info.pack(side=tk.LEFT)
    
    # Marco inferior
    footer_frame = tk.Frame(main_frame, bg="#e0e0e0", pady=15)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    # Botón para salir
    tk.Button(footer_frame, text="Salir", command=root.quit, 
             width=20, bg="#e74c3c", fg="white", 
             font=("Arial", 10, "bold"), padx=10, pady=5).pack()
    
    # Información del proyecto
    tk.Label(footer_frame, text="Simulador de algoritmos de balanceo de carga", 
             font=("Arial", 8), bg="#e0e0e0", fg="#7f8c8d", pady=5).pack()
    
    root.mainloop()

if __name__ == "__main__":
    main_gui()
