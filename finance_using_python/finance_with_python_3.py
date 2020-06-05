import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

df=pd.read_csv('tsla.csv',parse_dates=True, index_col=0)

df['100ma']= df['Adj Close'].rolling(window=100,min_periods=0).mean()


#100 moving average: today's price +99 prior days price to create a moving average for today.
# it smooths out price over time.
# that is when it the 100ma or 50ma moves over a upper threshold or below a given lower
#threshold we can deduce an up trend or down trend.


#####df.dropna(inplace=True)

# df['100ma'] produces top 99 columns as nan because it is not possible there so using dropna to
# to remove those rows which had nan
# now the problem is we lose a 100 days.

# So use min_periods=0 to avoid that it calculates like
#{
#	100 ,if present
#	0<x<100, if not
#}

print(df.head())

ax1=plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2=plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1 , sharex=ax1)

# This is used to create a figure with multiple subplots  
# the first is the size of the dataframe, second is the starting index of the plot
#cthird is the span
# the share x means they share a common x axis when we zoom in on one
# we automatically zoom it one the other, so, the alignment is never disturbed.



ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

#df.index means date as it is declared as index already

plt.show()

