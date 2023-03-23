import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def breakout(df):
    # Define the rolling window size
    window = 20

    # Calculate the rolling mean and standard deviation
    rolling_mean = df['Close'].rolling(window).mean()
    rolling_std = df['Close'].rolling(window).std()

    # Define the threshold for a breakout
    threshold = 2 * rolling_std

    # Create a new column that indicates if there is a breakout
    df['Breakout'] = np.where(df['Close'] > rolling_mean + threshold, 1, 0)

    # Plot the data
    plt.plot(df['Close'], label='Close Price')
    plt.plot(rolling_mean, label='Rolling Mean')
    plt.plot(rolling_mean + threshold, label='Threshold')
    plt.fill_between(df.index, rolling_mean - threshold, rolling_mean + threshold, alpha=0.1)
    plt.legend()
    plt.show()
    return df


# Load BankNifty data into a Pandas DataFrame
df = pd.read_csv("banknifty.csv")
