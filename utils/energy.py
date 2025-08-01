import pandas as pd
from datetime import timedelta

def load_usage(filepath):
    df = pd.read_csv(filepath, parse_dates=["Date"])
    return df

def filter_usage(df, days):
    end = df["Date"].max()
    start = end - timedelta(days=days)
    return df[(df["Date"] >= start) & (df["Date"] <= end)]

def block_consumption(df):
    return df.groupby("Block")["Electricity_Used_kWh"].sum().reset_index()

def idle_blocks(df):
    summary = block_consumption(df)
    return summary[summary["Electricity_Used_kWh"] == 0]["Block"].tolist()