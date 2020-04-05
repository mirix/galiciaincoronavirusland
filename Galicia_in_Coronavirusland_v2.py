#!/usr/bin/python3.6

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#    AUTHOR: Edelmiro Moman 2020, miromoman@gmail.com
#    https://sentidinho.eu/sentidinho/galicia-in-coronavirusland/

###############################
#          READ ME            #
###############################
# This Python script downloads COVID-19 data from two different sources (labelled as "raw"):
#    + Information about the Spanish Autonomous Communities from the Spanish Ministry of Health
#    + Worldwide information from the European Centre for Disease Prevention and Control (ECDC)
# The data is only updated once or twice per day, so there is no need in rerunning this more often
# It keeps only deceases data
# It converts it to cumulative format (per day)
# And to relative figures (deaths per million inhabitants)
# It formats and merges both sources
# It generates a new CSV file and two image files
# The script is self-explanatory. Each subsection is illuminated
# It intents to be a minimalistic template that can be easily modified and recycled
# In its current state in enables comparing data from my country (Galicia)
# and the rest of the world. It gives some peace of mind to my friends who live abroad...
# REQUIREMENTS: Python 3 along with the following modules/libraries:
#    + Pandas, wget, datetime


# By default, all the files will be downloaded to the folder from which this script will be executed
# If you want to change the destination folder, please, modify the value of the cwd variable below

import os
cwd = os.getcwd()

# This downloads a CSV file from the Instituto de Salud Carlos III (Spain)
# which contains information about each of the 17 so called "Autonomous Communities"
# This requires the wget Python module

import wget
urls = 'https://covid19.isciii.es/resources/serie_historica_acumulados.csv'
if os.path.exists(cwd + '/COVID19_Spanish_cas_raw.csv'):
    os.remove(cwd + '/COVID19_Spanish_cas_raw.csv')
wget.download(urls, cwd + '/COVID19_Spanish_cas_raw.csv')

# We import the CSV data into a Pandas dataframe
# This requires Pandas

import pandas as pd
df2 = pd.read_csv(cwd + '/COVID19_Spanish_cas_raw.csv', encoding='iso-8859-1').fillna(0)

# We extract the information pertaining our country, Galicia
# If you are interested in a different dataset
# look into the CSV file and modify this template accordingly

galiza =  df2['CCAA Codigo ISO'] == 'GA'
df2 = df2[galiza]

# We drop the information we are not going to use

df2 = df2.drop(columns=['CCAA Codigo ISO', 'Casos ', 'Hospitalizados', 'UCI', 'Recuperados'])

# We format the dates on the first collumn
# This requires the datetime python libraries

import datetime
df2['Fecha'] = pd.to_datetime(df2["Fecha"], infer_datetime_format=True)

# We change the column labels in order to make them consistent with the EU report (see below)

df2 = df2.rename(columns={"Fecha": "dateRep", "Fallecidos": "Galicia"})

# We convert cumulative to absolute values

df2nc = df2.copy()
df2nc['Galicia'] = df2nc['Galicia'].diff()

# In this dataset we are keeping only the number of deaths
# They are provided as absolute cumulative figures
# We convert them to relative figures (deaths per million inhabitants)

df2nc['Galicia'] = df2nc['Galicia'].truediv(2.701743)

df2['Galicia'] = df2['Galicia'].truediv(2.701743)

# This downloads an Excel file from the European Centre for Disease Prevention and Control (ECDC)
# It requires Python wget

url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
if os.path.exists(cwd + '/COVID19_worldwide_raw.xlsx'):
    os.remove(cwd + '/COVID19_worldwide_raw.xlsx')
wget.download(url, cwd + '/COVID19_worldwide_raw.xlsx')

# We import the data from the Excel file into a Pandas dataframe
# It requires Pandas

from pandas import read_excel
file_name = cwd + '/COVID19_worldwide_raw.xlsx'
df = read_excel(file_name, sheet_name=0)

# We are only interest in deaths
# We discard the rest

casual =  df['deaths']!=0
df = df[casual]
df = df.drop(columns=['day', 'month', 'year', 'cases', 'geoId', 'countryterritoryCode'])

# We reformat the dates Year-Month-Day (four digits year)

df['dateRep'] = pd.to_datetime(df["dateRep"], infer_datetime_format=True)

# We generate a list of consecutive dates from first death to last

def date_range(oldest, newest):
    r = (newest+datetime.timedelta(days=1)-oldest).days
    return [oldest+datetime.timedelta(days=i) for i in range(r)]
 
oldest = min(df['dateRep'])
newest = max(df['dateRep'])

dateList = date_range(oldest, newest)

# We remove the country population data
# We could have done it before, this was an afterthought
# We will keep it this way in case we change our minds 

df3 = df.drop(columns=['popData2018'])

# We split (group) the dataframe by country

grouped = df3.groupby(df.countriesAndTerritories)

# We create a new dataframe by merging the groups
# The purpose of this is to create a new CSV file
# With dates as the first column
# Country names as column labels
# Number of deaths as the only data
# In case of doubt, refer to the CSV output

result=pd.DataFrame(dateList, columns=['dateRep'])
for name, group in grouped.groups.items():
    country = grouped.get_group(name)
    country = country.rename(columns={'deaths': name})
    country = country.drop(columns=['countriesAndTerritories'])
    result = result.merge(country, on='dateRep', how='outer')
result.fillna(0, inplace=True)

# The data from the EU is per day, not cumulative
# We make it cumulative

resultnc = result.copy()
result.loc[:, result.columns != 'dateRep'] = result.loc[:, result.columns != 'dateRep'].cumsum()

# Now we are going to covert the absolute values 
# into relative ones (deaths per million)

df4 = df[['countriesAndTerritories', 'popData2018']]
df4 = df4.drop_duplicates(subset='countriesAndTerritories', keep='first')
df4['popData2018'] = df4['popData2018'].truediv(1000000)

for index, row in df4.iterrows():
    country = row[0]
    permil = row[1]
    resultnc[country] = resultnc[country].truediv(permil)

for index, row in df4.iterrows():
    country = row[0]
    permil = row[1]
    result[country] = result[country].truediv(permil)

# Finally, we merge the EU data and the Galician data

resultnc = resultnc.merge(df2nc, on='dateRep', how='outer')
resultnc.fillna(0, inplace=True)

result = result.merge(df2, on='dateRep', how='outer')
result.fillna(0, inplace=True)

# We drop the last lines if the Galician data is lagging
# behind the EU data by one or two days

lastnc = resultnc.iloc[-1]['Galicia']
if lastnc == 0:
    resultnc.drop(resultnc.tail(1).index,inplace=True)

lastnc = resultnc.iloc[-1]['Galicia']
if lastnc == 0:
    resultnc.drop(resultnc.tail(1).index,inplace=True)
 
last = result.iloc[-1]['Galicia']
if last == 0:
    result.drop(result.tail(1).index,inplace=True)

last = result.iloc[-1]['Galicia']
if last == 0:
    result.drop(result.tail(1).index,inplace=True)

# We save the formated CSV files
# It is very intuitive and easy to parse and plot

result.to_csv(cwd + '/Galicia_in_Coronavirusland.csv', index = False)
resultnc.to_csv(cwd + '/Galicia_in_Coronavirusland_absolute.csv', index = False)
