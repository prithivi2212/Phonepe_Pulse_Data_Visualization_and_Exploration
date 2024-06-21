import streamlit as st
from streamlit_option_menu import option_menu
import pymysql 
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image


#DataFrame Creation

#Connection to MySQL

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Mysql@123",
    database="Phonepe_data",
    port = 3306
    )
cursor =conn.cursor()

#aggregate_transaction_df
cursor.execute("SELECT* FROM aggregated_transaction")
conn.commit()
table1 = cursor.fetchall()

Agg_transaction = pd.DataFrame(table1, columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#aggregate_users_df
cursor.execute("SELECT* FROM aggregated_users")
conn.commit()
table2 = cursor.fetchall()

Agg_users = pd.DataFrame(table2, columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#aggregate_insurance_df
cursor.execute("SELECT* FROM aggregated_insurance")
conn.commit()
table3 = cursor.fetchall()

Agg_insurance = pd.DataFrame(table3, columns = ("States", "Years", "Quarter", "Name", "Transaction_count", "Transaction_amount"))

#map_transaction_df
cursor.execute("SELECT* FROM map_transaction")
conn.commit()
table4 = cursor.fetchall()

Map_transaction = pd.DataFrame(table4, columns = ("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))

#map_users_df
cursor.execute("SELECT* FROM map_users")
conn.commit()
table5 = cursor.fetchall()

Map_users = pd.DataFrame(table5, columns = ("States", "Years", "Quarter", "District", "Registered_users", "appOpens"))

#map_insurance_df
cursor.execute("SELECT* FROM map_insurance")
conn.commit()
table6 = cursor.fetchall()

Map_Insurance = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))

#top_transaction_df
cursor.execute("SELECT* FROM top_transaction")
conn.commit()
table7 = cursor.fetchall()

Top_transaction = pd.DataFrame(table7, columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#top_users_df
cursor.execute("SELECT* FROM top_users")
conn.commit()
table8 = cursor.fetchall()

Top_Users = pd.DataFrame(table8, columns = ("States", "Years", "Quarter", "Pincodes", "Registered_Users"))

#top_insurance_df
cursor.execute("SELECT* FROM top_insurance")
conn.commit()
table9 = cursor.fetchall()

Top_Insurance = pd.DataFrame(table9, columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))



#Transaction Amount Year

def Transaction_amount_count_Y(df, year):
    tacy = df[df["Years"] == year]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x= "States", y= "Transaction_amount", title = f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 650, width = 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x= "States", y= "Transaction_count", title = f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Peach_r, height = 650, width = 600)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", 
                                    color= "Transaction_amount", color_continuous_scale= "tealrose",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()), 
                                    hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds = "locations",
                                    height = 650, width = 600)
        fig_india_1.update_geos(visible= False)                            
        st.plotly_chart(fig_india_1)  

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", 
                                    color= "Transaction_count", color_continuous_scale= "tealrose",
                                    range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()), 
                                    hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds = "locations",
                                    height = 650, width = 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy


#Transaction Amount Quarter

def Transaction_amount_count_YQ(df, quarter):
    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x= "States", y= "Transaction_amount", title = f"{tacy['Years'].min()}, QUARTER {quarter} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 650, width = 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x= "States", y= "Transaction_count", title = f"{tacy['Years'].min()}, QUARTER {quarter} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Peach_r, height = 650, width = 600)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)

        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", 
                                    color= "Transaction_amount", color_continuous_scale= "tealrose",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()), 
                                    hover_name= "States", title= f"{tacy['Years'].min()},  QUARTER {quarter} TRANSACTION AMOUNT", fitbounds = "locations",
                                    height = 650, width = 600)
        fig_india_1.update_geos(visible= False)                            
        st.plotly_chart(fig_india_1)  

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", 
                                    color= "Transaction_count", color_continuous_scale= "tealrose",
                                    range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()), 
                                    hover_name= "States", title= f"{tacy['Years'].min()}, QUARTER {quarter} TRANSACTION COUNT", fitbounds = "locations",
                                    height = 650, width = 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

