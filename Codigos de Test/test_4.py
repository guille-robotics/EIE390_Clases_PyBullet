import pybullet as p
import pybullet_data
import time
import math # Necesitamos math para usar el valor de Pi

# 1. Configuración inicial
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# 2. Cargamos el brazo robótico KUKA
brazo = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0])
num_articulaciones = p.getNumJoints(brazo)

# --- NUEVO: CREAR LOS SLIDERS EN LA INTERFAZ ---

# Lista para guardar la información de nuestros sliders
# Guardaremos pares de datos: (indice_del_motor, id_del_slider)
controles_motores = []

print("Creando controles deslizantes para las articulaciones móviles...")

for i in range(num_articulaciones):
    info = p.getJointInfo(brazo, i)
    nombre = info[1].decode('utf-8')
    tipo = info[2]
    
    # En PyBullet, el tipo 0 (p.JOINT_REVOLUTE) significa que es un motor que gira.
    # Solo queremos crear sliders para las partes que realmente se mueven.
    if tipo == p.JOINT_REVOLUTE:
        # Creamos el slider: nombre, valor mínimo (-180°), valor máximo (180°), valor inicial (0°)
        # Usamos radianes, por lo que -180° es -Pi y 180° es +Pi
        slider_id = p.addUserDebugParameter(nombre, -math.pi, math.pi, 0)
        
        # Guardamos qué slider controla a qué motor
        controles_motores.append((i, slider_id))

print("¡Listo! Mueve los controles en la pantalla.")



# 3. Bucle de simulación
while True:
    p.stepSimulation()
    
    # En cada paso de la simulación, leemos dónde está cada slider
    # y le mandamos esa orden al motor correspondiente
    for indice_motor, slider_id in controles_motores:
        angulo_deseado = p.readUserDebugParameter(slider_id)
        
        p.setJointMotorControl2(
            bodyUniqueId=brazo,
            jointIndex=indice_motor,
            controlMode=p.POSITION_CONTROL,
            targetPosition=angulo_deseado
        )
        
    time.sleep(1./240.)