import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import moschino_folder, moschino_excel, templates


def moschino_templates_update():
    moschino_file = pd.read_excel(moschino_excel)

    moschino_file = moschino_file[[
        "Variant ID", "Variant SKU", "Variant Barcode","Command",
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
        """moschino {model_code} {color_code} {color_frame} {type} for {gender}"""
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
    moschino_file["Metafield: title_tag [string]"] = moschino_file.apply(get_metatitle, axis = 1)

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
    moschino_file["Metafield: description_tag [string]"] = moschino_file.apply(get_meta_description, axis = 1)

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

        sun = f"""<p><span style="font-weight: 400;">Loved by trendsetters, </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> inject a playful charm into your daily wardrobe. The captivating </span><strong>{frame_color} {model_code} {color_code}</strong><span style="font-weight: 400;">, a true Moschino masterpiece meticulously crafted by top eyewear artisans, guarantees comfort and durability.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Meet the essential Moschino sunglass &ndash; an infusion of Moschino's signature coolness into your look. These shades effortlessly blend contemporary style with timeless aesthetics, ensuring a polished and sophisticated edge.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Discover the latest trends in the <a href="/collections/moschino-sunglasses" target="_blank">{brand} {item_type} 2025</a> collection for a glimpse into the newest models and designs that promise to enhance your style.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Loved by trendsetters, </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> inject a playful charm into your daily wardrobe. The captivating </span><strong>{frame_color} {model_code} {color_code}</strong><span style="font-weight: 400;">, a true Moschino masterpiece meticulously crafted by top eyewear artisans, guarantees comfort and durability.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Meet the essential Moschino sunglass &ndash; an infusion of Moschino's signature coolness into your look. These shades effortlessly blend contemporary style with timeless aesthetics, ensuring a polished and sophisticated edge.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Discover the latest trends in the <a href="/collections/moschino-eyeglasses" target="_blank">{brand} {item_type} 2025</a> collection for a glimpse into the newest models and designs that promise to enhance your style.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye
    moschino_file["Body HTML"] = moschino_file.apply(get_product_descript, axis = 1)

    # DROP ALL ROWS WHERE 'FOR WHO' IS EMPTY TO AVOID DUPLICATE
    moschino_file = moschino_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.for_who [single_line_text_field]'])
    
    moschino_file["Option1 Name"] = "Size"
    moschino_file["Variant SKU"] = moschino_file["Variant SKU"].astype(str)
    moschino_file["Option1 Value"] = moschino_file["Variant SKU"].str[-4:-2]

    # SORTING BY HANDLE
    moschino_file = moschino_file.sort_values(by="Handle")

    # SAVING
    moschino_file.to_excel(f"{moschino_folder}/moschino_templates_ok.xlsx", index = False)
    moschino_file.to_excel(f"{templates}/moschino_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Updating Moschino templates...")
        moschino_templates_update()
        print("Moschino templates updated successfully..")
    except Exception as err:
        print(f"An error occurred in the Moschino Templates Updater: \n {type(err).__name__}: {err}")


