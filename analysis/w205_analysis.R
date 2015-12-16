# W205  - Final Project
# Stock Price and Social Media correlator
# Author : Hetal Chandaria

rm(list = ls())
setwd("~/programming/R")
Sys.getenv("HOME")
library(ggplot2) 
library(reshape)
library(Rcmdr)
dataDirectory <-file.path(Sys.getenv("HOME"),"programming","R","W205")
dataFile <-file.path(dataDirectory,"stock_tweet.csv")
stock_tweet <-read.csv(dataFile,header=TRUE)
colnames(stock_tweet)

#convert tweet count to num
stock_tweet$Tweetcount = as.numeric(sub(",","",(as.character(stock_tweet$Tweetcount))))

all_price_tweet = lm(Price ~ Tweetcount + Indicoscore+Textblobscore,stock_tweet)
summary(all_price_tweet)

price_tweet = lm(Price ~ Tweetcount + Indicoscore+Textblobscore,stock_tweet[stock_tweet$Ticker =='AAPL',])
summary(price_tweet)

cor(stock_tweet[stock_tweet$Ticker=='AAPL',c("Price","Tweetcount","Indicoscore","Textblobscore")])
