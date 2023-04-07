#setup
from optibook.synchronous_client import Exchange

import time
import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

exchange = Exchange()
_ = exchange.connect()

stock_a_id = 'PHILIPS_A'
stock_b_id = 'PHILIPS_B'

def buy_a():
    ask_price_a = exchange.get_last_price_book(stock_a_id).asks[0].price
    bid_price_b = exchange.get_last_price_book(stock_b_id).bids[0].price
    ask_volume_a = exchange.get_last_price_book(stock_a_id).asks[0].volume
    bid_volume_b = exchange.get_last_price_book(stock_b_id).bids[0].volume
    
    if ask_price_a < bid_price_b:
        ## buy A, sell B
        min_vol = min(bid_volume_b, ask_volume_a, 20)
        exchange.insert_order(stock_a_id, price=bid_price_b, volume=min_vol, side='ask', order_type='ioc')
        exchange.insert_order(stock_b_id, price=ask_price_a, volume=min_vol, side='bid', order_type='ioc')
        
def sell_a():
    ask_price_b = exchange.get_last_price_book(stock_b_id).asks[0].price
    bid_price_a = exchange.get_last_price_book(stock_a_id).bids[0].price
    bid_volume_a = exchange.get_last_price_book(stock_a_id).bids[0].volume
    ask_volume_b = exchange.get_last_price_book(stock_b_id).asks[0].volume
    
    if ask_price_b < bid_price_a:
        ## sell A, buy B
        min_vol = min(bid_volume_a, ask_volume_b, 20)
        exchange.insert_order(stock_a_id, price=bid_price_a, volume=min_vol, side='ask', order_type='ioc')
        exchange.insert_order(stock_b_id, price=ask_price_b, volume=min_vol, side='bid', order_type='ioc')
        
while True:
    if exchange.get_positions()[stock_a_id] > 100:
        sell_a()
    elif exchange.get_positions()[stock_a_id] < -100:
        buy_a()
    else:
        sell_a()
        buy_a()
        sell_a()
        buy_a()
