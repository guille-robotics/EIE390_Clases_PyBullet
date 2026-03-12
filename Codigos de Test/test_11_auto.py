import pybullet as p
import pybullet_data
import time

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Cargamos el suelo
suelo = p.loadURDF("plane.urdf")

# Cargamos nuestro auto un poquito en el aire (Z=0.1) para que caiga sobre sus ruedas
auto = p.loadURDF("auto.urdf", [0, 0, 0.1])

print("Auto cargado. Arrancando motores en 3 segundos...")
for _ in range(3 * 240):
    p.stepSimulation()
    time.sleep(1./240.)

# Los IDs de las articulaciones (según el orden en que las escribimos en el XML) son:
# 0: delantera izquierda, 1: delantera derecha
# 2: trasera izquierda, 3: trasera derecha
ruedas = [0, 1, 2, 3]
velocidad_deseada = 10.0 # Radianes por segundo

print("¡Acelerando hacia adelante!")

# Le damos velocidad a las 4 ruedas
for rueda in ruedas:
    p.setJointMotorControl2(
        bodyUniqueId=auto,
        jointIndex=rueda,
        controlMode=p.VELOCITY_CONTROL, # Control por velocidad
        targetVelocity=velocidad_deseada,
        force=50 # Fuerza (Torque) máxima del motor
    )

# Bucle infinito para ver al auto alejarse
while True:
    p.stepSimulation()
    
    # Hacemos que la cámara siga al auto automáticamente
    posicion_auto, _ = p.getBasePositionAndOrientation(auto)
    p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=45, cameraPitch=-30, cameraTargetPosition=posicion_auto)
    
    time.sleep(1./240.)