import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import polaroid_folder, polaroid_excel, templates


def polaroid_templates_update():
    polaroid_file = pd.read_excel(polaroid_excel)

    polaroid_file = polaroid_file[[
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
        """polaroid {model_code} {color_code} {color_frame} {type} for {gender}"""
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
    polaroid_file["Metafield: title_tag [string]"] = polaroid_file.apply(get_metatitle, axis = 1)

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
    polaroid_file["Metafield: description_tag [string]"] = polaroid_file.apply(get_meta_description, axis = 1)

    # PRODUCT DESCRIPTION
    def get_product_descript(row):
        brand = row["Vendor"]
        model_code = row["Title"][1]
        color_code = row["Title"][2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        lens_color = row["Metafield: my_fields.lens_color [single_line_text_field]"]
        item_type = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        sun = f"""<p><span style="font-weight: 400;">Light, comfortable and easy to wear, </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are ideal for people who are easy-going and relaxed, love the simple life, and care for their eyes.</span></p>
<p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is the perfect choice for</span><strong> men</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This stylish, unique,</span><strong> {frame_color} </strong><span style="font-weight: 400;">model was designed and manufactured by Polaroid in collaboration with Italian producer Safilo to bring you the ultimate lifestyle eyewear.</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/polaroid-sunglasses"><span style="font-weight: 400;">{brand} {item_type} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Light, comfortable and easy to wear, </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are ideal for people who are easy-going and relaxed, love the simple life, and care for their eyes.</span></p>
<p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is the perfect choice for</span><strong> men</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This stylish, unique,</span><strong> {frame_color} </strong><span style="font-weight: 400;">model was designed and manufactured by Polaroid in collaboration with Italian producer Safilo to bring you the ultimate lifestyle eyewear.</span></p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/polaroid-eyeglasses"><span style="font-weight: 400;">{brand} {item_type} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye
    polaroid_file["Body HTML"] = polaroid_file.apply(get_product_descript, axis = 1)

    # DROP ALL ROWS WHERE 'FOR WHO' IS EMPTY TO AVOID DUPLICATE
    polaroid_file = polaroid_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.for_who [single_line_text_field]'])
    
    polaroid_file["Option1 Name"] = "Size"
    polaroid_file["Variant SKU"] = polaroid_file["Variant SKU"].astype(str)
    polaroid_file["Option1 Value"] = polaroid_file["Variant SKU"].str[-4:-2]

    # SORTING BY HANDLE
    polaroid_file = polaroid_file.sort_values(by="Handle")

    # SAVING
    polaroid_file.to_excel(f"{polaroid_folder}/polaroid_templates_ok.xlsx", index = False)
    polaroid_file.to_excel(f"{templates}/polaroid_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Updating polaroid templates...")
        polaroid_templates_update()
        print("polaroid templates updated successfully..")
    except Exception as err:
        print(f"An error occurred in the polaroid Templates Updater: \n {type(err).__name__}: {err}")


