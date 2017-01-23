# Relevant imports
import matplotlib.pyplot as plt
import datetime
from yahoo_finance import Share
from statistics import mean
import matplotlib.dates as dt
import matplotlib.finance as mfinance
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
import matplotlib.ticker as ticker
# Create a class to contain relevant stock values for a time period
class Bar:
    def __init__(self,open,high,low,close,volume):
        self.Open=open
        self.High=high
        self.Low=low
        self.Close=close
        self.Volume=volume
    def __repr__(self):
        return('O=%0.2f, H=%0.2f, L=%0.2f, C=%0.2f, V=%d'%(self.Open,self.High,self.Low,self.Close,self.Volume))

# Also want a daily Bar that contain the OHLC of a stock with the date and stock symbol
class Daily_Bar(Bar):
    def __init__(self, open, high, low, close,date,volume):
        super().__init__(open,high,low,close,volume)
        self.Date=date

# Want a class of data series to perform functions on
class Data_Series:
    def __init__(self,data_list):
        self.DataList=data_list
    # Create a function to find the simple moving average
    def get_simple_moving_average(self,average_number):
        sma=[]
        for i in range(len(self.DataList)-(average_number-1)):
            sum_data=0
            for j in range(average_number):
                sum_data=sum_data+self.DataList[i+j]
            sma.append(sum_data/average_number)
        return(sma)


# Defining smaller functions that will become relevant in the later function
def make_string_date(date):
    return(str(date.year) + '-' + str(date.month) + '-' + str(date.day))


def get_daily_data(data):
    KeyInfo=[]
    for i in range(len(data)):
        KeyInfo.append([float(data[i]['Open']), float(data[i]['Close']), float(data[i]['High']), float(data[i]['Low'])])
    return(KeyInfo)

def create_list(x, KeyFigures):
    list=[]
    for i in range(len(KeyFigures)):
        list.append(KeyFigures[i][x])
    return(list)

def get_list(value, KeyFigures):
    list=[]
    for i in range(len(KeyFigures)):
        list.append(KeyFigures[i].__getattribute__(value))
    return(list)

# Function that produces a list of Bars for a stock from a start date to an end date
def read_daily_bars(symbol_name, start_date, end_date):
    # Turn datetime objects into strings
    str_start_date=make_string_date(start_date)
    str_end_date=make_string_date(end_date)
    #Fetch information on shares from yahoo_finance
    share=Share(symbol_name)
    yahoo_data=share.get_historical(str_start_date,str_end_date)

    # Create a  list of Bars for the time period
    key_figures=[]
    for i in range(len(yahoo_data)):
        key_figures.append(Daily_Bar(float(yahoo_data[i]["Open"]),float(yahoo_data[i]["High"]),float(yahoo_data[i]["Low"]),float(yahoo_data[i]["Close"]),yahoo_data[i]["Date"],float(yahoo_data[i]["Volume"])))
    return(key_figures)

# Need to return ohlc data in list form
def get_candlestick_list(list_daily_bars):
    candlestick_list=[]
    for i in range(len(list_daily_bars)):
        candlestick_list.append([list_daily_bars[i].Date,list_daily_bars[i].Open,list_daily_bars[i].High,list_daily_bars[i].Low,list_daily_bars[i].Low])
    return(candlestick_list)

# Start the overall purpose function which returns the years OHLC, average
# OHLC and company name for a given symbol
def analyse_recent_year(symbol):
    # Find the date today as datetime object
    today = datetime.date.today()

    # Create date time object for last year
    last_year = today - datetime.timedelta(days=365)

    # Create a list of the OHLC daily bars ove the last year
    list_daily_bars=read_daily_bars(symbol, last_year, today)

    # Retrieve the OHLC of the stock for each day of the year
    list_opens=get_list('Open', list_daily_bars)
    list_close=get_list('Close', list_daily_bars)
    list_highs=get_list('High', list_daily_bars)
    list_lows=get_list('Low', list_daily_bars)
    list_volumes=get_list('Volume',list_daily_bars)

    # Extract the OHLC for the years period
    year_open=list_opens[-1]
    year_close=list_close[0]
    year_high=max(list_highs)
    year_low=min(list_lows)
    year_volume=sum(list_volumes)
    # Calculate the Average OHLC for the years period
    average_open=mean(list_opens)
    average_close=mean(list_close)
    average_high=mean(list_highs)
    average_low=mean(list_lows)
    average_volume=mean(list_volumes)
    #Get Company name
    share=Share(symbol)
    share_name=share.get_name()
    # Answer a tuple, the first element is the OHLC bar for the year and the second element is the
    # average bar for the year. The third element is the share name. Tuples are nice ways to return more than one thing from a function.
    return((Bar(year_open,year_high,year_low,year_close,year_volume),Bar(average_open,average_high,average_low,average_close,average_volume),share_name))



# Need to convert lists of string dates to lists of dates that can be plotted
def make_list_plot_dates(list_dates):
    list_plot_dates=[]
    for i in range(len(list_dates)):
        list_plot_dates.append(dt.datestr2num(list_dates[i]))
    return(list_plot_dates)

# Want to plot the close share value for a certain time period
def plot_closes(symbol,start_date,end_date):
    # Creates a list of the daily bars for the stock
    list_daily_bars=read_daily_bars(symbol, start_date, end_date)

    # Need to create the lists for the axis
    list_dates=get_list("Date",list_daily_bars)
    list_closes=get_list("Close",list_daily_bars)
    list_plot_dates=make_list_plot_dates(list_dates)
   # Creating the plot with red line and dots for points
   # Also adding appropriate titles
    plt.plot_date(list_plot_dates,list_closes,'r-o', xdate=True)
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Stock Price for '+symbol)
    plt.show()

# Want to plot a candlestick graph a particular stock over a given time period
def plot_candlestick_with_yahoo(symbol,start_date = datetime.date.today()-datetime.timedelta(days=365),end_date=datetime.date.today()):
    # Need to get the data that we will need to plot
    list_daily_bars=read_daily_bars(symbol,start_date,end_date)
    list_opens=get_list('Open',list_daily_bars)
    list_highs=get_list('High',list_daily_bars)
    list_lows=get_list('Low',list_daily_bars)
    list_closes=get_list('Close',list_daily_bars)
    list_string_dates=get_list('Date',list_daily_bars)
    # Want the dates as datetime objects
    list_datetime_dates=[]
    for i in range(len(list_string_dates)):
        list_datetime_dates.append(datetime.datetime.strptime(list_string_dates[i],'%Y-%m-%d'))

    # Creating the plot we will work with
    fig, ax = plt.subplots()
    mfinance.candlestick2_ohlc(ax, list_opens, list_highs, list_lows, list_closes,width=1)
    # Creating a function to tell the graph what to rename the x-axis values too
    def mydate(x,pos):
        try:
            return list_datetime_dates[-(int(x)+1)]
        except IndexError:
            return('')
    # Rename and organise the x-axis
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Candlestick plot for '+symbol)
    fig.autofmt_xdate()
    plt.show()




#print(analyse_recent_year("BCS"))
#plot_closes("ITVPF",datetime.date.today()-datetime.timedelta(days=365),datetime.date.today())
#plot_candlestick_with_yahoo('DIS')
#plot_candlestick_with_yahoo('DIS')