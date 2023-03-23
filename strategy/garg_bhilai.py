from datetime import datetime, timedelta
import talib as ta
import pandas as pd
import numpy as np
from indicators import (
    SuperTrend,
    MACD,
    has_cross,
)
from historical_data import client

end_ = datetime.now().date()
start_ = end_ - timedelta(days=5)


def super_trend(tf=15, scrip_code=1660):
    df = client.historical_data('N', 'D', scrip_code, f'{tf}m', start_, end_)
    df = SuperTrend(df, 10, 1.5)
    return df


def macd(tf=30, scrip_code=1660):
    historical_data = client.historical_data('N', 'D', scrip_code, f'{tf}m', start_, end_)
    df = MACD(historical_data)
    df['macd_cross'] = np.where(df['macd_12_26_9'] > df['signal_12_26_9'], 'up', 'down')
    return df


def multi_emas(tf=5, scrip_code=1660):
    df = client.historical_data('N', 'D', scrip_code, f'{tf}m', start_, end_)
    df['ema_5'] = ta.EMA(df['Close'], timeperiod=5)
    df['ema_13'] = ta.EMA(df['Close'], timeperiod=13)
    df['ema_26'] = ta.EMA(df['Close'], timeperiod=26)
    df['ema_50'] = ta.EMA(df['Close'], timeperiod=50)
    df['ema_crossover'] = np.where((df['ema_5'] > df['ema_13']) &
                                   (df['ema_13'] > df['ema_26']) &
                                   (df['ema_26'] > df['ema_50']), 'up', '')
    df['ema_crossunder'] = np.where((df['ema_50'] > df['ema_26']) &
                                    (df['ema_26'] > df['ema_13']) &
                                    (df['ema_13'] > df['ema_5'])
                                    , 'down', '')
    df['has_cross'] = df['ema_crossover'] + df['ema_crossunder']
    df.drop(['ema_crossover', 'ema_crossunder'], axis=1, inplace=True)
    # print(df.tail(300))
    return df


def main():
    scrip_code = 41884
    _emas = multi_emas(scrip_code=scrip_code)
    _macd = macd(scrip_code=scrip_code)
    _super_trend = super_trend(scrip_code=scrip_code)
    ema5_super15_df = pd.merge(_emas, _super_trend[['Datetime', 'TR', 'ATR_10', 'ST_10_1.5', 'STX_10_1.5']],
                               on="Datetime", how="left", ).fillna(method='ffill')
    df = pd.merge(ema5_super15_df, _macd[
        ['Datetime', 'ema_12', 'ema_26', 'macd_12_26_9', 'signal_12_26_9', 'hist_12_26_9', 'macd_cross']],
                  on="Datetime", how="left", ).fillna(method='ffill')
    df['buy_signal'] = np.where((df['STX_10_1.5'] == 'up') &
                            (df['macd_cross'] == 'up') &
                            (df['has_cross'] == 'up'), 'Buy', '')

    df['sell_signal'] = np.where((df['STX_10_1.5'] == 'down') &
                            (df['macd_cross'] == 'down') &
                            (df['has_cross'] == 'down'), 'Sell', '')
    df['signal'] = df['buy_signal'] + df['sell_signal']
    df.drop(['buy_signal', 'sell_signal'], axis=1, inplace=True)
    df.to_csv(f"generated_results_{start_}_{end_}.csv")
    return df[['Datetime', 'Open', 'High', 'Low', 'Close', 'has_cross', 'STX_10_1.5', 'macd_cross', 'signal']]


if __name__ == "__main__":
    print(main().tail(300))
