
import pandas as pd
from google.cloud import storage
from io import StringIO

def readfilefrombucket(bucketname, destinationblobname):
    
    # connect to cloud storage
    # download file and read into data frame
 
    storageclient = storage.Client()
    bucket = storageclient.bucket(bucketname)
    blob = bucket.blob(destinationblobname)
    blob = blob.download_as_string()
    blob = blob.decode('utf-8')
    blob = StringIO(blob)  #transform bytes to string here
    df = pd.read_csv(blob) #read blob into dataframe
    return df


def createdf(dfAll):

    # prepare dataset
    
    df = pd.DataFrame(dfAll, columns= ['process','responsetimeorcount']) #create subset df with two columns
    df = df.query('process.str.contains("Response Time")') #filter df to have just "response time" data
    df['process'] = df['process'].str.slice(0, 8) # truncate the process string to display
    dfmeanprocess = df.groupby('process').responsetimeorcount.mean().reset_index()  #group and mean by unique process 
    dfmeanprocess['id'] = range(0, 0+len(dfmeanprocess)) # add new column id
    print(dfmeanprocess)
    return dfmeanprocess


def barchartvalue(ppbar, axval):
    
    #height is value on top of bar
    
    for p in ppbar:
        height = p.get_height()
        axval.annotate('{}'.format(round(height,1)),
            xy=(p.get_x() + p.get_width() / 2, height),
            xytext=(0, 3), # 3 points vertical offset
            textcoords="offset points",
            size=5.5,
            ha='center', va='bottom',
            )