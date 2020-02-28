import pandas as pd 
import numpy as np 
from datetime import datetime

def convert(string):
    """Converts a string to a datetime object.
    """
    date = datetime.strptime(string,'%m/%d/%Y') #Accepts date string, converts it to datetime object. 
    return date


def hwarrests(csv):
    """
    Accepts csv file and returns dataframe which displays the total number of arrests in Hollywood per 
    day, every day from January 1st, 2017 to December 31, 2019.
    
    Data: https://data.lacity.org/A-Safe-City/Arrest-Data-from-2010-to-Present/yru6-6re4
    """
    
    df = pd.read_csv(csv) #Reads csv file and forms a new dataframe 
    
    hdf = df[df['Area ID'] == 6] #Filters dataframe to only include date from Hollywood. 
    hdf['Converted Dates'] = hdf['Arrest Date'].apply(convert, 0) #Applies convert function to all dates in 'Arrest Date Column', and places those dates in new column called 'Converted Dates'
    
    
    
    start_date = datetime.strptime('1/1/2017','%m/%d/%Y') #Sets start date for filter
    end_date = datetime.strptime('12/31/2019','%m/%d/%Y') # Sets end date for filter 
    
    hdf = hdf[(hdf['Converted Dates'] >= start_date) & (hdf['Converted Dates'] <= end_date)] #Filters hdf to only include dates between start and end dates. 

    
    datecounts = pd.DataFrame(columns = ['Date', 'Number of Arrests']) #Creates empty dataframe with dates and number of arrests as columns
    dateray = np.array(hdf['Converted Dates'])  #Creates array of arrest dates in hdf
    
    unique_elements, counts_elements = np.unique(dateray, return_counts=True) #Returns two arrays with (1) unique dates and (2) number of arrests for those dates
    
    datecounts['Date'] = unique_elements #Sets array for unique dates to 'Date' in datecounts
    datecounts['Number of Arrests'] = counts_elements #sets array for arrest counts per date to 'Number of Arrest' in datecounts
    
    return datecounts.sort_values(by = 'Date') #Returns datecounts dataframe sorted by chronological order
