import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")
import time
from start_luxottica_templates import process_template, get_arnette_template, get_burberry_temp, get_dolce_gabbana_template,\
    get_emporio_armani_templates, get_giorgio_armani_templates, get_michael_kors_templates, get_miu_miu_templates,\
    get_oakley_templates, get_persol_templates, get_prada_templates, get_prada_linea_rossa_templates, get_ray_ban_templates,\
    get_swarovski_templates, get_tiffany_templates, get_versace_templates, get_vogue_templates
from start_kering_templates import start_kering_templates_updater
from start_marchon_templates import marchon_templates_updater
from start_marcolin_templates import start_marcolin_templates_updater
from start_rsf_templates import rsf_templates
from start_safilo_templates import safilo_templates_updater
from start_de_rigo_templates import start_derigo_updater
from safilo_paths import TODAY, logs_folder

def templates_updater():
    """ALL Templates updater"""
    with open(f"{logs_folder}/All_templates_logs.txt", "a") as file:
        # LUXOTTICA
        try:
            print("Start Luxottica products templates...")
            process_template("Arnette", get_arnette_template)
            process_template("Burberry", get_burberry_temp)
            process_template("Dolce & Gabbana", get_dolce_gabbana_template)
            process_template("Emporio Armani", get_emporio_armani_templates)
            process_template("Giorgio Armani", get_giorgio_armani_templates)
            process_template("Michael Kors", get_michael_kors_templates)
            process_template("Miu Miu", get_miu_miu_templates)
            process_template("Oakley", get_oakley_templates)
            process_template("Persol", get_persol_templates)
            process_template("Prada", get_prada_templates)
            process_template("Prada Linea Rossa", get_prada_linea_rossa_templates)
            process_template("Ray-Ban", get_ray_ban_templates)
            process_template("Swarovski", get_swarovski_templates)
            process_template("Tiffany", get_tiffany_templates)
            process_template("Versace", get_versace_templates)
            process_template("Vogue", get_vogue_templates)
            print("Luxottica templates updated successfully!")
            file.write(f"{TODAY} LUXOTTICA LOGS: all templates are successfully updated!\n")
        except Exception as err:
            file.write(f"{TODAY} Luxottica logs: Luxottica templates are not updated due to this error \n {type(err).__name__} -> {err}\n")

        time.sleep(1)

        # KERING
        try:
            print("Start Kering products templates...")
            start_kering_templates_updater()
            print("Kering products templates are successfully updated")
            file.write(f"{TODAY} Log of Kering templates: All items successfully updated\n")
        except Exception as err:
            file.write(f"{TODAY} Log of Kering templates: Kering products not updated due to this error: \n {type(err).__name__} -> {err}\n")

        time.sleep(1)

        # MARCHON
        try:
            print("Start updating Marchon templates...")
            marchon_templates_updater()
            print("All Marchon templates updated successfully.")
            file.write(f"{TODAY} Marchon Log: All items are successfully updated\n")
        except Exception as err:
            print(f"Marchon templates are not updated due to this error {type(err).__name__}: {err}")
            file.write(f"{TODAY} Marchon Log: Item templates are not updated due to this error.\n {type(err).__name__}: {err}\n")

        time.sleep(1)

        # MARCOLIN
        try:
            print("Start updating Marcolin templates...")
            start_marcolin_templates_updater()
            print("Marcolin templates are updated successfully!")
            file.write(f"{TODAY} Marcolin templates log: all templates are successfully updated!\n")
        except Exception as err:
            print(f"Marcolin templates are not updated due to this error {type(err).__name__}: {err}")
            file.write(f"{TODAY} Marcolin templates log: templates are not updated due to this error!\n {type(err).__name__} -> {err}\n")

        time.sleep(1)

        # RSF
        try:
            print("Updating RetroSuperFuture templates...")
            rsf_templates()
            print("Templates RetroSuperFuture updated.")
            file.write(f"{TODAY} RSF TEMPLATES LOG: RetroSuperFuture templates are updated successfully!\n")
        except Exception as err:
            print(f"RetroSuperFuture templates are not updated due to this error {type(err).__name__}: {err}")
            file.write(f"{TODAY} RSF TEMPLATES LOG: RetroSuperFuture templates items not updated due to this error: {type(err).__name__}: {err}\n")

        time.sleep(1)

        # SAFILO
        try:
            print("Start Safilo items updater...")
            safilo_templates_updater()
            print("Safilo templates are successfully updated!")
            file.write(f"{TODAY} Safilo templates logs: all templates are successfully updated!\n")
        except Exception as err:
            print(f"Safilo templates are not updated due to this error {type(err).__name__}: {err}")
            file.write(f"{TODAY} Safilo templates logs: templates are not updated due to this error! {type(err).__name__} -> {err}\n")
            
        # DERIGO
        try:
            print("Start De Rigo items updater...")
            start_derigo_updater()
            print("De Rigo templates are successfully updated!")
            file.write(f"{TODAY} De Rigo templates logs: all templates are successfully updated!\n")
        except Exception as err:
            print(f"De Rigo templates are not updated due to this error {type(err).__name__}: {err}")
            file.write(f"{TODAY} De Rigo templates logs: templates are not updated due to this error! {type(err).__name__} -> {err}\n")
        

if __name__ == "__main__":
    templates_updater()
