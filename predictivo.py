from threading import Thread
from balanceador_base import BalanceadorBase
import random
import tkinter as tk
from tkinter import messagebox

class BalanceadorPredictivo(BalanceadorBase):
    def ejecutar(self):
        self.tipo_balanceador = "Predictivo"
        self.crear_ventana("Balanceo Predictivo", 
                        "== BALANCEO PREDICTIVO ==\nSe asignarán tareas según predicción de carga estimada.")
        
        hilos = []
        historial = [random.uniform(3, 10) for _ in range(self.num_workers)]
        asignaciones = ""
        
        for i, tarea in enumerate(self.tareas):
            predicciones = [(w, historial[w]) for w in range(self.num_workers)]
            predicciones.sort(key=lambda x: x[1])
            worker_id = predicciones[0][0]
            asignaciones += f"Tarea {i+1} → Worker {worker_id} (tiempo estimado: {historial[worker_id]:.2f}s)\n"
            
            try:
                t = Thread(target=self.worker, args=(worker_id, tarea))
                hilos.append(t)
                t.start()
                historial[worker_id] += random.uniform(2, 5)
            except Exception as e:
                asignaciones += f"Error asignando tarea {i+1}: {e}\n"
                
        self.crear_ventana("Asignaciones Predictivo", f"Asignaciones realizadas:\n\n{asignaciones}")
        
        for t in hilos:
            t.join()
            
        self.mostrar_resultados()
