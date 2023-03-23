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
        if order_side == 'buy':
            self.entry_transaction_type = self.xt.TRANSACTION_TYPE_BUY
        else:
            self.entry_transaction_type = self.xt.TRANSACTION_TYPE_SELL

    def place_order_if_not_exists(self):
        entry_response = []
        positions = self.get_position_(param=1)
        running_position = positions.loc[
            (pd.to_numeric(positions['ExchangeInstrumentId']) == int(self.scrip_code)) &
            (pd.to_numeric(positions['Quantity']) != 0)
            ]
        if not running_position.empty:
            print(
                f"Position exists for {self.scrip_code} with "
                f"quantity {running_position['Quantity'].iloc[0]}. Order will not be placed.")
        else:
            print(f"No position exists for {self.scrip_code}. Initiating order.")
            # entry_response = self.entry(entry_transaction_type=self.entry_transaction_type)

        return entry_response

