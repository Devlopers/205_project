# Author : Hetal Chandaria
#This code loops uses tow different externam API's to determine tweet sentiment score

from __future__ import print_function
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import HiveContext

import urllib3
import indicoio
import sys
import os
import pydoop.hdfs

from pyspark.sql.types import FloatType
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


dfs_handle = pydoop.hdfs.hdfs()
BASE_DATA_DIR = "twitter_data/tweets/"
PROCESSED_DATA_DIR = "twitter_data/processed/"
INDICOIO = "indicoio"
INDICOIO_SCORE = "indicoScore"
TEXTBLOB = "textblob"
TEXTBLOB_SCORE = "textblobScore"
COMBINED = "combined"
TEXTBLOB_NB = "textblob_NB"
TEXTBLOB_NB_POS_SCORE = "textblobScore_NB_pos"
TEXTBLOB_NB_NEG_SCORE = "textblobScore_NB_neg"

# Function to find which dirs are not processed
# Processed tweets i.e. ones for which sentiment already calculated
# will have dirs created under the processed/model_name/ dir
def find_unprocessed_dirs(model_name):
  tweet_datadirs = dfs_handle.list_directory(BASE_DATA_DIR)
  datadirs = {}
  processdirs = {}
  unprocessed_dirs = {}
  for tweet_datadir in tweet_datadirs:
    if (tweet_datadir['kind'] != 'directory'):
      continue
    filename = os.path.basename(tweet_datadir['name'])
    datadirs[filename] = tweet_datadir['name']
  try:
    tweet_processdirs = dfs_handle.list_directory(PROCESSED_DATA_DIR + model_name + "/")
    for tweet_processdir in tweet_processdirs:
      if (tweet_processdir['kind'] != 'directory'):
        continue
      filename = os.path.basename(tweet_processdir['name'])
      processdirs[filename] = tweet_processdir['name']
  except IOError:
    pass
  for datadir in datadirs.keys():
    if datadir not in processdirs:
      unprocessed_dirs[datadir] = datadirs[datadir]
  return unprocessed_dirs

# Sentiment analysis function using Indicoio https://indico.io/
def indicoioSentiment(x):
  urllib3.disable_warnings()
  indicoio.config.api_key = '<add ur key here >'
  return indicoio.sentiment(x)

# Sentiment analysis using TextBlob http://textblob.readthedocs.org/en/dev/index.html
def textblobSentiment(x):
  t = TextBlob(x)
  return t.sentiment.polarity

# Sentiment analysis using TextBlob http://textblob.readthedocs.org/en/dev/index.html
# this function uses Naibe Bayes classifier
def textblobSentiment_NB_pos(x):
    t = TextBlob(x,analyzer=NaiveBayesAnalyzer())
    return t.sentiment.p_pos

# Sentiment analysis using TextBlob http://textblob.readthedocs.org/en/dev/index.html
# this function uses Naibe Bayes classifier
def textblobSentiment_NB_neg(x):
    t = TextBlob(x,analyzer=NaiveBayesAnalyzer())
    return t.sentiment.p_neg

models = {}
models[INDICOIO] = [INDICOIO]
models[TEXTBLOB] = [TEXTBLOB]
models[TEXTBLOB_NB]=[TEXTBLOB_NB]
models[COMBINED] = [INDICOIO, TEXTBLOB]

#convert date into a safer string for using as table name
def safeDirName(x):
  return x.replace("-","")

#construct query based on enabled models
def constructQuery(tableName, models):
  query = "SELECT " + tableName + ".*"
  if INDICOIO in models:
    query = query + ", indicoioSentiment(" + tableName + ".text) AS " + INDICOIO_SCORE
  if TEXTBLOB in models:
    query = query + ", textblobSentiment(" + tableName + ".text) AS " + TEXTBLOB_SCORE
  if TEXTBLOB_NB in models:
    query = query + ", textblobSentiment_NB_pos(" + tableName + ".text) AS " + TEXTBLOB_NB_POS_SCORE
    query = query + ", textblobSentiment_NB_neg(" + tableName + ".text) AS " + TEXTBLOB_NB_NEG_SCORE
  query = query + " FROM " + tableName
  return query

def executeSentimentAnalysis(dataDirName, dataDir, modelName, tableName, query):
  df = sqlContext.read.json(dataDir + "/tweets_*/")
  print ("Processing " + str(df.count()) + " tweets from " + datadir + " using query: " + query)
  sqlContext.registerDataFrameAsTable(df, tableName)
  analysed_df = sqlContext.sql(query)
  finalOutputDirectory = PROCESSED_DATA_DIR + modelName + "/" + dataDirName + "/"
  print ("Writing " + str(analysed_df.count()) + " tweets to " + finalOutputDirectory)
  analysed_df.write.format("json").save(finalOutputDirectory)
  # rows = analysed_df.head(10)
  # for row in rows:
  #   print row

if __name__ == "__main__":
    sc = SparkContext()
    sqlContext = SQLContext(sc)
    urllib3.disable_warnings()

    #register UDFs
    sqlContext.registerFunction("indicoioSentiment", indicoioSentiment, FloatType())
    sqlContext.registerFunction("textblobSentiment", textblobSentiment, FloatType())
    sqlContext.registerFunction("textblobSentiment_NB_pos", textblobSentiment_NB_pos, FloatType())
    sqlContext.registerFunction("textblobSentiment_NB_neg", textblobSentiment_NB_neg, FloatType())

    APPLY_MODEL = COMBINED

    tweet_datadirs = dfs_handle.list_directory("twitter_data/tweets/")
    datadirs = find_unprocessed_dirs(APPLY_MODEL)

    print ("No. of unprocessed dirs: "+str(len(datadirs)))
    for datadir in datadirs.keys():
      print ("Processing tweets from datadir: " + datadirs[datadir])
      tableName = "tweetTable" + safeDirName(datadir)
      query = constructQuery(tableName, models[APPLY_MODEL])
      executeSentimentAnalysis(datadir, datadirs[datadir], APPLY_MODEL, tableName, query)
      break
