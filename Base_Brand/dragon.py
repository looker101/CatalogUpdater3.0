import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marchon_paths import DRAGON_EXCEL, DRAGON_FOLDER_FTP, price_quantity

class Dragon(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()
        self.set_variant_price()
        self.quantity_0_items()
        self.get_options_variants()
        self.sort_by_handle()

        self._df.to_excel(f"{DRAGON_FOLDER_FTP}/Dragon_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/Dragon_price_quantity.xlsx", index=False)

# Instantiate and run the adidas_sport processor
dragon = Dragon(DRAGON_EXCEL)

if __name__ == "__main__":
    print("Starting Dragon brand processor")
    dragon.apply_rules()
    print("Dragon brand updated and saved successfully.")
