import sys
import time

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
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Ray-Ban/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Swarovski/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Tiffany/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Versace/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Vogue Eyewear/")

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
from Ray_Ban_Temp import get_ray_ban_templates
from Swarovski_Temp import get_swarovski_templates
from Tiffany_Temp import get_tiffany_templates
from Versace_Temp import get_versace_templates
from Vogue_Temp import get_vogue_templates

print("Run start_temp.py")
time.sleep(1)

# This function will handle the template processing
def process_template(template_name, template_func):
    try:
        print(f"Editing {template_name} templates..")
        template_func()
        print(f"{template_name} templates complete successfully")
        time.sleep(1)
    except Exception as err:
        print(f"{template_name} templates not updated due to this error. {type(err).__name__}: {err}")

# Process templates individually
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
