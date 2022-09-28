import streamlit as st
import pandas as pd
import requests as rq
import snowflake.connector as sc
from urllib.error import URLError

st.title('My Parents New Healthy Diner')
st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('Build Your Own Fruit Smoothie')

myFruitList = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
myFruitList = myFruitList.set_index('Fruit')
# st.dataframe(myFruitList)

# Add a pick list so users can select the fruit they want included
fruitSelected = st.multiselect('Pick some fruits:', list(myFruitList.index), ['Avocado', 'Strawberries'])
fruitToShow = myFruitList.loc[fruitSelected]

# display table on the page
st.dataframe(fruitToShow)

#fruitChoice = st.text_input('What fruit would you like information about?', 'Kiwi')
#st.write('The user entered', fruitChoice)
def getFruityviceData(thisFruitChoice):
  fruityviceResponse = rq.get("https://fruityvice.com/api/fruit/" + thisFruitChoice)
  fruityviceNormalized = pd.json_normalize(fruityviceResponse.json())
  return fruityviceNormalized

# New section to display fruityvice API response
st.header('Fruityvice Fruit Advice!')
try:
  fruitChoice = st.text_input('What fruit would you like information about?')
  if not fruitChoice:
    st.error('Please select a fruit to get information')
  else:
    backFromFunction = getFruityViceData(fruitChoice)
    st.dataframe(backFromFunction)

except URLError as e:
  st.error()

# fruityviceResponse = rq.get("https://fruityvice.com/api/fruit/" + 'kiwi')
# st.text(fruityviceResponse.json())

# normalize the json response from fruityverse
# fruityviceNormalized = pd.json_normalize(fruityviceResponse.json())
# output it to the screen as a table
# st.dataframe(fruityviceNormalized)
st.stop()

myCnx = sc.connect(**st.secrets['snowflake'])
myCur = myCnx.cursor()
myCur.execute('select * from fruit_load_list')
myDataRows = myCur.fetchall()
st.header('The fruit load list contains:')
st.dataframe(myDataRows)

# Allow end user to add a fruit to the list
addMyFruit = st.text_input('What fruit would you like to add?', 'jackfruit')
st.write('Thanks for adding', addMyFruit)

myCur.execute("insert into fruit_load_list values ('from streamlit')")
