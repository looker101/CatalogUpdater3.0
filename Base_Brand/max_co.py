import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marcolin_paths import max_co_excel, max_co_folder, price_quantity

class Max_Co(BaseBrand):
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
        self._df.to_excel(f"{max_co_folder}/max_co_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/max_co_price_quantity.xlsx", index=False)

max_co = Max_Co(max_co_excel)

if __name__ == "__main__":
    print("Starting Max_Co brand processor")
    Max_Co.apply_rules()
    print("Max_Co brand updated and saved successfully.")
