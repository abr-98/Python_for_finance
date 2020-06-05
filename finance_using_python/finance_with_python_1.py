import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

#datareader returns pndas data frame from finance APIs

style.use('ggplot')
start= dt.datetime(2000,1,1)
end=dt.datetime(2016,12,31)

df=web.DataReader('TSLA', 'yahoo', start, end)

#First is a ticker which a short 3 to 4 letter word representing the stock

# yahoo is the source where from to get the data

#start and end are the limits.

print(df.head())
# if in the head we pass an integer x we will get x rows

#df.tail() # for the end

#Adjusted close: When a stock price goes too high it is adjusted by the 
#Company. Else it is same as the close. #Normally it is a stock split
# i,e when a stock goes too high. The price is divided into two stocks of equal price.

df.to_csv('tsla.csv')


