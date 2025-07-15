from threading import Thread
from balanceador_base import BalanceadorBase
import tkinter as tk
from tkinter import messagebox

class BalanceadorCentralizado(BalanceadorBase):
    def ejecutar(self):
        self.tipo_balanceador = "Centralizado"
        self.crear_ventana("Balanceo Centralizado", 
                        "== BALANCEO CENTRALIZADO ==\nLas tareas se asignarán de forma secuencial (round-robin).")
        
        hilos = []
        asignaciones = ""
        for i, tarea in enumerate(self.tareas):
            worker_id = i % self.num_workers
            asignaciones += f"Tarea {i+1} → Worker {worker_id}\n"
            try:
                t = Thread(target=self.worker, args=(worker_id, tarea))
                hilos.append(t)
                t.start()
            except Exception as e:
                asignaciones += f"Error asignando tarea {i+1}: {e}\n"
        
        self.crear_ventana("Asignaciones Centralizado", f"Asignaciones realizadas:\n\n{asignaciones}")
        
        for t in hilos:
            t.join()
        
        self.mostrar_resultados()
        self.mostrar_resultados()
