import sys
import time
import datetime

# Re-append each path as you had in the original code
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Arnette/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Burberry/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Dolce & gabbana/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Emporio Armani/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Giorgio Armani/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Michael Kors/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Miu Miu/")
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
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

# Import statements exactly as you had them
from Arnette_Temp import get_arnette_template
from Burberry_temp import get_burberry_temp
from Dolce_Gabbana_temp import get_dolce_gabbana_template
from Emporio_Armani_Temp import get_emporio_armani_templates
from Giorgio_Armani_Temp import get_giorgio_armani_templates
from Michael_Kors_Temp import get_michael_kors_templates
from MiuMiu_Temp import get_miu_miu_templates
from Oakley_Temp import get_oakley_templates
from Persol_Temp import get_persol_templates
from Prada_Temp import get_prada_templates
from PLR_Temp import get_prada_linea_rossa_templates
from ralph_templates import get_ralph_templates
from Ray_Ban_Temp import get_ray_ban_templates
from Swarovski_Temp import get_swarovski_templates
from Tiffany_Temp import get_tiffany_templates
from Versace_Temp import get_versace_templates
from Vogue_Temp import get_vogue_templates
from luxottica_paths import get_templates

print("Run start_temp.py")
time.sleep(1)

def get_luxottica_templates():

    # ARNETTE
    try:
        get_arnette_template()
        with open(get_templates, "a") as file:
            file.write(f"   Arnette templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Arnette are not updated due this error \n {type(err).__name__}: {err}")
    
    # BURBERRY
    try:
        get_burberry_temp()
        with open(get_templates, "a") as file:
            file.write(f"   Burberry templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Burberry are not updated due this error \n {type(err).__name__}: {err}")    
            
    # DOLCE & GABBANA
    try:
        get_dolce_gabbana_template()
        with open(get_templates, "a") as file:
            file.write(f"   Dolce & Gabbana templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Dolce & Gabbana are not updated due this error \n {type(err).__name__}: {err}")
    
    # EMPORIO ARMANI
    try:
        get_emporio_armani_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Emporio Armani templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Emporio Armani are not updated due this error \n {type(err).__name__}: {err}")
    
    # GIORGIO ARMANI
    try:
        get_giorgio_armani_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Giorgio Armani templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Giorgio Armani are not updated due this error \n {type(err).__name__}: {err}")
            
    # MICHAEL KORS
    try:
        get_michael_kors_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Michael Kors templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Michael Kors are not updated due this error \n {type(err).__name__}: {err}")
            
    # MIU MIU
    try:
        get_miu_miu_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Miu Miu templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Miu Miu are not updated due this error \n {type(err).__name__}: {err}")
            
    # OAKLEY
    try:
        get_oakley_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Oakley templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Oakley are not updated due this error \n {type(err).__name__}: {err}")
            
    # PERSOL
    try:
        get_persol_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Persol templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Persol are not updated due this error \n {type(err).__name__}: {err}")
            
    # PRADA
    try:
        get_prada_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Prada templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Prada are not updated due this error \n {type(err).__name__}: {err}")
            
    # PRADA LINEA ROSSA
    try:
        get_prada_linea_rossa_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Prada Linea Rossa templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Prada Linea Rossa are not updated due this error \n {type(err).__name__}: {err}")
            
    # RALPH
    try:
        get_ralph_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Ralph templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Ralph are not updated due this error \n {type(err).__name__}: {err}")
            
    # RAY-BAN
    try:
        get_ray_ban_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Ray-Ban templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Ray-Ban are not updated due this error \n {type(err).__name__}: {err}")
            
    # SWAROVSKI
    try:
        get_swarovski_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Swarovski templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Swarovski are not updated due this error \n {type(err).__name__}: {err}")
            
    # TIFFANY
    try:
        get_tiffany_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Tiffany templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Tiffany are not updated due this error \n {type(err).__name__}: {err}")
            
    # VERSACE
    try:
        get_versace_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Versace templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Versace are not updated due this error \n {type(err).__name__}: {err}")
    
    # VOGUE EYEWEAR
    try:
        get_vogue_templates()
        with open(get_templates, "a") as file:
            file.write(f"   Vogue Eyewear templates updated successfully. \n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"   Vogue Eyewear are not updated due this error \n {type(err).__name__}: {err}")
    
    
if __name__ == "__main__":
    try:
        with open(get_templates, "a") as file:
            current_time = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            file.write(f"[{current_time}] Starting Luxottica templates getter \n")
        get_luxottica_templates()
        with open(get_templates, "a") as file:
            file.write("Luxottica templates are updated successfully \n")
            file.write(f"Closing Luxottica templates getter \n\n")
            file.write("="*50 + "\n")
    except Exception as err:
        with open(get_templates, "a") as file:
            file.write(f"Luxottica templates are not updated due this error: \n {type(err).__name__}: {err}")
            file.write(f"Closing Luxottica templates getter \n\n")
            file.write("="*50 + "\n")