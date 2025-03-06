import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import max_co_excel, max_co_folder, templates


def max_co_templates_updater():
    max_co = pd.read_excel(max_co_excel)
    
    max_co = max_co[[
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

    max_co["Metafield: title_tag [string]"] = max_co.apply(metaTitle, axis=1)

    def metaDescript(row):
        # New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express WorldWide Shipping ✓ 100% Original | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"].lower()
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        return f"New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express World Wide Shipping ✓ 100% Original | LookerOnline"

    max_co["Metafield: description_tag [string]"] = max_co.apply(metaDescript, axis=1)

    def productDescription(row):
        brand = row["Vendor"]
        # product_name = row["Title"].split()[2]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]

        sun = f"""<p><span style="font-weight: 400;">Ditch the ordinary shades, </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are your gateway to effortless summer chic. Designed for the woman who embraces life's adventures with a touch of Italian flair, these sunglasses elevate your look with a dose of sunshine confidence.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Max&amp;Co.'s signature blend of playful femininity and timeless design. Crafted from high-quality materials with a focus on comfort and sun protection, these sunglasses feature statement shapes and unexpected details that turn heads.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Whether you're conquering the beach scene or strolling through charming piazzas, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Max&amp;Co. adds a touch of effortless glamour to your look. Check out all the latest models and designs in the new <a href="/collections/max-co-sunglasses" target="_blank">{brand} {product_type} 2025</a> collection and discover the perfect pair to embrace every sun-kissed moment in style.</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Forget fussy frames, </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are the ultimate wardrobe essentials. Designed for the woman who curates her style with a sharp eye, these frames seamlessly transition from workday chic to weekend wanderings.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Max&amp;Co.'s dedication to elevated basics. Crafted from premium materials in a lightweight yet sturdy design, these glasses boast clean lines and subtle details that whisper luxury.</span></p>
<p><br /><span style="font-weight: 400;">Whether you're leading a brainstorming session or sipping coffee with friends, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Max&amp;Co. injects a touch of effortless polish into your look. Check out all the latest models and designs in the new <a href="/collections/max-co-eyeglasses" target="_blank">{brand} {product_type} 2025</a> collection and discover the perfect pair to become your signature staple.</span></p>"""
        if row["Type"] == "Sunglasses":
            return sun
        return eye

    max_co["Body HTML"] = max_co.apply(productDescription, axis=1)

    # REMOVE ALL DUPLICATES BY HANDLE
    max_co = max_co.drop_duplicates("Title")

    max_co = max_co.sort_values(by="Title")
    max_co.to_excel(f"{max_co_folder}max_co_Templates_updated.xlsx", index=False)
    max_co.to_excel(f"{templates}/max_co_templates_ok.xlsx",
                              index = False)


if __name__ == "__main__":
    try:
        print("Max & Co templates updating...")
        max_co_templates_updater()
        print("Max & Co templates updated successfully into directory!")
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
