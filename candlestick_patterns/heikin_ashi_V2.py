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
