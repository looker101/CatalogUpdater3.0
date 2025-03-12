import pandas as pd
import openpyxl
import time
import os
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from luxottica_paths import miumiu_folder, miumiu_new, logs_folder, to_import_images

def get_miu_miu_images():

    # Carica il dataframe e definisci la cartella immagini
    df = pd.read_excel(miumiu_new)
    image_folder = '/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Immagini/'

    df = df[[
        "ID", "Handle", "Command", "Title", "Vendor", "Type", "Tags", "Tags Command", "Template Suffix",
         "Variant Barcode", "Variant SKU", "Variant Price", "Variant Compare At Price",
        "Variant Inventory Qty", "Inventory Available: +39 05649689443", "Metafield: my_fields.lens_color [single_line_text_field]",
        "Metafield: my_fields.frame_color [single_line_text_field]", "Metafield: my_fields.frame_shape [single_line_text_field]",
        "Metafield: my_fields.frame_material [single_line_text_field]", "Metafield: my_fields.product_size [single_line_text_field]",
        "Metafield: my_fields.for_who [single_line_text_field]", "Option1 Name", "Option1 Value"
        # "Metafield: custom.main_frame_shape [single_line_text_field]",
        # "Metafield: custom.main_frame_material [single_line_text_field]",
        # "Metafield: custom.main_frame_color [single_line_text_field]",
        # "Metafield: custom.main_lens_color [single_line_text_field]",
        # "Metafield: custom.main_lens_technology [single_line_text_field]",
        # "Metafield: custom.main_size [single_line_text_field]"
    ]]

    df["Image Alt Text"] = df["Vendor"] + ' ' + df["Variant SKU"]

    # Pulisce la colonna "Variant SKU" e aggiunge lo zero iniziale, se richiesto
    df["Check_IMG"] = df["Variant SKU"].str[:-2]
    df["Check_IMG"] = df["Check_IMG"].str.strip().str.replace(' ', '_', 1)
    df["Check_IMG"] = df["Check_IMG"].str.strip().str.replace(' ', '__')
    df["Check_IMG"] = df.apply(lambda row: f'0{row["Check_IMG"]}', axis=1)

    # Standardize "Title" column to ensure "Miu Miu" appears correctly
    df["Title"] = df["Title"].str.replace("Miu miu", "Miu Miu", case=False).str.strip()

    # Funzione per generare le URL e controllare la presenza delle immagini nella cartella
    def generate_image_urls(row):
        sku = row["Check_IMG"]
        # Suffixes per le immagini
        suffixes = ["", ".jpeg", "__P21__shad__fr.png", "__P21__shad__al2.png", "__P21__shad__al3.png",
                    "__P21__shad__bk.png",
                    "__P21__shad__cfr.png", "__P21__shad__lt.png", "__P21__shad__qt.png",
                    "_000A.png", "_030A.png", "_060A.png", "_090A.png", "_120A.png", "_150A.png", "_180A.png",
                    "_210A.png", "_240A.png", "_270A.png", "_300A.png", "_330A.png",
                    "__STD__shad__bk.png", "__STD__shad__cfr.png", "__STD__shad__fr.png", "__STD__shad__lt.png",
                    "__STD__shad__qt.png"]

        #Genera le URL e i nomi di file locali
        urls = []
        for suffix in suffixes:
            # URL per il nome dell'immagine con suffisso
            url = f"https://staging.lookeronline.com/script/Catalog/Luxottica/Immagini/{sku}{suffix}"
            # Nome file nella cartella immagini
            filename = f"{sku}{suffix}"
            # Se il file esiste nella cartella, aggiungi l'URL alla lista
            if os.path.isfile(os.path.join(image_folder, filename)):
                urls.append(url)

        # Unisce tutte le URL trovate, separate da ";"
        return ";".join(urls)

    # Applica la funzione per generare e popolare la colonna "Image SRC"
    df["Image Src"] = df.apply(generate_image_urls, axis=1)


    # def count_imageSrc(row):
    #     tags_cleaned = pd.Series(row["Tags"]).str.replace(r'spinimages=\d+,', '', regex=True).values[0]
    #     images = row["Image Src"].split(";")
    #     n_images = len(images)
    #     return f"{tags_cleaned}, spinimages={n_images}"
    #
    # df["Tags"] = df.apply(count_imageSrc, axis=1)

    df["Image Src"] = df["Image Src"].replace("", pd.NA)
    df = df.dropna(how='any', axis=0, subset=["Image Src"])


    df = df.drop(columns={"Check_IMG"})

    df = df.sort_values(by="Title")

    # Salva il risultato in un nuovo file Excel
    def check_df_is_empty(df):
        if df.empty:
            print("Miu Miu doesn't have Images")
        else:
            df.to_excel(f"{miumiu_folder}/MiuMiu_IMG_OK.xlsx", index=False)
            df.to_excel(f"{to_import_images}/miu_miu_img_ok.xlsx", index = False)
            # Rename the sheet to "Products
            wb = openpyxl.load_workbook(f"{to_import_images}/miu_miu_img_ok.xlsx")
            ws = wb.active
            ws.title = "Products"
            wb.save(f"{to_import_images}/miu_miu_img_ok.xlsx")

    check_df_is_empty(df)

if __name__ == "__main__":
    try:
        print("Getting Miu Miu images for new products...")
        time.sleep(1)
        get_miu_miu_images()
        print("Miu Miu done")
    except Exception as err:
        print("!!!Warning!!! Something went wrong")
        print(f"{type(err).__name__}: {err}")