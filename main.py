# response = x_executor.place_order_bracket_(
#                     exchange_segment=x_executor.EXCHANGE_NSEFO,
#                     exchange_instrument_id=item['scrip_code'],
#                     limit_price=item['Open'],
#                     stop_loss_price=item['sl'],
#                     square_off=item['tp'],
#                     trailing_stop_loss=0,
#                     order_quantity=50,
#                     order_type=x_executor.ORDER_TYPE_LIMIT,
#                     order_side=x_executor.TRANSACTION_TYPE_SELL,
#                 )