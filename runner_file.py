import request_data as rd 
import buy_sell_signals as bs 
import Alpaca_trades as at 
import time 
import schedule

def run_task():
    
    data = rd.Obtain_Data('SP500.csv')
    data.ticker_list()
    
    signals = bs.Signals('SP500.csv')
    signals.place_order()






def main():
    run_task()
    
    schedule.every().day.at("15:30").do(run_task)

    while True:
        schedule.run_pending()
        time.sleep(1000)
    
main()