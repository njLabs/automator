from brokers.XTS import Orders
from common import nearest_round_decimal
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class OrderInitiator(Orders):
    def __init__(self, df, order_side="buy"):
        super().__init__(df, order_side=order_side)
        self.df = df
        self.order_side = order_side
        self.close = df['Close']
        self.scrip_code = pd.to_numeric(self.df['scrip_code'])
        self.sl = round(df['sl'], 1)
        self.tp = round(df['tp'], 1)
        self.order_quantity = 50
        self.order_unique_identifier = "sukhw@l"

    def order_puncher(self):
        order_list = []
        try:
            positions = self.xt.get_position_(param=1)
            positions = positions['result']['positionList']
            entry_response = []
            for position in positions:
                exchange_instrument_id = pd.to_numeric(position['ExchangeInstrumentId']).values[0]
                abs_quantity = pd.to_numeric(position['Quantity']).values[0]
                print(abs_quantity, type(abs_quantity), "abs_quantity")
                if abs_quantity > 0 and exchange_instrument_id == self.scrip_code:
                    print("already a position: ", position['Quantity'], position['ExchangeInstrumentId'])
                    continue
                elif abs_quantity == 0 and exchange_instrument_id == self.scrip_code and self.order_side == 'buy':
                    entry_transaction_type = self.xt.TRANSACTION_TYPE_BUY
                    # entry_response = self.entry(entry_transaction_type)
                    print("order_puncher-Buy:- ", entry_response)
                    return entry_response
                elif abs_quantity == 0 and exchange_instrument_id == self.scrip_code and self.order_side == 'sell':
                    entry_transaction_type = self.xt.TRANSACTION_TYPE_SELL
                    # entry_response = self.entry(entry_transaction_type)
                    print("order_puncher-Sell:- ", entry_response)
                    return entry_response
                else:
                    print("NaN--------", self.df['scrip_code'])
            #
            # if self.order_side == 'buy':
            #     for position in positions:
            #         if position['Quantity'] and int(position['ExchangeInstrumentId']) == self.df['scrip_code']:
            #             print("already a position: ", position['Quantity'], position['ExchangeInstrumentId'])
            #             continue
            #         else:
            #             print("Buy")
            #             entry_transaction_type = x_executor.TRANSACTION_TYPE_BUY
            #             entry_response = self.entry(entry_transaction_type)
            #             return entry_response
            #
            # elif self.order_side == 'sell':
            #     for position in positions:
            #         if position['Quantity'] and int(position['ExchangeInstrumentId']) == self.df['scrip_code']:
            #             print("already a position: ", position['Quantity'], position['ExchangeInstrumentId'])
            #             continue
            #         else:
            #             print("Sell")
            #             entry_transaction_type = x_executor.TRANSACTION_TYPE_SELL
            #             entry_response = self.entry(entry_transaction_type)
            #             return entry_response
        except Exception as err:
            print(str(err))
            # if self.order_side == 'buy':
            #     entry_transaction_type = self.xt.TRANSACTION_TYPE_BUY
            #     entry_response = self.entry(entry_transaction_type)
            #     print("order_puncher-Buy: ", entry_response)
            # elif self.order_side == 'sell':
            #     entry_transaction_type = self.xt.TRANSACTION_TYPE_SELL
            #     entry_response = self.entry(entry_transaction_type)
            #     print("order_puncher-Sell: ", entry_response)
            # else:
            #     print("check error")
            #     entry_response = str(err)
            # order_list.append(entry_response)
            # return entry_response
        return order_list

    def order_checker(self):
        try:
            trade_book = self.trade_book_()
            positions = self.get_position_()
            positions_trade_book = pd.merge(trade_book, positions, on='TradingSymbol')
            positions_trade_book = positions_trade_book[
                ['ExchangeTransactTime', 'TradingSymbol', 'AppOrderID', 'Quantity',
                 'OrderStatus', 'OrderSide', 'OrderType', 'OrderAverageTradedPrice',
                 'LastTradedPrice', 'ExchangeInstrumentId']].sort_values(by=['AppOrderID'])
            """instruments list"""
            # exchange_instrument_id = positions.loc[pd.to_numeric(positions['Quantity']) > 0]  # ExchangeInstrumentId
            unique_instrument_ids = trade_book.ExchangeInstrumentID.unique()
            for instrument_id in unique_instrument_ids:
                instrument_df = trade_book.loc[trade_book['ExchangeInstrumentID'] == instrument_id]
                buy_quantity = instrument_df[instrument_df['OrderSide'] == 'BUY']['OrderQuantity'].sum()
                sell_quantity = instrument_df[instrument_df['OrderSide'] == 'SELL']['OrderQuantity'].sum()
                if buy_quantity == sell_quantity:
                    print(f"All squared off for instrument_id: {instrument_id}.")
                    continue
                else:
                    print(f"running position for instrument_id: {instrument_id}.")

                    running_position = positions.loc[pd.to_numeric(positions['ExchangeInstrumentId']) == int(instrument_id)]
                    if running_position['BuyAveragePrice'].empty:
                        average_price = pd.to_numeric(running_position['BuyAveragePrice'])
                        target_price = nearest_round_decimal((average_price + (average_price * 0.25 / 100)), 0.05)
                        stop_loss = nearest_round_decimal((average_price - (average_price * 0.2 / 100)), 0.05)
                        print("Buy: ", target_price.values, stop_loss.values, instrument_id)
                    else:
                        average_price = pd.to_numeric(running_position['SellAveragePrice'])
                        target_price = nearest_round_decimal((average_price + (average_price * 0.25 / 100)), 0.05)
                        stop_loss = nearest_round_decimal((average_price - (average_price * 0.2 / 100)), 0.05)
                        print("Sell: ", target_price.values, stop_loss.values, instrument_id)
                    # print(target_price.values, stop_loss.values, )
                    target_position = running_position.loc[
                        (int(running_position['ExchangeInstrumentId']) == int(instrument_id)) &
                        (pd.to_numeric(running_position['Quantity']) > 0) &
                        (pd.to_numeric(running_position['BuyAveragePrice']) >= target_price)]
                    stop_loss_position = running_position.loc[
                        (int(running_position['ExchangeInstrumentId']) == int(instrument_id)) &
                        (pd.to_numeric(running_position['Quantity']) > 0) &
                        (pd.to_numeric(running_position['BuyAveragePrice']) <= stop_loss)]
                    print(running_position)
                    # print(target_position)
                    # print(stop_loss_position)

                    if target_price.empty:
                        print("target_position: ")
                        print(target_position)

                    elif stop_loss.empty:
                        print("stop_loss_position: ")
                        print(stop_loss_position)
                    else:
                        print("still running")
        except Exception as err:
            print("no running trade || Haven't initiated a trade yet.")
        return


