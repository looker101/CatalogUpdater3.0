import pandas as pd


def get_spinimages_pictures():
    try:
        # Carica il file Excel
        luxottica = pd.read_excel(
            "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_backup/Luxottica_IMG.xlsx",
            engine="openpyxl")
        print("luxottica file read correctly")
    except FileNotFoundError as err:
        raise FileNotFoundError("luxottica file is not in the directory")

    # Sostituisci NaN con stringhe vuote nella colonna "Image Src"
    luxottica["Image Src"] = luxottica["Image Src"].fillna("")

    # Raggruppa per "Title" e concatena i valori di "Image Src" con il separatore ";"
    image_src_grouped = luxottica.groupby("Title", as_index=False)["Image Src"].agg(";".join)

    # Unisci il risultato al DataFrame originale senza duplicare le colonne
    luxottica_merged = luxottica.drop(columns=["Image Src"]).drop_duplicates().merge(image_src_grouped, on="Title",
                                                                               how="left")

    # Filtra solo per i valori che NON contengono spinimages
    mask_spinimages_tag = ~luxottica_merged["Tags"].str.contains("spinimages")
    luxottica_merged = luxottica_merged[mask_spinimages_tag]

    # Funzione per rimuovere spinimages=n dalla colonna "Tags" e aggiungere il conteggio delle immagini
    def get_spinimages(row):
        #tags_cleaned = pd.Series(row["Tags"]).str.replace(r'spinimages=\d+', '', regex=True).values[0]
        images = row["Image Src"].split(";")
        n_images = len(images)
        return f"{row['Tags']}, spinimages={n_images}"

    # Applica la funzione per aggiornare la colonna "Tags" in luxottica_merged
    luxottica_merged["Tags"] = luxottica_merged.apply(get_spinimages, axis=1)

    # Esporta il risultato in un nuovo file Excel
    output_filename = "luxottica_File_Spinimages_ok.xlsx"
    luxottica_merged.to_excel(output_filename, index=False)
    print(f"File {output_filename} saved successfully")


if __name__ == "__main__":
    print("Starting luxottica spinimages.py")
    get_spinimages_pictures()
    print("Closing luxottica spinimages.py")
