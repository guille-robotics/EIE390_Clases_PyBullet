import pybullet as p
import pybullet_data
import time

# --- 1. CONFIGURACIÓN INICIAL ---
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# Cargar el robot con una altura inicial para evitar colisiones bruscas con el suelo
posicion_inicial = [0, 0, 0.5] 
orientacion_inicial = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF("urdf/robot_movil.urdf", 
                      basePosition=posicion_inicial,
                      baseOrientation=orientacion_inicial)

# --- 2. DEFINICIÓN DE MOTORES Y VELOCIDADES ---
# Índices basados en el URDF
ruedas_derechas = [0, 2]   # rueda_delantera_derecha, rueda_trasera_derecha
ruedas_izquierdas = [1, 3] # rueda_delantera_izquierda, rueda_trasera_izquierda

# Velocidades objetivo (radianes/segundo)
velocidad_derecha = 8.0 
velocidad_izquierda = 4.0

print("Iniciando simulación: Movimiento + Telemetría...")
print("Presiona Ctrl+C en la consola para detenerla.")

# --- 3. BUCLE PRINCIPAL ---
try:
    while True:
        # --- A. LECTURA DE TELEMETRÍA (PERCEPCIÓN) ---
        # 1. Leer posición y orientación
        posicion, orientacion = p.getBasePositionAndOrientation(robot_id)
        
        # 2. Desempaquetar X, Y, Z
        x, y, z = posicion
        
        # 3. Convertir cuaternión a Euler (Roll, Pitch, Yaw)
        angulos_euler = p.getEulerFromQuaternion(orientacion)
        yaw = angulos_euler[2] # El yaw es el índice 2 (inclinación en Z)
        
        # 4. Imprimir los datos en consola
        print(f"Posición -> X: {x:.2f}m, Y: {y:.2f}m | Orientación -> Yaw: {yaw:.2f} rad")

        # --- B. ENVÍO DE COMANDOS (ACCIÓN) ---
        # Controlar ruedas derechas
        for joint in ruedas_derechas:
            p.setJointMotorControl2(
                bodyUniqueId=robot_id,
                jointIndex=joint,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=velocidad_derecha
            )
            
        # Controlar ruedas izquierdas
        for joint in ruedas_izquierdas:
            p.setJointMotorControl2(
                bodyUniqueId=robot_id,
                jointIndex=joint,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=velocidad_izquierda
            )
            
        # --- C. AVANCE DE LA SIMULACIÓN ---
        p.stepSimulation()
        time.sleep(1. / 240.)

except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")

p.disconnect()