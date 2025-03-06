import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog")
from marchon_paths import NIKE_EXCEL, FERRAGAMO_EXCEL, LACOSTE_EXCEL, DRAGON_EXCEL, TODAY, marchon_price_qty_log

#from calvin_klein import Calvin_Klein
from ferragamo import Ferragamo
from lacoste import Lacoste
from nike import Nike
from dragon import Dragon
#from victoria_beckham import Victoria_Beckham

def marchon_price_qty_updater():
    marchon_brands = [
        (Ferragamo, FERRAGAMO_EXCEL),
        (Lacoste, LACOSTE_EXCEL),
        (Nike, NIKE_EXCEL),
        (Dragon, DRAGON_EXCEL)
    ]

    for brand_class, brand_file_excel in marchon_brands:
        try:
            istance = brand_class(brand_file_excel)
            istance.apply_rules()
            with open(marchon_price_qty_log, 'a') as file:
                file.write(f'   {brand_class.__name__}\'s Price and quantity are updated successfully\n')
            print(f'{brand_class.__name__}\'s Price and quantity are updated successfully\n')
        except Exception as err:
            with open(marchon_price_qty_log, 'a') as file:
                file.write(f'   {brand_class.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}\n')
                print(f'{brand_class.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}\n')

if __name__ == "__main__":
    try:
        with open(marchon_price_qty_log, 'a') as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n [{current_time}]: Starting Marchon price and quantity updater\n")
        print(f"Starting Marchon price and quantity updater")

        # Chiama la funzione principale
        marchon_price_qty_updater()

        # Scrive la chiusura del log
        with open(marchon_price_qty_log, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}]: Closing Marchon price and quantity updater\n\n")
        print(f"Closing Marchon price and quantity updater")

    except Exception as err:
        with open(marchon_price_qty_log, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}]: Marchon price and quantity are not updated due this err: \n")
            file.write(f"   {type(err).__name__}: {err}")
