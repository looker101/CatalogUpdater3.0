import pandas as pd
import sys
sys.path.append("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Paths")

from marchon_paths import FTP_MARCHON_CSV, DRAGON_MARCHON_FILE

marchon_file = pd.read_csv(FTP_MARCHON_CSV)
dragon_file = pd.read_excel(DRAGON_MARCHON_FILE)

dfs_list = pd.concat([marchon_file, dragon_file])

dfs_list.to_csv("Marchon.csv", index=False)
