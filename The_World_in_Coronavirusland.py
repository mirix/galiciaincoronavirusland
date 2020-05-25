#!/usr/bin/env python3

import os
cwd = os.getcwd()

import wget

import pandas as pd

import datetime

# This downloads a CSV file from the European Centre for Disease Prevention and Control (ECDC)
# It requires Python wget

url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/'
if os.path.exists(cwd + '/COVID19_worldwide_raw.csv'):
    os.remove(cwd + '/COVID19_worldwide_raw.csv')
wget.download(url, cwd + '/COVID19_worldwide_raw.csv')

# We import the data from the CSV file into a Pandas dataframe
# It requires Pandas

#from pandas import read_excel
#file_name = cwd + '/COVID19_worldwide_raw.xlsx'
#df = read_excel(file_name, sheet_name=0)
#df = df.rename(columns={"https://www.ecdc.europa.eu/en/novel-coronavirus-china/sources-updated": "dateRep"})

df = pd.read_csv(cwd + '/COVID19_worldwide_raw.csv', sep=',').fillna(0)

# Remove protectorates
protectorates = ['Cases_on_an_international_conveyance_Japan','San_Marino','Andorra','Sint_Maarten','Monaco','Guernsey','Turks_and_Caicos_islands','Gibraltar','Jersey','Liechtenstein','Guam','Northern_Mariana_Islands','Isle_of_Man','United_States_Virgin_Islands','Bermuda','Cayman_Islands','CuraÃ§ao']
df = df[~df.countriesAndTerritories.isin(protectorates)]

# We are only interest in deaths
# We discard the rest

casual =  df['deaths']!=0
df = df[casual]

# We remove uninteresting columns 

#df = df.drop(columns=['day', 'month', 'year', 'cases', 'geoId', 'countryterritoryCode'])
df.drop(df.columns.difference(['dateRep','deaths','countryterritoryCode','popData2018']), 1, inplace=True)

# We reformat the dates Year-Month-Day (four digits year)

df['dateRep'] = pd.to_datetime(df["dateRep"], infer_datetime_format=True)

# We split (group) the dataframe by country

df.fillna(0, inplace=True)
df = df.iloc[::-1]
df['cumsum'] = df.groupby('countryterritoryCode')['deaths'].transform(pd.Series.cumsum)

result = df.groupby('countryterritoryCode').tail(1).copy()

result['popData2018'] = result['popData2018'].truediv(1000000)
result['drate'] = result['cumsum']/result['popData2018']

result.drop(result.columns.difference(['countryterritoryCode','drate']), 1, inplace=True)
result = result[result.countryterritoryCode != 0]

# Import latitude and longitude

df2 = pd.read_csv(cwd + '/country_codes_and_coordinates.csv')

result = result.merge(df2, on='countryterritoryCode', how='left')

result = result.dropna()

result.drate = result.drate.round().astype(int)

result.to_csv(cwd + '/World_in_Coronavirusland.csv', index = False)

# PLOT MAP

pink = ['DEU','BGD','NZL','NOR','DNK','ISL','BEL','BRB','SRB','FIN','MMR','TWN','BOL']

import folium

world_geo = os.path.join(cwd , 'world-countries.json')
 
world_data = pd.read_csv(cwd + '/World_in_Coronavirusland.csv')

world_data.drate = world_data.drate.round().astype(int)
 
# Initialize the map:
m = folium.Map(location=[20, 0], zoom_start=3)
 
# Add the color for the chloropleth:
folium.Choropleth(
	geo_data=world_geo,
	name='choropleth',
	data=world_data,
	columns=['countryterritoryCode', 'drate'],
	key_on='feature.id',
	nan_fill_color='#F5F5F5',
	fill_color='YlOrRd',
	bins=9,
	fill_opacity=0.8,
	line_opacity=0.2,
	legend_name='COVID-19 Deaths per Million'
).add_to(m)

for i in range(0,len(result)):
	if world_data.iloc[i]['countryterritoryCode'] in pink :
		folium.Marker([world_data.iloc[i]['lat'], world_data.iloc[i]['lon']], popup=world_data.iloc[i]['drate'], icon=folium.Icon(icon='cloud', color='purple')).add_to(m)
	else :
		folium.Marker([world_data.iloc[i]['lat'], world_data.iloc[i]['lon']], popup=world_data.iloc[i]['drate'], icon=folium.Icon(icon='cloud', color='blue')).add_to(m)

# Save to html
m.save('COVID19_World_Map_Deaths_per_Million.html')
