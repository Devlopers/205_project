set hive.input.dir.recursive=true;
set hive.mapred.supports.subdirectories=true;
set hive.supports.subdirectories=true;
set mapred.input.dir.recursive=true;

drop table raw_tweets;
create external table raw_tweets (json string)
location '/user/w205/twitter_data/processed/combined/';

drop table dj_30_tickers;
create external table dj_30_tickers (ticker string);
load data local inpath '/home/w205/205_project/Hive_script/stock_tickers.csv' overwrite into table dj_30_tickers;

drop table tweets;
create table tweets as
    select get_json_object(json, "$.stock_ticker") as ticker,
          to_date(from_unixtime(unix_timestamp(get_json_object(json, "$.createdAt"),
                "MMM dd, yyyy hh:mm:ss a"))) as date,
           get_json_object(json, "$.indicoScore") as indicoScore, get_json_object(json, "$.textblobScore") as textblobScore
    from raw_tweets;

drop table tweet_data_per_day;
create table tweet_data_per_day as
select ticker, date, count(*) as tweetcount, avg(indicoScore) as indicoScore, avg(textblobScore) as textblobScore from tweets where tweets.ticker in (select * from dj_30_tickers) group by ticker, date order by tweetcount desc;

drop table raw_stock_prices;
create external table raw_stock_prices (json string)
location '/user/w205/stock_data';

drop table stock_prices;
create table stock_prices as
    select get_json_object(json, "$.symbol") as ticker,
          get_json_object(json, "$.date") as date,
          get_json_object(json, "$.price") as price

    from raw_stock_prices;
select * from stock_prices;

drop table stock_tweet_data;
create table stock_tweet_data as
select t.ticker, t.date, t.tweetcount, t.indicoScore, t.textblobScore, s.price from tweet_data_per_day t inner join stock_prices as s on (t.ticker = s.ticker and t.date = s.date) order by tweetcount desc;

select * from stock_tweet_data limit 20;
