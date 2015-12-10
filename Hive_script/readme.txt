READ ME
December 9, 2015
Amin

=================================
 Updates completed in this commit
=================================
- created hive script tweet_stock_hive_script.hql to store, transform, and aggregate raw tweet and stock data into hive tables
- created a stock_tickers.csv file for easy hive ingestion
- updated the stock_pusher.py to output the needed file format for easy hive processing

===========
Instructions
===========

- Make sure that file "stock_tickers.csv" is in '/home/w205/205_project/Hive_script.csv'
- Generate historical stock data using the updated version of stock_pusher.py and place in HDFS in '/user/w205/stock_data'

- Ensure tweet data in '/user/w205/twitter_data/processed/combined/'
- Run the script tweet_stock_hive_script.hql as follows $ hive -f tweet_stock_hive_script.hql
- This will load raw data into hive, process into Hive tables and then aggregate into one final table called "stock_tweet_data" that has the following fields:
    - ticker
    - date
    - tweet count: number of tweets on a given day
    - indicoScore: average indico sentiment Score across all tweets from given day
    - textblobScore: average textblob sentiment Score across all tweets from given day

    - price: ending stock price on given day
- Note: stock_tweet_data will only have entries for where we have both tweet and stock price data for  given company on a given day
