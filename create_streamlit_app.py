import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want from your custom Smoothie!
    """)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

fruit_options = my_dataframe.collect()

# Extracting fruit names and corresponding search terms into a dictionary
fruit_search_mapping = {row['FRUIT_NAME']: row['SEARCH_ON'] for row in fruit_options}

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',
    list(fruit_search_mapping.keys()),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        search_term = fruit_search_mapping.get(fruit_chosen)
        if search_term:
            ingredients_string += fruit_chosen + ' '
            st.subheader(fruit_chosen + ' Nutrition Information')
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_term)
            fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

