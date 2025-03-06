import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from kering_paths import sl_folder, sl_excel, sl_for_temp, templates

def sl_templates_updater():
    sl = pd.read_excel(sl_excel)

    sl = sl[[
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

    sl["Metafield: title_tag [string]"] = sl.apply(get_metatitle, axis = 1)

    def get_metadescription(row):
        title = row["Title"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]
        return f"""Buy the new {title} {product_type} at a bargain price This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING"""

    sl["Metafield: description_tag [string]"] = sl.apply(get_metadescription, axis = 1)

    def get_product_description(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"][1]
        color_code = row["Variant SKU"][2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        lens_color = row["Metafield: my_fields.lens_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">Bold designs, high-quality materials, and fine detailing: </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are a unique blend of timeless class, fashion-forward style, and sophistication.</span></p>
<p><span style="font-weight: 400;">Beautifully designed by YSL&rsquo;s best designers and perfectly crafted by world-renowned French eyewear manufacturer Kering, the new </span><strong>{frame_color}</strong> <strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> with </span><strong>{lens_color}</strong><span style="font-weight: 400;"> lenses are the ultimate sunglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">. Get yours today and take your eyewear game to the next level!</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/saint-laurent-sunglasses">{brand} {product_type} 2025</a> <span style="font-weight: 400;">collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Bold designs, high-quality materials, and fine detailing: </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are a unique blend of timeless class, fashion-forward style, and sophistication.</span></p>
<p><span style="font-weight: 400;">Beautifully designed by YSL&rsquo;s best designers and perfectly crafted by world-renowned French eyewear manufacturer Kering, the new </span><strong>{frame_color}</strong> <strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> are the ultimate eyeglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">. Get yours today and take your eyewear game to the next level!</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/saint-laurent-sunglasses">{brand} {product_type} 2025</a> <span style="font-weight: 400;">collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    sl["Body HTML"] = sl.apply(get_product_description, axis = 1)

    # sl = sl[[
    #     "Variant SKU", "Variant Barcode", "Variant Price", "Variant Compare At Price", "ID", "Handle", "Title",
    #     "Command", "Body HTML", "Vendor", "Type", "Tags", "Tags Command", "Status", "Template Suffix",
    #     "URL", "Total Inventory Qty", "Variant ID", "Option1 Name", "Option1 Value",
    #     "Inventory Available: +39 05649689443", "Metafield: title_tag [string]", "Metafield: description_tag [string]",
    #     "Metafield: my_fields.lens_color [single_line_text_field]", "Metafield: my_fields.frame_color [single_line_text_field]",
    #     "Metafield: my_fields.frame_shape [single_line_text_field]", "Metafield: my_fields.frame_material [single_line_text_field]",
    #     "Metafield: my_fields.lens_material [single_line_text_field]", "Metafield: my_fields.product_size [single_line_text_field]",
    #     "Metafield: my_fields.for_who [single_line_text_field]"
    # ]]

    sl = sl.drop_duplicates("Title")

    # SAVING INTO sl FOLDER AND TO_IMPORT FOLDER
    sl = sl.sort_values(by="Title")
    sl.to_excel(f"{sl_folder}sl_templates_ok.xlsx", index = False)
    sl.to_excel(f"{templates}/sl_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Starting Saint Laurent templates updater")
        sl_templates_updater()
        print("Saint Laurent templates updated succesfully! \n Closing sl templates.")
    except Exception as err:
        print(f"Saint Laurent not updated due this error \n {type(err).__name__}: {err}")
