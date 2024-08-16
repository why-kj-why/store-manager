# from llama_index.legacy.llms.azure_openai import AzureOpenAI
import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

DB_HOST = "tellmoredb.cd24ogmcy170.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASS = "2yYKKH8lUzaBvc92JUxW"
DB_PORT = "3306"
# DB_NAME = "retail_panopticon"
DB_NAME = "claires_data"
CONVO_DB_NAME = "store_questions"

#Declaring Colours
CLAIRE_DEEP_PURPLE = '#553D94'
CLAIRE_MAUVE = '#D2BBFF'

# AZURE_OPENAI_KEY = "94173b7e3f284f2c8f8eb1804fa55699"
# AZURE_OPENAI_ENDPOINT = "https://tellmoredemogpt.openai.azure.com/"
# AZURE_OPENAI_ENGINE = "tellmore-demo-gpt35"
# AZURE_OPENAI_MODEL_NAME = "gpt-3.5-turbo-0125"
# AZURE_OPENAI_TYPE = "azure"

# llm = AzureOpenAI(
#     model=AZURE_OPENAI_MODEL_NAME,
#     engine=AZURE_OPENAI_ENGINE,
#     api_key=AZURE_OPENAI_KEY,
#     azure_endpoint=AZURE_OPENAI_ENDPOINT,
#     api_type=AZURE_OPENAI_TYPE,
#     api_version="2024-03-01-preview",
#     temperature=0.3,
# )


def connect_to_db(db_name):
    return pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASS,
        db=db_name
    )


def execute_query(query, connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            getResult = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
        return pd.DataFrame(getResult, columns=columns)
    finally:
        connection.close()


def get_queries_from_db():
    connection = connect_to_db(CONVO_DB_NAME)
    query = "SELECT question, sql_query FROM pinned_questions;"
    df = execute_query(query, connection)
    questions = {"Select a query": None}
    questions.update(dict(zip(df['question'], df['sql_query'])))
    return questions


st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

def set_custom_css():
    """
    This function is used to set the custom CSS properties.
    
    Existing Functionality:

    1. Center align the Query Result table.

    Features to Add:

    1. Shorten the drop down menu
    2.Try and reduce the space between elements.

    """
    # Custom CSS to center-align the dataframe
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
    # Inject the CSS
    st.markdown(custom_css, unsafe_allow_html=True)

set_custom_css()

#Load the logo 

with open(r'Claires_logo.svg', 'r') as image:
    image_data = image.read()
    
    
st.logo(image=image_data)

# Claire Purple top bar on Top.
st.markdown("""
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100px; background-color: {}; z-index: 1000;">
</div>
""".format(CLAIRE_DEEP_PURPLE), unsafe_allow_html=True)

queries = get_queries_from_db()

result = None

# col = st.columns((2, 1, 1), gap='medium')

st.markdown("""
    <h4 style="background-color: {}; color: white; padding: 10px;">
        North Riverside Park Mall, Store001
    </h4>
""".format(CLAIRE_DEEP_PURPLE), unsafe_allow_html=True)

#Adding Padding
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)


