import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from marcolin_paths import zegna_excel, zegna_folder, templates

def zegna_templates_updater():
    zegna = pd.read_excel(zegna_excel)

    zegna = zegna[[
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
        # {Brand} {model_code} {color_code} {product_type} | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        return f"{brand} {model_code} {color_code} {product_type} | LookerOnline"

    zegna["Metafield: title_tag [string]"] = zegna.apply(metaTitle, axis=1)

    def metaDescript(row):
        # New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express WorldWide Shipping ✓ 100% Original | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        return f"New {brand} {model_code} {color_code} {gender} {product_type} on sale! ✓ Express World Wide Shipping ✓ 100% Original | LookerOnline"

    zegna["Metafield: description_tag [string]"] = zegna.apply(metaDescript, axis=1)

    def productDescription(row):
        brand = row["Vendor"]
        # product_name = row["Title"].split()[2]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_type = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]

        sun = f"""<p><span style="font-weight: 400;">For over a century, Zegna has defined Italian luxury with its meticulous tailoring and premium materials. This heritage extends to the new </span><strong>{brand} {product_type}</strong><span style="font-weight: 400;">, each pair meticulously crafted to embody timeless elegance and unparalleled quality.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Zegna's commitment to fusing their rich heritage with modern innovation. Crafted from premium materials like precious woods or lightweight titanium, and featuring hand-finished details, these sunglasses offer exceptional comfort, superior protection, and sophisticated style.</span></p>
<p><br /><span style="font-weight: 400;">Whether you're strolling through historic piazzas or traversing bustling avenues, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Zegna elevates your look with a touch of Italian legacy. Explore the latest offerings from the <a href="/collections/ermenegildo-zegna-sunglasses" target="_blank">{brand} {product_type} 2025</a> collection and discover the perfect pair to express your discerning taste!</span></p>"""

        eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> embody the brand's dedication to timeless elegance and Italian craftsmanship. Founded in 1910, Zegna is renowned for its luxurious fabrics and sartorial expertise, qualities it seamlessly translates into its eyewear collection.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">This distinct </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model exemplifies Zegna's commitment to fusing classic design with contemporary innovation. Crafted from high-quality materials like acetate or lightweight titanium, and featuring meticulous details, these eyeglasses offer exceptional durability and sophisticated style.</span></p>
<p><br /><span style="font-weight: 400;">Whether you're leading a board meeting or enjoying a stroll, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> by Zegna elevates your look with effortless refinement. Check out all the latest offerings from the <a href="/collections/ermenegildo-zegna-eyeglasses" target="_blank">{brand} {product_type} 2025</a> collection and discover the perfect pair to define your signature style!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    zegna["Body HTML"] = zegna.apply(productDescription, axis=1)


    # REMOVE ALL DUPLICATES BY HANDLE
    zegna = zegna.drop_duplicates("Title")

    zegna = zegna.sort_values(by="Title")
    zegna.to_excel(f"{zegna_folder}zegna_Templates_updated.xlsx", index=False)
    zegna.to_excel(f"{templates}/zegna_templates_ok.xlsx",
                              index = False)


if __name__ == "__main__":
    try:
        print("Zegna templates updating...")
        zegna_templates_updater()
        print("ZegNA templates updated successfully into directory!")
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
