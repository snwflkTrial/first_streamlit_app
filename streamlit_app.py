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
fruitSelected = st.multiselect('Pick some fruits:', list(myFruitList.index), ['Avocado', 'Strawberries'])
fruitToShow = myFruitList.loc[fruitSelected]

# display table on the page
st.dataframe(fruitToShow)

# New section to display fruityvice API response
st.header('Fruityvice Fruit Advice!')
fruitChoice = st.text_input('What fruit would you like information about?', 'Kiwi')
st.write('The user entered', fruitChoice)

import requests as rq
fruityviceResponse = rq.get("https://fruityvice.com/api/fruit/" + 'kiwi')
# st.text(fruityviceResponse.json())

# normalize the json response from fruityverse
fruityviceNormalized = pd.json_normalize(fruityviceResponse.json())
# output it to the screen as a table
st.dataframe(fruityviceNormalized)

import snowflake.connector as sc
myCnx = sc.connect(**st.secrets['snowflake'])
myCur = myCnx.cursor()
myCur.execute('SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()')
myDataRow = myCur.fetchone()
st.text('Hello from Snowflake:')
st.text(myDataRow)
