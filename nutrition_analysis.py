import pandas as pd
import os

# ✅ Set correct path
base_path = r"C:\Users\appal\OneDrive\Desktop\MY PROJECTS\FoodNutritionAnalysis\FoodNutritionAnalysis"

# Load USDA files
food_df = pd.read_csv(os.path.join(base_path, "food.csv"))
nutrient_df = pd.read_csv(os.path.join(base_path, "food_nutrient.csv"), low_memory=False)
nutrient_names_df = pd.read_csv(os.path.join(base_path, "nutrient.csv"))

# Merge nutrient names
nutrient_df = nutrient_df.merge(nutrient_names_df[['id', 'name']], left_on='nutrient_id', right_on='id', how='left')

# Filter key nutrients
key_nutrients = [
    'Energy',
    'Protein',
    'Carbohydrate, by difference',
    'Total lipid (fat)',
    'Fiber, total dietary'
]
nutrient_df = nutrient_df[nutrient_df['name'].isin(key_nutrients)]

# Rename nutrients
rename_map = {
    'Energy': 'Calories',
    'Protein': 'Protein_g',
    'Carbohydrate, by difference': 'Carbs_g',
    'Total lipid (fat)': 'Fat_g',
    'Fiber, total dietary': 'Fiber_g'
}
nutrient_df['name'] = nutrient_df['name'].map(rename_map)

# Pivot nutrients
nutrient_pivot = nutrient_df.pivot_table(index='fdc_id', columns='name', values='amount', aggfunc='mean').reset_index()

# Merge with food names
merged_df = food_df[['fdc_id', 'description']].merge(nutrient_pivot, on='fdc_id', how='left')
merged_df = merged_df.rename(columns={'description': 'Food_Name'})

# Fill missing values
nutrient_cols = ['Calories', 'Protein_g', 'Carbs_g', 'Fat_g', 'Fiber_g']
for col in nutrient_cols:
    if col not in merged_df.columns:
        merged_df[col] = 0
    else:
        merged_df[col] = merged_df[col].fillna(0)

# Save cleaned dataset
output_path = os.path.join(base_path, "cleaned_nutrition_data.csv")
merged_df.to_csv(output_path, index=False)
print(f"✅ Cleaned dataset saved with {len(merged_df)} foods.")
