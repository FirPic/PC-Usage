import psutil
import time
import GPUtil
import csv
import os

def get_cpu_usage():
    return psutil.cpu_percent(interval=1, percpu=True)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_gpu_usage():
    gpus = GPUtil.getGPUs()
    if gpus:
        return gpus[0].load * 100  # Utilisation du premier GPU
    else:
        return 0  # Aucun GPU détecté, renvoyer 0%

def get_disk_usages():
    disk_usages = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usages[partition.device] = usage.percent
    return disk_usages

# Nom du fichier CSV
csv_filename = 'usage_data.csv'

# Vérifier si le fichier CSV existe déjà
csv_exists = os.path.exists(csv_filename)

# Ouvrir le fichier CSV en mode append si le fichier existe, sinon en mode écriture
mode = 'a' if csv_exists else 'w'

# Déterminer les noms de colonnes
fieldnames = ['timestamp', 'memory_usage', 'gpu_usage', 'cpu_usage']
partitions = psutil.disk_partitions()
disk_fieldnames = [partition.device for partition in partitions]
fieldnames.extend(disk_fieldnames)

# Ouvrir le fichier CSV en mode append ou écriture
with open(csv_filename, mode, newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if not csv_exists:
        writer.writeheader()

    while True:
        timestamp = time.time()
        memory_usage = format(get_memory_usage(), '.2f')
        gpu_usage = format(get_gpu_usage(), '.2f')
        cpu_usage = get_cpu_usage()
        disk_usages = get_disk_usages()
    
        row = {
            'timestamp': timestamp,
            'memory_usage': memory_usage,
            'gpu_usage': gpu_usage,
            'cpu_usage': cpu_usage
        }
        row.update(disk_usages)
        writer.writerow(row)
        csvfile.flush()  # Pour s'assurer que les données sont écrites immédiatement sur le disque

        print(f"Timestamp: {timestamp} | Memory Usage: {memory_usage}% | GPU Usage: {gpu_usage}% | CPU Usage: {cpu_usage} | Disk Usages: {disk_usages}")
        
        time.sleep(0.001)
