
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

def get_data_from_yahoo(reload_sp500=False):
	if reload_sp500:
		tickers=save_sp500_tickers()
	else:
		with open("sp500tickers.pickle",'rb') as f:
			tickers=pickle.load(f)


	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')


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

#get_data_from_yahoo()

def compile_data():
	with open("sp500tickers.pickle",'rb') as f:
			tickers=pickle.load(f)

	main_df=pd.DataFrame()

	for count,ticker in enumerate(tickers):
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			continue
		df=pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		df.set_index('Date',inplace=True)

		df.rename(columns={'Adj Close': ticker}, inplace=True)
		df.drop(['Open','High','Low',"Close",'Volume'],axis=1,inplace=True)

		#We only have Adj close by ticker name only 
		if main_df.empty:
			main_df=df
		else:
			main_df=main_df.join(df,how='outer')
			#this prevents data to be dropped for any body

		if count%10==0:
			print(count)


	print(main_df.head())
	main_df.to_csv('sp500_joined_closes.csv')
'''

	                  MMM       ABT  ABBV      ABMD  ...       ZBRA  ZBH       ZION  ZTS
Date                                             ...                                
1999-12-31  27.055576  6.810734   NaN  18.37500  ...  26.000000  NaN  43.440506  NaN
2000-01-03  26.088079  6.564564   NaN  18.25000  ...  25.027779  NaN  40.734089  NaN
2000-01-04  25.051456  6.377004   NaN  17.81250  ...  24.666666  NaN  38.761597  NaN
2000-01-05  25.777090  6.365284   NaN  18.00000  ...  25.138889  NaN  38.715733  NaN
2000-01-06  27.850321  6.588011   NaN  18.03125  ...  23.777779  NaN  39.266190  NaN

'''
# some of them has NaN because they were not trading back then.
# So, this actually creates a csv containing all the companies closing prices 
#daywise


compile_data()

