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
robot_id = p.loadURDF("urdf/robot_movil.urdf", [0, 0, 0.5])

# ==========================================
# 2. CREACIÓN DE UNA PARED (Obstáculo)
# ==========================================
# Creamos una forma visual y de colisión (un cubo estirado)
visual_pared = p.createVisualShape(shapeType=p.GEOM_BOX, 
                                   halfExtents=[0.1, 1.5, 0.5], 
                                   rgbaColor=[0.7, 0.2, 0.2, 1]) # Color rojizo

colision_pared = p.createCollisionShape(shapeType=p.GEOM_BOX, 
                                        halfExtents=[0.1, 1.5, 0.5])

# Colocamos la pared a 3 metros de distancia (X=3)
p.createMultiBody(baseMass=0, # Masa 0 significa que es un objeto estático (pared)
                  baseCollisionShapeIndex=colision_pared,
                  baseVisualShapeIndex=visual_pared,
                  basePosition=[3, 0, 0.5])

# ==========================================
# 3. HABILITAR SENSORES DE FUERZA
# ==========================================
# Por defecto, PyBullet no gasta recursos midiendo torque/fuerza.
# DEBEMOS activarlo explícitamente para los motores que queremos monitorear.
indice_rueda_frontal = 0 # Rueda delantera derecha
p.enableJointForceTorqueSensor(robot_id, indice_rueda_frontal, enableSensor=True)

# Velocidad para avanzar directo a la pared
velocidad_objetivo = 10.0

# Variable para controlar la cantidad de prints en consola
paso = 0

print("Robot avanzando hacia la pared. Presiona Ctrl+C para detener.")

# ==========================================
# 4. BUCLE DE EJECUCIÓN (Try/While)
# ==========================================
try:
    while True:
        # Aplicamos potencia a todos los motores para avanzar
        for i in range(4):
            p.setJointMotorControl2(
                bodyUniqueId=robot_id,
                jointIndex=i,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=velocidad_objetivo
            )

        p.stepSimulation()

        # LEER EL SENSOR DE FUERZA
        # Recordemos: estado[2] es el compartimento de fuerzas/torques
        estado = p.getJointState(robot_id, indice_rueda_frontal)
        fuerzas_reaccion = estado[2] 
        
        # El sensor devuelve 6 valores: [Fx, Fy, Fz, Mx, My, Mz]
        fuerza_x = fuerzas_reaccion[0] # Fuerza en el eje de avance
        fuerza_z = fuerzas_reaccion[2] # Fuerza vertical (peso/impacto)

        if paso % 20 == 0:
            # Imprimimos la fuerza en X para notar el choque
            if abs(fuerza_x) > 0.1: # Filtramos un poco el ruido
                print(f"Impacto detectado - Fuerza en X: {fuerza_x:.2f} N")
        
        paso+=1
        
        time.sleep(1. / 240.)

except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")
    p.disconnect()