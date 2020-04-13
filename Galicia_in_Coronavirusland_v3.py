#!/usr/bin/env python3

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
# The data is only updated once or twice per day, so there is no need to rerunning it more often
# It formats and merges both sources
# It generates a two CSV files and two image files
# The CVS files contain chronological data of deaths per million.
# One contains deaths per million per day
# The other cumulative deaths per million
# The image files plot this data for the countries whose death rate is higher than Germany (included)
# Sorted from worst to best
# Each of the images is provided as PNG as SVG (vector, editable)
# The script is self-explanatory. Each subsection is illuminated
# It intents to be a minimalistic template that can be easily modified and recycled
# In its current state in enables comparing data from my country (Galicia)
# and the rest of the world. It gives some peace of mind to my friends who live abroad...
# REQUIREMENTS: Python 3 along with the following modules/libraries:
#    + Pandas, wget, datetime, matplotlib


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

galiza =  df2['CCAA'] == 'GA'
df2 = df2[galiza]

# We drop the information we are not going to use

#df2 = df2.drop(columns=['CCAA Codigo ISO', 'Casos ', 'Hospitalizados', 'UCI', 'Recuperados'])
df2.drop(df2.columns.difference(['FECHA','Fallecidos']), 1, inplace=True)

# We format the dates on the first collumn
# This requires the datetime python libraries

import datetime
df2['FECHA'] = pd.to_datetime(df2["FECHA"], infer_datetime_format=True)

# We change the column labels in order to make them consistent with the EU report (see below)

df2 = df2.rename(columns={"FECHA": "dateRep", "Fallecidos": "Galicia"})

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

# We create a new dataframe with population data (millions of habitants)

df4 = df[['countriesAndTerritories', 'popData2018']]
df4 = df4.drop_duplicates(subset='countriesAndTerritories', keep='first')
df4['popData2018'] = df4['popData2018'].truediv(1000000)

# We remove uninteresting columns 

#df = df.drop(columns=['day', 'month', 'year', 'cases', 'geoId', 'countryterritoryCode'])
df.drop(df.columns.difference(['dateRep','deaths','countriesAndTerritories']), 1, inplace=True)

# We reformat the dates Year-Month-Day (four digits year)

df['dateRep'] = pd.to_datetime(df["dateRep"], infer_datetime_format=True)

# We generate a list of consecutive dates from first death to last

def date_range(oldest, newest):
    r = (newest+datetime.timedelta(days=1)-oldest).days
    return [oldest+datetime.timedelta(days=i) for i in range(r)]
 
oldest = min(df['dateRep'])
newest = max(df['dateRep'])

dateList = date_range(oldest, newest)

# We split (group) the dataframe by country

grouped = df.groupby(df.countriesAndTerritories)

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

for index, row in df4.iterrows():
    country = row[0]
    permil = row[1]
    resultnc[country] = resultnc[country].truediv(permil)
    result[country] = result[country].truediv(permil)

# Finally, we merge the EU data and the Galician data

resultnc = resultnc.merge(df2nc, on='dateRep', how='outer')
resultnc.fillna(0, inplace=True)

result = result.merge(df2, on='dateRep', how='outer')
result.fillna(0, inplace=True)

# We drop the last lines if the Galician data is lagging
# behind the EU data by one day

lastnc = resultnc.iloc[-1]['Galicia']
if lastnc == 0:
    resultnc.drop(resultnc.tail(1).index,inplace=True)

#lastnc = resultnc.iloc[-1]['Galicia']
#if lastnc == 0:
#    resultnc.drop(resultnc.tail(1).index,inplace=True)
 
last = result.iloc[-1]['Galicia']
if last == 0:
    result.drop(result.tail(1).index,inplace=True)

#last = result.iloc[-1]['Galicia']
#if last == 0:
#    result.drop(result.tail(1).index,inplace=True)

# We save the formated CSV files
# It is very intuitive and easy to parse and plot

