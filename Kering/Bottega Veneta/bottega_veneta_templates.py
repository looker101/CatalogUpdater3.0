import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from kering_paths import bottega_veneta_folder, bottega_veneta_excel, bv_for_temp, templates

def bottega_veneta_templates_updater():
    bottega_veneta = pd.read_excel(bottega_veneta_excel)

    bottega_veneta = bottega_veneta[[
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

    bottega_veneta["Metafield: title_tag [string]"] = bottega_veneta.apply(get_metatitle, axis = 1)

    def get_metadescription(row):
        title = row["Title"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]
        return f"""Buy the new {title} {product_type} at a bargain price This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING"""

    bottega_veneta["Metafield: description_tag [string]"] = bottega_veneta.apply(get_metadescription, axis = 1)

    def get_product_description(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"][1]
        color_code = row["Variant SKU"][2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        lens_color = row["Metafield: my_fields.lens_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">Discover </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;">' timeless elegance and understated luxury. These glasses feature sleek and tasteful frames made of high-quality materials for a uniquely versatile unisex appeal and a super comfortable fit.</span></p>
<p><span style="font-weight: 400;">Beautifully designed by Bottega Veneta&rsquo;s best designers and crafted to perfection by world-renowned French eyewear manufacturer Kering, the new </span><strong>{frame_color}</strong> <strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> are the ultimate eyeglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">. Get yours today and take your eyewear game to the next level!&nbsp;</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/bottega-veneta-eyeglasses">{brand} {product_type} 2025</a> <span style="font-weight: 400;">collection.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Discover </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;">' timeless elegance and understated luxury. These glasses feature sleek and tasteful frames made of high-quality materials for a uniquely versatile unisex appeal and a super comfortable fit.</span></p>
<p><span style="font-weight: 400;">Beautifully designed by Bottega Veneta&rsquo;s best designers and crafted to perfection by world-renowned French eyewear manufacturer Kering, the new </span><strong>{frame_color}</strong> <strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> are the ultimate eyeglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">. Get yours today and take your eyewear game to the next level!&nbsp;</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/bottega-veneta-eyeglasses">{brand} {product_type} 2025</a> <span style="font-weight: 400;">collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    bottega_veneta["Body HTML"] = bottega_veneta.apply(get_product_description, axis = 1)

    # bottega_veneta = bottega_veneta[[
    #     "Variant SKU", "Variant Barcode", "Variant Price", "Variant Compare At Price", "ID", "Handle", "Title",
    #     "Command", "Body HTML", "Vendor", "Type", "Tags", "Tags Command", "Status", "Template Suffix",
    #     "URL", "Total Inventory Qty", "Variant ID", "Option1 Name", "Option1 Value",
    #     "Inventory Available: +39 05649689443", "Metafield: title_tag [string]", "Metafield: description_tag [string]",
    #     "Metafield: my_fields.lens_color [single_line_text_field]", "Metafield: my_fields.frame_color [single_line_text_field]",
    #     "Metafield: my_fields.frame_shape [single_line_text_field]", "Metafield: my_fields.frame_material [single_line_text_field]",
    #     "Metafield: my_fields.lens_material [single_line_text_field]", "Metafield: my_fields.product_size [single_line_text_field]",
    #     "Metafield: my_fields.for_who [single_line_text_field]"
    # ]]

    bottega_veneta = bottega_veneta.drop_duplicates("Title")

    # SAVING INTO bottega_veneta FOLDER AND TO_IMPORT FOLDER
    bottega_veneta = bottega_veneta.sort_values(by="Title")
    bottega_veneta.to_excel(f"{bottega_veneta_folder}bottega_veneta_templates_ok.xlsx", index = False)
    bottega_veneta.to_excel(f"{templates}/bottega_veneta_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Starting Bottega Veneta templates updater")
        bottega_veneta_templates_updater()
        print("Bottega Veneta templates updated succesfully! \n Closing bottega_veneta templates.")
    except Exception as err:
        print(f"Bottega Veneta not updated due this error \n {type(err).__name__}: {err}")
