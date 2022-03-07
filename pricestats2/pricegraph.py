import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import requests
import io
from util import access_secret_version

def plotgraph(formdata):
   
   #plot graph using symbol and days values passed in this method
          
    stock = formdata.get('symbol') #user selected from dropdown
    N = int(formdata.get('days'))
   
    # get apikey from Secret Manager
    apikey = access_secret_version('pricestats', 'apikey', '1')
    
    #alpha vantage URL link
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={apikey}'
    
    # fetch price data
    r = requests.get(url)
    data = r.json()
    
    # convert to dataframe
    df = pd.DataFrame(data["Time Series (Daily)"])
    df1 = df.head(10)
    # tranpose datframe to have "Open", "High", "Low", "Close" and "Volume" columns 
    dft = df1.T  # Transpose Dataframe for desired results

    dft.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    # force all values to numeric
    dft['Open'] = pd.to_numeric(dft['Open'], errors='coerce')
    dft['Close'] = pd.to_numeric(dft['Close'], errors='coerce')
    dft['High'] = pd.to_numeric(dft['High'], errors='coerce')
    dft['Low'] = pd.to_numeric(dft['Low'], errors='coerce')
   
    #truncate the data to last N days. Where N days is provided by user
    dft = dft[:N]
    
    #reverse DataFrame - day 1 should be first row and day N as last row
    #example 
    # #2021-11-29 ... 
    # #2021-11-30 ... 
    # #2021-12-01 .... 
    # etc
    dft = dft.iloc[::-1]
    
    #create fig and axis plot    
    fig, ax = plt.subplots()
    
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    # Loop through a range of 4 and create plots for High, Low, Open and Close
    for i in range(0,4):
        ax.set_title(f'{stock} Daily Data - Last {N} days')
        if i == 0:
           p1, = ax.plot(dft.index, dft['High'], color='red', marker='o', label='High')
        elif i == 1:
           p2, = ax.plot(dft.index, dft['Low'], color='blue',marker='o', label='Low')  
        elif i == 2:
           p3 = ax.scatter(dft.index, dft['Open'], color='green',marker='^', label='Open')  
        elif i == 3:
           p4 = ax.scatter(dft.index, dft['Close'], color='gold',marker='^', label='Close') 
        
    ax.set_ylabel('Price')
    ax.set_xlabel('Days')
    ax.legend(handles=[p1, p2, p3, p4]) #provide legend
    
    #save fig as jpeg format
    fig.savefig('pricestate',
            format='jpeg',
            dpi=100,
            bbox_inches='tight')
    
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_jpeg(output) #print fig to output
    
    return output