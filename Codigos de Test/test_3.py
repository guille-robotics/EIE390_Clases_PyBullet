import pybullet as p
import pybullet_data
import time

# 1. Configuración inicial
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
suelo = p.loadURDF("plane.urdf")

# 2. Cargamos un brazo robótico industrial (KUKA iiwa) en el origen
brazo = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0])

# --- NUEVO: LECTURA Y CONTROL DE MOTORES ---

# 3. Averiguar cuántas articulaciones tiene el robot
num_articulaciones = p.getNumJoints(brazo)
print(f"El robot tiene {num_articulaciones} articulaciones en total.\n")

# 4. Explorar qué es cada articulación
print("Detalle de las articulaciones:")
for i in range(num_articulaciones):
    info = p.getJointInfo(brazo, i)
    id_articulo = info[0]
    # El nombre viene en un formato de bytes, lo decodificamos a texto normal
    nombre = info[1].decode('utf-8') 
    tipo = info[2]
    
    # Imprimimos la información en la consola
    print(f"ID: {id_articulo} | Nombre: {nombre} | Tipo: {tipo}")

print("\nEnviando orden de movimiento al motor de la base...")

# 5. Mover una articulación específica (Control de Posición)
# Los ángulos en PyBullet (y en casi toda la robótica) se manejan en Radianes.
# 1.57 radianes son aproximadamente 90 grados.
p.setJointMotorControl2(
    bodyUniqueId=brazo,
    jointIndex=0, # Movemos la articulación con el ID 0 (la base)
    controlMode=p.POSITION_CONTROL, # Le decimos que queremos controlar la posición
    targetPosition=1.57 # El ángulo objetivo en radianes
)

# 6. Bucle de simulación
while True:
    p.stepSimulation()
    time.sleep(1./240.)