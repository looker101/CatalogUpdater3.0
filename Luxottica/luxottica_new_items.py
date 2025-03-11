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

# ========================================== FILL COLUMNS ==========================================
# TEMPLATE SUFFIX AS "Default product"
new_items["Template Suffix"] = "Default product"

# Size -> Product Variants
new_items["Option1 Name"] = "Size"
new_items["Option1 Value"] = new_items["Size"]

# =============================================== BARCODE BRANDS NAME, ITEMS TITLE, SKU AND ITEMS TYPE =======================================
# VARIANT BARCODE
new_items["Variant Barcode"] = new_items["UPC"]


# GET KIDS CATEGORIES FROM LUXOTTICA BRAND NAME E.G. BURBERRY KIDS
# IF KIDS, YOUTH, JUNIOR IN BRAND NAME, GENDER WILL BE KIDS
def get_kids_gender(row):
    brand_name = str(row["Brand Name"]).strip().lower()
    kids_category = ["kids", "youth", "junior"]
    for category in kids_category:
        if category in brand_name:
            return "Kids"
    return row["Gender"]


new_items["Metafield: my_fields.for_who [single_line_text_field]"] = new_items.apply(get_kids_gender, axis=1)


# FROM BRANND NAME COLUMN, REMOVE USELESS NAME AS KIDS, FRAME OR SOMETHING LIKE THIS
def get_main_brand(row):
    luxottica_brand_name = str(row["Brand Name"]).strip().lower()
    if luxottica_brand_name == "burberry kids":
        return "Burberry"
    elif luxottica_brand_name == "dolce & gabbana kids":
        return "Dolce & Gabbana"
    elif luxottica_brand_name == "emporio armani kids":
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


# ITEMS TITLE
def get_items_title(row):
    brand = row["Vendor"].title()
    if row["Model Code"].startswith("0"):
        model_code = row["Model Code"].replace("0", "", 1)
    else:
        model_code = row["Model Code"].replace("A", "", 1)
    color_code = row["Color Code"]
    if pd.notna(row["Model Name Description"]):
        product_name = row["Model Name Description"].title()
        return f"{brand} {product_name} {model_code} {color_code}"
    else:
        return f"{brand} {model_code} {color_code}"

new_items["Title"] = new_items.apply(get_items_title, axis=1)

# SET ITEMS SKU
def get_variant_sku(row):
    model_code = row["Model Code"]
    color_code = row["Color Code"]
    size = row["Size"]
    if model_code.startswith('0'):
        # Rimuovi il primo carattere se è '0'
        model_code = model_code[1:]
    elif model_code.startswith('A'):
        # Rimuovi il primo carattere se è 'A'
        model_code = model_code[1:]
    return f"{model_code} {color_code} {size}"
new_items["Variant SKU"] = new_items.apply(get_variant_sku, axis=1)

# ITEMS TYPE: SHOPIFY TYPE == LUXOTTICA COLLECTION
new_items["Type_shopify"] = new_items["Collection"]
# ================================================ PRICE & COST===========================================================
# GET RETAIL PRICE
new_items["Variant Compare At Price"] = new_items["Suggested Retail Price"]


# SET RIGHT FORMAT FOR RRP -> LUXOTTICA FILE IS WITH COMMA I NEED POINT
def get_right_format_for_compare_price(row):
    retail_price = row["Variant Compare At Price"]
    if isinstance(retail_price, str):
        retail_price = retail_price.strip()
        retail_price = retail_price.replace(".", "")
        retail_price = retail_price.replace(",", ".")
    return float(retail_price)


new_items["Variant Compare At Price"] = new_items.apply(get_right_format_for_compare_price, axis=1)

# ============================================= QUANTITY ======================================================
new_items[[
    "Variant Inventory Qty", "Inventory Available: +39 05649689443"
]] = 0

# =========================================== FRAME ===========================================================
# Color, Shape, Material
new_items["Metafield: my_fields.frame_color [single_line_text_field]"] = new_items["Front Colour"]
new_items["Metafield: my_fields.frame_shape [single_line_text_field]"] = new_items["Shape"]
new_items["Metafield: my_fields.frame_material [single_line_text_field]"] = new_items["Front Material"]

# =========================================== LENS ===========================================================
# Color, Material
new_items["Metafield: my_fields.lens_color [single_line_text_field]"] = new_items["Lens Color"]
new_items["Metafield: my_fields.lens_material [single_line_text_field]"] = new_items["Lens Material"]


# Technology
def get_lens_technology(row):
    polar = str(row["Polarized"]).strip().lower()
    photo = str(row["Photochromic"]).strip().lower()

    lens_techno = []

    if pd.notna(row["Photochromic"]):
        lens_techno.append("Photochromic")
    if pd.notna(row["Polarized"]):
        lens_techno.append("Polarized")
    if pd.isna(row["Photochromic"]) and pd.isna(row["Polarized"]):
        lens_techno.append("Standard")

    return ",".join(lens_techno)


new_items["Metafield: my_fields.lens_technology [single_line_text_field]"] = new_items.apply(get_lens_technology,
                                                                                             axis=1)


# SIZE - BRIDGE - TEMPLES
def get_size_bridge_temples(row):
    if pd.notna(row["Width Lens"]):
        size = int(row["Width Lens"])
    else:
        size = ""
    if pd.notna(row["Lens Height"]):
        bridge = int(row["Lens Height"])
    else:
        bridge = ""
    if pd.notna(row["Temple Length"]):
        temples = int(row["Temple Length"])
    else:
        temples = ""

    return f"{size}-{bridge}-{temples}"


new_items["Metafield: my_fields.product_size [single_line_text_field]"] = new_items.apply(get_size_bridge_temples,
                                                                                          axis=1)

# ================================================== TAGS ==================================================
# Insert only "new"
def get_tags(row):
    new = str(row["New"])
    best_seller = str(row["Best Seller"])

    tags_list = []

    if pd.notna(new) and new == "X":
        tags_list.append("tag__new_New")
    if pd.notna(best_seller) and best_seller == "X":
        tags_list.append("tag__hot_Best Seller")

    return ",".join(tags_list)
new_items["Tags"] = new_items.apply(get_tags, axis=1)

# Tags Command
new_items["Tags Command"] = "REPLACE"

# ================================================== REMOVE LUXOTTICA FILE COLUMNS =================================
column_to_keep = [
    "ID", "Handle", "Command", "Title", "Body HTML",
    "Vendor", "Type_looker", "Tags", "Tags Command",
    "Status", "Template Suffix", "URL", "Variant ID", "Variant SKU",
    "Variant Barcode", "Option1 Name", "Option1 Value", "Variant Price",
    "Variant Compare At Price",
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
    "Metafield: my_fields.for_who [single_line_text_field]"
    #"New", "Best Seller", "Advertising"
]
new_items = new_items[column_to_keep]
new_items = new_items.rename(columns={"Type_looker": "Type"})
# ========================================== SAVE ==========================================
new_items = new_items.sort_values(by="Title")
new_items.to_excel("ProvaNuovi.xlsx", index=False)
