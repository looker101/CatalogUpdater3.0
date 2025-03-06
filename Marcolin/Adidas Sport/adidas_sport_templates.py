import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import adidas_sport_excel, adidas_sport_folder, templates


def adidas_sport_templates_updater():
    adidas_sport = pd.read_excel(adidas_sport_excel)

    adidas_sport = adidas_sport[[
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


        sun = f"""<p align="juistify">Simple, young, sporty and super-comfortable, <strong>{brand} {product_type}</strong> will take your game to the next level without compromising on quality and style. 
                    <br /><br /> The <strong>{brand} {model_code} {color_code}</strong> is the perfect choice for <strong>{gender}</strong>. 
                    This stylish and sporty <strong>{frame_color}</strong> model was designed and manufactured by Italian producer Marcolin to meet Adidas top-quality standards.<br /><br />
                Check out hundreds of new models and designs in the new <a href="/collections/adidas-sport-sunglasses" target="_blank"><i>Adidas Sport sunglasses</i></a> collection!
                </p>"""

        eye = f"""<p align="justify" data-mce-fragment="1">With a focus on optimal fit, eye protection and superior performance, <strong>{brand} {product_type}</strong> will take your game to the next level without compromising on quality and style.<br /><br /> 
                The&nbsp;<strong>{brand} {model_code} {color_code}</strong> is the perfect choice for <strong>{gender}</strong>. 
                This stylish and sporty <strong>{frame_color}</strong> model was designed and manufactured by Italian producer Marcolin to meet Adidas top-quality standards<br /><br />. 
                Check out hundreds of new models and designs in the new <a href="/collections/adidas-sport-eyeglasses" target="_blank" rel="noopener"><em>2025 Adidas Sport eyeglasses collection</em></a>!</p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    adidas_sport["Metafield: title_tag [string]"] = adidas_sport.apply(metaTitle, axis = 1)
    adidas_sport["Metafield: description_tag [string]"] = adidas_sport.apply(metaDescript, axis = 1)
    adidas_sport["Body HTML"] = adidas_sport.apply(productDescription, axis=1)

    # REMOVE ALL DUPLICATES BY HANDLE
    adidas_sport = adidas_sport.drop_duplicates("Title")

    adidas_sport = adidas_sport.sort_values(by="Title")
    adidas_sport.to_excel(f"{adidas_sport_folder}Adidas_Sport_templates.xlsx", index = False)
    adidas_sport.to_excel(f"{templates}/adidas_sport_templates_ok.xlsx",
                          index=False)


if __name__ == "__main__":
    try:
        print("Saving Adidas sport template.")
        adidas_sport_templates_updater()
        print("Adidas sport templates saved successfully into To_import folder")
    except Exception as err:
        print("Error in Adidas Sport file creation process:\n")
        print(f"{type(err).__name__}: {err}")
