from threading import Thread
from balanceador_base import BalanceadorBase
import tkinter as tk
from tkinter import messagebox

class BalanceadorAdaptativo(BalanceadorBase):
    def ejecutar(self):
        self.tipo_balanceador = "Adaptativo"
        self.crear_ventana("Balanceo Adaptativo", 
                        "== BALANCEO ADAPTATIVO ==\nSe asignarán tareas usando round-robin o por carga mínima según la saturación.")
        
        hilos = []
        cargas = [0] * self.num_workers
        asignaciones = ""
        
        for i, tarea in enumerate(self.tareas):
            # Si algún worker tiene 3 o más tareas, usar carga mínima
            if max(cargas) >= 3:
                worker_id = cargas.index(min(cargas))
                estrategia = "Carga mínima"
            else:
                worker_id = i % self.num_workers
                estrategia = "Round-robin"
                
            asignaciones += f"Tarea {i+1} → Worker {worker_id} ({estrategia})\n"
            
            try:
                t = Thread(target=self.worker, args=(worker_id, tarea))
                hilos.append(t)
                t.start()
                cargas[worker_id] += 1
            except Exception as e:
                asignaciones += f"Error asignando tarea {i+1}: {e}\n"
                
        self.crear_ventana("Asignaciones Adaptativo", f"Asignaciones realizadas:\n\n{asignaciones}")
        
        for t in hilos:
            t.join()
            
        self.mostrar_resultados()
