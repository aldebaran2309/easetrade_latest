import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import datetime

try:
    ticker = "^NSEI"
    start_date = st.date_input("Enter Start date", datetime.date(2014, 1, 1))
    end_date = st.date_input("Enter End date", datetime.date.today())

    st.title("NIFTY 50 HEATMAP")
    # Download the historical data for NIFTY 50
    data = yf.download(ticker, start=start_date, end=end_date)

    # Resample the data on a monthly basis
    data_monthly = data.resample("M").last()

    # Calculate the monthly returns
    monthly_returns = data_monthly["Adj Close"].pct_change()

    # Convert monthly returns to a pandas DataFrame
    monthly_returns_df = pd.DataFrame(monthly_returns)

    # Pivot the DataFrame to create a matrix of monthly returns by year and month
    monthly_returns_matrix = monthly_returns_df.pivot_table(
        values="Adj Close",
        index=monthly_returns_df.index.year,
        columns=monthly_returns_df.index.month,
    )

    # Set the column names to the month names
    monthly_returns_matrix.columns = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    # Multiply by 100 to convert to percentages
    monthly_returns_matrix *= 100

    # Set the font scale
    sns.set(font_scale=1.2)

    # Plot the heatmap using seaborn
    ab = plt.figure(figsize=(16, 10))
    sns.heatmap(
        monthly_returns_matrix,
        annot=True,
        cmap="RdYlGn",
        center=0,
        fmt=".2f",  # This ensures two decimal places
        cbar=True,  # Display color bar
        cbar_kws={"format": "%.0f%%"},  # Format color bar as percentage
    )
    plt.title("Nifty Monthly Returns by Year and Month", fontsize=20)
    plt.xlabel("Month", fontsize=14)
    plt.ylabel("Year", fontsize=12)
    plt.yticks(rotation=45)
    st.pyplot(ab)

except Exception as e:
    st.error(f"Error: {e}")
