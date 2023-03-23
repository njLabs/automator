# TODO: implement RSI strategy with divergence
# TODO: timeframe
import numpy as np
import pandas as pd
import talib as ta
# from pyti.linear_weighted_moving_average import linear_weighted_moving_average as lwma


class ComputeRsiResults:
    def compute_rsi_ma(self, ticker):
        df = ticker
        open, high, low, close = df['Open'], df['High'], df['Low'], df['Close']

        # implement RSI
        rsi = ta.RSI(close, timeperiod=14).fillna(0)
        RSI = pd.DataFrame(rsi, columns=['RSI']).fillna(0)
        ma21 = pd.DataFrame(ta.WMA(rsi, timeperiod=21), columns=['ma21'])  # TODO: check (WMA == LinearWightedMA)
        ma3 = pd.DataFrame(ta.EMA(rsi, timeperiod=3), columns=['ma3']).fillna(0)
        ma50 = pd.DataFrame(ta.EMA(close, timeperiod=55), columns=['ma50']).fillna(0)
        ma200 = pd.DataFrame(ta.EMA(close, timeperiod=200), columns=['ma200']).fillna(0)

        # store data in csv
        df['RSI'] = round(RSI, 2)
        df['ma3'] = round(ma3, 2)
        df['ma21'] = round(ma21, 2)
        df['ma50'] = round(ma50, 2)
        df['ma200'] = round(ma200, 2)
        DeathCross, GoldenCross = 0, 1
        # DeathCross, GoldenCross = 'DeathCross', 'GoldenCross'
        Buy, Sell = 1, 0
        # Buy, Sell = 'Buy', 'Sell'
        df['CrossOver'] = np.where(df['ma50'] < df['ma200'], DeathCross, GoldenCross)
        df['maCross'] = np.where(df['ma21'] >= df['ma3'], df['ma21'], df['ma3'])
        df['Signal'] = np.where(df['RSI'] >= df['maCross'], Buy, Sell)
        df['Signal21R'] = np.where(df['RSI'] >= df['ma21'], Buy, Sell)

        return df
