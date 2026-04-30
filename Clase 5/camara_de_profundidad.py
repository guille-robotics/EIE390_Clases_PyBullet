import pybullet as p
import pybullet_data
import time
import numpy as np
import cv2

# =======================================================
# 1. INICIALIZACIÓN DEL ENTORNO
# =======================================================
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Opcional: Ocultar los paneles laterales de PyBullet para ver mejor
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

# Cargar piso y robot
p.loadURDF("plane.urdf")
robot_id = p.loadURDF("urdf/robot_movil.urdf", [0, 0, 0.1])

# Cargar un "obstáculo" (cubo rojo) para que la cámara lo vea
cubo_id = p.loadURDF("cube.urdf", [1.5, 0.0, 0.1], globalScaling=0.2)
p.changeVisualShape(cubo_id, -1, rgbaColor=[1, 0, 0, 1])

# =======================================================
# 2. CONFIGURACIÓN ÓPTICA DEL LENTE (Se hace una vez)
# =======================================================
ancho = 320
alto = 240
fov = 60.0
aspect = ancho / alto
near_val = 0.1
far_val = 100.0

# Matriz de Proyección (El lente estático)
matriz_proyeccion = p.computeProjectionMatrixFOV(fov, aspect, near_val, far_val)

# Le damos una velocidad inicial al robot para que avance
ruedas = [0, 1, 2, 3] # Índices de articulaciones según tu URDF
for r in ruedas:
    p.setJointMotorControl2(robot_id, r, p.VELOCITY_CONTROL, targetVelocity=10.0, force=50)

print("\n--- Simulación de Cámara y Profundidad Iniciada ---")

# =======================================================
# 3. BUCLE PRINCIPAL DE SIMULACIÓN
# =======================================================
try:
    while True:
        p.stepSimulation()
        
        # --- A. ACTUALIZAR POSICIÓN DE LA CÁMARA ---
        pos_robot, ori_robot = p.getBasePositionAndOrientation(robot_id)
        
        # Posición del lente (0.2m adelante, 0.1m arriba del centro)
        pos_camara, _ = p.multiplyTransforms(pos_robot, ori_robot, [0.2, 0.0, 0.1], [0, 0, 0, 1])

       # Hacia dónde mira (1.0m adelante, pero ahora mirando hacia abajo en Z)
        punto_objetivo, _ = p.multiplyTransforms(pos_robot, ori_robot, [1.0, 0.0, 0.05], [0, 0, 0, 1])
        
        # Matriz de Vista dinámica
        matriz_vista = p.computeViewMatrix(
            cameraEyePosition=pos_camara,
            cameraTargetPosition=punto_objetivo,
            cameraUpVector=[0, 0, 1]
        )

        # --- B. TOMAR LA FOTO ---
        datos_camara = p.getCameraImage(
            width=ancho,
            height=alto,
            viewMatrix=matriz_vista,
            projectionMatrix=matriz_proyeccion
        )

        # --- C. PROCESAR IMAGEN A COLOR (RGB) ---
        rgb_plano = datos_camara[2]
        # Aseguramos formato uint8 (0-255) para evitar el error de OpenCV
        imagen_rgba = np.array(rgb_plano, dtype=np.uint8).reshape((alto, ancho, 4))
        imagen_bgr = cv2.cvtColor(imagen_rgba, cv2.COLOR_RGBA2BGR)

        # --- D. PROCESAR IMAGEN DE PROFUNDIDAD (DEPTH) ---
        depth_plano = datos_camara[3]
        depth_buffer = np.reshape(depth_plano, (alto, ancho))
        
        # Linealización: Convertir Z-Buffer a Metros reales
        profundidad_metros = far_val * near_val / (far_val - (far_val - near_val) * depth_buffer)
        
        # Escalar a 0-255 para poder visualizarlo en pantalla
        profundidad_visual = (depth_buffer * 255).astype(np.uint8)

        # Imprimir en consola la distancia al objeto central
        distancia_frente = profundidad_metros[alto//2, ancho//2]
        print(f"Distancia al frente: {distancia_frente:.2f} metros", end='\r') # end='\r' sobreescribe la línea

        # --- E. VISUALIZACIÓN EN OPENCV ---
        cv2.imshow("Vision del Robot (Color)", imagen_bgr)
        cv2.imshow("Mapa de Profundidad", profundidad_visual)
        cv2.waitKey(1)

        # Sincronizar con el motor físico (240 Hz)
        time.sleep(1./240.)

except KeyboardInterrupt:
    print("\nSimulación terminada.")
    cv2.destroyAllWindows()
    p.disconnect()