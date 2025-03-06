import datetime

#RETROSUPERFUTURE
FTP_FIRST_PART = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script"
RETROSUPERFUTURE_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/RetroSuperFuture/"
DAILY_LOOKER = f"{RETROSUPERFUTURE_FOLDER_FTP}/daily_looker_2.xlsx"
RETRO_UPDATE = f"{RETROSUPERFUTURE_FOLDER_FTP}RetroUpdate.xlsx"
RETRO_ON_SHOPIFY = f"{RETROSUPERFUTURE_FOLDER_FTP}/retro_shopify.xlsx"
RETRO_BACKUP = f"{FTP_FIRST_PART}/Catalog/Brand_backup/RSF.xlsx"

RETRO_LOGS = f"{FTP_FIRST_PART}/logs/RSF_Logs.txt"
TO_IMPORT = f"{FTP_FIRST_PART}/Catalog/To_Import"
PRODUCTS_OUT = f"{FTP_FIRST_PART}/Catalog/To_Import/RSF/out"

PRICE_QUANTITY = f"{FTP_FIRST_PART}/Catalog/To_Import/RSF/Price_quantity"
TEMPLATES = f"{FTP_FIRST_PART}/Catalog/To_Import/RSF/Templates"

TODAY = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")