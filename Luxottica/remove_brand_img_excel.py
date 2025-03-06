import os
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import arnette_folder, burberry_folder, dolce_gabbana_folder, emporio_armani_folder, \
    giorgio_armani_folder, michael_kors_folder, miumiu_folder, oakley_folder, persol_folder, \
    prada_folder, plr_folder, ralph_folder, ray_ban_folder, swarovski_folder, tiffany_folder, versace_folder, \
    vogue_folder

# Lista di tutte le cartelle da controllare
brand_folders = [
    arnette_folder, burberry_folder, dolce_gabbana_folder, emporio_armani_folder,
    giorgio_armani_folder, michael_kors_folder, miumiu_folder, oakley_folder,
    persol_folder, prada_folder, plr_folder, ralph_folder, ray_ban_folder, swarovski_folder,
    tiffany_folder, versace_folder, vogue_folder
]

# Funzione per eliminare i file Excel se contengono "IMG" o "IMG_OK" nel nome
def delete_img_files(folder_path):
    try:
        for filename in os.listdir(folder_path):
            # Verifica se il nome del file contiene "IMG" o "IMG_OK" ed è un file Excel con estensione .xlsx
            if ("IMG" in filename or "IMG_OK" in filename) and filename.endswith(".xlsx"):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"File '{filename}' eliminato nella cartella: {folder_path}")
                    time.sleep(1)
    except FileNotFoundError:
        print(f"Attenzione: la cartella {folder_path} non esiste.")
    except Exception as err:
        print(f"Errore durante l'eliminazione dei file nella cartella {folder_path}: {type(err).__name__}, {err}")

# Itera su tutte le cartelle dei brand e chiama la funzione
for folder in brand_folders:
    delete_img_files(folder)
