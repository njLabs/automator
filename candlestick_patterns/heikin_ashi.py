import pandas as pd
import plotly.express as px

# Load the data into a pandas DataFrame
df = pd.read_csv("candlestick_data.csv")

# Calculate the average price
df['average_price'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

# Calculate the Heikin-ashi close
df['heikin_ashi_close'] = (df['heikin_ashi_close'].shift(1) + df['average_price']) / 2

# Calculate the Heikin-ashi open
df['heikin_ashi_open'] = (df['heikin_ashi_open'].shift(1) + df['heikin_ashi_close'].shift(1)) / 2

# Calculate the Heikin-ashi high
df['heikin_ashi_high'] = df[['average_price', 'heikin_ashi_close', 'heikin_ashi_open']].max(axis=1)

# Calculate the Heikin-ashi low
df['heikin_ashi_low'] = df[['average_price', 'heikin_ashi_close', 'heikin_ashi_open']].min(axis=1)

# Plot the Heikin-ashi chart
fig = px.candlestick(df,
                     open='heikin_ashi_open',
                     high='heikin_ashi_high',
                     low='heikin_ashi_low',
                     close='heikin_ashi_close',
                     title='Heikin-ashi Candlestick Chart')
fig.show()



import pandas as pd

def heikin_ashi(df):
    df = df.copy()
    df['ha_close'] = (df['open'] + df['close']) / 2
    df.loc[:, 'ha_open'] = df.loc[:, 'ha_close'].shift(1)
    df.loc[df.index[0], 'ha_open'] = (df.loc[df.index[0], 'open'] + df.loc[df.index[0], 'close']) / 2
    df['ha_high'] = df[['high', 'ha_open', 'ha_close']].max(axis=1)
    df['ha_low'] = df[['low', 'ha_open', 'ha_close']].min(axis=1)
    return df

# Load the data into a pandas DataFrame
df = pd.read_csv("candlestick_data.csv")

# Convert the candlestick chart to Heikin-ashi chart
df = heikin_ashi(df)

# Show the Heikin-ashi chart
print(df)
