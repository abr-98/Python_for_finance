import numpy as np
import pandas as pd
import pickle


## this is the start of machine learning
# now there are two types of prediction
# first: we have seen all companies are correlated with each other
# so, maybe if we can study the change in all of them probably 
# we can predict something about the others
#######################################################

## second:  we can predict about a company from its chart only
# in past times.

# we are going to change the pricing data to percentage change to 
#normalize things THese will be features

##We will try to label every thing as buy sell or hold

#Now the way we are labelling that is we will look at the features
#Ask the question based on the training data 
#Did the stock price in the data based on these features go up 2% 
#in next 7 days. If its a yes its a buy 
##it falls 2% if yes its a sell
# if nothing we keep it on hold

def process_data_for_labels(ticker):
	##Each model will be on a particular company basis
	#but each company will take in features as the price of all other 
	#companies

	hm_days=7
	##how many days

	df=pd.read_csv("sp500_joined_closes.csv",index_col=0)

	tickers=df.columns.values.tolist()
	df.fillna(0, inplace=True)

	#exchanges nan with 0

	for i in range(1,hm_days+1):
		df['{}_{}d'.format(ticker,i)]= (df[ticker].shift(-i) - df[ticker])/df[ticker]

		# the shift(-i) actually is there to shift to the future.

		##so this will be the ticker and the day number like day i in the future
		# the value will be (the price in two days - today's price)/ today's price * 100

	df.fillna(0,inplace=True)


process_data_for_labels('XOM')



