import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import under_armour_excel, under_armour_folder, price_quantity

class Under_Armour(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()
        self.set_variant_price() #AveMaria Brand
        self.quantity_0_items()
        self.safilo_get_options_variants()
        self.sort_by_handle()
        self._df.to_excel(f"{under_armour_folder}/UnderArmour_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/UnderArmour_price_quantity.xlsx", index=False)

under_armour = Under_Armour(under_armour_excel)

if __name__ == "__main__":
    print("Starting Under Armour (AveMaria) brand processor")
    under_armour.apply_rules()
    print("Under Armour brand updated and saved successfully.")
