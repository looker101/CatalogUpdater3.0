import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from kering_paths import gucci_folder, gucci_excel, gucci_for_temp, templates

def gucci_templates_updater():
    gucci_file = pd.read_excel(gucci_excel)

    gucci_file = gucci_file[[
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

    # Metatitle
    def meta_title(row):
        """brand model_code color_code frame_color type for gender """
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        category = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        return f"{brand} {model_code} {color_code} {frame_color} {category} for {gender}"
    gucci_file["Metafield: title_tag [string]"] = gucci_file.apply(meta_title, axis = 1)

    # Meta Description
    def meta_description(row):
        """New brand model_code color_code category on sale! ✓ Express Shipping ✓ 100% Original | LookerOnline"""
        brand = row["Vendor"]
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        category = row["Type"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]
        return f"New {brand} {model_code} {color_code} {category} for {gender} on sale! ✓ Express Shipping ✓ 100% Original | LookerOnline"
    gucci_file["Metafield: description_tag [string]"] = gucci_file.apply(meta_description, axis = 1)

    # Product Description
    def product_description(row):
        model_code = row["Variant SKU"].split()[0]
        color_code = row["Variant SKU"].split()[1]
        category = row["Type"]
        frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
        gender = row["Metafield: my_fields.for_who [single_line_text_field]"]

        sun = f"""<p align="justify">Nothing says style like a pair of <strong>Gucci</strong>. Eclectic, romantic, psychedelic, timeless: <strong>Gucci</strong> <strong>eyewear</strong> is simply unique.</p>
    <p align="justify">The<strong>  {model_code} {color_code} {category}</strong> are the perfect choice for <strong>{gender}</strong>. This super stylish, elegant, one-of-a-kind<strong> {frame_color} </strong>model with<strong> smoke</strong> lenses is as good as it gets. Imagined by the world's top fashion designers and manufactured to perfection by luxury powerhouse Kering, these <strong>Gucci sunglasses</strong> are a thing of absolute beauty.</p>
    <p align="justify">Check out hundreds of new models and designs in the latest <a title="LookerOnline | Gucci Sunglasses" href="/collections/gucci-sunglasses">2025 Gucci sunglasses</a> collection!</p>
    <p align="justify">&nbsp;</p>"""

        eye = f"""<p align="juistify">Nothing says style like a pair of <strong>Gucci</strong>. Eclectic, romantic, psychedelic, timeless: <strong>Gucci eyeglasses</strong> are simply unique.
        <br /><br />The <strong>Gucci {model_code} {color_code}</strong> is the perfect choice for <strong>{gender}</strong>. This super stylish, elegant, one-of-a-kind, <strong>{frame_color}</strong> model is as good as it gets. 
        Imagined by the world's top fashion designers and manufactured to perfection by luxury powerhouse Kering, these eyeglasses are a thing of absolute beauty. <br /><br />Check out hundreds of new models and designs in the latest <a href="/collections/gucci-eyeglasses" target="_blank" rel="noopener">Gucci glasses 2025 collection! </a></p>"""

        if row["Type"] == "Sunglasses":
            return sun
        return eye

    gucci_file["Body HTML"] = gucci_file.apply(product_description, axis = 1)

    # gucci_file = gucci_file.drop(columns=["Metafield: description_tag [single_line_text_field]"])
    # if 'Unnamed: 0' in gucci_file.columns:
    #     gucci_file = gucci_file.drop(columns=['Unnamed: 0'])

    # gucci_file = gucci_file[[
    #     "Variant SKU", "Variant Barcode", "Variant Price", "Variant Compare At Price", "ID", "Handle", "Title",
    #     "Command", "Body HTML", "Vendor", "Type", "Tags", "Tags Command", "Status", "Template Suffix",
    #     "URL", "Total Inventory Qty", "Variant ID", "Option1 Name", "Option1 Value",
    #     "Inventory Available: +39 05649689443", "Metafield: title_tag [string]", "Metafield: description_tag [string]",
    #     "Metafield: my_fields.lens_color [single_line_text_field]", "Metafield: my_fields.frame_color [single_line_text_field]",
    #     "Metafield: my_fields.frame_shape [single_line_text_field]", "Metafield: my_fields.frame_material [single_line_text_field]",
    #     "Metafield: my_fields.lens_material [single_line_text_field]", "Metafield: my_fields.product_size [single_line_text_field]",
    #     "Metafield: my_fields.for_who [single_line_text_field]"
    # ]]

    gucci_file = gucci_file.drop_duplicates("Title")

    #SAVING
    gucci_file = gucci_file.sort_values(by="Title")
    gucci_file.to_excel(f"{gucci_folder}Gucci_templates_ok.xlsx", index=False)
    gucci_file.to_excel(f"{templates}/Gucci_templates_ok.xlsx", index=False)

if __name__ == "__main__":
    try:
        print("Starting Gucci templates updater")
        gucci_templates_updater()
        print("Gucci templates updated succesfully! \n Closing Gucci templates.")
    except Exception as err:
        print(f"Gucci not updated due this error \n {type(err).__name__}: {err}")
