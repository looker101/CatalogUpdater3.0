import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import luxottica_to_import_folder, oakley_update, lux_only_templates


def get_oakley_templates():
    # Read oakley file
    oakley_file = pd.read_excel(oakley_update)
    # oakley_file = oakley_file.dropna(axis = 0, how = "any",
    # subset=["Metafield: my_fields.frame_color [single_line_text_field]"])

    oakley_file = oakley_file[[
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

    oakley_file["Vendor"] = "Oakley"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("A"):
            return row["Variant SKU"].replace("A", "", 1)
        return row["Variant SKU"]

    oakley_file["Variant SKU"] = oakley_file.apply(remove_0_from_variant_sku, axis=1)

    # def get_kids_tag(row):
    #     if row["Type"] == "Eyeglasses Kids" or row["Type"] == "Sunglasses Kids":
    #         return "Kids"
    #     return row["Metafield: my_fields.for_who [single_line_text_field]"]
    #
    # oakley_file["Metafield: my_fields.for_who [single_line_text_field]"] = oakley_file.apply(get_kids_tag, axis = 1)

    # Create metaTitle
    # {Brand} {Product Name} {model_code} {color_code} {frame_color} for {geneder} | Lookeronline
    def getMetaTitle(row):
        item_title = row["Title"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        item_type = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{item_title} {frame_color} {item_type}"
        return f"{item_title} {frame_color} {item_type} for {gender}"

    oakley_file["Metafield: title_tag [string]"] = oakley_file.apply(getMetaTitle, axis=1)

    # Create Meta Description
    def getMetaDescription(row):
        brand = row["Vendor"]
        product_name = row["Title"].split()[1]
        model_code = row["Title"].split()[2]
        color_code = row["Title"].split()[3]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"].lower()
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()

        return f"Buy the new {brand} {product_name} {model_code} {color_code} {style} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    oakley_file["Metafield: description_tag [string]"] = oakley_file.apply(getMetaDescription, axis=1)

    # Create product description (Body HTML)
    def getProductDescription(row):
        brand = row["Vendor"]
        product_name = row["Title"].split()[1]
        model_code = row["Title"].split()[2]
        color_code = row["Title"].split()[3]
        if pd.isna(row["Metafield: my_fields.frame_color [single_line_text_field]"]):
            frame_color = ""
        else:
            frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"].lower()
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        sun = f"""<p><span style="font-weight: 400;">With a focus on eye protection, high-performance and great fit,</span><strong> {brand} {style}</strong><span style="font-weight: 400;"> will take your game to the next level.</span></p>
    <p><span style="font-weight: 400;">The</span> <strong>Oakley </strong><strong>{product_name} {model_code} {color_code} </strong><span style="font-weight: 400;">is the perfect choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This stylish and sporty </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model was designed and manufactured by world leading eyewear manufacturer Luxottica to meet Oakley top-quality standards.</span></p>
    <p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><span style="font-weight: 400;"> <a href="/collections/oakley-sunglasses" target="_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">With a focus on eye protection, high-performance and great fit,</span><strong> {brand} {style}</strong><span style="font-weight: 400;"> will take your game to the next level.</span></p>
    <p><span style="font-weight: 400;">The</span> <strong>Oakley </strong><strong>{product_name} {model_code} {color_code} </strong><span style="font-weight: 400;">is the perfect choice for</span><strong> {gender}</strong><span style="font-weight: 400;">.</span> <span style="font-weight: 400;">This stylish and sporty </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model was designed and manufactured by world leading eyewear manufacturer Luxottica to meet Oakley top-quality standards.</span></p>
    <p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><span style="font-weight: 400;"> <a href="/collections/oakley-eyeglasses" target="_blank">{brand} {style} 2025</a></span><span style="font-weight: 400;"> collection!</span></p>"""

        goggles = f"""<p><span style="font-weight: 400;">Discover the ultimate blend of style and performance with </span><strong>{brand} {style}</strong><span style="font-weight: 400;">. Trusted by athletes and outdoor enthusiasts, these goggles are crafted for peak functionality in challenging alpine conditions. Designed with precision and comfort in mind, Oakley snow goggles boast an ergonomic fit and cutting-edge technology.</span></p>
<h2>&nbsp;</h2>
<p><span style="font-weight: 400;">The distinctive </span><strong>{frame_color}</strong><span style="font-weight: 400;"> model showcases Oakley's commitment to excellence, providing unparalleled performance on the slopes. Ideal for everyone seeking top-tier protection, the </span><strong>{product_name} {model_code} {color_code}</strong><span style="font-weight: 400;"> promises to elevate your skiing experience with Oakley's renowned quality.</span></p>
<h2>&nbsp;</h2>
<p><span style="font-weight: 400;">Check out all the latest models and designs in the new <a href="/collections/oakley-ski-goggles" target="_blank">{brand} {style} 2025</a> collection.</span></p>"""

        match row["Type"]:
            case "Sunglasses":
                return sun
            case "Ski & Snowboard Goggles":
                return goggles
            case _:
                return eye

        # if row["Type"] == "Sunglasses":
        #     return sun
        # return eye

    oakley_file["Body HTML"] = oakley_file.apply(getProductDescription, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    oakley_file = oakley_file.dropna(axis=0, how='any',
                                     subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    oakley_file = oakley_file.sort_values(by="Handle")

    # Saving
    oakley_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Oakley/Oakley_Templates.xlsx",
        index=False)
    print("Oakley updated and saved on Oakley folder")

    # oakley_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Oakley.xlsx")
    # print("Oakley updated and saved on Brand data processor folder")

    oakley_file.to_excel(
        f"{lux_only_templates}/Oakley_templates.xlsx",
        index=False)
    print("Oakley templates updated and saved in Luxottica_to_import_folder")


if __name__ == "__main__":
    get_oakley_templates()
