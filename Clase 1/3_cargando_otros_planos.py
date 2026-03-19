import pybullet as p
import pybullet_data
import time

# 1. Conectar al simulador. Usamos p.GUI para ver la interfaz gráfica.
# Si usáramos p.DIRECT, correría en segundo plano (útil para entrenar IA rápido, pero no para enseñar).
physicsClient = p.connect(p.GUI)

# 2. PyBullet trae modelos 3D básicos por defecto. Aquí le decimos dónde encontrarlos.
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 3. Configurar la gravedad (eje X, eje Y, eje Z).
# En la Tierra, la gravedad tira hacia abajo en el eje Z a 9.81 m/s^2.
p.setGravity(0, 0, -9.81)

# 4. Cargar un plano que servirá como nuestro "suelo".
#planeId = p.loadURDF("plane.urdf")
entornoId = p.loadURDF("plane100.urdf") 


print("Simulación iniciada. Cierra la ventana o presiona Ctrl+C en la consola para terminar.")

# 5. El bucle principal de la simulación.
# PyBullet no avanza el tiempo solo; tú debes decirle explícitamente que calcule el siguiente paso.
while True:
    p.stepSimulation()
    time.sleep(1./240.) # PyBullet calcula la física a 240 Hz (240 pasos por segundo)

# 6. Desconectar al terminar (buena práctica)
p.disconnect()