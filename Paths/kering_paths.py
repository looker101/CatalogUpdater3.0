import sys
import datetime

TODAY = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Alexander McQueen")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Balenciaga")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Bottega Veneta")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Chloe")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Gucci")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Saint Laurent")

# BACKUP KERING
kering_backup = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_backup/Kering.xlsx"

# TEMPLATES
amq_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Alexander McQueen/amq_templates.py"
balenciaga_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Balenciaga/balenciaga_templates.py"
bottega_veneta_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Bottega Veneta/bottega_veneta_templates.py"
chloe_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Chloe/chloe_templates.py"
gucci_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Gucci/gucci_templates.py"
sl_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Saint Laurent/saint_laurent_templates.py"

# EXCEL
amq_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Alexander McQueen/Alexander McQueen.xlsx"
balenciaga_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Balenciaga/Balenciaga.xlsx"
bottega_veneta_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Bottega Veneta/Bottega Veneta.xlsx"
chloe_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Chloe/Chloe.xlsx"
gucci_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Gucci/Gucci.xlsx"
sl_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Saint Laurent/Saint Laurent.xlsx"

# EXCEL AFTER BRAND DATA PROCESSOR
# amq_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Alexander McQueen/amq_ok.xlsx"
# balenciaga_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Balenciaga/balenciaga_ok.xlsx"
# bottega_veneta_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Bottega Veneta/bottega_veneta_ok.xlsx"
# chloe_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Chloe/chloe_ok.xlsx"
# gucci_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Gucci/gucci_ok.xlsx"
# sl_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Saint Laurent/saint_laurent_ok.xlsx"

# FILE TO UPDATE TEMPLATES
amq_for_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Alexander McQueen/Alexander McQueen_for_templates.xlsx"
balenciaga_for_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Balenciaga/Balenciaga_for_templates.xlsx"
bv_for_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Bottega Veneta/Bottega Veneta_for_templates.xlsx"
chloe_for_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Chloe/Chloe_for_templates.xlsx"
gucci_for_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Gucci/Gucci_for_templates.xlsx"
sl_for_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Saint Laurent/Saint Laurent_for_templates.xlsx"

# FOLDERS
amq_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Alexander McQueen/"
balenciaga_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Balenciaga/"
bottega_veneta_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Bottega Veneta/"
chloe_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Chloe/"
gucci_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Gucci/"
sl_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/Saint Laurent/"


# TO IMPORT
#templates_to_import_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Templates"
to_import_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Kering/"
price_quantity = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Kering/Price_quantity"
templates = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Kering/Templates"
gemini_folder = '/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Gemini'


# Logs
logs_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs"
logs_templates = f"{logs_folder}/Kering_templates_logs.txt"
price_qty_log = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs/Price_Qty_logs.txt"
splitting_kering_brands = f"{logs_folder}/Kering_splitting_brands.txt"
kering_price_qty_log = f"{logs_folder}/Kering_price_qty.txt"
