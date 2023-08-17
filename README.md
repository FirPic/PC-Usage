# PC-Usage

**Monitoring.py - Surveiller et Enregistrer les Ressources Système**

Le script "Monitoring.py" permet de surveiller en temps réel les ressources système telles que le CPU, la mémoire, le GPU et les disques. Il recueille ces informations à des intervalles définis et les enregistre dans un fichier CSV. Les options en ligne de commande permettent de spécifier le chemin du fichier CSV et le délai entre les relevés. Le script est utile pour collecter des données de performance système pour une analyse ultérieure.

**Graphic.py - Visualiser les Données d'Utilisation des Ressources**

Le script "Graphic.py" offre une interface graphique interactive pour visualiser les données d'utilisation des ressources système enregistrées dans un fichier CSV. Il génère un graphique avec des courbes pour l'utilisation de la mémoire, du GPU et du CPU au fil du temps. En survolant le graphique, les informations détaillées d'utilisation de ressources sont affichées pour un moment spécifique. Les options en ligne de commande permettent de personnaliser le fichier CSV et la durée d'affichage. Le script est pratique pour analyser les tendances d'utilisation des ressources système sur une période donnée.

---- 

## Monitoring.py

1) **Installation des dépendances :** 

        Assurez-vous d'avoir les bibliothèques nécessaires installées en exécutant la commande suivante :

        `pip install psutil gputil`

2) **Utilisation du script :** 
   Le script prend en charge les options en ligne de commande pour personnaliser son comportement :
   
   * `-f` ou `--file`: Chemin du fichier CSV dans lequel les données seront enregistrées (par défaut : `usage_data.csv`).
   * `-d` ou `--delay`: Délai en secondes entre chaque relevé de données (par défaut : 0.001).

3) **Exécution du script :**
   Pour exécuter le script, utilisez la commande suivante en ligne de commande :
   `python Monitoring.py -f <chemin_vers_fichier_csv> -d <delai_entre_releves>`

4) **Sortie :**

        Le script enregistre périodiquement les informations de ressources système dans le fichier CSV spécifié. Les informations enregistrées comprennent le timestamp, l'utilisation de la mémoire, l'utilisation du GPU, l'utilisation du CPU (par cœur) et l'utilisation des disques.



## **Graphic.py**

1) **Installation des dépendances :**
   
   Assurez-vous d'avoir la bibliothèque matplotlib installée en exécutant la commande suivante :
   
   `pip install matplotlib`

2) **Utilisation du script :**
   
   Le script prend en charge les options en ligne de commande pour personnaliser son comportement :
   
   * `-f` ou `--file`: Chemin du fichier CSV contenant les données d'utilisation (par défaut : `usage_data.csv`).
   * `-t` ou `--time`: Durée en minutes pour laquelle les données seront affichées (par défaut : 30).

3) **Exécution du script :**
   
   Pour exécuter le script, utilisez la commande suivante en ligne de commande :
   
   `python Graphic.py -f <chemin_vers_fichier_csv> -t <duree_affichage_en_minutes>`

4) **Sortie :**
   
   Le script génère un graphique interactif qui affiche l'utilisation de la mémoire, du GPU et du CPU au fil du temps. Le graphique permet de survoler les données avec la souris, affichant les informations détaillées d'utilisation de ressources pour un moment spécifique.

    
