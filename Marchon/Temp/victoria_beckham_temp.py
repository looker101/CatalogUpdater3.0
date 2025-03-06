import pandas as pd
import datetime
from config_paths import FTP_VICTORIA_BECKHAM_UPDATED, FTP_TEMPLATES

today = datetime.datetime.now().strftime('%d-%m')

# Variabile per il DataFrame inizializzata come None
victoria_beckham = None

try:
    victoria_beckham = pd.read_excel(FTP_VICTORIA_BECKHAM_UPDATED)
    print(f"File letto correttamente: {FTP_VICTORIA_BECKHAM_UPDATED}")
except Exception as err:
    print(f"Errore riscontrato nel file Victoria Beckham: {type(err).__name__} - {err}")
    victoria_beckham = None  # Assicura che la variabile rimanga None in caso di errore

def getMetaTitle(row):
    brand = row["Vendor"].capitalize()
    model_code = row["Variant SKU"].split()[0]
    lens_code = row["Variant SKU"].split()[1]
    frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).capitalize()
    item_type = row["Type"]
    return f"{brand} {model_code} {lens_code} - {frame_color} {item_type} | LookerOnline"

def getMetaDescript(row):
    brand = row["Vendor"]
    model_code = row["Variant SKU"].split()[0]
    color_code = row["Variant SKU"].split()[1]
    product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"].lower()
    for_who = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
    product_type = row["Type"]
    return f"New {brand} {model_code} {color_code} {product_shape} {product_type} on sale! ✓ Express Shipping ✓ 100% Original and Authentic | LookerOnline"

def getProductDescription(row):
    brand = row["Vendor"]
    model_code = row["Variant SKU"].split()[0]
    color_code = row["Variant SKU"].split()[1]
    product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"].lower()
    for_who = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
    frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
    product_type = row["Type"]

    sun = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are a perfect blend of high-fashion and modern elegance, embodying the chic and sophisticated style of the Victoria Beckham brand. Ideal for those who appreciate luxury and refined design, these sunglasses make a bold fashion statement.</span><br /></p>
<p><span style="font-weight: 400;">Handcrafted with precision, the </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> showcases the brand&rsquo;s dedication to quality and detail. Perfect for fashion-forward individuals, these sunglasses offer both style and superior comfort.</span><br /></p>
<p><span style="font-weight: 400;">Explore the latest <a href="/collections/victoria-beckham-sunglasses" target = "_blank">{brand} {product_type}</a> 2024 collection and discover eyewear that epitomizes luxury and sophistication.</span></p>"""

    eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> combine contemporary design with timeless elegance, reflecting the sophisticated style of the Victoria Beckham brand. Perfect for those who value luxury and refined aesthetics, these eyeglasses offer a chic and modern look.</span><br /></p>
<p><span style="font-weight: 400;">Crafted with high-quality materials, the </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> ensures comfort and durability for everyday wear. Ideal for individuals who appreciate high-fashion and sophistication, these eyeglasses provide both functionality and style.</span><br /></p>
<p><span style="font-weight: 400;">Discover the latest <a href="/collections/victoria-beckham-eyeglasses" target = "_blank">{brand} {product_type}</a> 2024 collection and find frames that elevate your everyday look with modern elegance.</span></p>"""

    if row["Type"] == "Sunglasses":
        return sun
    return eye

def callAllFunctions():
    if victoria_beckham is not None:
        victoria_beckham["Metafield: title_tag [string]"] = victoria_beckham.apply(getMetaTitle, axis=1)
        victoria_beckham["Metafield: description_tag [string]"] = victoria_beckham.apply(getMetaDescript, axis=1)
        victoria_beckham["Body HTML"] = victoria_beckham.apply(getProductDescription, axis=1)
        victoria_beckham.to_excel(f"{FTP_TEMPLATES}Victoria_Beckham_Templates.xlsx", index=False)
    else:
        print("Il DataFrame Victoria Beckham non è stato caricato correttamente.")

if __name__ == "__main__":
    try:
        print("Start Victoria_Beckham templates updating...")
        callAllFunctions()
        print("Victoria_Beckham templates updated succesfully!")
    except Exception as err:
        print(f"Victoria_Beckham templates not updated due to this error: {type(err).__name__} - {err}")