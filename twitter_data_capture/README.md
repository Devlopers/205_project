# README

### Pre-requisites
- Run on UCB_w206_postgres_py2.7 AMI 
- maven ( https://maven.apache.org/download.cgi or brew install maven)

### Location of custom code 
- The source code is located : src/main/scala/com/ucb/w205/

#### TwitterFinanceStocksFeed.scala (Final)
This pull tweets from Twitter to HDFS.  


## How to compile code
- Run "mvn clean install -DskipTests" to compile the code. 
- This will create jar file in target/w205-0.0.1-SNAPSHOT.jar

## How to run the code

- Please create twitter_data/tweets within the home directory of the user on HDFS. For example, /user/w205/twitter_data/tweets/

```sh
$ spark15/bin/spark-submit --packages 'org.twitter4j:twitter4j-stream:3.0.4'  --class com.ucb.w205.TwitterFinanceStocksFeed <path to w205-0.0.1-SNAPSHOT.jar>  <consumer key> <consumer secret> <access token> <access token secret>  <path to stock ticker list>

If you are not running m3.large instance of EC2 than you need to modify the above command 
$ spark15/bin/spark-submit --master local[3] --packages 'org.twitter4j:twitter4j-stream:3.0.4'  --class com.ucb.w205.TwitterFinanceStocksFeed <path to w205-0.0.1-SNAPSHOT.jar>  <consumer key> <consumer secret> <access token> <access token secret>  <path to stock ticker list>
```

- TweetTransform is no longer needed but can serve as example code on how to load the generated data for additional processing.

```sh
$ spark15/bin/spark-submit --class com.ucb.w205.TweetTransform <path to w205-0.0.1-SNAPSHOT.jar>  'twitter_data/tweets/tweets*/part-*'
```

