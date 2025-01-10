import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the Excel file
def load_data(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name="Log")
    # Extract the goal row and data rows
    goals_row = df.iloc[0]
    df = df.iloc[1:].copy()
    # Convert relevant columns to numeric
    numeric_columns = [
        "Calories (kcal)", "Protein (g)", "Carbs (g)", "Fat (g)", "Fiber (g)",
        "Cholesterol (mg)", "Calcium (mg)", "Vitamin D (IU)", "Vitamin B12 (mcg)",
        "Saturated Fat (g)", "Sugar (g)", "Omega-3 (mg)", "Omega-6 (mg)",
        "Phosphorus (mg)", "Sodium (mg)", "Iron (mg)", "Hydration (Liters)"
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    # Summarize daily totals
    daily_totals = df.groupby("Date")[numeric_columns].sum()
    # Extract goals as a dictionary
    goals = goals_row[numeric_columns].to_dict()
    return daily_totals, goals

# Plot trends for specific nutrients
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

# Combined plot for multiple nutrients
def plot_combined_trends(daily_totals, goals, nutrients):
    plt.figure(figsize=(10, 6))
    for nutrient in nutrients:
        plt.plot(
            daily_totals.index, 
            daily_totals[nutrient], 
            marker="o", 
            label=f"{nutrient} (Intake)"
        )
        plt.axhline(goals[nutrient], linestyle="--", label=f"{nutrient} Goal")
    plt.title("Nutrient Trends vs Goals", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Nutrient Values", fontsize=12)
    plt.legend(loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(plt)

# Streamlit app
st.title("Nutrition Tracker Dashboard")

# File path for the Excel file
file_path = "./Macro tracker.xlsx"  # Local file path for Streamlit to access

# Load data
try:
    daily_totals, goals = load_data(file_path)
    st.write("### Summary of Daily Totals")
    st.dataframe(daily_totals)

    # Plot individual nutrient trends
    nutrients = ["Calories (kcal)", "Protein (g)", "Carbs (g)", "Sodium (mg)", "Sugar (g)", "Iron (mg)", "Vitamin B12 (mcg)"]
    for nutrient in nutrients:
        plot_trend(daily_totals, goals, nutrient)

    # Plot combined trends
    st.write("### Combined Trends")
    plot_combined_trends(daily_totals, goals, nutrients)
except Exception as e:
    st.error("An error occurred while loading the data or generating charts.")
    st.write(str(e))
