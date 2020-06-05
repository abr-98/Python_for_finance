import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

#datareader returns pndas data frame from finance APIs

#style.use('ggplot')
#start= dt.datetime(2000,1,1)
#end=dt.datetime(2016,12,31)

#df=web.DataReader('TSLA', 'yahoo', start, end)
#df.to_csv('tsla.csv')

df=pd.read_csv('tsla.csv',parse_dates=True, index_col=0)
print(df.head())

#parse_dates helps to use dates and index_cols lets us use dates as indices instead of
#producing its own indices 0,1,2,3... etc.

df.plot()
plt.show()

#the image shows volume line because it is on a much higher basis then the other 
#values. So it is reflected the most.

df['Adj Close'].plot()
plt.show()

# shows only adjusted close in graph.

print(df[['Open','High']].head())
# prints the open and high with date index head part.

