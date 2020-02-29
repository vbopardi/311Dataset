import numpy as np 
import pandas as pd 
from datetime import datetime

def convert(string):
    """Converts from string to datetime
    """
    date = datetime.strptime(string,'%m/%d/%Y') #Accepts date string, converts it to datetime object. 
    return date


def hwvehstops(csv):
    """ 
    Reads csv file and returns dataframe which displays total number of
    vehicle stops in Hollywood for every day between January 1st, 2017 and December 31, 2019. 
    """
    
    df = pd.read_csv(csv)
    hdf = df[(df['Division Description 1'] == 'HOLLYWOOD') & (df['Stop Type'] == 'VEH')] #Filters dataframe to only include Hollywood pedestrian stops. 
    hdf['Converted Dates'] = hdf['Stop Date'].apply(convert, 0)
    
    
    
    start_date = datetime.strptime('1/1/2017','%m/%d/%Y') #Sets start date for filter
    end_date = datetime.strptime('12/31/2019','%m/%d/%Y') # Sets end date for filter
    
    hdf = hdf[(hdf['Converted Dates'] >= start_date) & (hdf['Converted Dates'] <= end_date)] #Filters hdf to only include relevant dates
   
    datecounts = pd.DataFrame(columns = ['Date', 'Number of Vehicle Stops'])
    dateray = np.array(hdf['Converted Dates'])
    unique_elements, counts_elements = np.unique(dateray, return_counts = True)
    
    datecounts['Date'] = unique_elements
    datecounts['Number of Vehicle Stops'] = counts_elements
    
    return datecounts
