import pandas as pd
import time
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from luxottica_paths import luxottica_item_master, luxottica_backup, luxottica_folder, luxottica_shared_products_log

def luxottica_shared_products():
    # Read Luxottica Item Master Catalogue
    # Read Luxottica-Shopify backup
    print("Read Item Master Data and Shopify backup")
    luxottica_file = pd.read_excel(luxottica_item_master)
    shopify = pd.read_excel(luxottica_backup)

    # Remove new, best seller and adv from tag
    # shopify["Tags"] = shopify["Tags"].str.replace("Best-seller,", "")
    # shopify["Tags"] = shopify["Tags"].str.replace("Best-seller", "")
    # shopify["Tags"] = shopify["Tags"].str.replace("New", "")
    # shopify["Tags"] = shopify["Tags"].str.replace("New,", "")
    # shopify["Tags"] = shopify["Tags"].str.replace("ADV", "")
    # shopify["Tags"] = shopify["Tags"].str.replace("ADV,", "")


    # check disponibili subito on Backup file
    def check_available_now_tag(row):
        if "available now" in row["Tags"]:
            return "disponibili-subito"
        return "Default product"
    shopify["Template Suffix"] = shopify.apply(check_available_now_tag, axis = 1)

    # Merge dataframe
    print("Merging dataframes")
    shared_file = shopify.merge(luxottica_file,
                                how = "inner",
                                left_on="Variant Barcode",
                                right_on="UPC",
                                suffixes=("_looker", "_lux"),
                                indicator=True)

    shared_file["Variant Cost"] = shared_file["Wholesale Price"]

    # KEEP COLUMNS
    keep_columns = [
        "ID", "Handle", "Command", "Title", "Body HTML",
         "Vendor", "Type_looker", "Tags", "Tags Command",
        "Status", "Template Suffix", "URL", "Variant ID", "Variant SKU",
        "Variant Barcode", "Variant Price", "Variant Compare At Price", "Variant Cost",
        "Variant Inventory Qty", "Inventory Available: +39 05649689443",
        "Metafield: title_tag [string]", "Metafield: description_tag [string]",
        "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]",
        "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]",
        "Metafield: my_fields.lens_technology [single_line_text_field]",
        "Metafield: my_fields.lens_material [single_line_text_field]",
        "Metafield: my_fields.product_size [single_line_text_field]",
        "Metafield: my_fields.gtin1 [single_line_text_field]",
        "Metafield: my_fields.for_who [single_line_text_field]",
        "New", "Best Seller", "Advertising"
    ]
    shared_file = shared_file[shared_file]


    def add_new_adv_bs_in_tag(row):
        tags = row["Tags"].split(',') if row["Tags"] else []

        if row["New"] == "X":
            tags.append("New")

        if row["Best Seller"] == "X":
            tags.append("Best Seller")

        if row["Advertising"] == "X":
            tags.append("ADV")

        return ', '.join(tags)

    shared_file["Tags"] = shared_file.apply(add_new_adv_bs_in_tag, axis = 1)

    shared_file = shared_file.rename(columns={"Type_looker":"Type"})

    # Filtered by "Default product" template suffix
    mask = shared_file["Template Suffix"] == "Default product"
    shared_file = shared_file[mask]

    # Set all availabily as 5
    shared_file[[
        "Variant Inventory Qty", "Inventory Available: +39 05649689443"
    ]] = 5

    shared_file["Variant Cost"] = shared_file["Variant Cost"].str.strip().str.replace(',', '.')
    #shared_file["Vendor"] = shared_file["Vendor"].str.replace('Ray-ban', 'Ray-Ban')
    shared_file["Vendor"] = shared_file["Vendor"].str.title()
    #shared_file["Title"] = shared_file["Title"].str.title()

    luxottica_brands = shared_file["Vendor"].unique()
    for brand in luxottica_brands:
        try:
            mask = shared_file["Vendor"] == brand
            brand_file = shared_file[mask].sort_values(by="Handle")
            brand_file.to_excel(f"{luxottica_folder}/{brand}/{brand}.xlsx", index = False)
            print(f"{brand} saved successfully.")
        except Exception as err:
            print(f"{type(err).__name__}: {err}")

    shared_file.to_excel("Luxottica_shared_products.xlsx", index=False)
    print("File saved successfully")

if __name__ == "__main__":
    with open(luxottica_shared_products_log, "a") as file:
        current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
        try:
            luxottica_shared_products()
            file.write(f"[{current_time}] Luxottica regular products are updated!\n")
        except Exception as err:
            file.write(f"[{current_time}] Luxottica regulare products are not updated due this error:\n")
            file.write(f"{type(err).__name__}: {err}\n")
