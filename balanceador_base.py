import time
import threading
from threading import Thread
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class BalanceadorBase:
    def __init__(self, tareas, num_workers=3):
        self.tareas = tareas
        self.num_workers = num_workers
        self.resultados = [[] for _ in range(num_workers)]
        self.tiempos = [[] for _ in range(num_workers)]
        self.root = None
        self.tipo_balanceador = "Base"  # Será sobrescrito por las subclases
        self.colores_worker = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
        
    def worker(self, worker_id, tarea):
        inicio = time.time()
        try:
            result = tarea()
            tiempo = time.time() - inicio
            self.tiempos[worker_id].append(tiempo)
            self.resultados[worker_id].append(True)
            return True, tiempo, result
        except Exception as e:
            tiempo = time.time() - inicio
            self.tiempos[worker_id].append(tiempo)
            self.resultados[worker_id].append(False)
            return False, tiempo, str(e)

    def crear_ventana(self, titulo, mensaje):
        """Método seguro para mostrar ventanas en el hilo principal"""
        if not hasattr(self, 'root') or self.root is None:
            self.root = tk.Tk()
            self.root.withdraw()
        return messagebox.showinfo(titulo, mensaje)

    def mostrar_resultados(self):
        """Muestra resultados con gráficos en una ventana detallada"""
        # Crear ventana para gráficos
        ventana_resultados = tk.Toplevel()
        ventana_resultados.title(f"Resultados - {self.tipo_balanceador}")
        ventana_resultados.geometry("900x700")
        ventana_resultados.configure(bg="#f5f5f5")
        
        # Frame para título y resumen
        frame_superior = tk.Frame(ventana_resultados, bg="#f5f5f5", padx=20, pady=10)
        frame_superior.pack(fill=tk.X)
        
        tk.Label(frame_superior, text=f"RESULTADOS DEL BALANCEO {self.tipo_balanceador.upper()}", 
                 font=("Arial", 16, "bold"), bg="#f5f5f5").pack()
        
        # Descripción del algoritmo
        descripciones = {
            "Centralizado": "Balanceo centralizado: Distribuye las tareas de manera secuencial (round-robin), asignando cada tarea al siguiente worker en la secuencia. Ofrece una distribución equitativa ideal para tareas similares.",
            "Distribuido": "Balanceo distribuido: Cada worker tiene una capacidad máxima propia y decide independientemente si acepta nuevas tareas. La asignación es aleatoria simulando un entorno descentralizado.",
            "Adaptativo": "Balanceo adaptativo: Cambia dinámicamente entre round-robin y asignación por carga mínima según la saturación del sistema. Se adapta automáticamente al estado actual de los workers.",
            "Predictivo": "Balanceo predictivo: Utiliza predicciones basadas en el historial de tiempos para asignar tareas al worker que se estima será más eficiente, actualizando constantemente sus predicciones.",
            "Reactivo": "Balanceo reactivo: Monitorea la carga de los workers y reacciona cuando detecta saturación, reasignando tareas a los menos ocupados para evitar cuellos de botella."
        }
        
        if self.tipo_balanceador in descripciones:
            tk.Label(frame_superior, text=descripciones[self.tipo_balanceador], 
                     font=("Arial", 10, "italic"), bg="#f5f5f5", wraplength=850, 
                     justify="left").pack(pady=10)
        
        # Datos para los gráficos
        tareas_completadas = [sum(self.resultados[i]) for i in range(self.num_workers)]
        tareas_fallidas = [len(self.resultados[i]) - sum(self.resultados[i]) for i in range(self.num_workers)]
        tiempos_totales = [sum(self.tiempos[i]) for i in range(self.num_workers)]
        tiempos_promedio = [sum(self.tiempos[i])/max(1,len(self.tiempos[i])) for i in range(self.num_workers)]
        
        # Frame para gráficos
        frame_graficos = tk.Frame(ventana_resultados, bg="#f5f5f5")
        frame_graficos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Gráfico 1: Tareas completadas vs fallidas (barras)
        fig1 = plt.Figure(figsize=(5, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ind = np.arange(self.num_workers)
        width = 0.35
        
        bar1 = ax1.bar(ind, tareas_completadas, width, label='Completadas', color='#2ecc71')
        bar2 = ax1.bar(ind + width, tareas_fallidas, width, label='Fallidas', color='#e74c3c')
        
        # Añadir etiquetas con valores
        for i, v in enumerate(tareas_completadas):
            ax1.text(i, v + 0.1, str(v), ha='center')
        for i, v in enumerate(tareas_fallidas):
            ax1.text(i + width, v + 0.1, str(v), ha='center')
        
        ax1.set_ylabel('Número de tareas')
        ax1.set_title('Distribución de Tareas por Worker')
        ax1.set_xticks(ind + width / 2)
        ax1.set_xticklabels([f'Worker {i}' for i in range(self.num_workers)])
        ax1.legend()
        fig1.tight_layout()
        
        # Gráfico 2: Tiempo total por worker (pastel)
        fig2 = plt.Figure(figsize=(5, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        labels = [f'Worker {i}' for i in range(self.num_workers)]
        wedges, texts, autotexts = ax2.pie(tiempos_totales, labels=labels, autopct='%1.1f%%', 
                startangle=90, colors=self.colores_worker[:self.num_workers],
                shadow=True, wedgeprops={'edgecolor': 'white'})
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax2.set_title('Distribución del Tiempo Total de Ejecución')
        fig2.tight_layout()
        
        # Gráfico 3: Tiempos promedio (barras horizontales)
        fig3 = plt.Figure(figsize=(5, 4), dpi=100)
        ax3 = fig3.add_subplot(111)
        bars = ax3.barh(range(self.num_workers), tiempos_promedio, 
                     color=self.colores_worker[:self.num_workers], alpha=0.8)
        
        # Añadir etiquetas con valores
        for i, bar in enumerate(bars):
            ax3.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    f"{tiempos_promedio[i]:.2f}s", va='center')
            
        ax3.set_yticks(range(self.num_workers))
        ax3.set_yticklabels([f'Worker {i}' for i in range(self.num_workers)])
        ax3.set_xlabel('Tiempo (segundos)')
        ax3.set_title('Tiempo Promedio por Worker')
        fig3.tight_layout()
        
        # Colocar los gráficos en la ventana
        canvas1 = FigureCanvasTkAgg(fig1, frame_graficos)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        canvas2 = FigureCanvasTkAgg(fig2, frame_graficos)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        canvas3 = FigureCanvasTkAgg(fig3, frame_graficos)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        frame_graficos.grid_columnconfigure(0, weight=1)
        frame_graficos.grid_columnconfigure(1, weight=1)
        frame_graficos.grid_rowconfigure(0, weight=1)
        frame_graficos.grid_rowconfigure(1, weight=1)
        
        # Tabla de resumen en la parte inferior
        frame_resumen = tk.Frame(ventana_resultados, bg="#f5f5f5", padx=20, pady=10)
        frame_resumen.pack(fill=tk.X)
        
        # Crear una tabla con mejor diseño
        encabezados = ["Worker", "Tareas Completadas", "Tareas Fallidas", "Tiempo Total (s)", "Tiempo Promedio (s)"]
        for i, header in enumerate(encabezados):
            tk.Label(frame_resumen, text=header, font=("Arial", 10, "bold"), 
                    bg="#34495e", fg="white", width=15, relief=tk.RIDGE, pady=5).grid(row=0, column=i, sticky="nsew")
        
        for i in range(self.num_workers):
            tk.Label(frame_resumen, text=f"Worker {i}", bg=self.colores_worker[i], fg="white", 
                    relief=tk.RIDGE, pady=5).grid(row=i+1, column=0, sticky="nsew")
            tk.Label(frame_resumen, text=f"{tareas_completadas[i]}", bg="#f0f0f0",
                    relief=tk.RIDGE, pady=5).grid(row=i+1, column=1, sticky="nsew")
            tk.Label(frame_resumen, text=f"{tareas_fallidas[i]}", bg="#f0f0f0",
                    relief=tk.RIDGE, pady=5).grid(row=i+1, column=2, sticky="nsew")
            tk.Label(frame_resumen, text=f"{tiempos_totales[i]:.2f}", bg="#f0f0f0",
                    relief=tk.RIDGE, pady=5).grid(row=i+1, column=3, sticky="nsew")
            tk.Label(frame_resumen, text=f"{tiempos_promedio[i]:.2f}", bg="#f0f0f0",
                    relief=tk.RIDGE, pady=5).grid(row=i+1, column=4, sticky="nsew")
        
        # Fila de totales
        tk.Label(frame_resumen, text="TOTAL", font=("Arial", 9, "bold"), bg="#2c3e50", fg="white",
                relief=tk.RIDGE, pady=5).grid(row=self.num_workers+1, column=0, sticky="nsew")
        tk.Label(frame_resumen, text=f"{sum(tareas_completadas)}", font=("Arial", 9, "bold"), bg="#ecf0f1",
                relief=tk.RIDGE, pady=5).grid(row=self.num_workers+1, column=1, sticky="nsew")
        tk.Label(frame_resumen, text=f"{sum(tareas_fallidas)}", font=("Arial", 9, "bold"), bg="#ecf0f1",
                relief=tk.RIDGE, pady=5).grid(row=self.num_workers+1, column=2, sticky="nsew")
        tk.Label(frame_resumen, text=f"{sum(tiempos_totales):.2f}", font=("Arial", 9, "bold"), bg="#ecf0f1",
                relief=tk.RIDGE, pady=5).grid(row=self.num_workers+1, column=3, sticky="nsew")
        tk.Label(frame_resumen, text=f"{sum(tiempos_promedio)/self.num_workers:.2f}", font=("Arial", 9, "bold"), bg="#ecf0f1",
                relief=tk.RIDGE, pady=5).grid(row=self.num_workers+1, column=4, sticky="nsew")
        
        # Ajustar tabla para que se expanda
        for i in range(5):
            frame_resumen.grid_columnconfigure(i, weight=1)
        
        # Botón para cerrar
        tk.Button(ventana_resultados, text="Cerrar", command=ventana_resultados.destroy,
                 padx=10, pady=5, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=20).pack(pady=15)
        
        # Si hay una ventana root, destrúyela ya que ahora tenemos los resultados
        if hasattr(self, 'root') and self.root is not None:
            self.root.destroy()
            self.root = None
