import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, plr_update, lux_only_templates


def get_prada_linea_rossa_templates():
    # from Burberry.Burberry_temp import getMetaDescription

    prada_linea_rossa_file = pd.read_excel(plr_update)

    # prada_linea_rossa_file = prada_linea_rossa_file.dropna(axis = 0, how = "any",
    # subset=["Metafield: my_fields.frame_color [single_line_text_field]"])

    prada_linea_rossa_file = prada_linea_rossa_file[[
        "ID", "Handle", "Command", "Title", "Body HTML",
        "Vendor", "Type", "Tags", "Tags Command",
        "Status", "Template Suffix", "URL", "Variant ID", "Variant SKU",
        "Variant Barcode",
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
        "Metafield: custom.main_frame_shape [single_line_text_field]",
        "Metafield: custom.main_frame_material [single_line_text_field]",
        "Metafield: custom.main_frame_color [single_line_text_field]",
        "Metafield: custom.main_lens_color [single_line_text_field]",
        "Metafield: custom.main_lens_technology [single_line_text_field]",
        "Metafield: custom.main_size [single_line_text_field]"
    ]]

    prada_linea_rossa_file["Vendor"] = "Prada Linea Rossa"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    prada_linea_rossa_file["Variant SKU"] = prada_linea_rossa_file.apply(remove_0_from_variant_sku, axis=1)

    # Create metaTitle
    # {Brand} {model_code} {color_code} {frame_color} for {geneder}
    def getMetaTitle(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {model_code} {color_code} {style} {frame_color}"
        return f"{brand} {model_code} {color_code} {style} {frame_color} for {gender}"

    prada_linea_rossa_file["Metafield: title_tag [string]"] = prada_linea_rossa_file.apply(getMetaTitle, axis=1)

    # Create MetaDescription
    def getMetaDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        style = row["Type"].lower()

        return f"Buy the new {brand} {style} {model_code} {color_code} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    prada_linea_rossa_file["Metafield: description_tag [string]"] = prada_linea_rossa_file.apply(getMetaDescription,
                                                                                                 axis=1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">{brand}, influenced by the world of sports and 90s' aesthetics, is all about dynamic designs, versatility, and sustainable materials.</span></p>
    <p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code}</strong><span style="font-weight: 400;"> is the perfect choice for</span><strong> man</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This super-stylish, unique,</span><strong> {frame_color}</strong><span style="font-weight: 400;">model was designed and manufactured by Prada in collaboration with world leading eyewear producer Luxottica. These </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> are the perfect choice for those who seek premium comfort and performance but don't want to compromise on style.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><span style="font-weight: 400;"><a href="/collections/prada-linea-rossa-sunglasses" target="_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">{brand}, influenced by the world of sports and 90s' aesthetics, is all about dynamic designs, versatility, and sustainable materials.</span></p>
    <p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code}</strong><span style="font-weight: 400;"> is the perfect choice for</span><strong> man</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This super-stylish, unique,</span><strong> {frame_color}</strong><span style="font-weight: 400;">model was designed and manufactured by Prada in collaboration with world leading eyewear producer Luxottica. These </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> are the perfect choice for those who seek premium comfort and performance but don't want to compromise on style.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><span style="font-weight: 400;"><a href="/collections/prada-linea-rossa-eyeglasses" target="_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    prada_linea_rossa_file = prada_linea_rossa_file.sort_values("Handle")

    prada_linea_rossa_file["Body HTML"] = prada_linea_rossa_file.apply(getProductDescription, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    prada_linea_rossa_file = prada_linea_rossa_file.dropna(axis=0, how='any', subset=[
        'Metafield: my_fields.lens_color [single_line_text_field]'])

    prada_linea_rossa_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Prada Linea Rossa/Prada_Linea_Rossa_Template.xlsx",
        index=False)
    print("Prada Linea Rossa updated and saved on Prada Linea Rossa folder")

    # prada_linea_rossa_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Prada Linea Rossa.xlsx",
    #                                 index = False)
    # print("Prada Linea Rossa updated and saved on Brand data processor folder")

    prada_linea_rossa_file.to_excel(
        f"{lux_only_templates}/PLR_templates.xlsx",
        index=False)
    print("Prada Linea Rossa updated and saved on Luxottica_import folder")


if __name__ == "__main__":
    get_prada_linea_rossa_templates()
