import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
style.use('ggplot')

df=pd.read_csv('tsla.csv',parse_dates=True, index_col=0)

#df['100ma']= df['Adj Close'].rolling(window=100,min_periods=0).mean()

#RESAMPLING:

# sample up: 10 day data from 1 day data
# sample down: 1 day data from seconds or minutes data



#It can be 10D 10M or anything 10D means 10Days

df_ohlc= df['Adj Close'].resample('10D').ohlc()
df_volume=df['Volume'].resample('10D').sum()
# .mean() takes mean of every 10 days
#.sum() takes sum of every 10 days
# .ohlc() is open high low close as shown in the candlesticks

#print(df_ohlc.head())
'''
                 open       high        low      close
Date                                                  
2010-06-29  23.889999  23.889999  15.800000  17.459999
2010-07-09  17.400000  20.639999  17.049999  20.639999
2010-07-19  21.910000  21.910000  20.219999  20.719999
2010-07-29  20.350000  21.950001  19.590000  19.590000
2010-08-08  19.600000  19.600000  17.600000  19.150000

'''

df_ohlc.reset_index(inplace=True)
# this changes dates to columns because candle sticks wants columns
#date as mdates,open, high,low,close

df_ohlc['Date']=df_ohlc['Date'].map(mdates.date2num)



ax1=plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2=plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1 , sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1,df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)


plt.show()

