import pybullet as p
import pybullet_data
import time

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# Cargamos el robot
robot_id = p.loadURDF("urdf/robot_movil.urdf", [0, 0, 0.1])

# ==========================================
# 2. CREAMOS UN OBSTÁCULO (Caja Azul)
# ==========================================
visual_caja = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5], rgbaColor=[0.2, 0.2, 0.8, 1])
colision_caja = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.5])

# Colocamos la caja a 6 metros de distancia en el eje X
caja_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=colision_caja, 
                            baseVisualShapeIndex=visual_caja, basePosition=[6, 0, 0.5])

# Variable para guardar la línea dibujada y poder borrarla en el siguiente frame
linea_laser = -1 
velocidad_robot = 4.0
paso = 0

print("Iniciando Raycasting. Presiona Ctrl+C para detener.")

# ==========================================
# 3. BUCLE DE EJECUCIÓN
# ==========================================
try:
    while True:
        # 1. Avanzamos el robot lentamente hacia la caja
        for i in range(4):
            p.setJointMotorControl2(robot_id, i, p.VELOCITY_CONTROL, targetVelocity=velocidad_robot)

        p.stepSimulation()

        # 2. SENSOR LiDAR (RAYCASTING)
        # Obtenemos la posición del robot para saber desde dónde disparar
        posicion_base, orientacion_base = p.getBasePositionAndOrientation(robot_id)
        robot_x, robot_y, robot_z = posicion_base

        # Configuramos el láser
        largo_rayo = 10.0
        origen = [robot_x, robot_y, 0.5] # El origen es el centro del robot, un poco levantado
        destino = [robot_x + largo_rayo, robot_y, 0.5] # Apunta 10 metros directo hacia adelante (Eje X)

        # ¡Disparamos el láser matemático!
        resultado = p.rayTest(origen, destino)
        info_impacto = resultado[0]

        # Extraemos los datos clave
        objeto_chocado = info_impacto[0]
        fraccion = info_impacto[2]
        pos_impacto = info_impacto[3]

        distancia_real = largo_rayo * fraccion

        # ==========================================
        # 4. VISUALIZACIÓN EN PANTALLA (Magia para los alumnos)
        # ==========================================
        # Borramos el láser del frame anterior (si existe)
        if linea_laser != -1:
            p.removeUserDebugItem(linea_laser)

        # Lógica de detección
        if fraccion < 1.0: 
            # ¡CHOCÓ CON ALGO! Dibujamos el láser rojo hasta el punto de impacto
            linea_laser = p.addUserDebugLine(origen, pos_impacto, lineColorRGB=[1, 0, 0], lineWidth=4)
            
            if paso % 20 == 0:
                print(f"⚠️ ¡Obstáculo detectado! ID: {objeto_chocado} | Distancia: {distancia_real:.2f} m")
                
            # Si el robot está a menos de 1.5 metros, ¡frenamos para no chocar!
            if distancia_real < 1.5:
                velocidad_robot = 0.0
        else:
            # CAMINO DESPEJADO. Dibujamos el láser verde hasta su límite de 10 metros
            linea_laser = p.addUserDebugLine(origen, destino, lineColorRGB=[0, 1, 0], lineWidth=2)
            
            if paso % 20 == 0:
                print(f"✅ Camino despejado. Viendo hasta {distancia_real:.2f} m")

        paso += 1
        time.sleep(1. / 240.)

except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")
    p.disconnect()