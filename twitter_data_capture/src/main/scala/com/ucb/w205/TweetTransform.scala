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


    val tweetTable = sqlContext.read.json(tweetInput).cache()
    //tweetTable.registerTempTable("tweetTable")

    println("------Tweet Schema---")
    tweetTable.printSchema()

    println(tweetTable.show(1))

//    // sample script to expand hashtag entities
//    val foo = tweetTable.select("hashtagEntities", "id", "text")
//
//    case class fooTag (hashtag_end:Long, hashtag_start:Long, hashtag_text: String)
//
//    val explodedFoo = foo.explode(foo("hashtagEntities")) {
//      case Row(hashtagEntity : Seq[Row]) => hashtagEntity.map(hashtagEntity =>
//        fooTag(hashtagEntity(0).asInstanceOf[Long], hashtagEntity(1).asInstanceOf[Long], hashtagEntity(2).asInstanceOf[String])
//      )
//    }

  }

}
