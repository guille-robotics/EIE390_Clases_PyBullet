import pybullet as p
import pybullet_data
import time

# 1. Iniciar la simulación con interfaz gráfica
p.connect(p.GUI)

# 2. Decirle a PyBullet dónde buscar los modelos 3D que trae por defecto
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 3. Configurar la gravedad (eje Z hacia abajo)
p.setGravity(0, 0, -9.81)

# 4. Cargar el suelo para que nuestro robot no caiga al infinito
suelo = p.loadURDF("plane.urdf")

# 5. Definir dónde y cómo aparecerá el robot en el espacio (Cinemática Básica)
# [x, y, z] -> Lo ponemos a 1 metro de altura en el eje Z
posicion_inicial = [0, 0, 1] 

# PyBullet usa Cuaterniones para la rotación. 
# Esta función convierte ángulos de Euler (Roll, Pitch, Yaw) a Cuaterniones.
orientacion_inicial = p.getQuaternionFromEuler([0, 0, 0]) 

# 6. Cargar el modelo del robot R2D2
robot = p.loadURDF("r2d2.urdf", posicion_inicial, orientacion_inicial)

print("¡Simulación corriendo! Presiona Ctrl+C en la terminal para salir.")

# 7. El bucle de simulación
# Avanzamos el motor de físicas paso a paso
while True:
    p.stepSimulation()
    time.sleep(1./240.) # PyBullet trabaja a 240 Hz por defecto