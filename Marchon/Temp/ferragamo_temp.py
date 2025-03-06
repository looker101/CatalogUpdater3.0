import pandas as pd
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marchon_paths import FERRAGAMO_EXCEL, FERRAGAMO_FOLDER_FTP, templates

today = datetime.datetime.now().strftime('%d-%m')


def ferragamo_templates_updater():
    ferragamo = pd.read_excel(FERRAGAMO_EXCEL)


    ferragamo = ferragamo[[
        "Variant ID", "Variant SKU", "Variant Barcode", "Image Src",
        "ID", "Handle", "Title", "Body HTML", "Vendor", "Type", "URL", "Tags", "Tags Command", "Template Suffix", "Inventory Available: +39 05649689443",
        "Metafield: title_tag [string]", "Metafield: description_tag [string]", "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]", "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]",
        "Metafield: my_fields.product_size [single_line_text_field]", "Metafield: my_fields.for_who [single_line_text_field]",
        "Metafield: custom.main_frame_shape [single_line_text_field]",
        "Metafield: custom.main_frame_material [single_line_text_field]", "Metafield: custom.main_frame_color [single_line_text_field]",
        "Metafield: custom.main_lens_color [single_line_text_field]", "Metafield: custom.main_lens_technology [single_line_text_field]",
        "Metafield: custom.main_size [single_line_text_field]"

    ]]


    def getMetaTitle(row):
        brand = row["Vendor"].capitalize()
        model_code = row["Variant SKU"].split()[0]
        lens_code = row["Variant SKU"].split()[1]
        frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).capitalize()
        item_type = row["Type"]
        return f"{brand} {model_code} {lens_code} - {frame_color} {item_type} | LookerOnline"

    ferragamo["Metafield: title_tag [string]"] = ferragamo.apply(getMetaTitle, axis=1)


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

    ferragamo["Metafield: description_tag [string]"] = ferragamo.apply(getMetaDescript, axis=1)


    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"]
        for_who = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        product_type = row["Type"]

        sun = f"""<p><strong> {brand} {product_type}</strong><span style="font-weight: 400;"> exude timeless elegance and luxury, embodying the sophisticated style that the Ferragamo brand is known for. 
        Perfect for those who appreciate refined design and exquisite craftsmanship, these sunglasses make a chic fashion statement.</span><br /></p>
    <p><span style="font-weight: 400;">Handcrafted in Italy, the </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> reflects the brand&rsquo;s dedication to quality and detail. 
    Ideal for individuals with a taste for luxury, these sunglasses offer both style and superior comfort.</span></p><br />
    <p><span style="font-weight: 400;">Explore the latest <a href = "/collections/ferragamo-sunglasses" target = "_blank">{brand} {product_type} 2025</a> collection and discover eyewear that epitomizes classic sophistication and modern elegance.</span></p>"""

        eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> blend classic design with contemporary flair, reflecting the brand&rsquo;s heritage of elegance and craftsmanship. 
        Perfect for those who value sophistication and quality, these eyeglasses add a touch of luxury to everyday wear.</span><br /></p>
    <p><span style="font-weight: 400;">Meticulously crafted in Italy, the </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> showcases the brand&rsquo;s commitment to excellence and refined style. 
    These eyeglasses offer a sophisticated look that combines comfort and durability.</span></p>
    <p><span style="font-weight: 400;">Discover the latest <a href= "/collections/ferragamo-sunglasses" target = "_blank">{brand} {product_type} 2025</a> collection and find frames that elevate your everyday style with timeless elegance.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    ferragamo["Body HTML"] = ferragamo.apply(getProductDescription, axis=1)

    # SORT BY TITLE (NOT FOR HANDE DUE THE NEW PRODUCTS DON'T HAVE HANDLE)
    ferragamo = ferragamo.sort_values(by="Title")

    ferragamo.to_excel(f"{FERRAGAMO_FOLDER_FTP}Ferragamo_Templates.xlsx", index=False)
    ferragamo.to_excel(f"{templates}/Ferragamo_Templates.xlsx", index = False)


if __name__ == "__main__":
    try:
        print("Start Ferragamo templates updating...")
        ferragamo_templates_updater()
        print("Ferragamo templates updated succesfully!")
    except Exception as err:
        print(f"Ferragamo templates not updated due this error: {type(err).__name__} - > {err}")
