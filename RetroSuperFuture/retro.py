from xxlimited_35 import error

import pandas as pd
import sys
import datetime
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from retro_paths import DAILY_LOOKER, RETRO_LOGS, TODAY, TO_IMPORT, RETROSUPERFUTURE_FOLDER_FTP,\
    PRICE_QUANTITY

#today = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")

def retro_update_catalog():
    daily = pd.read_excel(DAILY_LOOKER)

    mask = daily["Vendor"] == "RETROSUPERFUTURE"
    mask1 = daily["Type"] == "Eyewear"
    daily = daily[mask & mask1]

    # Add "RetroSuperFuture" prefix to the Title
    def addRetroSuperFuture(row):
        return "RetroSuperFuture" + " " + row

    daily["Title"] = daily["Title"].apply(addRetroSuperFuture)

    # Set default values for some columns
    daily["Variant Inventory Tracker"] = "shopify"
    daily["Template Suffix"] = "retrosuperfuture"
    daily["Metafield: description_tag [string]"] = ""

    # Set the Type based on Tags
    def get_type(row):
        if "Sunglass" in row["Tags"]:
            return "Sunglasses"
        return "Eyeglasses"

    daily["Type"] = daily.apply(get_type, axis=1)

    # Apply a 20% discount to the Variant Price
    # def discount20(row):
    #         return int(round(row["Variant Price"] * 0.8, 2))


    daily["Variant Price"] = daily["Variant Price"]
    #daily["Variant Price"] = daily.apply(discount20, axis = 1)

    daily["Command"] = "MERGE"

    # Group by 'Handle' and concatenate 'Image Src' values
    # If Handle rows are equal, concatenate 'Image Src' values separated by ";"
    daily["Image Src"] = daily.groupby("Handle")["Image Src"].transform(lambda x: ';'.join(x.dropna().astype(str)))
    # Drop duplicate rows based on 'Handle' after concatenation
    daily = daily.drop_duplicates(subset=["Handle"])

    daily = daily.sort_values(by="Handle")

    # Save the modified DataFrame to an Excel file
    daily.to_excel(f"{RETROSUPERFUTURE_FOLDER_FTP}/RetroUpdate.xlsx", index=False)
    daily.to_excel(f"{PRICE_QUANTITY}/RSF_price_qty.xlsx", index=False)

if __name__ == "__main__":
    with open(RETRO_LOGS, "a") as file:
        try:
            retro_update_catalog()
            file.write(f"[{TODAY}] RSF regular items are correctly updated \n")
        except Exception as err:
            file.write(f"[{TODAY}]. RSF regular items not updated due this error:\n - {type(err).__name__}: {err} \n")