# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)


Name_on_Order = st.text_input("Name on Smoothie")
st.write("The Name on Smoothie will be: ", Name_on_Order)



cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:"
    ,my_dataframe
    ,max_selections=5
    )

if ingredients_list: 
    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string+= each_fruit+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(each_fruit+ 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +each_fruit)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_Order)
            values ('""" + ingredients_string + """','"""+Name_on_Order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()      
    st.success('Your Smoothie is ordered, {}!'.format(Name_on_Order), icon="✅")