#Aggregated Transaction Type
   
def Agg_trans_type(df, state):
    tacy = df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= tacyg, names = "Transaction_type", values = "Transaction_amount",
                        width = 600, title = f"{state.upper()} TRANSACTION AMOUNT", hole = 0.5)
        st.plotly_chart(fig_pie_1)
    
    with col2:
        fig_pie_2 = px.pie(data_frame= tacyg, names = "Transaction_type", values = "Transaction_count",
                        width = 600, title = f"{state.upper()} TRANSACTION COUNT", hole = 0.5)
        st.plotly_chart(fig_pie_2)

#Aggegated Users 1

def Agg_user_plt1(df, year):
    aguy = Agg_users[Agg_users["Years"] == 2018]
    aguy.reset_index(drop = True, inplace = True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace = True)

    fig_bar_1 = px.bar(aguyg, x = "Brands", y = "Transaction_count", title = f"{year} BRANDS & TRANSACTION COUNT",
                    width = 800, color_discrete_sequence= px.colors.sequential.Emrld, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggregated User 2

def Agg_user_plt2(df, quarter):
    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop = True, inplace = True)

    aguyqg =pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace = True)

    fig_bar_2 = px.bar(aguyqg, x = "Brands", y = "Transaction_count", title = f"QUARTER {quarter}, BRANDS & TRANSACTION COUNT",
                        width = 800, color_discrete_sequence= px.colors.sequential.Peach_r)
    st.plotly_chart(fig_bar_2)

    return aguyq

#Aggregated User 3

def Agg_user_plt3(df, state):
    auyqs = df[df["States"] == state]
    auyqs.reset_index(drop = True, inplace = True)

    # Grouping by 'Brands' and summing the 'Transaction_count'
    auyqs_grouped = auyqs.groupby("Brands")[["Transaction_count", "Percentage"]].sum().reset_index()

    fig_line_1 = px.line(auyqs_grouped, x = "Brands", y = "Transaction_count", hover_data= ["Percentage"],
                        title = f"{state.upper()} BRANDS, TRANSACTION COUNTS & PERCENTAGE", width = 1000, markers = True)
    st.plotly_chart(fig_line_1)

#Map Insurance

def Map_insr_dist(df, state):
    tacy = df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("District")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x = "Transaction_amount", y = "District", orientation= "h", height = 600,
                        title = f"{state.upper()} DISTRICTS & TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:    
        fig_bar_2 = px.bar(tacyg, x = "Transaction_count", y = "District", orientation= "h", height = 600,
                        title = f"{state.upper()} DISTRICTS & TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

# Map Users Plot 1

def map_user_plot1(df, year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop = True, inplace = True)

    muyg = muy.groupby("States")[["Registered_users", "appOpens"]].sum()
    muyg.reset_index(inplace = True)

    fig_line_1 = px.line(muyg, x = "States", y = ["Registered_users", "appOpens"],
                            title = f" {year} REGISTERED USERS & APPOPENS", width = 1000, height = 800, markers = True)
    st.plotly_chart(fig_line_1)

    return muy


# Map Users Plot 2

def map_user_plot2(df, quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop = True, inplace = True)

    muyqg = muyq.groupby("States")[["Registered_users", "appOpens"]].sum()
    muyqg.reset_index(inplace = True)

    fig_line_2 = px.line(muyqg, x = "States", y = ["Registered_users", "appOpens"],
                            title = f"{df['Years'].min()} QUARTER {quarter} - REGISTERED USERS & APPOPENS", width = 1000, height = 800, markers = True,
                            color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_2)

    return muyq

# Map Users Plot 3

def map_user_plot3(df, state):
    muyqs = df[df["States"] ==state]
    muyqs.reset_index(drop = True, inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x = "Registered_users", y = "District", orientation= "h",
                                title = f"{state.upper()} REGISTERED USERS", height = 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x = "appOpens", y = "District", orientation= "h",
                                title = f"{state.upper()} APPOPENS", height = 800, color_discrete_sequence= px.colors.sequential.Emrld_r)
        st.plotly_chart(fig_map_user_bar_2)

# Top Insurance Plot 1

def Top_Insurance_plot1(df, state):
    tiy = df[df["States"] == state]
    tiy.reset_index(drop = True, inplace = True)

    tiyg = tiy.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    tiyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)

    with col1:
        fig_top_insr_bar_1 = px.bar(tiy, x = "Quarter", y = "Transaction_amount", hover_data= "Pincodes",
                                    title = f"{state.upper()} TRANSACTION AMOUNT", height = 650, width = 600, color_discrete_sequence= px.colors.sequential.Oryel_r)
        st.plotly_chart(fig_top_insr_bar_1) 

    with col2:
        fig_top_insr_bar_2 = px.bar(tiy, x = "Quarter", y = "Transaction_count", hover_data= "Pincodes",
                                    title = f"{state.upper()} TRANSACTION COUNT", height = 650, width = 600, color_discrete_sequence= px.colors.sequential.Oryel)
        st.plotly_chart(fig_top_insr_bar_2)       
   

