import stockretriever as st
import json
from datetime import datetime
from stock_symbols import dj_30

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

if __name__ == "__main__":
    resp = raw_input('today/historical?: ')
    if resp == 'today':
        path = raw_input('Path: ')
        out_path = path + "/stocks_" + str(datetime.now().strftime('%Y-%m-%d')) + ".txt"
        with open(out_path, 'w') as outfile:
            stock_info = st.get_current_info(dj_30)
            stock_data = {}
            for blob in range(len(stock_info)):
                stock_data[blob] = {"symbol":{},"time":{},"price":{}}
                stock_data[blob]["symbol"] = stock_info[blob]["Symbol"] 
                stock_data[blob]["time"] = datetime.strptime(stock_info[blob]["LastTradeDate"]+" "+stock_info[blob]["LastTradeTime"], '%m/%d/%Y %I:%M%p')
                stock_data[blob]["price"] = float(stock_info[blob]["LastTradePriceOnly"])
            print stock_data
            json.dump(stock_data, outfile, sort_keys = True, indent = 4, ensure_ascii=False, default=date_handler)
    elif resp == 'historical':
        path = raw_input('Path: ')
        start_date = raw_input('Start Date (in mm/dd/yy format): ')
        end_date = raw_input('End Date (in mm/dd/yy format): ')
        for stock_symb in dj_30:
            out_path = path + "/historical_stocks_" + stock_symb + "_" + start_date.replace("/",".") + "_to_" + end_date.replace("/",".") + ".txt"
            try:
                with open(out_path, 'w') as outfile:
                        stock_info = st.get_historical_info(stock_symb, start_date, end_date)
                        stock_data = {}
                        for blob in range(len(stock_info)):
                            stock_data[blob] = {"price":{}, "symbol":stock_symb,"date":{}}
                            stock_data[blob]["price"] = float(stock_info[blob]["Close"])
                            stock_data[blob]["date"] = stock_info[blob]['Date']
                        print stock_data
                        json.dump(stock_data, outfile, sort_keys = True, indent = 4, ensure_ascii=False, default=date_handler)
            except Exception as e:
                print e
            		