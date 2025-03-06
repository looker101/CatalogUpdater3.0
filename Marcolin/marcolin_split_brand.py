import pandas as pd
import time
import datetime
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from marcolin_paths import splitting_marcolin_brands, marcolin_backup
from marcolin_mapping_colors_materials import marcolin_lens_colors, marcolin_frame_colors, marcolin_frame_material, \
    marcolin_frame_shape, marcolin_for_who


def marcolin_split_brands():

    #Lettura file
    marcolin_file = pd.read_excel(marcolin_backup)

    # Marcolin updatet by scraper. I can work without image src??
    # Remove Image Src column and remove all empty cell
    marcolin_file = marcolin_file.drop("Image Src", axis=1)
    marcolin_file = marcolin_file.dropna(how="any", axis=0, subset=["Variant ID"])

    marcolin_file["Status"] = "Active"
    marcolin_file["Command"] = "MERGE"

    def maxmara_title(row):
        if row["Vendor"] == "MaxMara":
            row["Title"] = row["Title"].replace("Maxmara", "MaxMara")
            return row["Title"]
        return row["Title"]

    marcolin_file["Title"] = marcolin_file.apply(maxmara_title, axis=1)

    def get_vendor_as_title(row):
        if row["Vendor"] != "MaxMara":
            return row["Vendor"].title()
        return "MaxMara"

    marcolin_file["Vendor"] = marcolin_file.apply(get_vendor_as_title, axis=1)

    # GET
    marcolin_file["Metafield: my_fields.for_who [single_line_text_field]"] = marcolin_file["Metafield: italian.per_chi [single_line_text_field]"]

    # For Who == Man, Woman, Unisex, Kids
    def get_gender(row):
        items_gender = str(row["Metafield: my_fields.for_who [single_line_text_field]"]).strip().title()

        if not isinstance(items_gender, str):
            return ""

        for mother, children in marcolin_for_who.items():
            for color in children:
                if items_gender == color.strip().title():
                    return mother
        return "Unisex"

    marcolin_file["Metafield: my_fields.for_who [single_line_text_field]"] = marcolin_file.apply(get_gender, axis=1)

    # Type: Get Sunglasses and Eyeglasses Kids
    def get_kids_type(row):
        items_for_who = str(row["Metafield: my_fields.for_who [single_line_text_field]"]).strip().title()
        items_type = str(row["Type"]).strip().title()
        if pd.notna(items_for_who):
            if items_for_who == "Kids" and items_type == "Sunglasses":
                return "Sunglasses Kids"

            if items_for_who == "Kids" and items_type == "Eyeglasses":
                return "Eyeglasses Kids"
            return row["Type"]

    marcolin_file["Type"] = marcolin_file.apply(get_kids_type, axis=1)

    # ================================================ MAIN VALUES ================================================
    # GET MAIN LENS COLOR
    def get_main_lens_color(row):
        """Determino il colore madre per le lenti"""
        items_lens_color = str(row["Metafield: my_fields.lens_color [single_line_text_field]"]).strip()

        if not isinstance(items_lens_color, str):
            return ""

        if "Eyeglasses" not in row["Type"]:
            for mother, children in marcolin_lens_colors.items():
                for color in children:
                    if items_lens_color == color.strip().title():
                        return mother
        return "DEMO"

    marcolin_file["Metafield: custom.main_lens_color [single_line_text_field]"] = marcolin_file.apply(
        get_main_lens_color, axis=1)

    # GET MAIN FRAME COLOR
    def get_main_frame_color(row):
        """Determino il colore madre per la montatura."""
        items_frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).strip().title()

        if not isinstance(items_frame_color, str):
            return ""

        for mother, children in marcolin_frame_colors.items():
            for color in children:
                if items_frame_color == color.strip().title():
                    return mother
        return "Miscellaneous"

    marcolin_file["Metafield: custom.main_frame_color [single_line_text_field]"] = marcolin_file.apply(
        get_main_frame_color, axis=1)

    # GET MOTHER FRAME MATERIAL
    def get_main_frame_material(row):
        """Determino il materiale per la montatura"""
        items_frame_material = str(row["Metafield: my_fields.frame_material [single_line_text_field]"]).strip().title()

        if not isinstance(items_frame_material, str):
            return ""

        for mother, children in marcolin_frame_material.items():
            for color in children:
                if items_frame_material == color.strip().title():
                    return mother
        return "Other"

    marcolin_file["Metafield: custom.main_frame_material [single_line_text_field]"] = marcolin_file.apply(
        get_main_frame_material, axis=1)

    # GET LENS TECHNOLOGIES
    def get_lens_technologies(row):
        items_lens_technology = str(
            row["Metafield: my_fields.lens_technology [single_line_text_field]"]).strip().title()

        if not isinstance(items_lens_technology, str):
            return ""

        if items_lens_technology == "Polarized":
            return "Polarized"
        elif items_lens_technology == "Photochromic":
            return "Photochromic"
        else:
            return "Standard"

    marcolin_file["Metafield: custom.main_lens_technology [single_line_text_field]"] = marcolin_file.apply(
        get_lens_technologies, axis=1)

    # GET FRAME SHAPE
    def get_frame_shape(row):
        items_frame_shape = str(row["Metafield: my_fields.frame_shape [single_line_text_field]"]).strip().title()
        if not isinstance(items_frame_shape, str):
            return ""
        for mother, children in marcolin_frame_shape.items():
            for color in children:
                if items_frame_shape == color.strip().title():
                    return mother
        return "Other"

    marcolin_file["Metafield: custom.main_frame_shape [single_line_text_field]"] = marcolin_file.apply(get_frame_shape,
                                                                                                       axis=1)
    # GET MAIN SIZE
    def get_main_size(row):
        val = row["Option1 Value"]
        if pd.isna(val) or val == "":
            return ""
        try:
            size_item = int(val)
        except ValueError:
            return ""
        if size_item < 48:
            return "S"
        elif size_item < 53:
            return "M"
        else:
            return "L"
    marcolin_file["Metafield: custom.main_size [single_line_text_field]"] = marcolin_file.apply(get_main_size, axis = 1)

    # ================================================ TAGS ================================================
    # GENERATE TAGS
    def generate_tags(row):

        tag_esistenti = str(row["Tags"]).strip()
        lista_tag_esistenti = [tag.strip() for tag in tag_esistenti.split(',')]

        tags_list = [
            str(row["Metafield: custom.main_frame_shape [single_line_text_field]"]) if pd.notna(
                row["Metafield: custom.main_frame_shape [single_line_text_field]"]) else "",
            str(row["Metafield: my_fields.for_who [single_line_text_field]"]) if pd.notna(
                row["Metafield: my_fields.for_who [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_frame_color [single_line_text_field]"]) if pd.notna(
                row["Metafield: custom.main_frame_color [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_lens_color [single_line_text_field]"]) if pd.notna(
                row["Metafield: custom.main_lens_color [single_line_text_field]"]) else "",
            str(row["Type"]) if pd.notna(row["Type"]) else "",
            str(row["Metafield: my_fields.lens_technology [single_line_text_field]"]) if pd.notna(
                row["Metafield: my_fields.lens_technology [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_frame_material [single_line_text_field]"]) if pd.notna(
                row["Metafield: custom.main_frame_material [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_size [single_line_text_field]"]) if pd.notna(
                row["Metafield: custom.main_size [single_line_text_field]"]) else ""
        ]

        tags_list = [str(tag).replace(",", "") for tag in tags_list if pd.notna(tag) and str(tag).strip() != ""]

        if "tag__new_New" in lista_tag_esistenti:
            tags_list.append("tag__new_New")
        if "tag__hot_Best Seller" in lista_tag_esistenti:
            tags_list.append("tag__hot_Best Seller")
        if "available now" in lista_tag_esistenti:
            tags_list.append("available now")
        if row["Vendor"] == "Adidas Sport":
            tags_list.append("Sport")

        return ','.join(tags_list)

    marcolin_file["NewTags"] = marcolin_file.apply(generate_tags, axis=1)

    marcolin_file["Tags"] = marcolin_file["NewTags"]
    marcolin_file.drop(columns=["NewTags"], inplace=True)

    # SE available now NON è PRESENTE NELLA LISTA TAG, IL TEMPLATE SUFFIX DEVE ESSERE "Default product"
    def get_template_suffix(row):
        lista_tag = row["Tags"]
        template = row["Template Suffix"]
        if template == "product-noindex":
            return "product-noindex"
        elif "available now" in lista_tag:
            return "disponibili-subito"
        return "Default product"
    marcolin_file["Template Suffix"] = marcolin_file.apply(get_template_suffix, axis = 1)

