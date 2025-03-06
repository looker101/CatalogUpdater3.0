import time
import sys
import datetime
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/De_Rigo/Police")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/De_Rigo/Porsche Design")

from police_temp import police_update
from porsche_temp import porsche_update
from de_rigo_paths import templates_logs

def derigo_templates_updater():
    # POLICE
    try:
        police_update()
        #with open(templates_logs, "a") as file:
        file.write("    Police templates updated successfully \n")
    except Exception as err:
        file.write(f"   Police are not updated due this error \n {type(err).__name__}: {err}")

    # PORSCHE DESIGN
    try:
        porsche_update()
        #with open(templates_logs, "a") as file:
        file.write("    Porsche Design templates updated successfully \n")
    except Exception as err:
        file.write(f"   Porsche Design are not updated due this error \n {type(err).__name__}: {err}")

if __name__ == "__main__":
    with open(templates_logs, "a") as file:
        try:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"\n[{current_time}] Starting DeRigo templates updater\n")
            derigo_templates_updater()
            file.write("DeRigo templates are updated successfully\n")
            file.write("Closing DeRigo templates updater\n")
        except Exception as err:
            file.write(f"DeRigo templates are not updated due this error \n {type(err).__name__}: {err}\n")
            file.write("Closing DeRigo templates updater")
            file.write("="*50 + "\n")

