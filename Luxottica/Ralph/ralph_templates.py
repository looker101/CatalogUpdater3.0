import pandas as pd
import sys

from openpyxl.worksheet.pagebreak import RowBreak

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, ralph_update, lux_only_templates


def get_ralph_templates():
    ralph_file = pd.read_excel(ralph_update)
    # ralph_file = ralph_file.dropna(axis = 0, how = "any",
    # subset=["Metafield: my_fields.frame_color [single_line_text_field]"])

    ralph_file = ralph_file[[
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

    ralph_file["Vendor"] = "Ralph"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    ralph_file["Variant SKU"] = ralph_file.apply(remove_0_from_variant_sku, axis=1)

    # Create metaTitle
    # {Brand} {model_code} {color_code} {frame_color} for {geneder}
    def getMetaTitle(row):
        brand = row["Vendor"]
        rh = row["Variant SKU"].split()[0]
        model_code = row["Variant SKU"].split()[1]
        color_code = row["Variant SKU"].split()[2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {style} {rh} {model_code} {color_code} {frame_color}"
        return f"{brand} {style} {rh} {model_code} {color_code} {frame_color} for {gender}"

    ralph_file["Metafield: title_tag [string]"] = ralph_file.apply(getMetaTitle, axis=1)

    # Create MetaDescription
    def getMetaDescription(row):
        brand = row["Vendor"]
        rh = row["Variant SKU"].split()[0]
        model_code = row["Variant SKU"].split()[1]
        color_code = row["Variant SKU"].split()[2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        style = row["Type"].lower()

        return f"Buy the new {brand} {style} {rh} {color_code} {model_code} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    ralph_file["Metafield: description_tag [string]"] = ralph_file.apply(getMetaDescription, axis=1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        #rh = row["Variant SKU"].split()[0]
        model_code = row["Variant SKU"].split()[1]
        color_code = row["Variant SKU"].split()[2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]
        frame_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"]

        sun = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> embody the quintessential American luxury and classic style of the brand. Rooted in a rich heritage, these sunglasses reflect a polished elegance combined with a timeless aesthetic. They stand as a symbol of prestige and refined taste, celebrating traditional craftsmanship and sophisticated simplicity.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">The latest </span><strong>{model_code} {color_code} {frame_color}</strong><span style="font-weight: 400;"> with </span><strong>{frame_shape}</strong><span style="font-weight: 400;"> shape are perfect designer sunglasses for </span><strong>{gender}</strong><span style="font-weight: 400;">. Ralph enhances every look with a touch of understated luxury and a commitment to fine detailing. These pieces serve not just as fashion statements but as staples of a distinguished lifestyle.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/ralph-sunglasses" target="_blank">{brand} {style} 2025</a> collection!</span></p>"""

        eye = f"""<p><strong>{brand} {style}</strong><span style="font-weight: 400;"> offer a seamless blend of timeless style and American sophistication. These frames capture the essence of the Ralph Lauren lifestyle, characterized by an elegant, preppy charm that's both classic and contemporary. Each pair is crafted with attention to detail, ensuring not only style but also comfort and durability.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Discover the </span><strong>{model_code} {color_code} {frame_color}</strong><span style="font-weight: 400;"> </strong><span style="font-weight: 400;">, ideal for </span><strong>{gender}</strong><span style="font-weight: 400;"> seeking both functionality and fashion. These eyeglasses highlight Ralph&rsquo;s dedication to quality and a refined aesthetic, making them essential for any wardrobe requiring a touch of class.</span></p>
<p>&nbsp;</p>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/ralph-eyeglasses" target="_blank">{brand} {style} 2025</a> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    ralph_file["Body HTML"] = ralph_file.apply(getProductDescription, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    ralph_file = ralph_file.dropna(axis=0, how='any',
                                   subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    ralph_file = ralph_file.sort_values("Handle")

    # Saving
    ralph_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Ralph/Ralph_templates.xlsx",
        index=False)
    print("ralph updated and saved on ralph folder")

    # ralph_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/ralph.xlsx", index = False)
    # print("ralph updated and saved on Brand data processor folder")

    ralph_file.to_excel(
        f"{lux_only_templates}/ralph_templates.xlsx",
        index=False)
    print("Ralph templates updated and saved in Luxottica_to_import_folder")


if __name__ == "__main__":
    try:
        get_ralph_templates()
    except Exception as e:
        print(f"{type(err).__name__}: {e}")