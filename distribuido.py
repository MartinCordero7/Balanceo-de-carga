from threading import Thread
from balanceador_base import BalanceadorBase
import random
import tkinter as tk
from tkinter import messagebox

class BalanceadorDistribuido(BalanceadorBase):
    def __init__(self, tareas, num_workers=3):
        super().__init__(tareas, num_workers)
        self.capacidad_max = [random.randint(1, 3) for _ in range(num_workers)]
        self.cargas_actuales = [0] * num_workers
        self.tipo_balanceador = "Distribuido"

    def ejecutar(self):
        capacidades = "\n".join([f"Worker {i}: capacidad máxima {cap}" for i, cap in enumerate(self.capacidad_max)])
        self.crear_ventana("Balanceo Distribuido", 
                        f"== BALANCEO DISTRIBUIDO ==\nCapacidades de los workers:\n{capacidades}")
        
        hilos = []
        asignaciones = ""
        
        for i, tarea in enumerate(self.tareas):
            asignado = False
            for intento in range(self.num_workers):
                w_id = random.randint(0, self.num_workers - 1)
                if self.cargas_actuales[w_id] < self.capacidad_max[w_id]:
                    self.cargas_actuales[w_id] += 1
                    asignaciones += f"Tarea {i+1} aceptada por Worker {w_id}\n"
                    try:
                        t = Thread(target=self.worker, args=(w_id, tarea))
                        hilos.append(t)
                        t.start()
                    except Exception as e:
                        asignaciones += f"Error asignando tarea {i+1}: {e}\n"
                    asignado = True
                    break
            if not asignado:
                asignaciones += f"Tarea {i+1} rechazada: todos los workers están ocupados.\n"
                
        self.crear_ventana("Asignaciones Distribuido", f"Asignaciones realizadas:\n\n{asignaciones}")
        
        for t in hilos:
            t.join()
            
        self.mostrar_resultados()
