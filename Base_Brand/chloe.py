import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/")
from kering_paths import chloe_excel, chloe_folder, price_quantity

class Chloe(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()

        #self.apply_discount(0.7)
        self.set_variant_price()

        self.quantity_0_items()
        self.get_options_variants()
        self.sort_by_handle()

        self._df.to_excel(f"{chloe_folder}/Chloe_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/Chloe_price_quantity.xlsx", index=False)

chloe = Chloe(chloe_excel)

if __name__ == "__main__":
    print("Starting Chloe brand processor")
    chloe.apply_rules()
    print("Chloe brand updated and saved successfully.")
