import time
import sys
import datetime

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Arnette/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Burberry/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Dolce & gabbana/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Emporio Armani/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Giorgio Armani/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Miu Miu/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Michael Kors/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Oakley/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Persol/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Prada/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Prada Linea Rossa/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Ralph/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Ray-Ban/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Swarovski/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Tiffany/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Versace/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Vogue Eyewear/")

from Arnette_IMG_updater import get_arnette_images
from Burberry_IMG_updater import get_burberry_images
from Dolce_Gabbana_IMG_updater import get_dg_images
from Emporio_Armani_IMG_updater import get_emporio_armani_images
from Giorgio_Armani_IMG_updater import get_giorgio_armani_images
from Michael_Kors_IMG_updater import get_michael_kors_images
from MiuMiu_IMG_updater import get_miu_miu_images
from Oakley_IMG_updater import get_oakley_images
from Persol_IMG_updater import get_persol_images
from Prada_IMG_updater import get_prada_images
from PLR_IMG_updater import get_PLR_images
from ralph_IMG_updater import get_ralph_images
from Ray_Ban_IMG_updater import get_ray_ban_images
from Swarovski_IMG_updater import get_swarovski_images
from Tiffany_IMG_updater import get_tiffany_images
from Versace_IMG_updater import get_versace_images
from Vogue_IMG_updater import get_vogue_images
from luxottica_paths import luxottica_new_products, get_images_logs

today = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")

