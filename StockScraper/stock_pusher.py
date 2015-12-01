import stockretriever as st
import json
from datetime import datetime
from stock_symbols import dj_30
from sys import argv

def data_org(info):
	stock_data = {}
	for blob in range(len(stock_info)):
    	stock_data[blob] = {"symbol":{},"time":{},"price":{}}
    	stock_data[blob]["symbol"] = stock_info[blob]["Symbol"] 
    	stock_data[blob]["time"] = datetime.strptime(stock_info[blob]["LastTradeDate"]+" "+stock_info[blob]["LastTradeTime"], '%m/%d/%Y %I:%M%p')
    	stock_data[blob]["price"] = float(stock_info[blob]["LastTradePriceOnly"])
    	return stock_data

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

if __name__ == "__main__":
    resp = raw_input('today/historical?: ')
    if resp == 'today':
    	out_path = argv[1] + "/stocks_" + str(datetime.now().strftime('%Y-%m-%d')) + ".txt"
    	with open(out_path, 'w') as outfile:
    		stock_info = st.get_current_info(dj_30)
    		stock_data = data_org(stock_info)
    		print stock_data
    		json.dump(stock_data, outfile, sort_keys = True, indent = 4, ensure_ascii=False, default=date_handler)
    elif resp == 'historical':
    	out_path = argv[1] + "/historical_stocks_" + str(argv[2]).replace("/",".") + "_to_" + str(argv[3]).replace("/",".") + ".txt"
    	with open(out_path, 'w') as outfile:
    		print hist_data
    		try:
    			stock_info = st.get_historical_info(dj_30, argv[2], argv[3])
    			stock_data = data_org(stock_info)
    			print stock_data
    			json.dump(stock_data, outfile, sort_keys = True, indent = 4, ensure_ascii=False, default=date_handler)
    		except Exception as e:
    			print "Error: historical needs a start date and an end date in the format mm/dd/yy, ie '08/10/15'."
    		