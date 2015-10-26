package com.ucb.w205

/**
 * Created by hetal on 10/25/15.
 */

import com.google.gson.{GsonBuilder, JsonParser}
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.Row
import org.apache.spark.{SparkConf, SparkContext}

object TweetTransform {

  val jsonParser = new JsonParser()
  val gson = new GsonBuilder().setPrettyPrinting().create()

  def main(args: Array[String]) {
    // Process program arguments and set properties
    if (args.length < 1) {
      System.err.println("Usage: " + this.getClass.getSimpleName +
        " <tweetInput>")
      System.exit(1)
    }

    //input file path where tweet data is stored
    val Array(tweetInput) = args

    val conf = new SparkConf().setAppName(this.getClass.getSimpleName)
    val sc = new SparkContext(conf)
    val sqlContext = new SQLContext(sc)

    // Pretty print some of the tweets.
    //val tweets = sc.textFile(tweetInput)

    // commented output to UI
//    println("------------Sample JSON Tweets-------")
//    for (tweet <- tweets.take(5)) {
//      println(gson.toJson(jsonParser.parse(tweet)))
//    }

    val tweetTable = sqlContext.read.json(tweetInput).cache()
    //tweetTable.registerTempTable("tweetTable")

    println("------Tweet Schema---")
    tweetTable.printSchema()

    println(tweetTable.show(1))
    //println("----Sample Tweet Text-----")
    //sqlContext.sql("SELECT createdAt,text,retweetCount,id,isPossiblySensitive FROM tweetTable LIMIT 10").collect().foreach(println)

//    println("------Sample Lang, Name, text---")
//    sqlContext.sql("SELECT user.lang, user.name, text FROM tweetTable LIMIT 1000").collect().foreach(println)
//
//    println("------Total count by languages Lang, count(*)---")
//    sqlContext.sql("SELECT user.lang, COUNT(*) as cnt FROM tweetTable GROUP BY user.lang ORDER BY cnt DESC LIMIT 25").collect.foreach(println)
//
//    println("--- Training the model and persist it")
//    val texts = sqlContext.sql("SELECT text from tweetTable").map(_.head.toString)
//    // Cache the vectors RDD since it will be used for all the KMeans iterations.
//    val vectors = texts.map(Utils.featurize).cache()
//    vectors.count()  // Calls an action on the RDD to populate the vectors cache.
//    val model = KMeans.train(vectors, numClusters, numIterations)
//    sc.makeRDD(model.clusterCenters, numClusters).saveAsObjectFile(outputModelDir)
//
//    val some_tweets = texts.take(100)
//    println("----Example tweets from the clusters")
//    for (i <- 0 until numClusters) {
//      println(s"\nCLUSTER $i:")
//      some_tweets.foreach { t =>
//        if (model.predict(Utils.featurize(t)) == i) {
//          println(t)
//        }
//      }
//    }
  }

}
