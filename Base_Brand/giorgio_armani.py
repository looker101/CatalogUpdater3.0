import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import giorgio_armani_folder, giorgio_armani_update, lux_price_and_quantity

class Giorgio_Armani(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()
        self.apply_discount(0.9) #Luxottica Brand
        self.quantity_0_items()
        self.get_options_variants()
        self.sort_by_handle()

        self._df.to_excel(f"{giorgio_armani_folder}/Giorgio_Armani_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{lux_price_and_quantity}/Giorgio_Armani_price_quantity.xlsx", index=False)

giorgio_armani = Giorgio_Armani(giorgio_armani_update)

if __name__ == "__main__":
    print("Starting Giorgio Armani brand processor")
    giorgio_armani.apply_rules()
    print("Giorgio Armani brand updated and saved successfully.")
