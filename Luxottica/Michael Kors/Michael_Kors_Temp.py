import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, michael_kors_update, lux_only_templates

def get_michael_kors_templates():
    michael_kors_file = pd.read_excel(michael_kors_update)
    
    michael_kors_file = michael_kors_file[[
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

    michael_kors_file["Vendor"] = "Michael Kors"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    michael_kors_file["Variant SKU"] = michael_kors_file.apply(remove_0_from_variant_sku, axis=1)

    # Create metaTitle
    # {Brand} {model_code} {color_code} {frame_color} for {geneder}
    def getMetaTitle(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_name = " ".join(row["Title"].split()[2:3])
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {product_name} {model_code} {color_code} {frame_color} {style}"
        return f"{brand} {product_name} {model_code} {color_code} {frame_color} {style} for {gender}"

    michael_kors_file["Metafield: title_tag [string]"] = michael_kors_file.apply(getMetaTitle, axis = 1)

    # Create MetaDescription
    def getMetaDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_name = " ".join(row["Title"].split()[2:3])
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        style = row["Type"].lower()

        return f"Buy the new {brand} {product_name} {model_code} {color_code} {style} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    michael_kors_file["Metafield: description_tag [string]"] = michael_kors_file.apply(getMetaDescription, axis = 1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_name = " ".join(row["Title"].split()[2:3])
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        lens_color = row["Metafield: my_fields.lens_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">Classic shapes, glamorous accents, and high-quality materials and detailing: </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> never cease to amaze.</span></p>
    <p><span style="font-weight: 400;">Beautifully designed by Michael Kors and perfectly crafted by world-leading eyewear manufacturer Luxottica, the new </span><strong>{frame_color} {product_name}</strong><span style="font-weight: 400;"> with </span><strong>{lens_color}</strong><span style="font-weight: 400;"> lenses are the ultimate designer sunglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">. Get yours today and add a touch of sophistication to your style!</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new</span><span style="font-weight: 400;"><a href="/collections/michael-kors-sunglasses" target="_blank"> {brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Classic shapes, glamorous accents, and high-quality materials and detailing: </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> never cease to amaze.</span></p>
    <p><span style="font-weight: 400;">Beautifully designed by Michael Kors and perfectly crafted by world-leading eyewear manufacturer Luxottica, the new </span><strong>{frame_color}</strong> <strong>{product_name}</strong><span style="font-weight: 400;"> are the ultimate designer eyeglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">. Get yours today and add a touch of sophistication to your style!&nbsp;</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new</span> <span style="font-weight: 400;"><a href="/collections/michael-kors-eyeglasses" target="_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    michael_kors_file["Body HTML"] = michael_kors_file.apply(getProductDescription, axis = 1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    michael_kors_file = michael_kors_file.dropna(axis = 0, how='any', subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    # SORT
    michael_kors_file = michael_kors_file.sort_values(by="Handle")

    # Saving
    michael_kors_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Michael Kors/Michael_Kors_Templates.xlsx", index = False)
    print("Michael Kors updated and saved on Michael Kors folder")

    # michael_kors_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Michael_Kors.xlsx")
    # print("Michael Kors updated and saved on Brand data processor folder")

    michael_kors_file.to_excel(
        f"{lux_only_templates}/Michael_Kors_Templates.xlsx",
        index=False)
    print("Michael Kors templates updated and saved in Luxottica_to_import_folder")
    
if __name__ == "__main__":
    get_michael_kors_templates()