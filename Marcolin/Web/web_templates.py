import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import web_excel, web_folder, templates


def web_templates_updater():
    web = pd.read_excel(web_excel)

    web = web[[
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

    # def metaTitle(row):
    #     # {Brand} {model_code} {color_code} {product_type} | LookerOnline
    #     brand = row["Vendor"]
    #     if pd.notna(row["Variant SKU"]):
    #         model_code = row["Variant SKU"].split()[0]
    #         color_code = row["Variant SKU"].split()[1]
    #     else:
    #         model_code = ""
    #         color_code = ""
    #     product_type = row["Type"]
    #     return f"{brand} {model_code} {color_code} {product_type} | LookerOnline"

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

    web["Metafield: title_tag [string]"] = web.apply(metaTitle, axis=1)

    # def metaDescript(row):
    #     # New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express WorldWide Shipping ✓ 100% Original | LookerOnline
    #     brand = row["Vendor"]
    #     if pd.notna(row["Variant SKU"]):
    #         model_code = row["Variant SKU"].split()[0]
    #         color_code = row["Variant SKU"].split()[1]
    #     else:
    #         model_code = ""
    #         color_code = ""
    #     product_type = row["Type"]
    #     gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
    #     return f"New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express World Wide Shipping ✓ 100% Original | LookerOnline"

    def metaDescript(row):
        # New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express WorldWide Shipping ✓ 100% Original | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"].lower()
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        return f"New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express World Wide Shipping ✓ 100% Original | LookerOnline"

    web["Metafield: description_tag [string]"] = web.apply(metaDescript, axis=1)

    def productDescription(row):
        brand = row["Vendor"]
        # product_name = row["Title"].split()[2]
        if pd.notna(row["Variant SKU"]):
            model_code = row["Variant SKU"].split()[0]
            color_code = row["Variant SKU"].split()[1]
        else:
            model_code = ""
            color_code = ""
        product_type = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]

        sun = f"""<p><strong>Web Eyewear sunglasses</strong><span style="font-weight: 400;"> are for those who embrace a dynamic perspective. Inspired by the spirit of curiosity and exploration, Web Eyewear offers sunglasses that push boundaries and redefine style.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Web Eyewear's commitment to fusing innovative design with statement-making style. Crafted from high-quality materials and featuring bold shapes or unexpected details, these sunglasses offer superior sun protection and a touch of audacious flair.</span></p>
<p><br /><span style="font-weight: 400;">Whether you're conquering city streets or soaking up the sun on an adventure, the </span><strong>{model_code}</strong><span style="font-weight: 400;"> by Web Eyewear elevates your look with a touch of pioneering spirit. Explore the latest offerings from the new <a href="/collections/web-eyewear-sunglasses" target="_blank">Web Eyewear sunglasses 2025</a> collection and discover the perfect pair to see the world through a bolder </span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Embrace the world with a fresh perspective through </span><strong>Web Eyewear eyeglasses</strong><span style="font-weight: 400;">. Designed for the curious and adventurous, Web Eyewear offers a unique blend of timeless appeal and contemporary flair.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Web Eyewear's commitment to fusing modern design with easy wearability. Crafted from high-quality materials and featuring clean lines and innovative details, these eyeglasses offer both comfort and a touch of distinctive style.</span></p>
<p><br /><span style="font-weight: 400;">Whether you're exploring new horizons or navigating the everyday, the </span>{model_code}<strong></strong><span style="font-weight: 400;"> by Web Eyewear elevates your look with a touch of modern sophistication. Discover the latest offerings from the new <a href="/collections/web-eyewear-eyeglasses" target = "_blank">Web Eyewear eyeglasses 2025</a> collection and find the perfect pair to fuel your adventures in style.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    web["Body HTML"] = web.apply(productDescription, axis=1)

    # REMOVE ALL DUPLICATES BY HANDLE
    web = web.drop_duplicates("Title")

    web = web.sort_values(by="Title")
    web.to_excel(f"{web_folder}Web_Templates_updated.xlsx", index=False)
    web.to_excel(f"{templates}/web_templates_ok.xlsx",
                              index = False)


if __name__ == "__main__":
    try:
        print("Web templates updating...")
        web_templates_updater()
        print("Web templates updated successfully into directory!")
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
