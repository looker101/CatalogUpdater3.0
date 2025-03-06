import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from de_rigo_paths import police_folder, police_excel, price_quantity

class Police(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()
        self.apply_discount(0.9) #AveMaria brand
        self.quantity_0_items()
        self.get_options_variants()
        self.sort_by_handle()
        self.save_price_and_quantity_file()
        self._df.to_excel(f"{police_folder}/Police_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/Police_price_quantity.xlsx", index=False)

police = Police(police_excel)

if __name__ == "__main__":
    print("Starting Police (AveMaria brand) brand processor")
    police.apply_rules()
    print("Police brand updated and saved successfully.")
