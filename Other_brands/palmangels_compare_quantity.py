import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from other_brands_paths import palm_angels_shopify, palm_angels_negozi

# Shopify si riferisce al file estrpolato dal Shopify
# negozi si rifersce al file estrapolato da Focus (quantità di pezzi nei negozi)

negozi = pd.read_excel(palm_angels_negozi)
shopify = pd.read_excel(palm_angels_shopify)

# Fare merge tra i due df
df_merged = shopify.merge(negozi,
                          left_on = "Variant Barcode",
                          right_on = "Codice a barre",
                          how = "inner")

# Il prezzo e le quantità su shopify deve essere uguale al prezzo retail su focus
df_merged["Variant Compare At Price"] = df_merged["Prezzo vendita"]
df_merged["Variant Price"] = df_merged["Prezzo vendita"]
df_merged["Variant Inventory Qty"] = df_merged["Quantità magazzino"]
df_merged["Inventory Available: +39 05649689443"] = df_merged["Quantità magazzino"]

# Mantenere solo le colonne necessarie all'import su shopify
df_merged = df_merged[[
    "ID", "Command", "Title", "Variant Price", "Variant Compare At Price",
    "Variant Inventory Qty", "Inventory Available: +39 05649689443", "Variant ID", "Template Suffix"
]]

df_merged["Template Suffix"] = "Default product"

df_merged.to_excel("PalmAngels_updated.xlsx", index = False)
