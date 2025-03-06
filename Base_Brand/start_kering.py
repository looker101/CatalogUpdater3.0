import sys
import pandas as pd
import time
import datetime
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog")

from kering_paths import amq_excel, balenciaga_excel, bottega_veneta_excel, chloe_excel,\
    gucci_excel, sl_excel, kering_price_qty_log

from amq import Alexander_McQueen
from balenciaga import Balenciaga
from bottega_veneta import Bottega_Veneta
from chloe import Chloe
from gucci import Gucci
from saint_laurent import Saint_Laurent

def kering_price_qty_updater():
    kering_brands = [
        (Alexander_McQueen, amq_excel),
        (Balenciaga, balenciaga_excel),
        (Bottega_Veneta, bottega_veneta_excel),
        (Chloe, chloe_excel),
        (Gucci, gucci_excel),
        (Saint_Laurent, sl_excel)
    ]

    for brand_class, brand_file_excel in kering_brands:
        try:
            istance = brand_class(brand_file_excel)
            istance.apply_rules()

            with open(kering_price_qty_log, 'a') as file:
                file.write(f'   -{brand_class.__name__}\'s Price and quantity are updated successfully\n')
            print(f'{brand_class.__name__}\'s Price and quantity are updated successfully')
            time.sleep(1)

        except Exception as err:
            with open(kering_price_qty_log, 'a') as file:
                file.write(f'   -{brand_class.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}\n')
            print(f'{brand_class.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}')
            time.sleep(1)

if __name__ == "__main__":
    try:
        with open(kering_price_qty_log, 'a') as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n [{current_time}]: Starting Kering price and quantity updater\n")
        print(f"Starting Kering price and quantity updater")

        # Chiama la funzione principale
        kering_price_qty_updater()

        # Scrive la chiusura del log
        with open(kering_price_qty_log, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}] Closing Kering price and quantity updater\n")
        print(f"Closing Kering price and quantity updater\n")

    except Exception as err:
        with open(kering_price_qty_log, 'a') as file:
            file.write(f"Kering price and quantity are not updated due this err: \n")
            file.write(f"   {type(err).__name__}: {err}")
            file.write(f"[{ending_time}] Closing Kering price and quantity updater\n")
