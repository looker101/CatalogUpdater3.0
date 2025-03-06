import time
import pandas as pd
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths/")
from luxottica_paths import luxottica_to_import_folder, dolce_gabbana_update, lux_only_templates


def get_dolce_gabbana_template():
    # dolce_gabbana_file = pd.read_excel(
    # "C:\\Users\\miche\\Desktop\\myVenv\\Catalogo\\Luxottica\\Dolce & gabbana\\dolce_gabbana_ok.xlsx")

    dolce_gabbana_file = pd.read_excel(dolce_gabbana_update)

    dolce_gabbana_file = dolce_gabbana_file[[
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

    dolce_gabbana_file["Metafield: my_fields.for_who [single_line_text_field]"] = dolce_gabbana_file[
        "Metafield: my_fields.for_who [single_line_text_field]"].fillna("")

    dolce_gabbana_file["Metafield: my_fields.frame_color [single_line_text_field]"] = dolce_gabbana_file[
        "Metafield: my_fields.frame_color [single_line_text_field]"].fillna("")

    dolce_gabbana_file["Vendor"] = "Dolce & Gabbana"

    # Remove "0" from Variant SKU
    def remove_0_from_variant_sku(row):
        if row["Variant SKU"].startswith("0"):
            return row["Variant SKU"].replace("0", "", 1)
        return row["Variant SKU"]

    dolce_gabbana_file["Variant SKU"] = dolce_gabbana_file.apply(remove_0_from_variant_sku, axis=1)

    def getMetaTitle(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "Men and Women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Kids":
            return f"{brand} {model_code} {color_code} {frame_color} {style}"
        return f"{brand} {model_code} {color_code} {frame_color} {style} for {gender}"

    dolce_gabbana_file["Metafield: title_tag [string]"] = dolce_gabbana_file.apply(getMetaTitle, axis=1)

    def getMetaDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"]
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()

        return f"Buy the new {brand} {model_code} {color_code} {style} at a bargain price. This super stylish, unique {frame_color} model is the ideal choice for {gender} | FREE SHIPPING |"

    dolce_gabbana_file["Metafield: description_tag [string]"] = dolce_gabbana_file.apply(getMetaDescription, axis=1)

    def getProductDescription(row):
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        style = row["Type"]
        gender = ""
        if row["Metafield: my_fields.for_who [single_line_text_field]"] == "Unisex":
            gender = "men and women"
        else:
            gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        eye = f"""<p><strong>{brand} {style} </strong><span style="font-weight: 400;">are timeless works of art. Superior quality, imaginative designs, cinematographic elegance, fine details: a lesson in style and confidence.</span></p>
    <p><span style="font-weight: 400;">This super stylish, one-of-a-kind</span><strong> gold </strong><span style="font-weight: 400;">model was carefully designed by </span><strong>{brand}</strong><span style="font-weight: 400;"> and manufactured to perfection by world leading eyewear producer Luxottica. An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the</span><strong> {model_code} {color_code} {frame_color}</strong><span style="font-weight: 400;"> are the ultimate show-stoppers.</span></p>
    <p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><a href="/collections/dolce-gabbana-eyeglasses"><span style="font-weight: 400;">{brand} {style} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>
        """

        sun = f"""<p><strong>{brand} {style} </strong><span style="font-weight: 400;">are timeless works of art. Superior quality, imaginative designs, cinematographic elegance, fine details: a lesson in style and confidence.</span></p>
    <p><span style="font-weight: 400;">This super stylish, one-of-a-kind</span><strong> gold </strong><span style="font-weight: 400;">model was carefully designed by </span><strong>{brand}</strong><span style="font-weight: 400;"> and manufactured to perfection by world leading eyewear producer Luxottica. An ideal choice for </span><strong>{gender}</strong><span style="font-weight: 400;">, the</span><strong> {model_code} {color_code} {frame_color}</strong><span style="font-weight: 400;"> are the ultimate show-stoppers.</span></p>
    <p><span style="font-weight: 400;">Check out hundreds of new models and designs in the latest </span><a href="/collections/dolce-gabbana-sunglasses"><span style="font-weight: 400;">{brand} {style} 2025</span></a><span style="font-weight: 400;"> collection!</span></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    dolce_gabbana_file["Body HTML"] = dolce_gabbana_file.apply(getProductDescription, axis=1)

    # DROP ROW WITHOUT VALUES ON LENS COLOR COLUM
    dolce_gabbana_file = dolce_gabbana_file.dropna(axis=0, how='any',
                                                   subset=['Metafield: my_fields.lens_color [single_line_text_field]'])

    # SORT
    dolce_gabbana_file = dolce_gabbana_file.sort_values(by="Handle")

    dolce_gabbana_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Dolce & gabbana/Dolce&Gabbana_templates.xlsx",
        index=False)
    dolce_gabbana_file.to_excel(
        "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Dolce & Gabbana/Dolce&Gabbana_templates.xlsx",
        index=False)
    print("Dolce & Gabbana updated and saved on Dolce & Gabbana folder")
    time.sleep(1)

    # dolce_gabbana_file.to_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor/Dolce & gabbana.xlsx", index=False)
    # print("Dolce & Gabbana updated and saved on Brand data processor folder")
    # time.sleep(1)

    dolce_gabbana_file.to_excel(f"{lux_only_templates}/Dolce&Gabbana_templates.xlsx", index=False)
    print("Dolce & Gabbana templates updated and saved in Luxottica_to_import_folder")
    time.sleep(1)


if __name__ == "__main__":
    get_dolce_gabbana_template()
