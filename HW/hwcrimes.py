def convert(string):
    """Converts from string to datetime
    """
    date = datetime.strptime(string[:10],'%m/%d/%Y') #Accepts date string, converts it to datetime object. 
    return date


def hwcrimes(csv):
    """ 
    Reads csv file and returns dataframe which displays total number of
    crimes committed in Hollywood for every day between January 1st, 2017 and December 31, 2019. 
    Data: https://data.lacity.org/A-Safe-City/Crime-Data-from-2010-to-2019/63jg-8b9z/data
    """
    
    df = pd.read_csv(csv)
    hdf = df[df['AREA '] == 6] #Filters dataframe to only include Hollywood pedestrian stops. 
    hdf['Converted Dates'] = hdf['DATE OCC'].apply(convert, 0)
    
    
    
    start_date = datetime.strptime('1/1/2017','%m/%d/%Y') #Sets start date for filter
    end_date = datetime.strptime('12/31/2019','%m/%d/%Y') # Sets end date for filter
    
    
    
    hdf = hdf[(hdf['Converted Dates'] >= start_date) & (hdf['Converted Dates'] <= end_date)] #Filters hdf to only include relevant dates
    
    
    datecounts = pd.DataFrame(columns = ['Date', 'Number of Crimes Committed'])
    dateray = np.array(hdf['Converted Dates'])
    unique_elements, counts_elements = np.unique(dateray, return_counts = True)
    
    datecounts['Date'] = unique_elements
    datecounts['Number of Crimes Committed'] = counts_elements
    
    return datecounts