import pybullet as p
import pybullet_data
import time
import math

# 1. Configuración inicial
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# 2. Cargamos el brazo robótico
brazo = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0])
num_articulaciones = p.getNumJoints(brazo)

# Identificamos el último eslabón (el efector final o "mano" del robot)
# Generalmente es el índice total menos 1
id_efector_final = num_articulaciones - 1 

# 3. Crear los sliders en la interfaz
controles_motores = []
for i in range(num_articulaciones):
    info = p.getJointInfo(brazo, i)
    if info[2] == p.JOINT_REVOLUTE:
        slider_id = p.addUserDebugParameter(info[1].decode('utf-8'), -math.pi, math.pi, 0)
        controles_motores.append((i, slider_id))

# Variable para guardar el ID del texto en pantalla y poder actualizarlo sin crear copias
texto_id = None

print("Mueve los sliders y observa cómo cambian las coordenadas en pantalla.")

# 4. Bucle de simulación
while True:
    p.stepSimulation()
    
    # A. Mover el robot leyendo los sliders
    for indice_motor, slider_id in controles_motores:
        angulo_deseado = p.readUserDebugParameter(slider_id)
        p.setJointMotorControl2(brazo, indice_motor, p.POSITION_CONTROL, targetPosition=angulo_deseado)
        
    # B. --- NUEVO: LEER LA POSICIÓN (CINEMÁTICA DIRECTA) ---
    
    # getLinkState devuelve mucha info. La posición [X, Y, Z] es el primer elemento (índice 0).
    estado_eslabon = p.getLinkState(brazo, id_efector_final)
    posicion_xyz = estado_eslabon[0] 
    
    # Formateamos los números a 3 decimales para que no sea un número gigante
    texto_coordenadas = f"X: {posicion_xyz[0]:.3f} | Y: {posicion_xyz[1]:.3f} | Z: {posicion_xyz[2]:.3f}"

    print(f"X: {posicion_xyz[0]:.3f} | Y: {posicion_xyz[1]:.3f} | Z: {posicion_xyz[2]:.3f}")
    
    # C. Mostrar las coordenadas flotando arriba del robot
    # Si es la primera vez, creamos el texto. Si ya existe, lo reemplazamos.
    if texto_id is None:
        texto_id = p.addUserDebugText(texto_coordenadas, textPosition=[0, 0, 1.5], textColorRGB=[1, 0, 0], textSize=1.5)
    else:
        texto_id = p.addUserDebugText(texto_coordenadas, textPosition=[0, 0, 1.5], textColorRGB=[1, 0, 0], textSize=1.5, replaceItemUniqueId=texto_id)

    time.sleep(1./240.)