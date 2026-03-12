import pybullet as p
import pybullet_data
import time

# 1. Configuración inicial
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# 2. Cargamos el robot Franka Panda (useFixedBase=True asegura que la base esté atornillada al suelo)
robot = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

# 3. Cargamos nuestro objetivo: un bloque en el suelo
# Lo ponemos un poco más cerca (X=0.4) para que el robot llegue cómodo
cubo = p.loadURDF("cube_small.urdf", [0.4, 0.0, 0.025])

# 4. Sliders para mover la "muñeca" del robot en X, Y, Z (Cinemática Inversa)
print("1. Usa X, Y, Z para ubicar la pinza sobre el cubo.")
print("2. Baja el eje Z hasta que la pinza rodee el cubo.")
print("3. Cierra la pinza con el último slider y levanta el eje Z.")
slider_x = p.addUserDebugParameter("Posicion X", 0.2, 0.7, 0.4)
slider_y = p.addUserDebugParameter("Posicion Y", -0.5, 0.5, 0.0)
slider_z = p.addUserDebugParameter("Posicion Z", 0.0, 0.8, 0.4) # Empezamos un poco alto

# 5. --- NUEVO: Slider para controlar la pinza ---
# El Panda tiene una apertura máxima de unos 0.04 metros (4 cm) por dedo.
slider_pinza = p.addUserDebugParameter("Pinza (0=Cerrada, 0.04=Abierta)", 0.0, 0.04, 0.04)

# En el modelo del Panda, el efector final (el centro de la pinza) es el eslabón 11
id_efector_final = 11 

# Bucle de simulación
while True:
    p.stepSimulation()
    
    # A. Leer posiciones para el brazo
    x = p.readUserDebugParameter(slider_x)
    y = p.readUserDebugParameter(slider_y)
    z = p.readUserDebugParameter(slider_z)
    
    # B. Calcular IK para mover el brazo hasta esa posición
    angulos = p.calculateInverseKinematics(robot, id_efector_final, [x, y, z])
    
    # C. Aplicar los ángulos a los primeros 7 motores (que son los del brazo)
    for i in range(7):
        p.setJointMotorControl2(robot, i, p.POSITION_CONTROL, angulos[i], force=100)
        
    # D. --- NUEVO: Controlar la Pinza ---
    apertura_deseada = p.readUserDebugParameter(slider_pinza)
    # En el modelo del Panda, los dedos de la pinza son las articulaciones 9 y 10.
    # Les damos mucha fuerza (force=100) para que puedan apretar el cubo sin que se resbale.
    p.setJointMotorControl2(robot, 9, p.POSITION_CONTROL, apertura_deseada, force=100)
    p.setJointMotorControl2(robot, 10, p.POSITION_CONTROL, apertura_deseada, force=100)
    
    time.sleep(1./240.)