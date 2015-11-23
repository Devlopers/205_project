import stockretriever as st
import json
from datetime import datetime
from stock_symbols import dj_30
from sys import argv

stock_info = st.get_current_info(dj_30)
stock_data = {}
for blob in range(len(stock_info)):
    stock_data[blob] = {"symbol":{},"time":{},"price":{}}
    stock_data[blob]["symbol"] = stock_info[blob]["Symbol"] 
    stock_data[blob]["time"] = datetime.strptime(stock_info[blob]["LastTradeDate"]+" "+stock_info[blob]["LastTradeTime"], '%m/%d/%Y %I:%M%p')
    stock_data[blob]["price"] = float(stock_info[blob]["LastTradePriceOnly"])

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

out_path = argv[1] + "/stocks_" + str(datetime.now().strftime('%Y-%m-%d')) + ".txt"

if __name__ == "__main__":
    with open(out_path, 'w') as outfile:
        print stock_data
        json.dump(stock_data, outfile, sort_keys = True, indent = 4, ensure_ascii=False, default=date_handler)