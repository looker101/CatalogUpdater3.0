import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import miumiu_folder, miumiu_update, lux_price_and_quantity

class Miu_Miu(BaseBrand):
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

        self._df.to_excel(f"{miumiu_folder}/MiuMiu_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{lux_price_and_quantity}/MiuMiu_price_quantity.xlsx", index=False)

miu_miu = Miu_Miu(miumiu_update)

if __name__ == "__main__":
    print("Starting Miu Miu brand processor")
    miu_miu.apply_rules()
    print("Miu Miu brand updated and saved successfully.")
