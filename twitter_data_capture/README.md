# README

### Pre-requisites
- Run on UCB_w206_postgres_py2.7 AMI 
- maven ( https://maven.apache.org/download.cgi or brew install maven)
## Location of custom code 
- The source code is located : src/main/scala/com/ucb/w205/

#### TwitterFinanceStocksFeed.scala (WIP)
This pull tweets from Twitter to HDFS.  

#### TweetTransform.scala (WIP)
This cleans up the data and transforms it.

## How to compile code
- Run "mvn clean install -DskipTests" to compile the code. 
- This will create jar file in target/w205-0.0.1-SNAPSHOT.jar

## How to run the code
- Please create twitter_data/tweets within the home directory of the user on HDFS. For example, /user/w205/twitter_data/tweets/
-
```sh
$ spark15/bin/spark-submit --packages 'org.twitter4j:twitter4j-stream:3.0.3'  --class com.ucb.w205.TwitterFinanceStocksFeed <path to w205-0.0.1-SNAPSHOT.jar>  <consumer key> <consumer secret> <access token> <access token secret> 

$ park15/bin/spark-submit --class com.ucb.w205.TweetTransform <path to w205-0.0.1-SNAPSHOT.jar>  'twitter_data/tweets/tweets*/part-*'
```

