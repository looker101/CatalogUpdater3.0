import pandas as pd
import time
import datetime
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from luxottica_paths import luxottica_item_master, luxottica_backup, luxottica_folder, luxottica_shared_products_log
from luxottica_colors_and_frames_mapping import lux_lens_colors, lux_frame_colors, luxottica_frame_material, \
    luxottica_frame_shape


# READING EXCEL FILES
def luxottica_shared_products():
    luxottica_file = pd.read_excel(luxottica_item_master)
    shopify = pd.read_excel(luxottica_backup)

    # PRIMA DI FARE IL MERGE, FILTRA ITEM MASTER DATA PER LE CATEGORIE NECESSARIE
    luxottica_file = luxottica_file[luxottica_file["Collection"].isin([
        "Sunglasses", "Eyeglasses", "Sunglasses Kids", "Eyeglasses Kids", "Goggles&Helmets"
    ])]
    luxottica_file["Collection"] = luxottica_file["Collection"].str.replace("Goggles&Helmets",
                                                                            "Ski & Snowboard Goggles")

    # REPLACE "GOGGLE&ACC  SNOW" NAME BRAND WITH OAKLEY
    luxottica_file["Brand Name"] = luxottica_file["Brand Name"].str.replace("GOGGLE&ACC  SNOW", "OAKLEY")
    luxottica_file["Brand Name"] = luxottica_file["Brand Name"].str.strip().str.title()

    shared_file = shopify.merge(
        luxottica_file,
        left_on="Variant Barcode",
        right_on="UPC",
        how="inner",
        suffixes=("_looker", "_lux"),
        indicator=True
    )

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

    shared_file["Metafield: my_fields.for_who [single_line_text_field]"] = shared_file.apply(get_kids_gender, axis=1)

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

    shared_file["Brand Name"] = shared_file.apply(get_main_brand, axis=1)
    shared_file["Vendor"] = shared_file["Brand Name"]

    # SET ITEMS TITLE
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

    shared_file["Title"] = shared_file.apply(get_items_title, axis=1)

    # GET TYPE FROM LUXOTTICA FILE
    shared_file["Type_looker"] = shared_file["Collection"]
    # ================================================ PRICE & COST===========================================================
    # GET RETAIL PRICE
    shared_file["Variant Compare At Price"] = shared_file["Suggested Retail Price"]

    # SET RIGHT FORMAT FOR RRP -> LUXOTTICA FILE IS WITH COMMA I NEED POINT
    def get_right_format_for_compare_price(row):
        retail_price = row["Variant Compare At Price"]
        if isinstance(retail_price, str):
            retail_price = retail_price.strip()
            retail_price = retail_price.replace(".", "")
            retail_price = retail_price.replace(",", ".")
        return float(retail_price)

    shared_file["Variant Compare At Price"] = shared_file.apply(get_right_format_for_compare_price, axis=1)

    # REMOVE VARIANT PRICE -> WILL FILL WITH PRICE_QTY SCRIPT
    shared_file["Variant Price"] = ""

    # VARIANT COST
    shared_file["Variant Cost"] = shared_file["Wholesale Price"].str.strip().str.replace(',', '.')
    # =========================== MAPPATURA COLONNE DA FILE LUXOTTICA DOPO IL MERGE =====================
    # All quantity as 5
    shared_file[[
        "Variant Inventory Qty", "Inventory Available: +39 05649689443"
    ]] = 5

    # Size
    shared_file["Option1 Name"] = "Size"
    shared_file["Option1 Value"] = shared_file["Size"]

    # =========================================== FRAME ===========================================================
    # Color, Shape, Material
    shared_file["Metafield: my_fields.frame_color [single_line_text_field]"] = shared_file["Front Colour"]
    shared_file["Metafield: my_fields.frame_shape [single_line_text_field]"] = shared_file["Shape"]
    shared_file["Metafield: my_fields.frame_material [single_line_text_field]"] = shared_file["Front Material"]

    # =========================================== LENS ===========================================================
    # Color, Material
    shared_file["Metafield: my_fields.lens_color [single_line_text_field]"] = shared_file["Lens Color"]
    shared_file["Metafield: my_fields.lens_material [single_line_text_field]"] = shared_file["Lens Material"]
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
    shared_file["Metafield: my_fields.lens_technology [single_line_text_field]"] = shared_file.apply(get_lens_technology, axis=1)

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
    shared_file["Metafield: my_fields.product_size [single_line_text_field]"] = shared_file.apply(get_size_bridge_temples, axis=1)

    # ================================================== REMOVE LUXOTTICA FILE COLUMNS =================================
    column_to_keep = [
        "ID", "Handle", "Command", "Title", "Body HTML",
        "Vendor", "Type_looker", "Tags", "Tags Command",
        "Status", "Template Suffix", "URL", "Variant ID", "Variant SKU",
        "Variant Barcode", "Option1 Name", "Option1 Value", "Variant Price",
        "Variant Compare At Price", "Variant Cost",
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
    shared_file = shared_file[column_to_keep]
    shared_file = shared_file.rename(columns={"Type_looker": "Type"})

    # ========================================= MAIN VALUES =========================================

    # LENS COLOR
    def get_main_lens_color(row):
        """Determino i colori madre per le lenti"""
        items_lens_color = str(row["Metafield: my_fields.lens_color [single_line_text_field]"]).strip()

        if row["Type"] in ["Sunglasses", "Sunglasses Kids"]:
            for mother, children in lux_lens_colors.items():
                for color in children:
                    if color in items_lens_color:
                        return mother

        elif row["Type"] == "Ski & Snowboard Goggles":
            for mother, children in lux_lens_colors.items():
                for color in children:
                    if color in items_lens_color:
                        return mother
            return "Prizm Snow"

        return "DEMO"

    shared_file["Metafield: custom.main_lens_color [single_line_text_field]"] = shared_file.apply(get_main_lens_color,
                                                                                                  axis=1)

    # FRAME COLOR
    def get_main_frame_color(row):
        """Determino i colori madre per le montature"""
        items_frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).strip()
        if not isinstance(items_frame_color, str):
            return ""
        for mother, children in lux_frame_colors.items():
            for color in children:
                if color in items_frame_color:
                    return mother
        return "Miscellaneous"

    shared_file["Metafield: custom.main_frame_color [single_line_text_field]"] = shared_file.apply(
        get_main_frame_color, axis=1)

    # FRAME MATERIAL
    def get_main_frame_material(row):
        items_frame_material = str(row["Metafield: my_fields.frame_material [single_line_text_field]"]).strip().title()

        if not isinstance(items_frame_material, str):
            return ""

        for mother, children in luxottica_frame_material.items():
            for color in children:
                if items_frame_material == color.strip().title():
                    return mother
        return 'Other'

    shared_file["Metafield: custom.main_frame_material [single_line_text_field]"] = shared_file.apply(
        get_main_frame_material, axis=1)

    # LENS TECHNOLOGY
    def get_lens_technology(row):
        items_lens_technology = str(
            row["Metafield: my_fields.lens_technology [single_line_text_field]"]).strip().title()

        if pd.notna(row["Metafield: my_fields.lens_technology [single_line_text_field]"]):
            if items_lens_technology == "Polarized":
                return "Polarized"
            elif items_lens_technology == "Photochromic":
                return "Photochromic"
        return "Standard"

    shared_file["Metafield: my_fields.lens_technology [single_line_text_field]"] = shared_file.apply(
        get_lens_technology, axis=1)
    shared_file["Metafield: custom.main_lens_technology [single_line_text_field]"] = shared_file.apply(
        get_lens_technology, axis=1)

    # FRAME SHAPE
    def get_main_frame_shape(row):
        items_frames_shape = str(row["Metafield: my_fields.frame_shape [single_line_text_field]"]).strip().title()
        if row["Type"] != "Ski & Snowboard Goggles":
            for mother, children in luxottica_frame_shape.items():
                for shape in children:
                    if items_frames_shape == shape.strip().title():
                        return mother
            return "Other"
        return "Mask"

    shared_file["Metafield: custom.main_frame_shape [single_line_text_field]"] = shared_file.apply(get_main_frame_shape,
                                                                                                   axis=1)

    # GET MAIN SIZE
    def get_main_size(row):
        items_size = int(row["Option1 Value"])
        if not isinstance(items_size, int):
            return ""
        if pd.notna(row["Option1 Value"]):
            if row["Option1 Value"] in range(0, 48):
                return "S"
            elif row["Option1 Value"] in range(48, 53):
                return "M"
            else:
                return "L"
        return ""

    shared_file["Metafield: custom.main_size [single_line_text_field]"] = shared_file.apply(get_main_size, axis=1)

    # ======================================================= TAGS ====================================================
    # Get Correct Tags
    def get_tags(row):
        """Inserimento dei Tags"""
        row["Tags"] = ""

        tags_list = [
            str(row["Metafield: my_fields.for_who [single_line_text_field]"]) if pd.notna(
                row["Metafield: my_fields.for_who [single_line_text_field]"]) else "",
            str(row["Metafield: my_fields.frame_shape [single_line_text_field]"]) if pd.notna(
                row["Metafield: my_fields.frame_shape [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_frame_color [single_line_text_field]"]) if pd.notna(
                row["Metafield: custom.main_frame_color [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_lens_color [single_line_text_field]"]) if pd.notna(
                row["Metafield: custom.main_lens_color [single_line_text_field]"]) else "",
            str(row["Type"]) if pd.notna(row["Type"]) else "",
            str(row["Metafield: my_fields.lens_technology [single_line_text_field]"]) if pd.notna(
                row["Metafield: my_fields.lens_technology [single_line_text_field]"]) else "",
            str(row["Metafield: my_fields.lens_material [single_line_text_field]"]) if pd.notna(
                row["Metafield: my_fields.lens_material [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_frame_material [single_line_text_field]"]) if pd.notna(
                row["Metafield: custom.main_frame_material [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_size [single_line_text_field]"]) if pd.notna(
                row["Metafield: custom.main_size [single_line_text_field]"]) else ""

        ]
        # Se il tag all'interno della lista 'tags_list' NON è NaN e non é vuoto, allora ritorna il tag sottoforma di stringa e togli la virgola
        tags_list = [str(tag).replace(",", "") for tag in tags_list if pd.notna(tag) and str(tag).strip() != ""]

        new = str(row["New"])
        best_seller = str(row["Best Seller"])
        adv = str(row["Advertising"])

        if pd.notna(new) and new == "X":
            tags_list.append("tag__new_New")
        if pd.notna(best_seller) and best_seller == "X":
            tags_list.append("tag__hot_Best Seller")
        if pd.notna(adv) and adv == "X":
            tags_list.append("ADV")
        if row["Vendor"] == "Oakley":
            tags_list.append("Sport")

        return ",".join(tags_list)

    shared_file["Tags"] = shared_file.apply(get_tags, axis=1)

    # SAVE
    shared_file.to_excel("Luxottica_shared_products.xlsx", index=False)

    luxottica_brands = shared_file["Vendor"].unique()
    for brand in luxottica_brands:
        try:
            mask = shared_file["Vendor"] == brand
            brand_file = shared_file[mask].sort_values(by="Handle")
            brand_file.to_excel(f"{luxottica_folder}/{brand}/{brand}.xlsx", index=False)
            print(f"{brand} saved successfully.")
        except Exception as err:
            print(f"{type(err).__name__}: {err}")

if __name__ == "__main__":
    with open(luxottica_shared_products_log, "a") as file:
        current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
        try:
            luxottica_shared_products()
            print("Done")
            file.write(f"[{current_time}] Luxottica regular products are updated!\n")
        except Exception as err:
            file.write(f"[{current_time}] Luxottica regular products are not updated due this error:\n")
            file.write(f"{type(err).__name__}: {err}\n")
            print(f"{type(err).__name__}: {err}\n")

