package com.ucb.w205

import java.io.File

import com.google.gson.Gson
import org.apache.spark.streaming.twitter.TwitterUtils
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext}


/**
 * Collect at least the specified number of tweets into json text files.
 */
object TwitterFinanceStocksFeed {
  private var gson = new Gson()
  private var partNum = 0
  private var numTweetCollected = 0L
  private val outputDirectory = "twitter_data/tweets/"
  private var numTweetsToCollect = 10
  private var intervalSecs = 10
  private var partitionsEachInterval = 1

  def main (args: Array[String]){
    if(args.length < 4){
      System.err.println("Usage: TwitterFinanceStocksFeed <consumer key> <consumer secret>" +
      "<access token> <access token secret> [<filters>]")
      System.exit(1)
    }

    val Array(consumerKey, consumerSecret, accessToken, accessTokenSecret) = args.take(4)
    //val filters = args.takeRight(args.length - 4)
    val filters = Array("news")

    // Set the system properties so that Twitter4j library used by twitter stream
    // can use them to generat OAuth credentials
    System.setProperty("twitter4j.oauth.consumerKey", consumerKey)
    System.setProperty("twitter4j.oauth.consumerSecret", consumerSecret)
    System.setProperty("twitter4j.oauth.accessToken", accessToken)
    System.setProperty("twitter4j.oauth.accessTokenSecret", accessTokenSecret)


    println("Initializing Streaming Spark Context...")

    val sparkConf = new SparkConf().setAppName(this.getClass.getSimpleName)
    val ssc = new StreamingContext(sparkConf, Seconds(20))

    var counter = 1

    val tweetStream = TwitterUtils.createStream(ssc, None, filters).map(gson.toJson(_))

    tweetStream.foreachRDD((rdd,time) => {
      val count = rdd.count()
      System.err.println("Entering rdd loop: "+counter +" Time = " + time)
      System.err.println("Number of tweets : "+count)
      counter += 1
      if(count > 0){
        val outputRDD = rdd.repartition(partitionsEachInterval)
        outputRDD.saveAsTextFile(outputDirectory +"/tweets_"+time.milliseconds.toString)
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