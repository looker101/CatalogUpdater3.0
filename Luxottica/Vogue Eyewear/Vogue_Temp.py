import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, vogue_update, lux_only_templates


def get_vogue_templates():
    vogue_file = pd.read_excel(vogue_update)
    # vogue_file = vogue_file.dropna(axis = 0, how = "any",
    # subset=["Metafield: my_fields.frame_color [single_line_text_field]"])

    vogue_file = vogue_file[[
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

    vogue_file["Vendor"] = "Vogue Eyewear"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    vogue_file["Variant SKU"] = vogue_file.apply(remove_0_from_variant_sku, axis=1)

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
            return f"{brand} {model_code} {color_code} {frame_color} {style}"
        return f"{brand} {model_code} {color_code} {frame_color} {style} for {gender}"

    vogue_file["Metafield: title_tag [string]"] = vogue_file.apply(getMetaTitle, axis=1)

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

    vogue_file["Metafield: description_tag [string]"] = vogue_file.apply(getMetaDescription, axis=1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">Carefully designed to be trendy and fashionable, meticulously manufactured to be comfortable and last for years, and sold at unbelievably low prices when considering the exceptional quality, </span><strong>{brand} {style} </strong><span style="font-weight: 400;">is hard to beat.</span></p>
    <p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This stylish, unique</span><strong> {frame_color} </strong><span style="font-weight: 400;">model truly is a thing of beauty. Check out hundreds of new models and designs in the latest </span><span style="font-weight: 400;"><a href="/collections/vogue-sunglasses" target="_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Carefully designed to be trendy and fashionable, meticulously manufactured to be comfortable and last for years, and sold at unbelievably low prices when considering the exceptional quality, </span><strong>{brand} {style} </strong><span style="font-weight: 400;">is hard to beat.</span></p>
    <p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This stylish, unique</span><strong> {frame_color} </strong><span style="font-weight: 400;">model truly is a thing of beauty. Check out hundreds of new models and designs in the latest </span><span style="font-weight: 400;"><a href="/collections/vogue-eyeglasses" target="_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    vogue_file["Body HTML"] = vogue_file.apply(getProductDescription, axis=1)

    # Product Title
    def get_product_title(row):
        """brand Model_Code Color_Code"""
        brand = row["Vendor"]
        model_code = row["Variant SKU"][:-2]
        return f"{brand} {model_code}"

    vogue_file["Title"] = vogue_file.apply(get_product_title, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    vogue_file = vogue_file.dropna(axis=0, how='any',
                                   subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    vogue_file = vogue_file.sort_values("Handle")

    # Saving
    vogue_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Vogue Eyewear/Vogue_Eyewear_Templates.xlsx",
        index=False)
    print("Vogue updated and saved on Vogue folder")

    # vogue_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Vogue_Eyewear.xlsx", index=False)
    # print("Vogue updated and saved on Brand data processor folder")

    vogue_file.to_excel(
        f"{lux_only_templates}/VogueEyewear_templates.xlsx",
        index=False)
    print("Vogue updated and saved on Luxottica_import folder")


if __name__ == "__main__":
    get_vogue_templates()
