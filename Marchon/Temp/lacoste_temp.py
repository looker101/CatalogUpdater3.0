import pandas as pd
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marchon_paths import LACOSTE_EXCEL, templates, LACOSTE_FOLDER_FTP

today = datetime.datetime.now().strftime('%d-%m')

def lacoste_templates_updater():

    lacoste = pd.read_excel(LACOSTE_EXCEL)


    lacoste = lacoste[[
        "Variant ID", "Variant SKU", "Variant Barcode", "Image Src",
        "ID", "Handle", "Title", "Body HTML", "Vendor", "Type", "URL", "Tags", "Tags Command", "Template Suffix", "Inventory Available: +39 05649689443",
        "Metafield: title_tag [string]", "Metafield: description_tag [string]", "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]", "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]",
        "Metafield: my_fields.product_size [single_line_text_field]", "Metafield: my_fields.for_who [single_line_text_field]",
        "Metafield: custom.main_frame_shape [single_line_text_field]",
        "Metafield: custom.main_frame_material [single_line_text_field]",
        "Metafield: custom.main_frame_color [single_line_text_field]",
        "Metafield: custom.main_lens_color [single_line_text_field]",
        "Metafield: custom.main_lens_technology [single_line_text_field]",
        "Metafield: custom.main_size [single_line_text_field]"

    ]]

    def getMetaTitle(row):
        brand = row["Vendor"].capitalize()
        model_code = row["Variant SKU"].split()[0]
        lens_code = row["Variant SKU"].split()[1]
        frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).capitalize()
        item_type = row["Type"]
        return f"{brand} {model_code} {lens_code} - {frame_color} {item_type} | LookerOnline"

    lacoste["Metafield: title_tag [string]"] = lacoste.apply(getMetaTitle, axis=1)


    def getMetaDescript(row):
        # {brand} {codice del modello} {codice del colore} {frame_colore} {forma} {genere} {tipologia}
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"]
        for_who = row["Metafield: my_fields.for_who [single_line_text_field]"]
        product_type = row["Type"]
        # frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        return f"New {brand} {model_code} {color_code} {product_shape} {product_type} on sale! ✓ Express Shipping ✓ 100% Original and Authentic | LookerOnline"

    lacoste["Metafield: description_tag [string]"] = lacoste.apply(getMetaDescript, axis=1)


    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"]
        for_who = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        product_type = row["Type"]

        sun = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> bring a touch of timeless elegance to modern eyewear, seamlessly blending the brand&rsquo;s heritage with contemporary design. 
        Ideal for those who appreciate classic style with a modern edge, these sunglasses embody the sophistication of Lacoste.</span></p>
        <p><span style="font-weight: 400;">The </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;">, with its refined frame and high-performance lenses, showcases the brand's commitment to quality and style. 
        Crafted with precision, these sunglasses offer not only a sleek look but also exceptional comfort and durability, making them perfect for everyday wear.</span><br /></p>
        <p><span style="font-weight: 400;">Check out the latest <a href="/collections/lacoste-sunglasses" target="_blank">{brand} {product_type} 2025</a> collection and discover the perfect pair that complements your style.</span></p>"""

        eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> represent the pinnacle of understated elegance, merging the brand&rsquo;s iconic style with modern functionality.
        Perfect for those who value both fashion and practicality, these eyeglasses reflect Lacoste&rsquo;s commitment to quality and design.</span><br /></p>
        <p><span style="font-weight: 400;">The </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> features a sleek, minimalist design with subtle branding, crafted from high-quality materials for a comfortable and durable fit. 
        Each pair embodies the brand's dedication to creating eyewear that is both stylish and functional, making them a versatile addition to any wardrobe.</span><br /></p>
        <p><span style="font-weight: 400;">Explore the latest <a href= "/collections/lacoste-eyeglasses" target="_blank">{brand} {product_type} 2025</a> collection and find the ideal frames that enhance your look with effortless sophistication.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    lacoste["Body HTML"] = lacoste.apply(getProductDescription, axis=1)

    # SORT BY TITLE (NOT FOR HANDE DUE THE NEW PRODUCTS DON'T HAVE HANDLE)
    lacoste = lacoste.sort_values(by="Title")

    # SAVE
    lacoste.to_excel(f"{LACOSTE_FOLDER_FTP}Lacoste_Templates.xlsx", index=False)
    lacoste.to_excel(f"{templates}/Lacoste_Templates.xlsx", index=False)
    # lacoste.to_excel("C:\\Users\\miche\\Desktop\\.py\\catalog_price\\Brand\\LACOSTE.xlsx", index = False)


if __name__ == "__main__":
    try:
        print("Start Lacoste templates updating...")
        lacoste_templates_updater()
        print("Lacoste templates updated succesfully!")
    except Exception as err:
        print(f"Lacoste templates not updated due this error: {type(err).__name__} - > {err}")

