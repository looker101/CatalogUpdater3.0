import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, versace_update, lux_only_templates

def get_versace_templates():

    versace_file = pd.read_excel(versace_update)
    #versace_file = versace_file.dropna(axis = 0, how = "any", subset=["Metafield: my_fields.frame_color [single_line_text_field]"])

    versace_file = versace_file[[
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


    versace_file["Vendor"] = "Versace"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    versace_file["Variant SKU"] = versace_file.apply(remove_0_from_variant_sku, axis=1)

    # Create metaTitle
    # {Brand} {model_code} {color_code} {frame_color} for {geneder}
    def getMetaTitle(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        #gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {model_code} {color_code} {frame_color} {style}"
        else:
            return f"{brand} {model_code} {color_code} {frame_color} {style} for {gender}"

    versace_file["Metafield: title_tag [string]"] = versace_file.apply(getMetaTitle, axis = 1)

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

    versace_file["Metafield: description_tag [string]"] = versace_file.apply(getMetaDescription, axis = 1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> needs no introduction. The Italian brand has been at the forefront of the fashion world for more than 40 years and has succeeded at mixing luxury fashion with pop culture like very few others. The match between classical elements and symbols, like the iconic Medusa, with ambitious motifs and styles, lives on in Versace's latest eyeglasses collection.</span></p>
    <p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">. This elegant </span><strong>{color_code} </strong><span style="font-weight: 400;">model was designed and manufactured to perfection by world-leading eyewear producer Luxottica to display Versace's bold style.</span></p>
    <p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><span style="font-weight: 400;"><a href="/collections/versace-sunglasses" target="_blank">{brand} {style} 2025</span><span style="font-weight: 400;"> collection.</span></p>"""

        eye = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> needs no introduction. The Italian brand has been at the forefront of the fashion world for more than 40 years and has succeeded at mixing luxury fashion with pop culture like very few others. The match between classical elements and symbols, like the iconic Medusa, with ambitious motifs and styles, lives on in Versace's latest eyeglasses collection.</span></p>
    <p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">. This elegant </span><strong>{color_code} </strong><span style="font-weight: 400;">model was designed and manufactured to perfection by world-leading eyewear producer Luxottica to display Versace's bold style.</span></p>
    <p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><span style="font-weight: 400;"><a href="/collections/versace-eyeglasses" target="_blank">{brand} {style} 2025</span><span style="font-weight: 400;"> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    versace_file["Body HTML"] = versace_file.apply(getProductDescription, axis = 1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    versace_file = versace_file.dropna(axis = 0, how='any', subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    versace_file = versace_file.sort_values("Handle")

    # Saving
    versace_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Versace/Versace_Templates.xlsx", index = False)
    print("Versace updated and saved on Versace folder")

    # versace_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Versace.xlsx", index=False)
    # print("Versace updated and saved on Brand data processor folder")

    versace_file.to_excel(
        f"{lux_only_templates}/Versace_templates.xlsx",
        index=False)
    print("Versace templates updated and saved in Luxottica_to_import_folder.")
    
if __name__ == "__main__":
    get_versace_templates()