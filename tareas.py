import numpy as np
import random

def calcular_primos_pesado(n=1_000_000):
    primos = []
    for num in range(2, n):
        es_primo = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                es_primo = False
                break
        if es_primo:
            primos.append(num)
    return len(primos)  # Devolver cantidad de primos encontrados

def multiplicar_matrices_gigantes(tamano=3000):
    A = np.random.rand(tamano, tamano)
    B = np.random.rand(tamano, tamano)
    return np.dot(A, B)  # Devolver resultado (aunque sea muy grande)

def simulacion_montecarlo(iteraciones=30_000_000):
    dentro = 0
    for _ in range(iteraciones):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            dentro += 1
    pi_aprox = (dentro / iteraciones) * 4
    return pi_aprox  # Devolver aproximación de PI
