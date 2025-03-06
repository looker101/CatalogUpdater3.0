# Import delle librerie
import pandas as pd
import datetime
from av_now_config_paths import LUXOTTICA, DERIGO, KERING, MARCHON, MARCOLIN, SAFILO, RSF, LOGS_FOLDER

# =======================================
# LETTURA FILE MAGAZZINO LOOKER
# =======================================

def update_available_now_items():
    df = pd.read_excel("MAG tot..xlsx", usecols=[
        "Vendor", "Variant Barcode", "Variant SKU", "Variant Inventory Qty"
    ])

    # =======================================
    # LETTURA FILE FORNITORI
    # =======================================

    suppliers_files = [LUXOTTICA, DERIGO, KERING, MARCHON, MARCOLIN, SAFILO]  # , RSF
    concat_suppliers_files = []

    for file in suppliers_files:
        supplier_df = pd.read_excel(file)
        supplier_df = supplier_df.drop("Image Src", axis=1)
        supplier_df = supplier_df.dropna(how="any", subset=["Variant Barcode"])
        concat_suppliers_files.append(supplier_df)

    # Unisce tutti i file dei fornitori in un unico DataFrame
    all_suppliers_df = pd.concat(concat_suppliers_files, ignore_index=True)

    # Unisce il magazzino Looker con i dati dei fornitori basandosi sul codice a barre
    disponibili_subito = df.merge(all_suppliers_df, how="inner", on="Variant Barcode")

    # =======================================
    # PULIZIA E FORMATTAZIONE DEI DATI
    # =======================================

    # Rimuove il tag "available now"
    # Rimozione del tag "available now" in tutte le posizioni
    # Pulizia della colonna Template Suffix
    disponibili_subito["Tags"] = disponibili_subito["Tags"].str.replace(r"\s*,?\s*available now\s*,?\s*", "", regex=True).str.strip()
    #disponibili_subito["Template Suffix"] = ""

    # Colonne da mantenere
    columns_to_keep = [
        "ID", "Vendor_y", "Variant Barcode", "Title", "Variant SKU_y",
        "Variant Inventory Qty_x", "Inventory Available: +39 05649689443",
        "Command", "Type", "Tags", "Tags Command", "Template Suffix",
        "Variant ID", "Option1 Name", "Option1 Value", "Variant Price",
        "Variant Compare At Price"
    ]
    disponibili_subito = disponibili_subito[columns_to_keep]

    # RINOMINA LE COLONNE
    disponibili_subito = disponibili_subito.rename(columns={
        "Vendor_y": "Vendor",
        "Variant SKU_y":"Variant SKU",
        "Variant Inventory Qty_x":"Variant Inventory Qty"
    })

    # =======================================
    # TAGS & TEMPLATE SUFFIX
    # =======================================

    # SE LA QUANTITA' E' UGUALE O MAGGIORE DI 1, INSERIRE TAG AVAILABLE NOW
    def assign_template_suffix(row):
        if row["Variant Inventory Qty"] > 0:
            return "disponibili-subito"
        return "Default product"
    disponibili_subito["Template Suffix"] = disponibili_subito.apply(assign_template_suffix, axis=1)

    #
    def get_available_now_tags(row):
        if row["Template Suffix"] == "disponibili-subito":
            return f"{row['Tags']}, available now"
        return row["Tags"]
    disponibili_subito["Tags"] = disponibili_subito.apply(get_available_now_tags, axis=1)

    # =========================================
    # TRACKING AND SORTING
    # ==========================================
    disponibili_subito["Variant Inventory Tracker"] = "shopify"

    disponibili_subito = disponibili_subito.sort_values(by="Variant SKU")

    # ===================================================SAVE===================================================

    disponibili_subito.to_excel("Available_now.xlsx", index = False)


if __name__ == "__main__":
    current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
    try:
        update_available_now_items()
        with open(f"{LOGS_FOLDER}/Available_now_logs.txt", "a") as file:
            file.write(f"[{current_time}]: Available now items are updated successfully! \n")
    except Exception as err:
        with open(f"{LOGS_FOLDER}/Available_now_logs.txt", "a") as file:
            file.write(
                f"[{current_time}]: Available now items are not updated due this error \n - {type(err).__name__}: {err} \n")

