import pandas
import requests

class Place_Orders:

    def __init__(self, bs, ss):
        self.buy_signal = bs
        self.sell_signal = ss
        self.BASE_URL = 'https://paper-api.alpaca.markets{request}'
        self.Auth_Headers = {'APCA-API-KEY-ID': 'XXXXXXXXXXXX', 'APCA-API-SECRET-KEY': 'XXXXXXXXXXXXX'}
        
    def get_account_info(self):
        data = requests.get(self.BASE_URL.format(request = '/v2/account'), headers = self.Auth_Headers).json()
        self.Account_Balance = data['cash']
    
    def place_orders(self):
        for ticker in self.sell_signal:
            try:
                position_list = self.get_open_positions()

                if ticker in position_list.keys():
                    requests.post(self.BASE_URL.format(request = '/v2/orders'), params = {'symbol': ticker, 'qty': position_list[ticker], 'side': 'sell', 'type': 'market', 'time_in_force': 'day' } )
            except:
                print(f'The following stock {ticker} could not be sold. ')

        for ticker in self.buy_signal.keys():
            try:
                if self.buy_signal['Close'] * self.buy_signal['Qty'] < self.Account_Balance:
                    requests.post(self.BASE_URL.format(request = '/v2/orders'), params = {'symbol': ticker, 'qty': self.buy_signal[ticker]['Qty'], 'side': 'buy', 'type': 'market', 'time_in_force': 'day' } )
                else:
                    print(f'The following stock {ticker} could not be bought due to insufficient funds.')
            except:
                print(f'{ticker} could not be purchased')
        
        
    def get_open_positions(self):

        position_list = {}
        full_position = requests.get(self.BASE_URL.format(request = '/v2/positions'))

        for position in full_position:
            position_list[position['symbol']] = position['qty']
        
        return position_list