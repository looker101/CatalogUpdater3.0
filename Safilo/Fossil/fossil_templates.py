import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import fossil_folder, fossil_excel, templates


def fossil_templates_update():
    fossil_file = pd.read_excel(fossil_excel)

    fossil_file = fossil_file[[
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
        """fossil {model_code} {color_code} {color_frame} {type} for {gender}"""
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
    fossil_file["Metafield: title_tag [string]"] = fossil_file.apply(get_metatitle, axis = 1)

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
    fossil_file["Metafield: description_tag [string]"] = fossil_file.apply(get_meta_description, axis = 1)

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

        sun = f"""<p><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are an essential accessory for those who appreciate timeless design and superior quality. With a rich heritage steeped in American craftsmanship, Fossil has been producing exceptional eyewear for decades.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinctive </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model epitomizes Fossil's dedication to blending classic aesthetics with contemporary sensibilities. Meticulously crafted from premium materials and boasting intricate detailing, these sunglasses offer both durability and style.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Whether you're lounging by the pool or strolling through the city streets, the {model_code} {color_code} by Fossil will effortlessly enhance your ensemble with its refined charm. Explore the latest additions to the <a href="/collections/fossil-sunglasses" target="_blank">Fossil sunglasses 2025</a> collection and find the perfect pair to complement your individuality.</span></p>"""

        eye = f"""<p><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are a staple accessory for those who value timeless style and quality craftsmanship. With a heritage rooted in American innovation, Fossil has been crafting exceptional eyewear for decades.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model embodies Fossil's commitment to blending classic design with contemporary flair. Crafted from premium materials and featuring precise detailing, these eyeglasses offer both durability and sophistication.</span></p>
<p><br /><span style="font-weight: 400;">Whether you're at the office or out on the town, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Fossil is sure to elevate your look with its understated elegance. Explore the latest offerings from the new <a href="/collections/fossil-eyeglasses" target="_blank">{brand} {item_type} 2025</a> collection and discover the perfect pair to complement your style.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye
    fossil_file["Body HTML"] = fossil_file.apply(get_product_descript, axis = 1)

    # DROP ALL ROWS WHERE 'FOR WHO' IS EMPTY TO AVOID DUPLICATE
    fossil_file = fossil_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.for_who [single_line_text_field]'])
    
    fossil_file["Option1 Name"] = "Size"
    fossil_file["Variant SKU"] = fossil_file["Variant SKU"].astype(str)
    fossil_file["Option1 Value"] = fossil_file["Variant SKU"].str[-4:-2]

    # SORTING BY HANDLE
    fossil_file = fossil_file.sort_values(by="Handle")

    # SAVING
    fossil_file.to_excel(f"{fossil_folder}/fossil_templates_ok.xlsx", index = False)
    fossil_file.to_excel(f"{templates}/fossil_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Updating Fossil templates...")
        fossil_templates_update()
        print("Fossil templates updated successfully..")
    except Exception as err:
        print(f"An error occurred in the Fossil Templates Updater: \n {type(err).__name__}: {err}")


