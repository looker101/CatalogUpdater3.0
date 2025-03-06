import pandas as pd
import os
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import luxottica_folder, luxottica_backup, products_out_folder, out_products

def old_products():
    print("Starting the process to identify old products...")
    for filename in os.listdir(luxottica_folder):
        if filename.startswith("Item Master Data") and filename.endswith(".xlsx"):
            luxottica_file = pd.read_excel(os.path.join(luxottica_folder, filename))
            print(f"Found Luxottica file: {filename}")
            break
        time.sleep(1)
    else:
        raise FileNotFoundError("Nessun file trovato che inizi con 'Item Master Data' nel percorso specificato.")
    print("Reading Shopify's Luxottica file")
    shopify_file = pd.read_excel(luxottica_backup)
    print("Shopify file loaded successfully")
    time.sleep(1)

    #luxottica_file["Brand Name"] = luxottica_file["Brand Name"].str.replace("Vogue", "Vogue Eyewear")
    #shopify_file["Vendor"] = shopify_file["Vendor"].str.replace("Vogue", "Vogue Eyewear")

    # Rinomino una colonna per poter fare il merge
    luxottica_file.rename(columns={"UPC": "Variant Barcode"}, inplace=True)
    print("Luxottica file loaded successfully")
    time.sleep(1)

    print("Merging Luxottica file with Shopify")
    shared = shopify_file.merge(luxottica_file, how="outer", on="Variant Barcode", indicator=True)
    mask = shared["_merge"] == "left_only"
    shared = shared[mask]
    time.sleep(1)
    print("Luxottica and Shopify files merged succeussfully")

    shared = shared[[
        "ID", "Handle", "Command", "Title", "Vendor", "Status",
        "Template Suffix", "URL", "Variant ID", "Variant SKU",
        "Variant Barcode", "Variant Price", "Option1 Name", "Option1 Value",
        "Variant Compare At Price", "Variant Inventory Qty",
        "Inventory Available: +39 05649689443"
    ]]
    shared = shared.rename(columns={"Type_x" : "Type"})
    
    mask = shared["Template Suffix"] == "Default product"
    shared = shared[mask]

    print("All products in the file will being set with quantity 0")
    shared[["Variant Inventory Qty", "Inventory Available: +39 05649689443"]] = 0
    time.sleep(1)
    print("All product setted with quantity 0 correctly")

    luxottica_brands = shared["Vendor"].unique()
    for brand in luxottica_brands:
        try:
            mask = shared["Vendor"] == brand
            brand_file = shared[mask]
            brand_file = brand_file.dropna(how="any", axis = 0, subset=["Variant Barcode"])
            brand_file = brand_file.sort_values(by="Handle")
            brand_file.to_excel(f"{luxottica_folder}/{brand}/{brand}_OUT.xlsx", index=False)
            brand_file.to_excel(f"{out_products}/{brand}_OUT.xlsx", index = False)
            print(f"File \"Products_OUT\" salvato per il brand {brand}")
            time.sleep(1)
        except Exception as err:
            print(f"{type(err).__name__}, {err}")

if __name__ == "__main__":
    print("Generating files for product out")
    old_products()
    print("All files generated successfully!")