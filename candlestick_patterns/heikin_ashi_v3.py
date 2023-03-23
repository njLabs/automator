
def heiken_ashi(df):
    df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    df['HA_Open'] = (df['Open'].shift(1) + df['Open'].shift(1)) / 2
    df.iloc[0, df.columns.get_loc("HA_Open")] = (df.iloc[0]['Open'] + df.iloc[0]['Close']) / 2
    df['HA_High'] = df[['High', 'Low', 'HA_Open', 'HA_Close']].max(axis=1)
    df['HA_Low'] = df[['High', 'Low', 'HA_Open', 'HA_Close']].min(axis=1)
    df = df.drop(['Open', 'High', 'Low', 'Close'], axis=1)  # remove old columns
    df = df.rename(
        columns={"HA_Open": "Open", "HA_High": "High", "HA_Low": "Low", "HA_Close": "Close", "Volume": "Volume"})
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]  # reorder columns

    # df = df[['Symbol', 'Series', 'Prev Close', 'Open', 'High', 'Low', 'Last',
    #          'Close', 'VWAP', 'Volume', 'Turnover', 'Trades', 'Deliverable Volume',
    #          '%Deliverble']]  # reorder columns
    return df

