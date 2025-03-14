import pandas as pd
from Base_brand import BaseBrand
import openpyxl
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marcolin_paths import guess_excel, guess_folder, price_quantity

class Guess(BaseBrand):
    def __init__(self, filename):
        self._df = pd.read_excel(filename)

    def apply_rules(self):
        self._df["Vendor"] = self._df["Vendor"].str.title()
        self.filter_for_template_suffix()
        self.set_price_with_correct_datatype()
        self.set_variant_price()
        self.quantity_0_items()
        self.get_options_variants()
        self.sort_by_handle()

        self._df.to_excel(f"{guess_folder}/guess_price_quantity.xlsx", index=False)
        self._df.to_excel(f"{price_quantity}/guess_price_quantity.xlsx", index=False)

guess = Guess(guess_excel)

if __name__ == "__main__":
    print("Starting Guess brand processor")
    guess.apply_rules()
    print("guess brand updated and saved successfully.")
