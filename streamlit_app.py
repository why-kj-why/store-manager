import streamlit as st
import pandas as pd
import pymysql
import time

# Database Configuration
DB_HOST = "tellmoredb.cd24ogmcy170.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASS = "2yYKKH8lUzaBvc92JUxW"
DB_PORT = "3306"
DB_NAME = "claires_data"
CONVO_DB_NAME = "store_questions"

# Declaring Colors
CLAIRE_DEEP_PURPLE = '#553D94'
CLAIRE_MAUVE = '#D2BBFF'

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')


def connect_to_db(db_name):
    return pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASS,
        db=db_name
    )


def set_custom_css():
    custom_css = """
    <style>
        .st-emotion-cache-9aoz2h.e1vs0wn30 {
            display: flex;
            justify-content: center; /* Center-align the DataFrame */
        }
        .st-emotion-cache-9aoz2h.e1vs0wn30 table {
            margin: 0 auto; /* Center-align the table itself */
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def execute_query(query, connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            getResult = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
        return pd.DataFrame(getResult, columns=columns)
    finally:
        connection.close()


def store_manager_app():
    # Load the logo
    with open(r'Claires_logo.svg', 'r') as image:
        image_data = image.read()
    st.logo(image=image_data)

    # Static store name and ID
    store_name = "BRISTOL SUPERSTORE"
    store_id = "STORE023"

    queries = {'Select a query': None,
               'Compare the sales performance for BRISTOL SUPERSTORE for this year against the previous year': 'SELECT DISTINCT STORE_ID, STORE_NAME, SALES_TY, SALES_LY FROM claires_data.store_total;'
    }

    st.markdown(f"""
    <h4 style="background-color: {CLAIRE_DEEP_PURPLE}; color: white; padding: 10px;">
        Store Manager App
    </h4>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <h4 style="background-color: {CLAIRE_MAUVE}; color: black; padding: 10px;">
        {store_name}, {store_id}
    </h4>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    selected_query = st.selectbox("Select a query", list(queries.keys()))

    if selected_query and selected_query != "Select a query":
        time.sleep(1)
        st.markdown("""
        The data table returned reports on the sales performance of STORE023 - BRISTOL SUPERSTORE for this year and the previous year.\n\nThe BRISTOL SUPERSTORE branch has seen a 3.6% increase in annual sales this year.\n\nThe average increase in sales for all Claire's Accessories stores this year has been: -1.19%\n
        """)


# Main Application
set_custom_css()

# Load the STORE MANAGER app directly without sidebar or toggle
store_manager_app()
