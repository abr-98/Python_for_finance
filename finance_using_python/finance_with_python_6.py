
import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web

def save_sp500_tickers():
	resp=requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup=bs.BeautifulSoup(resp.text)
	
	table=soup.find('table',{'class':'wikitable sortable'})

	tickers=[]

	for row in table.findAll('tr')[1:]:
		
		ticker=row.findAll('td')[0].text[:-1]
		
		tickers.append(ticker)

	with open("sp500tickers.pickle",'wb') as f:
		pickle.dump(tickers, f)


	return tickers


#save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
	if reload_sp500:
		tickers=save_sp500_tickers()
	else:
		with open("sp500tickers.pickle",'rb') as f:
			tickers=pickle.load(f)


	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')

	# Making repository for local data
	#yahoo pulls take time

	start= dt.datetime(2000,1,1)
	end=dt.datetime(2016,12,31)

	for ticker in tickers:
		print(ticker)
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			try:
				df=web.DataReader(ticker, 'yahoo', start, end)
				df.to_csv('stock_dfs/{}.csv'.format(ticker))
			except:
				print("Error")
				continue

		else:
			print('already have {}'.format(ticker))
 
		# here we are not updating if the file already exists
		# in practice these values are updated regualrly and
		# we keep a csv for every s&p 500 and we save it in the folder and 
		# if it is there we don't update here.

get_data_from_yahoo()

#Getting the data


