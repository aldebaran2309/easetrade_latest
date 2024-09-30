# easetrade_latest
Stock Market Prediction Using LSTM Model
This project is a web application that allows users to predict stock market prices using a pre-trained LSTM (Long Short-Term Memory) model. The app is built using Streamlit for the front-end and Keras with TensorFlow for the machine learning model. It uses historical stock data from Yahoo Finance via the yfinance library.

Features
Stock Ticker Input: Users can input the stock ticker symbol of any publicly traded company.
Dynamic Date Range: Users can choose the start and end dates for fetching the historical stock data.
Visualization:
Visualizes the stock’s closing prices over time.
Displays the 100-day and 200-day moving averages along with the closing prices.
Prediction:
Uses a pre-trained LSTM model to predict stock prices based on historical data.
Compares predicted prices with actual prices over the selected time period.
User-friendly Interface: Simple and interactive interface built with Streamlit.
Installation
Prerequisites
Before running this project, ensure you have Python 3.x and the following Python libraries installed:

streamlit
numpy
pandas
matplotlib
tensorflow
keras
yfinance
sklearn
pandas_datareader
Setup Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install required libraries:

You can install all the dependencies using pip:

bash
Copy code
pip install -r requirements.txt
Download or prepare your LSTM model:

Make sure you have your keras_model.h5 file (LSTM model) in the same directory as your main project file. If you haven't trained an LSTM model yet, follow the instructions in the next section to do so.

Run the Streamlit app:

To launch the application, simply run the following command:

bash
Copy code
streamlit run app.py
Access the app:

Once the app is running, it will provide a local URL (e.g., http://localhost:8501/) which you can open in your browser to use the application.

LSTM Model Training (Optional)
If you don't have the pre-trained keras_model.h5 file, you can train your own LSTM model with historical stock data. Here's a basic outline:

Collect Stock Data: Use the yfinance library to fetch stock data.

Preprocess Data: Scale the data using MinMaxScaler and prepare it for training (i.e., create sequences of past 100 days' data to predict the next day).

Build and Train LSTM Model: Use Keras to build a sequential LSTM model.

Save the Trained Model: After training the model, save it using model.save('keras_model.h5').



# Save the model
model.save("keras_model.h5")
Usage
Enter Stock Ticker: In the text box, enter the stock ticker symbol (e.g., AAPL for Apple Inc., RELIANCE.NS for Reliance Industries Ltd.).

Select Date Range: Choose the date range for the stock data you want to fetch. The model will use this data for prediction and visualization.

View Results:

Closing Price vs Time: The raw stock prices for the selected date range are plotted.
100-day and 200-day Moving Averages: The moving averages are displayed to analyze stock trends.
Prediction vs Original: The predicted stock prices based on the LSTM model are compared with the actual prices.
Example Output
The app generates the following charts:

Closing Price vs Time
100-day Moving Average vs Closing Price
200-day Moving Average vs Closing Price
Predicted vs Actual Stock Prices
Project Structure
