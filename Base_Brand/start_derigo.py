import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog")
from de_rigo_paths import police_excel, porsche_design_excel, price_quantity, \
    logs_folder, derigo_price_qty_log

from police import Police
from porsche_design import Porsche_Design

def update_derigo_catalog():
    de_rigo_brands = [
        (Police, police_excel),
        (Porsche_Design, porsche_design_excel)
    ]
    
    for brand_class, filename in de_rigo_brands:
        try:
            istance = brand_class(filename)
            istance.apply_rules()
            with open(derigo_price_qty_log, 'a') as file:
                file.write(f'   - {brand_class.__name__}\'s Price and quantity are updated successfully\n')
            print(f'{brand_class.__name__} updated successfully')
        except Exception as err:
            with open(derigo_price_qty_log, 'a') as file:
                file.write(f'   - {brand_class.__name__}\'s price are not updated due to this error\n{type(err).__name__}: {err}\n')
            print(f"Failed to update {brand_class.__name__} due to {type(err).__name__}: {err}")
            
if __name__ == "__main__":
    try:
        with open(derigo_price_qty_log, 'a') as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{current_time}]: Starting De Rigo price and quantity updater \n")
        print(f"Starting De Rigo price and quantity updater")

        update_derigo_catalog()

        with open(derigo_price_qty_log, 'a') as file:
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}]: Closing De Rigo price and quantity updater\n\n")
        print(f"Closing De Rigo price and quantity updater\n\n")

    except Exception as err:
        with open(derigo_price_qty_log, 'a') as file:
            file.write(f"[{ending_time}]: De Rigo price and quantity are not updated due this err: \n")
            file.write(f"   {type(err).__name__}: {err}")