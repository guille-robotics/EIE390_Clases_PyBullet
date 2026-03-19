import pybullet as p
import pybullet_data
import time

# 1. INICIAR EL SERVIDOR DE SIMULACIÓN
# p.GUI abre la ventana visual. Si usaramos p.DIRECT, correría en la consola sin gráficos.
physicsClient = p.connect(p.GUI)

# 2. CONFIGURAR EL ENTORNO
# Le decimos a PyBullet dónde encontrar los modelos por defecto (como el plano)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Configuramos la gravedad hacia abajo en el eje Z (-9.81 m/s^2)
p.setGravity(0, 0, -9.81)

# Cargamos el suelo para que los objetos no caigan al vacío infinito
planoId = p.loadURDF("plane.urdf")

# 3. CREAR NUESTRO PRIMER OBJETO (Un cubo rojo)
# Paso A: Forma de colisión (física)
colBoxId = p.createCollisionShape(shapeType=p.GEOM_BOX, 
                                  halfExtents=[0.5, 0.5, 0.5])

# Paso B: Forma visual (gráfica) - Le damos color rojo (R, G, B, Alpha)
visBoxId = p.createVisualShape(shapeType=p.GEOM_BOX, 
                               halfExtents=[0.5, 0.5, 0.5], 
                               rgbaColor=[127, 255, 0, 1])

# Paso C: Ensamblar el cuerpo en el espacio
# baseMass=1.0 hace que tenga masa y la gravedad lo afecte.
# basePosition=[0, 0, 3] lo ubica en el centro (X=0, Y=0) y a 3 metros de altura (Z=3).
cajaId = p.createMultiBody(baseMass=1.0,
                           baseCollisionShapeIndex=colBoxId, #Si comentamos esta linea veremos como la figura atraviesa el suelo.
                           baseVisualShapeIndex=visBoxId,
                           basePosition=[0, 0, 3])

# Hacemos que la caja sea un poco más elástica (rebotará más)
p.changeDynamics(cajaId, -1, restitution=0.8)

print("Iniciando simulación. Presiona Ctrl+C en la terminal para detener.")

# 4. BUCLE DE SIMULACIÓN (El motor del tiempo)
try:
    while True:
        # Avanzar el cálculo físico un paso (por defecto 1/240 segundos)
        p.stepSimulation()
        
        # Extraer la posición actual del cubo
        posicion, orientacion = p.getBasePositionAndOrientation(cajaId)
        
        # Imprimir la altura (coordenada Z, que es el índice 2 de la lista 'posicion')
        # Usamos \r para que se sobrescriba en la misma línea de la consola
        print(f"Altura de la caja: {posicion[2]:.3f} metros", end="\r")
        
        # Sincronizar el tiempo del simulador con el tiempo real para poder verlo
        time.sleep(1./240.)
        
except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")

# 5. CERRAR CONEXIÓN
p.disconnect()