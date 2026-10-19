"""Optional Streamlit dashboard for an Azure SQL event-log database."""

import os

import pandas as pd
import pyodbc
import streamlit as st


def get_data_from_sql():
    required = ("AZURE_SQL_SERVER", "AZURE_SQL_DATABASE", "AZURE_SQL_USERNAME", "AZURE_SQL_PASSWORD")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={os.environ['AZURE_SQL_SERVER']};"
        f"DATABASE={os.environ['AZURE_SQL_DATABASE']};"
        f"UID={os.environ['AZURE_SQL_USERNAME']};"
        f"PWD={os.environ['AZURE_SQL_PASSWORD']}"
    )
    with pyodbc.connect(connection_string) as connection:
        return pd.read_sql("SELECT * FROM wsn_events.dbo.events_log ORDER BY timestamp", connection)


st.title("IoT heritage-monitoring event log")
try:
    events = get_data_from_sql()
except RuntimeError as error:
    st.info(str(error))
    st.stop()

events["timestamp"] = pd.to_datetime(events["timestamp"], errors="coerce")
events = events.dropna(subset=["timestamp"])
st.dataframe(events, use_container_width=True)
st.bar_chart(events["event"].value_counts())
