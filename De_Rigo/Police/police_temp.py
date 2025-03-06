import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/De_Rigo")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from de_rigo_paths import police_folder, police_excel, templates

def police_update():

    police = pd.read_excel(police_excel)

    police = police[[
        "Variant ID", "Variant SKU", "Variant Barcode", "Variant Price",
        "ID", "Handle", "Title", "Body HTML", "Vendor", "Type", "URL", "Tags", "Tags Command", "Template Suffix", "Inventory Available: +39 05649689443",
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

    # def get_template_suffix(row):
    #     if pd.isna(row) or row == "":
    #         return "Default product"
    #     return row
    #
    # police["Template Suffix"] = police["Template Suffix"].apply(get_template_suffix)

    police["Template Suffix"] = police["Template Suffix"].fillna("Default product")

    #mask = police["Template Suffix"] = "Default product"
    #police = police[mask]

    def get_meta_title(row):
        # {Brand} {product_name} {model_code} {color} {type} for Men and Women
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        style = row["Type"].lower()
        return f"{brand} {model_code} {color_code} {style} for Men and Women"


    police["Metafield: title_tag [string]"] = police.apply(get_meta_title, axis=1)


    def get_meta_description(row):
        # New Police SPL872N men and women sunglasses on sale! ✓ Express Shipping ✓ 100% Original and Authentic
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        style = row["Type"].lower()
        return f"New {brand} {model_code} {color_code} men and women {style} on sale! ✓ Express Shipping ✓ 100% Original and Authentic"


    police["Metafield: description_tag [string]"] = police.apply(get_meta_description, axis=1)

    def get_product_title(row):
        # {brand} {model_code} {color_code}
        return row["Vendor"] + " " + row["Variant SKU"]

    police["Title"] = police.apply(get_product_title, axis = 1)

    def get_handle(row):
        brand = row["Vendor"].lower()
        sku = row["Variant SKU"].lower()
        sku_split = sku.split()
        sku_join = '-'.join(sku_split)
        return f'{brand}-{sku_join}'

    police["Handle"] = police.apply(get_handle, axis = 1)

    # get option variants
    police["Option1 Name"] = "Size"
    police["Option1 Value"] = police["Variant SKU"].str[-2:]

    def get_products_descript(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        style = row["Type"].lower()
        sun = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> blend urban style with bold sophistication, making them ideal for individuals who seek a daring and distinctive look. Reflecting the edgy aesthetic of the Police brand, these sunglasses offer a statement-making design that sets you apart.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">Crafted with durable materials, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> ensures long-lasting comfort and protection, perfect for all-day wear. Designed for those who embrace a bold attitude, these sunglasses offer both function and high-fashion.</span></p>
    <p><span style="font-weight: 400;"><br /></span><span style="font-weight: 400;">Explore the latest <a href="/collections/police-sunglasses" target="_blank">{brand} {style} 2025 collection</a> and discover eyewear that combines cutting-edge style with modern practicality.</span></p>"""
        eye = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> combine modern design with a rebellious edge, offering a unique style for those who want to stand out. Staying true to the Police brand&rsquo;s distinctive urban aesthetic, these eyeglasses provide a contemporary look that&rsquo;s effortlessly cool.</span></p>
    <p>&nbsp;</p>
    <p><span style="font-weight: 400;">Made with top-quality materials, the </span><strong>{model_code} {color_code}</strong><span style="font-weight: 400;"> delivers comfort and durability for daily wear. Ideal for individuals who appreciate bold and unconventional designs, these eyeglasses offer both style and practicality.</span></p>
    <p><span style="font-weight: 400;"><br /></span><span style="font-weight: 400;">Discover the latest <a href="/collections/police-eyeglasses" target="_blank">{brand} {style} 2025 collection</a> and elevate your everyday style with a touch of urban flair.</span></p>"""
        match row["Type"]:
            case "Sunglasses":
                return sun
            case _:
                return eye

    police["Body HTML"] = police.apply(get_products_descript, axis = 1)

    police = police.sort_values(by="Title")

    police.to_excel(f"{police_folder}/Police_templates.xlsx", index=False)
    police.to_excel(f"{templates}/Police_templates.xlsx", index=False)


if __name__ == "__main__":
    print("Updating Police catalog:")
    police_update()
    print("Police catalog updated successfully!")