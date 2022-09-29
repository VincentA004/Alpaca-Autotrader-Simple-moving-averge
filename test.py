import Alpaca_trades as at 

inst = at.Place_Orders([0], [0])

inst.get_account_info()
inst.get_open_positions()