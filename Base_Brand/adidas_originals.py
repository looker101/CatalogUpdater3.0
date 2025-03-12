import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marcolin_paths import adidas_originals_excel, adidas_originals_folder, price_quantity

# Load brand data
#brand_df = pd.read_excel(adidas_originals_excel)

class Adidas_Originals(BaseBrand):
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
        self._df.to_excel(f"{adidas_originals_folder}/Adidas_Originals_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/Adidas_Originals_price_quantity.xlsx", index=False)

adidas_originals = Adidas_Originals(adidas_originals_excel)

if __name__ == "__main__":
    print("Starting adidas_originals brand processor")
    adidas_originals.apply_rules()
    print("adidas_originals brand updated and saved successfully.")
