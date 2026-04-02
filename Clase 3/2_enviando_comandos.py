import pybullet as p
import pybullet_data
import time

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")
robot_id = p.loadURDF("urdf/robot_movil.urdf", [0, 0, 0.5])

# Definimos qué articulación (joint) corresponde a qué rueda
# El orden depende de cómo se declararon en el XML del URDF
ruedas_derechas = [0, 2] # rueda_delantera_derecha, rueda_trasera_derecha
ruedas_izquierdas = [1, 3] # rueda_delantera_izquierda, rueda_trasera_izquierda

# Velocidades objetivo (radianes/segundo)
# Para girar en círculo, aplicamos más velocidad a una rueda
velocidad_derecha = 8.0 
velocidad_izquierda = 4.0

print("Enviando comandos a los motores...")

try:
    while True:
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
            
        p.stepSimulation()
        time.sleep(1. / 240.)

except KeyboardInterrupt:
    print("Simulación detenida.")

p.disconnect()