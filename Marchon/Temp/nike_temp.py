import pandas as pd
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marchon_paths import NIKE_EXCEL, templates, NIKE_FOLDER_FTP

today = datetime.datetime.now().strftime('%d-%m')


def nike_templates_updater():

    nike = pd.read_excel(NIKE_EXCEL)

    nike = nike[[
        "Variant ID", "Variant SKU", "Variant Barcode", "Image Src",
        "ID", "Handle", "Title", "Body HTML", "Vendor", "Type", "Tags", "Tags Command", "Template Suffix",
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

    #nike["Title"] = nike["Variant SKU"].str[:-2]

    def get_meta_title(row):
        #{brand} {model_code} {lens_code} - {frame_color} {item_type} | LookerOnline
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[1]
        lens_code = row["Variant SKU"].split()[2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"].title()
        product_type = row["Type"]

        return f"{brand} {model_code} {lens_code} - {frame_color} {product_type} | LookerOnline"
    nike["Metafield: title_tag [string]"] = nike.apply(get_meta_title, axis=1)

    #print(nike["Variant SKU"].dtype)

    def get_meta_description(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[1]
        lens_code = row["Variant SKU"].split()[2]
        product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"].lower()
        product_type = row["Type"]
        return (f"New {brand} {model_code} {lens_code} {product_shape} {product_type} on sale! ✓ Express Shipping "
                f"✓ 100% Original and Authentic | LookerOnline")
    nike["Metafield: description_tag [string]"] = nike.apply(get_meta_description, axis = 1)

    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = str(row["Variant SKU"].split()[0])
        color_code = str(row["Variant SKU"].split()[1])
        product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"]
        for_who = row["Metafield: my_fields.for_who [single_line_text_field]"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        product_type = row["Type"]

        sun = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> merge cutting-edge technology with sleek athletic design, perfect for those who lead an active lifestyle and value performance. 
        These sunglasses embody the spirit of innovation and athletic excellence that defines the Nike brand.</span><br /></p>
    <p><span style="font-weight: 400;">Designed for maximum functionality, the </span><strong>{model_code} {frame_color}</strong><span style="font-weight: 400;"> is crafted with precision to ensure durability and comfort during any activity. 
    Ideal for athletes and fitness enthusiasts, these sunglasses offer superior protection and a stylish look.</span><br /></p>
    <p><span style="font-weight: 400;">Explore the latest <a href="/collections/nike-sunglasses" target = "_blank">{brand} {product_type} 2025</a> collection and discover eyewear that enhances your performance and complements your active lifestyle.</span></p>"""

        eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> combine contemporary style with practical functionality, designed for those who value both fashion and performance. 
        Reflecting the brand&rsquo;s commitment to innovation and excellence, these eyeglasses offer a modern and sporty look.</span></p>
    <p><span style="font-weight: 400;">Crafted with high-quality materials, the </span><strong>{model_code} {frame_color}</strong><span style="font-weight: 400;"> ensures comfort and durability for everyday wear. 
    Perfect for individuals who appreciate sleek design and active living, these eyeglasses provide both style and substance.</span></p>
    <p><span style="font-weight: 400;">Discover the latest <a href="/collections/nike-eyeglasses" target = "_blank">{brand} {product_type} 2025</a> collection and find frames that enhance your vision and fit seamlessly into your dynamic lifestyle.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    nike["Body HTML"] = nike.apply(getProductDescription, axis=1)

    nike["Option1 Name"] = "Size"
    nike["Option1 Value"] = nike["Variant SKU"].str[-2:]

    nike = nike.sort_values(by="Handle")

    nike.to_excel(f"{NIKE_FOLDER_FTP}Nike_Templates.xlsx", index=False)
    nike.to_excel(f"{templates}/Nike_Templates.xlsx", index=False)

if __name__ == "__main__":
    try:
        print("Start Nike templates updating...")
        nike_templates_updater()
        print("Nike templates updated succesfully!")
    except Exception as err:
        print(f"Nike templates not updated due this error: {type(err).__name__} - > {err}")

