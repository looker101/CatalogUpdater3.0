import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, arnette_update, lux_only_templates

# from Luxottica_paths import arnette_folder, brand_data_processor, to_import_folder

def get_arnette_template():
    # Read arnette file
    arnette_file = pd.read_excel(arnette_update)

    arnette_file = arnette_file[[
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

    arnette_file["Vendor"] = "Arnette"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]
    arnette_file["Variant SKU"] = arnette_file.apply(remove_0_from_variant_sku, axis = 1)

    # Create metaTitle
    def getMetaTitle(row):
        brand = row["Vendor"]
        product_name = row["Title"].split()[1]
        model_code = row["Title"].split()[2]
        color_code = row["Title"].split()[3]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {product_name} {model_code} {color_code} {frame_color} {style}"
        return f"{brand} {product_name} {model_code} {color_code} {frame_color} {style} for {gender}"

    arnette_file["Metafield: title_tag [string]"] = arnette_file.apply(getMetaTitle, axis=1)

    # Create Meta Description
    def getMetaDescription(row):
        brand = row["Vendor"]
        product_name = row["Title"].split()[1]
        model_code = row["Title"].split()[2]
        color_code = row["Title"].split()[3]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"].lower()
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        return f"Buy the new {brand} {product_name} {model_code} {color_code} {style} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    arnette_file["Metafield: description_tag [string]"] = arnette_file.apply(getMetaDescription, axis=1)

    # Create product description (Body HTML)
    def getProductDescription(row):
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        product_name = row["Title"].split()[1]

        sun = f'''<p><span style="font-weight: 400;">Loved by trendsetters and action sports enthusiasts, </span><strong>Arnette sunglasses</strong><span style="font-weight: 400;"> boast a distinctive urban style tht sets them apart. Designed to withstand active lifestyles, these shades capture the essence of youth and adventure.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">This exceptional </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model is a testament to Arnette's commitment to quality and style. Crafted with eyewear industry leader Luxottica, the </span><strong>{product_name}</strong><span style="font-weight: 400;"> is the perfect choice for those who appreciate fashion and functionality.</span></p>
    <p><br /><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/arnette-sunglasses" target="_blank">Arnette sunglasses 2025</span><span style="font-weight: 400;"> collection!</span></p>'''

        eye = f'''<p><span style="font-weight: 400;">&nbsp;Renowned for their urban-inspired designs and durability, </span><strong>Arnette eyeglasses</strong><span style="font-weight: 400;"> offer a unique blend of style and functionality. Crafted with an emphasis on quality, these frames are perfect for individuals who seek both fashion and comfort.</span></p>
<p><span style="font-weight: 400;">This exceptional </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model is a testament to Arnette's commitment to quality and style. Crafted with eyewear industry leader Luxottica, the </span><strong>{product_name}</strong><span style="font-weight: 400;"> is the perfect choice for those who appreciate fashion and functionality.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new</span><span style="font-weight: 400;"> <a href="/collections/arnette-eyeglasses" target="_blank">Arnette eyeglasses 2025</a> collection!</span></p>'''

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    arnette_file["Body HTML"] = arnette_file.apply(getProductDescription, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    arnette_file = arnette_file.dropna(axis = 0, how='any', subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    # SORT
    arnette_file = arnette_file.sort_values(by="Handle")

    # Saving
    arnette_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Arnette/Arnette_Templates.xlsx",
        index=False)
    print("Arnette updated and saved on Arnette folder")

    arnette_file.to_excel(f"{lux_only_templates}/Arnette_templates.xlsx", index = False)
    print("Arnette templates updated and saved in Luxottica_to_import_templates.")


    # arnette_file.to_excel(
    #     "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Arnette.xlsx",
    #     index=False)
    # print("Arnette updated and saved on Brand data processor folder")


if __name__ == "__main__":
    try:
        get_arnette_template()
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
