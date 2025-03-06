import pandas as pd
import datetime
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from de_rigo_paths import splitting_logs, derigo_backup
from derigo_mapping_color_and_frame import derigo_lens_color, derigo_lens_technology, derigo_frame_material,\
    derigo_frame_color

de_rigo_file = pd.read_excel(derigo_backup)

de_rigo_file = de_rigo_file.drop("Image Src", axis=1)
de_rigo_file = de_rigo_file.dropna(how="any", axis=0, subset=["Variant ID"])

# de_rigo_file["Vendor"] = de_rigo_file["Vendor"].astype(str)
#de_rigo_file["Tags"] = de_rigo_file["Tags"].astype(str)


def get_de_rigo_brands():

    # ====================================================MAIN VALUES==================================================
    # GET MAIN LENS COLOR
    def get_main_lens_color(row):
        items_lens_color = str(row["Metafield: my_fields.lens_color [single_line_text_field]"]).strip().title()
        if not isinstance(items_lens_color, str):
            return ""
        if "Eyeglasses" not in row["Type"]:
            for mother, children in derigo_lens_color.items():
                for color in children:
                    if items_lens_color == color.strip().title():
                        return mother
            return "Miscellaneous"
        return "DEMO"

    de_rigo_file["Metafield: custom.main_lens_color [single_line_text_field]"] = de_rigo_file.apply(get_main_lens_color,
                                                                                                    axis=1)

    # GET MAIN FRAME COLOR
    def get_main_frame_color(row):
        items_frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).strip().title()
        if not isinstance(items_frame_color, str):
            return ""
        for mother, children in derigo_frame_color.items():
            for colore in children:
                if items_frame_color == colore.strip().title():
                    return mother
        return "Miscellaneous"

    de_rigo_file["Metafield: custom.main_frame_color [single_line_text_field]"] = de_rigo_file.apply(
        get_main_frame_color, axis=1)

    # GET MAIN LENS TECHNOLOGY
    def get_main_lens_technology(row):
        items_lens_technology = str(
            row["Metafield: my_fields.lens_technology [single_line_text_field]"]).strip().title()
        if not isinstance(items_lens_technology, str):
            return ""
        for mother, children in derigo_lens_technology.items():
            for techno in children:
                if items_lens_technology == techno.strip().title():
                    return mother
        return "Standard"

    de_rigo_file["Metafield: custom.main_lens_technology [single_line_text_field]"] = de_rigo_file.apply(
        get_main_lens_technology, axis=1)

    # GET MAIN FRAME MATERIAL
    def get_main_frame_material(row):
        items_frame_material = str(row["Metafield: my_fields.frame_material [single_line_text_field]"]).strip().title()
        if not isinstance(items_frame_material, str):
            return ""
        for mother, children in derigo_frame_material.items():
            for materiale in children:
                if items_frame_material == materiale.strip().title():
                    return mother
        return "Other"

    de_rigo_file["Metafield: custom.main_frame_material [single_line_text_field]"] = de_rigo_file.apply(
        get_main_frame_material, axis=1)

    # GET MAIN SIZE
    def get_main_size(row):
        item_size = row["Option1 Value"]
        if pd.isna(item_size) or item_size == "":
            return ""

        try:
            size = int(item_size)
        except ValueError:
            return ""

        if size < 48:
            return "S"
        elif size < 53:
            return "M"
        else:
            return "L"

    de_rigo_file["Metafield: custom.main_size [single_line_text_field]"] = de_rigo_file.apply(get_main_size, axis=1)

    # ========================================================TAGS=====================================================
    # Considera che new e best seller li prende lo scraper
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
    de_rigo_file["NewTags"] = de_rigo_file.apply(generate_tags, axis=1)

    de_rigo_file["Tags"] = de_rigo_file["NewTags"]
    de_rigo_file.drop(columns=["NewTags"], inplace=True)
    
    # SE available now NON è PRESENTE NELLA LISTA TAG, IL TEMPLATE SUFFIX DEVE ESSERE "Default product"
    def get_template_suffix(row):
        lista_tag = row["Tags"]
        template = row["Template Suffix"]
        if template == "product-noindex":
            return "product-noindex"
        elif "available now" in lista_tag:
            return "disponibili-subito"
        return "Default product"
    de_rigo_file["Template Suffix"] = de_rigo_file.apply(get_template_suffix, axis = 1)

    # ====================================================== SAVE ======================================================

    de_rigo_brands = de_rigo_file["Vendor"].unique()
    for brand in de_rigo_brands:
        try:
            mask = de_rigo_file["Vendor"] == brand
            brand_file = de_rigo_file[mask]
            # brand_file["Vendor"] = brand_file["Vendor"].str.title()
            brand_file.to_excel(
                f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/De_Rigo/{brand}/{brand}.xlsx",
                index=False)
            print(f"Excel file saved for {brand} brand.")
            with open(splitting_logs, "a") as file:
                file.write(f"   {brand} are split successfully \n")
        except Exception as err:
            with open(splitting_logs, "a") as file:
                file.write(f"   {brand} are not split due this error: \n {type(err).__name__}: {err} \n")


if __name__ == "__main__":
    try:
        with open(splitting_logs, "a") as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n[{current_time}] Starting DeRigo splitting brands \n")
        get_de_rigo_brands()

        with open(splitting_logs, "a") as file:
            file.write(f"De Rigo's brand are split successfully \n")
            file.write(f"Closing DeRigo splitting brands \n")
    except Exception as err:
        with open(splitting_logs, "a") as file:
            file.write(f"De Rigo'0s brands are not split due this error: \n {type(err).__name__}: {err}")
