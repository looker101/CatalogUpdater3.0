import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, tiffany_update, lux_only_templates


def get_tiffany_templates():
    tiffany_file = pd.read_excel(tiffany_update)
    # tiffany_file = tiffany_file.dropna(axis = 0, how = "any", subset=["Metafield: my_fields.frame_color [single_line_text_field]"])

    tiffany_file = tiffany_file[[
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

    tiffany_file["Vendor"] = "Tiffany"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    tiffany_file["Variant SKU"] = tiffany_file.apply(remove_0_from_variant_sku, axis=1)

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

    tiffany_file["Metafield: title_tag [string]"] = tiffany_file.apply(getMetaTitle, axis=1)

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

    tiffany_file["Metafield: description_tag [string]"] = tiffany_file.apply(getMetaDescription, axis=1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">{brand} {style} embody the timeless elegance and iconic style of the New York luxury brand. The </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> model is crafted from high-quality materials and adorned with exquisite details, including the signature Tiffany accents and delicate metallic touches.</span></p>
    <p><span style="font-weight: 400;">These sunglasses are more than just a luxury accessory; they are a statement of sophistication and femininity, perfect for those who want to combine elegance and style for any occasion. Wear Tiffany to add a touch of everlasting class to your look.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models in the <a href="/collections/tiffany-co-sunglasses" target="_blank">{brand} {style} 2025</a> collection.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">{brand} {style} are a perfect blend of modern elegance and classic sophistication, embodying the essence of the iconic New York brand. The </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> model features a sleek design with delicate accents, such as the signature Tiffany blue and refined metallic elements.</span></p>
    <p><span style="font-weight: 400;">Ideal for both professional and casual settings, these eyeglasses offer not only superior comfort but also a distinctive style that elevates any outfit. Wear Tiffany eyeglasses to showcase your appreciation for timeless luxury and unparalleled craftsmanship.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models in the <a href="/collections/tiffany-co-eyeglasses" target="_blank">{brand} {style} 2025</a> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    tiffany_file["Body HTML"] = tiffany_file.apply(getProductDescription, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    tiffany_file = tiffany_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    tiffany_file = tiffany_file.sort_values("Handle")

    # Saving
    tiffany_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Tiffany/Tiffany_Templates.xlsx",
        index=False)
    print("Tiffany updated and saved on Tiffany folder")

    # tiffany_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Tiffany.xlsx", index = False)
    # print("Tiffany templates updated and saved in templates_to_import_folder.")

    tiffany_file.to_excel(
        f"{lux_only_templates}/Tiffany_templates.xlsx",
        index=False)
    print("Tiffany updated and saved on Luxottica_import folder")


if __name__ == "__main__":
    get_tiffany_templates()
