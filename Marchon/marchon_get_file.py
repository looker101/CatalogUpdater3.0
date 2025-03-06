import pandas as pd
import datetime
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from marchon_paths import FTP_MARCHON_CSV, MARCHON_BACKUP, FTP_MARCHON_FOLDER, marchon_update_regular_items
from marchon_colors_and_frames_mapping import marchon_lens_colors, marchon_frames_colors, items_shape, frame_material,\
    marchon_lens_technology

def get_marchon_regular_items():
    shopify = pd.read_excel(MARCHON_BACKUP)
    marchon = pd.read_csv(FTP_MARCHON_CSV)

    # merge two df how inner on Barcode. Get regular products
    merged_file = shopify.merge(marchon,
                                left_on = "Variant Barcode",
                                right_on = "UPC SKU",
                                how = "inner",
                                indicator = True)

    # Prices
    merged_file["Variant Compare At Price"] = merged_file["RRP"]
    merged_file["Variant Price"] = ""

    # If the item is in marchon file is available. Thus, insert with qty like 10
    merged_file["Variant Inventory Qty"] = 10
    merged_file["Inventory Available: +39 05649689443"] = 10

    # Fill columns
    merged_file["Metafield: my_fields.lens_color [single_line_text_field]"] = merged_file["LENS COLOR"]
    merged_file["Metafield: my_fields.frame_color [single_line_text_field]"] = merged_file["FRAME COLOR"]
    merged_file["Metafield: my_fields.frame_shape [single_line_text_field]"] = merged_file["Shape"]
    merged_file["Metafield: my_fields.frame_material [single_line_text_field]"] = merged_file["FRAME MATERIAL"]
    merged_file["Metafield: my_fields.gtin1 [single_line_text_field]"] = merged_file["Variant Barcode"]
    merged_file["Metafield: my_fields.lens_technology [single_line_text_field]"] = merged_file["LENS TYPE"]
    #merged_file["Title"] = merged_file["Material.1"]
    merged_file["Command"] = "MERGE"

    # Make sure the vendor name is capitalize (use rename function because there are some brand with two names)
    #merged_file["Vendor"] = merged_file["Vendor"].str.title()
    #merged_file["Title"] = merged_file["Title"].str.title()

    def get_title_nike(row):
        brand = str(row["Material.1"]) if pd.notna(row["Material.1"]) else ""
        vendor = str(row["Vendor"]) if pd.notna(row["Vendor"]) else ""
        color_code = str(row["Color code"]) if pd.notna(row["Color code"]) else ""

        #brand = str(row["Material.1"])

        if row["Vendor"] == "Nike" or row["Vendor"] == "NIKE":
            brand_splitted = brand.split()

            new_title = []

            for stringa in brand_splitted:
                if stringa.isalpha():
                    new_title.append(stringa.title())
                elif stringa.isdigit():
                    new_title.append(stringa.upper())
                else:
                    new_title.append(stringa.upper())

            new_title.append(str(row["Color code"]))

            return " ".join(new_title)
        else:
            return f'{row["Vendor"].title()} {row["Material.1"]} {row["Color code"]}'

    merged_file["Title"] = merged_file.apply(get_title_nike, axis = 1)
   #merged_file["Title"] = merged_file["Title"].str.title()

    # Gender must be singolar. Man or Woman
    def get_gender(row):
        """Determina il genere dell'occhiale"""
        if row["Gender"] == "MALE":
            return "Man"
        return "Woman"
    merged_file["Metafield: my_fields.for_who [single_line_text_field]"] = merged_file.apply(get_gender, axis = 1)

    # SIZE - BRIDGE - TEMPLES
    def get_size_brige_temples(row):
        """Determina il calibro, ponte ed asta"""
        size = row["LENS WIDTH"]
        bridge = row["BRIDGE"]
        temples = row["TEMPLE"]
        return f"{size}-{bridge}-{temples}"
    merged_file["Metafield: my_fields.product_size [single_line_text_field]"] = merged_file.apply(get_size_brige_temples, axis = 1)

    # Create a list with all images for each product
    def get_images_products(row):
        """Raggruppo tutte le immagini di ogni prodotto in una lista splittata da ;"""
        images_list = [
            str(row["Image URL"]), str(row["Image URL.1"]), str(row["Image URL.2"]), str(row["Image URL.3"]),
            str(row["Image URL.4"]), str(row["Image URL.5"]), str(row["Image URL.6"]), str(row["Image URL.7"])
        ]

        images_list = [img for img in images_list if img != "nan"]

        return ";".join(images_list)
    merged_file["Image Src"] = merged_file.apply(get_images_products, axis = 1)

    # Get only necessary columns to Shopify import
    columns_to_keep = [
        "Variant ID", "Variant SKU", "Variant Barcode", "Variant Price", "Variant Compare At Price",
        "Variant Inventory Qty", "ID", "Handle", "Tags", "Command", "Title", "Body HTML",  "Vendor",
        "Type", "Tags Command", "Status", "Template Suffix", "URL", "Total Inventory Qty", "Option1 Name",
        "Option1 Value", "Image Src", "Inventory Available: +39 05649689443", "Metafield: title_tag [string]",
        "Metafield: description_tag [string]", "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]", "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]", "Metafield: my_fields.product_size [single_line_text_field]",
        "Metafield: my_fields.gtin1 [single_line_text_field]", "Metafield: my_fields.for_who [single_line_text_field]",
        "Metafield: my_fields.lens_technology [single_line_text_field]"
    ]

    merged_file = merged_file[columns_to_keep]

