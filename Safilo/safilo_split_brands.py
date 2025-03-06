import pandas as pd
import time
import datetime
import sys

from pandas.io.formats.format import return_docstring

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from safilo_paths import safilo_splitting_logs, safilo_backup
from main_color_and_frame_mapping import safilo_lens_color, safilo_frame_color, safilo_frame_shape, \
    safilo_frame_material, safilo_gender


# UPDATE BY SCRAPER -> I can remove Image column and every empty rows

def split_safilo_brands():
    safilo_file = pd.read_excel(safilo_backup)

    safilo_file = safilo_file.drop('Image Src', axis=1)
    safilo_file = safilo_file.dropna(how='any', subset=['Variant Barcode'])

    safilo_file["Tags Command"] = "REPLACE"
    safilo_file["Status"] = "Active"

    # ============================================ MAIN VALUES ============================================
    # LENS COLOR
    def get_main_lens_color(row):
        items_lens_color = str(row["Metafield: my_fields.lens_color [single_line_text_field]"]).strip().title()
        if not isinstance(items_lens_color, str):
            return
        if "Eyeglasses" not in row["Type"]:
            for mother, children in safilo_lens_color.items():
                for color in children:
                    if items_lens_color == color.strip().title():
                        return mother
        return "DEMO"

    safilo_file["Metafield: custom.main_lens_color [single_line_text_field]"] = safilo_file.apply(get_main_lens_color,
                                                                                                  axis=1)

    # FRAME COLOR
    def get_main_frame_color(row):
        items_frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"])
        if not isinstance(items_frame_color, str):
            return ""
        for mother, children in safilo_frame_color.items():
            for color in children:
                if items_frame_color == color.strip().title():
                    return mother
        return "Miscellaneous"

    safilo_file["Metafield: custom.main_frame_color [single_line_text_field]"] = safilo_file.apply(get_main_frame_color,
                                                                                                   axis=1)

    # FRAME SHAPE
    def get_main_frame_shape(row):
        items_frame_shape = str(row["Metafield: my_fields.frame_shape [single_line_text_field]"]).strip().title()
        if not isinstance(items_frame_shape, str):
            return ""
        for mother, children in safilo_frame_shape.items():
            for shape in children:
                if items_frame_shape == shape.strip().title():
                    return mother
        return "Other"

    safilo_file["Metafield: custom.main_frame_shape [single_line_text_field]"] = safilo_file.apply(get_main_frame_shape,
                                                                                                   axis=1)

    # FRAME MATERIAL
    def get_main_frame_material(row):
        items_frame_material = str(row["Metafield: my_fields.frame_material [single_line_text_field]"]).strip().title()
        if not isinstance(items_frame_material, str):
            return ""
        for mother, children in safilo_frame_material.items():
            for material in children:
                if items_frame_material == material.strip().title():
                    return mother
        return "Other"

    safilo_file["Metafield: custom.main_frame_material [single_line_text_field]"] = safilo_file.apply(
        get_main_frame_material, axis=1)

    # GENDER
    def get_main_gender(row):
        items_gender = str(row["Metafield: my_fields.for_who [single_line_text_field]"]).strip().title()
        if not isinstance(items_gender, str):
            return ""
        for mother, children in safilo_gender.items():
            for gender in children:
                if items_gender == gender.strip().title():
                    return mother
        return ""

    safilo_file["Metafield: my_fields.for_who [single_line_text_field]"] = safilo_file.apply(get_main_gender, axis=1)

    # GET MAIN SIZE
    def get_main_size(row):
        items_size = row["Option1 Value"]

        if pd.isna(items_size) or items_size == "":
            return ""

        try:
            size = int(items_size)
        except ValueError:
            return ""

        if size < 48:
            return "S"
        elif size < 53:
            return "M"
        else:
            return "L"

    safilo_file["Metafield: custom.main_size [single_line_text_field]"] = safilo_file.apply(get_main_size, axis=1)

    # GET KIDS TYPE
    # Type -> If for kids, return Kids on Type
    def get_kids_on_type(row):
        items_for_who = str(row["Metafield: my_fields.for_who [single_line_text_field]"]).strip().title()
        items_type = str(row["Type"]).strip().title()
        if pd.notna(items_for_who):
            if items_for_who == "Kids" and items_type == "Sunglasses":
                return "Sunglasses Kids"
            elif items_for_who == "Kids" and items_type == "Eyeglasses":
                return "Eyeglasses Kids"
            return row["Type"]
    safilo_file["Type"] = safilo_file.apply(get_kids_on_type, axis = 1)

    # ============================================ TAGS ============================================
    # GET TAGS
    # TAGS ARE UPDATE BY SCRAPER -> MANTAIN NEW OR BEST SELLER AND ADD S M or L as size
    # I NEED TO CREATE A LIST WITH TAG ALREADY EXIST
    def get_tags(row):

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
        if row["Vendor"] in ["Carrera Ducati", "Under Armour"]:
            tags_list.append("Sport")

        return ','.join(tags_list)

    safilo_file["NewTags"] = safilo_file.apply(get_tags, axis=1)
    safilo_file["Tags"] = safilo_file["NewTags"]
    safilo_file.drop(columns=["NewTags"], inplace=True)
    
    # SE available now NON è PRESENTE NELLA LISTA TAG, IL TEMPLATE SUFFIX DEVE ESSERE "Default product"
    def get_template_suffix(row):
        lista_tag = row["Tags"]
        template = row["Template Suffix"]
        if template == "product-noindex":
            return "product-noindex"
        elif "available now" in lista_tag:
            return "disponibili-subito"
        return "Default product"
    safilo_file["Template Suffix"] = safilo_file.apply(get_template_suffix, axis = 1)

    # ============================================ SAVING ============================================

    safilo_file.to_csv("ProvaSport.csv", index=False)

    for brand in safilo_file["Vendor"].unique():
        try:
            mask = safilo_file["Vendor"] == brand
            brand_file = safilo_file[mask]
            brand_file.to_excel(f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/{brand}/{brand}.xlsx",
                                index = False)
            print(f"{brand} saved succesfully")
            with open(safilo_splitting_logs, "a") as file:
                file.write(f"   -{brand} is split successfully\n")
            time.sleep(1)
        except Exception as err:
            print(f"{type(err).__name__}: {err}")
            with open(safilo_splitting_logs, "a") as file:
                file.write(f"   -{brand} is not split due this error:\n {type(err).__name__}: {err} \n")

if __name__ == "__main__":
    try:
        with open(safilo_splitting_logs, "a") as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n[{current_time}] Starting Safilo split brands \n")
        split_safilo_brands()

        with open(safilo_splitting_logs, "a") as file:
            file.write("Safilo's brand are split successfully")
            file.write(f"\n Closing Safilo split brands \n")

    except Exception as err:
        with open(safilo_splitting_logs, "a") as file:
            file.write(f"Safilo's brands are not split due this error:\n {type(err).__name__}: {err} \n")
            file.write(f"\nClosing Safilo split brands \n")
