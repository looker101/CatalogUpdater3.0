import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, prada_update, lux_only_templates

def get_prada_templates():

    prada_file = pd.read_excel(prada_update)
    #prada_file = prada_file.dropna(axis = 0, how = "any",
                               # subset=["Metafield: my_fields.frame_color [single_line_text_field]"])
    
    prada_file = prada_file[[
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

    prada_file["Vendor"] = "Prada"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    prada_file["Variant SKU"] = prada_file.apply(remove_0_from_variant_sku, axis=1)

    # Create metaTitle
    # {Brand} {model_code} {color_code} {frame_color} for {geneder}
    def getMetaTitle(row):
        brand = row["Vendor"]
        pr = row["Variant SKU"].split()[0]
        model_code = row["Variant SKU"].split()[1]
        color_code = row["Variant SKU"].split()[2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {pr} {model_code} {color_code} {style} {frame_color}"
        return f"{brand} {pr} {model_code} {color_code} {style} {frame_color} for {gender}"

    prada_file["Metafield: title_tag [string]"] = prada_file.apply(getMetaTitle, axis = 1)

    # Create MetaDescription
    def getMetaDescription(row):
        brand = row["Vendor"]
        pr = row["Variant SKU"].split()[0]
        model_code = row["Variant SKU"].split()[1]
        color_code = row["Variant SKU"].split()[2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
        style = row["Type"].lower()

        return f"Buy the new {brand} {style} {pr} {color_code} {model_code} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    prada_file["Metafield: description_tag [string]"] = prada_file.apply(getMetaDescription, axis = 1)

    # Create Product Description
    def getProductDescription(row):
        brand = row["Vendor"]
        pr = row["Variant SKU"].split()[0]
        model_code = row["Variant SKU"].split()[1]
        color_code = row["Variant SKU"].split()[2]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        style = row["Type"]

        sun = f"""<p><span style="font-weight: 400;">Innovative, refined, ageless, unique: </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> is arguably the most original and creative we have in our store. Imagined by the world's top luxury designers and manufactured to perfection by leading producer Luxottica, </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> are the ultimate fashion accessory.</span></p>
    <p><span style="font-weight: 400;">The </span><strong>{brand} {pr} {model_code} {color_code} </strong><span style="font-weight: 400;">model, a one-of-a-kind, elegant, </span><strong>{frame_color} </strong><span style="font-weight: 400;">frame is the perfect choice for </span><strong>{gender}</strong><span style="font-weight: 400;">.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><span style="font-weight: 400;"><a href="/collections/prada-sunglasses" target = "_blank">{brand} {style} 2025</a><span style="font-weight: 400;"> collection!</span></p>"""

        eye = f"""<p><span style="font-weight: 400;">Innovative, refined, ageless, unique: </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> is arguably the most original and creative we have in our store. Imagined by the world's top luxury designers and manufactured to perfection by leading producer Luxottica, </span><strong>{brand} {style}</strong><span style="font-weight: 400;"> are the ultimate fashion accessory.</span></p>
    <p><span style="font-weight: 400;">The </span><strong>{brand} {pr} {model_code} {color_code} </strong><span style="font-weight: 400;">model, a one-of-a-kind, elegant, </span><strong>{frame_color} </strong><span style="font-weight: 400;">frame is the perfect choice for </span><strong>{gender}</strong><span style="font-weight: 400;">.</span></p>
    <p><span style="font-weight: 400;">Check out all the latest models and designs in the new </span><span style="font-weight: 400;"><a href="/collections/prada-eyesses" target = "_blank">{brand} {style} 2025</a><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    prada_file["Body HTML"] = prada_file.apply(getProductDescription, axis = 1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    prada_file = prada_file.dropna(axis = 0, how='any', subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    prada_file = prada_file.sort_values("Handle")
    
    # Saving
    prada_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Prada/Prada_Template.xlsx", index = False)
    print("Prada updated and saved on Prada folder")

    # prada_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Prada.xlsx", index = False)
    # print("Prada updated and saved on Brand data processor folder")

    prada_file.to_excel(
        f"{lux_only_templates}/Prada_templates.xlsx",
        index=False)
    print("Prada templates updated and saved in Luxottica_to_import_folder")
    
if __name__ == "__main__":
    get_prada_templates()