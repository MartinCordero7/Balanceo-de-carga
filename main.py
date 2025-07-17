from centralizado import BalanceadorCentralizado
from distribuido import BalanceadorDistribuido
from adaptativo import BalanceadorAdaptativo
from predictivo import BalanceadorPredictivo
from reactivo import BalanceadorReactivo
from tareas import calcular_primos_pesado, simulacion_montecarlo, multiplicar_matrices_gigantes
from servidor_simulado import ClusterServidores, generar_conjunto_tareas
from cargas_especializadas import (
    obtener_carga_centralizada, obtener_carga_distribuida, 
    obtener_carga_adaptativa, obtener_carga_predictiva, 
    obtener_carga_reactiva, obtener_carga_servidores_especializada,
    obtener_descripcion_carga
)
import tkinter as tk
from tkinter import messagebox, ttk
import threading

# Crear un cluster global de servidores para reutilizarlo
cluster_global = ClusterServidores(num_servidores=5)

def obtener_tareas(tipo="matematicas", balanceador=None):
    """Obtiene tareas según el tipo solicitado y el balanceador"""
    if tipo == "matematicas":
        # Usar cargas especializadas para cada balanceador si se especifica
        if balanceador == "centralizado":
            return obtener_carga_centralizada(cluster_global)
        elif balanceador == "distribuido":
            return obtener_carga_distribuida(cluster_global)
        elif balanceador == "adaptativo":
            return obtener_carga_adaptativa(cluster_global)
        elif balanceador == "predictivo":
            return obtener_carga_predictiva(cluster_global)
        elif balanceador == "reactivo":
            return obtener_carga_reactiva(cluster_global)
        # Si no se especifica balanceador, usar carga estándar
        return [
            lambda: calcular_primos_pesado(300_000),
            lambda: simulacion_montecarlo(10_000_000),
            lambda: multiplicar_matrices_gigantes(1000),
            lambda: calcular_primos_pesado(400_000),
            lambda: simulacion_montecarlo(15_000_000),
            lambda: multiplicar_matrices_gigantes(1200),
        ]
    elif tipo == "servidores":
        if balanceador:
            return obtener_carga_servidores_especializada(cluster_global, balanceador)
        return generar_conjunto_tareas(cluster_global, num_tareas=12)
    else:  # Mixtas
        # Combinación de tareas matemáticas y servidor, adaptadas por balanceador
        if balanceador == "centralizado":
            mat = obtener_carga_centralizada(cluster_global)[:3]
            srv = obtener_carga_servidores_especializada(cluster_global, balanceador)[:3]
        elif balanceador == "distribuido":
            mat = obtener_carga_distribuida(cluster_global)[:3]
            srv = obtener_carga_servidores_especializada(cluster_global, balanceador)[:3]
        elif balanceador == "adaptativo":
            mat = obtener_carga_adaptativa(cluster_global)[:3]
            srv = obtener_carga_servidores_especializada(cluster_global, balanceador)[:3]
        elif balanceador == "predictivo":
            mat = obtener_carga_predictiva(cluster_global)[:4]
            srv = obtener_carga_servidores_especializada(cluster_global, balanceador)[:4]
        elif balanceador == "reactivo":
            mat = obtener_carga_reactiva(cluster_global)[:3]
            srv = obtener_carga_servidores_especializada(cluster_global, balanceador)[:3]
        else:
            mat = [
                lambda: calcular_primos_pesado(200_000),
                lambda: simulacion_montecarlo(8_000_000),
                lambda: multiplicar_matrices_gigantes(800),
            ]
            srv = generar_conjunto_tareas(cluster_global, num_tareas=3)
        return mat + srv

def ejecutar_balanceador(tipo, root, tipo_tareas="matematicas"):
    """Ejecuta un tipo específico de balanceador en un hilo separado"""
    def run_balanceador():
        # Obtener tareas especializadas para el tipo de balanceador
        tareas = obtener_tareas(tipo_tareas, tipo)
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
                
            # Mostrar información sobre la carga especializada
            mostrar_info_carga_especializada(tipo)
                
            balanceador.ejecutar()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al ejecutar el balanceador:\n{str(e)}")
    
    # Ejecutar en un hilo separado para no bloquear la interfaz
    threading.Thread(target=run_balanceador).start()

