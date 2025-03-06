import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, swarovski_update, lux_only_templates


def get_swarovski_templates():
    swarovski_file = pd.read_excel(swarovski_update)
    # swarovski_file = swarovski_file.dropna(axis = 0, how = "any", subset=["Metafield: my_fields.frame_color [single_line_text_field]"])

    swarovski_file = swarovski_file[[
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

    swarovski_file["Vendor"] = "Swarovski"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    swarovski_file["Variant SKU"] = swarovski_file.apply(remove_0_from_variant_sku, axis=1)

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

    swarovski_file["Metafield: title_tag [string]"] = swarovski_file.apply(getMetaTitle, axis=1)

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

    swarovski_file["Metafield: description_tag [string]"] = swarovski_file.apply(getMetaDescription, axis=1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> are a synonym for class and distinction, elegance and style.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">The </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> is an ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">. This timeless, unique </span><strong>{frame_color}</strong><span style="font-weight: 400;"> frame really is a thing of absolute beauty. Carefully designed and manufactured by world-leading eyewear manufacturer Luxottica, these Swarovski eyeglasses are the ultimate head-turners.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/swarovski-sunglasses" target="_blank">{brand} {style} 2025</a> collection.</span></p>"""

        eye = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> are a synonym for class and distinction, elegance and style.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">The </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> is an ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">. This timeless, unique </span><strong>{frame_color}</strong><span style="font-weight: 400;"> frame really is a thing of absolute beauty. Carefully designed and manufactured by world-leading eyewear manufacturer Luxottica, these Swarovski eyeglasses are the ultimate head-turners.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/swarovski-sunglasses" target="_blank">{brand} {style} 2025</a> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    swarovski_file["Body HTML"] = swarovski_file.apply(getProductDescription, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    swarovski_file = swarovski_file.dropna(axis=0, how='any',
                                           subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    swarovski_file = swarovski_file.sort_values("Handle")

    # Saving
    swarovski_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Swarovski/Swarovski_Templates.xlsx",
        index=False)
    print("Swarovski updated and saved on Swarovski folder")

    # swarovski_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Swarovski.xlsx", index=False)
    # print("Swarovski updated and saved on Brand data processor folder")

    swarovski_file.to_excel(
        f"{lux_only_templates}/Swarovski_templates.xlsx",
        index=False)
    print("Swarovski templates updated and saved in Luxottica_to_import_folder.")


if __name__ == "__main__":
    get_swarovski_templates()
