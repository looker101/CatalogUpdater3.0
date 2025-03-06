import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from de_rigo_paths import porsche_design_folder, porsche_design_excel, price_quantity

class Porsche_Design(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()
        self.set_variant_price() #AveMaria brand
        self.quantity_0_items()
        self.get_options_variants()
        self.sort_by_handle()
        self.save_price_and_quantity_file()
        self._df.to_excel(f"{porsche_design_folder}/Porsche_Design_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/Porsche_Design_price_quantity.xlsx", index=False)

porsche_design = Porsche_Design(porsche_design_excel)

if __name__ == "__main__":
    print("Starting Porsche Design (AveMaria brand) brand processor")
    porsche_design.apply_rules()
    print("Porsche Design brand updated and saved successfully.")
