import datetime
import time
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marchon")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marchon/Temp")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from ferragamo_temp import ferragamo_templates_updater
from lacoste_temp import lacoste_templates_updater
from nike_temp import nike_templates_updater
from dragon_temp import dragon_templates_updater

from marchon_paths import marchon_logs_templates

def marchon_templates_updater():

    # FERRAGAMO
    try:
        ferragamo_templates_updater()
        file.write(f"   - Ferragamo template is updated correctly\n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   - Ferragamo template is not updated due this error \n {type(err).__name__}: {err}\n")

    # LACOSTE
    try:
        lacoste_templates_updater()
        file.write(f"   - Lacoste template is updated correctly\n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   - Lacoste template is not updated due this error \n {type(err).__name__}: {err}\n")

    # NIKE
    try:
        nike_templates_updater()
        file.write(f"   - Nike template is updated correctly\n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   - Nike template is not updated due this error \n {type(err).__name__}: {err}\n")

    # DRAGON
    try:
        dragon_templates_updater()
        file.write(f"   - Dragon template is updated correctly\n")
        time.sleep(1)
    except Exception as err:
        file.write(f"   - Dragon template is not updated due this error \n {type(err).__name__}: {err}\n")


if __name__ == "__main__":
    with open(marchon_logs_templates, "a") as file:
        try:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{current_time}] Starting Marchon templates updater \n")
            marchon_templates_updater()
            file.write(f"Marchon templates are updated successfully\n")
            ending_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{ending_time}] Closing Marchon templates updater \n")
            file.write("="*50 + "\n")

        except Exception as err:
            file.write(f"Marchon templates are not updated due this error \n {type(err).__name__}: {err}\n")
            file.write(f"[{ending_time}] Closing Marchon templates updater \n")
            file.write("=" * 50 + "\n")