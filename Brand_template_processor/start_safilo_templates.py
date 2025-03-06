import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/Carrera")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/David Beckham")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/Fossil")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/Kate Spade")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/Marc Jacobs")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/Moschino")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/Polaroid")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/Tommy Hilfiger")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Safilo/Under Armour")

from carrera_templates import carrera_templates_update
from david_beckham_templates import david_beckham_templates_update
from fossil_templates import fossil_templates_update
from kate_spade_templates import kate_spade_templates_update
from marc_jacobs_templates import marc_jacobs_templates_update
from moschino_templates import moschino_templates_update
from polaroid_templates import polaroid_templates_update
from tommy_hilfiger_templates import tommy_hilfiger_templates_update
from under_armour_templates import under_armour_templates_update
from safilo_paths import TODAY, safilo_logs_templates

def safilo_templates_updater():
    # CARRERA
    try:
        carrera_templates_update()
        with open(safilo_logs_templates, "a") as file:
            file.write("    Carrera templates updated successfully \n")
            print("Carrera OK")
    except Exception as err:
        file.write(f"   Carrera are not updated due this error \n {type(err).__name__}: {err}")
        print(f"   Carrera are not updated due this error \n {type(err).__name__}: {err}")

    # DAVID BECKHAM
    try:
        david_beckham_templates_update()
        with open(safilo_logs_templates, "a") as file:
            file.write("    David Beckham templates updated successfully \n")
            print("Beckahm OK")
    except Exception as err:
        with open(safilo_logs_templates, "a") as file:
            file.write(f"   David Beckham are not updated due this error \n {type(err).__name__}: {err}")
            print(f"   Beckham are not updated due this error \n {type(err).__name__}: {err}")

    # FOSSIL
    # try:
    #     fossil_templates_update()
    #     with open(safilo_logs_templates, "a") as file:
    #         file.write("    Fossil templates updated successfully \n")
    #         print("Fossil OK")
    # except Exception as err:
    #     with open(safilo_logs_templates, "a") as file:
    #         file.write(f"   Fossil are not updated due this error \n {type(err).__name__}: {err}")
    #         print(f"   Fossil are not updated due this error \n {type(err).__name__}: {err}")

    # KATE SPADE
    # try:
    #     kate_spade_templates_update()
    #     with open(safilo_logs_templates, "a") as file:
    #         file.write("    Kate Spade templates updated successfully \n")
    # except Exception as err:
    #     with open(safilo_logs_templates, "a") as file:
    #         file.write(f"   Kate Spade are not updated due this error \n {type(err).__name__}: {err}")

    # MARC JACOBS
    try:
        marc_jacobs_templates_update()
        with open(safilo_logs_templates, "a") as file:
            file.write("    Marc Jacobs templates updated successfully \n")
    except Exception as err:
        with open(safilo_logs_templates, "a") as file:
            file.write(f"   Marc Jacobs are not updated due this error \n {type(err).__name__}: {err}")

    # MOSCHINO
    try:
        moschino_templates_update()
        with open(safilo_logs_templates, "a") as file:
            file.write("    Moschino templates updated successfully \n")
    except Exception as err:
        with open(safilo_logs_templates, "a") as file:
            file.write(f"   Moschino are not updated due this error \n {type(err).__name__}: {err}")

    # POLAROID
    try:
        polaroid_templates_update()
        with open(safilo_logs_templates, "a") as file:
            file.write("    Polaroid templates updated successfully \n")
    except Exception as err:
        with open(safilo_logs_templates, "a") as file:
            file.write(f"   Polaroid are not updated due this error \n {type(err).__name__}: {err}")

    # TOMMY HILFIGER
    try:
        tommy_hilfiger_templates_update()
        with open(safilo_logs_templates, "a") as file:
            file.write("    Tommy Hilfiger templates updated successfully \n")
    except Exception as err:
        with open(safilo_logs_templates, "a") as file:
            file.write(f"   Tommy Hilfiger are not updated due this error \n {type(err).__name__}: {err}")

    # UNDER ARMOUR
    try:
        under_armour_templates_update()
        with open(safilo_logs_templates, "a") as file:
            file.write("    Under Armour templates updated successfully \n")
    except Exception as err:
        with open(safilo_logs_templates, "a") as file:
            file.write(f"   Under Armour are not updated due this error \n {type(err).__name__}: {err}")

if __name__ == "__main__":
    try:
        with open(safilo_logs_templates, "a") as file:
            file.write('\n'+"=" *50+ '\n')
            file.write(f"[{TODAY}] Starting Safilo templates getter \n")
            file.write("-"*50+'\n')

        safilo_templates_updater()
        with open(safilo_logs_templates, "a") as file:
            file.write("-" * 50 + '\n')
            file.write("Safilo templates are updated successfully \n")
            file.write(f"[{TODAY}] Closing Safilo templates getter \n")
    except Exception as err:
        with open(safilo_logs_templates, "a") as file:
            file.write("-" * 50 + '\n')
            file.write(f"[{TODAY}] Safilo templates are not updated due this error: \n {type(err).__name__}: {err}")