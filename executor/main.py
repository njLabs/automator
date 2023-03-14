import time
from strategy import bb
from brokers.XTS.xts_pythonclient_api_sdk import x_executor

while True:
    scrips = {55582: "N17000PE", 55575: "N16900PE", 55568: "N16800PE", 55589: "N17100PE",
              55614: "N17600CE", 55610: "N17500CE", 55606: "N17400CE", 55598: "N17300CE"}
    tf = '1'
    status, data = bb(scrips=scrips, tf=tf)
    if status:
        # _df = data.loc[(data['signal'] == True) | (data['signal'] == False)]
        _df = data
        for index, item in _df.iterrows():
            if item['signal'] is True:
                response = x_executor.place_order_(
                    exchange_segment=x_executor.EXCHANGE_NSEFO,
                    exchange_instrument_id=item['scrip_code'],
                    limit_price=item['Open'],
                    order_quantity=50,
                    product_type=x_executor.PRODUCT_NRML,
                    order_type=x_executor.ORDER_TYPE_LIMIT,
                    order_side=x_executor.TRANSACTION_TYPE_BUY,
                    time_in_force=x_executor.VALIDITY_DAY,
                    disclosed_quantity=0,
                    stop_price=0,
                )
                print("True", item['scrip_value'], response)
            elif item['signal'] is False:
                response = x_executor.place_order_(
                    exchange_segment=x_executor.EXCHANGE_NSEFO,
                    exchange_instrument_id=item['scrip_code'],
                    limit_price=item['Open'],
                    order_quantity=50,
                    product_type=x_executor.PRODUCT_NRML,
                    order_type=x_executor.ORDER_TYPE_LIMIT,
                    order_side=x_executor.TRANSACTION_TYPE_SELL,
                    time_in_force=x_executor.VALIDITY_DAY
                )
                print("False", item['scrip_value'], response)

            else:
                print("NaN", item['scrip_value'])

    else:
        print(data)
    time.sleep(int(tf) * 60)
