package com.ucb.w205

import java.io.File

import com.google.gson.Gson
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SQLContext
import org.apache.spark.streaming.twitter._
import org.apache.spark.sql.Row


/**
 * Collect at least the specified number of tweets into json text files.
 */
object TwitterFinanceStocksFeed {
  private var gson = new Gson()
  private var partNum = 0
  private var numTweetCollected = 0L
  private val outputDirectory = "twitter_data/tweets/"
  private var numTweetsToCollect = 100
  private var intervalSecs = 20
  private var partitionsEachInterval = 1

  case class symbols(stock_ticker: String)

  def main (args: Array[String]){
    if(args.length != 5){
      System.err.println("Usage: TwitterFinanceStocksFeed <consumer key> <consumer secret>" +
      "<access token> <access token secret> <filename>")
      System.exit(1)
    }

    val Array(consumerKey, consumerSecret, accessToken, accessTokenSecret) = args.take(4)
    val Array(stockFile) = args.takeRight(1)
    println ("Stock Ticker File path is :" +stockFile)
    val filters = scala.io.Source.fromFile(stockFile).getLines().toArray

    //val filters = Array("$AAPL","$GOOG","$GOOGL","TSLA","$NFLX","$BABA","$YHOO","$BIDU","$AMZN","$CSCO","$FB","$TWTR")

    // Set the system properties so that Twitter4j library used by twitter stream
    // can use them to generat OAuth credentials
    System.setProperty("twitter4j.oauth.consumerKey", consumerKey)
    System.setProperty("twitter4j.oauth.consumerSecret", consumerSecret)
    System.setProperty("twitter4j.oauth.accessToken", accessToken)
    System.setProperty("twitter4j.oauth.accessTokenSecret", accessTokenSecret)

    println("Initializing Streaming Spark Context...")

    val sparkConf = new SparkConf().setAppName(this.getClass.getSimpleName)
    val sc = new SparkContext(sparkConf)
    val ssc = new StreamingContext(sc, Seconds(20))
    val sqlContext = new SQLContext(sc)

    var counter = 1

    val tweetStream = TwitterUtils.createStream(ssc, None, filters).map(gson.toJson(_))

    tweetStream.foreachRDD((rdd,time) => {
      val count = rdd.count()
      System.err.println("Entering rdd loop: "+counter +" Time = " + time)
      System.err.println("Number of tweets : "+count)
      counter += 1
      if(count > 0){
        val outputRDD = rdd.repartition(partitionsEachInterval)
        val tweet_df = sqlContext.read.json(outputRDD)
        val tweet_tmp = tweet_df.select("id","createdAt","text","retweetCount","symbolEntities")
        val exploded_tweet = tweet_tmp.explode(tweet_tmp("symbolEntities")){
          case Row(symbolEntity :Seq[Row]) => symbolEntity.map(symbolEntity =>
            symbols(symbolEntity(2).asInstanceOf[String]))
        }
        val tweets = exploded_tweet.select("id","createdAt","text","retweetCount","stock_ticker")
        tweets.write.format("json").save(outputDirectory +"/tweets_"+time.milliseconds.toString)
        //outputRDD.saveAsTextFile(outputDirectory +"/tweets_"+time.milliseconds.toString)
        numTweetCollected += count

        if(numTweetCollected > numTweetsToCollect)
          {
            System.exit(0)
          }
      }
    })

    ssc.start()
    ssc.awaitTermination()


  }
}