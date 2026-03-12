import pybullet as p
import pybullet_data
import time
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración inicial (esta vez podemos usar p.DIRECT si no queremos ver la interfaz 3D, 
# pero usemos p.GUI para ver ambas cosas)
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")

# Carguemos un par de cosas para que la foto no salga vacía
p.loadURDF("cube_small.urdf", [0, 0, 0.025])
robot = p.loadURDF("r2d2.urdf", [0.5, 0.5, 0.5])

# Dejamos que la simulación corra un ratito para que R2D2 caiga al suelo
for _ in range(100):
    p.stepSimulation()
    time.sleep(1./240.)

# --- NUEVO: CONFIGURACIÓN DE LA CÁMARA VIRTUAL ---
ancho = 640
alto = 480

print("Configurando cámara y tomando fotografía...")

# A. Dónde está la cámara [X, Y, Z] y a dónde mira [X, Y, Z]
matriz_vista = p.computeViewMatrix(
    cameraEyePosition=[1.5, 1.5, 1.0], # Cámara flotando arriba y a la derecha
    cameraTargetPosition=[0, 0, 0.2],  # Mirando hacia el centro (donde está el cubo)
    cameraUpVector=[0, 0, 1]           # El eje Z es "hacia arriba"
)

# B. El lente de la cámara (Ángulo de visión FOV, Aspect Ratio, Rango de visión)
matriz_proyeccion = p.computeProjectionMatrixFOV(
    fov=60.0,
    aspect=ancho / alto,
    nearVal=0.1,
    farVal=100.0
)



# C. ¡Click! Tomamos la foto
# Esta función es pesada, devuelve ancho, alto, RGB, Profundidad y Segmentación
imagenes = p.getCameraImage(ancho, alto, matriz_vista, matriz_proyeccion)

# D. Procesamiento de la imagen (PyBullet entrega un formato especial de OpenGL)
# El índice 2 de la tupla 'imagenes' contiene los píxeles de color.
# Vienen en una lista plana, así que usamos numpy para darle forma de matriz de imagen (Alto, Ancho, 4 canales RGBA)
arreglo_rgba = np.reshape(imagenes[2], (alto, ancho, 4))

# Nos quedamos solo con los canales RGB (cortamos la transparencia/Alpha)
imagen_rgb = arreglo_rgba[:, :, :3]

print("¡Foto capturada! Abriendo visor...")

# Ocultar la ventana de PyBullet temporalmente si quieres, o cerrarla
p.disconnect()

# E. Mostrar la foto usando Matplotlib
plt.imshow(imagen_rgb)
plt.title("Visión Artificial: Imagen capturada desde PyBullet")
plt.axis('off') # Ocultamos los ejes para que parezca una foto real
plt.show()