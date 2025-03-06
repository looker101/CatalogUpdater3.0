import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, persol_update, lux_only_templates


def get_persol_templates():
    persol_file = pd.read_excel(persol_update)
    # persol_file = persol_file.dropna(axis = 0, how = "any",
    # subset=["Metafield: my_fields.frame_color [single_line_text_field]"])

    persol_file = persol_file[[
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

    persol_file["Vendor"] = "Persol"

    # Remove "0" from Variant SKU
    # def remove_0_from_variant_sku(row):
    #     if row["Variant SKU"].startswith("0"):
    #         return row["Variant SKU"].replace("0", "", 1)
    #     return row["Variant SKU"]
    #
    # persol_file["Variant SKU"] = persol_file.apply(remove_0_from_variant_sku, axis=1)

    # Create metaTitle
    # {Brand} {model_code} {color_code} {frame_color} for {geneder}
    def getMetaTitle(row):
        brand = row["Vendor"]
        style = row["Type"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {style} {model_code} {color_code} {frame_color}"
        return f"{brand} {style} {model_code} {color_code} {frame_color} for {gender}"

    persol_file["Metafield: title_tag [string]"] = persol_file.apply(getMetaTitle, axis=1)

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

    persol_file["Metafield: description_tag [string]"] = persol_file.apply(getMetaDescription, axis=1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><strong>{brand} {style} </strong><span style="font-weight: 400;">is like no other: you get one pair today and wear it until the end of time. Everyone knows that.</span></p>
    <p><span style="font-weight: 400;">This elegant, timeless</span><strong> {frame_color} </strong><span style="font-weight: 400;">model was designed to perfection by </span><strong>{brand}</strong><span style="font-weight: 400;"> in collaboration with world leading manufacturer Luxottica. An ideal choice for </span><strong>man</strong><span style="font-weight: 400;">, the</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is the ultimate definition of style.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><span style="font-weight: 400;"><a href="/collections/persol-sunglasses" target = "_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><strong>{brand} {style} </strong><span style="font-weight: 400;">is like no other: you get one pair today and wear it until the end of time. Everyone knows that.</span></p>
    <p><span style="font-weight: 400;">This elegant, timeless</span><strong> {frame_color} </strong><span style="font-weight: 400;">model was designed to perfection by </span><strong>{brand}</strong><span style="font-weight: 400;"> in collaboration with world leading manufacturer Luxottica. An ideal choice for </span><strong>man</strong><span style="font-weight: 400;">, the</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is the ultimate definition of style.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><span style="font-weight: 400;"><a href="/collections/persol-eyeglasses" target = "_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    persol_file["Body HTML"] = persol_file.apply(getProductDescription, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    persol_file = persol_file.dropna(axis=0, how='any',
                                     subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    persol_file = persol_file.sort_values("Handle")

    # Saving
    persol_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Persol/Persol_Templates.xlsx",
        index=False)
    print("Persol updated and saved on Persol folder")

    # persol_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Persol.xlsx", index = False)
    # print("Persol updated and saved on Brand data processor folder")

    persol_file.to_excel(
        f"{lux_only_templates}/Persol_templates.xlsx",
        index=False)
    print("Persol templates updated and saved in Luxottica_to_import_folder")


if __name__ == "__main__":
    get_persol_templates()
