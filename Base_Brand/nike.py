import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marchon_paths import NIKE_EXCEL, NIKE_FOLDER_FTP, price_quantity

class Nike(BaseBrand):
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
        self.save_price_and_quantity_file()
        self._df.to_excel(f"{NIKE_FOLDER_FTP}/Nike_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/Nike_price_quantity.xlsx", index=False)

nike = Nike(NIKE_EXCEL)

if __name__ == "__main__":
    print("Starting Nike brand processor")
    nike.apply_rules()
    print("Nike brand updated and saved successfully.")
