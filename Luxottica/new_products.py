import pandas as pd
import time
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import luxottica_backup, luxottica_item_master


def new_products():
    print("Starting New Product Luxottica file creation ")

    # Read ITEM MASTER CATALOGUE(LUXOTTICA)
    # Read Shopify-Luxottica Backup
    luxottica_file = pd.read_excel(luxottica_item_master)
    shopify_file = pd.read_excel(luxottica_backup)

    # Merge luxottica and shopify
    # Mantain only right df values == NEW PRODUCTS
    new_items = shopify_file.merge(
        luxottica_file,
        left_on="Variant Barcode",
        right_on="UPC",
        how="right",
        suffixes=("_shopify", "_looker"),
        indicator=True
    )
    mask = new_items["_merge"] == "right_only"
    new_items = new_items[mask]

    # Set Vendor column
    new_items["Vendor"] = new_items["Brand Name"].str.title()

    def shopify_vendor(row):
        if row["Vendor"] == "Oakley frame" or row["Vendor"] == "Oakley youth rx" or row[
            "Vendor"] == "Oakley youth sun" or row["Vendor"] == "Oakley Frame" or row["Vendor"] == "Oakley Youth Rx":
            return "Oakley"
        elif row["Vendor"] == "Ray-ban junior vista" or row["Vendor"] == "Ray-ban vista" or row[
            "Vendor"] == "Ray-Ban Junior" or row["Vendor"] == "Ray-Ban Vista" or row[
            "Vendor"] == "Ray-Ban Junior Vista":
            return "Ray-Ban"
        elif row["Vendor"] == "Goggle&acc  snow" and row["Brand Code"] == "OZ":
            return "Oakley"
        elif row["Vendor"] == "Dolce & Gabbana Kids":
            return "Dolce & Gabbana"
        elif row["Vendor"] == "Emporio Armani Kids":
            return "Emporio Armani"
        elif row["Vendor"] == "Burberry Kids":
            return "Burberry"
        elif row["Vendor"] == "Vogue Junior Sun" or row["Vendor"] == "Vogue Junior Ophthal":
            return "Vogue Eyewear"
        elif row["Vendor"] == "Versace Kids":
            return "Versace"
        return row["Vendor"]

    new_items["Vendor"] = new_items.apply(shopify_vendor, axis=1)

    # SET VENDOR VALUES AS TITLE()
    #new_items["Vendor"] = new_items["Vendor"].str.title()

    # def get_correct_vendor_name(row):
    #     match row["Vendor"]:
    #         case "Dolce & gabbana":
    #             return "Dolce & Gabbana"
    #         case "Emporio armani":
    #             return "Emporio Armani"
    #         case "Giorgio armani":
    #             return "Giorgio Armani"
    #         case "Michael kors":
    #             return "Michael Kors"
    #         case "Miu miu":
    #             return "Miu Miu"
    #         case "Prada linea rossa":
    #             return "Prada Linea Rossa"
    #         case "Ray-ban":
    #             return "Ray-Ban"
    #         case "Vogue":
    #             return "Vogue Eyewear"
    #         case _:
    #             return row["Vendor"]
    # new_items["Vendor"] = new_items.apply(get_correct_vendor_name, axis = 1)

    # Set collection
    new_items["Type_shopify"] == new_items["Collection"].str.title()

    def ski_and_snowboard_goggles_type(row):
        if row["Collection"] == "Goggles&Helmets":
            return "Ski & Snowboard Goggles"
        return row["Collection"]

    new_items["Type_shopify"] = new_items.apply(ski_and_snowboard_goggles_type, axis=1)

    def eyewear_accessories_templates(row):
        if row["Collection"] == "Eyewear Accessories":
            return "product-noindex"
        return row["Template Suffix"]

    new_items["Template Suffix"] = new_items.apply(eyewear_accessories_templates, axis=1)

    mask = new_items["Type_shopify"].isin([
        "Sunglasses", "Eyeglasses", "Sunglasses Kids", "Eyeglasses Kids", "Ski & Snowboard Goggles"
    ])
    new_items = new_items[mask]

    # Set Title
    def get_title(row):
        brand = row["Brand Name"].title()
        if row["Model Code"].startswith("0"):
            model_code = row["Model Code"].replace("0", "", 1)
        else:
            model_code = row["Model Code"].replace("A", "", 1)
        color_code = row["Color Code"]
        if pd.notna(row["Model Name Description"]):
            product_name = row["Model Name Description"].title()
            return f"{brand} {product_name} {model_code} {color_code}"
        else:
            return f"{brand} {model_code} {color_code}"

    new_items["Title"] = new_items.apply(get_title, axis=1)

    # Oakley ski goggles title
    # Replace "Goggle&acc  snow" with "Oakley"
    def oakley_ski_goggles_title(row):
        if row["Title"].startswith("Goggle&acc  snow"):
            oakley_goggles = row["Title"].replace("Goggle&acc  snow", "Oakley")
            return oakley_goggles
        return row["Title"].title()

    new_items["Title"] = new_items.apply(oakley_ski_goggles_title, axis=1)

    # Set tags
    # def get_tags(row):
    #     """Generate tags for a product based on various columns."""
    #     # Initialize tags_list to store individual tags
    #     tags_list = []
    #     # Extract brand name from row, capitalize it, and add to tags_list
    #     # brand = row["Brand Name"].capitalize()
    #     brand = row["Vendor"]
    #     tags_list.append(brand)
    #     # Check if 'Model Name Description' is available; capitalize if present, otherwise set as empty string
    #     if pd.notna(row["Model Name Description"]):
    #         product_name = row["Model Name Description"].title()
    #     else:
    #         product_name = ""
    #     # Extract and modify 'Model Code': if it starts with '0', remove the first '0'; if it starts with 'A', remove 'A'
    #     if row["Model Code"].startswith("0"):
    #         model_code = row["Model Code"].replace("0", "", 1)
    #     else:
    #         model_code = row["Model Code"].replace("A", "", 1)
    #     # Add 'Model Code' and 'Color Code' to tags_list
    #     color_code = row["Color Code"]
    #     tags_list.append(model_code)
    #     tags_list.append(color_code)
    #     # If product_name is not empty, add it to tags_list
    #     if product_name:
    #         tags_list.append(product_name)
    #     # If 'Shape' column is available and not null, add its value to tags_list
    #     if pd.notna(row["Shape"]):
    #         tags_list.append(row["Shape"])
    #     # Check 'Collection' type: if "Sunglasses", "Eyeglasses" or "Snow Goggles", add to tags_list accordingly
    #     collection = row.get("Collection", "")
    #     if collection == "Sunglasses":
    #         tags_list.append("Sunglasses")
    #     elif collection == "Eyeglasses":
    #         tags_list.append("Eyeglasses")
    #     elif collection == "Goggles&Helmets":
    #         tags_list.append("Ski & Snowboard Goggles")
    #     # Check 'Polarized' column: if marked with "X", add "Polarized" to tags_list
    #     if row["Polarized"] == "X":
    #         tags_list.append("Polarized")
    #     # Check 'Photochromic' column: if marked with "X", add "Photochromic" to tags_list
    #     if row["Photochromic"] == "X":
    #         tags_list.append("Photochromic")
    #     # If 'Best Seller' column has "X", add "Best-seller" tag to tags_list
    #     if row.get("Best Seller", "") == "X":
    #         tags_list.append("Best Seller")
    #     # If 'New' column has "X", add "New" tag to tags_list
    #     if row.get("New", "") == "X":
    #         tags_list.append("New")
    #     # If 'ADV' column has "X", add "ADV" tag to tags_list
    #     if row.get("ADV", "") == "X":
    #         tags_list.append("ADV")
    #     if row["Collection"] == "Sunglasses Kids" or row["Collection"] == "Eyeglasses Kids":
    #         tags_list.append("Kids")
    #     # Join all tags in tags_list with a comma separator and return the final tag string
    #     return ", ".join(tags_list)
    #
    # new_items["Tags"] = new_items.apply(get_tags, axis=1)

    # Set Variant SKU
    def get_variant_sku(row):
        model_code = row["Model Code"]
        color_code = row["Color Code"]
        size = row["Size"]
        if model_code.startswith('0'):
            # Rimuovi il primo carattere se è '0'
            model_code = model_code[1:]
        elif model_code.startswith('A'):
            # Rimuovi il primo carattere se è 'A'
            model_code = model_code[1:]
        return f"{model_code} {color_code} {size}"

    new_items["Variant SKU"] = new_items.apply(get_variant_sku, axis=1)

    # Set for WHO
    new_items["Metafield: my_fields.for_who [single_line_text_field]"] = new_items["Gender"]

    def for_kids(row):
        if row["Type_shopify"] == "Sunglasses Kids" or row["Type_shopify"] == "Eyeglasses Kids":
            return "Kids"
        return row["Metafield: my_fields.for_who [single_line_text_field]"]

    new_items["Metafield: my_fields.for_who [single_line_text_field]"] = new_items.apply(for_kids, axis=1)

    # Set size-bridge-temples
    def get_size_bridge_temples(row):
        size = row["Size"]

        # Handle NaN values in Bridge Size and Temple Length
        bridge = row["Bridge Size"]
        if pd.notna(bridge):
            bridge = int(bridge)
        else:
            bridge = 0  # Default value for missing bridge size

        temples = row["Temple Length"]
        if pd.notna(temples):
            temples = int(temples)
        else:
            temples = 0  # Default value for missing temple length
        return f"{size}-{bridge}-{temples}"

    new_items["Metafield: my_fields.product_size [single_line_text_field]"] = new_items.apply(get_size_bridge_temples,
                                                                                              axis=1)

    # Set all shopify columns with Luxottica values
    # Fill manually others shopify columns
    new_items["Command"] = "Merge"
    new_items["Tags Command"] = "Replace"
    new_items["Status"] = "Active"
    new_items["Published"] = "TRUE"
    new_items["Template Suffix"] = "Default product"
    new_items["Option1 Name"] = "Size"
    new_items["Option1 Value"] = new_items["Size"]
    new_items["Variant Compare At Price"] = new_items["Suggested Retail Price"]
    new_items["Variant Price"] = new_items["Variant Compare At Price"]
    new_items[["Variant Inventory Qty", "Inventory Available: +39 05649689443"]] = 0
    new_items["Metafield: my_fields.lens_color [single_line_text_field]"] = new_items["Lens Color"]
    new_items["Metafield: my_fields.frame_color [single_line_text_field]"] = new_items["Front Colour"]
    new_items["Metafield: my_fields.frame_shape [single_line_text_field]"] = new_items["Shape"]
    new_items["Metafield: my_fields.frame_material [single_line_text_field]"] = new_items["Front Material"]
    new_items["Metafield: my_fields.gtin1 [single_line_text_field]"] = new_items["Variant Barcode"]
    new_items["Variant Barcode"] = new_items["UPC"]
    new_items["Variant Cost"] = new_items["Wholesale Price"].str.replace(',', '.')

    # Set prices
    # "Replace ',' with '.'"
    new_items["Variant Compare At Price"] = new_items["Variant Compare At Price"].str.replace(",", ".")
    new_items["Variant Price"] = new_items["Variant Price"].str.replace(",", ".")
    new_items["Variant Cost"] = new_items["Variant Cost"].str.replace(",", ".")

    # Insert publishe scope column to sell produts through all sales channel
    new_items["Published Scope"] = "global"

    # Mantein only columns necessary to Shopify import
    new_items = new_items[[
        "ID", "Handle", "Command", "Title", "Body HTML", "Vendor", "Type_shopify", "Tags", "Tags Command",
        "Status", "Published", "Published Scope", "Template Suffix", "URL", "Variant ID", "Variant SKU",
        "Variant Barcode",
        "Variant Price", "Variant Compare At Price", "Variant Cost", "Variant Inventory Qty",
        "Inventory Available: +39 05649689443", "Metafield: title_tag [string]", "Metafield: description_tag [string]",
        "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]",
        "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]",
        "Metafield: my_fields.product_size [single_line_text_field]",
        "Metafield: my_fields.for_who [single_line_text_field]",
        "Metafield: my_fields.gtin1 [single_line_text_field]",
        "Option1 Name", "Option1 Value",
        "Metafield: custom.main_frame_shape [single_line_text_field]",
        "Metafield: custom.main_frame_material [single_line_text_field]",
        "Metafield: custom.main_frame_color [single_line_text_field]",
        "Metafield: custom.main_lens_color [single_line_text_field]",
        "Metafield: custom.main_lens_technology [single_line_text_field]",
        "Metafield: custom.main_size [single_line_text_field]"
    ]]

    # Rename Type_shopify with Type
    new_items = new_items.rename(columns={"Type_shopify": "Type"})

    # Create a txt file with all barcode to import on Luxottica to get pictures
    print("Create a txt file with all barcode to import on Luxottica to get pictures")
    new_items["Variant Barcode"] = new_items["Variant Barcode"].apply(
        lambda x: str(int(float(x))) if pd.notna(x) and x != "" else "")

    # Imposta il numero di barcode per file
    barcode_per_file = 248
    total_barcodes = len(new_items)
    file_index = 1

    # Itera attraverso i barcode in blocchi
    for i in range(0, total_barcodes, barcode_per_file):
        # Estrai un blocco di 250 barcode
        barcode_chunk = new_items["Variant Barcode"].iloc[i:i + barcode_per_file]

        # Salva il blocco in un file
        filename = f"barcode{file_index}.txt"
        with open(filename, "w") as file:
            for barcode in barcode_chunk:
                if barcode:  # Scrivi solo se non è vuoto
                    file.write(f"{barcode.strip()}\n")

        print(f"{filename} created!.")
        file_index += 1
    print("txt files are create successfully!")

    # Split brands and save them on own folder
    # Save all file on this directory
    for brand in new_items["Vendor"].unique():
        try:
            mask = new_items["Vendor"] == brand
            brand_file = new_items[mask]
            brand_file = brand_file.sort_values(by="Title")
            brand_file.to_excel(
                f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/{brand}/{brand}_IMG.xlsx",
                index=False)
            print(f"{brand} brand saved successfully on own folder.")
            brand_file.to_excel(
                f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/New/{brand}_NEW.xlsx",
                index=False)
            print(f"{brand} brand saved successfully on NEW folder.")
            time.sleep(1)
        except Exception as err:
            print("Something went wrong during saving files.")
            print(f"{type(err).__name__}: \n {err}")

    new_items.to_excel("Luxottica_New_Products.xlsx", index=False)


if __name__ == "__main__":
    try:
        new_products()
    except Exception as err:
        print(f"{type(err).__name__}: {err}")
