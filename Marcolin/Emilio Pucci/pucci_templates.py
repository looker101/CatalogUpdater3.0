import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import pucci_excel, pucci_folder, templates


def pucci_templates_updater():
    pucci = pd.read_excel(pucci_excel)


    pucci = pucci[[
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


        sun = f"""<p><span style="font-weight: 400;">Embrace the vivacious spirit of Italian fashion with </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;">. Famed for its kaleidoscopic prints and bold designs, Pucci translates its runway heritage into eyewear that turns heads.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Pucci's commitment to fusing iconic patterns with contemporary silhouettes. Crafted from high-quality materials and featuring signature prints or vibrant colorways, these sunglasses offer both durability and a touch of flamboyant flair.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Whether you're poolside or pounding the pavement, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Emilio Pucci adds a touch of drama to your look. Explore the latest offerings from the <a href="/collections/emilio-pucci-eyeglasses" target="_blank">{brand} {product_type} 2025</a> collection and discover the perfect pair to unleash your inner fashion icon.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Embrace the playful spirit of Italian fashion with </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;">. Famed for its kaleidoscopic prints and bold designs, Pucci translates its runway heritage into eyewear that injects personality into your everyday look.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Pucci's commitment to fusing iconic patterns with modern functionality. Crafted from high-quality materials and featuring signature prints or vibrant colorways, these eyeglasses offer both durability and a touch of whimsical flair.</span></p>
<p><br /><span style="font-weight: 400;">Whether you're leading a meeting or lost in a good book, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Emilio Pucci elevates your look with a touch of Italian joie de vivre. Explore the latest offerings from the <a href="/collections/emilio-pucci-eyeglasses" target="_blank">{brand} {product_type} 2025</a> collection and discover the perfect pair to showcase your unique style.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    pucci["Metafield: title_tag [string]"] = pucci.apply(metaTitle, axis = 1)
    pucci["Metafield: description_tag [string]"] = pucci.apply(metaDescript, axis = 1)
    pucci["Body HTML"] = pucci.apply(productDescription, axis=1)

    # REMOVE ALL DUPLICATES BY HANDLE
    pucci = pucci.drop_duplicates("Title")

    pucci = pucci.sort_values(by="Title")
    pucci.to_excel(f"{pucci_folder}pucci_templates.xlsx", index = False)
    pucci.to_excel(f"{templates}/pucci_templates_ok.xlsx",
                          index=False)


if __name__ == "__main__":
    try:
        print("Saving Emilio Pucci template.")
        pucci_templates_updater()
        print("Emilio Pucci templates saved successfully into To_import folder")
    except Exception as err:
        print("Error in Emilio Pucci file creation process:\n")
        print(f"{type(err).__name__}: {err}")
