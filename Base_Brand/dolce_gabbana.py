import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import dolce_gabbana_folder, dolce_gabbana_update, lux_price_and_quantity

class Dolce_Gabbana(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()
        self.apply_discount(0.9) #Luxottica Brand
        self.quantity_0_items()
        self.get_options_variants()
        self.sort_by_handle()

        self._df.to_excel(f"{dolce_gabbana_folder}/DG_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{lux_price_and_quantity}/DG_price_quantity.xlsx", index=False)

dolce_gabbana = Dolce_Gabbana(dolce_gabbana_update )

if __name__ == "__main__":
    print("Starting D&G brand processor")
    dolce_gabbana.apply_rules()
    print("D&G brand updated and saved successfully.")