# Top User Plot 1

def Top_user_plot1(df, year):
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop = True, inplace = True)

    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarter"])["Registered_Users"].sum())
    tuyg.reset_index(inplace = True)

    fig_top_plot1 = px.bar(tuyg, x = "States", y = "Registered_Users", color = "Quarter", width = 1000, height = 800,
                        title = f"{year} REGISTERED USERS", color_discrete_sequence= px.colors.sequential.PuRd, hover_name= "States")
    st.plotly_chart(fig_top_plot1)

    return tuy

# Top user plot 2

def Top_user_plot2(df, state):
    tuys = df[df["States"] == state]
    tuys.reset_index(drop = True, inplace = True)

    fig_top_plot2 = px.bar(tuys, x = "Quarter", y = "Registered_Users", title = "REGISTERED USERS, PINCODES, QUARTERS",
                        width = 1000, height = 800, color = "Registered_Users", hover_data= "Pincodes", 
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot2)


#Top_chart SQL Query(Trans Amount)

def top_chart_trans_amount(table_name):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Mysql@123",
        database="Phonepe_data",
        port = 3306
        )
    cursor =conn.cursor()

    #plot1
    query1 = f'''SELECT States, sum(Transaction_amount) as Transaction_Amount 
                FROM {table_name}
                GROUP BY States
                Order by Transaction_Amount desc
                limit 10;'''

    cursor.execute(query1)
    table1= cursor.fetchall()
    conn.commit()

    df_1= pd.DataFrame(table1, columns= ("States", "Transaction_Amount"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount1 = px.bar(df_1, x= "States", y= "Transaction_Amount", title = "TOP 10 TRANSACTION AMOUNT", hover_name="States",
                                color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 650, width = 600)
        st.plotly_chart(fig_amount1)

    #plot2
    query2 = f'''SELECT States, sum(Transaction_amount) as Transaction_Amount 
                FROM {table_name}
                GROUP BY States
                Order by Transaction_Amount
                limit 10;'''

    cursor.execute(query2)
    table2= cursor.fetchall()
    conn.commit()

    df_2= pd.DataFrame(table2, columns= ("States", "Transaction_Amount"))

    with col2:
        fig_amount2 = px.bar(df_2, x= "States", y= "Transaction_Amount", title = "BOTTOM 10 TRANSACTION AMOUNT", hover_name="States",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height = 650, width = 600)
        st.plotly_chart(fig_amount2)

    #plot3
    query3 = f'''SELECT States, sum(Transaction_amount) as Transaction_Amount 
                FROM {table_name}
                GROUP BY States
                Order by Transaction_Amount'''

    cursor.execute(query3)
    table3= cursor.fetchall()
    conn.commit()

    df_3= pd.DataFrame(table3, columns= ("States", "Transaction_Amount"))

    fig_amount3 = px.bar(df_3, y= "States", x= "Transaction_Amount", title = "AVERAGE TRANSACTION AMOUNT", hover_name="States", orientation = "h",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 800, width = 1000)
    st.plotly_chart(fig_amount3)


#Top_chart SQL Query (Trans Count)

def top_chart_trans_count(table_name):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Mysql@123",
        database="Phonepe_data",
        port = 3306
        )
    cursor =conn.cursor()

    #plot1
    query1 = f'''SELECT States, sum(Transaction_count) as Transaction_Count 
                FROM {table_name}
                GROUP BY States
                Order by Transaction_Count desc
                limit 10;'''

    cursor.execute(query1)
    table1= cursor.fetchall()
    conn.commit()

    df_1= pd.DataFrame(table1, columns= ("States", "Transaction_Count"))

    col1, col2= st.columns(2)

    with col1:
        fig_amount1 = px.bar(df_1, x= "States", y= "Transaction_Count", title = "TOP 10 TRANSACTION COUNT", hover_name="States",
                                color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 650, width = 600)
        st.plotly_chart(fig_amount1)

    #plot2
    query2 = f'''SELECT States, sum(Transaction_count) as Transaction_Count 
                FROM {table_name}
                GROUP BY States
                Order by Transaction_Count
                limit 10;'''

    cursor.execute(query2)
    table2= cursor.fetchall()
    conn.commit()

    df_2= pd.DataFrame(table2, columns= ("States", "Transaction_Count"))

    with col2:
        fig_amount2 = px.bar(df_2, x= "States", y= "Transaction_Count", title = "BOTTOM 10 TRANSACTION COUNT", hover_name="States",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height = 650, width = 600)
        st.plotly_chart(fig_amount2)

    #plot3
    query3 = f'''SELECT States, sum(Transaction_count) as Transaction_Count 
                FROM {table_name}
                GROUP BY States
                Order by Transaction_Count'''

    cursor.execute(query3)
    table3= cursor.fetchall()
    conn.commit()

    df_3= pd.DataFrame(table3, columns= ("States", "Transaction_Count"))

    fig_amount3 = px.bar(df_3, y= "States", x= "Transaction_Count", title = "AVERAGE TRANSACTION COUNT", hover_name="States", orientation = "h",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 800, width = 1000)
    st.plotly_chart(fig_amount3)


#Top_chart SQL Query(Registered Users)

def top_chart_reg_users(table_name, state):
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Mysql@123",
            database="Phonepe_data",
            port = 3306
            )
        cursor =conn.cursor()

        #plot1
        query1 = f'''SELECT Districts, SUM(Registered_Users) AS Registered_Users 
                     FROM {table_name}
                     WHERE States = '{state}'
                     GROUP BY Districts
                     ORDER BY Registered_Users DESC
                     LIMIT 10;'''

        cursor.execute(query1)
        table1= cursor.fetchall()
        conn.commit()

        df_1= pd.DataFrame(table1, columns= ("Districts", "Registered_Users"))

        col1, col2 = st.columns(2)
        with col1:
            fig_amount1 = px.bar(df_1, x= "Districts", y= "Registered_Users", title = "TOP 10 REGISTERED USERS", hover_name="Districts",
                                    color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 650, width = 600)
            st.plotly_chart(fig_amount1)

        #plot2
        query2 = f'''SELECT Districts, SUM(Registered_Users) AS Registered_Users 
                     FROM {table_name}
                     WHERE States = '{state}'
                     GROUP BY Districts
                     ORDER BY Registered_Users
                     LIMIT 10;'''

        cursor.execute(query2)
        table2= cursor.fetchall()
        conn.commit()

        df_2= pd.DataFrame(table2, columns= ("Districts", "Registered_Users"))

        with col2:
            fig_amount2 = px.bar(df_2, x= "Districts", y= "Registered_Users", title = "BOTTOM 10 REGISTERED USERS", hover_name="Districts",
                                    color_discrete_sequence=px.colors.sequential.Agsunset, height = 650, width = 600)
            st.plotly_chart(fig_amount2)

        #plot2
        query3 = f'''SELECT Districts, AVG(Registered_Users) AS Registered_Users 
                     FROM {table_name}
                     WHERE States = '{state}'
                     GROUP BY Districts
                     ORDER BY Registered_Users'''

        cursor.execute(query3)
        table3= cursor.fetchall()
        conn.commit()

        df_3= pd.DataFrame(table3, columns= ("Districts", "Registered_Users"))

        fig_amount3 = px.bar(df_3, y= "Districts", x= "Registered_Users", title = "AVERAGE REGISTERED USERS", hover_name="Districts", orientation = "h",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount3)

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        # Ensure the connection is closed
        cursor.close()
        conn.close()

