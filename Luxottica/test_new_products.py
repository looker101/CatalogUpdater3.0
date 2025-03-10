import pandas as pd
import time
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import luxottica_backup, luxottica_item_master

shopify_file = pd.read_excel(luxottica_backup)
luxottica_file = pd.read_excel(luxottica_item_master)

# PRIMA DI FARE IL MERGE, FILTRA ITEM MASTER DATA PER LE CATEGORIE NECESSARIE
luxottica_file = luxottica_file[luxottica_file["Collection"].isin([
    "Sunglasses", "Eyeglasses", "Sunglasses Kids", "Eyeglasses Kids", "Goggles&Helmets"
])]
luxottica_file["Collection"] = luxottica_file["Collection"].str.replace("Goggles&Helmets",
                                                                        "Ski & Snowboard Goggles")

# REPLACE "GOGGLE&ACC  SNOW" NAME BRAND WITH OAKLEY
luxottica_file["Brand Name"] = luxottica_file["Brand Name"].str.replace("GOGGLE&ACC  SNOW", "OAKLEY")
luxottica_file["Brand Name"] = luxottica_file["Brand Name"].str.strip().str.title()

new_items = shopify_file.merge(
    luxottica_file,
    left_on="Variant Barcode",
    right_on="UPC",
    how="right",
    suffixes=("_shopify", "_looker"),
    indicator=True
)

mask = new_items["_merge"] == "right_only"
new_items = new_items[mask]


# =============================================== BRANDS NAME AND ITEMS TYPE =======================================
# GET KIDS CATEGORIES FROM LUXOTTICA BRAND NAME E.G. BURBERRY KIDS
# IF KIDS, YOUTH, JUNIOR IN BRAND NAME, GENDER WILL BE KIDS
def get_kids_gender(row):
    brand_name = str(row["Brand Name"]).strip().lower()
    kids_category = ["kids", "youth", "junior"]
    for category in kids_category:
        if category in brand_name:
            return "Kids"
    return row["Gender"]
new_items["Metafield: my_fields.for_who [single_line_text_field]"] = new_items.apply(get_kids_gender, axis = 1)

# FROM BRANND NAME COLUMN, REMOVE USELESS NAME AS KIDS, FRAME OR SOMETHING LIKE THIS
def get_main_brand(row):
    luxottica_brand_name = str(row["Brand Name"]).strip().lower()
    if luxottica_brand_name == "burberry kids":
        return "Burberry"
    elif luxottica_brand_name == "dolce & gabbana kids":
        return "Dolce & Gabbana"
    elif luxottica_brand_name == "emporio armani aids":
        return "Emporio Armani"
    elif luxottica_brand_name == "oakley frame" or luxottica_brand_name == "oakley youth rx" or luxottica_brand_name == "oakley youth sun":
        return "Oakley"
    elif luxottica_brand_name == "ray-ban junior" or luxottica_brand_name == "ray-ban junior vista" or luxottica_brand_name == "ray-ban vista":
        return "Ray-Ban"
    elif luxottica_brand_name == "versace kids":
        return "Versace"
    elif luxottica_brand_name == "vogue junior sun" or luxottica_brand_name == "vogue junior ophthal":
        return "Vogue Eyewear"
    return row["Brand Name"]

new_items["Brand Name"] = new_items.apply(get_main_brand, axis=1)
new_items["Vendor"] = new_items["Brand Name"]


new_items.to_excel("ProvaNuovi.xlsx", index = False)