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
            #print stock_info
            stock_data = []
            for stock in stock_info:
                stock_data.append({"symbol":stock["Symbol"], "date":stock["LastTradeDate"], "price":float(stock["LastTradePriceOnly"])})
            #print stock_data
            for i in range(len(stock_data)):
                print json.dumps(stock_data[i])
                outfile.write(json.dumps(stock_data[i]))
                outfile.write("\n")
                #json.dumps(stock_data[i], outfile) # sort_keys = True, indent = 4, ensure_ascii=False, default=date_handler)
        outfile.close()
        print "wrote data to %s" % out_path  
    elif resp == 'historical':
        path = raw_input('Path: ')
        start_date = raw_input('Start Date (in mm/dd/yy format): ')
        end_date = raw_input('End Date (in mm/dd/yy format): ')
        for stock_symb in dj_30:
            out_path = path + "/historical_stocks_" + stock_symb + "_" + start_date.replace("/",".") + "_to_" + end_date.replace("/",".") + ".txt"
            try:
                with open(out_path, 'w') as outfile:
                        stock_info = st.get_historical_info(stock_symb, start_date, end_date)
                        stock_data = []
                        for stock in stock_info:
                            stock_data.append({"symbol":stock_symb, "date": stock['Date'], "price":float(stock["Close"])})
                        print stock_data
                        for i in range(len(stock_data)):
                          outfile.write(json.dumps(stock_data[i]))
                          outfile.write("\n")  
                          #json.dump(stock_data[i], outfile, sort_keys = True, indent = 4, ensure_ascii=False, default=date_handler)
            except Exception as e:
                print e
        print "wrote data to files located at: %s" % path 		
