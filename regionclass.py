import pandas as pd
import numpy as np
from datetime import datetime

class Region(object):
    """
    Class for creating csv file datasets for 
    each region in LA. 
    """

    def __init__(self):
        """
        Constructor for Region Class
        """
        self.arrests = pd.DataFrame() #Arrests
        self.vehped = pd.DataFrame()  #Vehicle and Pedestrian Stops
        self.crimes = pd.DataFrame()  #Crimes
        self.sr = pd.DataFrame()      #Service Requests
        self.srt = pd.DataFrame()     #Service Request Types
    
    def convert(self, string):
        """
        Converts date and time string to datetime object. 
        """
        date = datetime.strptime(string[:10],'%m/%d/%Y')   
        return date
   
    def regarrests(self, csv, regionid):
        """
        Returns dataframe which displays the total number of arrests in inputted region  
        per day, every day since January 1st, 2017 until December 31, 2019.  
        Data: https://data.lacity.org/A-Safe-City/Arrest-Data-from-2010-to-Present/yru6-6re4/data
        """

        #Read csv file and create dataframe
        df = pd.read_csv(csv)  
        
        #Filter dataframe to only include arrests from region inputted into function, and convert dates of arrests to datetime objects using convert function. 
        df = df[df['Area ID'] == regionid] 
        df['Converted Dates'] = df['Arrest Date'].apply(self.convert, 0)
        
        #Filter dataframe to only include dates between 1/1/2017 and 12/31/2019
        start_date = datetime.strptime('1/1/2017','%m/%d/%Y') 
        end_date = datetime.strptime('12/31/2019','%m/%d/%Y')      
        df = df[(df['Converted Dates'] >= start_date) & (df['Converted Dates'] <= end_date)]  

        #Creates dataframe with dates and arrest counts per date 
        datecounts = pd.DataFrame(columns = ['Date', 'Arrests'])   
        unique_elements, counts_elements = np.unique(df['Converted Dates'], return_counts = True) 
        datecounts['Date'] = unique_elements 
        datecounts['Arrests'] = counts_elements  
        
        #Checks for dates which are not present in the dataframe and assigns arrest count to 0. 
        idx = pd.date_range(start_date, end_date) 
        s = pd.Series(datecounts['Arrests'])
        s.index = datecounts['Date']
        s = s.reindex(idx, fill_value = 0) 
        datecounts = pd.DataFrame({'Date':s.index, 'Arrests':s.values})
        
        #Returns dataframe sorted by chronological order
        return datecounts.sort_values(by = 'Date') 
    
    def regvehstops(self, csv, region):
        """ 
        Reads csv file and returns dataframe which displays total number of
        vehicle stops in specified region for every day between January 1st, 2017 and December 31, 2019. 
        """

        #Read csv file and create dataframe filtered by region
        df = pd.read_csv(csv)
        df = df[(df['Division Description 1'] == region) & (df['Stop Type'] == 'VEH')] 
        df['Converted Dates'] = df['Stop Date'].apply(self.convert, 0)

        #Filters dataframe to only include dates between start and end dates
        start_date = datetime.strptime('1/1/2017','%m/%d/%Y') 
        end_date = datetime.strptime('12/31/2019','%m/%d/%Y') 
        df = df[(df['Converted Dates'] >= start_date) & (df['Converted Dates'] <= end_date)] 
        
        #Creates dataframe with dates and vehicle stop counts per date 
        datecounts = pd.DataFrame(columns = ['Date', 'Number of Vehicle Stops'])
        unique_elements, counts_elements = np.unique(df['Converted Dates'], return_counts = True)
        datecounts['Date'] = unique_elements
        datecounts['Number of Vehicle Stops'] = counts_elements
        
        #Checks for dates which are not present in the dataframe and assigns corresponding count to 0. 
        idx = pd.date_range(start_date, end_date) 
        s = pd.Series(datecounts['Number of Vehicle Stops'])
        s.index = datecounts['Date']
        s = s.reindex(idx, fill_value = 0) 
        datecounts = pd.DataFrame({'Date':s.index, 'Number of Vehicle Stops':s.values})
        
        return datecounts

    def regpedstops(self, csv, region):
        """ 
        Reads csv file and returns dataframe which displays total number of
        pedestrian stops in Hollywood for every day between January 1st, 2017 and December 31, 2019. 
        """

        #Read csv file and create dataframe filtered by region
        df = pd.read_csv(csv)
        df = df[(df['Division Description 1'] == region) & (df['Stop Type'] == 'PED')] #Filters dataframe to only include Hollywood pedestrian stops. 
        df['Converted Dates'] = df['Stop Date'].apply(self.convert, 0)
        
        #Filters dataframe to only include dates between start and end dates
        start_date = datetime.strptime('1/1/2017','%m/%d/%Y')  
        end_date = datetime.strptime('12/31/2019','%m/%d/%Y') 
        df = df[(df['Converted Dates'] >= start_date) & (df['Converted Dates'] <= end_date)]  

        #Creates dataframe with dates and pedestrian stop counts per date 
        datecounts = pd.DataFrame(columns = ['Date', 'Number of Pedestrian Stops'])
        unique_elements, counts_elements = np.unique(df['Converted Dates'], return_counts = True)
        datecounts['Date'] = unique_elements
        datecounts['Number of Pedestrian Stops'] = counts_elements
    
        #Checks for dates which are not present in the dataframe and assigns corresponding count to 0. 
        idx = pd.date_range(start_date, end_date) 
        s = pd.Series(datecounts['Number of Pedestrian Stops'])
        s.index = datecounts['Date']
        s = s.reindex(idx, fill_value = 0) 
        datecounts = pd.DataFrame({'Date':s.index, 'Number of Pedestrian Stops':s.values})
        
        return datecounts
    
    def combinevp(self, csv, region):
        """
        Creates combined dataframe for vehicle and pedestrian counts
        in specified region.
        Data: https://data.lacity.org/A-Safe-City/Vehicle-and-Pedestrian-Stop-Data-2010-to-Present/ci25-wgt7/data
        Note: Make sure to filter data to only include pedestrian and vehicle stops between 2017 and 2019, otherwise 
        you won't be able to download the dataset properly!
        """
        #Create dataframes with for vehicle stop counts and pedestrian stop counts
        peddf = self.regpedstops(csv, region) 
        vehdf = self.regvehstops(csv, region)

        #Adds vehicle stop counts to pedestrian stop counts dataframe and returns that dataframe
        peddf['Number of Vehicle Stops'] = vehdf['Number of Vehicle Stops'] 
        
        return peddf 
    
    def regcrimes(self, csv, regionid):
        """ 
        Reads csv file and returns dataframe which displays total number of
        crimes committed in specified region for every day between January 1st, 2017 and December 31, 2019. 
        Data: https://data.lacity.org/A-Safe-City/Crime-Data-from-2010-to-2019/63jg-8b9z/data
        """
        
        #Read csv file and create dataframe filtered by specified region (Use self.convertcrime!)
        df = pd.read_csv(csv)
        df = df[df['AREA '] == regionid]  
        df['Converted Dates'] = df['DATE OCC'].apply(self.convert, 0)
        
        #Filters dataframe to only include dates between start and end dates
        start_date = datetime.strptime('1/1/2017','%m/%d/%Y') 
        end_date = datetime.strptime('12/31/2019','%m/%d/%Y') 
        df = df[(df['Converted Dates'] >= start_date) & (df['Converted Dates'] <= end_date)]  
        
        #Creates dataframe with dates and pedestrian stop counts per date 
        datecounts = pd.DataFrame(columns = ['Date', 'Number of Crimes Committed'])
        unique_elements, counts_elements = np.unique(df['Converted Dates'], return_counts = True)
        datecounts['Date'] = unique_elements
        datecounts['Number of Crimes Committed'] = counts_elements
        
        #Checks for dates which are not present in the dataframe and assigns corresponding count to 0. 
        idx = pd.date_range(start_date, end_date) 
        s = pd.Series(datecounts['Number of Crimes Committed'])
        s.index = datecounts['Date']
        s = s.reindex(idx, fill_value=0) 
        datecounts = pd.DataFrame({'Date':s.index, 'Number of Crimes Committed':s.values})
        
        return datecounts
    
    def totalsr(self, csv, region):
        """ 
        Reads csv file and returns dataframe which displays total number of service requests
        per date in specified region for every day between 2017 and 2019. 
        """

        #Read csv file and create dataframe filtered by region
        df = pd.read_csv(csv)
        df = df[df['PolicePrecinct'] == region] 
        df['Converted Dates'] = df['CreatedDate'].apply(self.convert, 0) 

        #Creates dataframe with dates and service request counts per date 
        datecounts = pd.DataFrame(columns = ['Date', 'Service Requests'])
        unique_elements, counts_elements = np.unique(df['Converted Dates'], return_counts = True)
        datecounts['Date'] = unique_elements
        datecounts['Service Requests'] = counts_elements
    
        #Checks for dates which are not present in the dataframe and assigns corresponding count to 0. 
        start_date = datetime.strptime('1/1/2017','%m/%d/%Y')  
        end_date = datetime.strptime('12/31/2019','%m/%d/%Y') 
        
        idx = pd.date_range(start_date, end_date) 
        s = pd.Series(datecounts['Service Requests'])
        s.index = datecounts['Date']
        s = s.reindex(idx, fill_value = 0) 
        datecounts = pd.DataFrame({'Date':s.index, 'Service Requests':s.values})
        
        return datecounts
    
    def srthelper(self, df, date, cols):
        """ 
        Helper function for stypes. 
        """

        t = df[df['Converted Dates'] == date]['RequestType']
        unique_elements, counts_elements = np.unique(t, return_counts = True)
        s = pd.Series(counts_elements)
        s.index = unique_elements
        s = s.reindex(cols, fill_value = 0)
        
        return s.values
       
    def srtypes(self, csv, region):
        """
        Returns dataframe which displays number of times each of the 
        12 service request types were request per day in specified region, for 
        every day between 2017 and 2019. 
        """
        
        #Read csv file and add Converted Dates column
        df = pd.read_csv(csv)
        df['Converted Dates'] = df['CreatedDate'].apply(self.convert, 0)
        
        #Create empty datecounts dataframe
        dates = np.unique(df['Converted Dates'])
        cols = np.unique(df['RequestType'])
        datecounts = pd.DataFrame(pd.np.empty((1095, 12))).set_index(dates)
        datecounts.columns = cols
        
        #Filters dataframe by region
        df = df[df['PolicePrecinct'] == region]
        
        #Apply helper function to all dates and add results to datecounts
        for index, row in datecounts.iterrows():
            datecounts.loc[index] = self.srthelper(df, index, cols)
        
        return datecounts
    
    def create(self, arrestcsv, vehpedcsv, crimecsv, srcsv, regionid, region):
        """
        Combines all data into one dataframe. 
        """

        self.arrests = self.regarrests(arrestcsv, regionid)
        self.vehped = self.combinevp(vehpedcsv, region)
        self.crimes = self.regcrimes(crimecsv, regionid)
        self.sr = self.totalsr(srcsv, region)
        self.srt = self.srtypes(srcsv, region)

        finaldf = self.arrests

        finaldf['Vehicle Stops'] = self.vehped['Number of Vehicle Stops']
        finaldf['Pedestrian Stops'] = self.vehped['Number of Pedestrian Stops']
        finaldf['Crimes Committed'] = self.crimes['Number of Crimes Committed']
        finaldf['Service Requests'] = self.sr['Service Requests']
        finaldf = pd.concat([finaldf.reset_index(drop=True),self.srt.reset_index(drop = True)], axis=1)

        return finaldf


REG = Region()
REG.create('arrestdata.csv', 'vehped.csv', 'lacrimes.csv', 'allservice.csv', regionid, region)


#Regionid and Regions
"""
1, 'CENTRAL'  
2, 'RAMPART' 
3, 'SOUTH WEST'
4, 'HOLLENBECK'
5, 'HARBOR'
6, 'HOLLYWOOD'
7, 'WILSHIRE'
8, 'WEST LA'
9, 'VAN NUYS' 
10, 'WEST VALLEY'
11, 'NORTH EAST'
12, 'SEVENTY-SEVENTH'
13, 'NEWTON'
14, 'PACIFIC'
15, 'NORTH HOLLYWOOD'
16, 'FOOTHILL'
17, 'DEVONSHIRE'
18, 'SOUTH EAST'
19, 'MISSION'
20, 'OLYMPIC'
21, 'TOPANGA'
"""