# class OrderChecker(OrderInitiator):
#     def __init__(self, df, order_side='buy'):
#         super().__init__(df, order_side)
#
#     def trade_book(self):
#         trade_book = []
#         try:
#             trade_book = self.xt.get_trade(clientID=self.xt.CLIENT_ID)
#             trade_book = pd.DataFrame(trade_book['result']).sort_values(by='AppOrderID', ascending=False)
#             trade_book = trade_book.loc[trade_book['OrderStatus'] == 'Filled']
#         except KeyError as err:
#             print("trade_book-error: ", str(err))
#         return trade_book
#
#     def all_positions(self):
#         positions = self.xt.get_position_daywise(self.xt.CLIENT_ID)
#         positions = pd.DataFrame(positions['result']['positionList'])
#         return positions
#
#     def order_book(self):
#         order_book = self.xt.get_order_book(self.xt.CLIENT_ID)
#         order_book = pd.DataFrame(order_book['result'])
#         return order_book
#
#     def order_checker(self):
#         print("here---------------------")
#
#         try:
#             print("trade_book", self.trade_book())
#             trade_book = self.trade_book()
#             positions = self.all_positions()
#             positions_trade_book = pd.merge(trade_book, positions, on='TradingSymbol')
#             positions_trade_book = positions_trade_book[
#                 ['ExchangeTransactTime', 'TradingSymbol', 'AppOrderID', 'Quantity', 'OrderStatus', 'OrderSide',
#                  'OrderType', 'OrderAverageTradedPrice', 'LastTradedPrice', 'ExchangeInstrumentId']].sort_values(
#                 by=['AppOrderID'])
#             """instruments list"""
#             exchange_instrument_id = positions.loc[pd.to_numeric(positions['Quantity']) > 0]  # ExchangeInstrumentId
#             unique_instrument_ids = trade_book.ExchangeInstrumentID.unique()
#             # print(unique_instrument_ids)
#             instrument_id = unique_instrument_ids[0]
#
#             instrument_df = trade_book.loc[trade_book['ExchangeInstrumentID'] == instrument_id]
#             buy_quantity = instrument_df[instrument_df['OrderSide'] == 'BUY']['OrderQuantity'].sum()
#             sell_quantity = instrument_df[instrument_df['OrderSide'] == 'SELL']['OrderQuantity'].sum()
#
#             if buy_quantity == sell_quantity:
#                 print(f"All squared off for {instrument_id}.")
#             else:
#                 running_position = positions.loc[pd.to_numeric(positions['ExchangeInstrumentId']) == int(instrument_id)]
#                 if running_position['BuyAveragePrice'].empty:
#                     average_price = pd.to_numeric(running_position['BuyAveragePrice'])
#                     target_price = nearest_round_decimal((average_price + (average_price * 0.25 / 100)), 0.05)
#                     stop_loss = nearest_round_decimal((average_price - (average_price * 0.2 / 100)), 0.05)
#                     print("Buy: ", target_price.values, stop_loss.values, instrument_id)
#                 else:
#                     average_price = pd.to_numeric(running_position['SellAveragePrice'])
#                     target_price = nearest_round_decimal((average_price + (average_price * 0.25 / 100)), 0.05)
#                     stop_loss = nearest_round_decimal((average_price - (average_price * 0.2 / 100)), 0.05)
#                     print("Sell: ", target_price.values, stop_loss.values, instrument_id)
#                 # print(target_price.values, stop_loss.values, )
#                 target_position = running_position.loc[
#                     (int(running_position['ExchangeInstrumentId']) == int(instrument_id)) &
#                     (pd.to_numeric(running_position['Quantity']) > 0) &
#                     (pd.to_numeric(running_position['BuyAveragePrice']) >= target_price)]
#                 stop_loss_position = running_position.loc[
#                     (int(running_position['ExchangeInstrumentId']) == int(instrument_id)) &
#                     (pd.to_numeric(running_position['Quantity']) > 0) &
#                     (pd.to_numeric(running_position['BuyAveragePrice']) <= stop_loss)]
#                 print(running_position)
#                 # print(target_position)
#                 # print(stop_loss_position)
#
#                 if target_price.empty:
#                     print("target_position: ")
#                     print(target_position)
#
#                 elif stop_loss.empty:
#                     print("stop_loss_position: ")
#                     print(stop_loss_position)
#                 else:
#                     print("still running")
#         except Exception as err:
#             print("no running trade or Haven't initiated a trade yet.", str(err))
#         return
# print(OrderChecker().order_checker())

