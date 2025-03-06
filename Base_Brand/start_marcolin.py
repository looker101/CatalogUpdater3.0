import pandas as pd
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog")
from marcolin_paths import adidas_originals_excel, adidas_sport_excel, guess_excel, max_co_excel, \
    max_mara_excel, pucci_excel, timberland_excel, tom_ford_excel, web_excel, zegna_excel, marcolin_price_qty_log

from adidas_originals import Adidas_Originals
from adidas_sport import Adidas_Sport
from guess import Guess
from max_co import Max_Co
from max_mara import Max_Mara
from pucci import Emilio_Pucci
from timberland import Timberland
from tom_ford import Tom_Ford
from web import Web
from zegna import Zegna

def marcolin_price_qty_updater():
    marcolin_brands = [
        (Adidas_Originals, adidas_originals_excel),
        (Adidas_Sport, adidas_sport_excel),
        (Guess, guess_excel),
        (Max_Co, max_co_excel),
        (Max_Mara, max_mara_excel),
        (Emilio_Pucci, pucci_excel),
        (Timberland, timberland_excel),
        (Tom_Ford, tom_ford_excel),
        (Web, web_excel),
        (Zegna, zegna_excel)
    ]

    for brand_clss, brand_file_excel in marcolin_brands:
        try:
            istance = brand_clss(brand_file_excel)
            istance.apply_rules()

            # Scrive il log del successo
            with open(marcolin_price_qty_log, 'a') as file:
                file.write(f'   {brand_clss.__name__}\'s Price and quantity are updated successfully\n')
            print(f'{brand_clss.__name__}\'s Price and quantity are updated successfully')
        except Exception as err:
            # Scrive il log dell'errore
            with open(marcolin_price_qty_log, 'a') as file:
                file.write(f'   {brand_clss.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}\n')
            print(f'{brand_clss.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}')

if __name__ == "__main__":
    try:
        with open(marcolin_price_qty_log, 'a') as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n [{current_time}]: Starting Marcolin price and quantity updater\n")
        print(f"Starting Marcolin price and quantity updater")

        # Chiama la funzione principale
        marcolin_price_qty_updater()

        # Scrive la chiusura del log
        with open(marcolin_price_qty_log, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}]: Closing Marcolin price and quantity updater\n")
        print(f"Closing Marcolin price and quantity updater")

    except Exception as err:
        with open(marcolin_price_qty_log, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}]: Marcolin price and quantity are not updated due this err: \n")
            file.write(f"   {type(err).__name__}: {err}")