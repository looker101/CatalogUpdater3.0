import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import guess_excel, guess_folder, templates


def guess_updater_templates():
    guess = pd.read_excel(guess_excel)

    guess = guess[[
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


        sun = f"""<p><span style="font-weight: 400;">Contemporary, classic yet modern,</span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are beautiful, fashionable and super-affordable.</span></p>
                  <p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This stylish </span><strong>{frame_color} </strong><span style="font-weight: 400;">model was designed and manufactured by Guess in collaboration with Italian producer Marcolin to take your looks to the next level.</span></p>
                  <p align="justify"><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><a href="/collections/guess-sunglasses" target="_blank"><span style="font-weight: 400;">{brand} {product_type}</span></a><span style="font-weight: 400;"> collection.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Contemporary, classic yet modern,</span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are beautiful, fashionable and super-affordable.</span></p>
                <p><span style="font-weight: 400;">The</span><strong> {brand} {model_code} {color_code} </strong><span style="font-weight: 400;">is an ideal choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.
                </span> <span style="font-weight: 400;">This stylish </span><strong>{frame_color} </strong><span style="font-weight: 400;">model was designed and manufactured by Guess in collaboration with Italian producer Marcolin to take your looks to the next level.</span></p>
                <p align="justify"><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><a href="/collections/guess-eyeglasses" target="_blank"><span style="font-weight: 400;">{brand} {product_type}</span></a><span style="font-weight: 400;"> collection.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye


    guess["Metafield: title_tag [string]"] = guess.apply(metaTitle, axis = 1)
    guess["Metafield: description_tag [string]"] = guess.apply(metaDescript, axis = 1)
    guess["Body HTML"] = guess.apply(productDescription, axis=1)

    # REMOVE ALL DUPLICATES BY HANDLE
    guess = guess.drop_duplicates("Title")

    guess = guess.sort_values(by="Title")

    guess.to_excel(f"{guess_folder}/Guess_templates.xlsx", index = False)
    guess.to_excel(f"{templates}/Guess_templates.xlsx",
                          index=False)


if __name__ == "__main__":
    try:
        print("Starting Guess templates updater.")
        guess_updater_templates()
        print("Guess templates saved successfully into To_import folder")
    except Exception as err:
        print("Error in GUess file creation process:\n")
        print(f"{type(err).__name__}: {err}")