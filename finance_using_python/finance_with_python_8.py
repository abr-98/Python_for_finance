import matplotlib.pyplot as plt
from matplotlib import style
import bs4 as bs 
import pickle
import requests
import datetime as dt
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

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

	
		if main_df.empty:
			main_df=df
		else:
			main_df=main_df.join(df,how='outer')
		

		if count%10==0:
			print(count)


	print(main_df.head())
	main_df.to_csv('sp500_joined_closes.csv')

def visualize_data():
	df=pd.read_csv('sp500_joined_closes.csv')
	#df['AAPL'].plot()
	#plt.show()

	df_corr=df.corr()
	#df_corr.set_index('Date',inplace=True)

	##This will look at all the columns in our data frame compare 
	#all  relation and generate correlation value.

	print(df_corr.head())
	'''
	     Date        MMM       ABT  ABBV  ...       ZBRA  ZBH       ZION  ZTS
0  1999-12-31  27.055576  6.810734   NaN  ...  26.000000  NaN  43.440506  NaN
1  2000-01-03  26.088079  6.564564   NaN  ...  25.027779  NaN  40.734089  NaN
2  2000-01-04  25.051456  6.377004   NaN  ...  24.666666  NaN  38.761597  NaN
3  2000-01-05  25.777090  6.365284   NaN  ...  25.138889  NaN  38.715733  NaN
4  2000-01-06  27.850321  6.588011   NaN  ...  23.777779  NaN  39.266190  NaN

	'''
	## Correlations are pretty important because if two comapanies are highly 
	#correlated and one's price goes up other's price is bound to go up
	# or if they are negatively correlated then if one goes up others will go down
	#this gives us a insight of any event that may happen.

	data=df_corr.values


	fig=plt.figure()
	ax=fig.add_subplot(1,1,1)
	#(1x1) plot at subplot 1

	heatmap=ax.pcolor(data, cmap=plt.cm.RdYlGn)

	## it is a range of red yellow green, red->negative, yellow->neutral, green->positive

	fig.colorbar(heatmap)

	# it forms like legend to show ranges

	ax.set_xticks(np.arange(data.shape[0])+ 0.5, minor=False)
	ax.set_yticks(np.arange(data.shape[1])+ 0.5, minor=False)


	## We are setting the ticks to show proper company positions
	# we are installing tick marks at a distance of 0.5

	ax.invert_yaxis()
	ax.xaxis.tick_top()

	## positioning the row and column labels
	columns_labels=df_corr.columns

	#Taking up the company names

	row_labels=df_corr.index

	#taking up indices as dates

	ax.set_xticklabels(columns_labels)
	ax.set_yticklabels(row_labels)

	#getting the label values
	plt.xticks(rotation=90)

	#rotating the ticks by 90 so that they dont squeeze
	heatmap.set_clim(-1,1)
	## setting the heat map limeits between -1 to 1

	plt.tight_layout()
	plt.show()

visualize_data()

##if we watch 8.2 we will get some verystrong negative correaltion
##all red.
