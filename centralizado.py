from multiprocessing import Process
from balanceador_base import BalanceadorBase
from colorama import Fore

class BalanceadorCentralizado(BalanceadorBase):
    def ejecutar(self):
        print(Fore.MAGENTA + "\n== BALANCEO CENTRALIZADO ==")
        procesos = []
        for i, tarea in enumerate(self.tareas):
            worker_id = i % self.num_workers
            print(Fore.LIGHTMAGENTA_EX + f"Asignando Tarea {i+1} a Worker {worker_id}")
            p = Process(target=self.worker, args=(worker_id, tarea))
            procesos.append(p)
            p.start()

        for p in procesos:
            p.join()

        self.mostrar_resultados()