#Top_chart SQL Query(AppOpens)

def top_chart_appopens(table_name, state):
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Mysql@123",
            database="Phonepe_data",
            port = 3306
            )
        cursor =conn.cursor()

        #plot1
        query1 = f'''SELECT Districts, SUM(appOpens) AS AppOpens 
                     FROM {table_name}
                     WHERE States = '{state}'
                     GROUP BY Districts
                     ORDER BY AppOpens DESC
                     LIMIT 10;'''

        cursor.execute(query1)
        table1= cursor.fetchall()
        conn.commit()

        df_1= pd.DataFrame(table1, columns= ("Districts", "AppOpens"))

        col1, col2 = st.columns(2)
        with col1:
            fig_amount1 = px.bar(df_1, x= "Districts", y= "AppOpens", title = "TOP 10 APP OPENS", hover_name="Districts",
                                    color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 650, width = 600)
            st.plotly_chart(fig_amount1)

        #plot2
        query2 = f'''SELECT Districts, SUM(appOpens) AS AppOpens 
                     FROM {table_name}
                     WHERE States = '{state}'
                     GROUP BY Districts
                     ORDER BY AppOpens
                     LIMIT 10;'''

        cursor.execute(query2)
        table2= cursor.fetchall()
        conn.commit()

        df_2= pd.DataFrame(table2, columns= ("Districts", "AppOpens"))

        with col2:
            fig_amount2 = px.bar(df_2, x= "Districts", y= "AppOpens", title = "BOTTOM 10 APP OPENS", hover_name="Districts",
                                    color_discrete_sequence=px.colors.sequential.Agsunset, height = 650, width = 600)
            st.plotly_chart(fig_amount2)

        #plot2
        query3 = f'''SELECT Districts, AVG(appOpens) AS AppOpens 
                     FROM {table_name}
                     WHERE States = '{state}'
                     GROUP BY Districts
                     ORDER BY AppOpens'''

        cursor.execute(query3)
        table3= cursor.fetchall()
        conn.commit()

        df_3= pd.DataFrame(table3, columns= ("Districts", "AppOpens"))

        fig_amount3 = px.bar(df_3, y= "Districts", x= "AppOpens", title = "AVERAGE APP OPENS", hover_name="Districts", orientation = "h",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount3)

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        # Ensure the connection is closed
        cursor.close()
        conn.close()