def get_luxottica_images():
    #log_file_path = f"{get_images_logs}/Luxottica_images_logs.txt"

    def log_message(message):
        with open(get_images_logs, "a") as log_file:
            log_file.write(f"{message}\n")

    # ARNETTE
    try:
        print("Getting Arnette images for new products...")
        time.sleep(1)
        get_arnette_images()
        print("Arnette's images inserted on Arnette_IMG")
        log_message(f"Arnette's images inserted on Arnette_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Arnette")
        log_message(f"There are not new products for the brand Arnette")
    except Exception as err:
        print("Something went wrong during Arnette images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Arnette images update - {type(err).__name__}: {err}")

    # BURBERRY
    try:
        print("Getting Burberry images for new products...")
        time.sleep(1)
        get_burberry_images()
        print("Burberry's images inserted on Burberry_IMG")
        log_message(f"Burberry's images inserted on Burberry_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Burberry")
        log_message(f"There are not new products for the brand Burberry")
    except Exception as err:
        print("Something went wrong during Burberry images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Burberry images update - {type(err).__name__}: {err}")

    # DOLCE & GABBANA
    try:
        print("Getting Dolce & Gabbana images for new products...")
        time.sleep(1)
        get_dg_images()
        print("Dolce & Gabbana's images inserted on Dolce & Gabbana_IMG")
        log_message(f"Dolce & Gabbana's images inserted on Dolce & Gabbana_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Dolce & Gabbana")
        log_message(f"There are not new products for the brand Dolce & Gabbana")
    except Exception as err:
        print("Something went wrong during Dolce & Gabbana images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Dolce & Gabbana images update - {type(err).__name__}: {err}")

    # EMPORIO ARMANI
    try:
        print("Getting Emporio Armani images for new products...")
        time.sleep(1)
        get_emporio_armani_images()
        print("Emporio Armani's images inserted on Emporio Armani_IMG")
        log_message(f"Emporio Armani's images inserted on Emporio Armani_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Emporio Armani")
        log_message(f"There are not new products for the brand Emporio Armani")
    except Exception as err:
        print("Something went wrong during Emporio Armani images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Emporio Armani images update - {type(err).__name__}: {err}")

    # GIORGIO ARMANI
    try:
        print("Getting Giorgio Armani images for new products...")
        time.sleep(1)
        get_giorgio_armani_images()
        print("Giorgio Armani's images inserted on Giorgio Armani_IMG")
        log_message(f"Giorgio Armani's images inserted on Giorgio Armani_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Giorgio Armani")
        log_message(f"There are not new products for the brand Giorgio Armani")
    except Exception as err:
        print("Something went wrong during Giorgio Armani images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Giorgio Armani images update - {type(err).__name__}: {err}")

    # MICHAEL KORS
    try:
        print("Getting Michael Kors images for new products...")
        time.sleep(1)
        get_michael_kors_images()
        print("Michael Kors's images inserted on Michael Kors_IMG")
        log_message(f"Michael Kors's images inserted on Michael Kors_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Michael Kors")
        log_message(f"There are not new products for the brand Michael Kors")
    except Exception as err:
        print("Something went wrong during Michael Kors images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Michael Kors images update - {type(err).__name__}: {err}")

    # MIU MIU
    try:
        print("Getting Miu Miu images for new products...")
        time.sleep(1)
        get_miu_miu_images()
        print("Miu Miu's images inserted on Miu Miu_IMG")
        log_message(f"Miu Miu's images inserted on Miu Miu_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Miu Miu")
        log_message(f"There are not new products for the brand Miu Miu")
    except Exception as err:
        print("Something went wrong during Miu Miu images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Miu Miu images update - {type(err).__name__}: {err}")

    # OAKLEY
    try:
        print("Getting Oakley images for new products...")
        time.sleep(1)
        get_oakley_images()
        print("Oakley's images inserted on Oakley_IMG")
        log_message(f"Oakley's images inserted on Oakley_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Oakley")
        log_message(f"There are not new products for the brand Oakley")
    except Exception as err:
        print("Something went wrong during Oakley images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Oakley images update - {type(err).__name__}: {err}")
    
    # RALPH
    try:
        print("Getting Ralph images for new products...")
        time.sleep(1)
        get_ralph_images()
        print("Ralph's images inserted on Ralph_IMG")
        log_message(f"Ralph's images inserted on Ralph_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Ralph")
        log_message(f"There are not new products for the brand Ralph")
    except Exception as err:
        print("Something went wrong during Ralph images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Ralph images update - {type(err).__name__}: {err}")
    
    # RAY-BAN
    try:
        print("Getting Ray-Ban images for new products...")
        time.sleep(1)
        get_ray_ban_images()
        print("Ray-Ban's images inserted on Ray-Ban_IMG")
        log_message(f"Ray-Ban's images inserted on Ray-Ban_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Ray-Ban")
        log_message(f"There are not new products for the brand Ray-Ban")
    except Exception as err:
        print("Something went wrong during Ray-Ban images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Ray-Ban images update - {type(err).__name__}: {err}")

    # PERSOL
    try:
        print("Getting Persol images for new products...")
        time.sleep(1)
        get_persol_images()
        print("Persol's images inserted on Persol_IMG")
        log_message(f"Persol's images inserted on Persol_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Persol")
        log_message(f"There are not new products for the brand Persol")
    except Exception as err:
        print("Something went wrong during Persol images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Persol images update - {type(err).__name__}: {err}")

    # PRADA
    try:
        print("Getting Prada images for new products...")
        time.sleep(1)
        get_prada_images()
        print("Prada's images inserted on Prada_IMG")
        log_message(f"Prada's images inserted on Prada_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Prada")
        log_message(f"There are not new products for the brand Prada")
    except Exception as err:
        print("Something went wrong during Prada images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Prada images update - {type(err).__name__}: {err}")

    # PRADA LINEA ROSSA
    try:
        print("Getting Prada Linea Rossa images for new products...")
        time.sleep(1)
        get_PLR_images()
        print("Prada Linea Rossa's images inserted on Prada Linea Rossa_IMG")
        log_message(f"Prada Linea Rossa's images inserted on Prada Linea Rossa_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Prada Linea Rossa")
        log_message(f"There are not new products for the brand Prada Linea Rossa")
    except Exception as err:
        print("Something went wrong during Prada Linea Rossa images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Prada Linea Rossa images update - {type(err).__name__}: {err}")

    # SWAROVSKI
    try:
        print("Getting Swarovski images for new products...")
        time.sleep(1)
        get_swarovski_images()
        print("Swarovski's images inserted on Swarovski_IMG")
        log_message(f"Swarovski's images inserted on Swarovski_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Swarovski")
        log_message(f"There are not new products for the brand Swarovski")
    except Exception as err:
        print("Something went wrong during Swarovski images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Swarovski images update - {type(err).__name__}: {err}")

    # TIFFANY
    try:
        print("Getting Tiffany images for new products...")
        time.sleep(1)
        get_tiffany_images()
        print("Tiffany's images inserted on Tiffany_IMG")
        log_message(f"Tiffany's images inserted on Tiffany_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Tiffany")
        log_message(f"There are not new products for the brand Tiffany")
    except Exception as err:
        print("Something went wrong during Tiffany images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Tiffany images update - {type(err).__name__}: {err}")

    # VERSACE
    try:
        print("Getting Versace images for new products...")
        time.sleep(1)
        get_versace_images()
        print("Versace images inserted on Versace_IMG")
        log_message(f"Versace images inserted on Versace_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Versace")
        log_message(f"There are not new products for the brand Versace")
    except Exception as err:
        print("Something went wrong during Versace images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Versace images update - {type(err).__name__}: {err}")

    # VOGUE EYEWEAR
    try:
        print("Getting Vogue images for new products...")
        time.sleep(1)
        get_vogue_images()
        print("Vogue images inserted on Vogue_IMG")
        log_message(f"Vogue images inserted on Vogue_IMG")
    except FileNotFoundError:
        print("There are not new products for the brand Vogue Eyewear")
        log_message(f"There are not new products for the brand Vogue Eyewear")
    except Exception as err:
        print("Something went wrong during Vogue images updated")
        print(f"{type(err).__name__}; {err}")
        log_message(f"Something went wrong during Vogue images update - {type(err).__name__}: {err}")


if __name__ == "__main__":
    try:
        with open(get_images_logs, "a") as file:
            file.write("="*50 + f"\n [{today}] STARTING LUXOTTICA IMAGES GETTER \n")
            file.write("-" * 50 +"\n")
        get_luxottica_images()

        with open(get_images_logs, "a") as file:
            file.write("-" * 50 +"\n")
            file.write(f"[{today}] CLOSING LUXOTTICA IMAGES GETTER \n")
            file.write("LUXOTTICA IMAGES ARE UPDATED SUCCESSFULLY \n")

    except Exception as err:
        with open(log_file_path, "a") as file:
            file.write("-"*50 + "\n")
            file.write(f"[{today}] LUXOTTICA IMAGES ARE NOT UPDATED DUE THIS ERROR \n {type(err).__name__}: {err}\n")
            file.write("="*50 + "\n")
