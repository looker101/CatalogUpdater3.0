import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, ray_ban_update, lux_only_templates


def get_ray_ban_templates():
    ray_ban_file = pd.read_excel(ray_ban_update)
    # ray_ban_file = ray_ban_file.dropna(axis = 0, how = "any",
    # subset=["Metafield: my_fields.frame_color [single_line_text_field]"])

    ray_ban_file = ray_ban_file[[
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

    ray_ban_file["Vendor"] = "Ray-Ban"
    ray_ban_file["Title"] = ray_ban_file["Title"].str.replace("Ray-ban", "Ray-Ban")

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        variant_sku = row["Variant SKU"]
        if isinstance(variant_sku, str) and variant_sku.startswith("0"):
            return variant_sku.replace("0", "", 1)
        return variant_sku

    ray_ban_file["Variant SKU"] = ray_ban_file.apply(remove_0_from_variant_sku, axis=1)

    # def get_kids_tag(row):
    #     if row["Type"] == "Eyeglasses Kids" or row["Type"] == "Sunglasses Kids":
    #         return "Kids"
    #     return row["Metafield: my_fields.for_who [single_line_text_field]"]
    #
    # ray_ban_file["Metafield: my_fields.for_who [single_line_text_field]"] = ray_ban_file.apply(get_kids_tag, axis = 1)

    # Create metaTitle
    # {Brand} {model_code} {color_code} {frame_color} for {geneder}
    def getMetaTitle(row):
        item_title = row["Title"]
        style = row["Type"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{item_title} {frame_color} {style}"
        return f"{item_title} {frame_color} {style} for {gender}"

    ray_ban_file["Metafield: title_tag [string]"] = ray_ban_file.apply(getMetaTitle, axis=1)

    # Create MetaDescription
    def getMetaDescription(row):
        item_title = row["Title"]
        style = row["Type"].lower()
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        return f"Buy the new {item_title} {style} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    ray_ban_file["Metafield: description_tag [string]"] = ray_ban_file.apply(getMetaDescription, axis=1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        item_title = " ".join(row["Title"].split()[1:])
        style = row["Type"].lower()
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = ["Metafield: my_fields.for_who [single_line_text_field]"]

        sun = f"""<p><strong>{brand} {style} </strong><span style="font-weight: 400;">is like no other: you get one pair today and wear it until the end of time. Everyone knows that.</span></p>
    <p><span style="font-weight: 400;">This elegant, timeless</span><strong> {frame_color} </strong><span style="font-weight: 400;">model was designed to perfection by </span><strong>{brand}</strong><span style="font-weight: 400;"> in collaboration with world leading manufacturer Luxottica. An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the</span><strong> {item_title} </strong><span style="font-weight: 400;">is the ultimate definition of style.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><span style="font-weight: 400;"><a href="/collections/ray_ban-sunglasses" target = "_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><strong>{brand} {style} </strong><span style="font-weight: 400;">is like no other: you get one pair today and wear it until the end of time. Everyone knows that.</span></p>
    <p><span style="font-weight: 400;">This elegant, timeless</span><strong> {frame_color} </strong><span style="font-weight: 400;">model was designed to perfection by </span><strong>{brand}</strong><span style="font-weight: 400;"> in collaboration with world leading manufacturer Luxottica. An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the</span><strong> {item_title} </strong><span style="font-weight: 400;">is the ultimate definition of style.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><span style="font-weight: 400;"><a href="/collections/ray_ban-eyeglasses" target = "_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    ray_ban_file["Body HTML"] = ray_ban_file.apply(getProductDescription, axis=1)

    ray_ban_file = ray_ban_file.sort_values("Handle")

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    ray_ban_file = ray_ban_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    # Saving
    ray_ban_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Ray-Ban/Ray-Ban_Templates.xlsx",
        index=False)
    print("Ray-Ban updated and saved on Ray-Ban folder")

    # ray_ban_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Ray-Ban.xlsx", index=False)
    # print("Ray-Ban updated and saved on Brand data processor folder")

    ray_ban_file.to_excel(
        f"{lux_only_templates}/Ray-Ban_templates.xlsx",
        index=False)
    print("Ray-Ban updated and saved on Luxottica_import folder")


if __name__ == "__main__":
    get_ray_ban_templates()
