import pandas as pd
import time
import sys

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import luxottica_backup, luxottica_item_master

shopify_file = pd.read_excel(luxottica_backup)
luxottica_file = pd.read_excel(luxottica_item_master)

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

# RENAME TYPE_LOOKER WITH TYPE
new_items = new_items.rename(columns={"Type_shopify":"Type"})

# SET VENDOR
# ALL VENDOR VALUE MUST HAVE ONLY BRAND NAME AS TITLE()
new_items["Vendor"] = new_items["Brand Name"].str.title()

def shopify_vendor(row):
    if row["Vendor"] == "Oakley frame" or row["Vendor"] == "Oakley youth rx" or row[
        "Vendor"] == "Oakley youth sun" or row["Vendor"] == "Oakley Frame" or row["Vendor"] == "Oakley Youth Rx" or row[
        "Vendor"] == "Oakley Youth Sun":
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
    elif row["Vendor"] == "Vogue Junior Sun" or row["Vendor"] == "Vogue Junior Ophthal" or row["Vendor"] == "Vogue":
        return "Vogue Eyewear"
    elif row["Vendor"] == "Versace Kids":
        return "Versace"
    return row["Vendor"]


new_items["Vendor"] = new_items.apply(shopify_vendor, axis=1)

new_items["Command"] = "MERGE"
#new_items["Tags"] = "New"
new_items["Tags Command"] = "REPLACE"
new_items["Status"] = "ACTIVE"
new_items["Template Suffix"] = "Default product"
new_items["Option1 Name"] = "Size"
new_items["Option1 Value"] = new_items["Width Lens"]
new_items["Variant Compare At Price"] = new_items["Wholesale Price"]
new_items["Variant Price"] = new_items["Suggested Retail Price"]
new_items[["Variant Inventory Qty", "Inventory Available: +39 05649689443"]] = 0
new_items["Type"] = new_items["Collection"]
new_items["Metafield: my_fields.lens_color [single_line_text_field]"] = new_items["Lens Color"]
new_items["Metafield: my_fields.frame_color [single_line_text_field]"] = new_items["Front Colour"]
new_items["Metafield: my_fields.frame_shape [single_line_text_field]"] = new_items["Shape"]
#new_items["Metafield: my_fields.for_who [single_line_text_field]"] = new_items["Gender"]
new_items["Metafield: my_fields.frame_material [single_line_text_field]"] = new_items["Front Material"]
new_items["Variant Barcode"] = new_items["UPC"]

# SET ITEMS TITLE
def get_items_title(row):
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
new_items["Title"] = new_items.apply(get_items_title, axis=1)

# SET ITEMS SKU
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

# SET ITEMS TYPE
def get_items_type(row):
    items_type = str(row["Collection"]).strip().title()
    if pd.notna(items_type):
        if row["Collection"] == "Goggles&Helmets":
            return "Ski & Snowboard Goggles"
        return row["Collection"]
new_items["Type"] = new_items.apply(get_items_type, axis=1)

# KEEP ITEMS TYPE -> THESE TYPE ARE LUXOTTICA DEFAULT
mask_type = new_items["Type"].isin(["Eyeglasses", "Eyeglasses Kids",
                                    "Sunglasses", "Sunglasses Kids",
                                    "Ski & Snowboard Goggles"])
new_items = new_items[mask_type]

# GET GENDER AND KIDS TYPE -> GET KIDS ON 'FOR WHO' FIELD THROUGHT ITEMS TYPE
def get_gender_and_kids_type(row):
    items_type = str(row["Type"]).strip().title()
    items_gender = str(row["Gender"]).strip().title()
    if "Kids" in items_type:
        return "Kids"
    return items_gender
new_items["Metafield: my_fields.for_who [single_line_text_field]"] = new_items.apply(get_gender_and_kids_type, axis = 1)


# KEEP COLUMNS
columns_to_keep = [
    "ID", "Handle", "Command", "Title", "Body HTML", "Vendor", "Type", "Tags", "Tags Command", "Status",
    "Template Suffix", "URL", "Image Src", "Variant ID", "Option1 Name", "Option1 Value", "Variant SKU",
    "Variant Barcode", "Variant Price", "Variant Compare At Price", "Variant Inventory Qty",
    "Inventory Available: +39 05649689443", "Metafield: my_fields.for_who [single_line_text_field]",
    "Metafield: my_fields.lens_color [single_line_text_field]",
    "Metafield: my_fields.frame_color [single_line_text_field]",
    "Metafield: my_fields.frame_shape [single_line_text_field]",
    "Metafield: my_fields.frame_material [single_line_text_field]",
    "Metafield: my_fields.product_size [single_line_text_field]"
]
new_items = new_items[columns_to_keep]

# =========================SAVE======================

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
        #brand_file.to_excel(
        #    f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/New/{brand}_NEW.xlsx",
        #    index=False)
        #print(f"{brand} brand saved successfully on NEW folder.")
        time.sleep(1)
    except Exception as err:
        print("Something went wrong during saving files.")
        print(f"{type(err).__name__}: \n {err}")

new_items.to_excel("Luxottica_New_Products.xlsx", index=False)


# if __name__ == "__main__":
#     try:
#         new_products()
#     except Exception as err:
#         print(f"{type(err).__name__}: {err}")
