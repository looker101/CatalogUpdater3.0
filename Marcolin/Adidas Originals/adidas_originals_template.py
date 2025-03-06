import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import adidas_originals_excel, adidas_originals_folder, templates


def adidas_originals_templates_updater():
    adidas_originals = pd.read_excel(adidas_originals_excel)

    adidas_originals = adidas_originals[[
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

    adidas_originals["Metafield: title_tag [string]"] = adidas_originals.apply(metaTitle, axis=1)

    def metaDescript(row):
        # New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express WorldWide Shipping ✓ 100% Original | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"].lower()
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        return f"New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express World Wide Shipping ✓ 100% Original | LookerOnline"

    adidas_originals["Metafield: description_tag [string]"] = adidas_originals.apply(metaDescript, axis=1)

    def productDescription(row):
        brand = row["Vendor"]
        # product_name = row["Title"].split()[2]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]

        sun = f"""<p><span style="font-weight: 400;">Simple, young, sporty and super-comfortable,</span><strong> Adidas Originals {product_type.lower()}</strong><span style="font-weight: 400;"> will take your game to the next level without compromising on quality and style.</span></p>
<p><span style="font-weight: 400;">The</span><strong> Adidas Originals {model_code} {color_code} </strong><span style="font-weight: 400;">is the perfect choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This stylish and sporty </span><strong>{frame_color} </strong><span style="font-weight: 400;">model was designed and manufactured by Italian producer Marcolin to meet Adidas top-quality standards.</span></p>
<p><span style="font-weight: 400;">Check out hundreds of new models and designs in the new </span><a href="/collections/adidas-originals-eyeglasses" target="blank"><span style="font-weight: 400;">Adidas Originals {product_type.lower()} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Simple, young, sporty and super-comfortable,</span><strong> Adidas Originals {product_type.lower()}</strong><span style="font-weight: 400;"> will take your game to the next level without compromising on quality and style.</span></p>
<p><span style="font-weight: 400;">The</span><strong> Adidas Originals {model_code} {color_code} </strong><span style="font-weight: 400;">is the perfect choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This stylish and sporty </span><strong>{frame_color} </strong><span style="font-weight: 400;">model was designed and manufactured by Italian producer Marcolin to meet Adidas top-quality standards.</span></p>
<p><span style="font-weight: 400;">Check out hundreds of new models and designs in the new </span><a href="/collections/adidas-originals-eyeglasses" target="blank"><span style="font-weight: 400;">Adidas Originals {product_type.lower()} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    adidas_originals["Body HTML"] = adidas_originals.apply(productDescription, axis=1)


    # REMOVE ALL DUPLICATES BY HANDLE
    #adidas_originals = adidas_originals.drop_duplicates("Title")


    adidas_originals = adidas_originals.sort_values(by="Title")
    adidas_originals.to_excel(f"{adidas_originals_folder}adidas_originals_Templates_updated.xlsx", index=False)
    adidas_originals.to_excel(f"{templates}/adidas_originals_templates_ok.xlsx",
                              index = False)


if __name__ == "__main__":
    try:
        print("Adidas Originals templates updating...")
        adidas_originals_templates_updater()
        print("Adidas Originals templates updated successfully into directory!")
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