#
# class OrderCloser(OrderInitiator):
#     def __init__(self):
#         self.ORDER_UNIQUE_IDENTIFIER = "sukh"
#         ################ XTS creds #####################
#         self.BASE_URL = "http://sapi2.shareindia.com:3003/"
#         self.INTERACTIVE_URL = f"{self.BASE_URL}/interactive"
#         self.MARKET_URL = f"{self.BASE_URL}/marketdata"
#         self.USER_ID = "CXTS14"
#         self.CLIENT_ID = "VCXTS14"
#         self.SOURCE = "WEBAPI"
#         ## Market data key and secret key
#         # self.API_KEY = "9e9d6763d833f7b59af795"
#         # self.API_SECRET = "Umwk805@qU"
#         ## Interactive data key and secret key
#         self.API_KEY = "3e220f0baa5308670a3426"
#         self.API_SECRET = "Pocp773#2q"
#         super().__init__(self.API_KEY, self.API_SECRET, self.SOURCE)
#         self.xt = XTSConnect(self.API_KEY, self.API_SECRET, self.SOURCE, root=self.BASE_URL)
#         login_response = self.xt.interactive_login()
#         # print("Logged In: ", login_response)
#
#     def compute_sl(self, df):
#         self.df = df
#         self.df['sl'] = self.df['Open'] - (self.df['Open'] * 0.1 / 100)
#         return self
#
#     def compute_tps(self, df):
#         self.df = df
#         # self.df['tp'] = self.df['Open'] + self.df['Open'] * 0.15 / 100
#         tp = round(
#             (pd.to_numeric(self.df['BuyAveragePrice']) + (pd.to_numeric(self.df['BuyAveragePrice']) * 0.15 / 100)), 2)
#         self.df['tp'] = tp
#         # print(tp, "tp", self.df)
#         return self
#
#     def get_ltp(self, exchangeInstrumentID):
#         instruments = [{'exchangeSegment': 2, 'exchangeInstrumentID': exchangeInstrumentID}]
#         response = self.xt.get_quote(
#             Instruments=instruments,
#             xtsMessageCode=1501,
#             publishFormat='JSON')
#
#         data = json.loads(response['result']['listQuotes'][0])
#         ltp = data['Touchline']['LastTradedPrice']
#         return ltp
#
#     def trade_book(self):
#         trade_book = []
#         try:
#             trade_book = self.xt.get_trade(clientID=self.CLIENT_ID)
#             trade_book = pd.DataFrame(trade_book['result']).sort_values(by='AppOrderID', ascending=False)
#             trade_book = trade_book.loc[trade_book['OrderStatus'] == 'Filled']
#         except KeyError as err:
#             print("trade_book-error: ", str(err))
#         return trade_book
#
#     def all_positions(self):
#         positions = self.xt.get_position_daywise(self.CLIENT_ID)
#         positions = pd.DataFrame(positions['result']['positionList'])
#         return positions
#
#     def order_book(self):
#         order_book = self.xt.get_order_book(self.CLIENT_ID)
#         order_book = pd.DataFrame(order_book['result'])
#         return order_book
#
#     def order_checker(self):
#         try:
#             trade_book = self.trade_book()
#             positions = self.all_positions()
#             positions_trade_book = pd.merge(trade_book, positions, on='TradingSymbol')
#             positions_trade_book = positions_trade_book[
#                 ['ExchangeTransactTime', 'TradingSymbol', 'AppOrderID', 'Quantity', 'OrderStatus', 'OrderSide',
#                  'OrderType', 'OrderAverageTradedPrice', 'LastTradedPrice', 'ExchangeInstrumentId']].sort_values(
#                 by=['AppOrderID'])
#             """instruments list"""
#             exchange_instrument_id = positions.loc[pd.to_numeric(positions['Quantity']) > 0]  # ExchangeInstrumentId
#             unique_instrument_ids = trade_book.ExchangeInstrumentID.unique()
#             # print(unique_instrument_ids)
#             instrument_id = unique_instrument_ids[0]
#
#             instrument_df = trade_book.loc[trade_book['ExchangeInstrumentID'] == instrument_id]
#             buy_quantity = instrument_df[instrument_df['OrderSide'] == 'BUY']['OrderQuantity'].sum()
#             sell_quantity = instrument_df[instrument_df['OrderSide'] == 'SELL']['OrderQuantity'].sum()
#
#             if buy_quantity == sell_quantity:
#                 print(f"All squared off for {instrument_id}.")
#             else:
#                 running_position = positions.loc[pd.to_numeric(positions['ExchangeInstrumentId']) == int(instrument_id)]
#                 """
#                     ['AccountID', 'TradingSymbol', 'ExchangeSegment', 'ExchangeInstrumentId',
#                    'ProductType', 'Marketlot', 'Multiplier', 'BuyAveragePrice',
#                    'SellAveragePrice', 'OpenBuyQuantity', 'OpenSellQuantity', 'Quantity',
#                    'BuyAmount', 'SellAmount', 'NetAmount', 'UnrealizedMTM', 'RealizedMTM',
#                    'MTM', 'BEP', 'SumOfTradedQuantityAndPriceBuy',
#                    'SumOfTradedQuantityAndPriceSell', 'StatisticsLevel',
#                    'IsInterOpPosition', 'childPositions', 'MessageCode', 'MessageVersion',
#                    'TokenID', 'ApplicationType', 'SequenceNumber']
#                 """
#                 if running_position['BuyAveragePrice'].empty:
#                     average_price = pd.to_numeric(running_position['BuyAveragePrice'])
#                     target_price = nearest_round_decimal((average_price + (average_price * 0.25 / 100)), 0.05)
#                     stop_loss = nearest_round_decimal((average_price - (average_price * 0.2 / 100)), 0.05)
#                     print("Buy: ", target_price.values, stop_loss.values, instrument_id)
#                 else:
#                     average_price = pd.to_numeric(running_position['SellAveragePrice'])
#                     target_price = nearest_round_decimal((average_price + (average_price * 0.25 / 100)), 0.05)
#                     stop_loss = nearest_round_decimal((average_price - (average_price * 0.2 / 100)), 0.05)
#                     print("Sell: ", target_price.values, stop_loss.values, instrument_id)
#                 # print(target_price.values, stop_loss.values, )
#                 target_position = running_position.loc[
#                     (int(running_position['ExchangeInstrumentId']) == int(instrument_id)) &
#                     (pd.to_numeric(running_position['Quantity']) > 0) &
#                     (pd.to_numeric(running_position['BuyAveragePrice']) >= target_price)]
#                 stop_loss_position = running_position.loc[
#                     (int(running_position['ExchangeInstrumentId']) == int(instrument_id)) &
#                     (pd.to_numeric(running_position['Quantity']) > 0) &
#                     (pd.to_numeric(running_position['BuyAveragePrice']) <= stop_loss)]
#                 print(running_position)
#                 # print(target_position)
#                 # print(stop_loss_position)
#
#                 if target_price.empty:
#                     print("target_position: ")
#                     print(target_position)
#
#                 elif stop_loss.empty:
#                     print("stop_loss_position: ")
#                     print(stop_loss_position)
#                 else:
#                     print("still running")
#         except Exception as err:
#             print("no running trade or Haven't initiated a trade yet.", str(err))
#         return

# while 1:
#     obj = OrderCloser().order_checker()
#
