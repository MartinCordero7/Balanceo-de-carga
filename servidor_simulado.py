import time
import random
import socket
import threading
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class ServidorSimulado:
    """Simula un servidor con capacidad limitada y tiempos de respuesta variables"""
    
    def __init__(self, nombre, capacidad=10, latencia_base=0.05):
        self.nombre = nombre
        self.capacidad = capacidad  # Máximo número de conexiones simultáneas
        self.conexiones_activas = 0
        self.latencia_base = latencia_base  # Latencia base en segundos
        self.carga_cpu = 0.1  # Comienza con baja carga
        self.disponible = True
        self.lock = threading.RLock()
        self.solicitudes_totales = 0
        self.solicitudes_rechazadas = 0
        print(f"Servidor {nombre} iniciado con capacidad {capacidad}")
    
    def procesar_solicitud(self, tipo_solicitud, datos=None):
        """Procesa una solicitud simulando carga de servidor"""
        with self.lock:
            # Verificar si podemos aceptar más conexiones
            if self.conexiones_activas >= self.capacidad:
                self.solicitudes_rechazadas += 1
                return False, "Servidor saturado, solicitud rechazada"
            
            self.conexiones_activas += 1
            self.solicitudes_totales += 1
        
        try:
            # Simular latencia de red variable
            latencia = self.latencia_base * (1 + random.random())
            time.sleep(latencia)
            
            # Diferentes tipos de solicitudes tienen diferentes cargas
            if tipo_solicitud == "calculo":
                tiempo_proceso = random.uniform(0.5, 3.0) * (1 + self.carga_cpu)
                resultado = self._realizar_calculo_complejo(datos)
            elif tipo_solicitud == "consulta_db":
                tiempo_proceso = random.uniform(0.2, 1.5) * (1 + self.carga_cpu)
                resultado = self._simular_consulta_db(datos)
            elif tipo_solicitud == "procesamiento_img":
                tiempo_proceso = random.uniform(1.0, 5.0) * (1 + self.carga_cpu)
                resultado = self._simular_procesamiento_imagen()
            else:
                tiempo_proceso = random.uniform(0.1, 0.5) * (1 + self.carga_cpu)
                resultado = "Solicitud genérica procesada"
            
            # Simular tiempo de procesamiento
            time.sleep(tiempo_proceso)
            
            # Aumentar la carga del servidor temporalmente
            self._actualizar_carga(0.05)
            
            return True, {"resultado": resultado, "tiempo": tiempo_proceso + latencia}
        finally:
            with self.lock:
                self.conexiones_activas -= 1
    
    def _actualizar_carga(self, incremento):
        """Actualiza la carga del servidor"""
        with self.lock:
            self.carga_cpu = min(0.95, self.carga_cpu + incremento)
            # La carga disminuye con el tiempo en un thread separado
            threading.Thread(target=self._disminuir_carga, daemon=True).start()
    
    def _disminuir_carga(self):
        """Disminuye gradualmente la carga del servidor"""
        time.sleep(2)  # Esperar antes de disminuir
        with self.lock:
            self.carga_cpu = max(0.1, self.carga_cpu - 0.03)
    
    def _realizar_calculo_complejo(self, datos):
        """Simula un cálculo matemático complejo"""
        if not datos or not isinstance(datos, (int, float)):
            valor = random.randint(1000, 10000)
        else:
            valor = datos
        
        # Cálculo simulado (área bajo la curva normal)
        x = np.linspace(-5, 5, int(valor/100))
        y = 1/(np.sqrt(2*np.pi)) * np.exp(-x**2/2)
        resultado = np.trapz(y, x)
        return f"Resultado del cálculo: {resultado:.6f}"
    
    def _simular_consulta_db(self, query):
        """Simula una consulta a base de datos"""
        tablas = ["usuarios", "productos", "ventas", "inventario", "clientes"]
        operaciones = ["SELECT", "INSERT", "UPDATE", "DELETE", "JOIN"]
        
        if not query:
            tabla = random.choice(tablas)
            operacion = random.choice(operaciones)
            query = f"{operacion} en tabla {tabla}"
        
        # Simular diferentes tiempos según complejidad de la consulta
        if "JOIN" in query:
            # Las JOINs son más lentas
            time.sleep(random.uniform(0.2, 0.8))
        
        registros = random.randint(5, 500)
        return f"Consulta '{query}' completada. {registros} registros procesados."
    
    def _simular_procesamiento_imagen(self):
        """Simula procesamiento de imagen"""
        dimensiones = [(800, 600), (1024, 768), (1920, 1080), (3840, 2160)]
        dim = random.choice(dimensiones)
        filtros = ["blur", "sharpen", "grayscale", "resize", "rotate"]
        filtro = random.choice(filtros)
        
        # Imágenes más grandes = más tiempo
        factor_tiempo = (dim[0] * dim[1]) / (800 * 600)
        time.sleep(random.uniform(0.1, 0.3) * factor_tiempo)
        
        return f"Imagen {dim[0]}x{dim[1]} procesada con filtro {filtro}"
    
    def obtener_estadisticas(self):
        """Devuelve estadísticas del servidor"""
        with self.lock:
            return {
                "nombre": self.nombre,
                "capacidad": self.capacidad,
                "conexiones_activas": self.conexiones_activas,
                "carga_cpu": self.carga_cpu,
                "solicitudes_totales": self.solicitudes_totales,
                "solicitudes_rechazadas": self.solicitudes_rechazadas,
                "tasa_rechazo": self.solicitudes_rechazadas / max(1, self.solicitudes_totales)
            }

