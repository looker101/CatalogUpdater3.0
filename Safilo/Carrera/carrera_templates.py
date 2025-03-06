import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from safilo_paths import carrera_folder, carrera_excel, templates


def carrera_templates_update():
    carrera_file = pd.read_excel(carrera_excel)

    carrera_file["Variant SKU"] = carrera_file["Variant SKU"].astype(str)

    carrera_file = carrera_file[[
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
        """Carrera {model_code} {color_code} {color_frame} {type} for {gender}"""
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

    carrera_file["Metafield: title_tag [string]"] = carrera_file.apply(get_metatitle, axis=1)

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

    carrera_file["Metafield: description_tag [string]"] = carrera_file.apply(get_meta_description, axis=1)

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

        sun = f"""<p><span style="font-weight: 400;">From rock stars to racing fans and celebrities, </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are revered by people who live life by their own standards.</span></p>
    <p><span style="font-weight: 400;">This one-of-a-kind, bold, flawless </span><strong>black white</strong><span style="font-weight: 400;"> model was designed and manufactured by Carrera in collaboration with Italian producer Safilo. An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the </span><strong>Carrera {model_code} {color_code}</strong><span style="font-weight: 400;"> are the ultimate expression of superior quality design and high-performance eyewear technology.</span></p>
    <p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><a href="/collections/carrera-sunglasses" target ="_blank"><span style="font-weight: 400;">{brand} {item_type} 2025</span></a> <span style="font-weight: 400;">collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">From rock stars to racing fans and celebrities, </span><strong>{brand} {item_type}</strong><span style="font-weight: 400;"> are revered by people who live life by their own standards.</span></p>
    <p><span style="font-weight: 400;">This one-of-a-kind, bold, flawless </span><strong>black white</strong><span style="font-weight: 400;"> model was designed and manufactured by Carrera in collaboration with Italian producer Safilo. An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the </span><strong>Carrera {model_code} {color_code}</strong><span style="font-weight: 400;"> are the ultimate expression of superior quality design and high-performance eyewear technology.</span></p>
    <p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><a href="/collections/carrera-eyeglasses" target ="_blank"><span style="font-weight: 400;">{brand} {item_type} 2025</span></a> <span style="font-weight: 400;">collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    carrera_file["Body HTML"] = carrera_file.apply(get_product_descript, axis=1)

    # DROP ALL ROWS WHERE 'FOR WHO' IS EMPTY TO AVOID DUPLICATE
    carrera_file = carrera_file.dropna(axis=0, how='any',
                                       subset=['Metafield: my_fields.for_who [single_line_text_field]'])

    # CREATING OPTION Name & Value
    carrera_file["Option1 Name"] = "Size"
    carrera_file["Metafield: my_fields.product_size [single_line_text_field]"] = carrera_file[
        "Metafield: my_fields.product_size [single_line_text_field]"].astype(str)

    carrera_file["Option1 Value"] = carrera_file["Variant SKU"].str[-4:-2]

    # SORTING BY HANDLE
    carrera_file = carrera_file.sort_values(by="Title")

    # SAVING
    carrera_file.to_excel(f"{carrera_folder}/carrera_templates_ok.xlsx", index=False)
    carrera_file.to_excel(f"{templates}/carrera_templates_ok.xlsx", index=False)


if __name__ == "__main__":
    try:
        print("Updating Carrera templates...")
        carrera_templates_update()
        print("Carrera templates updated successfully..")
    except Exception as err:
        print(f"An error occurred in the Carrera Templates Updater: \n {type(err).__name__}: {err}")
