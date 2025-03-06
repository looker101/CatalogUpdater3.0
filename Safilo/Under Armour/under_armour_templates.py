import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import under_armour_folder, under_armour_excel, templates


def under_armour_templates_update():
    under_armour_file = pd.read_excel(under_armour_excel)

    under_armour_file = under_armour_file[[
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
        """under_armour {model_code} {color_code} {color_frame} {type} for {gender}"""
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
    under_armour_file["Metafield: title_tag [string]"] = under_armour_file.apply(get_metatitle, axis = 1)

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
    under_armour_file["Metafield: description_tag [string]"] = under_armour_file.apply(get_meta_description, axis = 1)

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

        sun = f"""<p><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> embody the brand's ethos of performance and innovation, catering to the needs of athletes and outdoor enthusiasts alike. The </span><strong>{frame_color}</strong><span style="font-weight: 400;"> design exemplifies Under Armour's dedication to merging cutting-edge technology with stylish aesthetics.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Crafted from premium materials, these sunglasses are engineered for durability, providing optimum comfort and protection in any environment. From intense workouts to outdoor adventures, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> sunglasses by Under Armour are designed to enhance your performance while keeping you looking sharp.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Explore the latest offerings from the new <a href="/collections/under-armour-sunglasses" target="_blank">{brand} {item_type} 2025</a> collection and discover the perfect pair to elevate your active lifestyle.</span></p>"""

        eye = f"""<p><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are a testament to the brand's dedication to performance and innovation. With a legacy built on enhancing athletic performance, Under Armour has seamlessly transitioned into crafting high-quality eyewear for the modern athlete.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This cutting-edge </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model embodies Under Armour's commitment to merging advanced technology with sleek design. Constructed from premium materials and engineered for optimal comfort and durability, these eyeglasses deliver both style and functionality.</span></p>
<p><br /><span style="font-weight: 400;">Whether you're hitting the gym or navigating a busy day, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Under Armour ensures you'll perform at your best with its fusion of style and performance. Explore the latest additions to the <a href="/collections/under-armour-eyeglasses" target = "_blank">{brand} {item_type} 2025</a> collection and find the ideal pair to elevate your active lifestyle.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye
    under_armour_file["Body HTML"] = under_armour_file.apply(get_product_descript, axis = 1)

    # DROP ALL ROWS WHERE 'FOR WHO' IS EMPTY TO AVOID DUPLICATE
    under_armour_file = under_armour_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.for_who [single_line_text_field]'])
    
    under_armour_file["Option1 Name"] = "Size"
    under_armour_file["Variant SKU"] = under_armour_file["Variant SKU"].astype(str)
    under_armour_file["Option1 Value"] = under_armour_file["Variant SKU"].str[-4:-2]

    # SORTING BY HANDLE
    under_armour_file = under_armour_file.sort_values(by="Handle")

    # SAVING
    under_armour_file.to_excel(f"{under_armour_folder}/under_armour_templates_ok.xlsx", index = False)
    under_armour_file.to_excel(f"{templates}/under_armour_templates_ok.xlsx", index = False)

if __name__ == "__main__":
    try:
        print("Updating Under Armour templates...")
        under_armour_templates_update()
        print("Under Armour templates updated successfully..")
    except Exception as err:
        print(f"An error occurred in the Marc Jacobs Templates Updater: \n {type(err).__name__}: {err}")


