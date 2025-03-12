import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from kering_paths import amq_excel, amq_folder, price_quantity

class Alexander_McQueen(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        #self._df["Vendor"] = self._df["Vendor"].str.title()
        self._df["Vendor"] = "Alexander McQueen"
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()

        #self.apply_discount(0.7)
        self.set_variant_price()

        self.quantity_0_items()
        self.get_options_variants()
        self.sort_by_handle()
    
        self._df.to_excel(f"{amq_folder}/AMQ_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/AMQ_price_quantity.xlsx", index=False)

amq = Alexander_McQueen(amq_excel)

if __name__ == "__main__":
    print("Starting amq brand processor")
    amq.apply_rules()
    print("amq brand updated and saved successfully.")
