import pandas as pd
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from marchon_paths import FTP_MARCHON_CSV, MARCHON_BACKUP, marchon_new_item_log, new_items, TO_IMPORT_FOLDER

# all new products will be inserted with quantity 0. All products will be updated with new catalog updating

marchon = pd.read_csv(FTP_MARCHON_CSV)
shopify = pd.read_excel(MARCHON_BACKUP)

def get_marchon_new_products():

    # Merge on UPC SKU and Variant Barcode
    merged_file = shopify.merge(marchon,
                                left_on="Variant Barcode",
                                right_on="UPC SKU",
                                how="outer",
                                indicator=True)

    # lascio solo i brand che sono disponibili  sul sito (ferragamo, lacoste, nike)
    mask = merged_file["Brand.1"].isin(["LACOSTE", "FERRAGAMO", "NIKE", "DRAGON"])
    merged_file = merged_file[mask]
    # voglio solo i prodotti nel file marchon (DX)
    mask1 = merged_file["_merge"] == "right_only"
    merged_file = merged_file[mask1]

    # setto tutto come stringhe per rendere possibile la concatenazione
    merged_file["Material"] = merged_file["Material"].astype(str)
    merged_file["Color code"] = merged_file["Color code"].astype(str).str.replace('.0', '')
    merged_file["LENS WIDTH"] = merged_file["LENS WIDTH"].astype(str).str.replace('.0', '')
    merged_file["BRIDGE"] = merged_file["BRIDGE"].astype(str).str.replace('.0', '')
    merged_file["TEMPLE"] = merged_file["TEMPLE"].astype(str).str.replace('.0', '')

    # compilo le colonne shopify
    merged_file["Vendor"] = merged_file["Brand.1"]
    merged_file["Variant SKU"] = merged_file["Material"] + ' ' + merged_file["Color code"]+ ' ' + merged_file["LENS WIDTH"]
    merged_file["Variant Barcode"] = merged_file["UPC SKU"]
    merged_file["Variant Compare At Price"] = merged_file["RRP"]
    merged_file["Variant Price"] = merged_file["RRP"]
    merged_file["Metafield: my_fields.lens_color [single_line_text_field]"] = merged_file["LENS COLOR"]
    merged_file["Metafield: my_fields.frame_color [single_line_text_field]"] = merged_file["FRAME COLOR"]
    merged_file["Metafield: my_fields.frame_shape [single_line_text_field]"] = merged_file["Shape"]
    merged_file["Metafield: my_fields.frame_material [single_line_text_field]"] = merged_file["FRAME MATERIAL"]
    merged_file["Option1 Value"] = merged_file["LENS WIDTH"]
    merged_file["Variant Inventory Qty"] = 0
    merged_file["Inventory Available: +39 05649689443"] = 0
    merged_file["Tags Command"] = "REPLACE"
    merged_file["Status"] = "ACTIVE"
    merged_file["Template Suffix"] = "Default product"
    merged_file["Option1 Name"] = "Size"
    merged_file["COMMAND"] = "Merge"

    # rinomino i vendor da upper a title
    merged_file["Vendor"] = merged_file["Vendor"].str.title()

    # TITLE
    def get_title_nike_new(row):
        brand = str(row["Material.1"]) if pd.notna(row["Material.1"]) else ""
        vendor = str(row["Vendor"]) if pd.notna(row["Vendor"]) else ""
        color_code = str(row["Color code"]) if pd.notna(row["Color code"]) else ""

        if vendor == "Nike" or vendor == "NIKE":
            brand_splitted = brand.split()

            new_title = []

            for stringa in brand_splitted:
                if stringa.isalpha():
                    new_title.append(stringa.title())
                elif stringa.isdigit():
                    new_title.append(stringa.upper())
                else:
                    new_title.append(stringa.upper())

            new_title.append(color_code)

            return " ".join(new_title)
        else:
            return f'{vendor.title()} {brand} {color_code}'

    merged_file["Title"] = merged_file.apply(get_title_nike_new, axis=1)

    # def get_tile(row):
    #     # Brand Model-Code Color-Code
    #     brand = row["Vendor"]
    #     model_code = row["Material"]
    #     color_code = row["Color code"]
    #     return f"{brand} {model_code} {color_code}"
    # merged_file["Title"] = merged_file.apply(get_tile, axis = 1)

    # TYPE
    def get_type(row):
        if row["External Matl Group"] == "SUN":
            return "Sunglasses"
        return "Eyeglasses"
    merged_file["Type"] = merged_file.apply(get_type, axis=1)

    # FOR WHO
    def get_for_who(row):
        if row["Gender"] == "MALE":
            return "Man"
        return "Woman"
    merged_file["Metafield: my_fields.for_who [single_line_text_field]"] = merged_file.apply(get_for_who, axis=1)

    # SIZE-BRIDGE-TEMPLES
    def get_size_bridge_temples(row):
        size = row["LENS WIDTH"]
        bridge = row["BRIDGE"]
        temples = row["TEMPLE"]
        return f"{size} - {bridge} - {temples}"
    merged_file["Metafield: my_fields.product_size [single_line_text_field]"] = merged_file.apply(get_size_bridge_temples,
                                                                                                  axis=1)
    # IMAGES
    def get_images(row):
        images_list = [
            row["Image URL"], row["Image URL.1"], row["Image URL.2"], row["Image URL.3"], row["Image URL.4"],
            row["Image URL.5"], row["Image URL.6"], row["Image URL.7"]
        ]
        image_string_list = [str(image) for image in images_list]
        return ';'.join(image_string_list)
    merged_file["Image Src"] = merged_file.apply(get_images, axis = 1)

    # TAGS
    def create_tag(row):
        tag_list = [
            str(row["Vendor"]),
            str(row["Material"]),
            str(row["Color code"]),
            "tag__new_New",
            str(row["Metafield: my_fields.frame_shape [single_line_text_field]"]),
            str(row["Metafield: my_fields.frame_color [single_line_text_field]"]),
            str(row["Metafield: my_fields.lens_color [single_line_text_field]"]),
            str(row["Metafield: my_fields.for_who [single_line_text_field]"])
        ]   # Lista per ogni riga
        return ', '.join(tag_list)
    merged_file["Tags"] = merged_file.apply(create_tag, axis=1)

    #Mantengo solo le colonne necessarie per l'import con matrixify
    merged_file = merged_file[[
        "Variant ID", "Variant SKU", "Variant Barcode", "Variant Price", "Variant Compare At Price", "Variant Inventory Qty",
        "ID", "Handle", "Tags", "Command", "Title", "Vendor", "Type", "Tags Command", "Status",
        "Template Suffix", "Option1 Name", "Option1 Value", "Image Src", "Inventory Available: +39 05649689443",
        "Metafield: title_tag [string]", "Metafield: description_tag [string]",
        "Metafield: my_fields.lens_color [single_line_text_field]", "Metafield: my_fields.frame_color [single_line_text_field]",
        "Metafield: my_fields.frame_shape [single_line_text_field]", "Metafield: my_fields.frame_material [single_line_text_field]",
        "Metafield: my_fields.product_size [single_line_text_field]", "Metafield: my_fields.for_who [single_line_text_field]"
    ]]

    merged_file.to_excel(f"{TO_IMPORT_FOLDER}/new/Marchon_new_products.xlsx", index=False)
    merged_file.to_excel(f"Marchon_new_products.xlsx", index=False)

if __name__ == "__main__":
    with open(marchon_new_item_log, "a") as file:
        current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
        file.write(f"[{current_time}] Starting Marchon new products getter \n")
        try:
            get_marchon_new_products()
            file.write(f"New Marchon products are updated successfully \n")
            file.write("Closing Marchon new products getter \n \n")
            print("Tutto ok")
        except Exception as err:
            file.write(f"Error during Marchon new products updating: \n")
            file.write(f"{type(err).__name__}, {err}")
            file.write("Closing Marchon new products getter \n \n")
            print(f"{type(err).__name__}, {err}")