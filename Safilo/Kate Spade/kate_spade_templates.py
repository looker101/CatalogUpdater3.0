import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import kate_spade_folder, kate_spade_excel, templates


def kate_spade_templates_update():
    kate_spade_file = pd.read_excel(kate_spade_excel)

    kate_spade_file = kate_spade_file[[
        "Variant ID", "Variant SKU", "Variant Barcode", "Command",
        "ID", "Handle", "Title", "Body HTML", "Vendor", "Type", "URL", "Tags", "Tags Command", "Template Suffix",
        "Metafield: title_tag [string]", "Metafield: description_tag [string]", "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]", "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]", "Metafield: my_fields.lens_technology [single_line_text_field]",
        "Metafield: my_fields.product_size [single_line_text_field]", "Metafield: my_fields.for_who [single_line_text_field]",
        "Metafield: custom.main_frame_shape [single_line_text_field]",
        "Metafield: custom.main_frame_material [single_line_text_field]",
        "Metafield: custom.main_frame_color [single_line_text_field]",
        "Metafield: custom.main_lens_color [single_line_text_field]",
        "Metafield: custom.main_lens_technology [single_line_text_field]",
        "Metafield: custom.main_size [single_line_text_field]"
    ]]

    # METATITLE
    def get_metatitle(row):
        """kate_spade {model_code} {color_code} {color_frame} {type} for {gender}"""
        item_title = row["Title"]
        if pd.notna(row["Metafield: my_fields.frame_color [single_line_text_field]"]):
            frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        else:
            frame_color = ''
        item_type = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        return f"{item_title} {frame_color} {item_type} for {gender} | LookerOnline"
    kate_spade_file["Metafield: title_tag [string]"] = kate_spade_file.apply(get_metatitle, axis = 1)

    # META DESCRIPTION
    def get_meta_description(row):
        item_title = row["Title"]
        if pd.notna(row["Metafield: my_fields.frame_color [single_line_text_field]"]):
            frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        else:
            frame_color = ''
        item_type = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        return f"New {item_title} {frame_color} {item_type} for {gender} on sale! ✓ Express Shipping ✓ 100% Original and Authentic | LookerOnline"
    kate_spade_file["Metafield: description_tag [string]"] = kate_spade_file.apply(get_meta_description, axis = 1)

    # PRODUCT DESCRIPTION
    def get_product_descript(row):
        brand = row["Vendor"]
        model_code = row["Title"][2]
        color_code = row["Title"][3]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        lens_color = row["Metafield: my_fields.lens_color [single_line_text_field]"]
        item_type = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        sun = f"""<p><span style="font-weight: 400;">Elevate your style with the timeless charm of </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;">. Loved by fashion enthusiasts and trendsetters alike, these shades exude sophistication and elegance. Designed by the creative minds behind Kate Spade New York, these sunglasses are a perfect blend of fashion and function.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This exceptional </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model was meticulously crafted in collaboration with renowned eyewear manufacturer Safilo, ensuring the highest quality and attention to detail. A must-have accessory for anyone seeking a boost in style, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> will effortlessly enhance your everyday look with a touch of class.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/kate-spade-sunglasses" target="_blank">{brand} {item_type} 2025</a> collection.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Elevate your style with the timeless charm of </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;">. Loved by fashion enthusiasts and trendsetters alike, these shades exude sophistication and elegance. Designed by the creative minds behind Kate Spade New York, these {item_type.lower()} are a perfect blend of fashion and function.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This exceptional </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model was meticulously crafted in collaboration with renowned eyewear manufacturer Safilo, ensuring the highest quality and attention to detail. A must-have accessory for anyone seeking a boost in style, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> will effortlessly enhance your everyday look with a touch of class.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/kate-spade-eyeglasses" target="_blank" rel="noopener">{brand} {item_type} 2025</a> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye
    kate_spade_file["Body HTML"] = kate_spade_file.apply(get_product_descript, axis = 1)

    # DROP ALL ROWS WHERE 'FOR WHO' IS EMPTY TO AVOID DUPLICATE
    kate_spade_file = kate_spade_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.for_who [single_line_text_field]'])
    
    kate_spade_file["Option1 Name"] = "Size"
    kate_spade_file["Variant SKU"] = kate_spade_file["Variant SKU"].astype(str)
    kate_spade_file["Option1 Value"] = kate_spade_file["Variant SKU"].str[-4:-2]

    # SORTING BY HANDLE
    kate_spade_file = kate_spade_file.sort_values(by="Handle")

    # SAVING
    kate_spade_file.to_excel(f"{kate_spade_folder}/kate_spade_templates_ok.xlsx", index = False)
    kate_spade_file.to_excel(f"{templates}/kate_spade_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Updating Kate Spade templates...")
        kate_spade_templates_update()
        print("Kate Spade templates updated successfully..")
    except Exception as err:
        print(f"An error occurred in the Kate Spade Templates Updater: \n {type(err).__name__}: {err}")


