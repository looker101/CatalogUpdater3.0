import datetime
# LUXOTTICA PATHS
## Folders
#Brand_data_process
luxottica_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica"
brand_data_processor = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_data_processor"
luxottica_backup = f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_backup/Luxottica.xlsx"
luxottica_backup_complete = f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_backup/Luxottica_complete_20-10.xlsx"
arnette_folder = f"{luxottica_folder}/Arnette"
burberry_folder = f"{luxottica_folder}/Burberry"
dolce_gabbana_folder = f"{luxottica_folder}/Dolce & Gabbana"
emporio_armani_folder = f"{luxottica_folder}/Emporio Armani"
giorgio_armani_folder = f"{luxottica_folder}/Giorgio Armani"
michael_kors_folder = f"{luxottica_folder}/Michael Kors"
miumiu_folder = f"{luxottica_folder}/Miu Miu"
oakley_folder = f"{luxottica_folder}/Oakley"
persol_folder = f"{luxottica_folder}/Persol"
prada_folder = f"{luxottica_folder}/Prada"
plr_folder = f"{luxottica_folder}/Prada Linea Rossa"
ralph_folder = f"{luxottica_folder}/Ralph"
ray_ban_folder = f"{luxottica_folder}/Ray-Ban"
swarovski_folder = f"{luxottica_folder}/Swarovski"
tiffany_folder = f"{luxottica_folder}/Tiffany"
versace_folder = f"{luxottica_folder}/Versace"
vogue_folder = f"{luxottica_folder}/Vogue Eyewear"

luxottica_item_master = f"{luxottica_folder}/Item Master Data Catalogue.xlsx"

# SAVING
luxottica_to_import_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Luxottica"

# Brand Files
arnette_update = f"{arnette_folder}/Arnette.xlsx"
arnette_old = f"{arnette_folder}/OLD_Arnette.xlsx"
arnette_BDP = f"{arnette_folder}/Arnette_ok.xlsx"
arnette_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Arnette/Arnette_IMG.xlsx"

burberry_update = f"{burberry_folder}/Burberry.xlsx"
burberry_old = f"{burberry_folder}/OLD_Bubrerry.xlsx"
burberry_BDP = f"{burberry_folder}/Burberry_ok.xlsx"
burberry_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Burberry/Burberry_IMG.xlsx"

dolce_gabbana_update = f"{dolce_gabbana_folder}/Dolce & Gabbana.xlsx"
dolce_gabbana_old = f"{dolce_gabbana_folder}/OLD_Dolce %26 Gabbana.xlsx"
dolce_gabbana_BDP = f"{dolce_gabbana_folder}/Dolce & Gabbana_ok.xlsx"
dolce_gabbana_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Dolce & Gabbana/Dolce_Gabbana_IMG.xlsx"

emporio_armani_update = f"{emporio_armani_folder}/Emporio Armani.xlsx"
emporio_armani_old = f"{emporio_armani_folder}/OLD_Emporio Armani.xlsx"
emporio_armani_BDP = f"{emporio_armani_folder}/Emporio Armani_ok.xlsx"
emporio_armani_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Emporio Armani/Emporio Armani_IMG.xlsx"

giorgio_armani_update = f"{giorgio_armani_folder}/Giorgio Armani.xlsx"
giorgio_armani_old = f"{giorgio_armani_folder}/OLD_Giorgio Armani.xlsx"
giorgio_armani_BDP = f"{giorgio_armani_folder}/Giorgio Armani_ok.xlsx"
giorgio_armani_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Giorgio Armani/Giorgio Armani_IMG.xlsx"

michael_kors_update = f"{michael_kors_folder}/Michael Kors.xlsx"
michael_kors_old = f"{michael_kors_folder}/OLD_Michael Kors.xlsx"
michael_kors_BDP = f"{michael_kors_folder}/Michael Kors_ok.xlsx"
michael_kors_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Michael Kors/Michael Kors_IMG.xlsx"

miumiu_update = f"{miumiu_folder}/Miu Miu.xlsx"
miumiu_old = f"{miumiu_folder}/OLD_Miu Miu.xlsx"
miumiu_BDP = f"{miumiu_folder}/Miu Miu_ok.xlsx"
miumiu_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Miu Miu/Miu Miu_IMG.xlsx"

