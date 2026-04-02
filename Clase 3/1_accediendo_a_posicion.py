import pybullet as p
import pybullet_data
import time

# Conexión y configuración inicial
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# Cargar el robot
posicion_inicial = [0, 0, 0.5] 
orientacion_inicial = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF("urdf/robot_movil.urdf", 
                      basePosition=posicion_inicial,
                      baseOrientation=orientacion_inicial)

print("Iniciando lectura de telemetría. Presiona Ctrl+C para salir.")

try:
    while True:
        # 1. Leer posición (tupla xyz) y orientación (tupla cuaternión)
        posicion, orientacion = p.getBasePositionAndOrientation(robot_id)
        
        # 2. Desempaquetar X, Y, Z
        x, y, z = posicion
        
        # 3. Convertir cuaternión a Euler (Roll, Pitch, Yaw)
        angulos_euler = p.getEulerFromQuaternion(orientacion)
        yaw = angulos_euler[2] # El yaw es el índice 2 (inclinación en Z)
        
        # 4. Imprimir los datos en consola de forma limpia
        print(f"Posición -> X: {x:.2f}m, Y: {y:.2f}m | Orientación -> Yaw: {yaw:.2f} rad")
        
        p.stepSimulation()
        time.sleep(1. / 240.)

except KeyboardInterrupt:
    print("Simulación detenida.")

p.disconnect()