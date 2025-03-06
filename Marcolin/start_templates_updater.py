import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Originals/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Sport/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Guess/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Max&Co/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/MaxMara/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Timberland/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Tom Ford/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Web/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Zegna/")

from adidas_originals_template import adidas_originals_templates_updater
from adidas_sport_templates import adidas_sport_templates_updater
from guess_templates import guess_updater_templates
from max_co_template import max_co_templates_updater
from maxmara_templates import max_mara_templates_updater
from timberland_templates import timberland_templates_update
from tom_ford_templates import tom_ford_templates_updater
from web_templates import web_templates_updater
from zegna_templates import zegna_templates_updater

if __name__ == "__main__":
    # ADIDAS ORIGINALS
    try:
        print("Updating Adidas Originals templates...")
        adidas_originals_templates_updater()
        print("Adidas Originals templates updated succesfully!")
    except Exception as err:
        print("Error during Adidas Originals templates updating")
        print(f"{type(err)}: {err}")

    # ADIDAS SPORT
    try:
        print("Updating Adidas Sport templates...")
        adidas_sport_templates_updater()
        print("Adidas Sport templates updated succesfully!")
    except Exception as err:
        print("Error during Adidas Sport templates updating")
        print(f"{type(err)}: {err}")

    # GUESS
    try:
        print("Updating Guess templates...")
        guess_updater_templates()
        print("Guess templates updated succesfully!")
    except Exception as err:
        print("Error during Guess templates updating")
        print(f"{type(err)}: {err}")

    # MAX & CO
    try:
        print("Updating Max & Co templates...")
        max_co_templates_updater()
        print("Max & Co templates updated succesfully!")
    except Exception as err:
        print("Error during Max & Co templates updating")
        print(f"{type(err)}: {err}")

    # MAX MARA
    try:
        print("Updating MaxMara templates...")
        max_mara_templates_updater()
        print("MaxMara templates updated succesfully!")
    except Exception as err:
        print("Error during MaxMara templates updating")
        print(f"{type(err)}: {err}")

    # TIMBERLAND
    try:
        print("Updating Timberland templates...")
        timberland_templates_update()
        print("Timberland templates updated succesfully!")
    except Exception as err:
        print("Error during Timberland templates updating")
        print(f"{type(err)}: {err}")

    # TOM FORD
    try:
        print("Updating Tom Ford templates...")
        tom_ford_templates_updater()
        print("Tom Ford templates updated succesfully!")
    except Exception as err:
        print("Error during Tom Ford templates updating")
        print(f"{type(err)}: {err}")

    # WEB
    try:
        print("Updating Web templates...")
        web_templates_updater()
        print("Web templates updated succesfully!")
    except Exception as err:
        print("Error during Web templates updating")
        print(f"{type(err)}: {err}")

    # ZEGNA
    try:
        print("Updating Zegna templates...")
        zegna_templates_updater()
        print("Zegna templates updated succesfully!")
    except Exception as err:
        print("Error during Zegna templates updating")
        print(f"{type(err)}: {err}")