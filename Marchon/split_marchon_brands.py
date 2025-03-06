import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
import pandas as pd
import time
from marchon_paths import MARCHON_BACKUP, FTP_SHOPIFY_FOLDER

def get_shopify_brands():
    print("All Marchon's brand on LookerOnline will be split by brand")

    df = pd.read_excel(MARCHON_BACKUP)
    
    # Filter by items with "Default Product" as template suffix value
    #mask = df["Template Suffix"] == "Default Product"
    #df = df[mask]

    df["Vendor"] = df["Vendor"].str.replace("Lacoste", "LACOSTE")
    
    shopify_brands = df["Vendor"].unique()
    print(f"Extracting for: {shopify_brands}")

    for brand in shopify_brands:
        time.sleep(1)
        mask = df["Vendor"] == brand
        file_brand = df[mask]

        file_brand = file_brand[[
            "Variant SKU", "Variant Barcode", "Variant Price", "Variant Compare At Price", "Variant Inventory Qty",
            "ID", "Handle", "Command", "Title", "Body HTML", "Vendor", "Type", "Template Suffix", "URL",
            "Total Inventory Qty", "Option1 Name", "Option1 Value", "Inventory Available: +39 05649689443",
            "Metafield: title_tag [string]", "Metafield: description_tag [string]",
            "Metafield: my_fields.frame_color [single_line_text_field]",
            "Metafield: my_fields.frame_shape [single_line_text_field]",
            "Metafield: my_fields.frame_material [single_line_text_field]",
            "Metafield: my_fields.product_size [single_line_text_field]",
            "Metafield: my_fields.for_who [single_line_text_field]"

        ]]

        file_brand.to_excel(f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marchon/{brand.capitalize()}/{brand}.xlsx", index = False)
        print(f"File \"Shopify Items\" salvato per il brand {brand}")

if __name__ == "__main__":
    try:
        print("Starting file_shopify_brand_FTP")
        get_shopify_brands()
        print("All Marchon's brand are splitted correctly!")
    except Exception as err:
        print(f"Marchon's brands are not splitted due this error: {type(err).__name__} -> {err}")
