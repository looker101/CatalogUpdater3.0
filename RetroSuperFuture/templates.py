import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
from retro_paths import RETRO_UPDATE, RETRO_LOGS, TODAY, TEMPLATES

def rsf_templates():
    # metafields = pd.read_excel("RetroMetafields.xlsx")
    metafields = pd.read_excel(RETRO_UPDATE)

    # METADESCRIPTION
    def metaDescript(row):
        model = row["Title"].split()
        sku = row["Handle"]
        return f"Buy the new {model[0]} {model[1]} {sku} sunglasses at a bargain price. This super stylish, unique {model[-1]} model is the ideal choice for mand & woman | FREE SHIPPING |"

    metafields["Title"] = metafields["Title"].astype(str)
    metafields["Metafield: description_tag [string]"] = metafields["Metafield: description_tag [string]"].astype(str)
    metafields["Metafield: description_tag [string]"] = metafields.apply(metaDescript, axis=1)

    metafields["Variant Inventory Qty"] = metafields["Variant Inventory Qty"].fillna(0)

    metafields["Inventory Available: +39 05649689443"] = metafields["Variant Inventory Qty"]

    # METATITLE
    def metaTitle(row):
        # model = row["Title"].split()
        return f'{row["Title"]} for men and women | LookerOnline'

    metafields["Metafield: title_tag [string]"] = metafields.apply(metaTitle, axis=1)

    # PRODUCT DESCRIPTION
    def bodyHtmlSunOrOptical(row):
        model = row["Title"]
        # SOLE
        anchor_text_sun = "Retrosuperfuture sunglasses 2025"
        url_sun = "https://lookeronline.com/collections/retrosuperfuture-sunglasses"
        # VISTA
        anchor_text_eye = "Retrosuperfuture Eyeglasses 2025"
        url_eye = "https://lookeronline.com/collections/retrosuperfuture-eyeglasses"
        descript_sun = (
            "<strong>Retrosuperfuture sunglasses</strong> stand at the forefront of contemporary eyewear, known for their distinct blend of modern aesthetics and impeccable craftsmanship.<br />"
            "These sunglasses are designed for those who value individuality and style and are a testament to Italian design excellence.\n <br /><br />"
            f"The <strong>{model} </strong>model, with its unique frame and high-quality lenses, embodies the brand’s dedication to creating bold and innovative eyewear. <br />"
            "Each pair is meticulously handcrafted in Italy, ensuring a striking appearance, durability, and comfort.\n <br /><br />"
            f'Check out all the latest models and designs in the new <a href={url_sun}> {anchor_text_sun} </a> collection and find the perfect pair that reflects your unique style.<br />'
        )

        descript_eye = (
            "<strong>Retrosuperfuture sunglasses</strong> stand at the forefront of contemporary eyewear, known for their distinct blend of modern aesthetics and impeccable craftsmanship.<br />"
            "These sunglasses are designed for those who value individuality and style and are a testament to Italian design excellence.\n <br /><br />"
            f"The <strong>{model} </strong>model, with its unique frame and high-quality lenses, embodies the brand’s dedication to creating bold and innovative eyewear. <br />"
            "Each pair is meticulously handcrafted in Italy, ensuring a striking appearance, durability, and comfort.\n <br /><br />"
            f'Check out all the latest models and designs in the new <a href={url_eye}> {anchor_text_eye} </a> collection and find the perfect pair that reflects your unique style.<br />'
        )

        if row["Type"] == "Eyeglasses":
            return descript_eye
        return descript_sun

    metafields["Body HTML"] = metafields.apply(bodyHtmlSunOrOptical, axis=1)

    metafields = metafields.sort_values(by="Handle")

    # AGGIUNGI FUNZIONE GET_IMAGES
    def get_images(df):
        # Concateno le immagini per ogni handle separandole con ";"
        images = df.groupby('Handle')['Image Src'].agg(lambda x: ";".join(x.dropna().unique()))
        # Unisco le immagini concatenate al DataFrame originale
        df = df.drop(columns=['Image Src']).drop_duplicates('Handle')
        df = df.merge(images, on='Handle', how='left')
        return df

    # Applica la funzione get_images al DataFrame
    metafields = get_images(metafields)

    #metafields = metafields.dropna()

    metafields.to_excel("Retro_Templates.xlsx", index=False)
    metafields.to_excel(f"{TEMPLATES}/RSF_templates.xlsx", index=False)


if __name__ == "__main__":
    with open(RETRO_LOGS, "a") as file:
        try:
            rsf_templates()
            file.write(f"[{TODAY}] RSF Templates are updated successfully! \n")
        except Exception as err:
            file.write(f"[{TODAY}] RSF Templates are not updated due this error: \n {type(err).__name__}: {err}")