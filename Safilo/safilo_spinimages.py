import pandas as pd


def get_spinimages_pictures():
    try:
        # Carica il file Excel
        safilo = pd.read_excel(
            "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_backup/Safilo_IMG.xlsx",
            engine="openpyxl")
        print("safilo file read correctly")
    except FileNotFoundError as err:
        raise FileNotFoundError("safilo file is not in the directory")

    # Sostituisci NaN con stringhe vuote nella colonna "Image Src"
    safilo["Image Src"] = safilo["Image Src"].fillna("")

    # Raggruppa per "Title" e concatena i valori di "Image Src" con il separatore ";"
    image_src_grouped = safilo.groupby("Title", as_index=False)["Image Src"].agg(";".join)

    # Unisci il risultato al DataFrame originale senza duplicare le colonne
    safilo_merged = safilo.drop(columns=["Image Src"]).drop_duplicates().merge(image_src_grouped, on="Title",
                                                                               how="left")

    # Funzione per rimuovere spinimages=n dalla colonna "Tags" e aggiungere il conteggio delle immagini
    def get_spinimages(row):
        tags_cleaned = pd.Series(row["Tags"]).str.replace(r'spinimages=\d+', '', regex=True).values[0]
        images = row["Image Src"].split(";")
        n_images = len(images)
        return f"{tags_cleaned}, spinimages={n_images}"

    # Applica la funzione per aggiornare la colonna "Tags" in safilo_merged
    safilo_merged["Tags"] = safilo_merged.apply(get_spinimages, axis=1)

    # Esporta il risultato in un nuovo file Excel
    output_filename = "safilo_File_Spinimages_ok.xlsx"
    safilo_merged.to_excel(output_filename, index=False)
    print(f"File {output_filename} saved successfully")


if __name__ == "__main__":
    print("Starting safilo spinimages.py")
    get_spinimages_pictures()
    print("Closing safilo spinimages.py")
