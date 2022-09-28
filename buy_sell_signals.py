import pandas as pd 
import csv
import math
import requests
import Alpaca_trades as at

class Signals:
    def __init__(self, file):
        self.file = file
        self.buy_signal, self.sell_signal = self.gen_signals()
        self.trade = at.Place_Orders(self.buy_signal, self.sell_signal)
        

    def gen_signals(self):
        open_file = open(self.file,'r')
        csv_file = csv.reader(open_file, delimiter = ',')
        ticker_list = list(csv_file)

        full_df = pd.HDFStore('SP500_full_data.h5')

        buy_signal = {}
        sell_signal = []

        for ticker in ticker_list:
            ticker_data = full_df.get(ticker[0])
            ticker_data = ticker_data.astype('float64')
            ticker_data = ticker_data.dropna()


            dates = list(ticker_data.index)[-2:]

            if ticker_data.loc[dates[1], 'SMA200'] > ticker_data.loc[dates[1],'Close'] and ticker_data.loc[dates[0], 'SMA200'] < ticker_data.loc[dates[0],'Close']:
                buy_signal[ticker[0]] = {'Close': ticker_data.loc[dates[1],'Close'], 'Qty': math.floor(2000/ticker_data.loc[dates[1],'Close']) }
            elif ticker_data.loc[dates[1], 'SMA200'] < ticker_data.loc[dates[1],'Close'] and ticker_data.loc[dates[0], 'SMA200'] > ticker_data.loc[dates[0],'Close']:
                sell_signal.append(ticker[0])
        print(buy_signal)
        print(sell_signal)
        return buy_signal, sell_signal

    def place_order(self):
        self.trade.place_orders()


