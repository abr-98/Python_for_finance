
##S&P 500: Top 500 companies by market cap
# Market cap:No of shares * price 
# top 500 companies
import bs4 as bs
import pickle
import requests

# We are going to save the top 500 S&P list from wikipedia by 
# scrapping it


def save_sp500_tickers():
	resp=requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup=bs.BeautifulSoup(resp.text)
	#We only want the text portion 
	table=soup.find('table',{'class':'wikitable sortable'})
	#<table class="wikitable sortable" id="constituents"> 
	# this is present in the source code so we just need to find it
	#and set the class here same as the class on the table
	#Soup will find the object table with class name .....
	tickers=[]

	for row in table.findAll('tr')[1:]:
		#tr is table rows
		# first has some information we don't need
		ticker=row.findAll('td')[0].text[:-1]
		#td is the table data
		# it will give a list as there are mutiple columns
		# we only comany tickers so only 0 th element we are taking
		#soup returns soup object so convert to text

		tickers.append(ticker)

	with open("sp500tickers.pickle",'wb') as f:
		pickle.dump(tickers, f)

	print(tickers)

	return tickers


save_sp500_tickers()