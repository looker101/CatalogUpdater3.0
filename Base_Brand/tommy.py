import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import tommy_hilfiger_excel, tommy_hilfiger_folder, price_quantity

class Tommy_Hilfiger(BaseBrand):
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
        self._df.to_excel(f"{tommy_hilfiger_folder}/Tommy_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/Tommy_price_quantity.xlsx", index=False)

# Instantiate and run the adidas_sport processor
tommy_hilfiger = Tommy_Hilfiger(tommy_hilfiger_excel)

if __name__ == "__main__":
    print("Starting Tommy Hilfiger brand processor")
    tommy_hilfiger.apply_rules()
    print("Tommy Hilfiger brand updated and saved successfully.")
