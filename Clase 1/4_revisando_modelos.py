import os
import pybullet_data

# Obtener la ruta de datos por defecto
path_data = pybullet_data.getDataPath()

# Listar todos los archivos .urdf en esa carpeta
modelos = [f for f in os.listdir(path_data) if f.endswith(".urdf")]

print("Modelos URDF disponibles en pybullet_data:")
for modelo in modelos:
    print("- " + modelo)