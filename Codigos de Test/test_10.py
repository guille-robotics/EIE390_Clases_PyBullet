import pybullet as p
import time

p.connect(p.GUI)
p.setGravity(0, 0, -9.81)

# Usamos useFixedBase=True para que la base azul quede anclada al aire/suelo
# y no se caiga todo el conjunto por la gravedad.
mi_robot = p.loadURDF("mi_robot.urdf", useFixedBase=True)

print("Robot cargado con éxito. Observa cómo cae el brazo rojo por la gravedad.")

while True:
    p.stepSimulation()
    time.sleep(1./240.)