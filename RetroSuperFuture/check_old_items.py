import pandas as pd
import sys
import datetime

print("check_old starting")

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from retro_paths import RETROSUPERFUTURE_FOLDER_FTP, DAILY_LOOKER, RETRO_BACKUP, RETRO_LOGS, TODAY, PRODUCTS_OUT

def rsf_out_products():
    daily = pd.read_excel(DAILY_LOOKER)
    rsf_backup = pd.read_excel(RETRO_BACKUP)

    eyewear_filter = daily["Type"] == "Eyewear"
    daily = daily[eyewear_filter]

    daily["Variant Barcode"] = daily["Variant Barcode"].astype(str).replace('.0','')
    rsf_backup["Variant Barcode"] = rsf_backup["Variant Barcode"].astype(str).replace('.0','')

    df_merged = daily.merge(rsf_backup,
                            how = 'outer',
                            on = 'Handle',
                            suffixes=('_daily', '_shopify'),
                            indicator = True)
    mask = df_merged['_merge'] == 'right_only'
    old_items = df_merged[mask]

    old_items = old_items[[
        "Handle", "ID", "Command", "Title_shopify", "Vendor_shopify", "Total Inventory Qty_shopify",
        "Variant ID", "Variant Barcode_shopify", "Variant Inventory Qty_shopify", "Variant Price_shopify"
    ]]

    old_items = old_items.rename(columns={
        "Title_shopify":"Title", "Vendor_shopify":"Vendor", "Total Inventory Qty_shopify":"Total Inventory Qty",
        "Variant Barcode_shopify":"Variant Barcode", "Variant Inventory Qty_shopify":"Variant Inventory Qty",
        "Variant Price_shopify":"Variant Price"
    })

    old_items[[
        "Variant Inventory Qty", "Total Inventory Qty"
    ]] = 0

    old_items["Template Suffix"] = "retrosuperfuture"

    old_items.to_excel("RSF_out.xlsx", index=False)
    old_items.to_excel(f"{PRODUCTS_OUT}/RSF_out.xlsx", index=False)

if __name__ == "__main__":
    with open(RETRO_LOGS, 'a') as file:
        try:
            rsf_out_products()
            file.write(f"[{TODAY}] RSF OUT products are updated successfully.\n")
        except Exception as err:
            file.write(f"[{TODAY}] RSF OUT products are not updated due this error:\n {type(err).__name__}: {err}")
    print("check old ended")



