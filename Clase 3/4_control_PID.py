import pybullet as p
import pybullet_data
import time
import math

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")
robot_id = p.loadURDF("urdf/robot_movil.urdf", [0, 0, 0.5])

ruedas_derechas = [0, 2]
ruedas_izquierdas = [1, 3]

# 1. Definir nuestro punto de destino (Target)
target_x = 3.0
target_y = 3.0

# 2. Constantes Proporcionales (Kp)
Kp_lineal = 2.5   # Controla qué tan rápido avanza hacia el objetivo
Kp_angular = 5.0  # Controla qué tan rápido gira para corregir el rumbo

# Variable para controlar la cantidad de prints en consola
step_counter = 0

print("=========================================")
print(f"INICIANDO NAVEGACIÓN HACIA: ({target_x}, {target_y})")
print("=========================================")

try:
    while True:
        # --- LECTURA ---
        pos, orn = p.getBasePositionAndOrientation(robot_id)
        x, y, _ = pos
        _, _, yaw = p.getEulerFromQuaternion(orn)
        
        # --- CÁLCULO DE ERRORES ---
        # Error de distancia (Teorema de Pitágoras)
        error_distancia = math.sqrt((target_x - x)**2 + (target_y - y)**2)
        
        # Error de ángulo
        angulo_deseado = math.atan2(target_y - y, target_x - x)
        error_angulo = angulo_deseado - yaw
        
        # Normalizar el error de ángulo entre -pi y pi
        error_angulo = (error_angulo + math.pi) % (2 * math.pi) - math.pi
        
        # --- LÓGICA DE CONTROL (Controlador P) ---
        if error_distancia < 0.1:
            vel_lineal = 0
            vel_angular = 0
            
            # Imprimir solo una vez por segundo cuando ya llegó para no saturar
            if step_counter % 240 == 0:
                print("\n[ ÉXITO ] ¡Objetivo alcanzado!")
                print(f"Posición Final -> X: {x:.2f}m, Y: {y:.2f}m")
        else:
            vel_lineal = Kp_lineal * error_distancia
            vel_angular = Kp_angular * error_angulo
            
            # Limitar la velocidad máxima
            vel_lineal = max(min(vel_lineal, 10.0), -10.0)
            vel_angular = max(min(vel_angular, 5.0), -5.0)

            # --- IMPRESIÓN DE DATOS (TELEMETRÍA) ---
            # Imprimimos cada 24 pasos (10 veces por segundo) para que sea legible
            if step_counter % 24 == 0:
                print("-" * 40)
                print(f"POSICIÓN ACTUAL    : X: {x:.2f}m | Y: {y:.2f}m")
                print(f"DISTANCIA RESTANTE : {error_distancia:.2f}m")
                # Convertimos radianes a grados solo para la lectura humana
                print(f"ÁNGULO ACTUAL      : {math.degrees(yaw):.1f}°")
                print(f"ÁNGULO DESEADO     : {math.degrees(angulo_deseado):.1f}°")
                print(f"ERROR ANGULAR      : {math.degrees(error_angulo):.1f}°")
                print(f"COMANDO ENVIADO    : V_Lineal: {vel_lineal:.2f} | V_Angular: {vel_angular:.2f}")

        # --- MEZCLA DIFERENCIAL ---
        vel_izq = vel_lineal - vel_angular
        vel_der = vel_lineal + vel_angular

        # --- ACCIÓN ---
        for joint in ruedas_derechas:
            p.setJointMotorControl2(robot_id, joint, p.VELOCITY_CONTROL, targetVelocity=vel_der)
        for joint in ruedas_izquierdas:
            p.setJointMotorControl2(robot_id, joint, p.VELOCITY_CONTROL, targetVelocity=vel_izq)

        p.stepSimulation()
        time.sleep(1. / 240.)
        
        # Aumentamos el contador de pasos
        step_counter += 1

except KeyboardInterrupt:
    print("\nSimulación detenida por el usuario.")

p.disconnect()