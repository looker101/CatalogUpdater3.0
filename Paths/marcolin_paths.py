import sys
import datetime

sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Originals/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Sport/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Guess/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Max&Co/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/MaxMara/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Emilio Pucci/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Timberland/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Tom Ford/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Web/")
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Zegna/")

# BACKUP
marcolin_backup = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_backup/Marcolin.xlsx"

# TEMPLATES UPDATER
adidas_originals_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Originals/adidas_originals_template.py"
adidas_sport_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Sport/adidas_sport_template.py"
guess_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Guess/guess_template.py"
max_co_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Max&Co/max&co_template.py"
max_mara_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/MaxMara/maxmara_templates.py"
pucci_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Emilio Pucci/pucci_templates.py"
timberland_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Timberland/timberland_template.py"
tom_ford_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Tom Ford/tom_ford_template.py"
web_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Web/web_templates.py"
zegna_temp = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Zegna/zegna_templates.py"

# EXCEL
adidas_originals_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Originals/Adidas Originals.xlsx"
adidas_sport_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Sport/Adidas Sport.xlsx"
guess_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Guess/Guess.xlsx"
max_co_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Max&Co/Max&Co.xlsx"
max_mara_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/MaxMara/MaxMara.xlsx"
pucci_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Emilio Pucci/Emilio Pucci.xlsx"
timberland_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Timberland/Timberland.xlsx"
tom_ford_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Tom Ford/Tom Ford.xlsx"
web_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Web/Web.xlsx"
zegna_excel = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Zegna/Zegna.xlsx"

# EXCEL AFTER BRAND DATA PROCESSOR
# adidas_originals_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Originals/Adidas_Originals_ok.xlsx"
# adidas_sport_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Sport/adidas_sport_ok.xlsx"
# pucci_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Emilio Pucci/pucci_ok.xlsx"
# guess_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Guess/guess_ok.xlsx"
# max_co_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Max&Co/Max%26Co_ok.xlsx"
# max_mara_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/MaxMara/max_mara_ok.xlsx"
# timberland_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Timberland/Timberland_ok.xlsx"
# tom_ford_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Tom Ford/tom_ford_ok.xlsx"
# web_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Web/web_ok.xlsx"
# zegna_BDP = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Zegna/zegna_ok.xlsx"

# BRANDS FOLDER
adidas_originals_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Originals/"
adidas_sport_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Adidas Sport/"
guess_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Guess/"
max_co_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Max&Co/"
max_mara_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/MaxMara/"
pucci_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Emilio Pucci/"
timberland_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Timberland/"
tom_ford_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Tom Ford/"
web_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Web/"
zegna_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Marcolin/Zegna/"

# TO IMPORT
to_import_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Marcolin"
price_quantity = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Marcolin/price_quantity"
templates = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Marcolin/templates"

logs_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs"
templates_logs = f"{logs_folder}/Marcolin_templates_logs.txt"
splitting_marcolin_brands = f"{logs_folder}/Marcolin_splitting_brands.txt"
marcolin_price_qty_log = f"{logs_folder}/Marcolin_price_qty.txt"

TODAY = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
price_qty_log = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs/Price_Qty_logs.txt"