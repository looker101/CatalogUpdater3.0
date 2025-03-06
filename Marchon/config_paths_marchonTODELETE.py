import datetime
# FTP PATH
FTP_FIRST_PART = "/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script"
# Marchon Folder
FTP_MARCHON_FOLDER = f"{FTP_FIRST_PART}/Catalog/Marchon/"
# MARCHON_GET_FILE_IMPORT: upload
FTP_MARCHON_CSV = f"{FTP_FIRST_PART}/Catalog/Marchon/Marchon.csv"
FTP_TEMPLATE_SHOPIFY = f"{FTP_FIRST_PART}/Catalog/Marchon/Template.xlsx"
MARCHON_BACKUP = f"{FTP_FIRST_PART}/Catalog/Brand_backup/Marchon.xlsx"
# MARCHON_GET_FILE_IMPORT: saving
FTP_BRAND_DATA_PROCESSOR = f"{FTP_FIRST_PART}/Catalog/Brand_data_processor"
# BRAND > CATALOG PRICE: upload
CALVIN_KLEIN_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/CALVIN KLEIN.xlsx"
DRAGON_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/DRAGON.xlsx"
FERRAGAMO_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/FERRAGAMO.xlsx"
LACOSTE_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/LACOSTE.xlsx"
NIKE_BRAND_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/NIKE_marchon.xlsx"
VICTORIA_BECKHAM_DATA_PROCESSOR_FTP = f"{FTP_BRAND_DATA_PROCESSOR}/VICTORIA BECKHAM.xlsx"
# BRAND > CATALOG PRICE SAVING INTO MARCHON BRAND FOLDER
CALVIN_KLEIN_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Calvin Klein/"
DRAGON_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Dragon/"
FERRAGAMO_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Ferragamo/"
LACOSTE_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Lacoste/"
NIKE_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Nike/"
VICTORIA_BECKHAM_FOLDER_FTP = f"{FTP_FIRST_PART}/Catalog/Marchon/Victoria Beckham/"
# BRANDS TEMPLATE
# Upload all file updated into folder for each brand
FTP_CALVIN_KLEIN_UPDATED = f"{FTP_FIRST_PART}/Catalog/Marchon/Calvin Klein/Calvin Klein_updated.xlsx"
FTP_DRAGON_UPDATED = f"{FTP_FIRST_PART}/Catalog/Marchon/Dragon/Dragon.xlsx"
FTP_FERRAGAMO_UPDATED = f"{FTP_FIRST_PART}/Catalog/Marchon/Ferragamo/Ferragamo_updated.xlsx"
FTP_LACOSTE_UPDATED = f"{FTP_FIRST_PART}/Catalog/Marchon/Lacoste/Lacoste_updated.xlsx"
FTP_NIKE_UPDATED = f"{FTP_FIRST_PART}/Catalog/Marchon/Nike/Nike_updated.xlsx"
FTP_VICTORIA_BECKHAM_UPDATED = f"{FTP_FIRST_PART}/Catalog/Marchon/Victoria Beckham/Victoria Beckham_updated.xlsx"
# Saving on Temp Folder
FTP_TEMPLATES = f"{FTP_FIRST_PART}/Catalog/Marchon/Temp/"
# Shopify's Brand to Compare
# Upload
#FTP_MARCHON_BRAND_SHOPIFY = f"{FTP_FIRST_PART}/Catalog/Brand_backup/Marchon.xlsx"
# Save into Shopify's folder
FTP_SHOPIFY_FOLDER = f"{FTP_FIRST_PART}/Catalog/Marchon/Shopify/"
TO_IMPORT = f"{FTP_FIRST_PART}/Catalog/To_Import"
MARCHON_LOGS_FOLDER = f"{FTP_FIRST_PART}/logs/Marchon_logs.txt"
TODAY = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")