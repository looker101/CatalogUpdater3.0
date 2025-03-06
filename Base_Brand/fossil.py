import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import fossil_excel, fossil_folder, price_quantity

class Fossil(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()

        #self.apply_discount(0.7)
        self.set_variant_price()

        self.quantity_0_items()
        self.safilo_get_options_variants()
        self.sort_by_handle()
        self.save_price_and_quantity_file()
        self._df.to_excel(f"{fossil_folder}/Fossil_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/Fossil_price_quantity.xlsx", index=False)

fossil = Fossil(fossil_excel)

if __name__ == "__main__":
    print("Starting Fossil brand processor")
    fossil.apply_rules()
    print("Fossil brand updated and saved successfully.")
