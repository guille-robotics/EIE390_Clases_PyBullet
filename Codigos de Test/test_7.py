import pybullet as p
import pybullet_data
import time

# 1. Configuración inicial
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# 2. Cargamos el brazo robótico KUKA
brazo = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0])
num_articulaciones = p.getNumJoints(brazo)
id_efector_final = num_articulaciones - 1 

# 3. --- NUEVO: AGREGAR UN OBJETO FÍSICO (CUBO) ---
# pybullet_data trae un modelo de un cubo pequeño ya configurado con masa y colisiones
# Lo colocamos en [0.5, 0, 0.1] para que quede justo frente al robot, apoyado en el suelo
cubo = p.loadURDF("cube_small.urdf", [0.5, 0.0, 0.1])

# 4. Nuestro objetivo visual (esfera roja translúcida para que no tape la vista)
forma_esfera = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=0.04, rgbaColor=[1, 0, 0, 0.5])
# baseMass=0 significa que es "fantasma", no le afecta la gravedad ni choca con nada
esfera_objetivo = p.createMultiBody(baseMass=0, baseVisualShapeIndex=forma_esfera, basePosition=[0.5, 0, 0.5])

# 5. Controles deslizantes para mover el objetivo
print("Usa los sliders para acercar el robot al cubo y empujarlo.")
slider_x = p.addUserDebugParameter("Objetivo X", -0.8, 0.8, 0.6)
slider_y = p.addUserDebugParameter("Objetivo Y", -0.8, 0.8, 0.0)
slider_z = p.addUserDebugParameter("Objetivo Z", 0.05, 1.0, 0.3)

# 6. Bucle de simulación
while True:
    p.stepSimulation()
    
    # A. Leer posiciones de los sliders
    obj_x = p.readUserDebugParameter(slider_x)
    obj_y = p.readUserDebugParameter(slider_y)
    obj_z = p.readUserDebugParameter(slider_z)
    posicion_objetivo = [obj_x, obj_y, obj_z]
    
    # B. Mover el objetivo visual
    p.resetBasePositionAndOrientation(esfera_objetivo, posicion_objetivo, [0, 0, 0, 1])
    
    # C. Calcular Cinemática Inversa
    angulos_calculados = p.calculateInverseKinematics(brazo, id_efector_final, posicion_objetivo)
    
    # D. Mover los motores aplicando un torque máximo
    for i in range(num_articulaciones):
        info = p.getJointInfo(brazo, i)
        if info[2] == p.JOINT_REVOLUTE:
            p.setJointMotorControl2(
                bodyUniqueId=brazo, 
                jointIndex=i, 
                controlMode=p.POSITION_CONTROL, 
                targetPosition=angulos_calculados[i],
                force=50  # --- NUEVO: Fuerza (Torque) máxima del motor en Newtons/metro ---
            )
            
    time.sleep(1./240.)