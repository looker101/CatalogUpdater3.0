import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/De_Rigo")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from de_rigo_paths import porsche_design_folder, porsche_design_excel, logs_folder, templates

def porsche_update():

    # Read the file
    porsche = pd.read_excel(porsche_design_excel)

    porsche = porsche[[
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

    # Template Suffix == Default Product
    # def get_template_suffix(row):
    #     """Working on Default product only """
    #     if pd.isna(row) or row == "":
    #         return "Default product"
    #     return row
    # porsche["Template Suffix"] = porsche["Template Suffix"].apply(get_template_suffix)

    porsche["Template Suffix"] = porsche["Template Suffix"].fillna("Default product")

    #mask = porsche["Template Suffix"] = "Default product"
    #porsche = porsche[mask]

    # MetaTitle
    def get_meta_title(row):
        """{Brand} {product_name} {model_code} {color} {type} for Men and Women"""
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        if pd.isna(row["Metafield: my_fields.frame_color [single_line_text_field]"]):
            frame_color = "Sport"
        else:
            frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"]
        return f"{brand} {model_code} {color_code} - {frame_color} {style} for Men and Women"
    porsche["Metafield: title_tag [string]"] = porsche.apply(get_meta_title, axis=1)

    # MetaDescriptiom
    def get_meta_description(row):
        """New porsche SPL872N men and women sunglasses on sale! ✓ Express Shipping ✓ 100% Original and Authentic"""
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        style = row["Type"].lower()
        return f"New {brand} {model_code} {color_code} men and women {style} on sale! ✓ Express Shipping ✓ 100% Original and Authentic"
    porsche["Metafield: description_tag [string]"] = porsche.apply(get_meta_description, axis=1)

    # Product Title
    def get_product_title(row):
        """Get Product Title == H1"""
        # {brand} {model_code} {color_code}
        return row["Vendor"] + " " + row["Variant SKU"]
    porsche["Title"] = porsche.apply(get_product_title, axis = 1)

    # Handle
    def get_handle(row):
        """Get Handle tag and URL"""
        brand = row["Vendor"].lower()
        sku = row["Variant SKU"].lower()
        sku_split = sku.split()
        sku_join = '-'.join(sku_split)
        return f'{brand}-{sku_join}'
    porsche["Handle"] = porsche.apply(get_handle, axis = 1)

    # get option variants
    porsche["Option1 Name"] = "Size"
    porsche["Option1 Value"] = porsche["Variant SKU"].str[-2:]

    # Product Description
    def get_products_descript(row):
        """Get Product Descript"""
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"].lower()
        sun = f"""<p><strong>Porsche Design sunglasses</strong><span style="font-weight: 400;"> embody a synergy of innovative engineering and minimalist luxury, crafted for those who appreciate both form and function in their accessories. Drawing inspiration from the precision and aerodynamic lines of Porsche cars, these sunglasses reflect the brand's commitment to technical excellence and contemporary style.</span></p>
<p><span style="font-weight: 400;">The </span><strong>{frame_color} {model_code} {color_code}</strong><span style="font-weight: 400;"> combines high-tech materials with a streamlined silhouette, offering unparalleled comfort and durability for any journey. Ideal for discerning individuals who seek more than just eyewear, these sunglasses deliver sophisticated protection and a striking aesthetic.</span></p>
<p><span style="font-weight: 400;">Explore the latest <a href="/collections/porsche-design-sunglasses" target = "_blank">Porsche Design sunglasses 2025</a> collection and discover eyewear that mirrors the performance-driven ethos of Porsche, setting a new standard in luxury and functionality.</span></p>"""

        eye = f"""<p><strong>Porsche Design eyeglasses</strong><span style="font-weight: 400;"> fuse technical innovation with timeless elegance, appealing to those who expect precision and style in every detail. Reflecting the brand&rsquo;s heritage of German engineering and iconic design, these eyeglasses offer a refined yet modern look that seamlessly adapts to a dynamic lifestyle.</span></p>
<p><span style="font-weight: 400;">The </span><strong>{frame_color} {model_code} {color_code}</strong><span style="font-weight: 400;"> is crafted from premium materials, ensuring both durability and lightweight comfort, ideal for all-day wear. Perfect for individuals who value understated luxury and a minimalist aesthetic, these frames blend advanced technology with a design inspired by Porsche&rsquo;s legacy of excellence.</span></p>
<p><span style="font-weight: 400;">Discover the latest <a href="/collections/porsche-design-eyeglasses" target="_blank">Porsche Design eyeglasses 2025</a> collection and experience eyewear that combines visionary design with everyday sophistication, ideal for those who live life in the fast lane.</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    porsche["Body HTML"] = porsche.apply(get_products_descript, axis = 1)

    porsche = porsche.sort_values(by="Title")

    # Save on To_import
    porsche.to_excel(f"{porsche_design_folder}/Porsche_design_templates_ok.xlsx", index=False)
    porsche.to_excel(f"{templates}/Porsche_Design_templates_ok.xlsx", index=False)


if __name__ == "__main__":
    print("Updating porsche catalog:")
    porsche_update()
    print("porsche catalog updated successfully!")