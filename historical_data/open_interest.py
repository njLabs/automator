# 3rd party imports
import talib
import pandas as pd
import matplotlib.pyplot as plt

#
from historical_data import client as paisa_5_client
from common import nearest_round

# pandas set options for full length view
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class OpenInterest:
    def __init__(self):
        self.client = paisa_5_client


    def rounded_LTP(self, expiry_data):
        self.LTP = expiry_data['lastrate'][0].get('LTP')
        self.rounded_ltp = nearest_round(self.LTP)
        return self

    def timestamp_to_int(self, timestamp):
        return timestamp.split('(')[1].split('+')[0]

    def get_expiry(self, is_stock: bool = True, is_monthly: bool = True, symbol='infy', index=0):
        # if is_monthly or is_stock:
        #     index = -1
        # else:
        #     index = index
        self.expiry_dates_obj = self.client.get_expiry("N", symbol=symbol.upper())
        self.rounded_ltp = self.rounded_LTP(self.expiry_dates_obj).rounded_ltp
        self.expiry_dates = self.expiry_dates_obj.get('Expiry')
        self.expiry = self.expiry_dates[index].get('ExpiryDate')
        self.expiry_int = self.timestamp_to_int(self.expiry)
        return self

    def get_option_chain(self, expiry=None, exchange="N", symbol="infy", index=0, strike_rate: int = None):
        if not expiry or not index:
            print(index)
            expiry = self.get_expiry(symbol=symbol, index=index).expiry_int
        self.oi = self.client.get_option_chain(exchange, symbol.upper(), expiry)
        self.option_chain = pd.DataFrame(self.oi.get('Options'))
        if strike_rate:
            self.option_chain = self.option_chain[self.option_chain['StrikeRate'] == strike_rate]
        return self

    def get_strike(self, rounded_ltp: int = None, symbol="infy", expiry=None):
        if not expiry:
            expiry = self.get_expiry().expiry_int
        if not rounded_ltp:
            rounded_ltp = self.get_expiry(symbol=symbol).rounded_ltp
        option_chain = self.get_option_chain(symbol=symbol.upper(), expiry=expiry).option_chain
        option_chain = option_chain[(option_chain['LastRate'] > 0)]
        self.itm_calls = option_chain[(option_chain['StrikeRate'] < rounded_ltp) & (option_chain['CPType'] == 'CE')][
            'StrikeRate']
        self.itm_puts = option_chain[(option_chain['StrikeRate'] > rounded_ltp) & (option_chain['CPType'] == 'PE')][
            'StrikeRate']
        return self

    def get_itm_volume(self, rounded_ltp: int = None, symbol="NIFTY", expiry=None, CPType='CE', min_vol=0,
                       max_vol=100000000000):
        if not expiry:
            expiry = self.get_expiry().expiry_int
        if not rounded_ltp:
            rounded_ltp = self.get_expiry(symbol=symbol).rounded_ltp
        print(rounded_ltp, expiry)
        option_chain = self.get_option_chain(symbol=symbol, expiry=expiry).option_chain
        if CPType == 'CE':
            self.itm_calls = option_chain[
                (option_chain['StrikeRate'] < rounded_ltp) & (option_chain['CPType'] == CPType) & (
                        option_chain['Volume'] > min_vol) & (option_chain['Volume'] < max_vol)]
        else:
            # print(option_chain)
            # print(rounded_ltp, symbol)
            # self.itm_puts = option_chain[(option_chain['StrikeRate'] > rounded_ltp) & (option_chain['CPType'] == CPType) & (option_chain['Volume'] > min_vol) & (option_chain['Volume'] < max_vol)]
            self.itm_puts = option_chain[
                (option_chain['StrikeRate'] > rounded_ltp) & (option_chain['CPType'] == CPType)]

        # atm_strikes = option_chain[option_chain['StrikeRate'] == rounded_ltp]
        # atm_index = atm_strikes.index

        return self

    def generate_csv(self, rounded_ltp: int = None, symbol="NIFTY", expiry=None):
        get_itm = self.get_strike(symbol=symbol)
        self.itm_ce = get_itm.itm_calls
        self.itm_pe = get_itm.itm_puts
        last_rate = obj.LTP
        df = pd.concat([self.itm_ce, self.itm_pe]).reset_index()
        df.insert(2, "spot", last_rate)
        df.insert(3, "diff", (df['StrikeRate'] - df['spot']) / last_rate * 100)
        self.df = df.drop(['index'], axis=1)
        return self

    def get_future_price(self, scrip_code: int = 55270):
        self.df = df[(df['ExchType'] == 'D') & (df['CpType'] == 'XX') & (df['Root'] == 'RELIANCE') & (df['QtyLimit'] > 0)]
        print(self.df)
        print(self.client)
        self.future_data = self.client.historical_data('N', 'D', scrip_code, '1m', '2022-12-13', '2022-12-13')
        return self


obj = paisa_5_client

# print(obj.generate_csv(symbol='infy').df)
# option_chain = obj.get_option_chain(symbol='banknifty', strike_rate=44000)
# print(option_chain.option_chain)

# print(obj.get_future_price().df)
# data = obj.get_option_chain(symbol='nifty').oi['Options']
# data = pd.DataFrame(data)
# ltp = (data['LastRate'])
# print(data.tail())

# print(type(ltp.values), ltp.values)
# print(talib.RSI(ltp.values))
# print(data['LastRate'].values)
# exit()
data = obj.get_future_price().future_data
print(data, type(data))
data['upperband'], data['middleband'], data['lowerband'] = talib.BBANDS(data['LastRate'].values, timeperiod=14, nbdevup=2, nbdevdn=2, matype=0)
data[['LastRate', 'upperband', 'middleband', 'lowerband']].plot(figsize=(10, 7))
plt.legend()

# Define the label for the title of the figure
plt.title("Adjusted Close Price", fontsize=16)

# Define the labels for x-axis and y-axis
plt.ylabel('Price', fontsize=14)
plt.xlabel('Year', fontsize=14)

# Plot the grid lines
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
plt.show()