class ClusterServidores:
    """Gestiona un grupo de servidores simulados"""
    
    def __init__(self, num_servidores=3):
        self.servidores = []
        for i in range(num_servidores):
            # Servidores con capacidades variables
            capacidad = random.randint(5, 15)
            latencia = random.uniform(0.03, 0.1)
            servidor = ServidorSimulado(f"Servidor-{i}", capacidad, latencia)
            self.servidores.append(servidor)
    
    def enviar_solicitud(self, servidor_id, tipo_solicitud, datos=None):
        """Envía una solicitud a un servidor específico"""
        if 0 <= servidor_id < len(self.servidores):
            return self.servidores[servidor_id].procesar_solicitud(tipo_solicitud, datos)
        return False, "Servidor no encontrado"
    
    def obtener_estadisticas_cluster(self):
        """Obtiene estadísticas de todos los servidores"""
        return [servidor.obtener_estadisticas() for servidor in self.servidores]

# Generadores de tareas que utilizan los servidores simulados
def generar_tarea_calculo(cluster, servidor_id=None):
    """Genera una tarea de cálculo intensivo"""
    if servidor_id is None:
        servidor_id = random.randint(0, len(cluster.servidores) - 1)
    
    def tarea():
        valor = random.randint(5000, 20000)
        exito, respuesta = cluster.enviar_solicitud(servidor_id, "calculo", valor)
        if not exito:
            raise Exception(f"Error en servidor {servidor_id}: {respuesta}")
        return respuesta["resultado"]
    
    return tarea

def generar_tarea_consulta_db(cluster, servidor_id=None):
    """Genera una tarea de consulta a base de datos"""
    if servidor_id is None:
        servidor_id = random.randint(0, len(cluster.servidores) - 1)
    
    def tarea():
        consultas = [
            "SELECT * FROM usuarios WHERE activo=1",
            "UPDATE productos SET precio=precio*1.05 WHERE categoria='electronics'",
            "SELECT p.nombre, c.nombre FROM productos p JOIN categorias c ON p.categoria_id = c.id",
            "DELETE FROM sesiones WHERE fecha < NOW() - INTERVAL 1 DAY"
        ]
        consulta = random.choice(consultas)
        exito, respuesta = cluster.enviar_solicitud(servidor_id, "consulta_db", consulta)
        if not exito:
            raise Exception(f"Error en servidor {servidor_id}: {respuesta}")
        return respuesta["resultado"]
    
    return tarea

def generar_tarea_procesamiento_imagen(cluster, servidor_id=None):
    """Genera una tarea de procesamiento de imagen"""
    if servidor_id is None:
        servidor_id = random.randint(0, len(cluster.servidores) - 1)
    
    def tarea():
        exito, respuesta = cluster.enviar_solicitud(servidor_id, "procesamiento_img")
        if not exito:
            raise Exception(f"Error en servidor {servidor_id}: {respuesta}")
        return respuesta["resultado"]
    
    return tarea

# Función para generar un conjunto mixto de tareas
def generar_conjunto_tareas(cluster, num_tareas=10):
    """Genera un conjunto mixto de tareas para balanceo"""
    tareas = []
    tipos_tarea = [
        generar_tarea_calculo,
        generar_tarea_consulta_db,
        generar_tarea_procesamiento_imagen
    ]
    
    for _ in range(num_tareas):
        generador = random.choice(tipos_tarea)
        tarea = generador(cluster)
        tareas.append(tarea)
    
    return tareas

# Prueba simple del simulador si se ejecuta directamente
if __name__ == "__main__":
    # Crear un clúster con 3 servidores
    cluster = ClusterServidores(3)
    
    # Generar algunas tareas de prueba
    tareas = generar_conjunto_tareas(cluster, 10)
    
    # Ejecutar las tareas y mostrar resultados
    print("\n=== PRUEBA DE TAREAS ===")
    for i, tarea in enumerate(tareas):
        try:
            inicio = time.time()
            resultado = tarea()
            tiempo = time.time() - inicio
            print(f"Tarea {i+1} completada en {tiempo:.2f}s: {resultado[:50]}...")
        except Exception as e:
            print(f"Tarea {i+1} falló: {e}")
    
    # Mostrar estadísticas del clúster
    print("\n=== ESTADÍSTICAS DEL CLÚSTER ===")
    for stats in cluster.obtener_estadisticas_cluster():
        print(f"Servidor: {stats['nombre']}")
        print(f"  Capacidad: {stats['capacidad']}, Conexiones activas: {stats['conexiones_activas']}")
        print(f"  Carga CPU: {stats['carga_cpu']:.2f}, Tasa de rechazo: {stats['tasa_rechazo']:.2%}")
        print()
