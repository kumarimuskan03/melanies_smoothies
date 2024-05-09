import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your Smoothie!")

# Establish Snowflake connection
conn = snowflake.connector.connect(user='your_user', password='your_password', account='your_account', warehouse='your_warehouse', database='your_database', schema='your_schema')
cursor = conn.cursor(DictCursor)

# Retrieve fruit options from Snowflake table
cursor.execute("SELECT FRUIT_NAME FROM smoothies.public.fruit_options")
rows = cursor.fetchall()
fruit_options = [row["FRUIT_NAME"] for row in rows]

name_on_order = st.text_input("Name on Smoothie")
st.write("The name of your smoothie will be ", name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients',
    fruit_options,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    my_insert_stmt = f"INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES ('{ingredients_string}', '{name_on_order}')"
    st.write(my_insert_stmt)
    
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        cursor.execute(my_insert_stmt)
        conn.commit()
        st.success(f'Your Smoothie is ordered {name_on_order}!', icon="🧊")

# Close Snowflake connection
cursor.close()
conn.close()

# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write(
#     "Choose the fruits you want in your Smoothie!"
    
# )

# cnx = st.snowflake()
# session =cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# # st.dataframe(data=my_dataframe, use_container_width=True)

# name_on_order = st.text_input("Name on Smoothie")
# st.write("The name of your smoothie will be ", name_on_order)


# ingredients_list=st.multiselect(
#     'Choose up the 5 ingredients',
#     my_dataframe,
#     max_selections=5
# )



# if ingredients_list:
#     # st.write(ingrediants_list)
#     # st.text(ingrediants_list)
#     ingredients_string=''
#     for fruit in ingredients_list:
#         ingredients_string+=fruit+ ' '
#     # st.write(ingredients_string)
#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
#             values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

#     st.write(my_insert_stmt)
    
#     time_to_insert=st.button("Submit Order")
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success(f'Your Smoothie is ordered {name_on_order}!',icon="🧊")




