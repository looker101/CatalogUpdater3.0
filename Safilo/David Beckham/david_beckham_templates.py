import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import david_beckham_folder, david_beckham_excel, templates


def david_beckham_templates_update():
    david_beckham_file = pd.read_excel(david_beckham_excel)

    david_beckham_file = david_beckham_file[[
        "Variant ID", "Variant SKU", "Variant Barcode", "Command",
        "ID", "Handle", "Title", "Body HTML", "Vendor", "Type", "URL", "Tags", "Tags Command", "Template Suffix",
        "Metafield: title_tag [string]", "Metafield: description_tag [string]",
        "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]",
        "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]",
        "Metafield: my_fields.lens_technology [single_line_text_field]",
        "Metafield: my_fields.product_size [single_line_text_field]",
        "Metafield: my_fields.for_who [single_line_text_field]",
        "Metafield: custom.main_frame_shape [single_line_text_field]",
        "Metafield: custom.main_frame_material [single_line_text_field]",
        "Metafield: custom.main_frame_color [single_line_text_field]",
        "Metafield: custom.main_lens_color [single_line_text_field]",
        "Metafield: custom.main_lens_technology [single_line_text_field]",
        "Metafield: custom.main_size [single_line_text_field]"
    ]]

    # METATITLE
    def get_metatitle(row):
        """david_beckham {model_code} {color_code} {color_frame} {type} for {gender}"""
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

    david_beckham_file["Metafield: title_tag [string]"] = david_beckham_file.apply(get_metatitle, axis=1)

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

    david_beckham_file["Metafield: description_tag [string]"] = david_beckham_file.apply(get_meta_description, axis=1)

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

        sun = f"""<p><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> find their origin in the finest materials, the attention to details, and the utmost quality of Italian design.</span></p>
<p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This elegant, timeless,</span><strong> gold </strong><span style="font-weight: 400;">model is a true lesson in style. Designed and manufactured to perfection by Italian eyewear producer Safilo, these </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are as classy and refined as their name would suggest.</span></p>
<p><span style="font-weight: 400;">Check out hundreds of new models and designs in the new</span><a href="/collections/david-beckham-sunglasses" target="_blank"><span style="font-weight: 400;">{brand} {item_type} 2025</span></a><span style="font-weight: 400;"> collection.</span></p>"""

        eye = f"""<p><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> find their origin in the finest materials, the attention to details, and the utmost quality of Italian design.</span></p>
<p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This elegant, timeless,</span><strong> gold </strong><span style="font-weight: 400;">model is a true lesson in style. Designed and manufactured to perfection by Italian eyewear producer Safilo, these </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are as classy and refined as their name would suggest.</span></p>
<p><span style="font-weight: 400;">Check out hundreds of new models and designs in the new</span><a href="/collections/david-beckham-eyeglasses" target="_blank"><span style="font-weight: 400;">{brand} {item_type} 2025</span></a><span style="font-weight: 400;"> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    david_beckham_file["Body HTML"] = david_beckham_file.apply(get_product_descript, axis=1)

    # DROP ALL ROWS WHERE 'FOR WHO' IS EMPTY TO AVOID DUPLICATE
    david_beckham_file = david_beckham_file.dropna(axis=0, how='any',
                                                   subset=['Metafield: my_fields.for_who [single_line_text_field]'])

    # CREATING OPTION Name & Value
    david_beckham_file["Metafield: my_fields.product_size [single_line_text_field]"] = david_beckham_file[
        "Metafield: my_fields.product_size [single_line_text_field]"].str.replace(", ", "")

    david_beckham_file["Option1 Name"] = "Size"
    david_beckham_file["Variant SKU"] = david_beckham_file["Variant SKU"].astype(str)
    david_beckham_file["Option1 Value"] = david_beckham_file["Variant SKU"].str[-4:-2]


    # SORTING BY TITLE
    david_beckham_file = david_beckham_file.sort_values(by="Handle")

    # SAVING
    david_beckham_file.to_excel(f"{david_beckham_folder}/david_beckham_templates_ok.xlsx", index=False)
    david_beckham_file.to_excel(f"{templates}/david_beckham_templates_ok.xlsx", index=False)


if __name__ == "__main__":
    try:
        print("Updating David Beckham templates...")
        david_beckham_templates_update()
        print("David Beckham templates updated successfully..")
    except Exception as err:
        print(f"An error occurred in the David Beckham Templates Updater: \n {type(err).__name__}: {err}")