def mostrar_info_carga_especializada(tipo_balanceador):
    """Muestra información sobre la carga especializada para este balanceador"""
    descripcion = obtener_descripcion_carga(tipo_balanceador)
    
    top = tk.Toplevel()
    top.title(f"Carga Especializada - {tipo_balanceador.capitalize()}")
    top.geometry("500x300")
    top.configure(bg="#f5f5f5")
    
    # Título
    tk.Label(top, text=f"CARGA ESPECIALIZADA PARA BALANCEADOR {tipo_balanceador.upper()}", 
             font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#2c3e50", pady=10).pack()
    
    # Texto informativo con scroll
    frame = tk.Frame(top, bg="#f5f5f5")
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # Scrollbar
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Cuadro de texto para la información
    info_text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, 
                       bg="#ffffff", padx=10, pady=10)
    info_text.insert(tk.END, descripcion)
    info_text.config(state=tk.DISABLED)  # Hacer que sea de solo lectura
    info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar.config(command=info_text.yview)
    
    # Botón para cerrar
    tk.Button(top, text="Entendido", command=top.destroy, 
             padx=10, pady=5, bg="#3498db", fg="white", width=15).pack(pady=10)

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

def mostrar_info_cluster():
    """Muestra información sobre el estado del cluster de servidores"""
    stats = cluster_global.obtener_estadisticas_cluster()
    
    top = tk.Toplevel()
    top.title("Estado del Clúster de Servidores")
    top.geometry("600x400")
    top.configure(bg="#f5f5f5")
    
    # Título
    tk.Label(top, text="ESTADÍSTICAS DEL CLÚSTER DE SERVIDORES", 
             font=("Arial", 14, "bold"), bg="#f5f5f5", pady=10).pack()
    
    # Frame para la información
    frame = tk.Frame(top, bg="#f5f5f5", padx=20, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Cabeceras de la tabla
    headers = ["Servidor", "Capacidad", "Conexiones", "Carga CPU", "Total Sol.", "Rechazadas", "Tasa Rechazo"]
    for i, header in enumerate(headers):
        tk.Label(frame, text=header, font=("Arial", 10, "bold"), 
                 bg="#34495e", fg="white", padx=5, pady=3).grid(row=0, column=i, sticky="ew")
    
    # Datos de los servidores
    for i, server_stats in enumerate(stats):
        tk.Label(frame, text=server_stats["nombre"], 
                 bg="#3498db", fg="white", padx=5, pady=2).grid(row=i+1, column=0, sticky="ew")
        tk.Label(frame, text=str(server_stats["capacidad"]), 
                 bg="#f0f0f0", padx=5, pady=2).grid(row=i+1, column=1, sticky="ew")
        tk.Label(frame, text=str(server_stats["conexiones_activas"]), 
                 bg="#f0f0f0", padx=5, pady=2).grid(row=i+1, column=2, sticky="ew")
        tk.Label(frame, text=f"{server_stats['carga_cpu']:.2f}", 
                 bg="#f0f0f0", padx=5, pady=2).grid(row=i+1, column=3, sticky="ew")
        tk.Label(frame, text=str(server_stats["solicitudes_totales"]), 
                 bg="#f0f0f0", padx=5, pady=2).grid(row=i+1, column=4, sticky="ew")
        tk.Label(frame, text=str(server_stats["solicitudes_rechazadas"]), 
                 bg="#f0f0f0", padx=5, pady=2).grid(row=i+1, column=5, sticky="ew")
        tk.Label(frame, text=f"{server_stats['tasa_rechazo']:.1%}", 
                 bg="#f0f0f0", padx=5, pady=2).grid(row=i+1, column=6, sticky="ew")
    
    # Botones
    btn_frame = tk.Frame(top, bg="#f5f5f5", pady=10)
    btn_frame.pack(fill=tk.X)
    
    tk.Button(btn_frame, text="Actualizar", command=lambda: mostrar_info_cluster(),
             bg="#3498db", fg="white", padx=10, pady=5, width=15).pack(side=tk.LEFT, padx=10)
    
    tk.Button(btn_frame, text="Cerrar", command=top.destroy,
             bg="#e74c3c", fg="white", padx=10, pady=5, width=15).pack(side=tk.RIGHT, padx=10)
    
    # Configurar expansión de columnas
    for i in range(len(headers)):
        frame.grid_columnconfigure(i, weight=1)

def main_gui():
    root = tk.Tk()
    root.title("Simulador de Balanceo de Carga")
    root.geometry("650x700")  # Un poco más alto para acomodar el nuevo texto
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
    tk.Label(main_frame, text="Cada balanceador ejecutará una carga de trabajo especializada", 
             font=("Arial", 10, "italic"), bg="#e0e0e0", pady=5).pack()
    
    tk.Label(main_frame, text="Seleccione un algoritmo de balanceo para simular", 
             font=("Arial", 10), bg="#e0e0e0", pady=5).pack()
    
    # Selector de tipo de tareas
    tipo_tareas_frame = tk.Frame(main_frame, bg="#e0e0e0", pady=10)
    tipo_tareas_frame.pack(fill=tk.X)
    
    tk.Label(tipo_tareas_frame, text="Tipo de tareas:", 
             font=("Arial", 10, "bold"), bg="#e0e0e0").pack(side=tk.LEFT, padx=20)
    
    tipo_tareas_var = tk.StringVar(value="matematicas")
    
    tipo_opciones = [
        ("matematicas", "Matemáticas"),
        ("servidores", "Servidores"),
        ("mixto", "Mixto")
    ]
    
    for valor, texto in tipo_opciones:
        tk.Radiobutton(tipo_tareas_frame, text=texto, variable=tipo_tareas_var, 
                       value=valor, bg="#e0e0e0").pack(side=tk.LEFT, padx=10)
    
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
                               command=lambda t=tipo: ejecutar_balanceador(t, root, tipo_tareas_var.get()),
                               width=20, font=("Arial", 10, "bold"), padx=10, pady=5)
        btn_ejecutar.pack(side=tk.LEFT, padx=5)
        
        # Botón para mostrar información sobre el balanceador
        btn_info = tk.Button(frame, text="?", bg="#7f8c8d", fg="white",
                           command=lambda t=tipo: mostrar_info_balanceador(t),
                           width=3, font=("Arial", 10, "bold"))
        btn_info.pack(side=tk.LEFT)
        
        # Botón para mostrar información sobre la carga especializada
        btn_carga = tk.Button(frame, text="Carga", bg="#34495e", fg="white",
                            command=lambda t=tipo: mostrar_info_carga_especializada(t),
                            width=6, font=("Arial", 10, "bold"))
        btn_carga.pack(side=tk.LEFT, padx=5)
    
    # Botón para ver estado del clúster
    cluster_frame = tk.Frame(main_frame, bg="#e0e0e0", pady=10)
    cluster_frame.pack(fill=tk.X)
    
    tk.Button(cluster_frame, text="Ver Estado del Clúster", bg="#34495e", fg="white",
             command=mostrar_info_cluster, width=25, font=("Arial", 10, "bold"), padx=10, pady=5).pack()
    
    # Separador visual
    ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, padx=20, pady=10)
    
    # Información sobre los tipos de tareas
    info_frame = tk.Frame(main_frame, bg="#e0e0e0", padx=20, pady=5)
    info_frame.pack(fill=tk.X)
    
    tk.Label(info_frame, text="TIPOS DE TAREAS DISPONIBLES", 
             font=("Arial", 12, "bold"), bg="#e0e0e0").pack(pady=5)
    
    tipos_info = tk.Text(info_frame, height=8, wrap=tk.WORD, padx=10, pady=10, bg="#f0f0f0")
    tipos_info.insert(tk.END, """• Matemáticas: Tareas de cálculo intensivo (primos, matrices, Monte Carlo).
• Servidores: Simulación de solicitudes a un clúster de servidores con latencia de red, capacidades limitadas y cargas dinámicas.
• Mixto: Combinación de tareas matemáticas y solicitudes a servidores.

Las tareas de servidores simulan un entorno real con latencia variable y posibilidad de rechazos por sobrecarga.""")
    tipos_info.config(state=tk.DISABLED)  # Solo lectura
    tipos_info.pack(fill=tk.X)
    
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
