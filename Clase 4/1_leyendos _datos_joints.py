import pybullet as p
import pybullet_data
import time

# ==========================================
# 1. INICIALIZAR LA API
# ==========================================
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
# Agregamos gravedad para que las ruedas tengan fricción con el suelo
p.setGravity(0, 0, -9.81) 

# ==========================================
# 2. CARGAR EL MUNDO Y EL ROBOT
# ==========================================
plano_id = p.loadURDF("plane.urdf")
# Cargamos el robot ligeramente elevado en Z (0.5) para que caiga al suelo
robot_id = p.loadURDF("urdf/robot_movil.urdf", [0, 0, 0.5])

# ==========================================
# 3. CONFIGURAR MOTORES
# ==========================================
# Índices de los motores según el URDF
ruedas_derechas = [0, 2] 
ruedas_izquierdas = [1, 3] 

# Velocidades objetivo (radianes/segundo)
velocidad_derecha = 8.0 
velocidad_izquierda = 4.0

# Variable para controlar la cantidad de prints en consola
paso = 0

print("Iniciando movimiento y lectura de sensores...\n")

# ==========================================
# 4. BUCLE DE SIMULACIÓN (Paso 1 al 200)
# ==========================================
try:
    while True:
    
        # --- A) ENVIAR COMANDOS DE MOVIMIENTO ---
        # Ruedas derechas
        for joint in ruedas_derechas:
            p.setJointMotorControl2(
                bodyUniqueId=robot_id,
                jointIndex=joint,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=velocidad_derecha
            )
            
        # Ruedas izquierdas
        for joint in ruedas_izquierdas:
            p.setJointMotorControl2(
                bodyUniqueId=robot_id,
                jointIndex=joint,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=velocidad_izquierda
            )
            
        # Avanzamos un "frame" en el motor físico
        p.stepSimulation()
        
        # --- B) LEER SENSORES TRAS EL MOVIMIENTO ---
        # 1. GPS (Posición global del chasis)
        posicion_base, orientacion_base = p.getBasePositionAndOrientation(robot_id)
        x, y, z = posicion_base
        
        # 2. Encoder (Estado de la rueda delantera derecha)
        estado_rueda_dd = p.getJointState(robot_id, 0)
        posicion_rueda = estado_rueda_dd[0]  # Radianes acumulados
        velocidad_rueda = estado_rueda_dd[1] # Radianes/segundo actuales
        
        # --- C) MOSTRAR RESULTADOS ---
        if paso % 20 == 0:
            print(f"--- Paso de simulación: {paso} ---")
            print(f"GPS     -> Chasis en X: {x:.3f} m, Y: {y:.3f} m")
            print(f"Encoder -> Rueda DD ha girado {posicion_rueda:.3f} rad totales, girando a {velocidad_rueda:.3f} rad/s\n")

        paso+=1
            
        time.sleep(1. / 240.)

except KeyboardInterrupt:
    print("Simulación detenida.")

# ==========================================
# 5. CERRAR EL SIMULADOR
# ==========================================
p.disconnect()
print("Simulación completada con éxito.")