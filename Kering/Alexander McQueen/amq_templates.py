import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from kering_paths import amq_for_temp, amq_excel, amq_folder, templates

def amq_templates_updater():
    amq = pd.read_excel(amq_excel)
    
    amq = amq[[
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

    amq["Metafield: title_tag [string]"] = amq.apply(get_metatitle, axis = 1)

    def get_metadescription(row):
        title = row["Title"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]
        return f"Buy the new {title} {product_type} at a bargain price This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING"

    amq["Metafield: description_tag [string]"] = amq.apply(get_metadescription, axis = 1)

    def get_product_description(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"][1]
        color_code = row["Variant SKU"][2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        lens_color = row["Metafield: my_fields.lens_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]

        sun = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> express the innovative and uncompromising identity of the fashion house. Integral to the McQueen culture, the eyewear styles represent a juxtaposition between contrasting elements: femininity and masculinity, fragility and strength, tradition and modernity.</span></p>
    <p><span style="font-weight: 400;">The new </span><strong>{frame_color}</strong> <strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> with </span><strong>{lens_color}</strong><span style="font-weight: 400;"> lenses are the ultimate designer sunglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">.</span><span style="font-weight: 400;"> Alexander McQueen pushes the boundaries with avant-garde designs that challenge conventions. The result is timeless sunglasses that you will never want to stop wearing.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new</span> <a href="/collections/alexander-mcqueen-sunglasses" target="_blank">{brand} {product_type} 2025</a><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""{brand} {product_type} express the innovative and uncompromising identity of the fashion house. Integral to the McQueen culture, the eyewear styles represent a juxtaposition between contrasting elements: femininity and masculinity, fragility and strength, tradition and modernity.
    The new {frame_color} {model_code} {color_code} are the ultimate designer eyeglasses for {gender}. Alexander McQueen pushes the boundaries with avant-garde designs that challenge conventions. The result is timeless eyeglasses that you will never want to stop wearing.
    Check out all the latest models and designs in the new <a href="/collections/alexander-mcqueen-eyeglasses" target="_blank">{brand} {product_type}</a> 2025 collection!"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    amq["Body HTML"] = amq.apply(get_product_description, axis = 1)

    # amq = amq[[
    #     "Variant SKU", "Variant Barcode", "Variant Price", "Variant Compare At Price", "ID", "Handle", "Title",
    #     "Command", "Body HTML", "Vendor", "Type", "Tags", "Tags Command", "Status", "Template Suffix",
    #     "URL", "Total Inventory Qty", "Variant ID", "Option1 Name", "Option1 Value",
    #     "Inventory Available: +39 05649689443", "Metafield: title_tag [string]", "Metafield: description_tag [string]",
    #     "Metafield: my_fields.lens_color [single_line_text_field]", "Metafield: my_fields.frame_color [single_line_text_field]",
    #     "Metafield: my_fields.frame_shape [single_line_text_field]", "Metafield: my_fields.frame_material [single_line_text_field]",
    #     "Metafield: my_fields.lens_material [single_line_text_field]", "Metafield: my_fields.product_size [single_line_text_field]",
    #     "Metafield: my_fields.for_who [single_line_text_field]"
    # ]]

    amq = amq.drop_duplicates("Title")

    # SAVING INTO AMQ FOLDER AND TO_IMPORT FOLDER
    amq = amq.sort_values(by="Title")
    amq.to_excel(f"{amq_folder}Amq_templates_ok.xlsx", index = False)
    amq.to_excel(f"{templates}/Amq_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Starting Alexander McQueen templates updater")
        amq_templates_updater()
        print("Alexander McQueen templates updated succesfully! \n Closing AMQ templates.")
    except Exception as err:
        print(f"Alexander McQueen not updated due this error \n {type(err).__name__}: {err}")
