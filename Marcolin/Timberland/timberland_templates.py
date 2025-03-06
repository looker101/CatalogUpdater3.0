import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import timberland_excel, timberland_folder, templates

def timberland_templates_update():

    timberland = pd.read_excel(timberland_excel)

    timberland = timberland[[
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
        #{Brand} {model_code} {color_code} {product_type} for {gender} | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Man and Woman"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        return f"{brand} {model_code} {color_code} {product_type} for {gender} | LookerOnline"

    def metaDescript(row):
        #New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express World Wide Shipping ✓ 100% Original | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"].lower()
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        return f"New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express World Wide Shipping ✓ 100% Original | LookerOnline"

    def productDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]

        sun = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> build on the brand's legendary heritage of classic comfort and superior wearability to bring you light and sustainable materials, timeless design and outstanding finishes.</span></p>
                <p><span style="font-weight: 400;">The </span><strong>{brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This affordable, stylish,</span><strong> {frame_color} </strong><span style="font-weight: 400;">model was carefully designed and manufactured by Italian producer Marcolin to meet </span><strong>Timberland</strong><span style="font-weight: 400;">'s top-quality standards.</span></p>
                <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/timberland-sunglasses" target = "_blank"><span style="font-weight: 400;">{brand} {product_type}</span></a><span style="font-weight: 400;"> 2025 collection.</span></p>"""

        eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> build on the brand's legendary heritage of classic comfort and superior wearability to bring you light and sustainable materials, timeless design and outstanding finishes.</span></p>
                <p><span style="font-weight: 400;">The </span><strong>{brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This affordable, stylish,</span><strong> {frame_color} </strong><span style="font-weight: 400;">model was carefully designed and manufactured by Italian producer Marcolin to meet </span><strong>Timberland</strong><span style="font-weight: 400;">'s top-quality standards.</span></p>
                <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><a href="/collections/timberland-eyeglasses" target = "_blank"><span style="font-weight: 400;">{brand} {product_type}</span></a><span style="font-weight: 400;"> 2025 collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye


    timberland["Metafield: title_tag [string]"] = timberland.apply(metaTitle, axis = 1)
    timberland["Metafield: description_tag [string]"] = timberland.apply(metaDescript, axis = 1)
    timberland["Body HTML"] = timberland.apply(productDescription, axis=1)


    # REMOVE ALL DUPLICATES BY HANDLE
    timberland = timberland.drop_duplicates("Title")

    timberland = timberland.sort_values(by="Title")
    timberland.to_excel(f"{timberland_folder}Timberland_templates_ok.xlsx", index=False)
    timberland.to_excel(f"{templates}/timberland_templates_ok.xlsx", index=False)

if __name__ == "__main__":
    try:
        print("Timberland templates updating...")
        timberland_templates_update()
        print("Timberland templates updated successfully into directory!")
    except Exception as err:
        print(f"{type(err).__name__}: {err}")