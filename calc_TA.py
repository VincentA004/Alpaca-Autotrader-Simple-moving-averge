import pandas as pd 
import talib as ta


class calc_TA_data:

    def __init__(self, type1):
        self.type = type1

    def gen_ta(self, paired_stock):

       
        sma200 = ta.SMA(paired_stock['Close'], timeperiod = 200)
        
        stock = {
                "Close": paired_stock['Close'], "SMA200":sma200}

        full_stock_data = pd.DataFrame(stock)

        return full_stock_data