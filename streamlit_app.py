# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f" :cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want  in your custom smoothie!
  """
)

name_on_order = st.text_input("Name On Smoothie:")
st.write("The name of your smoothie will be:", name_on_order)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert snowpark dataframe to pandas dataframe so we can use the loc function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredient_list = st.multiselect(
    "choose up to 5 intgredients:",
    my_dataframe.to_pandas()['FRUIT_NAME'].tolist(),
    max_selections=5,
)

if ingredient_list:
  ingredient_string = ''
  for fruit_chosen in ingredient_list:
    ingredient_string += fruit_chosen + ' '
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    st.subheader(fruit_chosen + 'Nutrition Information')
    #st.write(ingredient_string)

    #my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
    #values ('""" + ingredient_string.strip() + """','""" + name_on_order + """')"""

    #time_to_insert = st.button('Submit Order')
    #if time_to_insert:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")

    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
    st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