#====================================================== SAVE ======================================================

    for brand in marcolin_file["Vendor"].unique():
        try:
            mask = marcolin_file["Vendor"] == brand
            brand_file = marcolin_file[mask]
            brand_file.to_excel(f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/{brand}/{brand}.xlsx",
                                index = False)
            print(f"{brand} saved successfully")
            with open(splitting_marcolin_brands, "a") as file:
                file.write(f"   {brand} are split successfully \n")
            time.sleep(1)
        except Exception as err:
            print(f"{type(err).__name__}: {err}")
            with open(splitting_marcolin_brands, "a") as file:
                file.write(f"   {brand} is not split due this error: \n {type(err).__name__}: {err} \n")

    marcolin_file.to_excel("Marcolin_Test.xlsx", index=False)

if __name__ == "__main__":
    try:
        with open(splitting_marcolin_brands, "a") as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n[{current_time}] Starting Marcolin splitting brands. \n")
        marcolin_split_brands()

        with open(splitting_marcolin_brands, "a") as file:
            file.write(f"Marcolin brands are split successfully. \n")
            file.write(f"Closing Marcolin splitting brands. \n")

    except Exception as err:
        with open(splitting_marcolin_brands, "a") as file:
            file.write(f"Marcolin brands are not split due this error: {type(err).__name__}: {err} \n")
