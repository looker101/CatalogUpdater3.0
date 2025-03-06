import pandas as pd
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog")

from luxottica_paths import arnette_update, burberry_update, dolce_gabbana_update, \
    emporio_armani_update, giorgio_armani_update, michael_kors_update, miumiu_update, \
    oakley_update, persol_update, prada_update, plr_update, ralph_update, ray_ban_update, \
    swarovski_update, tiffany_update, versace_update, vogue_update, luxottica_price_qty_log

from arnette import Arnette
from burberry import Burberry
from dolce_gabbana import Dolce_Gabbana
from emporio_armani import Emporio_Armani
from giorgio_armani import Giorgio_Armani
from michael_kors import Michael_Kors
from miu_miu import Miu_Miu
from oakley import Oakley
from persol import Persol
from prada import Prada
from prada_linea_rossa import Prada_Linea_Rossa
from ralph import Ralph
from ray_ban import Ray_Ban
from swarovski import Swarovski
from tiffany import Tiffany
from versace import Versace
from vogue import Vogue

def luxottica_price_qty_updater():
    luxottica_brands = [
        (Arnette, arnette_update),
        (Burberry, burberry_update),
        (Dolce_Gabbana, dolce_gabbana_update),
        (Emporio_Armani, emporio_armani_update),
        (Giorgio_Armani, giorgio_armani_update),
        (Michael_Kors, michael_kors_update),
        (Miu_Miu, miumiu_update),
        (Oakley, oakley_update),
        (Persol, persol_update),
        (Prada, prada_update),
        (Prada_Linea_Rossa, plr_update),
        (Ralph, ralph_update),
        (Ray_Ban, ray_ban_update),
        (Swarovski, swarovski_update),
        (Tiffany, tiffany_update),
        (Versace, versace_update),
        (Vogue, vogue_update)
    ]
    
    for brand_class, brand_file_excel in luxottica_brands:
        try:
            istance = brand_class(brand_file_excel)
            istance.apply_rules()
            with open(luxottica_price_qty_log, 'a') as file:
                file.write(f'   - {brand_class.__name__}\'s Price and quantity are updated successfully\n')
            print(f'{brand_class.__name__}\'s Price and quantity are updated successfully\n')
        except Exception as err:
            with open(luxottica_price_qty_log, 'a') as file:
                file.write(f'   - {brand_class.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}\n')
            print(f'{brand_class.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}\n')
            
if __name__ == "__main__":
    try:
        with open(luxottica_price_qty_log, 'a') as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n [{current_time}]: Starting Luxottica price and quantity updater\n")
        print(f"Starting Luxottica price and quantity updater")

        # Chiama la funzione principale
        luxottica_price_qty_updater()

        # Scrive la chiusura del log
        with open(luxottica_price_qty_log, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}]: Closing Luxottica price and quantity updater\n\n")
        print(f"Closing Luxottica price and quantity updater")

    except Exception as err:
        with open(luxottica_price_qty_log, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"Luxottica price and quantity are not updated due this err: \n")
            file.write(f"   {type(err).__name__}: {err}")
            file.write(f"[{ending_time}]: Closing Luxottica price and quantity updater\n\n")
