import pandas as pd
import os
import datetime
from av_now_config_paths import LUXOTTICA, DERIGO, KERING, MARCHON, MARCOLIN, SAFILO, RSF, LOGS_FOLDER

today = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")

def update_available_now_items():
    # read warehouse file
    df = pd.read_excel("MAG tot..xlsx", usecols=[
        "Vendor", "Variant Barcode", "Variant SKU", "Variant Inventory Qty"
    ])

    #excl_brands = ["Oakley", "Ray-Ban", "Persol", "Police"]

    # list with all suppliers excel file
    suppliers_files = [
        LUXOTTICA, DERIGO, KERING, MARCHON, MARCOLIN, SAFILO#, RSF
    ]

    luxottica = [
        "Burberry", "Dolce & Gabbana", "Emporio Armani", "Giorgio Armani", "Michael Kors",
        "Miu Miu", "Oakley", "Persol", "Prada", "Prada Linea Rossa", "Ralph", "Swarovski",
        "Tiffany", "Versace", "Vogue Eyewear"
    ]

    # xlsx file become dataframe
    concat_suppliers_files = [pd.read_excel(file) for file in suppliers_files]

    # concat all suppliers dataframes
    all_suppliers_df = pd.concat(concat_suppliers_files, ignore_index=True)

    # merge warehouse file with concat suppliers file
    disponibili_subito = df.merge(all_suppliers_df, how = "inner", on = "Variant Barcode")

    # choice the right columns
    disponibili_subito = disponibili_subito[[
        "Vendor_x", "Variant Barcode", "Variant Inventory Qty_x", "ID", "Handle", "Command", "Title", "Type",
        "Tags", "Tags Command", "Template Suffix", "URL", "Variant ID", "Variant SKU_y", "Variant Price",
        "Variant Compare At Price", "Metafield: title_tag [string]", "Metafield: description_tag [string]",
        "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]",
        "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]",
        "Metafield: my_fields.lens_material [single_line_text_field]",
        "Metafield: my_fields.for_who [single_line_text_field]",
        "Metafield: custom.main_lens_technology [single_line_text_field]",
        "Metafield: custom.main_frame_shape [single_line_text_field]",
        "Metafield: custom.main_frame_material [single_line_text_field]",
        "Metafield: custom.main_frame_color [single_line_text_field]",
        "Metafield: custom.main_lens_color [single_line_text_field]",
        "Metafield: custom.main_size [single_line_text_field]"
    ]]

    # columns rename
    disponibili_subito = disponibili_subito.rename(columns={
        "Vendor_x":"Vendor", "Variant Inventory Qty_x":"Variant Inventory Qty", "Variant SKU_y":"Variant SKU"
    })

    # REMOVE AVAILABLE NOW TAG
    disponibili_subito["Tags"] = disponibili_subito["Tags"].str.replace(", available now", "")
    disponibili_subito["Tags"] = disponibili_subito["Tags"].str.replace("available now,", "")


    # Make sure to have the correct brand name
    disponibili_subito["Vendor"] = disponibili_subito["Vendor"].astype(str).str.title()

    # Luxottica Brand -10%
    # AveMaria: Persol -10%
    # AveMaria: oakley -10%
    # AveMaria: rayban -5%
    # AveMaria: guess 0
    # AveMaria: polaroid 0
    # AveMaria: arnette 0
    # AveMaria: vogue 0
    # AveMaria: under armour 0
    # AveMaria: Police -10% RETROSUPERFUTURE
    # AveMaria: RETROSUPERFUTURE 0

    # def get_discount(row):
    #     """Apply Discount throught Variant Compare At Price"""
    #
    #     if row["Vendor"] in luxottica:
    #         return round(row["Variant Compare At Price"] * 0.9)
    #     elif row["Vendor"] == "Ray-Ban":
    #         return round(row["Variant Compare At Price"] * 0.95)
    #     else:
    #         return row["Variant Compare At Price"]
    #
    # disponibili_subito["Variant Price"] = disponibili_subito.apply(get_discount, axis = 1)

    # ASSIGN disponibili-subito TEMPLATE SUFFIX IF QUANTITY IS GREATER THAN 0
    #disponibili_subito["Variant Inventory Qty"] = disponibili_subito["Variant Inventory Qty"].fillna(0).astype(int)
    # if variant price == 0 or 7, variant price must be 0
    def remove_quantity(row):
        if row["Variant Price"] == 0 or row["Variant Price"] == 7:
            return 0
        return row["Variant Inventory Qty"]
    disponibili_subito["Variant Inventory Qty"] = disponibili_subito.apply(remove_quantity, axis = 1)

    def assign_template_suffix(row):
        if row["Variant Inventory Qty"] > 0:
            return "disponibili-subito"
        return "Default product"
    disponibili_subito["Template Suffix"] = disponibili_subito.apply(assign_template_suffix, axis = 1)

    # Insert "available now" on tags column
    def get_available_now_tags(row):
        if row["Template Suffix"] == "disponibili-subito":
            return f"{row['Tags']}, available now"
        return row["Tags"]
    disponibili_subito["Tags"] = disponibili_subito.apply(get_available_now_tags, axis=1)

    disponibili_subito["Variant Compare At Price"] = disponibili_subito["Variant Compare At Price"].fillna(0).astype(float)

    # Setting Variant Inventory Tracker column as shopify
    disponibili_subito["Variant Inventory Tracker"] = "shopify"
    
    # sort values
    disponibili_subito = disponibili_subito.sort_values(by="Variant SKU")

    # save dataframe
    disponibili_subito.to_excel("Available_now.xlsx", index = False)
    #print("Data processing completed successfully!")


if __name__ == "__main__":
    try:
        update_available_now_items()
        with open(f"{LOGS_FOLDER}/Available_now_logs.txt", "a") as file:
            file.write(f"[{today}]: Available now items are updated successfully! \n")
    except Exception as err:
        with open(f"{LOGS_FOLDER}/Available_now_logs.txt", "a") as file:
            file.write(
                f"[{today}]: Available now items are not updated due this error \n - {type(err).__name__}: {err} \n")