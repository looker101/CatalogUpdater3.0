import datetime
import time
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
from pucci_templates import pucci_templates_updater
from guess_templates import guess_updater_templates
from max_co_template import max_co_templates_updater
from maxmara_templates import max_mara_templates_updater
from timberland_templates import timberland_templates_update
from tom_ford_templates import tom_ford_templates_updater
from web_templates import web_templates_updater
from zegna_templates import zegna_templates_updater

from marcolin_paths import templates_logs

def marcolin_templates_updater():
    # ADIDAS ORIGINALS
    try:
        adidas_originals_templates_updater()

        file.write("    Adidas Originals templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Adidas Originals are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)

    # ADIDAS SPORT
    try:
        adidas_sport_templates_updater()
        file.write("    Adidas Sport templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Adidas Sport are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)


    # EMILIO PUCCI
    try:
        pucci_templates_updater()
        file.write("    Emilio Pucci templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Emilio Pucci are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)

    # GUESS
    try:
        guess_updater_templates()
        file.write("    Guess templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Guess are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)

    # MAX & CO
    try:
        max_co_templates_updater()
        file.write("    Max & Co templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Max & Co are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)

    # MAX MARA
    try:
        max_mara_templates_updater()
        file.write("    Max Mara templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Max Mara are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)

    # TIMBERLAND
    try:
        timberland_templates_update()
        file.write("    Timberland templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Timberland are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)

    # TOM FORD
    try:
        tom_ford_templates_updater()
        file.write("    Tom Ford templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Tom Ford are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)

    # WEB
    try:
        web_templates_updater()
        file.write("    Web templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Web are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)

    # ZEGNA
    try:
        zegna_templates_updater()
        file.write("    Zegna templates updated successfully \n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   Zegna are not updated due this error \n {type(err).__name__}: {err}")
        time.sleep(1)

if __name__ == "__main__":
    with open(templates_logs, "a") as file:
        try:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write('\n'+"=" *50+ '\n')
            file.write(f"[{current_time}] Starting Marcolin templates getter \n")
            file.write("-"*50+'\n')

            marcolin_templates_updater()
            file.write("-" * 50 + '\n')
            file.write("Marcolin templates are updated successfully \n")
            file.write(f"Closing Marcolin templates getter \n")
        except Exception as err:
            file.write("-" * 50 + '\n')
            file.write(f"Marcolin templates are not updated due this error: \n {type(err).__name__}: {err}")
