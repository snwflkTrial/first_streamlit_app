import streamlit as st

st.title('My Parents New Healthy Diner')
st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('Build Your Own Fruit Smoothie')

import pandas as pd
myFruitList = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
myFruitList = myFruitList.set_index('Fruit')
# st.dataframe(myFruitList)

# Add a pick list so users can select the fruit they want included
st.multiselect('Pick some fruits:', list(myFruitList.index))

# display table on the page
st.dataframe(myFruitList)
