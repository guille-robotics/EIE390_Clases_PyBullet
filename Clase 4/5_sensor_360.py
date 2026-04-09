import pybullet as p
import pybullet_data
import time
import math

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

robot_id = p.loadURDF("urdf/robot_movil.urdf", [0, 0, 0.1])

# ==========================================
# 2. CREAMOS UN ENTORNO (Habitación)
# ==========================================
# Creamos 3 cajas alrededor del robot para que el LiDAR las detecte
caja_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 2.0, 1.0])
visual_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.5, 2.0, 1.0], rgbaColor=[0.2, 0.5, 0.8, 1])

# Pared Norte
p.createMultiBody(baseMass=0, baseCollisionShapeIndex=caja_shape, baseVisualShapeIndex=visual_shape, basePosition=[4, 0, 1])
# Pared Sur
p.createMultiBody(baseMass=0, baseCollisionShapeIndex=caja_shape, baseVisualShapeIndex=visual_shape, basePosition=[-4, 0, 1])
# Pared Este
p.createMultiBody(baseMass=0, baseCollisionShapeIndex=caja_shape, baseVisualShapeIndex=visual_shape, basePosition=[0, 4, 1], baseOrientation=p.getQuaternionFromEuler([0,0,1.57]))

# ==========================================
# 3. CONFIGURACIÓN DEL LIDAR
# ==========================================
num_rayos = 64
rango_lidar = 6.0

# Pre-creamos líneas invisibles en PyBullet para luego solo actualizarlas (Optimización CRÍTICA)
lineas_ids = [p.addUserDebugLine([0,0,0], [0,0,0.1], lineColorRGB=[0,0,0], lifeTime=0) for _ in range(num_rayos)]

print(f"Iniciando LiDAR 360 con {num_rayos} rayos. Presiona Ctrl+C para detener.")

# ==========================================
# 4. BUCLE DE EJECUCIÓN
# ==========================================
try:
    while True:
        # Hacemos que el robot gire sobre su propio eje para ver el efecto
        p.setJointMotorControl2(robot_id, 0, p.VELOCITY_CONTROL, targetVelocity=2.0) # Der
        p.setJointMotorControl2(robot_id, 2, p.VELOCITY_CONTROL, targetVelocity=2.0) # Der
        p.setJointMotorControl2(robot_id, 1, p.VELOCITY_CONTROL, targetVelocity=-2.0) # Izq
        p.setJointMotorControl2(robot_id, 3, p.VELOCITY_CONTROL, targetVelocity=-2.0) # Izq

        p.stepSimulation()

        # Posición central del robot
        posicion_base, _ = p.getBasePositionAndOrientation(robot_id)
        rx, ry, rz = posicion_base
        z_lidar = 0.5 # Altura del sensor

        # Listas para el Batch
        lista_origenes = []
        lista_destinos = []

        # 1. CALCULAMOS LA MATEMÁTICA DEL CÍRCULO
        for i in range(num_rayos):
            # Calculamos el ángulo actual (de 0 a 2*PI)
            angulo = i * (2 * math.pi / num_rayos)
            
            # Origen: Siempre el centro del robot
            lista_origenes.append([rx, ry, z_lidar])
            
            # Destino: Trigonometría para formar el círculo
            dx = rx + (rango_lidar * math.cos(angulo))
            dy = ry + (rango_lidar * math.sin(angulo))
            lista_destinos.append([dx, dy, z_lidar])

        # 2. DISPARAMOS TODOS LOS RAYOS DE UNA SOLA VEZ
        resultados = p.rayTestBatch(lista_origenes, lista_destinos)

        # 3. PROCESAMOS RESULTADOS Y DIBUJAMOS
        for i in range(num_rayos):
            info_impacto = resultados[i]
            fraccion = info_impacto[2]
            pos_impacto = info_impacto[3]

            origen_rayo = lista_origenes[i]

            if fraccion < 1.0:
                # CHOCÓ: Dibujamos la línea en ROJO hasta el punto de impacto
                p.addUserDebugLine(origen_rayo, pos_impacto, lineColorRGB=[1, 0, 0], lineWidth=2, replaceItemUniqueId=lineas_ids[i])
            else:
                # LIBRE: Dibujamos la línea en VERDE hasta el rango máximo
                destino_rayo = lista_destinos[i]
                p.addUserDebugLine(origen_rayo, destino_rayo, lineColorRGB=[0, 1, 0], lineWidth=1, replaceItemUniqueId=lineas_ids[i])

        time.sleep(1. / 240.)

except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")
    p.disconnect()