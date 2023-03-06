
import streamlit
import pandas as pd
import requests 
import snowflake.connector
from urllib.error import URLError


streamlit.title('First Attempt Snowflake Api')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#reading csv from  s3 bucket
#import pandas
myfruit_list= pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(myfruit_list)
#select the column to set the index
myfruit_list = myfruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(myfruit_list.index))


#select list #preselect
fruits_selected=streamlit.multiselect("Pick some fruits:", list(myfruit_list.index),['Avocado','Strawberries'])
fruits_to_show=myfruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)



#create function
def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
        # transform json  to normalize
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
     # show json data into table 
    return fruityvice_normalized
                                        
    

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        returnback=get_fruityvice_data(fruit_choice)
        streamlit.dataframe(returnback)    
except URLError as e:
    streamlit.error()



    





streamlit.header("The fruit load list contains")
#function to get the fruit from snowflake 
def get_fruit_load_list():
    with my_cnx.cursor as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

#add button 
if streamlit.button('Get Fruit Load List'):
    #connection snowflake -add in the app the config of snowflake params
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows=get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlit')")
    return ('Thanks for adding',new_fruit)

add_my_fruit= streamlit.text_input ('What fruit would you like to add?','jackfruit')
if streamlit.button('Insert new fruit'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_funciton=insert_row_snowflake(add_my_fruit)
    streamlit.write(back_funciton)
