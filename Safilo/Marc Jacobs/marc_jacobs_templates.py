import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import marc_jacobs_folder, marc_jacobs_excel, templates


def marc_jacobs_templates_update():
    marc_jacobs_file = pd.read_excel(marc_jacobs_excel)

    marc_jacobs_file = marc_jacobs_file[[
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
        """marc_jacobs {model_code} {color_code} {color_frame} {type} for {gender}"""
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
    marc_jacobs_file["Metafield: title_tag [string]"] = marc_jacobs_file.apply(get_metatitle, axis = 1)

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
    marc_jacobs_file["Metafield: description_tag [string]"] = marc_jacobs_file.apply(get_meta_description, axis = 1)

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

        sun = f"""<p><span style="font-weight: 400;">Creative, irreverent, unique: </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are perfect for those who love fashion and don't fear being different.</span></p>
<p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This super-stylish, one-of-a-kind,</span><strong> medium havana </strong><span style="font-weight: 400;">model is a thing of absolute beauty. Designed and manufactured by Marc Jacobs in collaboration with Italian producer Safilo, these eyeglasses are the ultimate show-stoppers.</span></p>
<p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><a href="/collections/marc-jacobs-sunglasses"><span style="font-weight: 400;">{brand} {item_type} 2025</span></a><span style="font-weight: 400;"> collection.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Creative, irreverent, unique: </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are perfect for those who love fashion and don't fear being different.</span></p>
<p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This super-stylish, one-of-a-kind,</span><strong> medium havana </strong><span style="font-weight: 400;">model is a thing of absolute beauty. Designed and manufactured by Marc Jacobs in collaboration with Italian producer Safilo, these eyeglasses are the ultimate show-stoppers.</span></p>
<p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><a href="/collections/marc-jacobs-eyeglasses"><span style="font-weight: 400;">{brand} {item_type} 2025</span></a><span style="font-weight: 400;"> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye
    marc_jacobs_file["Body HTML"] = marc_jacobs_file.apply(get_product_descript, axis = 1)

    # DROP ALL ROWS WHERE 'FOR WHO' IS EMPTY TO AVOID DUPLICATE
    marc_jacobs_file = marc_jacobs_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.for_who [single_line_text_field]'])
    
    marc_jacobs_file["Option1 Name"] = "Size"
    marc_jacobs_file["Variant SKU"] = marc_jacobs_file["Variant SKU"].astype(str)
    marc_jacobs_file["Option1 Value"] = marc_jacobs_file["Variant SKU"].str[-4:-2]

    # SORTING BY TITLE
    marc_jacobs_file = marc_jacobs_file.sort_values(by="Handle")

    # SAVING
    marc_jacobs_file.to_excel(f"{marc_jacobs_folder}/marc_jacobs_templates_ok.xlsx", index = False)
    marc_jacobs_file.to_excel(f"{templates}/marc_jacobs_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Updating Marc Jacbos templates...")
        marc_jacobs_templates_update()
        print("Marc Jacobs templates updated successfully..")
    except Exception as err:
        print(f"An error occurred in the Marc Jacobs Templates Updater: \n {type(err).__name__}: {err}")


