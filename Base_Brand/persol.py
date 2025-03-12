import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import persol_folder, persol_update, lux_price_and_quantity

class Persol(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()
        self.apply_discount(0.9) #AveMaria-Luxottica brand
        self.quantity_0_items()
        self.get_options_variants()

        self._df.to_excel(f"{persol_folder}/Persol_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{lux_price_and_quantity}/Persol_price_quantity.xlsx", index=False)

persol = Persol(persol_update)

if __name__ == "__main__":
    print("Starting Persol (AveMaria) brand processor")
    persol.apply_rules()
    print("Persol brand updated and saved successfully.")
