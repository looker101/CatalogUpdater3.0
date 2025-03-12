import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import ray_ban_folder, ray_ban_update, lux_price_and_quantity

class Ray_Ban(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()
        self.apply_discount(0.95) #Luxottica | AveMaria Brand
        self.quantity_0_items()
        self.get_options_variants()
        self.sort_by_handle()

        self._df.to_excel(f"{ray_ban_folder}/Ray-Ban_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{lux_price_and_quantity}/Ray-Ban_price_quantity.xlsx", index=False)

ray_ban = Ray_Ban(ray_ban_update)

if __name__ == "__main__":
    print("Starting Ray-Ban brand processor")
    ray_ban.apply_rules()
    print("Ray-Ban brand updated and saved successfully.")
