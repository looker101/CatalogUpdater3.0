import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, emporio_armani_update, lux_only_templates


def get_emporio_armani_templates():
    emporio_armani_file = pd.read_excel(emporio_armani_update)

    emporio_armani_file = emporio_armani_file[[
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

    emporio_armani_file["Vendor"] = "Emporio Armani"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    emporio_armani_file["Variant SKU"] = emporio_armani_file.apply(remove_0_from_variant_sku, axis=1)

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

    emporio_armani_file["Metafield: title_tag [string]"] = emporio_armani_file.apply(getMetaTitle, axis=1)

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
        style = row["Type"]

        return f"Buy the new {brand} {style} {model_code} {color_code} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    emporio_armani_file["Metafield: description_tag [string]"] = emporio_armani_file.apply(getMetaDescription, axis=1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">Crafted with precision and finesse, the </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> collection is celebrated for its attention to detail and premium materials. The </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> model, a testament to the brand's commitment to excellence, exemplifies a perfect blend of style and comfort.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">Designed in collaboration with renowned eyewear manufacturer Luxottica, these sunglasses assure unparalleled quality. Whether you're making a professional statement or adding a finishing touch to your casual ensemble, these gorgeous Emporio Armani shades guarantee to boost your style.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/emporio-armani-sunglasses" target="_blank">{brand} {style} 2025 collection</a> and embrace a vision of elegance that stands the test of time.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Crafted with precision and finesse, </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> are celebrated for their attention to detail and premium materials. The </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> model, a testament to the brand's commitment to excellence, exemplifies a perfect blend of style and comfort.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">Designed in collaboration with renowned eyewear manufacturer Luxottica, these eyeglasses assure unparalleled quality. Whether you're making a professional statement or adding a finishing touch to your casual ensemble, these gorgeous Giorgio Armani spectacles guarantee to boost your style.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/emporio-armani-eyeglasses" target="_blank">{brand} {style} 2025 collection</a> and embrace a vision of elegance that stands the test of time.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    emporio_armani_file["Body HTML"] = emporio_armani_file.apply(getProductDescription, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    emporio_armani_file = emporio_armani_file.dropna(axis=0, how='any', subset=[
        'Metafield: my_fields.lens_color [single_line_text_field]'])

    # SORT
    emporio_armani_file = emporio_armani_file.sort_values(by="Handle")

    # Saving
    emporio_armani_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Emporio Armani/Emporio_Armani_Templates.xlsx",
        index=False)
    print("Emporio Armani updated and saved on Emporio Armani folder")

    # emporio_armani_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Emporio Armani.xlsx", index = False)
    # print("Emporio Armani updated and saved on Brand data processor folder")

    emporio_armani_file.to_excel(f"{lux_only_templates}/EmporioArmani_templates.xlsx", index=False)
    print("Emporio Armani templates updated and saved in Luxottica_to_import_folder.")


if __name__ == "__main__":
    get_emporio_armani_templates()
