import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import tom_ford_excel, tom_ford_folder, templates


def tom_ford_templates_updater():
    tom_ford = pd.read_excel(tom_ford_excel)
    
    tom_ford = tom_ford[[
        "Variant ID", "Variant SKU", "Variant Barcode",
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

    def metaTitle(row):
        # {Brand} {model_code} {color_code} {product_type} for {gender} | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Man and Woman"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        return f"{brand} {model_code} {color_code} {product_type} for {gender} | LookerOnline"

    tom_ford["Metafield: title_tag [string]"] = tom_ford.apply(metaTitle, axis=1)

    def metaDescript(row):
        # New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express WorldWide Shipping ✓ 100% Original | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"].lower()
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        return f"New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express World Wide Shipping ✓ 100% Original | LookerOnline"

    tom_ford["Metafield: description_tag [string]"] = tom_ford.apply(metaDescript, axis=1)

    def productDescription(row):
        brand = row["Vendor"]
        # product_name = row["Title"].split()[2]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]

        sun = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are the ultimate fashion accessory. Stunningly beautiful, innovative yet essentially classic, flawless, imaginative, unique.</span></p>
                  <p><span style="font-weight: 400;">This super-stylish, one-of-a-kind,</span> coloured <strong> {frame_color} </strong><span style="font-weight: 400;">model was designed and manufactured to perfection by </span><strong>Tom Ford</strong><span style="font-weight: 400;"> in partnership with Italian producer </span><strong>Marcolin</strong><span style="font-weight: 400;">. An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">are a thing of absolute beauty and timeless elegance.</span></p>
                  <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/tom-ford-sunglasses"><span style="font-weight: 400;">{brand} {product_type} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are the ultimate fashion accessory. Stunningly beautiful, innovative yet essentially classic, flawless, imaginative, unique.</span></p>
                  <p><span style="font-weight: 400;">This super-stylish, one-of-a-kind,</span> coloured <strong> {frame_color} </strong><span style="font-weight: 400;">model was designed and manufactured to perfection by </span><strong>Tom Ford</strong><span style="font-weight: 400;"> in partnership with Italian producer </span><strong>Marcolin</strong><span style="font-weight: 400;">. 
                  An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the</span><strong> {brand} {model_code} {color_code} {frame_color} </strong><span style="font-weight: 400;">are a thing of absolute beauty and timeless elegance.</span></p>
                  <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/tom-ford-eyeglasses"><span style="font-weight: 400;">{brand} {product_type} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    tom_ford["Body HTML"] = tom_ford.apply(productDescription, axis=1)

    # REMOVE ALL DUPLICATES BY HANDLE
    tom_ford = tom_ford.drop_duplicates("Title")

    tom_ford = tom_ford.sort_values(by="Title")
    tom_ford.to_excel(f"{tom_ford_folder}Tom_Ford_Templates_updated.xlsx", index=False)
    tom_ford.to_excel(
        f"{templates}/tom_ford_templates_ok.xlsx",
        index=False)


if __name__ == "__main__":
    try:
        print("Tom Ford templates updating...")
        tom_ford_templates_updater()
        print("Tom Ford templates updated successfully into directory!")
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
