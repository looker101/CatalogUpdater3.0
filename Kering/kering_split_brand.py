import pandas as pd
import time
import sys
import datetime

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from kering_paths import kering_backup, splitting_kering_brands
from kering_colors_frame_mapping import kering_lens_color, kering_frame_color, kering_frame_shape,\
    kering_frame_material, kering_lens_technology

# Working only on Default product items


def split_kering():

    kering_file = pd.read_excel(kering_backup)

    kering_file = kering_file.drop("Image Src", axis=1)
    kering_file = kering_file.dropna(how="any", axis=0, subset=["Variant Barcode"])

    # DISPONIBILI SUBITO -> Tags editing will remove 'available now' tag
    # def check_available_now_tag(row):
    #     if "available now" in row["Tags"]:
    #         return "disponibili-subito"
    #     return "Default product"
    # kering_file["Template Suffix"] = kering_file.apply(check_available_now_tag, axis=1)

    def get_correct_vendor_name(row):
        if row["Vendor"] == "GUCCI":
            return "Gucci"
        if row["Vendor"] == "Alexander Mcqueen":
            return "Alexander McQueen"
        return row["Vendor"]

    kering_file["Vendor"] = kering_file.apply(get_correct_vendor_name, axis=1)

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
    kering_file["Type"] = kering_file.apply(get_kids_on_type, axis = 1)

    # ========================================================= MAIN VALUES ==========================================
    # GET LENS COLOR
    def main_lens_color(row):
        items_lens_color = str(row["Metafield: my_fields.lens_color [single_line_text_field]"]).strip().title()
        if "Eyeglasses" not in row["Type"]:
            for mother, children in kering_lens_color.items():
                for color in children:
                    if items_lens_color == color.strip().title():
                        return mother
        return "DEMO"

    kering_file["Metafield: custom.main_lens_color [single_line_text_field]"] = kering_file.apply(main_lens_color,
                                                                                                  axis=1)
    print("LENS COLOR OK")

    # GET FRAME COLOR
    def get_main_frame_color(row):
        items_frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).strip().title()
        for mother, children in kering_frame_color.items():
            for color in children:
                if items_frame_color == color.strip().title():
                    return mother
        return "Miscellaneous"

    kering_file["Metafield: custom.main_frame_color [single_line_text_field]"] = kering_file.apply(get_main_frame_color,
                                                                                                   axis=1)
    print("FRAME COLOR OK")

    # MAIN FRAME SHAPE
    def main_frame_shape(row):
        items_frame_shape = str(row["Metafield: my_fields.frame_shape [single_line_text_field]"]).strip().title()
        for mother, children in kering_frame_shape.items():
            for shape in children:
                if items_frame_shape == shape.strip().title():
                    return mother
        return "Other"

    kering_file["Metafield: custom.main_frame_shape [single_line_text_field]"] = kering_file.apply(main_frame_shape,
                                                                                                   axis=1)
    print("FRAME SHAPE OK")

    # GET MAIN FRAME MATERIAL
    def get_main_frame_material(row):
        items_frame_material = str(row["Metafield: my_fields.frame_material [single_line_text_field]"]).strip().title()
        for mother, children in kering_frame_material.items():
            for material in children:
                if items_frame_material == material.strip().title():
                    return mother
        return "Other"

    kering_file["Metafield: custom.main_frame_material [single_line_text_field]"] = kering_file.apply(
        get_main_frame_material, axis=1)
    print("FRAME MATERIAL OK")

    # GET MAIN LENS TECHNOLOGY
    def get_main_lens_technology(row):
        items_lens_techno = str(row["Metafield: my_fields.lens_technology [single_line_text_field]"]).strip().title()
        if "Eyeglasses" not in row["Type"]:
            for mother, children in kering_lens_technology.items():
                for technology in children:
                    if items_lens_techno == technology.strip().title():
                        return mother
        return "Standard"

    kering_file["Metafield: custom.main_lens_technology [single_line_text_field]"] = kering_file.apply(
        get_main_lens_technology, axis=1)
    print("LENS TECNHO OK")

    # GET MAIN SIZE
    def get_main_size(row):
        val = row["Option1 Value"]

        if pd.isna(val) or val == "":
            return ""
        try:
            size_int = int(val)
        except ValueError:
            return ""

        if size_int < 48:
            return "S"
        elif size_int < 53:
            return "M"
        else:
            return "L"

    kering_file["Metafield: custom.main_size [single_line_text_field]"] = kering_file.apply(get_main_size, axis = 1)

    # ========================================================= TAGS ==========================================
    # GET TAGS
    # TAGS ARE UPDATE BY SCRAPER -> MANTAIN NEW OR BEST SELLER
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

        return ','.join(tags_list)
    kering_file["NewTags"] = kering_file.apply(generate_tags, axis = 1)

    kering_file["Tags"] = kering_file["NewTags"]
    kering_file.drop(columns=["NewTags"], inplace=True)

    # SE available now NON è PRESENTE NELLA LISTA TAG, IL TEMPLATE SUFFIX DEVE ESSERE "Default product"
    def get_template_suffix(row):
        lista_tag = row["Tags"]
        template = row["Template Suffix"]
        if template == "product-noindex":
            return "product-noindex"
        elif "available now" in lista_tag:
            return "disponibili-subito"
        return "Default product"
    kering_file["Template Suffix"] = kering_file.apply(get_template_suffix, axis = 1)

    # ====================================================== SAVE ======================================================

    kering_brands = kering_file["Vendor"].unique()
    for brand in kering_brands:
        try:
            mask = kering_file["Vendor"] == brand
            brand_file = kering_file[mask]
            brand_file.to_excel(
                f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/{brand}/{brand}.xlsx",
                index=False)
            print(f"{brand} saved successfully")
            with open(splitting_kering_brands, "a") as file:
                file.write(f"   {brand} saved successfully \n")
            time.sleep(1)
        except Exception as err:
            print(f"{type(err).__name__}: {err}")
            with open(splitting_kering_brands, "a") as file:
                file.write(f"   {brand} is not split due this error: \n {type(err).__name__}: {err} \n")


if __name__ == "__main__":
    try:
        with open(splitting_kering_brands, "a") as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n[{current_time}] Starting Kering splitting brands. \n")
        split_kering()

        with open(splitting_kering_brands, "a") as file:
            file.write(f"Kering brands are split successfully. \n")
            file.write(f"Closing Kering splitting brands. \n")

    except Exception as err:
        with open(splitting_kering_brands, "a") as file:
            file.write(f"Kering brands are not splitted due this error: {type(err).__name__}: {err} \n")
