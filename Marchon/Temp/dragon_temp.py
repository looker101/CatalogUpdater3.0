import pandas as pd
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marchon_paths import DRAGON_EXCEL, DRAGON_FOLDER_FTP, templates

today = datetime.datetime.now().strftime('%d-%m')


def dragon_templates_updater():

    dragon = pd.read_excel(DRAGON_EXCEL)

    mask = dragon["Template Suffix"] == "Default product"
    dragon = dragon[mask]

    dragon = dragon[[
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
        brand = row["Vendor"].title()
        model_code = row["Variant SKU"].split()[0]
        lens_code = row["Variant SKU"].split()[1]
        frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).title()
        item_type = row["Type"]
        return f"{brand} {model_code} {lens_code} - {frame_color} {item_type} | LookerOnline"

    dragon["Metafield: title_tag [string]"] = dragon.apply(getMetaTitle, axis=1)


    def getMetaDescript(row):
        # {brand} {codice del modello} {codice del colore} {frame_colore} {forma} {genere} {tipologia}
        brand = row["Vendor"].title()
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"].lower()

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            for_who = "Man and Woman"
        else:
            for_who = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()

        product_type = row["Type"]
        # frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        return f"New {brand} {model_code} {color_code} {product_shape} {product_type} for {for_who} on sale! ✓ Express Shipping ✓ 100% Original and Authentic | LookerOnline"

    dragon["Metafield: description_tag [string]"] = dragon.apply(getMetaDescript, axis=1)


    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            for_who = "Man and Woman"
        else:
            for_who = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()

        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        product_type = row["Type"]

        sun = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are designed for adventurers and thrill-seekers, combining rugged durability with bold design. Perfect for those who embrace an active and adventurous lifestyle, these sunglasses reflect the dynamic spirit of the {brand} brand.</span></p>
<p><span style="font-weight: 400;">Engineered for performance, the </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> is crafted with innovative materials to withstand the elements while providing maximum comfort and protection. Ideal for outdoor enthusiasts, these sunglasses offer a stylish yet functional accessory for any adventure.</span></p>
<p><span style="font-weight: 400;">Explore the latest <a href="/collections/dragon-sunglasses" target="_blank"> {brand} {product_type} 2025 </a>collection and discover eyewear that meets the demands of your adventurous spirit.</span></p>"""

        eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are designed for adventurers and thrill-seekers, combining rugged durability with bold design. Perfect for those who embrace an active and adventurous lifestyle, these sunglasses reflect the dynamic spirit of the {brand} brand.</span></p>
<p><span style="font-weight: 400;">Engineered for performance, the </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> is crafted with innovative materials to withstand the elements while providing maximum comfort and protection. Ideal for outdoor enthusiasts, these sunglasses offer a stylish yet functional accessory for any adventure.</span></p>
<p><span style="font-weight: 400;">Explore the latest <a href="/collections/dragon-eyeglasses" target="_blank"> {brand} {product_type} 2025 </a>collection and discover eyewear that meets the demands of your adventurous spirit.</span></p>"""

        goggles = f"""<p><span style="font-weight: 400;"><strong>Dragon snow goggles</strong> are engineered for high-performance and extreme conditions, making them the perfect choice for athletes and thrill-seekers. With cutting-edge technology and a bold design, these {product_type} reflect the fearless innovation of the Dragon brand.<br /></span><span style="font-weight: 400;"><br /></span><span style="font-weight: 400;">Built for durability and clarity, the <strong>{frame_color} {model_code}</strong> features advanced lens technology and a secure fit for optimal vision and protection. Designed for those who push the limits, these goggles offer both superior performance and uncompromising style.<br /></span><span style="font-weight: 400;"><br /></span><span style="font-weight: 400;">Explore the latest <a href="/collections/dragon-ski-goggles">{brand} {product_type} 2025</a> collection and experience eyewear that enhances every adventure with precision and confidence.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        elif row["Type"] == "Eyeglasses":
            return eye
        return goggles

    dragon["Body HTML"] = dragon.apply(getProductDescription, axis=1)

    # SORT BY TITLE (NOT FOR HANDE DUE THE NEW PRODUCTS DON'T HAVE HANDLE)
    dragon = dragon.sort_values(by="Title")

    dragon.to_excel(f"{DRAGON_FOLDER_FTP}Dragon_Templates.xlsx", index=False)
    dragon.to_excel(f"{templates}/Dragon_Templates.xlsx", index = False)


if __name__ == "__main__":
    try:
        print("Start dragon templates updating...")
        dragon_templates_updater()
        print("dragon templates updated succesfully!")
    except Exception as err:
        print(f"dragon templates not updated due this error: {type(err).__name__} - > {err}")
