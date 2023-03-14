from brokers.XTS.xts_pythonclient_api_sdk import x_executor


class SLTP_initiator:
    def __init__(self, df, order_initiated="buy"):
        self.df = df
        self.close = df['Close']
        self.sl = df['sl']
        self.tp = df['tp']
        if order_initiated == 'buy':
            self.sl_transaction_type = x_executor.TRANSACTION_TYPE_SELL
            self.tp_transaction_type = x_executor.TRANSACTION_TYPE_SELL
        else:
            self.sl_transaction_type = x_executor.TRANSACTION_TYPE_BUY
            self.tp_transaction_type = x_executor.TRANSACTION_TYPE_BUY

    def sl(self):
        response = x_executor.place_order_(
            exchange_segment=x_executor.EXCHANGE_NSEFO,
            exchange_instrument_id=self.df['scrip_code'],
            limit_price=self.sl,
            order_quantity=50,
            product_type=x_executor.PRODUCT_NRML,
            order_type=x_executor.ORDER_TYPE_LIMIT,
            order_side=self.sl_transaction_type,
            time_in_force=x_executor.IOC,
            disclosed_quantity=0,
            stop_price=0,
        )
        return response

    def tp(self):
        response = x_executor.place_order_(
            exchange_segment=x_executor.EXCHANGE_NSEFO,
            exchange_instrument_id=self.df['scrip_code'],
            limit_price=self.tp,
            order_quantity=50,
            product_type=x_executor.PRODUCT_NRML,
            order_type=x_executor.ORDER_TYPE_LIMIT,
            order_side=self.tp_transaction_type,
            time_in_force=x_executor.VALIDITY_DAY,
            disclosed_quantity=0,
            stop_price=0,
        )
        return response