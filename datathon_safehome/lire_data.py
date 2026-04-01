import os
import numpy as np

# 1. LE CHEMIN VERS LE DOSSIER (On s'arrête à '1')
folder_path = r'C:\Users\taqis\.cache\kagglehub\datasets\hungkhoi\skeleton-data-of-ntu-rgbd-60-dataset\versions\1'

# 2. VÉRIFICATION DU DOSSIER
if os.path.exists(folder_path):
    print(" Le dossier a été trouvé !")
    
    # On liste le contenu du dossier
    contenu = os.listdir(folder_path)
    print("Contenu du dossier :", contenu)

    # 3. CHARGEMENT DU FICHIER (On construit le chemin complet vers x_train.npy)
    # Assure-toi que 'x_train.npy' est bien écrit comme dans la liste 'contenu'
    file_name = "x_train.npy" # Modifie ici si le nom est différent (ex: 'NTU_60_X.npy')
    file_to_load = os.path.join(folder_path, file_name)

    if os.path.exists(file_to_load):
        print(f" Chargement de {file_name}...")
        # mmap_mode='r' lit depuis le disque sans charger en RAM (crucial pour NTU)
        data = np.load(file_to_load, mmap_mode='r')
        print("Succès ! Taille des données :", data.shape)
    else:
        print(f" Erreur : Le fichier {file_name} n'est pas dans ce dossier.")
else:
    print("Erreur : Le chemin du dossier est introuvable. Vérifie le chemin.")

