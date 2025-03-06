import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import marc_jacobs_excel, marc_jacobs_folder, price_quantity

class Marc_Jacobs(BaseBrand):
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
        self._df.to_excel(f"{marc_jacobs_folder}/MJ_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/MJ_price_quantity.xlsx", index=False)

marc_jacobs = Marc_Jacobs(marc_jacobs_excel)

if __name__ == "__main__":
    print("Starting Marc Jacobs brand processor")
    marc_jacobs.apply_rules()
    print("Marc Jacobs brand updated and saved successfully.")
