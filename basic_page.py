import  streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from file_graph_functions import *
@st.cache_resource#23/11/25
def get_connection():
    return psycopg2.connect(
        dbname="bizops_Database",
        user="postgres",
        password="Postgres123@",
        host="localhost",
        port="5432"  # Default PostgreSQL port
    )
cursor = get_connection()#23/11/25
# cursor = conn.cursor()#19-11-25
# data =  []
st.title("Welcome BizOps")
st.text("Lets make your business more profitable")
st.header("Please enter the following details")
date = st.date_input("Date")
fuel_used = st.number_input("Fuel used (litres",min_value=0.0,step = 0.1)
distance = st.number_input("Distance (km)",min_value=0.0,step = 0.1)
maintenance = st.number_input("Maintenance Cost",min_value=0.0,step = 10.0)
#21/11/25--->calculating values for total usage
fuel_cost = fuel_used * 108
fuel_efficiency = 0
if fuel_used!=0:
    fuel_efficiency =  distance/fuel_used
else:
    fuel_efficiency = 0
total_transport_cost = fuel_cost + maintenance
carbon_emissions = fuel_used*2.64
@st.cache_data(ttl=3600)
def weekly_summary():
    query = """
        SELECT
            SUM(fuel_used) AS total_fuel,
            SUM(distance) AS total_distance,
            SUM(maintenance) AS total_maintenance,
            SUM(fuel_cost) AS total_fuel_cost,
            SUM(carbon_emissions) AS total_carbon_emissions,
            AVG(fuel_efficiency) AS avg_fuel_efficiency
        FROM transport_logs
        WHERE entry_date >= CURRENT_DATE- INTERVAL '7 days';
    """
    return run_query(query)
###21/11/25
insert_query = "INSERT INTO transport_logs(entry_date,fuel_used,distance,maintenance,fuel_cost,fuel_efficiency,total_transport_cost,carbon_emissions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" #19/11/25
data_to_insert = (date, fuel_used, distance, maintenance,fuel_cost,fuel_efficiency,total_transport_cost,carbon_emissions)#after maintenence the part was added on 21/11 up and down
if st.button("Insert Data"):#19-11/25
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(insert_query, data_to_insert)
        conn.commit()
    st.success("Data Inserted!")
def run_query(query,params=None):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
if st.button("Show My data"):
    st.write("Your data")
    rows = run_query("SELECT * FROM transport_logs")
    # print(rows)
    df = pd.DataFrame(rows,columns=["id", "entry_date", "fuel_used", "distance", "maintenance","fuel_cost","fuel_efficiency","total_transport_cost","carbon_emissions"])
    st.table(df)
if st.button("Show Weekly Summary"):
    summary = weekly_summary()
    if not summary or len(summary) == 0:
        st.write("No data for the 7 last days")
    else:
        (
            total_fuel,
            total_distance,
            total_maintenance,
            total_fuel_cost,
            total_carbon_emissions,
            avg_fuel_efficiency
        ) = summary[0]
        total_fuel = total_fuel or 0
        total_distance = total_distance or 0
        total_maintenance = total_maintenance or 0
        total_fuel_cost = total_fuel_cost or 0
        total_carbon_emissions = total_carbon_emissions or 0
        avg_fuel_efficiency = avg_fuel_efficiency or 0
    if total_fuel > 0:
        avg_eff = total_distance / total_fuel
    else:
        avg_eff = 0
    st.subheader("Weekly Summary (Last 7 Days)")
    st.write(f"**Total Fuel Used:** {total_fuel} litres")
    st.write(f"**Total Distance:** {total_distance} km")
    st.write(f"**Total Maintenance:** ₹{total_maintenance}")
    st.write(f"**Total Fuel Cost:** ₹{total_fuel_cost}")
    st.write(f"**Total Carbon Emissions:** {total_carbon_emissions} kg CO2")
    st.write(f"**Average Fuel Efficiency:** {avg_fuel_efficiency:.2f} km/litre")
if st.button("Show Weekly Chart"):
    display_chart()
if st.button("Download Data"):
    download_option()
if st.button("Show Monthly Summary"):
    display_monthly_summary()
#displaying data in streamlit
#Close the connection always
# cursor.close()
# conn.close()
# print("Connection closed")#19/11/25
14/11/25
# data.append([date,fuel_used,distance,maintenance])
# column_name = ['date','fuel_used','distance','maintenance']
# st.button("View Data")
# df = pd.DataFrame(data, columns = column_name)
# st.subheader("Your Data")
# st.dataframe(df)
#FuelCost
# Fuel_Cost = round(fuel_used * 108,2)
# Total_transport_cost = Fuel_Cost + maintenance
# Fuel_efficiency = int(distance/fuel_used)
# if st.button("Add Entry"):
#     st.success("Entry added(temporary – will connect to database soon)")
# 6/11/25 -->improved on 8/11/25
#8/11/25
# st.text_input("How many employees")
# st.text_input("What kind of transport do you use")
# st.text_input("How do you calculate raw material in you business")
