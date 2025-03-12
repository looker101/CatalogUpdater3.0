from typing import final
import pandas as pd
import openpyxl
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from kering_paths import gemini_folder

class BaseBrand:
    def __init__(self, df):
        self._df = df

    @property
    def df(self):
        return self._df

    # Set correct template suffix (Default product)
    # Fill empty cells with Default product
    # [REMOVED]  Filter to "Default product" template suffix
    def filter_for_template_suffix(self):
        """Working on Default product only"""
        self._df["Template Suffix"] = self._df["Template Suffix"].str.replace("Default Product", "Default product")
        self._df["Template Suffix"] = self._df["Template Suffix"].fillna("Default product")
        #mask = self._df["Template Suffix"] == "Default product"
        #self._df = self._df[mask]
        self._df = self._df[[
            "ID", "Handle", "Command", "Title", "Vendor", "Type", "Tags", "Tags Command",
            "Status", "Template Suffix", "URL", "Variant ID", "Variant SKU",
            "Variant Barcode", "Variant Price", "Variant Compare At Price",
            "Variant Inventory Qty", "Inventory Available: +39 05649689443",
        ]]
        return self._df

    # Set variant compare at price and Variant Price
    def set_price_with_correct_datatype(self):
        """Set Variant Compare At Price and Variant Price as numeric"""
        self._df["Variant Compare At Price"] = self._df["Variant Compare At Price"].astype("float").fillna(0)
        self._df["Variant Price"] = self._df["Variant Price"].astype("float").fillna(0)
        return self._df

    def set_variant_price(self):
        """Set Variant Price as Variant Compare At Price"""
        self._df["Variant Price"] = round(self._df["Variant Compare At Price"])
        return self._df

    # Set discount price
    def apply_discount(self, discount):
        """Apply discount to Variant Price"""

        def apply_row_discount(row):
            if row["Variant Compare At Price"] not in [0,7]:
                return int(round(row["Variant Compare At Price"] * discount, 2))
            return row["Variant Compare At Price"]

        self._df["Variant Price"] = self._df.apply(apply_row_discount, axis=1)

    # Remove all products with 0€ price
    def quantity_0_items(self):
        """Don't show products with €0 price"""

        def remove_products_0_quantity(row):
            if row["Variant Price"] in [0, 7] or pd.isna(row["Variant Price"]):
                return 0
            return row["Inventory Available: +39 05649689443"]

        self._df["Inventory Available: +39 05649689443"] = self._df.apply(remove_products_0_quantity, axis=1)
        self._df["Variant Inventory Qty"] = self._df.apply(remove_products_0_quantity, axis = 1)

    # Option value & option name: last two digits of Variant SKU (Safilo excluded)
    def get_options_variants(self):
        """Set 'Size' as the option name and the last two Variant SKU digits as the option value"""
        self._df["Option1 Name"] = "Size"
        self._df["Option1 Value"] = self._df["Variant SKU"].str[-2:]
        return self._df

    # Option value & option name: last two digits of Variant SKU for SAFILO BRANDS
    def safilo_get_options_variants(self):
        """Set 'Size' for Safilo brands"""
        self._df["Option1 Name"] = "Size"
        self._df["Option1 Value"] = self._df["Variant SKU"].str[-4:-2]
        return self._df

    def sort_by_handle(self):
        self._df = self._df.sort_values(by="Handle")
        return self._df

    # GEMINI
    # File with quantity
    # File with prices
    # def save_price_and_quantity_file(self):
    #     price_file = self._df[[
    #         "Variant SKU", "Variant Price", "Variant Compare At Price"
    #     ]]
    #     qty_file = self._df[[
    #         "Variant SKU", "Variant Inventory Qty", "Inventory Available: +39 05649689443"
    #     ]]
    #     price_file.to_csv(f"{gemini_folder}/{self.__class__.__name__}_price.csv", index=False)
    #     qty_file.to_csv(f"{gemini_folder}/{self.__class__.__name__}_qty.csv", index=False)
