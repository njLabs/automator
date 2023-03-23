import time
import threading
from strategy import bb
# from order_management_xts import OrderInitiator
from xts_order_management import OrderInitiator

while True:
    # threading.Thread(target=OrderCloser().order_checker).start()
    # scrips = {55556: "N16500PE", 55560: "N16600PE", 55564: "N16700PE",
    #           55614: "N17600CE", 55610: "N17500CE", 55618: "N17700CE", 55598: "N17300CE"}
    # scrips = {41841: "41841", 41847: "41847", 41856: "41856",
    #           41861: "41861", 41866: "41866", 41908: "41908", 41904: "41904", 41898: "41898", 41891: "41891",
    #           41884: "41884", 41878:"41878"}
    scrips = {41891: "41891", 41879: "41879", }
    tf = '1'
    status, data = bb(scrips=scrips, tf=tf)
    if status:
        _df = data
        for index, item in _df.iterrows():
            if item['signal'] is True:
                response = OrderInitiator(item, order_side='buy').place_order_if_not_exists()
                print(item['signal'], item['scrip_value'], response)
            elif item['signal'] is False:
                response = OrderInitiator(item, order_side='sell').place_order_if_not_exists()
                print(item['signal'], item['scrip_value'], response)
            else:
                OrderInitiator(item, order_side='buy').place_order_if_not_exists()
                print(item['signal'], item['scrip_value'])
            print("----------")
        print("#############################################")

    else:
        print(data)
    time.sleep(int(tf) * 10)
