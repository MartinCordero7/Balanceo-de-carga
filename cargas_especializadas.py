"""
Este módulo define cargas de trabajo especializadas para diferentes tipos de balanceadores.
Cada carga está diseñada para mostrar las fortalezas y debilidades de un algoritmo específico,
manteniendo un equilibrio para comparaciones justas entre balanceadores.
"""

import random
from tareas import calcular_primos_pesado, simulacion_montecarlo, multiplicar_matrices_gigantes
from servidor_simulado import (
    generar_tarea_calculo, generar_tarea_consulta_db, 
    generar_tarea_procesamiento_imagen, generar_conjunto_tareas
)

# Constantes para equilibrar cargas
NUM_TAREAS_ESTANDAR = 8  # Cada balanceador tendrá exactamente este número de tareas
COMPLEJIDAD_BASE = {
    "primos": 200_000,
    "montecarlo": 8_000_000,
    "matrices": 900,
}

def obtener_carga_centralizada(cluster):
    """
    Carga especializada para el balanceador centralizado:
    - Tareas homogéneas en complejidad
    - Distribución uniforme
    - Ideal para round-robin
    """
    return [
        # 8 tareas computacionales similares para distribución uniforme
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] + 10000),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"]),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] + 5000),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] - 5000),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] + 15000),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] - 10000),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] + 20000),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] - 15000),
    ]

