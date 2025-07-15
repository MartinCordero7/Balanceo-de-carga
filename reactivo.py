# reactivo.py

from threading import Thread
from balanceador_base import BalanceadorBase
import tkinter as tk
from tkinter import messagebox

class BalanceadorReactivo(BalanceadorBase):
    def ejecutar(self):
        self.tipo_balanceador = "Reactivo"
        self.crear_ventana("Balanceo Reactivo", 
                        "== BALANCEO REACTIVO ==\nSe reasignarán tareas si un worker está saturado (límite 2 tareas).")
        
        hilos = []
        cargas = [0] * self.num_workers
        limite = 2
        asignaciones = ""
        
        for i, tarea in enumerate(self.tareas):
            worker_id = cargas.index(min(cargas))
            if cargas[worker_id] >= limite:
                reasignado = False
                for j in range(self.num_workers):
                    if cargas[j] < limite:
                        worker_id = j
                        reasignado = True
                        asignaciones += f"Tarea {i+1} → Worker {worker_id} (reasignado por saturación)\n"
                        break
                if not reasignado:
                    asignaciones += f"Tarea {i+1} no pudo ser asignada: todos saturados.\n"
                    continue
            else:
                asignaciones += f"Tarea {i+1} → Worker {worker_id}\n"
                
            try:
                t = Thread(target=self.worker, args=(worker_id, tarea))
                hilos.append(t)
                t.start()
                cargas[worker_id] += 1
            except Exception as e:
                asignaciones += f"Error asignando tarea {i+1}: {e}\n"
                
        self.crear_ventana("Asignaciones Reactivo", f"Asignaciones realizadas:\n\n{asignaciones}")
        
        for t in hilos:
            t.join()
            
        self.mostrar_resultados()
