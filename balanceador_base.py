from multiprocessing import Process, Queue
from colorama import Fore, Style, init
import time

init(autoreset=True)

class BalanceadorBase:
    def __init__(self, tareas, num_workers=3):
        self.tareas = tareas
        self.num_workers = num_workers
        self.resultados = Queue()

    def worker(self, worker_id, tarea_func):
        print(Fore.CYAN + f"[WORKER {worker_id}] Iniciando tarea...")
        inicio = time.time()
        tarea_func()
        fin = time.time()
        duracion = round(fin - inicio, 2)
        self.resultados.put((worker_id, duracion))
        print(Fore.GREEN + f"[WORKER {worker_id}] Finalizó en {duracion:.2f}s")

    def mostrar_resultados(self):
        print(Fore.YELLOW + "\nResumen de ejecución:\n")
        while not self.resultados.empty():
            w_id, duracion = self.resultados.get()
            print(Fore.LIGHTBLUE_EX + f"  -> Worker {w_id} tardó {duracion} segundos")
