
import streamlit as st
import pandas as pd
import datetime
from pathlib import Path

st.set_page_config(page_title='AI TravelMate - Hotel Booking Prototype', layout='wide')

st.title('AI TravelMate — Hotel Booking Prototype (Simulated)')

DATA_PATH = Path(__file__).parent / 'hotels.csv'
df = pd.read_csv(DATA_PATH)

# Sidebar: user preferences
st.sidebar.header('Booking Preferences')
city = st.sidebar.text_input('City', value='Paris')
check_in = st.sidebar.date_input('Check-in date', value=datetime.date.today() + datetime.timedelta(days=7))
check_out = st.sidebar.date_input('Check-out date', value=check_in + datetime.timedelta(days=2))
max_price = st.sidebar.number_input('Max price per night (EUR)', value=120)
min_rating = st.sidebar.slider('Minimum rating', 0.0, 5.0, 4.0, 0.1)
min_stars = st.sidebar.selectbox('Minimum stars', [0,1,2,3,4,5], index=3)

nights = (check_out - check_in).days
if nights <= 0:
    st.sidebar.error('Check-out must be after check-in.')

# Simple LLM-like parsing: allow natural language ask (very simple rule-based)
st.sidebar.markdown('---')
nl_input = st.sidebar.text_area('Optional: Describe your preferences in one sentence (e.g., "3-star near center under 90 euros")', height=100)
if nl_input:
    st.sidebar.info('Parsed terms: ' + ', '.join([w for w in nl_input.replace(',', ' ').split() if len(w)>1][:6]))

# Filter hotels by city, price, rating, stars
results = df[df['city'].str.lower().str.contains(city.strip().lower())]
results = results[results['price_per_night'] <= max_price]
results = results[results['rating'] >= min_rating]
results = results[results['stars'] >= min_stars]

st.subheader(f'Search results for "{city}" — {len(results)} hotels found')
if results.empty:
    st.info('No hotels match your filters. Try increasing price or lowering rating/stars.')
else:
    # Ranking score: combine rating, stars, price into a simple score
    results = results.copy()
    results['score'] = (results['rating'] * 2 + results['stars']) / (results['price_per_night'] / 50)
    results = results.sort_values(by='score', ascending=False)

    # Show top 3 suggestions
    top = results.head(3)
    for idx, row in top.iterrows():
        st.markdown('---')
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f"### {row['name']} — {int(row['stars'])}★ — €{row['price_per_night']} / night")
            st.write(f"Rating: {row['rating']} — Available rooms: {row['available_rooms']}")
            st.write('Short description: Comfortable stay with helpful staff and convenient location.')
            st.write(f"Total for {nights} nights: €{row['price_per_night'] * max(1, nights)}")
        with col2:
            if st.button(f"Book {row['name']}", key=f"book_{row['id']}"):
                if row['available_rooms'] > 0:
                    # Simulated booking - update CSV (note: local only, not persistent across multiple app runs in deployed environments)
                    df.loc[df['id'] == row['id'], 'available_rooms'] = row['available_rooms'] - 1
                    df.to_csv(DATA_PATH, index=False)
                    st.success(f"Booking simulated for {row['name']}. Confirmation ID: TM-{row['id']}{int(pd.Timestamp.now().timestamp()) % 10000}")
                else:
                    st.error('No rooms available.')
    st.markdown('---')
    st.write('Full results table:')
    st.dataframe(results[['id','name','city','price_per_night','stars','rating','available_rooms','score']])