def obtener_carga_distribuida(cluster):
    """
    Carga especializada para el balanceador distribuido:
    - Mezcla de tareas con diferentes niveles de complejidad
    - Algunas tareas muy pesadas que podrían saturar un worker
    - Beneficia la distribución aleatoria y la capacidad de rechazo
    """
    return [
        # Mezcla de tareas ligeras y pesadas para beneficiar la distribución por capacidad
        lambda: simulacion_montecarlo(COMPLEJIDAD_BASE["montecarlo"] // 2),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] // 2),
        lambda: multiplicar_matrices_gigantes(int(COMPLEJIDAD_BASE["matrices"] * 1.3)),
        lambda: simulacion_montecarlo(COMPLEJIDAD_BASE["montecarlo"]),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"]),
        lambda: multiplicar_matrices_gigantes(int(COMPLEJIDAD_BASE["matrices"] * 1.5)),
        lambda: simulacion_montecarlo(COMPLEJIDAD_BASE["montecarlo"] // 3),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] // 3),
    ]

def obtener_carga_adaptativa(cluster):
    """
    Carga especializada para el balanceador adaptativo:
    - Comienza con tareas ligeras y va incrementando la carga
    - Termina con tareas muy pesadas que provocan saturación
    - Ideal para ver el cambio de estrategia del balanceador
    """
    return [
        # Tareas que incrementan progresivamente en carga
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] // 3),
        lambda: simulacion_montecarlo(COMPLEJIDAD_BASE["montecarlo"] // 2),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] // 2),
        lambda: simulacion_montecarlo(COMPLEJIDAD_BASE["montecarlo"]),
        lambda: multiplicar_matrices_gigantes(COMPLEJIDAD_BASE["matrices"]),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"]),
        lambda: multiplicar_matrices_gigantes(int(COMPLEJIDAD_BASE["matrices"] * 1.2)),
        lambda: simulacion_montecarlo(int(COMPLEJIDAD_BASE["montecarlo"] * 1.3)),
    ]

def obtener_carga_predictiva(cluster):
    """
    Carga especializada para el balanceador predictivo:
    - Patrones repetitivos de tareas que benefician la predicción
    - Algunos cambios repentinos para probar adaptabilidad
    - Ideal para algoritmos que aprenden del historial
    """
    # Patrón repetitivo
    tareas = []
    
    # Patrón: MatricesChicas → Primos → Montecarlo → MatricesChicas
    # Repetido dos veces para aprendizaje
    for _ in range(2):
        tareas.extend([
            lambda: multiplicar_matrices_gigantes(COMPLEJIDAD_BASE["matrices"] // 2),
            lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"]),
            lambda: simulacion_montecarlo(COMPLEJIDAD_BASE["montecarlo"]),
        ])
    
    # Agregar tareas finales para completar las 8 estándar
    tareas.extend([
        lambda: multiplicar_matrices_gigantes(COMPLEJIDAD_BASE["matrices"] // 2),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] * 1.2),  # Un cambio para ver adaptabilidad
    ])
    
    return tareas

def obtener_carga_reactiva(cluster):
    """
    Carga especializada para el balanceador reactivo:
    - Tareas con alta variabilidad
    - Algunos picos de carga que causan saturación
    - Ideal para ver reacciones a sobrecargas repentinas
    """
    return [
        # Mezcla que genera picos de carga para probar reactividad
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] // 2),
        lambda: simulacion_montecarlo(COMPLEJIDAD_BASE["montecarlo"] // 2),
        # Pico de carga repentino
        lambda: multiplicar_matrices_gigantes(int(COMPLEJIDAD_BASE["matrices"] * 1.4)),
        lambda: multiplicar_matrices_gigantes(int(COMPLEJIDAD_BASE["matrices"] * 1.5)),
        # Retorno a carga normal
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"]),
        lambda: simulacion_montecarlo(COMPLEJIDAD_BASE["montecarlo"]),
        # Otro pico más moderado
        lambda: multiplicar_matrices_gigantes(int(COMPLEJIDAD_BASE["matrices"] * 1.2)),
        lambda: calcular_primos_pesado(COMPLEJIDAD_BASE["primos"] // 3),  # Tarea ligera final
    ]

def obtener_carga_servidores_especializada(cluster, tipo_balanceador):
    """
    Genera cargas de trabajo específicas para servidores según el balanceador
    """
    # Asegurar que todas las cargas de servidor tengan exactamente NUM_TAREAS_ESTANDAR tareas
    if tipo_balanceador == "centralizado":
        # Tareas homogéneas para centralizado (solo consultas a base de datos)
        return [generar_tarea_consulta_db(cluster) for _ in range(NUM_TAREAS_ESTANDAR)]
    
    elif tipo_balanceador == "distribuido":
        # Mezcla equilibrada de tipos con algunas tareas pesadas
        tareas = []
        # 3 cálculos, 3 consultas DB, 2 procesamientos imagen
        for _ in range(3):
            tareas.append(generar_tarea_calculo(cluster))
        for _ in range(3):
            tareas.append(generar_tarea_consulta_db(cluster))
        for _ in range(2):
            tareas.append(generar_tarea_procesamiento_imagen(cluster))
        return tareas
    
    elif tipo_balanceador == "adaptativo":
        # Carga progresiva de menor a mayor intensidad
        tareas = []
        # 3 consultas DB (ligeras), 3 cálculos (medias), 2 procesamiento de imágenes (pesadas)
        for _ in range(3):
            tareas.append(generar_tarea_consulta_db(cluster))
        for _ in range(3):
            tareas.append(generar_tarea_calculo(cluster))
        for _ in range(2):
            tareas.append(generar_tarea_procesamiento_imagen(cluster))
        return tareas
    
    elif tipo_balanceador == "predictivo":
        # Patrones repetitivos para beneficiar la predicción
        tareas = []
        # Patrón: consulta DB → cálculo → consulta DB → cálculo (repetido)
        for _ in range(2):
            tareas.append(generar_tarea_consulta_db(cluster))
            tareas.append(generar_tarea_calculo(cluster))
            tareas.append(generar_tarea_consulta_db(cluster))
            tareas.append(generar_tarea_calculo(cluster))
        return tareas
    
    elif tipo_balanceador == "reactivo":
        # Picos de carga para probar la reactividad
        tareas = []
        # Carga normal
        for _ in range(2):
            tareas.append(generar_tarea_consulta_db(cluster))
        # Pico de carga
        for _ in range(3):
            tareas.append(generar_tarea_procesamiento_imagen(cluster))
        # Carga normal de nuevo
        for _ in range(1):
            tareas.append(generar_tarea_calculo(cluster))
        # Otro pico de carga
        for _ in range(2):
            tareas.append(generar_tarea_procesamiento_imagen(cluster))
        return tareas
    
    # Por defecto, carga mixta equilibrada
    tareas = []
    for _ in range(3):
        tareas.append(generar_tarea_consulta_db(cluster))
    for _ in range(3):
        tareas.append(generar_tarea_calculo(cluster))
    for _ in range(2):
        tareas.append(generar_tarea_procesamiento_imagen(cluster))
    return tareas

def obtener_descripcion_carga(tipo_balanceador):
    """
    Devuelve una descripción de la carga especializada para cada balanceador
    """
    descripciones = {
        "centralizado": f"""
        CARGA ESPECIALIZADA: TAREAS HOMOGÉNEAS ({NUM_TAREAS_ESTANDAR} tareas)
        
        • Conjunto de {NUM_TAREAS_ESTANDAR} tareas de complejidad similar (cálculo de números primos)
        • Todas las tareas tienen complejidad cercana a {COMPLEJIDAD_BASE["primos"]:,} operaciones
        • Distribución uniforme sin picos de carga
        • Ideal para la asignación round-robin del balanceador centralizado
        • Muestra su eficacia cuando las tareas son predecibles
        """,
        
        "distribuido": f"""
        CARGA ESPECIALIZADA: CARGA VARIABLE ({NUM_TAREAS_ESTANDAR} tareas)
        
        • Mezcla de tareas ligeras y pesadas con complejidad equilibrada
        • {NUM_TAREAS_ESTANDAR} tareas en total con diferentes tipos (Monte Carlo, primos, matrices)
        • Incluye algunas multiplicaciones de matrices grandes que pueden saturar workers
        • Diseñada para mostrar la capacidad de rechazo y distribución por capacidad
        • Beneficia la asignación aleatoria respetando límites de capacidad
        """,
        
        "adaptativo": f"""
        CARGA ESPECIALIZADA: INCREMENTO PROGRESIVO ({NUM_TAREAS_ESTANDAR} tareas)
        
        • {NUM_TAREAS_ESTANDAR} tareas que incrementan progresivamente en dificultad
        • Comienza con tareas ligeras y va aumentando hasta tareas intensivas
        • La progresión permite observar el cambio de estrategia del balanceador
        • Diseñada para activar la adaptación entre round-robin y asignación por carga
        • Muestra cómo el balanceo se ajusta según la saturación del sistema
        """,
        
        "predictivo": f"""
        CARGA ESPECIALIZADA: PATRONES REPETITIVOS ({NUM_TAREAS_ESTANDAR} tareas)
        
        • {NUM_TAREAS_ESTANDAR} tareas con secuencias repetitivas para beneficiar la predicción
        • Patrón: matrices pequeñas → primos → Monte Carlo (repetido)
        • La repetición permite al algoritmo aprender y mejorar sus predicciones
        • Incluye algunas variaciones al final para probar la adaptabilidad
        • Ideal para algoritmos que aprenden del historial de rendimiento
        """,
        
        "reactivo": f"""
        CARGA ESPECIALIZADA: PICOS DE CARGA ({NUM_TAREAS_ESTANDAR} tareas)
        
        • {NUM_TAREAS_ESTANDAR} tareas con picos de carga estratégicamente ubicados
        • Alterna entre periodos de carga normal y picos de alta demanda
        • Incluye matrices grandes que pueden saturar temporalmente los workers
        • Diseñada para probar la capacidad de reacción ante sobrecargas
        • Muestra cómo el balanceador responde a cambios repentinos de carga
        """
    }
    
    return descripciones.get(tipo_balanceador, f"Carga de trabajo estándar ({NUM_TAREAS_ESTANDAR} tareas)")
