import pandas as pd
import time
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from safilo_paths import safilo_splitting_logs, safilo_backup

# UPDATE BY SCRAPER -> I can remove Image column and every empty rows

def split_safilo_brands():
    safilo_file = pd.read_excel(safilo_backup)

    safilo_file = safilo_file.drop('Image Src', axis = 1)
    safilo_file = safilo_file.dropna(how='any', subset=['Variant Barcode'])

    safilo_file["Tags Command"] = "REPLACE"
    safilo_file["Status"] = "Active"

    def check_available_now_tag(row):
        if "available now" in row["Tags"]:
            return "disponibili-subito"
        return "Default product"
    safilo_file["Template Suffix"] = safilo_file.apply(check_available_now_tag, axis=1)

    for brand in safilo_file["Vendor"].unique():
        try:
            mask = safilo_file["Vendor"] == brand
            brand_file = safilo_file[mask]
            brand_file.to_excel(f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/{brand}/{brand}.xlsx",
                                index = False)
            print(f"{brand} saved succesfully")
            with open(safilo_splitting_logs, "a") as file:
                file.write(f"   -{brand} is split successfully\n")
            time.sleep(1)
        except Exception as err:
            print(f"{type(err).__name__}: {err}")
            with open(safilo_splitting_logs, "a") as file:
                file.write(f"   -{brand} is not split due this error:\n {type(err).__name__}: {err} \n")

if __name__ == "__main__":
    try:
        with open(safilo_splitting_logs, "a") as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n[{current_time}] Starting Safilo split brands \n")
        split_safilo_brands()

        with open(safilo_splitting_logs, "a") as file:
            file.write("Safilo's brand are split successfully")
            file.write(f"\n Closing Safilo split brands \n")

    except Exception as err:
        with open(safilo_splitting_logs, "a") as file:
            file.write(f"Safilo's brands are not split due this error:\n {type(err).__name__}: {err} \n")
            file.write(f"\nClosing Safilo split brands \n")
