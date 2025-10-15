import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------
# APP HEADER
# -----------------------------
st.set_page_config(page_title="AI TravelMate", page_icon="🌍", layout="wide")

st.title("🌍 AI TravelMate – Smart Hotel Booking Assistant")
st.write("Welcome! Let’s help you find the perfect hotel for your trip ✈️")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_hotels():
    try:
        return pd.read_csv("hotels.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Hotel", "City", "Price_per_night", "Rating", "Link"])

hotels_df = load_hotels()

# -----------------------------
# USER INPUT
# -----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    city = st.text_input("Enter destination city:")
with col2:
    check_in = st.date_input("Check-in date:", min_value=date.today())
with col3:
    nights = st.number_input("Number of nights:", min_value=1, max_value=30, step=1)

budget = st.slider("Your total budget (USD):", 50, 2000, 500)

# -----------------------------
# AI HOTEL RECOMMENDER
# -----------------------------
if st.button("🔍 Find Hotels"):
    if city.strip() == "":
        st.warning("Please enter a destination city.")
    else:
        results = hotels_df[hotels_df["City"].str.contains(city, case=False, na=False)]

        if results.empty:
            st.error("❌ Sorry, no hotels found for that destination.")
        else:
            st.success(f"✅ Found {len(results)} hotels in {city.title()}")
            for i, row in results.iterrows():
                total_price = row["Price_per_night"] * nights
                if total_price <= budget:
                    st.markdown(f"""
                    ### 🏨 {row['Hotel']}
                    - 📍 Location: {row['City']}
                    - 💰 Price per night: **${row['Price_per_night']}**
                    - ⭐ Rating: {row['Rating']}
                    - 📅 Total for {nights} nights: **${total_price}**
                    - 🔗 [Book Now]({row['Link']})
                    ---
                    """)
            if not any(results["Price_per_night"] * nights <= budget):
                st.info("All hotels found are above your budget 💸. Try increasing your budget!")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Developed by Rayani Minoli – AI TravelMate Project 💡")