oakley_update = f"{oakley_folder}/Oakley.xlsx"
oakley_old = f"{oakley_folder}/OLD_Oakley.xlsx"
oakley_BDP = f"{oakley_folder}/Oakley_ok.xlsx"
oakley_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Oakley/Oakley_IMG.xlsx"

persol_update = f"{persol_folder}/Persol.xlsx"
persol_old = f"{persol_folder}/OLD_Persol.xlsx"
persol_BDP = f"{persol_folder}/Persol_ok.xlsx"
persol_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Persol/Persol_IMG.xlsx"

prada_update = f"{prada_folder}/Prada.xlsx"
prada_old = f"{prada_folder}/OLD_Prada.xlsx"
prada_BDP = f"{prada_folder}/Prada_ok.xlsx"
prada_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Prada/Prada_IMG.xlsx"

plr_update = f"{plr_folder}/Prada Linea Rossa.xlsx"
plr_old = f"{plr_folder}/OLD_Prada Linea Rossa.xlsx"
plr_BDP = f"{plr_folder}/Prada Linea Rossa_ok.xlsx"
plr_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Prada Linea Rossa/PLR_IMG.xlsx"

ralph_update = f"{ralph_folder}/Ralph.xlsx"
ralph_old = f"{ralph_folder}/OLD_Ralph.xlsx"
ralph_DBP = f"{ralph_folder}/Ralph_ok.xlsx"
ralph_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Ralph/Ralph_IMG.xlsx"

ray_ban_update = f"{ray_ban_folder}/Ray-Ban.xlsx"
ray_ban_old = f"{ray_ban_folder}/OLD_Ray-Ban.xlsx"
ray_ban_BDP = f"{ray_ban_folder}/Ray-Ban_ok.xlsx"
ray_ban_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Ray-Ban/Ray-Ban_IMG.xlsx"

swarovski_update = f"{swarovski_folder}/Swarovski.xlsx"
swarovski_old = f"{swarovski_folder}/OLD_Swarovski.xlsx"
swarovski_BDP = f"{swarovski_folder}/Swarovski_ok.xlsx"
swarovski_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Swarovski/Swarovski_IMG.xlsx"

tiffany_update = f"{tiffany_folder}/Tiffany.xlsx"
tiffany_old = f"{tiffany_folder}/OLD_Tiffany.xlsx"
tiffany_BDP = f"{tiffany_folder}/Tiffany_ok.xlsx"
tiffany_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Tiffany/Tiffany_IMG.xlsx"

versace_update = f"{versace_folder}/Versace.xlsx"
versace_old = f"{versace_folder}/OLD_Versace.xlsx"
versace_BDP = f"{versace_folder}/Versace_ok.xlsx"
versace_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Versace/Versace_IMG.xlsx"

vogue_update = f"{vogue_folder}/Vogue Eyewear.xlsx"
vogue_old = f"{vogue_folder}/OLD_Vogue.xlsx"
vogue_BDP = f"{vogue_folder}/Vogue Eyewear.xlsx"
vogue_new = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Luxottica/Vogue Eyewear/Vogue_IMG.xlsx"

# Ski Goggles
ski_goggles_folder = f"{luxottica_folder}/Goggle&acc  snow"
ski_goggles_folder_excel = f"{luxottica_folder}/Goggle&acc  snow/Goggle&acc  snow_IMG.xlsx"

# Files
luxottica_updated_file = f"{luxottica_folder}/Item Master Data Catalogue.xlsx"
products_out_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Out"
luxottica_new_products = f"{luxottica_folder}/Luxottica_New_Products.xlsx"

# LOGS
logs_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs"
get_images_logs = f"{logs_folder}/Luxottica_get_images_logs.txt"
get_templates = f"{logs_folder}/Luxottica_get_templates.txt"
luxottica_price_qty_log = f"{logs_folder}/Luxottica_price_qty.txt"
luxottica_shared_products_log = f"{logs_folder}/luxottica_shared_products.txt"

# TO_IMPORT_FOLDERS
to_import_templates = f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Templates"
to_import_images = f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Luxottica/Images"
lux_price_and_quantity = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Luxottica/Price_quantity"
lux_only_templates = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Luxottica/Templates"
out_products = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Luxottica/Out"
price_qty_log = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs/Price_Qty_logs.txt"