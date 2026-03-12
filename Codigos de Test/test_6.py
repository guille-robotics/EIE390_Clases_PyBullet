import pybullet as p
import pybullet_data
import time

# 1. Configuración inicial
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# 2. Cargamos el brazo robótico
brazo = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0])
num_articulaciones = p.getNumJoints(brazo)
id_efector_final = num_articulaciones - 1 

# 3. --- NUEVO: CREAR UN OBJETIVO VISUAL (Esfera Roja) ---
# Creamos una forma visual de esfera de 5 cm de radio, color rojo (RGB + Transparencia)
forma_esfera = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=0.05, rgbaColor=[1, 0, 0, 1])
# Colocamos la esfera en el mundo (baseMass=0 significa que flota, no le afecta la gravedad)
esfera_objetivo = p.createMultiBody(baseMass=0, baseVisualShapeIndex=forma_esfera, basePosition=[0.5, 0, 0.5])

# 4. Controles deslizantes para mover la esfera en X, Y, Z
print("Mueve los sliders de X, Y, Z para cambiar la posición del objetivo.")
slider_x = p.addUserDebugParameter("Objetivo X", -0.8, 0.8, 0.4)
slider_y = p.addUserDebugParameter("Objetivo Y", -0.8, 0.8, 0.0)
slider_z = p.addUserDebugParameter("Objetivo Z", 0.1, 1.2, 0.4)

# 5. Bucle de simulación
while True:
    p.stepSimulation()
    
    # A. Leemos la posición deseada desde los sliders
    obj_x = p.readUserDebugParameter(slider_x)
    obj_y = p.readUserDebugParameter(slider_y)
    obj_z = p.readUserDebugParameter(slider_z)
    posicion_objetivo = [obj_x, obj_y, obj_z]
    
    # B. Movemos la esfera roja a esa posición para verla
    p.resetBasePositionAndOrientation(esfera_objetivo, posicion_objetivo, [0, 0, 0, 1])
    
    # C. --- MAGIA PURA: CÁLCULO DE CINEMÁTICA INVERSA ---
    # Le pasamos el robot, el efector final y la coordenada. 
    # PyBullet nos devuelve una lista con los ángulos ideales para cada motor.
    angulos_calculados = p.calculateInverseKinematics(brazo, id_efector_final, posicion_objetivo)
    
    # D. Aplicamos esos ángulos a los motores del robot
    for i in range(num_articulaciones):
        info = p.getJointInfo(brazo, i)
        if info[2] == p.JOINT_REVOLUTE:
            # Enviamos la orden de posición a cada motor individual
            p.setJointMotorControl2(
                bodyUniqueId=brazo, 
                jointIndex=i, 
                controlMode=p.POSITION_CONTROL, 
                targetPosition=angulos_calculados[i]
            )
            
    time.sleep(1./240.)