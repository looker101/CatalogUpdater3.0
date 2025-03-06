import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import max_mara_excel, max_mara_folder, templates


def max_mara_templates_updater():
    max_mara = pd.read_excel(max_mara_excel)
    
    max_mara = max_mara[[
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
    
    max_mara["Metafield: description_tag [single_line_text_field]"] = ""
    max_mara["Metafield: title_tag [single_line_text_field]"] = ""

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

    max_mara["Metafield: title_tag [string]"] = max_mara.apply(metaTitle, axis=1)

    def metaDescript(row):
        # New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express WorldWide Shipping ✓ 100% Original | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"].lower()
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        return f"New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express World Wide Shipping ✓ 100% Original | LookerOnline"

    max_mara["Metafield: description_tag [string]"] = max_mara.apply(metaDescript, axis=1)

    def productDescription(row):
        brand = row["Vendor"]
        # product_name = row["Title"].split()[2]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]

        sun = f"""<p><strong>{brand}  {product_type}</strong><span style="font-weight: 400;"> are more than just sun protection; they're a statement of refined confidence.&nbsp; Designed for the woman who embodies effortless elegance, they offer superior UV protection with a touch of timeless Italian glamour.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Max Mara's dedication to marrying luxury with functionality. Crafted from premium materials with high-performance lenses, these sunglasses offer unparalleled protection without compromising on style. Exquisite details and timeless silhouettes ensure they become a signature piece in your wardrobe.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Whether navigating cityscapes or soaking up the sun on a luxurious getaway, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Max Mara elevates your look with a touch of sophisticated allure. Check out all the latest models and designs from the new <a href="/collections/max-mara-eyeglasses" target="_blank">{brand}  {product_type}</a> 2025 collection and discover the perfect pair to unveil your confidence in every ray of light.</span></p>"""

        eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> transcend trends, embodying the essence of understated elegance. Designed for a woman who appreciates quality and craftsmanship, they elevate your everyday look with a touch of timeless sophistication.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Max Mara's unwavering commitment to refined luxury. Crafted from the finest materials with meticulous attention to detail, these eyeglasses boast clean lines and classic silhouettes that never go out of style.</span></p>
<p><br /><span style="font-weight: 400;">Whether you're gracing the boardroom or enjoying a leisurely afternoon, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Max Mara exudes quiet confidence and effortless style. Check out all the latest models and designs from the new <a href="/collections/max-mara-sunglasses" target="_blank">{brand} {product_type} 2025</a> collection and discover the perfect pair to become a cornerstone of your sophisticated wardrobe.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    max_mara["Body HTML"] = max_mara.apply(productDescription, axis=1)

    # REMOVE ALL DUPLICATES BY HANDLE
    max_mara = max_mara.drop_duplicates("Title")

    max_mara = max_mara.sort_values(by="Title")
    max_mara.to_excel(f"{max_mara_folder}max_mara_Templates_updated.xlsx", index=False)
    max_mara.to_excel(f"{templates}/max_mara_templates_ok.xlsx",
                              index = False)


if __name__ == "__main__":
    try:
        print("MaxMara templates updating...")
        max_mara_templates_updater()
        print("MaxMara templates updated successfully into directory!")
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
