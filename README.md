**W205 Project : Stock Price and Social Media Correlator**
----------------------------------------------------------

**Amin A, Amin V, Hetal C & Johnny Y**


Setup instructions!
===================

Steps
-------------
 1. Create an m3.large Amazon EC2 instance with EBS volume of 10GB.
 2. Follow the instructions of TheEasyButtonforYourAWSEnvironment_2_2.pdf to install the required software. 
 3. Data Ingestion Layer : We have 2 data sources for this project.
   StockScraper : Picks stock price using Yahoo Finance API
   twitter_data_capture : Stream live tweets from twitter using spark streaming.
 4. Sentiment Analysis (tweet_sentimentscore ) : Use 2 different sentiment API's to determine sentiment score for tweets
 5. Data Aggregation (Hive_script) : aggregates stock and twitter data into hive tables.
 6. Most the code is run as user w205 on the AMI.
 7. Follow setup instructions in each of the individual listed folders.
