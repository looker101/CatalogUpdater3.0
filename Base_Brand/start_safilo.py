import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog")
from safilo_paths import carrera_excel, david_beckham_excel, fossil_excel, kate_spade_excel, marc_jacobs_excel, \
    moschino_excel, polaroid_excel, tommy_hilfiger_excel, under_armour_excel, safilo_price_qty_logs

from carrera import Carrera
from david_beckham import David_Beckham
from fossil import Fossil
from kate_spade import Kate_Spade
from marc_jacobs import Marc_Jacobs
from moschino import Moschino
from polaroid import Polaroid
from tommy import Tommy_Hilfiger
from under_armour import Under_Armour

def update_safilo_catalog():
    safilo_brands = [
        (Carrera, carrera_excel),
        (David_Beckham, david_beckham_excel),
        (Fossil, fossil_excel),
        (Kate_Spade, kate_spade_excel),
        (Marc_Jacobs, marc_jacobs_excel),
        (Moschino, moschino_excel),
        (Polaroid, polaroid_excel),
        (Tommy_Hilfiger, tommy_hilfiger_excel),
        (Under_Armour, under_armour_excel)
    ]

    for brand_class, brand_file_excel in safilo_brands:
        try:
            istance = brand_class(brand_file_excel)
            istance.apply_rules()
            with open(safilo_price_qty_logs, 'a') as file:
                file.write(f'   -{brand_class.__name__}\'s Price and quantity are updated successfully\n')
            print(f'{brand_class.__name__}\'s Price and quantity are updated successfully\n')
        except Exception as err:
            with open(safilo_price_qty_logs, 'a') as file:
                file.write(f'   -{brand_class.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}\n')
                print(f'{brand_class.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}\n')
            
if __name__ == "__main__":
    try:
        with open(safilo_price_qty_logs, 'a') as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n [{current_time}]: Starting Safilo price and quantity updater\n")
        print(f"Starting Safilo price and quantity updater")

        # Chiama la funzione principale
        update_safilo_catalog()

        # Scrive la chiusura del log
        with open(safilo_price_qty_logs, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}]: Closing Safilo price and quantity updater\n\n")
        print(f"Closing Safilo price and quantity updater")

    except Exception as err:
        with open(safilo_price_qty_logs, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}]: Safilo price and quantity are not updated due this err: \n")
            file.write(f"   {type(err).__name__}: {err}")
            file.write(f"[{ending_time}]: Closing Safilo price and quantity updater\n\n")