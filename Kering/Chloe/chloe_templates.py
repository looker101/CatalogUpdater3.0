import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from kering_paths import chloe_folder, chloe_excel, chloe_for_temp, templates

def chloe_templates_updater():
    chloe = pd.read_excel(chloe_excel)
    
    chloe = chloe[[
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

    def get_metatitle(row):
        """brand | model_code | color_code | - type for gender | LookerOnline"""
        title = row["Title"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]
        return f"{title} - {frame_color} {product_type} for {gender} | LookerOnline"

    chloe["Metafield: title_tag [string]"] = chloe.apply(get_metatitle, axis = 1)

    def get_metadescription(row):
        title = row["Title"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]
        return f"Buy the new {title} {product_type} at a bargain price This super stylish, unique{frame_color} model is the ideal choice for {gender} | FREE SHIPPING"

    chloe["Metafield: description_tag [string]"] = chloe.apply(get_metadescription, axis = 1)

    def get_product_description(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"][1]
        color_code = row["Variant SKU"][2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        lens_color = row["Metafield: my_fields.lens_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">Chic and fashionable designs, unconventional details and unique color combinations, high-quality materials and craftsmanship: </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are always the perfect choice.</span></p>
<p><span style="font-weight: 400;">Beautifully designed by Chlo&eacute; and perfectly crafted by world-leading eyewear manufacturer Kering, the new </span><strong>{frame_color}</strong> <strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> with </span><strong>{lens_color}</strong><span style="font-weight: 400;"> lenses are the ultimate designer sunglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">. Get yours today and add a touch of sophistication to your style!</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new</span> <a href="/collections/chloe-sunglasses" target="_blank" rel="noopener">{brand} {product_type} 2025</a><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Chic and fashionable designs, unconventional details and unique color combinations, high-quality materials and craftsmanship: </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are always the perfect choice.</span></p>
<p><span style="font-weight: 400;">Beautifully designed by Chlo&eacute; and perfectly crafted by French eyewear manufacturer Kering, the new </span><strong>{frame_color}</strong> <strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> are the ultimate designer eyeglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">. Get yours today and add a touch of sophistication to your style!&nbsp;</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new</span> <a href="/collections/chloe-eyeglasses">{brand} {product_type} 2025</a> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    chloe["Body HTML"] = chloe.apply(get_product_description, axis = 1)

    # chloe = chloe[[
    #     "Variant SKU", "Variant Barcode", "Variant Price", "Variant Compare At Price", "ID", "Handle", "Title",
    #     "Command", "Body HTML", "Vendor", "Type", "Tags", "Tags Command", "Status", "Template Suffix",
    #     "URL", "Total Inventory Qty", "Variant ID", "Option1 Name", "Option1 Value",
    #     "Inventory Available: +39 05649689443", "Metafield: title_tag [string]", "Metafield: description_tag [string]",
    #     "Metafield: my_fields.lens_color [single_line_text_field]", "Metafield: my_fields.frame_color [single_line_text_field]",
    #     "Metafield: my_fields.frame_shape [single_line_text_field]", "Metafield: my_fields.frame_material [single_line_text_field]",
    #     "Metafield: my_fields.lens_material [single_line_text_field]", "Metafield: my_fields.product_size [single_line_text_field]",
    #     "Metafield: my_fields.for_who [single_line_text_field]"
    # ]]

    chloe = chloe.drop_duplicates("Title")

    # SAVING INTO chloe FOLDER AND TO_IMPORT FOLDER
    chloe = chloe.sort_values(by="Title")
    chloe.to_excel(f"{chloe_folder}chloe_templates_ok.xlsx", index = False)
    chloe.to_excel(f"{templates}/chloe_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Starting Chloe templates updater")
        chloe_templates_updater()
        print("Chloe templates updated succesfully! \n Closing chloe templates.")
    except Exception as err:
        print(f"Chloe not updated due this error \n {type(err).__name__}: {err}")
