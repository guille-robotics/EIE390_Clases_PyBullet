import pybullet as p
import pybullet_data
import time
import matplotlib.pyplot as plt
from collections import deque

# ==========================================
# 1. CONFIGURACIÓN INICIAL DE PYBULLET
# ==========================================
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

robot_id = p.loadURDF("urdf/robot_movil.urdf", [0, 0, 0.5])

# Creamos la pared a 3 metros
visual_pared = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=[0.1, 1.5, 0.5], rgbaColor=[0.7, 0.2, 0.2, 1])
colision_pared = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=[0.1, 1.5, 0.5])
p.createMultiBody(baseMass=0, baseCollisionShapeIndex=colision_pared, baseVisualShapeIndex=visual_pared, basePosition=[3, 0, 0.5])

# Habilitar el sensor en la rueda
indice_rueda_frontal = 0
p.enableJointForceTorqueSensor(robot_id, indice_rueda_frontal, enableSensor=True)

velocidad_objetivo = 10.0
paso = 0

# ==========================================
# 2. CONFIGURACIÓN DE LA GRÁFICA EN TIEMPO REAL
# ==========================================
plt.ion() # Activamos el modo interactivo de Matplotlib
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_title("Sensor de Fuerza X (Impacto contra la pared)")
ax.set_xlabel("Pasos de Simulación")
ax.set_ylabel("Fuerza Fx (Newtons)")
ax.grid(True)

# Creamos la línea vacía que iremos actualizando
linea_fuerza, = ax.plot([], [], 'r-', linewidth=2, label="Fuerza X")
ax.legend()

# Usamos 'deque' para crear una ventana móvil (solo guardamos los últimos 300 datos)
# Esto hace que la gráfica avance como un osciloscopio
historial_pasos = deque(maxlen=300)
historial_fuerzas = deque(maxlen=300)

print("Robot avanzando. Observa la gráfica de fuerza. Presiona Ctrl+C en la consola para detener.")

# ==========================================
# 3. BUCLE DE EJECUCIÓN
# ==========================================
try:
    while True:
        # 1. Mover el robot
        for i in range(4):
            p.setJointMotorControl2(bodyUniqueId=robot_id, jointIndex=i,
                                    controlMode=p.VELOCITY_CONTROL, targetVelocity=velocidad_objetivo)

        p.stepSimulation()

        # 2. Leer el sensor
        estado = p.getJointState(robot_id, indice_rueda_frontal)
        fuerzas_reaccion = estado[2] 
        fuerza_x = fuerzas_reaccion[0]

        # 3. Guardar datos para la gráfica
        historial_pasos.append(paso)
        historial_fuerzas.append(fuerza_x)

        # 4. Actualizar la gráfica (cada 10 pasos para no ralentizar la simulación)
        if paso % 10 == 0:
            linea_fuerza.set_xdata(historial_pasos)
            linea_fuerza.set_ydata(historial_fuerzas)
            
            # Ajustar los límites de la gráfica automáticamente
            ax.relim()
            ax.autoscale_view()
            
            # Dibujar los nuevos datos sin bloquear el código
            fig.canvas.draw()
            fig.canvas.flush_events()

            # Opcional: seguir imprimiendo impactos fuertes en la consola
            if abs(fuerza_x) > 5.0:
                print(f"Impacto fuerte detectado: {fuerza_x:.2f} N")

        paso += 1
        time.sleep(1. / 240.)

except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")
    
    # Mantener la ventana de la gráfica abierta al final
    plt.ioff()
    plt.show()
    p.disconnect()