#st.markdown("#### Store Ops App")
#Subheader
st.markdown("""
    <h4 style="background-color: {}; color: black; padding: 10px;">
        Store Management App
    </h4>
""".format(CLAIRE_MAUVE), unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# with col[0]:
#     st.markdown("#### North Riverside Park Mall, Store001")
#     st.markdown("#### Store Ops App")

selected_query = st.selectbox("Select a query", list(queries.keys()))
if selected_query and selected_query != "Select a query":
    query_sql = queries[selected_query]
    conn = connect_to_db(DB_NAME)
    result = execute_query(query_sql, conn)
        # language_prompt = f"""
        #     following is a business question: {selected_query}\n
        #     columns from an enterprise database schema were identified to answer this question\n
        #     upon querying the columns, the following SQL data table was returned: {result}\n
        #     generate a natural language response explaining the data table that was 
        #     returned, with the business question as context\n
        #     respond only with the natural language explanation of the data table output, do not explain the 
        #     business question or how the columns were selected and queried\n
        # """
        # ans = llm.complete(language_prompt)
        # ans = ans.text
        # st.markdown(ans)
    # st.markdown("The data table returned provides information about regular customers aged over 50 who have spent more than 15000. It includes columns such as Customer_ID, Customer_Name, Age, and Total_Spent. The table consists of 780 rows, each representing a different customer. The Customer_ID column contains unique identifiers for each customer. The Customer_Name column displays the names of the customers. The Age column indicates the age of each customer. The Total_Spent column shows the amount of money each customer has spent. The table includes details of customers who meet the criteria specified in the business question, such as Amy Marsh, Tabitha Graves, Christopher Campbell, Sandra Jacobs, Pamela Brooks, and many others.")
    st.markdown("""
The data table returned provides information on the sales performance of different stores for this year and the previous year. The table includes columns such as STORE_ID, STORE_NAME, SALES_TY (sales for this year), and SALES_LY (sales for the previous year).\n\n
Looking at the data, we can observe that the sales for most stores vary between this year and the previous year. Some stores have seen an increase in sales, while others have experienced a decrease.\n\n
For example, stores like BRISTOL SUPERSTORE, CWMBRAN, and CARDIFF have seen an increase in sales this year compared to the previous year. On the other hand, stores like NEWPORT, CRIBBS CAUSEWAY, and SWANSEA have shown a decrease in sales.\n\n
It is also interesting to note that some stores have had significant changes in sales performance. For instance, stores like West End New, Budapest Arena Plaza, and Arkad Budapest have experienced a significant increase in sales this year compared to the previous year. Conversely, stores like Budapest Vaci Utca and Gyor Arkad have seen a significant decrease in sales.\n\n
Overall, the data table provides a comparison of sales performance across all stores for this year against the previous year, highlighting the varying trends in sales for different stores.
    """)
    st.dataframe(result, height=300)

# with col[1]:
#     if result is not None and not result.empty:
#         st.subheader("Visualizations")

#         if selected_query == "List the allocation strategies for products with the 30 lowest inventory turnover rates":
#             turnover_by_strategy = result.groupby('Inventory_Allocation_Strategy')[
#                 'Inventory_Monthly_Turnover_Rate'].sum().reset_index()

#             bar_fig_turnover = px.bar(
#                 turnover_by_strategy,
#                 x='Inventory_Allocation_Strategy',
#                 y='Inventory_Monthly_Turnover_Rate',
#                 title='Sum of Inventory Turnover Rates by Allocation Strategy',
#             )

#             st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
#             st.plotly_chart(bar_fig_turnover)
#             st.markdown('</div>', unsafe_allow_html=True)

#     else:
#         st.write("Please select a query from the dropdown menu.")

# with col[2]:
#     if result is not None and not result.empty:
#         st.subheader("")

#         if selected_query == "List the allocation strategies for products with the 30 lowest inventory turnover rates":
#             safety_stock_by_strategy = result.groupby('Inventory_Allocation_Strategy')[
#                 'Safety_Stock_Levels'].sum().reset_index()

#             bar_fig_safety_stock = px.bar(
#                 safety_stock_by_strategy,
#                 x='Inventory_Allocation_Strategy',
#                 y='Safety_Stock_Levels',
#                 title='Sum of Safety Stock Levels by Allocation Strategy',
#             )

#             bar_fig_turnover.update_layout(
#                 autosize=True,
#                 title={
#                     'text': """Sum of Inventory Turnover Rates 
#                         by Allocation Strategy""",
#                     'x': 0.5,
#                     'xanchor': 'center',
#                     'yanchor': 'top'
#                 },
#                 title_font=dict(size=14),
#                 margin=dict(l=0, r=0, t=40, b=0)
#             )
#             st.markdown('<div class="plotly-container">', unsafe_allow_html=True)
#             st.plotly_chart(bar_fig_safety_stock)
#             st.markdown('</div>', unsafe_allow_html=True)

else:
    pass
