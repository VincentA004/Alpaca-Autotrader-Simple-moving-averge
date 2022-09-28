import requests
import pandas as pd 
import time
import calc_TA as t
import csv



BASE_URL = 'https://www.alphavantage.co/query?'
API_KEY = 'CVXYL4XHJEIGFCTC'

class Obtain_Data:

    def __init__(self, file):
        self.csv_file = file
        self.ta = t.calc_TA_data('1')
        self.full_data_file = pd.HDFStore(f'SP500_full_data.h5')
        self.temp_data = pd.HDFStore('temp.h5')
        
    
    def get_ticker_data(self, ticker):
        try:
            param = {'function' : 'TIME_SERIES_DAILY_ADJUSTED', 'symbol' : 'AAPL' , 'outputsize': 'full', 'datatype': 'json', 'apikey': API_KEY}
            r = requests.get(BASE_URL, params = param)
        
            response_dict = r.json()
           
            fin_data = pd.DataFrame(response_dict["Time Series (Daily)"]).T.iloc[::-1].rename(columns = {'1. open': 'Open', '2. high': 'High', '3. low':'Low', '4. close': "Close", '6. volume': "Volume"}).drop(columns = ['5. adjusted close', '7. dividend amount', '8. split coefficient'])
            
            self.temp_data.put(ticker, fin_data, format = 'Table')
            
        except:
            print(f"The following {ticker} was not found.")


    def store_ticker_data(self, ticker):
        full_stock_data = self.ta.gen_ta(self.temp_data.get(ticker))

        self.full_data_file.put(f"{ticker}", full_stock_data, format = "Table")

      
    def ticker_list(self):
        open_file = open(self.csv_file,'r')
        csv_file = csv.reader(open_file, delimiter = ',')

        #self.index_name = next(csv_file)[0]
        
        ticker_list = list(csv_file)

        for count, ticker in enumerate(ticker_list):
            try:
                self.get_ticker_data(ticker[0])
                self.store_ticker_data(ticker[0])
                print(f"{count}. {ticker[0]} was added and cleaned.")
            except:
                print(f'The {ticker[0]} could not be added/cleaned to the file')


    
    



