from datetime import datetime
import pandas as pd
import numpy as np
import talib as ta
from historical_data import client

to_date = datetime.now().date().isoformat()


class ScannerBB:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.df['bb_high'], self.df['bb_mid'], self.df['bb_low'] = ta.BBANDS(self.df['Close'], timeperiod=20)

    def bb_scanner(self):
        # sl_value = candle_data['close'] + (atr_multiplier * candle_data['atr'])
        self.df['faker'] = (self.df['bb_low'] * 0.15 / 100)
        self.df['diff'] = (self.df['bb_low'] + self.df['faker']) > self.df.shift(2)['bb_low']
        self.df['higher'] = (self.df['High'] * 0.15 / 100) + self.df['bb_high']
        self.df['lower'] = self.df['bb_low'] - (self.df['Low'] * 0.15 / 100)
        self.df.loc[(self.df['High'] > self.df['higher'], '_higher')] = False
        self.df.loc[(self.df['Low'] < self.df['lower'], '_higher')] = True
        return

    def compute_sl(self):
        self.df['sl'] = self.df['Open'] - (self.df['Open'] * 0.1 / 100)
        return self

    def compute_tps(self):
        self.df['tp'] = self.df['Open'] + self.df['Open'] * 0.15 / 100
        return self

    def bb_signal(self):
        self.bb_scanner()
        self.df['signal'] = np.where((self.df['diff'] == self.df['_higher']), self.df['_higher'], np.nan)
        self.compute_sl()
        self.compute_tps()
        return self


def bb(scrips, tf='1'):
    bb_df = pd.DataFrame(columns=['Datetime', 'scrip_code', 'scrip_value', 'Open', 'High', 'Low', 'Close', 'signal', 'tp', 'sl'])
    try:
        for scrip_code, scrip_value in scrips.items():
            historical_of = {'Exch': 'N', 'ExchangeSegment': 'D', 'ScripCode': scrip_code, 'time': f'{tf}m',
                             'From': '2023-03-01',
                             'To': to_date}
            df = client.historical_data(**historical_of)
            df['scrip_value'] = scrip_value
            obj = ScannerBB(df).compute_tps()
            obj_df = obj.bb_signal().df
            obj_df['scrip_code'] = scrip_code
            result_df = obj_df[['Datetime', 'scrip_code', 'scrip_value', 'Open', 'High', 'Low', 'Close', 'signal', 'tp', 'sl']]
            # result_df = signals_df.loc[(signals_df['signal'] == True) | (signals_df['signal'] == False)]
            length = len(result_df)-1
            arr = result_df.iloc[length].values
            bb_df.loc[-1] = arr
            bb_df.reset_index(drop=True, inplace=True)
        return True, bb_df
    except Exception as err:
        return False, str(err)
