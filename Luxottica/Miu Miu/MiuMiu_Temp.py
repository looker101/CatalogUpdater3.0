import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import miumiu_update, luxottica_to_import_folder, lux_only_templates

def get_miu_miu_templates():
    
    miu_miu_file = pd.read_excel(miumiu_update)

    miu_miu_file = miu_miu_file[[
        "ID", "Handle", "Command", "Title", "Body HTML",
        "Vendor", "Type", "Tags", "Tags Command",
        "Status", "Template Suffix", "URL", "Variant ID", "Variant SKU",
        "Variant Barcode",
        "Metafield: title_tag [string]", "Metafield: description_tag [string]",
        "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]",
        "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]",
        "Metafield: my_fields.lens_technology [single_line_text_field]",
        "Metafield: my_fields.lens_material [single_line_text_field]",
        "Metafield: my_fields.product_size [single_line_text_field]",
        "Metafield: my_fields.gtin1 [single_line_text_field]",
        "Metafield: my_fields.for_who [single_line_text_field]",
        "Metafield: custom.main_frame_shape [single_line_text_field]",
        "Metafield: custom.main_frame_material [single_line_text_field]",
        "Metafield: custom.main_frame_color [single_line_text_field]",
        "Metafield: custom.main_lens_color [single_line_text_field]",
        "Metafield: custom.main_lens_technology [single_line_text_field]",
        "Metafield: custom.main_size [single_line_text_field]"
    ]]

    miu_miu_file["Vendor"] = "Miu Miu"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    miu_miu_file["Variant SKU"] = miu_miu_file.apply(remove_0_from_variant_sku, axis=1)

    # Create metaTitle
    # {Brand} {model_code} {color_code} {frame_color} for {geneder}
    def getMetaTitle(row):
        brand = row["Vendor"]
        mu = row["Variant SKU"].split()[0]
        model_code = row["Variant SKU"].split()[1]
        color_code = row["Variant SKU"].split()[2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {mu} {model_code} {color_code} {frame_color} {style}"
        return f"{brand} {mu} {model_code} {color_code} {frame_color} {style} for {gender}"

    miu_miu_file["Metafield: title_tag [string]"] = miu_miu_file.apply(getMetaTitle, axis = 1)

    # Create MetaDescription
    def getMetaDescription(row):
        brand = row["Vendor"]
        mu = row["Variant SKU"].split()[0]
        model_code = row["Variant SKU"].split()[1]
        color_code = row["Variant SKU"].split()[2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        style = row["Type"].lower()

        return f"Buy the new {brand} {mu} {model_code} {color_code} {style} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    miu_miu_file["Metafield: description_tag [string]"] = miu_miu_file.apply(getMetaDescription, axis = 1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        mu = row["Variant SKU"].split()[0]
        model_code = row["Variant SKU"].split()[1]
        #product_name = " ".join(row["Title"].split()[2:3])
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        lens_color = row["Metafield: my_fields.lens_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">Super popular among celebrities and influencers, </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> are distinctive, unique and eye-catching. Made prioritizing ergonomic design and a comfortable fit, these shades are designed by the same fashion minds that are behind Prada eyewear.&nbsp;&nbsp;</span></p>
    <p><span style="font-weight: 400;">This one-of-a-kind </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model </span><span style="font-weight: 400;">with </span><strong>{lens_color}</strong><span style="font-weight: 400;"> lenses </span><span style="font-weight: 400;">was designed and manufactured to perfection by Miu Miu in partnership with world-leading eyewear producer Luxottica. An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the </span><strong>{mu}{model_code}</strong><span style="font-weight: 400;"> is going to add a touch of timeless elegance to your everyday look.</span></p>
    <p><br /><span style="font-weight: 400;">Check out all the latest models and designs in the new</span> <span style="font-weight: 400;"><a href="/collections/miu-miu-sunglasses" target="_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Super popular among celebrities and influencers, </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> are distinctive, unique and eye-catching. Made prioritizing ergonomic design and a comfortable fit, these shades are designed by the same fashion minds that are behind Prada eyewear.&nbsp;&nbsp;</span></p>
    <p><span style="font-weight: 400;">This one-of-a-kind </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model was designed and manufactured to perfection by Miu Miu in partnership with world-leading eyewear producer Luxottica. An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the </span><strong>{mu}{model_code}</strong><span style="font-weight: 400;"> is going to add a touch of timeless elegance to your everyday look.</span></p>
    <p><br /><span style="font-weight: 400;">Check out all the latest models and designs in the new</span> <span style="font-weight: 400;"><a href="/collections/miu-miu-eyeglasses" target="_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    miu_miu_file["Body HTML"] = miu_miu_file.apply(getProductDescription, axis = 1)
    miu_miu_file["Title"] = miu_miu_file["Title"].str.replace("Miu miu", "Miu Miu")

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    miu_miu_file = miu_miu_file.dropna(axis = 0, how='any', subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    miu_miu_file = miu_miu_file.sort_values(by="Handle")

    # SAVING
    miu_miu_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Miu Miu/Miu_Miu_Template.xlsx", index = False)
    print("Miu Miu updated and saved on Miu Miu folder")

    # miu_miu_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Miu Miu.xlsx")
    # print("Miu Miu updated and saved on Brand data processor folder")

    miu_miu_file.to_excel(
        f"{lux_only_templates}/MiuMiu_templates.xlsx",
        index=False)
    print("Miu Miu templates updated and saved in Luxottica_to_import_folder")
    
if __name__ == "__main__":
    get_miu_miu_templates()