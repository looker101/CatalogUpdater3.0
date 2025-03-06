import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marchon_paths import FTP_MARCHON_CSV, FTP_MARCHON_FOLDER,\
    FTP_SHOPIFY_FOLDER, MARCHON_BACKUP, products_out

# Per ogni brand devo confrontare il nuovo file ottenuto con quello precedente, in modo da impostare i prodotti
# che non sono presenti nel file aggiornato, in quantità 0

#marchon = pd.read_csv(FTP_MARCHON_CSV)  # , encoding='latin1', delimiter=";"

# controllare i file splittati con il file della marchon
# devo avere in output i file con solo i prodotti nel file di shopify

def compare_quantity():
    marchon_file = pd.read_csv(FTP_MARCHON_CSV)
    shopify_backup = pd.read_excel(MARCHON_BACKUP)

    merged_file = marchon_file.merge(shopify_backup,
                                     left_on = "UPC SKU",
                                     right_on = "Variant Barcode",
                                     how = "outer",
                                     indicator = True)

    mask = merged_file["_merge"] == "right_only"
    product_zero = merged_file[mask]

    #product_zero.to_excel("prova.xlsx", index=False)

    product_zero = product_zero[[
        "ID", "Handle", "Command", "Vendor", "Variant Inventory Qty", "Inventory Available: +39 05649689443",
        "Variant SKU", "Variant Barcode"

    ]]

    product_zero[["Variant Inventory Qty", "Inventory Available: +39 05649689443"]] = 0


    product_zero["Vendor"] = product_zero["Vendor"].fillna("UNKNOWN")
    product_zero["Vendor"] = product_zero["Vendor"].str.strip().str.upper()
    product_zero["Vendor"] = product_zero["Vendor"].str.title()
    # product_zero["Vendor"] = product_zero["Vendor"].replace({
    #     "NIKE": "Nike",
    #     "FERRAGAMO": "Ferragamo",
    #     "LACOSTE": "Lacoste"
    # })

    # product_zero["Vendor"] = product_zero["Vendor"].str.strip()
    # product_zero["Vendor"] = product_zero["Vendor"].replace({
    #     "NIKE":"Nike", "FERRAGAMO":"Ferragamo", "LACOSTE":"Lacoste"
    # })

    product_zero = product_zero.dropna(how = 'any', subset=["Variant Barcode"])

    for brand in product_zero["Vendor"].unique():
        mask = product_zero["Vendor"] == brand  # Filtro corretto
        brand_file = product_zero[mask]
        print(f"Searching products out for {brand} brand.")
        brand_file = brand_file.sort_values(by="Handle")
        brand_file.to_excel(f"{FTP_MARCHON_FOLDER}/{brand}/{brand}_product_zero.xlsx", index=False)
        brand_file.to_excel(f"{products_out}/{brand}_product_zero.xlsx", index=False)
        print(f"Products out file are saved for {brand} brand.")


if __name__ == "__main__":
    print("Starting Marchon products zero")
    compare_quantity()
    print("Closing Marchon products zero")
