import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import kate_spade_excel, kate_spade_folder, price_quantity

class Kate_Spade(BaseBrand):
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

        self._df.to_excel(f"{kate_spade_folder}/KateSpade_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/KateSpade_price_quantity.xlsx", index=False)

kate_spade = Kate_Spade(kate_spade_excel)

if __name__ == "__main__":
    print("Starting Kate Spade brand processor")
    kate_spade.apply_rules()
    print("Kate Spade brand updated and saved successfully.")