result.to_csv(cwd + '/Galicia_in_Coronavirusland.csv', index = False)
resultnc.to_csv(cwd + '/Galicia_in_Coronavirusland_absolute.csv', index = False)

#########################
#       PLOTTING        #
#########################

# List of protectorates and similar regions

protectorates = ['Cases_on_an_international_conveyance_Japan','San_Marino','Andorra','Sint_Maarten','Monaco','Guernsey','Turks_and_Caicos_islands','Gibraltar','Jersey','Liechtenstein','Guam','Northern_Mariana_Islands','Isle_of_Man','United_States_Virgin_Islands','Bermuda','Cayman_Islands','CuraÃ§ao']

##############
# CUMULATIVE #
##############

# We drop the first 50 days

result.drop(result.head(50).index,inplace=True) 

# We sort the columns (countries) on descending order according to the value of the most recent date

rown = result.tail(1).index.item()
scolumns = result.loc[:, result.columns != 'dateRep'].sort_values(by=rown, ascending=False, axis=1)
# We keep only the countries up to Germany

scolumns = scolumns.loc[:,:'Germany']

# We remove the "protectorates"

topcount = result[['dateRep']].copy()
for (country, columnData) in scolumns.iteritems():
    if country not in protectorates:
        topcount[country] = scolumns[country]

# We fill with zeros and reformat the date, just in case

topcount.fillna(0)
topcount['dateRep'] = pd.to_datetime(topcount["dateRep"], infer_datetime_format=True)

# We save the new dataframe as CSV

topcount.to_csv(cwd + '/Galicia_in_Coronavirusland_topcount.csv', index = False)

##########################################################################################

# The following two lines are required for the script to be run from crontab
# Otherwise plot() expects a display to be available

import matplotlib as mpl
mpl.use('Agg')

# Now we import matplotlib as usual

import matplotlib.pyplot as plt

ax = plt.gca()
ax.set_title('COVID-19 pandemic')
ax.set_ylabel('Cumulative deaths per million')

#Removing top and right borders

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# We are going to plot galicia differently from other countries

for country in topcount.columns[1:]:
	if country == 'Galicia':
		topcount.plot(kind='line',x='dateRep',y='Galicia',ax=ax,color='#1ce5e3',linewidth=5)
	else:
		topcount.plot(kind='line',x='dateRep',y=country,ax=ax,linewidth=3)
		
# We add a grid

plt.grid(b=True, which='major', color='#cccccc', linestyle='-', alpha=0.2)

# And place the legend outside of the plotting area 

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

# We save the plot in SVG (editable vectorial graph)
# and PNG formats

plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot_top.svg', bbox_inches='tight')
plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot_top.png', dpi=300, bbox_inches='tight')

#plt.show()
plt.close()

##############
#   DAILY    #
##############

# We drop the first 50 days

resultnc.drop(resultnc.head(50).index,inplace=True)

# Use the same columns (countries) as for the cumulative data

topcountc = resultnc[topcount.columns]

# We save the new dataframe as CSV

topcountc.to_csv(cwd + '/Galicia_in_Coronavirusland_topcount_noncumulative.csv', index = False)

##########################################################################################

ax = plt.gca()
ax.set_title('COVID-19 pandemic')
ax.set_ylabel('Daily deaths per million')

#Removing top and right borders

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# We are going to plot galicia differently from other countries

for country in topcountc.columns[1:]:
	if country == 'Galicia':
		topcountc.plot(kind='line',x='dateRep',y='Galicia',ax=ax,color='#1ce5e3',linewidth=5)
	else:
		topcountc.plot(kind='line',x='dateRep',y=country,ax=ax,linewidth=3)
		
# We add a grid

plt.grid(b=True, which='major', color='#cccccc', linestyle='-', alpha=0.2)

# And place the legend outside of the plotting area 

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

# We save the plot in SVG (editable vectorial graph)
# and PNG formats

plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot_top_noncumlative.svg', bbox_inches='tight')
plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot_top_noncumulative.png', dpi=300, bbox_inches='tight')

#plt.show()
plt.close()
