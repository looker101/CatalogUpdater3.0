import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from kering_paths import balenciaga_folder, balenciaga_excel, balenciaga_for_temp, templates

def balenciaga_templates_updater():
    balenciaga = pd.read_excel(balenciaga_excel)

    balenciaga = balenciaga[[
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

    balenciaga["Metafield: title_tag [string]"] = balenciaga.apply(get_metatitle, axis = 1)

    def get_metadescription(row):
        title = row["Title"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]
        return f"Buy the new {title} {product_type} at a bargain price This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING"

    balenciaga["Metafield: description_tag [string]"] = balenciaga.apply(get_metadescription, axis = 1)

    def get_product_description(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"][1]
        color_code = row["Variant SKU"][2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        lens_color = row["Metafield: my_fields.lens_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">Clear lines and silhouettes, understated elegance, and meticulous attention to the finest details: </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are this and much more.</span></p>
<p><span style="font-weight: 400;">The new </span><strong>{frame_color}</strong> <strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> are the ultimate designer eyeglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">.</span><span style="font-weight: 400;"> Balenciaga pushes the boundaries of traditional fashion with oversized shapes, exaggerated proportions, and avant-garde designs that challenge conventions. The result is timeless eyewear that you will want to sport over and over.</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new</span> <a href="/collections/balenciaga-sunglasses" target="_blank"><span style="font-weight: 400;">{brand} {product_type} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Clear lines and silhouettes, understated elegance, and meticulous attention to the finest details: </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are this and much more.</span></p>
<p><span style="font-weight: 400;">The new </span><strong>{frame_color}</strong> <strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> are the ultimate designer eyeglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">.</span><span style="font-weight: 400;"> Balenciaga pushes the boundaries of traditional fashion with oversized shapes, exaggerated proportions, and avant-garde designs that challenge conventions. The result is timeless eyewear that you will want to sport over and over.</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new</span> <a href="/collections/balenciaga-eyeglasses" target="_blank"><span style="font-weight: 400;">{brand} {product_type} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    balenciaga["Body HTML"] = balenciaga.apply(get_product_description, axis = 1)

    # balenciaga = balenciaga[[
    #     "Variant SKU", "Variant Barcode", "Variant Price", "Variant Compare At Price", "ID", "Handle", "Title",
    #     "Command", "Body HTML", "Vendor", "Type", "Tags", "Tags Command", "Status", "Template Suffix",
    #     "URL", "Total Inventory Qty", "Variant ID", "Option1 Name", "Option1 Value",
    #     "Inventory Available: +39 05649689443", "Metafield: title_tag [string]", "Metafield: description_tag [string]",
    #     "Metafield: my_fields.lens_color [single_line_text_field]", "Metafield: my_fields.frame_color [single_line_text_field]",
    #     "Metafield: my_fields.frame_shape [single_line_text_field]", "Metafield: my_fields.frame_material [single_line_text_field]",
    #     "Metafield: my_fields.lens_material [single_line_text_field]", "Metafield: my_fields.product_size [single_line_text_field]",
    #     "Metafield: my_fields.for_who [single_line_text_field]"
    # ]]

    balenciaga = balenciaga.drop_duplicates("Title")

    # SAVING INTO balenciaga FOLDER AND TO_IMPORT FOLDER
    balenciaga = balenciaga.sort_values(by="Title")
    balenciaga.to_excel(f"{balenciaga_folder}balenciaga_templates_ok.xlsx", index = False)
    balenciaga.to_excel(f"{templates}/balenciaga_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Starting Balenciaga templates updater")
        balenciaga_templates_updater()
        print("Balenciaga templates updated succesfully! \n Closing balenciaga templates.")
    except Exception as err:
        print(f"Balenciaga not updated due this error \n {type(err).__name__}: {err}")
