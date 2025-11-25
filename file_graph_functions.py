import matplotlib.pyplot as plt
import pandas as pd

from basic_page import weekly_summary,run_query
import streamlit as st
import io
def display_chart():
    chart_summary = weekly_summary()
    if chart_summary and chart_summary[0][0] is not None:
        total_fuel,total_distance,total_maintenance, total_fuel_cost, total_carbon_emissions, avg_efficiency = chart_summary[0]
        labels = ['Fuel (L)','Distance (km)','Maintenance (Rs)']
        values =  [total_fuel,total_distance,total_maintenance]

        fig,ax = plt.subplots()
        ax.bar(labels,values)
        st.pyplot(fig)
    else:
        st.write("No data for last 7 days")
def download_option():
    csv_summary = weekly_summary()
    if csv_summary and csv_summary[0][0] is not None:
        df = pd.DataFrame([csv_summary[0]],columns = [
            "total_fuel","total_distance", "total_maintenance",
            "total_fuel_cost", "total_carbon_emissions",
            "avg_fuel_efficiency"
        ])
        csv = df.to_csv(index = False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data  = csv,
            file_name = "weekly_summary.csv",
            mime = "text/csv"
        )
    else:
        st.write("No data to download")
@st.cache_data(ttl=3600)
def monthly_summary():
    query = """
        SELECT
            SUM(fuel_used),
            SUM(distance),
            SUM(maintenance),
            SUM(fuel_cost),
            SUM(carbon_emissions),
            AVG(fuel_efficiency)
        FROM transport_logs
        WHERE entry_date >= CURRENT_DATE - INTERVAL '30 days';
    """
    return run_query(query)
def display_monthly_summary():
    month_summary = monthly_summary()
    if month_summary and month_summary[0][0] is not None:
        total_fuel, total_distance, total_maintenance, total_fuel_cost, total_carbon_emissions, avg_eff = month_summary[0]

        st.subheader("Monthly Summary (Last 30 Days)")
        st.write(f"**Total Fuel Used:** {total_fuel} L")
        st.write(f"**Total Distance:** {total_distance} km")
        st.write(f"**Total Maintenance:** ₹{total_maintenance}")
        st.write(f"**Total Fuel Cost:** ₹{total_fuel_cost}")
        st.write(f"**Total Carbon Emissions:** {total_carbon_emissions} kg")
        st.write(f"**Average Fuel Efficiency:** {avg_eff:.2f} km/L")
    else:
        st.write("No data for last 30 days")
