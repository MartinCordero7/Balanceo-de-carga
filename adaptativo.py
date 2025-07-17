from threading import Thread, Lock
from balanceador_base import BalanceadorBase
import tkinter as tk
from tkinter import messagebox
import time
import random

class BalanceadorAdaptativo(BalanceadorBase):
    def __init__(self, tareas, num_workers=3):
        super().__init__(tareas, num_workers)
        # Inicializar cargas de trabajadores y estimaciones de tareas
        self.cargas_workers = [0] * self.num_workers
        self.estimaciones_tareas = []
        self.carga_umbral = 2.5  # Umbral para cambiar de estrategia
        self.lock = Lock()  # Agregar un lock para sincronización
        
    def estimar_peso_tarea(self, tarea):
        """Estima el peso/dificultad de una tarea basado en características conocidas"""
        # Intentamos detectar el tipo de tarea por su nombre o atributos
        tarea_str = str(tarea)
        if "calcular_primos" in tarea_str:
            if "pesado" in tarea_str:
                return 3.0  # tarea pesada
            return 2.0
        elif "multiplicar_matrices" in tarea_str:
            return 2.5
        elif "simulacion_montecarlo" in tarea_str:
            return 1.8
        elif "servidor" in tarea_str or "request" in tarea_str:
            # Para tareas de servidor, asumimos un peso aleatorio pero predecible
            # basado en alguna característica de la función
            return 1.0 + (hash(tarea_str) % 100) / 50.0
        # Para tareas desconocidas, peso intermedio
        return 1.5
        
    def ejecutar(self):
        self.tipo_balanceador = "Adaptativo"
        self.crear_ventana("Balanceo Adaptativo", 
                        "== BALANCEO ADAPTATIVO ==\nSe asignarán tareas usando round-robin o por carga mínima según la saturación.")
        
        hilos = []
        self.cargas_workers = [0] * self.num_workers
        asignaciones = ""
        
        # Pre-estimamos los pesos de las tareas
        self.estimaciones_tareas = [self.estimar_peso_tarea(tarea) for tarea in self.tareas]
        
        for i, tarea in enumerate(self.tareas):
            peso_tarea = self.estimaciones_tareas[i]
            
            # Si algún worker tiene carga por encima del umbral, usar carga mínima
            carga_maxima = max(self.cargas_workers)
            if carga_maxima >= self.carga_umbral:
                worker_id = self.cargas_workers.index(min(self.cargas_workers))
                estrategia = f"Carga mínima (carga máx: {carga_maxima:.2f} > umbral {self.carga_umbral})"
            else:
                worker_id = i % self.num_workers
                estrategia = f"Round-robin (carga máx: {carga_maxima:.2f} < umbral {self.carga_umbral})"
                
            asignaciones += f"Tarea {i+1} (peso {peso_tarea:.2f}) → Worker {worker_id} ({estrategia})\n"
            
            try:
                # Actualizar la carga del worker seleccionado
                self.cargas_workers[worker_id] += peso_tarea
                
                # Crear un hilo para ejecutar la tarea
                t = Thread(target=self.worker_adaptativo, args=(worker_id, tarea, peso_tarea))
                hilos.append(t)
                t.start()
            except Exception as e:
                asignaciones += f"Error asignando tarea {i+1}: {e}\n"
                
        self.crear_ventana("Asignaciones Adaptativo", f"Asignaciones realizadas:\n\n{asignaciones}")
        
        for t in hilos:
            t.join()
            
        self.mostrar_resultados()

    def worker_adaptativo(self, worker_id, tarea, peso_tarea):
        """Worker modificado que ajusta la carga al completar la tarea"""
        inicio = time.time()
        
        # Ejecutar la tarea
        try:
            resultado = tarea()
            tiempo = time.time() - inicio
            with self.lock:
                # Almacenar los resultados en el formato que espera la clase base
                while len(self.resultados[worker_id]) < len(self.tiempos[worker_id]):
                    self.resultados[worker_id].append(False)
                self.resultados[worker_id].append(True)
                self.tiempos[worker_id].append(tiempo)
                # Reducir la carga del worker una vez completada la tarea
                self.cargas_workers[worker_id] -= peso_tarea
        except Exception as e:
            tiempo = time.time() - inicio
            with self.lock:
                # Registrar el error
                while len(self.resultados[worker_id]) < len(self.tiempos[worker_id]):
                    self.resultados[worker_id].append(False)
                self.resultados[worker_id].append(False)
                self.tiempos[worker_id].append(tiempo)
                # Reducir la carga aunque haya habido un error
                self.cargas_workers[worker_id] -= peso_tarea
