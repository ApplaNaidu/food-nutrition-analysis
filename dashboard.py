import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Correct path to cleaned dataset
data_path = r"C:\Users\appal\OneDrive\Desktop\MY PROJECTS\FoodNutritionAnalysis\FoodNutritionAnalysis\cleaned_nutrition_data.csv"
df = pd.read_csv(data_path)

# Extract food names
food_names = df["Food_Name"].dropna().unique().tolist()

# 🏷️ Title
st.set_page_config(page_title="Food Nutrition Dashboard", layout="wide")
st.title("🥗 Food Nutrition Analysis Dashboard")
st.markdown("Explore nutrient profiles of foods and discover healthy options.")

# 🔍 Search Bar at Top
search_query = st.text_input("🔍 Search Food Type", "", help="Type to search for a food item")
filtered_foods = [food for food in food_names if search_query.lower() in food.lower()]

if filtered_foods:
    selected_food = st.selectbox("Select a food:", filtered_foods)
else:
    st.warning("No matching foods found.")
    selected_food = None

# 🥣 Nutrient Distribution
if selected_food:
    food_row = df[df["Food_Name"] == selected_food].iloc[0]
    nutrients = {
        "Calories": food_row["Calories"],
        "Protein (g)": food_row["Protein_g"],
        "Carbs (g)": food_row["Carbs_g"],
        "Fat (g)": food_row["Fat_g"],
        "Fiber (g)": food_row["Fiber_g"]
    }

    total = sum(nutrients.values())
    if total > 0:
        st.subheader(f"Nutrient Distribution for: {selected_food}")
        pie_df = pd.DataFrame.from_dict(nutrients, orient='index', columns=['Amount']).reset_index()
        pie_df.columns = ['Nutrient', 'Amount']
        fig = px.pie(pie_df, names='Nutrient', values='Amount', title='Nutrient Breakdown')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No nutrient data available for this food.")

    # 📋 Nutrient Table for Selected Food
    st.subheader("📋 Nutrient Values")
    nutrient_table = pd.DataFrame([nutrients])
    nutrient_table.index = [selected_food]
    st.dataframe(nutrient_table)

# 💪 Top 5 High-Protein Foods
st.subheader("💪 Top 5 High-Protein Foods")
top_protein = df.sort_values(by="Protein_g", ascending=False).head(5)
bar_fig = px.bar(top_protein, x="Protein_g", y="Food_Name", orientation='h', title="Top Protein Foods")
st.plotly_chart(bar_fig, use_container_width=True)

# 📈 Calories vs. Protein Scatter Plot
st.subheader("📈 Calories vs. Protein")
scatter_fig = px.scatter(df, x="Calories", y="Protein_g", hover_data=["Food_Name"], title="Calories vs. Protein")
st.plotly_chart(scatter_fig, use_container_width=True)

# 📊 Dataset Statistics
st.subheader("📊 Dataset Statistics")
st.write(f"Total Foods: {len(df)}")
st.write(f"Average Protein: {df['Protein_g'].mean():.2f} g")
st.write(f"Average Calories: {df['Calories'].mean():.2f}")
