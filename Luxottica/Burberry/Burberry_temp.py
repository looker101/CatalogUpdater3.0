import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, burberry_update, lux_only_templates

def get_burberry_temp():
    burberry_file = pd.read_excel(burberry_update)
    
    burberry_file = burberry_file[[
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
    

    burberry_file["Vendor"] = "Burberry"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    burberry_file["Variant SKU"] = burberry_file.apply(remove_0_from_variant_sku, axis = 1)

    def getMetaTitle(row):
        brand = row["Vendor"]
        product_name = ""
        if len(row["Title"].split()) == 3:
            product_name = ""
        elif len(row["Title"].split()) == 4:
            product_name = row["Title"].split()[1]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"]
        #gender = ""
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {product_name} {model_code} {color_code} {frame_color} {style}"

        return f"{brand} {product_name} {model_code} {color_code} {frame_color} {style} for {gender}"

    burberry_file["Metafield: title_tag [string]"] = burberry_file.apply(getMetaTitle, axis =1)

    def getMetaDescription(row):
        brand = row["Vendor"]
        product_name = ""
        if len(row["Title"].split()) == 3:
            product_name = ""
        elif len(row["Title"].split()) == 4:
            product_name = row["Title"].split()[1]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"]
        gender = ""
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        return f"Buy the new {brand} {product_name} {model_code} {color_code} {style} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    burberry_file["Metafield: description_tag [string]"] = burberry_file.apply(getMetaDescription, axis = 1)

    def getProductDescription(row):
        brand = row["Vendor"]
        product_name = ""
        if len(row["Title"].split()) == 3:
            product_name = ""
        elif len(row["Title"].split()) == 4:
            product_name = row["Title"].split()[1]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"]
        gender = ""
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        eye = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> are synonymous for excellence and style, refined aesthetics and classic-meets-modern designs.</span></p>
    <p><span style="font-weight: 400;">The</span><strong> {product_name} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This elegant, timeless</span><strong> light gold </strong><span style="font-weight: 400;">model was designed and carefully manufactured by </span><strong>{brand}</strong><span style="font-weight: 400;"> together with eyewear world leader </span><strong>Luxottica</strong><span style="font-weight: 400;"> to offer a sunglass that has no equal.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the </span><a href="/collections/burberry-eyeglasses" target="_blank"><span style="font-weight: 400;">new {brand} {style} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>
    <p>&nbsp;</p>"""

        sun = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> are synonymous for excellence and style, refined aesthetics and classic-meets-modern designs.</span></p>
    <p><span style="font-weight: 400;">The</span><strong> {product_name} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This elegant, timeless</span><strong> light gold </strong><span style="font-weight: 400;">model was designed and carefully manufactured by </span><strong>{brand}</strong><span style="font-weight: 400;"> together with eyewear world leader </span><strong>Luxottica</strong><span style="font-weight: 400;"> to offer a sunglass that has no equal.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the </span><a href="/collections/burberry-sunglasses" target="_blank"><span style="font-weight: 400;">new {brand} {style} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>
    <p>&nbsp;</p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    burberry_file["Body HTML"] = burberry_file.apply(getProductDescription, axis = 1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    burberry_file = burberry_file.dropna(axis = 0, how='any', subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    # Sort
    burberry_file = burberry_file.sort_values(by="Handle")

    # Saving
    burberry_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Burberry/Burberry_Templates.xlsx", index = False)
    print("Burberry updated and saved on Burberry folder")

    # burberry_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Burberry.xlsx", index = False)
    # print("Burberry updated and saved on Brand data processor folder")

    burberry_file.to_excel(f"{lux_only_templates}/Burberry_templates.xlsx", index = False)
    print("templates updated and saved in Luxottica_to_import_folder")

if __name__ == "__main__":
    try:
        print("Editing Burberry Templates..")
        get_burberry_temp()
        print("Burberry edited successfully")
    except Exception as err:
        print(f"{type(err).__name__}")