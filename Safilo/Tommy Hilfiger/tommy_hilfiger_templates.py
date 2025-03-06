import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import tommy_hilfiger_folder, tommy_hilfiger_excel, templates


def tommy_hilfiger_templates_update():
    tommy_hilfiger_file = pd.read_excel(tommy_hilfiger_excel)

    tommy_hilfiger_file = tommy_hilfiger_file[[
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
        """tommy_hilfiger {model_code} {color_code} {color_frame} {type} for {gender}"""
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
    tommy_hilfiger_file["Metafield: title_tag [string]"] = tommy_hilfiger_file.apply(get_metatitle, axis = 1)

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
    tommy_hilfiger_file["Metafield: description_tag [string]"] = tommy_hilfiger_file.apply(get_meta_description, axis = 1)

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

        sun = f"""<p><span style="font-weight: 400;">Elevate your eyewear game with </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;">, where classic American style meets contemporary design. Crafted with attention to detail and a focus on quality, these shades are the epitome of timeless fashion.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This iconic </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model represents Tommy Hilfiger's commitment to combining sophistication with everyday wearability. Designed and produced in collaboration with Italian eyewear manufacturer Safilo, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> offers a blend of elegance and practicality, making it a versatile accessory for any occasion.</span></p>
<p><br /><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/tommy-hilfiger-sunglasses" target="_blank">{brand} {item_type} 2025 </a></span><span style="font-weight: 400;">collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;"><strong>{brand} {item_type}</strong> are the go-to choice for folks who want classic American style with a modern twist. These glasses are all about looking good while keeping it practical in your daily life.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This iconic </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model represents Tommy Hilfiger's commitment to combining sophistication with everyday wearability. Designed and produced in partnership with Italian eyewear manufacturer Safilo, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> offers a blend of elegance and practicality, making it a versatile accessory for any occasion.</span></p>
<p><br /><span style="font-weight: 400;">Check out all the latest models and designs in the new</span> <span style="font-weight: 400;"><a href="/collections/tommy-hilfiger-eyeglasses" target="_blank">{brand} {item_type}</a> 2025</span><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye
    tommy_hilfiger_file["Body HTML"] = tommy_hilfiger_file.apply(get_product_descript, axis = 1)

    # DROP ALL ROWS WHERE 'FOR WHO' IS EMPTY TO AVOID DUPLICATE
    tommy_hilfiger_file = tommy_hilfiger_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.for_who [single_line_text_field]'])
    
    tommy_hilfiger_file["Option1 Name"] = "Size"
    tommy_hilfiger_file["Variant SKU"] = tommy_hilfiger_file["Variant SKU"].astype(str)
    tommy_hilfiger_file["Option1 Value"] = tommy_hilfiger_file["Variant SKU"].str[-4:-2]

    # SORTING BY HANDLE
    tommy_hilfiger_file = tommy_hilfiger_file.sort_values(by="Handle")

    # SAVING
    tommy_hilfiger_file.to_excel(f"{tommy_hilfiger_folder}/tommy_hilfiger_templates_ok.xlsx", index = False)
    tommy_hilfiger_file.to_excel(f"{templates}/tommy_hilfiger_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Updating Tommy Hilfiger templates...")
        tommy_hilfiger_templates_update()
        print("Tommy Hilfiger templates updated successfully..")
    except Exception as err:
        print(f"An error occurred in the Marc Jacobs Templates Updater: \n {type(err).__name__}: {err}")


