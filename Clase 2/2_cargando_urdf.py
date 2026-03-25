import pybullet as p
import pybullet_data
import time

# 1. Iniciar la conexión con el simulador en modo gráfico
physicsClient = p.connect(p.GUI)

# 2. Configurar la ruta para cargar modelos por defecto de PyBullet (el plano)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 3. Aplicar gravedad terrestre en el eje Z negativo
p.setGravity(0, 0, -9.81)

# 4. Cargar el suelo
plano_id = p.loadURDF("plane.urdf")

# 5. Configurar el punto de aparición de nuestro robot
# Altura de 0.5 metros (Z) para evitar que nazca incrustado en el piso
posicion_inicial = [0, 0, 0.5] 
# Orientación neutra (sin rotación)
orientacion_inicial = p.getQuaternionFromEuler([0, 0, 0])

# 6. Cargar nuestro archivo URDF personalizado
# Asegúrate de que el nombre del archivo coincida con el que guardaste
robot_id = p.loadURDF("urdf/robot_movil.urdf", 
                      basePosition=posicion_inicial,
                      baseOrientation=orientacion_inicial)

print("Simulación iniciada. Presiona Ctrl+C en la consola para detenerla.")

# 7. Bucle principal de simulación
try:
    while True:
        p.stepSimulation() # Calcula un paso de física
        time.sleep(1. / 240.) # Sincroniza la física con el tiempo real
except KeyboardInterrupt:
    print("Simulación detenida por el usuario.")

# 8. Desconectar ordenadamente al salir
p.disconnect()