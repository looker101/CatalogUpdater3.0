import pandas as pd
import datetime
from config_paths import FTP_CALVIN_KLEIN_UPDATED, FTP_TEMPLATES

today = datetime.datetime.now().strftime('%d-%m')

try:
     calvin_klein = pd.read_excel(FTP_CALVIN_KLEIN_UPDATED)
     print(f"File letto correttamente: {FTP_CALVIN_KLEIN_UPDATED}")
except Exception as err:
    print(f"Errore nel file template Calvin Klein.py: type{err}.__name__")


def getMetaTitle(row):
    brand = row["Vendor"].capitalize()
    model_code = row["Variant SKU"].split()[0]
    lens_code = row["Variant SKU"].split()[1]
    frame_color = str(row["Metafield: my_fields.frame_color [single_line_text_field]"]).capitalize()
    item_type = row["Type"]
    return f"{brand} {model_code} {lens_code} - {frame_color} {item_type} | LookerOnline"


def getMetaDescript(row):
    # {brand} {codice del modello} {codice del colore} {frame_colore} {forma} {genere} {tipologia}
    brand = row["Vendor"]
    model_code = row["Variant SKU"].split()[0]
    color_code = row["Variant SKU"].split()[1]
    product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"].lower()
    for_who = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
    product_type = row["Type"]
    # frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
    return f"New {brand} {model_code} {color_code} {product_shape} {product_type} on sale! ✓ Express Shipping ✓ 100% Original and Authentic | LookerOnline"


def getProductDescription(row):
    brand = row["Vendor"]
    model_code = row["Variant SKU"].split()[0]
    color_code = row["Variant SKU"].split()[1]
    product_shape = row["Metafield: my_fields.frame_shape [single_line_text_field]"].lower()
    for_who = row["Metafield: my_fields.for_who [single_line_text_field]"].lower()
    frame_color = row["Metafield: my_fields.frame_color [single_line_text_field]"]
    product_type = row["Type"]

    sun = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> are the epitome of minimalist sophistication, combining sleek design with modern aesthetics. Ideal for those who appreciate clean lines and understated elegance, these sunglasses reflect the iconic Calvin Klein brand.</span><br /></p>
<p><span style="font-weight: 400;">Crafted with meticulous attention to detail, the </span><strong>{frame_color} {model_code} </strong><span style="font-weight: 400;"> offers both style and comfort. Perfect for fashion-forward individuals, these sunglasses add a touch of sophistication to any look.</span><br /></p>
<p><span style="font-weight: 400;">Explore the latest <a href="/collections/calvin-klein-sunglasses" target="_blank">{brand} {product_type}</a> 2024 collection and discover eyewear that embodies the essence of modern minimalism.</span></p>"""

    eye = f"""<p><strong>{brand} {product_type}</strong><span style="font-weight: 400;"> offer a refined blend of contemporary design and classic elegance, perfect for those who value simplicity and sophistication. Reflecting the minimalist aesthetic of the Calvin Klein brand, these eyeglasses provide a sleek and modern look.</span><br /></p>
<p><span style="font-weight: 400;">Made with high-quality materials, the </span><strong>{frame_color} {model_code}</strong><span style="font-weight: 400;"> ensures durability and comfort for everyday wear. Ideal for individuals who appreciate timeless style, these eyeglasses offer both functionality and fashion.</span><br /></p>
<p><span style="font-weight: 400;">Discover the latest <a href="/collections/calvin-klein-eyeglasses" target = "_blank">{brand} {product_type}</a> 2024 collection and find frames that elevate your everyday style with minimalist elegance.</span></p>"""

    if row["Type"] == "Sunglasses":
        return sun
    return eye


def callAllFunctions():
    calvin_klein["Metafield: title_tag [string]"] = calvin_klein.apply(getMetaTitle, axis=1)
    calvin_klein["Metafield: description_tag [string]"] = calvin_klein.apply(getMetaDescript, axis=1)
    calvin_klein["Body HTML"] = calvin_klein.apply(getProductDescription, axis=1)
    calvin_klein.to_excel(f"{FTP_TEMPLATES}Calvin_Klein_Templates.xlsx", index=False)
    #calvin_klein.to_excel("C:\\Users\\miche\\Desktop\\.py\\catalog_price\\Brand\\CALVIN KLEIN.xlsx", index=False)

if __name__ == "__main__":
    try:
        print("Start Calvin Klein templates updating...")
        callAllFunctions()
        print("Calvin Klein templates updated succesfully!")
    except Exception as err:
        print(f"Calvin Klein templates not updated due this error: {type(err).__name__} - > {err}")

