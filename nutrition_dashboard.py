import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the Excel file from OneDrive
def load_data(file_path):
    df = pd.read_excel(file_path, sheet_name="Log")
    goals_row = df.iloc[0]
    df = df.iloc[1:].copy()
    numeric_columns = [
        "Calories (kcal)", "Protein (g)", "Carbs (g)", "Fat (g)", "Fiber (g)",
        "Cholesterol (mg)", "Calcium (mg)", "Vitamin D (IU)", "Vitamin B12 (mcg)",
        "Saturated Fat (g)", "Sugar (g)", "Omega-3 (mg)", "Omega-6 (mg)",
        "Phosphorus (mg)", "Sodium (mg)", "Iron (mg)", "Hydration (Liters)"
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    daily_totals = df.groupby("Date")[numeric_columns].sum()
    goals = goals_row[numeric_columns].to_dict()
    return daily_totals, goals

# Plot nutrient trends
def plot_trend(daily_totals, goals, nutrient):
    plt.figure(figsize=(10, 6))
    plt.plot(daily_totals.index, daily_totals[nutrient], label="Daily Intake", marker="o")
    plt.axhline(goals[nutrient], color="red", linestyle="--", label=f"Goal ({goals[nutrient]})")
    plt.title(f"{nutrient} Trends vs Goal", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel(nutrient, fontsize=12)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(plt)

# Streamlit app
st.title("Nutrition Tracker Dashboard")
file_path = st.text_input("Enter the path to your OneDrive file:", r"C:\Users\user\OneDrive\Documents\Macro tracker.xlsx")
if st.button("Load Data"):
    daily_totals, goals = load_data(file_path)
    st.write("### Summary of Daily Totals")
    st.dataframe(daily_totals)

    st.write("### Trend Charts")
    nutrients = ["Calories (kcal)", "Protein (g)", "Carbs (g)"]
    for nutrient in nutrients:
        plot_trend(daily_totals, goals, nutrient)
