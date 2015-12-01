Setup instructions!
===================

Steps
-------------
 1. All instructions are run as user 'root' from roots home directory unless specified and 
 2. Install python2.7 using the below command 
 ```
 $sudo yum install python27-devel –y
 ```
 
 3. Next we will install pip2.7
 ```
 curl -O https://bootstrap.pypa.io/ez_setup.py
 python2.7 ez_setup.py
 easy_install-2.7 pip
 ```
 4.  We will need some additional libraries so run the below command
 ```
pip2.7 install urllib3
pip2.7 install pandas
pip2.7 install IPython
 ```

 5. Next we will install Indico sentiment analysis API (ref: https://indico.io/ )
 ```
git clone https://github.com/IndicoDataSolutions/IndicoIo-Python.git
python2.7 setup.py install
 ```

 This API will return a number between 0 and 1. This number is a probability representing the likelihood that the analyzed text is positive or negative. Values greater than 0.5 indicate positive sentiment, while values less than 0.5 indicate negative sentiment.

 6.  Now onto text blob  (ref: http://textblob.readthedocs.org/en/dev/index.html)
 ```
pip2.7 install -U textblob
python2.7 -m textblob.download_corpora
 ```

 You might want to run the last command once again as user w205
 The sentiment property returns a namedtuple of the form Sentiment(polarity, subjectivity). The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
 
 7.  Modify the modify spark-env.sh file (location can be : 
~w205/spark15/conf/spark-env.sh) and set below variables
 ```
 export PYSPARK_PYTHON=/usr/bin/python2.7
 export PYSPARK_DRIVER_PYTHON=/usr/bin/ipython
 ```

> **Note:**

> - Create an api account at https://indico.io/ and have the api key generated for you to use.


Code modifcations 
-------------------

 1. Once you have the API key from Indico add it to the python script
 2. The code allows you to select a model for sentiment analysis. If you select COMBINED it currently runs INDICOCO and TEXTBLOB. I have not included the TEXTBLOB Naive Bayes classifier as its taking longer time to run. 
 3. The code processes one directory at a time. I added a break in the for loop to ensure we wouldn't hit the API limits.
 4. Data is written back into HDFS as  json file under the directory twitter_data/tweets/processed/<'model name'>/<'date of the original directory code processed'>
 5. Copy the python script to home directopry of user w205
 6. Run the code as user w205 and from spark15 directory.

 ```
 spark15>./bin/pyspark ~/tweet_sentiment.py
 ```
