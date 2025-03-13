import pandas as pd
import datetime
from av_now_config_paths import LUXOTTICA, DERIGO, KERING, MARCHON, MARCOLIN, SAFILO, RSF, LOGS_FOLDER

def update_available_now_items():
    current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
    try:
        # ===============================
        # LETTURA FILE MAGAZZINO LOOKER
        # ===============================
        df = pd.read_excel("MAG tot..xlsx", usecols=[
            "Vendor", "Variant Barcode", "Variant SKU", "Variant Inventory Qty"
        ])

        # ===============================
        # LETTURA FILE FORNITORI
        # ===============================
        suppliers_files = [LUXOTTICA, DERIGO, KERING, MARCHON, MARCOLIN, SAFILO]  # , RSF
        concat_suppliers_files = []

        for file in suppliers_files:
            supplier_df = pd.read_excel(file)
            supplier_df = supplier_df.drop("Image Src", axis=1)
            supplier_df = supplier_df.dropna(how="any", subset=["Variant Barcode"])
            concat_suppliers_files.append(supplier_df)

        all_suppliers_df = pd.concat(concat_suppliers_files, ignore_index=True)

        # JOIN con magazzino Looker
        disponibili_subito = df.merge(
            all_suppliers_df,
            how="inner",
            on="Variant Barcode",
            suffixes=("_magazzino", "_looker")
        )

        # ===============================
        # QUANTITA'
        # ===============================
        def get_products_quantity(row):
            if row["Variant Inventory Qty_magazzino"] >= 1:
                return row["Variant Inventory Qty_magazzino"]
            return row["Variant Inventory Qty_looker"]

        disponibili_subito["Variant Inventory Qty"] = disponibili_subito.apply(get_products_quantity, axis=1)
        disponibili_subito["Inventory Available: +39 05649689443"] = disponibili_subito["Variant Inventory Qty"]

        # ===============================
        # PULIZIA E FORMATTAZIONE
        # ===============================
        disponibili_subito["Tags"] = disponibili_subito["Tags"].str.replace(
            r"\s*,?\s*available now\s*,?\s*", "", regex=True
        ).str.strip()
        disponibili_subito["Tags"] = disponibili_subito["Tags"].str.replace(
            r"\s*,?\s*tag__sale_In Stock\s*,?\s*", "", regex=True
        ).str.strip()

        # Colonne da mantenere
        columns_to_keep = [
            "ID", "Vendor_looker", "Variant Barcode", "Title", "Variant SKU_looker",
            "Variant Inventory Qty", "Inventory Available: +39 05649689443",
            "Command", "Type", "Tags", "Tags Command", "Template Suffix",
            "Variant ID", "Option1 Name", "Option1 Value", "Variant Price",
            "Variant Compare At Price"
        ]

        disponibili_subito = disponibili_subito[columns_to_keep]

        # RINOMINA COLONNE
        disponibili_subito = disponibili_subito.rename(columns={
            "Vendor_looker": "Vendor",
            "Variant SKU_looker": "Variant SKU"
        })

        # ===============================
        # TAGS & TEMPLATE SUFFIX
        # ===============================
        def assign_template_suffix(row):
            if row["Variant Inventory Qty"] > 0:
                return "disponibili-subito"
            return "Default product"

        disponibili_subito["Template Suffix"] = disponibili_subito.apply(assign_template_suffix, axis=1)

        def get_available_now_tags(row):
            if row["Template Suffix"] == "disponibili-subito":
                return f"{row['Tags']}, available now, tag__sale_In Stock"
            return row["Tags"]

        disponibili_subito["Tags"] = disponibili_subito.apply(get_available_now_tags, axis=1)

        # TRACKING
        disponibili_subito["Variant Inventory Tracker"] = "shopify"

        # SORTING
        disponibili_subito = disponibili_subito.sort_values(by="Variant SKU")

        # SALVA FILE
        disponibili_subito.to_excel("Available_now.xlsx", index=False)

        # LOG
        with open(f"{LOGS_FOLDER}/Available_now_logs.txt", "a") as file:
            file.write(f"[{current_time}]: Available now items are updated successfully!\n")
            print(f"[{current_time}]: Available now items are updated successfully!")

    except Exception as err:
        with open(f"{LOGS_FOLDER}/Available_now_logs.txt", "a") as file:
            file.write(f"[{current_time}]: Available now items are not updated due to this error\n")
            file.write(f" - {type(err).__name__}: {err}\n")
            print(f"[{current_time}]: Available now items are not updated due to this error\n")
            print(f" - {type(err).__name__}: {err}\n")

if __name__ == "__main__":
    update_available_now_items()