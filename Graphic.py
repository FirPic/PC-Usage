
# Importation des bibliothèques nécessaires
import csv  # Module pour la manipulation de fichiers CSV
import matplotlib.pyplot as plt  # Module pour la création de graphiques
from datetime import datetime, timedelta  # Module pour la manipulation de dates et heures
import bisect
from matplotlib.widgets import Cursor

csv_filename = "usage_data.csv"  # Nom du fichier CSV contenant les données d'utilisation
time_show = 30 # Visualition des donner pour x minutes 

# Définition de la fonction pour calculer la moyenne d'une liste de valeurs
def calculer_moyenne(valeurs):    
    somme = sum(valeurs)  # Calcul de la somme des valeurs
    nombre_elements = len(valeurs)  # Calcul du nombre d'éléments dans la liste
    moyenne = somme / nombre_elements  # Calcul de la moyenne
    return moyenne

def find_nearest_timecode(target_timecode):
    data = []
    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    timestamps = [float(row['timestamp']) for row in data]
    index = bisect.bisect_left(timestamps, target_timecode)

    if index == 0:
        return (
            data[0]['memory_usage'],
            data[0]['gpu_usage'],
            data[0]['cpu_usage']
        )
    if index == len(data):
        return (
            data[-1]['memory_usage'],
            data[-1]['gpu_usage'],
            data[-1]['cpu_usage']
        )

    prev_timestamp = float(data[index - 1]['timestamp'])
    next_timestamp = float(data[index]['timestamp'])

    if abs(prev_timestamp - target_timecode) < abs(next_timestamp - target_timecode):
        return (
            data[index - 1]['memory_usage'],
            data[index - 1]['gpu_usage'],
            data[index - 1]['cpu_usage']
        )
    else:
        return (
            data[index]['memory_usage'],
            data[index]['gpu_usage'],
            data[index]['cpu_usage']
        )


# Définition de la fonction pour tracer les données combinées
def plot_combined_data():
    # Initialisation des listes pour stocker les données
    timestamps = []  # Liste pour stocker les horodatages
    memory_usages = []  # Liste pour stocker les utilisations de mémoire
    gpu_usages = []  # Liste pour stocker les utilisations du GPU
    cpu_usages = []  # Liste pour stocker les utilisations du CPU
    disk_usages = {}  # Dictionnaire pour stocker les utilisations des disques

    # Ouverture du fichier CSV contenant les données d'utilisation
    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)  # Création d'un lecteur de CSV
        for row in reader:  # Parcours des lignes du fichier CSV
            timestamp = float(row['timestamp'])  # Extraction du timestamp
            
            # Vérification si le timestamp est dans la dernière heure
            if datetime.now() - datetime.fromtimestamp(timestamp) <= timedelta(minutes=time_show):
                timestamps.append(timestamp)  # Ajout du timestamp à la liste
                memory_usages.append(float(row['memory_usage']))  # Ajout de l'utilisation de la mémoire
                gpu_usages.append(float(row['gpu_usage']))  # Ajout de l'utilisation du GPU
                
                cpu_core_usage = eval(row['cpu_usage'])  # Extraction de l'utilisation de chaque cœur de CPU
                cpu_usage = calculer_moyenne(cpu_core_usage)  # Calcul de la moyenne de l'utilisation du CPU
                cpu_usages.append(cpu_usage)  # Ajout de l'utilisation moyenne du CPU

                # Parcours des données d'utilisation des disques
                for disk_name, disk_usage in row.items():
                    if disk_name.startswith('/') and disk_name != 'timestamp':
                        # Création d'une liste associée au nom du disque s'il n'existe pas encore
                        disk_usages.setdefault(disk_name, []).append(float(disk_usage))

    # Création de la figure pour le tracé
    plt.figure(figsize=(10, 6))

    # Tracé de l'utilisation de la mémoire
    mem_line, = plt.plot(timestamps, memory_usages, label='Utilisation de la mémoire')

    # Tracé de l'utilisation du GPU
    gpu_line, = plt.plot(timestamps, gpu_usages, label='Utilisation du GPU')

    # Tracé de l'utilisation moyenne du CPU
    cpu_line, = plt.plot(timestamps, cpu_usages, label='Utilisation moyenne du CPU')

    # Tracé de l'utilisation des disques
    disk_lines = []
    for disk_name, disk_usage_list in disk_usages.items():
        disk_line, = plt.plot(timestamps, disk_usage_list, label=f'Disque {disk_name}')
        disk_lines.append(disk_line)

    # Configurations des axes et du titre du graphe
    plt.xlabel('Horodatage')
    plt.ylabel('Utilisation (%)')
    plt.title('Utilisation du système au fil du temps')
    plt.legend()
    plt.grid()


    '''
    lors du survole du graphique, on recupere la coordonne d'abcisses, on recherche dans le fichier csv, le cote temps le plus proche et 
    on sauvegarde les info associe sur l'utilisation de la RAM, GPU, CPU.
    Ensuite on place pour la RAM, GPU, CPU un point en fonction de x = abcisses et y = la valeur des cles  RAM, GPU, CPU.
    on affiche la valeur des cles RAM, GPU, CPU dans la legends.
    le tout doit pouvoir etre modifier a chaque deplacement de la souris
    
    mettre en œuvre une interaction avec un graphique qui affiche des données sur l'utilisation de la RAM, du GPU et du CPU. Vous voulez que les données associées 
    à la position en x (abscisse) du curseur de la souris soient récupérées depuis un fichier CSV, puis affichées sous forme de points sur le graphique pour 
    chaque métrique (RAM, GPU, CPU), avec des légendes correspondantes.
    
    '''
    
    hover_line, = plt.plot([], [], color='gray', linestyle='--')  # Création du tracé de survol initial
    
    def on_hover(event):
        if event.inaxes == plt.gca():
            x_value = event.xdata
            memory_usage, gpu_usage, cpu_core_usages = find_nearest_timecode(x_value)
            cpu_core_usages = cpu_core_usages.replace("[","").replace("]","").split(',') # Transforme la chaine de caractere en list
            cpu_usage=calculer_moyenne([float(cpu_core_usage) for cpu_core_usage in cpu_core_usages]) # Calcul de la moyenne de l'utilisation du CPU
            
            plt.gcf().canvas.draw_idle()
            
            memory_usage = float(memory_usage)
            gpu_usage = float(gpu_usage)
            cpu_usage = float(cpu_usage)
            
            datetime_x = datetime.fromtimestamp(x_value)
        
            text = f"Temps: {datetime_x}\nRAM: {memory_usage:.2f}%\nGPU: {gpu_usage:.2f}%\nCPU: {cpu_usage:.2f}%"
            legend_text.set_text(text)
            
            # Mise à jour des données du tracé de survol
            hover_line.set_data([x_value, x_value], [0, 100])
            plt.gcf().canvas.draw_idle()


    legend_text = plt.gca().text(-0.15, 1.02, '', transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))
    plt.gcf().canvas.mpl_connect('motion_notify_event', on_hover)
    cursor = Cursor(plt.gca(), useblit=True, color='red', linewidth=1)




    # Affichage du graphe
    plt.show()

# Appel de la fonction pour tracer les données combinées
plot_combined_data()
