import datetime

# FTP PATH
FTP_FIRST_PART = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script"
# MARCHON_GET_FILE_IMPORT: upload
FTP_MARCHON_CSV = f"{FTP_FIRST_PART}/Catalog/Marchon/Marchon.csv"
DRAGON_MARCHON_FILE = f"{FTP_FIRST_PART}/Catalog/Marchon/Dragon_Marchon.xlsx"
FTP_TEMPLATE_SHOPIFY = f"{FTP_FIRST_PART}/Catalog/Marchon/Template.xlsx"
# MARCHON_GET_FILE_IMPORT: saving
FTP_BRAND_DATA_PROCESSOR = f"{FTP_FIRST_PART}/Catalog/Brand_data_processor"
MARCHON_BACKUP = f"{FTP_FIRST_PART}/Catalog/Brand_backup/Marchon.xlsx"
# BRAND > CATALOG PRICE: upload
# BRAND > CATALOG PRICE SAVING INTO MARCHON BRAND FOLDER
CALVIN_KLEIN_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Calvin Klein/"
DRAGON_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Dragon/"
FERRAGAMO_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Ferragamo/"
LACOSTE_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Lacoste/"
NIKE_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Nike/"
VICTORIA_BECKHAM_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Victoria Beckham/"

# EXCEL
LACOSTE_EXCEL = f"{FTP_FIRST_PART}/Catalog/Marchon/Lacoste/Lacoste.xlsx"
FERRAGAMO_EXCEL = f"{FTP_FIRST_PART}/Catalog/Marchon/Ferragamo/Ferragamo.xlsx"
NIKE_EXCEL = f"{FTP_FIRST_PART}/Catalog/Marchon/Nike/Nike.xlsx"
DRAGON_EXCEL = f"{FTP_FIRST_PART}/Catalog/Marchon/Dragon/Dragon.xlsx"

#BDP
# LACOSTE_BDP = f"{FTP_FIRST_PART}/Catalog/Marchon/Lacoste/Lacoste_ok.xlsx"
# FERRAGAMO_BDP = f"{FTP_FIRST_PART}/Catalog/Marchon/Ferragamo/Ferragamo_ok.xlsx"
# NIKE_BDP = f"{FTP_FIRST_PART}/Catalog/Marchon/Nike/Nike_ok.xlsx"

# Saving on Temp Folder
FTP_TEMPLATES = f"{FTP_FIRST_PART}/Catalog/Marchon/Temp/"
FTP_MARCHON_BRAND_SHOPIFY = f"{FTP_FIRST_PART}/Catalog/Marchon/Shopify_brand.xlsx"
FTP_MARCHON_FOLDER = f"{FTP_FIRST_PART}/Catalog/Marchon"
FTP_SHOPIFY_FOLDER = f"{FTP_FIRST_PART}/Catalog/Marchon/Shopify/"


TO_IMPORT_FOLDER = f"{FTP_FIRST_PART}/Catalog/To_Import/Marchon"
price_quantity = f"{TO_IMPORT_FOLDER}/price_quantity"
templates = f"{TO_IMPORT_FOLDER}/templates"
new_items = f"{TO_IMPORT_FOLDER}/new/Marchon_new_products.xlsx"

TODAY = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
logs_folder = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs"
marchon_logs_templates = f"{logs_folder}/Marchon_templates_logs.txt"
products_out = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/To_Import/Marchon/out"

# LOGS
price_qty_log = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/logs/Price_Qty_logs.txt"
marchon_price_qty_log = f"{logs_folder}/Marchon_price_qty.txt"
marchon_update_regular_items = f"{logs_folder}/Marchon_regular_items_updater.txt"
marchon_new_item_log = f"{logs_folder}/Marchon_new_item.txt"

CALVIN_KLEIN_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/CALVIN KLEIN.xlsx"


# DRAGON_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/DRAGON.xlsx"
# FERRAGAMO_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/FERRAGAMO.xlsx"
# LACOSTE_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/LACOSTE.xlsx"
# NIKE_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/NIKE.xlsx"
# VICTORIA_BECKHAM_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/VICTORIA BECKHAM.xlsx"