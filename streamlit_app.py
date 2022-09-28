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
    backFromFunction = getFruityviceData(fruitChoice)
    st.dataframe(backFromFunction)

except URLError as e:
  st.error()

st.header('The fruit load list contains:')
def getFruitLoadList():
  with myCnx.cursor() as myCur:
    myCur.execute('select * from fruit_load_list')
    return myCur.fetchall()

# Add a button to load the fruit
if st.button('Get Fruit Load List'):
  myCnx = sc.connect(**st.secrets['snowflake'])
  myDataRows = getFruitLoadList()
  st.dataframe(myDataRows)

# allow end user to add fruit to the list
def insertRowSnwflk(newFruit):
  with myCnx.cursor() as myCur:
    myCur.execute("insert into fruit_load_list values ('" + newFruit + "')")
    return 'Thanks for adding ' + newFruit
  
addMyFruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the list'):
  myCnx = sc.connect(**st.secrets['snowflake'])
  backFromFunction = insertRowSnwflk(addMyFruit)
  st.text(backFromFunction)

if st.button('Get Fruit List'):
  myCnx = sc.connect(**st.secrets['snowflake'])
  myDataRows = getFruitLoadList()
  myCnx.close()
  st.dataframe(myDataRows)
  
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


