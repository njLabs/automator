import talib as ta
import pandas as pd
import numpy as np
from indicators import (
    SuperTrend,
    MACD,
    has_cross,
)
from historical_data import client


def super_trend(tf=15):
    df = client.historical_data('N', 'C', 1660, f'{tf}m', '2023-02-02', '2023-02-27')
    df = SuperTrend(df, 10, 1.5)
    return df


def macd(tf=30):
    df = client.historical_data('N', 'C', 1660, f'{tf}m', '2023-02-02', '2023-02-27')
    df = MACD(df)
    return df


def multi_emas(tf=5):
    df = client.historical_data('N', 'C', 1660, f'{tf}m', '2023-02-02', '2023-02-27')
    df['ema_5'] = ta.EMA(df['Close'], timeperiod=5)
    df['ema_13'] = ta.EMA(df['Close'], timeperiod=13)
    df['ema_26'] = ta.EMA(df['Close'], timeperiod=26)
    df['ema_50'] = ta.EMA(df['Close'], timeperiod=50)
    # Define the EMA periods
    ema_periods = [5, 13, 26, 50]
    # Check for crossover and crossunder points for each row
    df['has_cross'] = has_cross(df['Close'], ema_periods)

    return df


def main():
    _emas = multi_emas()
    _macd = macd()
    _super_trend = super_trend()
    # print(_emas.columns)
    # print(_macd.columns)
    # print(_super_trend.columns)
    # df_ema_macd = pd.merge(_emas, _macd, how='outer', left_index=True, right_index=True)
    # df = pd.merge(df_ema_macd, _super_trend, how='outer', left_index=True, right_index=True)
    # df = pd.concat([_super_trend, _macd, _emas])
    df = pd.merge(
        _emas,  # Your first df
        _super_trend,  # Second df
        how="left",
    )
    # print(df.columns)
    # print(_emas.tail(3))
    # print(_super_trend[['Datetime', 'TR', 'ATR_10', 'ST_10_1.5', 'STX_10_1.5']].tail(3))
    # print(_macd[['Datetime', 'macd_12_26_9', 'signal_12_26_9', 'hist_12_26_9']].tail(3))
    # print(df.tail(3))
    print(df.tail(30))

    # df = pd.DataFrame()
    # df['Signal'] = np.where((_super_trend['STX_10_1.5']=='up') &
    #                         (_macd['macd_12_26_9'] > _macd['signal_12_26_9']) &
    #                         (_emas['has_cross']==1)
    #                         , 'Buy', "Sell")
    return df
    # print(_super_trend.tail())

    # if _emas['has_cross'].all() and _super_trend['STX_10_1.5'].all == :
    #     print("Buy")
    # elif _emas['has_cross'].all():
    #     print("Sell")
    # else:
    #     print("DO NOTHING")


if __name__ == "__main__":
    main()
