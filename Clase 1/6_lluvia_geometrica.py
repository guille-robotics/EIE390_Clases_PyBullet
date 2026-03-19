import pybullet as p
import pybullet_data
import time

# Configuración inicial (Idéntica al script anterior)
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# Ajustar la cámara para ver mejor el espectáculo
p.resetDebugVisualizerCamera(cameraDistance=5.0, 
                             cameraYaw=45.0, 
                             cameraPitch=-30.0, 
                             cameraTargetPosition=[0, 0, 1])

# 1. CREAR UNA ESFERA AZUL
colSphere = p.createCollisionShape(p.GEOM_SPHERE, radius=0.5)
visSphere = p.createVisualShape(p.GEOM_SPHERE, radius=0.5, rgbaColor=[0, 0, 1, 1])
p.createMultiBody(baseMass=2.0, 
                  baseCollisionShapeIndex=colSphere, 
                  baseVisualShapeIndex=visSphere, 
                  basePosition=[2, 0, 3])

# 2. CREAR UN CILINDRO VERDE
colCyl = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.3, height=1.0)
visCyl = p.createVisualShape(p.GEOM_CYLINDER, radius=0.3, rgbaColor=[0,1,0,1])
p.createMultiBody(baseMass=1.5, 
                  baseCollisionShapeIndex=colCyl, 
                  baseVisualShapeIndex=visCyl, 
                  basePosition=[-2, 0, 3])

# 3. GENERACIÓN PROCEDURAL: TORRE DE CUBOS
# Creamos la geometría base UNA SOLA VEZ para ahorrar memoria
colBox = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.2, 0.2, 0.2])
#visBox = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.2, 0.2, 0.2], rgbaColor=[1, 1, 0, 1]) # Amarillo

print("Generando torre de cubos...")

# Bucle for para crear 10 cubos, uno encima del otro
for i in range(1,10):
    # basePosition va aumentando en Z en cada iteración
    visBox = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.2, 0.2, 0.2], rgbaColor=[1/i, 1/2*i, 0, 1]) # Cambios en el codigo para modificar color
    p.createMultiBody(baseMass=0.5,
                      baseCollisionShapeIndex=colBox,
                      baseVisualShapeIndex=visBox,
                      basePosition=[0, 0, 1 + (i * 0.5)]) 

# Bucle de simulación estándar
try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    pass

p.disconnect()