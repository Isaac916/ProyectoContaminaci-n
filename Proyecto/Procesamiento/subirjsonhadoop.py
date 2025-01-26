from hdfs import InsecureClient

# Configura el cliente HDFS con la URL del Namenode
HDFS_URL = 'http://namenode:50070'  # Cambia 'namenode:50070' por la URL de tu Namenode
HDFS_DIR = '/user/tu_usuario/json_files/'  # Ruta HDFS donde subirás los JSON

# Inicializa el cliente
client = InsecureClient(HDFS_URL, user='tu_usuario')  # Cambia 'tu_usuario' por tu usuario de HDFS

# Lista de archivos JSON a subir
local_json_files = ['Elche-LIMPIO.json', 'Torrevieja-LIMPIO.json', 'Orihuela-LIMPIO.json']

# Crea el directorio en HDFS si no existe
client.makedirs(HDFS_DIR)

# Sube los archivos a HDFS
for local_file in local_json_files:
    hdfs_path = HDFS_DIR + local_file  # Ruta completa en HDFS
    try:
        print(f'Subiendo {local_file} a {hdfs_path}...')
        with open(local_file, 'rb') as f:
            client.write(hdfs_path, f, overwrite=True)
        print(f'{local_file} subido correctamente.')
    except Exception as e:
        print(f'Error subiendo {local_file}: {e}')
