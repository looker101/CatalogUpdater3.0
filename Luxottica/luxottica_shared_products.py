import pandas as pd
import time
import datetime
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from luxottica_paths import luxottica_item_master, luxottica_backup, luxottica_folder, luxottica_shared_products_log
from luxottica_colors_and_frames_mapping import lux_lens_colors, lux_frame_colors, luxottica_frame_material, \
    luxottica_frame_shape


def luxottica_shared_products():
    # Read Luxottica Item Master Catalogue
    # Read Luxottica-Shopify backup
    luxottica_file = pd.read_excel(luxottica_item_master)
    shopify = pd.read_excel(luxottica_backup)

    # Merge dataframe how inner join
    shared_file = shopify.merge(luxottica_file,
                                how="inner",
                                left_on="Variant Barcode",
                                right_on="UPC",
                                suffixes=("_looker", "_lux"),
                                indicator=True)

    # Genrazione dei prezzi
    # WHOLESALE PRICE And RETAIL PRICE(VARIANT COMPARE AT PRICE)
    # LASCIA VUOTA LA COLONNA DEL VARIANT PRICE
    shared_file["Variant Cost"] = shared_file["Wholesale Price"]
    shared_file["Variant Compare At Price"] == shared_file["Suggested Retail Price"]
    shared_file["Variant Price"] = ""

    # FRAME SHAPE
    shared_file["Metafield: my_fields.frame_shape [single_line_text_field]"] = shared_file["Shape"]

    # Set all qty as 5
    shared_file[[
        "Variant Inventory Qty", "Inventory Available: +39 05649689443"
    ]] = 5

    shared_file["Variant Cost"] = shared_file["Variant Cost"].str.strip().str.replace(',', '.')
    shared_file["Vendor"] = shared_file["Vendor"].str.title()

    # LENS SIZE
    shared_file["Option1 Name"] = "Size"
    shared_file["Option1 Value"] = shared_file["Size"]
    # ALLA COLONNA FOR WHO ASSEGNO LO STESSO VALORE DELLA COLONNA GENDER DEL FILE LUXOTTICA
    shared_file["Metafield: my_fields.for_who [single_line_text_field]"] = shared_file["Gender"]

    # REMOVE USELESS TYPES
    mask_type = shared_file["Type_looker"].isin([
        "Sunglasses", "Eyeglasses", "Sunglasses Kids", "Eyeglasses Kids", "Ski & Snowboard Goggles"
    ])
    shared_file = shared_file[mask_type]

    # VENDOR -> LASCIARE SOLO IL NOME DEL BRAND IN TITLE()
    # RIMUOVERE TUTTO IL SUPERFLUO (KIDS, FRAME, JUNIOR)
    def get_vendor_eq_brand(row):
        pass

    # KEEPP COLUMNS
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

    # On Gender doesn't exist Kids category
    # Create Kids category based on "Type" row
    def get_kids_category(row):
        gender = str(row["Metafield: my_fields.for_who [single_line_text_field]"]).strip().title()
        item_type = str(row["Type"]).strip().title()

        kids_category = ["Sunglasses Kids", "Eyeglasses Kids"]

        if item_type in kids_category:
            return "Kids"
        return gender
    shared_file["Metafield: my_fields.for_who [single_line_text_field]"] = shared_file.apply(get_kids_category, axis=1)


    # # Type -> If for kids, return Kids on Type
    # def get_kids_on_type(row):
    #     items_for_who = str(row["Metafield: my_fields.for_who [single_line_text_field]"]).strip().title()
    #     items_type = str(row["Type"]).strip().title()
    #     if pd.notna(items_for_who):
    #         if items_for_who == "Kids" and items_type == "Sunglasses":
    #             return "Sunglasses Kids"
    #         elif items_for_who == "Kids" and items_type == "Eyeglasses":
    #             return "Eyeglasses Kids"
    #         return row["Type"]
    #
    # shared_file["Type"] = shared_file.apply(get_kids_on_type, axis=1)

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
    shared_file["Metafield: custom.main_size [single_line_text_field]"] = shared_file.apply(get_main_size, axis = 1 )

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

    shared_file.to_excel("Shared_Product.xlsx", index=False)

    luxottica_brands = shared_file["Vendor"].unique()
    for brand in luxottica_brands:
        try:
            mask = shared_file["Vendor"] == brand
            brand_file = shared_file[mask].sort_values(by="Handle")
            brand_file.to_excel(f"{luxottica_folder}/{brand}/{brand}.xlsx", index=False)
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
            print("Tutto ok")
        except Exception as err:
            file.write(f"[{current_time}] Luxottica regular products are not updated due this error:\n")
            file.write(f"{type(err).__name__}: {err}\n")
            print(f"{type(err).__name__}: {err}\n")