#===================================================== MAIN VALUES ===================================================
    # GET LENS COLOR
    def get_main_lens_color(row):
        """Determino il colore principale per le lenti"""
        lens_color_value = str(row["Metafield: my_fields.lens_color [single_line_text_field]"]).strip().title()
        # Evito che ci siano valori NaN
        if not isinstance(lens_color_value, str):
            lens_color_value = ""
        if "Eyeglasses" not in row["Tags"]:
            for mother, childs in marchon_lens_colors.items():
                for color in childs:
                    if lens_color_value == color.strip().title():
                        return mother
        return "DEMO"
    merged_file["Metafield: custom.main_lens_color [single_line_text_field]"] = merged_file.apply(get_main_lens_color, axis=1)
    print("Lens color ok")

    # GET MAIN FRAME COLOR
    def get_main_frame_color(row):
        """Determino il colore principale per il frame"""
        frame_color_value = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).strip().title()
        if not isinstance(frame_color_value, str):
            return ""
        for mother, child in marchon_frames_colors.items():
            for color in child:
                if frame_color_value == color.strip().title():
                    return mother
        return "Miscellaneous"
    merged_file["Metafield: custom.main_frame_color [single_line_text_field]"] = merged_file.apply(get_main_frame_color, axis =1)
    print("Frame color ok")

    # MAIN SHAPE
    def get_main_each_shape(row):
        """Determino la forma principale"""
        frame_shape_value = str(row["Metafield: my_fields.frame_shape [single_line_text_field]"]).strip().title()
        if not isinstance(frame_shape_value, str):
            return ""
        for mother, child in items_shape.items():
            for shape in child:
                if frame_shape_value == shape.strip().title():
                    return mother
        return "Other"
    merged_file["Metafield: custom.main_frame_shape [single_line_text_field]"] = merged_file.apply(get_main_each_shape, axis = 1)
    print("Frame shape ok")

    # MAIN FRAME MATERIAL
    def get_main_frame_material(row):
        """Determino il materiale del frame principale"""
        material = str(row["Metafield: my_fields.frame_material [single_line_text_field]"]).strip().title()
        if not isinstance(material, str):
            return ""
        for mother, child in frame_material.items():
            for materiale in child:
                if material == materiale.strip().title():
                    return mother
        return "Other"
    merged_file["Metafield: custom.main_frame_material [single_line_text_field]"] = merged_file.apply(get_main_frame_material, axis = 1)
    print("Frame material ok")

    # GET LENS TECHNLOGY
    def get_main_lens_technology(row):
        items_lens_technology = str(row["Metafield: my_fields.lens_technology [single_line_text_field]"]).strip().title()
        if not isinstance(items_lens_technology, str):
            return ""
        for mother, children in marchon_lens_technology.items():
            for techno in children:
                if items_lens_technology == techno.strip().title():
                    return mother
        return "Standard"
    merged_file["Metafield: custom.main_lens_technology [single_line_text_field]"] = merged_file.apply(get_main_lens_technology, axis = 1)
    print("Lens Technology OK")

    # GET MAIN SIZE
    def get_main_size(row):
        if pd.notna(row["Option1 Value"]):
            if row["Option1 Value"] in range(0, 48):
                return "S"
            elif row["Option1 Value"] in range(48, 53):
                return "M"
            else:
                return "L"
        return ""
    merged_file["Metafield: custom.main_size [single_line_text_field]"] = merged_file.apply(get_main_size, axis = 1 )

    # ===================================================== END MAIN VALUES ===================================================
    # TAGS
    def get_tags(row):
        """Genero la colonna tags con i valori presenti nelle altre colonne"""
        merged_file["Tags"] = ""

        tags_list = [
            str(row["Vendor"]) if pd.notna(row["Vendor"]) else "",
            str(row["Type"]) if pd.notna(row["Type"]) else "",
            str(row["Metafield: custom.main_lens_color [single_line_text_field]"]) if pd.notna(row["Metafield: custom.main_lens_color [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_frame_color [single_line_text_field]"]) if pd.notna(row["Metafield: custom.main_frame_color [single_line_text_field]"]) else "",
            str(row["Metafield: my_fields.frame_shape [single_line_text_field]"]) if pd.notna(row["Metafield: my_fields.frame_shape [single_line_text_field]"]) else "",
            str(row["Metafield: my_fields.frame_material [single_line_text_field]"].title()) if pd.notna(row["Metafield: my_fields.frame_material [single_line_text_field]"]) else "",
            str(row["Metafield: custom.main_size [single_line_text_field]"]).title() if pd.notna(row["Metafield: custom.main_size [single_line_text_field]"]) else ""
        ]
        tags_list = [str(tag).replace(",", "") for tag in tags_list if pd.notna(tag) and str(tag).strip() != ""]
        #tags_list = [str(tag).replace(",", "") for tag in tags_list]
        #print(tags_list)

        if row["Vendor"] == "Nike":
            tags_list.append("Sport")

        return ",".join(tags_list)
    merged_file["Tags"] = merged_file.apply(get_tags, axis = 1)

    marchon_brands = merged_file["Vendor"].unique()
    #print(marchon_brands)

    merged_file.to_excel("Marchon_test.xlsx", index=False)

    for brand in marchon_brands:
        brand_filter = merged_file["Vendor"] == brand
        brand_file = merged_file[brand_filter]
        brand_file.to_excel(f"{FTP_MARCHON_FOLDER}/{brand}/{brand}.xlsx", index = False)
        time.sleep(1)
        file.write(f"   - {brand} updated!\n")

if __name__ == "__main__":
    with open(marchon_update_regular_items, "a") as file:
        try:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{current_time}] Starting Marchon regular items updater\n")
            get_marchon_regular_items()
            file.write("Marchon regular items are updated successfully\n")
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"Closing Marchon regular items updater\n \n")
            print("Tutto ok")
        except Exception as err:
            file.write(f"Marchon items are not updated due this error\n {type(err).__name__}: {err} \n")
            file.write(f"Closing Marchon regular items updater\n \n")
            print(f"{type(err).__name__}: {err} \n")