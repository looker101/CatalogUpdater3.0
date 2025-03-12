import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from kering_paths import sl_excel, sl_folder, price_quantity

class Saint_Laurent(BaseBrand):
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

        self._df.to_excel(f"{sl_folder}/Saint_Laurent_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/Saint_Laurent_price_quantity.xlsx", index=False)

saint_laurent = Saint_Laurent(sl_excel)

if __name__ == "__main__":
    print("Starting Saint Laurent brand processor")
    saint_laurent.apply_rules()
    print("Saint Laurent brand updated and saved successfully.")