#Top_chart SQL Query(Registered Users - Top)

def top_chart_reg_users_tp(table_name):
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Mysql@123",
            database="Phonepe_data",
            port = 3306
            )
        cursor =conn.cursor()

        #plot1
        query1 = f'''SELECT States, sum(Registered_Users) as Registered_Users
                     FROM {table_name}
                     GROUP BY States
                     order by Registered_Users DESC
                     LIMIT 10;'''

        cursor.execute(query1)
        table1= cursor.fetchall()
        conn.commit()

        df_1= pd.DataFrame(table1, columns= ("States", "Registered_Users"))

        col1, col2 = st.columns(2)
        with col1:
            fig_amount1 = px.bar(df_1, x= "States", y= "Registered_Users", title = "TOP 10 REGISTERED USERS", hover_name="States",
                                    color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 650, width = 600)
            st.plotly_chart(fig_amount1)

        #plot2
        query2 = f'''select States, sum(Registered_Users) as Registered_Users
                     FROM {table_name}
                     GROUP BY States
                     order by Registered_Users 
                     LIMIT 10;'''
                     
        cursor.execute(query2)
        table2= cursor.fetchall()
        conn.commit()

        df_2= pd.DataFrame(table2, columns= ("States", "Registered_Users"))

        with col2:
            fig_amount2 = px.bar(df_2, x= "States", y= "Registered_Users", title = "BOTTOM 10 REGISTERED USERS", hover_name="States",
                                    color_discrete_sequence=px.colors.sequential.Agsunset, height = 650, width = 600)
            st.plotly_chart(fig_amount2)

        #plot3
        query3 = f'''select States, AVG(Registered_Users) as Registered_Users
                     FROM {table_name}
                     GROUP BY States
                     ORDER BY Registered_Users;'''
                     
        cursor.execute(query3)
        table3= cursor.fetchall()
        conn.commit()

        df_3= pd.DataFrame(table3, columns= ("States", "Registered_Users"))

        fig_amount3 = px.bar(df_3, y= "States", x= "Registered_Users", title = "AVERAGE REGISTERED USERS", hover_name="States", orientation = "h",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount3)

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        # Ensure the connection is closed
        cursor.close()
        conn.close()


