import pandas as pd

# Load the data
kering_file = pd.read_excel("/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Brand_backup/Kering.xlsx")

# Step 1: Group by "ID" and join "Image Src" values for each group
image_group = kering_file.groupby("ID")["Image Src"].apply(lambda x: ";".join(x.astype(str)))

# Step 2: Remove duplicates in the original data to keep only one row per ID
# We remove the "Image Src" column temporarily, so it doesn't conflict with the grouped column when we merge.
kering_file_no_duplicates = kering_file.drop_duplicates(subset="ID").drop(columns=["Image Src"])

# Step 3: Merge the grouped data back with the original data
# Now each ID will have all original columns plus the joined "Image Src" values
kering_result = kering_file_no_duplicates.merge(image_group, on="ID")

# Step 4: Save to Excel
kering_brands = kering_result["Vendor"].unique()
for brand in kering_brands:
    mask = kering_result["Vendor"] == brand
    brand_file = kering_result[mask]
    brand_file.to_excel(f"/var/www/vhosts/lookeronline.com/staging.lookeronline.com/script/Catalog/Kering/{brand}/{brand}.xlsx", index=False)
    print(f"{brand} saved successfully")

