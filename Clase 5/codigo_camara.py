import pybullet as p
import pybullet_data
import time
import numpy as np
import cv2  # Necesario para el procesamiento de la imagen

# 1. Iniciar simulación
p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0) # Opcional: Ocultar los paneles laterales de PyBullet para ver mejor
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Cargar entorno y robot
p.loadURDF("plane.urdf")
robot_id = p.loadURDF("urdf/robot_movil.urdf", [0, 0, 0.1])

# Cargar un "obstáculo" (un cubo rojo) para que la cámara tenga algo interesante que mirar
cubo_id = p.loadURDF("cube.urdf", [1.5, 0.0, 0.1], globalScaling=0.2)
p.changeVisualShape(cubo_id, -1, rgbaColor=[1, 0, 0, 1]) # Color rojo

# =======================================================
# CONFIGURACIÓN ÓPTICA (Se hace una sola vez antes del bucle)
# =======================================================
ancho = 320
alto = 240
fov = 60.0
aspect = ancho / alto
near_val = 0.1
far_val = 100.0

# Calculamos la Matriz de Proyección (El lente)
matriz_proyeccion = p.computeProjectionMatrixFOV(fov, aspect, near_val, far_val)

# Le damos una velocidad inicial baja para que el robot avance lentamente
ruedas = [0, 1, 2, 3] # Índices de las ruedas según tu URDF
for r in ruedas:
    p.setJointMotorControl2(robot_id, r, p.VELOCITY_CONTROL, targetVelocity=2.0, force=50)

print("\n--- Simulación de Cámara Iniciada ---")

try:
    while True:
        p.stepSimulation()
        
        # =======================================================
        # 1. ACTUALIZAR POSICIÓN DE LA CÁMARA (Matriz de Vista)
        # =======================================================
        # Obtenemos la posición (X,Y,Z) y rotación (Cuaternión) actual del chasis
        pos_robot, ori_robot = p.getBasePositionAndOrientation(robot_id)
        
        # TRUCO DE PYBULLET: Usamos multiplyTransforms para calcular coordenadas locales
        # Ponemos el "ojo" de la cámara ligeramente arriba y adelante del centro (0.2 en X, 0.1 en Z)
        pos_camara, _ = p.multiplyTransforms(pos_robot, ori_robot, [0.2, 0.0, 0.1], [0, 0, 0, 1])
        
        # El objetivo a mirar está 1 metro adelante del robot en el eje X local
        punto_objetivo, _ = p.multiplyTransforms(pos_robot, ori_robot, [1.0, 0.0, 0.1], [0, 0, 0, 1])
        
        # Calculamos la Matriz de Vista dinámica
        matriz_vista = p.computeViewMatrix(
            cameraEyePosition=pos_camara,
            cameraTargetPosition=punto_objetivo,
            cameraUpVector=[0, 0, 1]
        )

        # =======================================================
        # 2. TOMAR LA FOTO (Renderizado)
        # =======================================================
        datos_camara = p.getCameraImage(
            width=ancho,
            height=alto,
            viewMatrix=matriz_vista,
            projectionMatrix=matriz_proyeccion
        )

        # =======================================================
        # 3. PROCESAMIENTO DE DATOS (El problema 1D a 3D)
        # =======================================================
        # Extraemos la imagen RGBA (Índice 2 de la tupla devuelta)
        rgb_plano = datos_camara[2]
        
        # Transformamos la "lista plana" a una matriz (Alto, Ancho, 4 canales) 
        # y ASEGURAMOS que el tipo de dato sea uint8 (0-255) para OpenCV
        imagen_rgba = np.array(rgb_plano, dtype=np.uint8).reshape((alto, ancho, 4))
        
        # OpenCV usa BGR, PyBullet entrega RGBA. Convertimos el formato:
        imagen_bgr = cv2.cvtColor(imagen_rgba, cv2.COLOR_RGBA2BGR)

        # =======================================================
        # 4. VISUALIZACIÓN
        # =======================================================
        cv2.imshow("Vision del Robot (OpenCV)", imagen_bgr)
        cv2.waitKey(1) # Pequeña pausa requerida por OpenCV para refrescar la ventana

        time.sleep(1./240.) # Sincronizar física

except KeyboardInterrupt:
    cv2.destroyAllWindows()
    p.disconnect()