#Streamlit Part

st.set_page_config(layout = "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

    select = option_menu("Main Menu", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])
                         
if select == "HOME":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is a prominent digital payments and financial services app based in India")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\Dell\Downloads\PhonePe-Logo.wine.png"), width = 700)

    col3,col4= st.columns(2)

    with col3:
        st.video(r"C:\Users\Dell\Videos\4K Video Downloader+\PhonePe - Introduction.mp4")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.video(r"C:\Users\Dell\Videos\4K Video Downloader+\PhonePe India's Leading Payments App.mp4")


elif select == "DATA EXPLORATION":
    
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method_1 = st.radio("Select The Method", ["Aggregated Transaction", "Aggregated User", "Aggregated Insurance"])

        if method_1 == "Aggregated Transaction":

            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year_AT", Agg_transaction["Years"].min(), Agg_transaction["Years"].max(), Agg_transaction["Years"].min())
            agg_trac_Y = Transaction_amount_count_Y(Agg_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_AT", agg_trac_Y["States"].unique())
            Agg_trans_type(agg_trac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter_AT", agg_trac_Y["Quarter"].min(), agg_trac_Y["Quarter"].max(), agg_trac_Y["Quarter"].min())
            agg_trac_YQ = Transaction_amount_count_YQ(agg_trac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_At", agg_trac_YQ["States"].unique())

            Agg_trans_type(agg_trac_YQ, states)
            

        elif method_1 == "Aggregated User":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year_AU", Agg_users["Years"].min(), Agg_users["Years"].max(), Agg_users["Years"].min())
            Agg_user_Y = Agg_user_plt1(Agg_users, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter_AU", Agg_user_Y["Quarter"].min(), Agg_user_Y["Quarter"].max(), Agg_user_Y["Quarter"].min())
            Agg_user_YQ = Agg_user_plt2(Agg_user_Y, quarters)

            states = st.selectbox("Select The State_AU", Agg_user_YQ["States"].unique())
            Agg_user_YQS = Agg_user_plt3(Agg_user_YQ, states)

        

        elif method_1 == "Aggregated Insurance":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year_AI", Agg_insurance["Years"].min(), Agg_insurance["Years"].max(), Agg_insurance["Years"].min())
            tac_Y = Transaction_amount_count_Y(Agg_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_AI", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())
            Transaction_amount_count_YQ(tac_Y, quarters)



    with tab2:
        method_2 = st.radio("Select The Method", ["Map Transaction", "Map User", "Map Insurance"])

        if method_2 == "Map Transaction":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year_MT", Map_transaction["Years"].min(), Map_transaction["Years"].max(), Map_Insurance["Years"].min())
            map_trans_Y = Transaction_amount_count_Y(Map_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_MT", map_trans_Y["States"].unique())
            Map_insr_dist(map_trans_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select A Quarter_MT", map_trans_Y["Quarter"].min(), map_trans_Y["Quarter"].max(), map_trans_Y["Quarter"].min())
            map_trans_YQ = Transaction_amount_count_YQ(map_trans_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Mt", map_trans_YQ["States"].unique())

            Map_insr_dist(map_trans_YQ, states)

        elif method_2 == "Map User":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year_Map", Map_users["Years"].min(), Map_users["Years"].max(), Map_Insurance["Years"].min())
            map_user_Y = map_user_plot1(Map_users, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select A Quarter_Map", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min())
            map_user_YQ = map_user_plot2(map_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Map", map_user_YQ["States"].unique())

            map_user_plot3(map_user_YQ, states)


        elif method_2 == "Map Insurance":

            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year_MI", Map_Insurance["Years"].min(), Map_Insurance["Years"].max(), Map_Insurance["Years"].min())
            map_insr_Y = Transaction_amount_count_Y(Map_Insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_MI", map_insr_Y["States"].unique())
            Map_insr_dist(map_insr_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter_MI", map_insr_Y["Quarter"].min(), map_insr_Y["Quarter"].max(), map_insr_Y["Quarter"].min())
            map_insr_YQ = Transaction_amount_count_YQ(map_insr_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Mi", map_insr_YQ["States"].unique())

            Map_insr_dist(map_insr_YQ, states)


    
    with tab3:
        method_3 = st.radio("Select The Method", ["Top Transaction", "Top User", "Top Insurance"])

        if method_3 == "Top Transaction":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year_TT", Top_transaction["Years"].min(), Top_transaction["Years"].max(), Top_transaction["Years"].min())
            Top_trans_Y = Transaction_amount_count_Y(Top_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_TT", Top_trans_Y["States"].unique())
            Top_Insurance_plot1(Top_trans_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select A Quarter_TT", Top_trans_Y["Quarter"].min(), Top_trans_Y["Quarter"].max(), Top_trans_Y["Quarter"].min())
            Top_trans_YQ = Transaction_amount_count_YQ(Top_trans_Y, quarters)
            

        elif method_3 == "Top User":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year_TU", Top_Users["Years"].min(), Top_Users["Years"].max(), Top_Users["Years"].min())
            Top_user_Y = Top_user_plot1(Top_Users, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Tu", Top_user_Y["States"].unique())
            Top_user_plot2(Top_user_Y, states)


        elif method_3 == "Top Insurance":

            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year_Ti", Top_Insurance["Years"].min(), Top_Insurance["Years"].max(), Top_Insurance["Years"].min())
            top_insr_Y = Transaction_amount_count_Y(Top_Insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State_Ti", top_insr_Y["States"].unique())
            Top_Insurance_plot1(top_insr_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select A Quarter_Ti", top_insr_Y["Quarter"].min(), top_insr_Y["Quarter"].max(), top_insr_Y["Quarter"].min())
            top_insr_YQ = Transaction_amount_count_YQ(top_insr_Y, quarters)



elif select == "TOP CHARTS":
    
    questions = st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction" ,
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. AppOpens of Map User",
                                                    "10.Registered users of Top User",
                                                    ])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

    if questions == "1. Transaction Amount and Count of Aggregated Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("aggregated_insurance")

    elif questions == "2. Transaction Amount and Count of Map Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("map_insurance")

    elif questions == "3. Transaction Amount and Count of Top Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("top_insurance")

    elif questions == "4. Transaction Amount and Count of Aggregated Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("aggregated_transaction")

    elif questions == "5. Transaction Amount and Count of Map Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("map_transaction")

    elif questions == "6. Transaction Amount and Count of Top Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("top_transaction")

    elif questions == "7. Transaction Count of Aggregated User":
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_count("aggregated_users")

    elif questions == "8. Registered users of Map User":
        
        states = st.selectbox("Select the State", Map_users["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_reg_users("map_users", states)

    elif questions == "9. AppOpens of Map User":

        states = st.selectbox("Select the State", Map_users["States"].unique())
        st.subheader("APP OPENS")
        top_chart_appopens("map_users", states)

    elif questions == "10.Registered users of Top User":
        st.subheader("REGISTERED USERS")
        top_chart_reg_users_tp("top_users")