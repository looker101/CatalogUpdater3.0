import sys
import datetime
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/De_Rigo/Police")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/De_Rigo/Porsche Design")

TODAY = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")

# BACKUP
derigo_backup = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_backup/DeRigo.xlsx"

# FOLDERS
police_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/De_Rigo/Police"
porsche_design_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/De_Rigo/Porsche Design/"

# Excel
police_excel = f"{police_folder}/Police.xlsx"
porsche_design_excel = f"{porsche_design_folder}/Porsche Design.xlsx"

price_quantity = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/De_Rigo/price_quantity"
templates = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/De_Rigo/templates"

# LOGS
logs_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs/"
price_qty_log = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs/Price_Qty_logs.txt"
templates_logs = f"{logs_folder}/Derigo_templates_logs.txt"
splitting_logs = f"{logs_folder}/Derigo_splitting.txt"
derigo_price_qty_log = f"{logs_folder}/Derigo_price_qty.txt"