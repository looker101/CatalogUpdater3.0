import sys
import time
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Alexander McQueen")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Balenciaga")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Bottega Veneta")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Chloe")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Gucci")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Saint Laurent")

from amq_templates import amq_templates_updater
from balenciaga_templates import balenciaga_templates_updater
from bottega_veneta_templates import bottega_veneta_templates_updater
from chloe_templates import chloe_templates_updater
from gucci_templates import gucci_templates_updater
from saint_laurent_templates import sl_templates_updater
from kering_paths import TODAY, logs_templates

def kering_templates_updater():
    # AMQ
    try:
        amq_templates_updater()
        with open(logs_templates, "a") as file:
            file.write("    AMQ templates updated successfully \n")
    except Exception as err:
        file.write(f"   AMQ are not updated due this error \n {type(err).__name__}: {err}")

    # BALENCIAGA
    try:
        balenciaga_templates_updater()
        with open(logs_templates, "a") as file:
            file.write("    Balenciaga templates updated successfully \n")
    except Exception as err:
        file.write(f"   Balenciaga are not updated due this error \n {type(err).__name__}: {err}")

    # BOTTEGA VENETA
    try:
        bottega_veneta_templates_updater()
        with open(logs_templates, "a") as file:
            file.write("    Bottega Veneta templates updated successfully \n")
    except Exception as err:
        file.write(f"   Bottega Veneta are not updated due this error \n {type(err).__name__}: {err}")

    # CHLOE
    try:
        chloe_templates_updater()
        with open(logs_templates, "a") as file:
            file.write("    Chloe templates updated successfully \n")
    except Exception as err:
        file.write(f"   Chloe are not updated due this error \n {type(err).__name__}: {err}")

    # GUCCI
    try:
        gucci_templates_updater()
        with open(logs_templates, "a") as file:
            file.write("    Gucci templates updated successfully \n")
    except Exception as err:
        file.write(f"   Gucci are not updated due this error \n {type(err).__name__}: {err}")

    # SAINT LAURENT
    try:
        sl_templates_updater()
        with open(logs_templates, "a") as file:
            file.write("    Saint Laurent templates updated successfully \n")
    except Exception as err:
        file.write(f"   Saint Laurent are not updated due this error \n {type(err).__name__}: {err}")

if __name__ == "__main__":
    try:
        with open(logs_templates, "a") as file:
            file.write('\n'+"=" *50+ '\n')
            file.write(f"[{TODAY}] Starting Kering templates getter \n")
            file.write("-"*50+'\n')

        kering_templates_updater()
        with open(logs_templates, "a") as file:
            file.write("-" * 50 + '\n')
            file.write("Kering templates are updated successfully \n")
            file.write(f"[{TODAY}] Closing Kering templates getter \n")
    except Exception as err:
        with open(logs_templates, "a") as file:
            file.write("-" * 50 + '\n')
            file.write(f"[{TODAY}] Kering templates are not updated due this error: \n {type(err).__name__}: {err}")


