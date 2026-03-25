import pybullet as p
import pybullet_data
import time

# 1. Iniciar la conexión con el simulador
physicsClient = p.connect(p.GUI)

# 2. Configurar la ruta a los modelos por defecto de PyBullet
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 3. Aplicar gravedad para que los objetos caigan
p.setGravity(0, 0, -9.81)

# 4. Cargar el suelo base
plano_id = p.loadURDF("plane.urdf")

# 5. Cargar el robot R2D2
# Posición: X=0, Y=0, Z=0.5 (medio metro de altura para que caiga al piso)
posicion_r2d2 = [0, 0, 0.5]
r2d2_id = p.loadURDF("r2d2.urdf", posicion_r2d2)

# 6. Cargar el brazo industrial KUKA iiwa
# Posición: X=-1 (un metro hacia atrás para que no choque con R2D2), Y=0, Z=0
# useFixedBase=True es OBLIGATORIO para que la base se ancle al piso y no se caiga
posicion_kuka = [-1, 0, 0]
kuka_id = p.loadURDF("kuka_iiwa/model.urdf", posicion_kuka, useFixedBase=True)


# 7. Demostración en consola (Imprime cuántas piezas/articulaciones tienen)
num_art_r2d2 = p.getNumJoints(r2d2_id)
num_art_kuka = p.getNumJoints(kuka_id)
print(f"El robot R2D2 tiene {num_art_r2d2} articulaciones (eslabones/joints).")
print(f"El brazo KUKA tiene {num_art_kuka} articulaciones (eslabones/joints).")

print("Simulación iniciada. Presiona Ctrl+C en la consola para detenerla.")

# 8. Bucle principal de la simulación
try:
    while True:
        p.stepSimulation()
        time.sleep(1. / 240.) # Sincronizar a 240 Hz reales
except KeyboardInterrupt:
    print("Simulación detenida por el usuario.")

# 9. Desconectar ordenadamente al cerrar
p.disconnect()