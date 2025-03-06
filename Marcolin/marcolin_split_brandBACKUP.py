import pandas as pd
import time
import datetime
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from marcolin_paths import splitting_marcolin_brands, marcolin_backup

marcolin_file = pd.read_excel(marcolin_backup)

marcolin_file = marcolin_file.drop("Image Src", axis = 1)
marcolin_file = marcolin_file.dropna(how = "any", axis = 0, subset=["Variant ID"])

marcolin_file["Status"] = "Active"
marcolin_file["Command"] = "MERGE"

def marcolin_split_brands():
    
    def check_available_now_tag(row):
        if "available now" in row["Tags"]:
            return "disponibili-subito"
        return "Default product"
    marcolin_file["Template Suffix"] = marcolin_file.apply(check_available_now_tag, axis=1)
    #marcolin_file.to_excel("Fix_availableNowTags.xlsx", index=False)
    
    def tom_ford_vendor(row):
        if row["Vendor"] == "tom Ford":
            return "Tom Ford"
        return row["Vendor"]
    marcolin_file["Vendor"] = marcolin_file.apply(tom_ford_vendor, axis = 1)

    def maxmara_title(row):
        if row["Vendor"] == "MaxMara":
            row["Title"] = row["Title"].replace("Maxmara", "MaxMara")
            return row["Title"]
        return row["Title"]
    marcolin_file["Title"] = marcolin_file.apply(maxmara_title, axis = 1)

    for brand in marcolin_file["Vendor"].unique():
        try:
            mask = marcolin_file["Vendor"] == brand
            brand_file = marcolin_file[mask]
            brand_file.to_excel(f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/{brand}/{brand}.xlsx",
                                index = False)
            print(f"{brand} saved successfully")
            with open(splitting_marcolin_brands, "a") as file:
                file.write(f"   {brand} are split successfully \n")
            time.sleep(1)
        except Exception as err:
            print(f"{type(err).__name__}: {err}")
            with open(splitting_marcolin_brands, "a") as file:
                file.write(f"   {brand} is not split due this error: \n {type(err).__name__}: {err} \n")

if __name__ == "__main__":
    try:
        with open(splitting_marcolin_brands, "a") as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n[{current_time}] Starting Marcolin splitting brands. \n")
        marcolin_split_brands()

        with open(splitting_marcolin_brands, "a") as file:
            file.write(f"Marcolin brands are split successfully. \n")
            file.write(f"Closing Marcolin splitting brands. \n")

    except Exception as err:
        with open(splitting_marcolin_brands, "a") as file:
            file.write(f"Marcolin brands are not split due this error: {type(err).__name__}: {err} \n")
