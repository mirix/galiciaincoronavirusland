#!/usr/bin/env python3

# By default, all the files will be downloaded to the folder from which this script will be executed
# If you want to change the destination folder, please, modify the value of the cwd variable below

import os
cwd = os.getcwd()

# This downloads a CSV file from the Instituto de Salud Carlos III (Spain)
# which contains information about each of the 17 so called "Autonomous Communities"
# This requires the wget Python module

import wget
urls = 'https://cnecovid.isciii.es/covid19/resources/agregados.csv'
if os.path.exists(cwd + '/COVID19_Spanish_cas_raw.csv'):
    os.remove(cwd + '/COVID19_Spanish_cas_raw.csv')
wget.download(urls, cwd + '/COVID19_Spanish_cas_raw.csv')

# We import the CSV data into a Pandas dataframe
# This requires Pandas

import pandas as pd
df2 = pd.read_csv(cwd + '/COVID19_Spanish_cas_raw.csv', encoding='iso-8859-1', sep=',').fillna(0)
df2.columns = df2.columns.str.strip('"')
df2['CCAA'] = df2['CCAA'].str.replace('"', '')
#df2 = df2.str.replace('NA', 0)
df2.drop(df2.columns.difference(['CCAA','FECHA','Fallecidos']), 1, inplace=True)
df2 = df2[['FECHA','CCAA','Fallecidos']]
casual =  df2['Fallecidos']!=0
df2 = df2[casual]

import datetime
df2['FECHA'] = pd.to_datetime(df2["FECHA"], dayfirst=True )

# We generate a list of consecutive dates from first death to last

def date_range(oldest, newest):
    r = (newest+datetime.timedelta(days=1)-oldest).days
    return [oldest+datetime.timedelta(days=i) for i in range(r)]
 
oldest = min(df2['FECHA'])
newest = max(df2['FECHA'])

dateList = date_range(oldest, newest)

df22 = pd.read_csv(cwd + '/spanish_regions.csv')
df22['Population'] = df22['Population'].truediv(1000000)

dictionary = pd.Series(df22.Region.values,index=df22.CCAA).to_dict()
df2 = df2.replace({"CCAA": dictionary})
#df2.to_csv(cwd + '/test.csv', index = False)

# We create a new dataframe by merging the groups
# The purpose of this is to create a new CSV file
# With dates as the first column
# Country names as column labels
# Number of deaths as the only data
# In case of doubt, refer to the CSV output

grouped = df2.groupby(df2.CCAA)

result=pd.DataFrame(dateList, columns=['FECHA'])
for name, group in grouped.groups.items():
    country = grouped.get_group(name)
    country = country.rename(columns={'Fallecidos': name})
    country = country.drop(columns=['CCAA'])
    result = result.merge(country, on='FECHA', how='outer')
result.fillna(0, inplace=True)

for index, row in df22.iterrows():
    country = row[1]
    permil = row[2]
    result[country] = result[country].truediv(permil)

result.fillna(0, inplace=True)

regions = df22['Region'].tolist()
regions.append("FECHA")
result = result[result.columns.intersection(regions)]
result = result.rename(columns={"FECHA": "dateRep"})

# PORTUGAL

df = pd.read_csv(cwd + '/Galicia_in_Coronavirusland_topcount.csv')
df['dateRep'] = pd.to_datetime(df["dateRep"], infer_datetime_format=True)
df = df[['dateRep','Portugal','Spain']]

result = result.merge(df, on='dateRep', how='left')

############

dates = result[['dateRep']].copy()
rown = result.tail(1).index.item()
resulto = result.loc[:, result.columns != 'dateRep'].sort_values(by=rown, ascending=False, axis=1)

resulto.insert(0, 'dateRep', dates)


###########3

resulto.to_csv(cwd + '/Iberia_in_Coronavirusland.csv', index = False)

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

for country in resulto.columns[1:]:
	if country == 'Galicia':
		resulto.plot(kind='line',x='dateRep',y='Galicia',ax=ax,color='#1ce5e3',linewidth=5)
	else:
		resulto.plot(kind='line',x='dateRep',y=country,ax=ax,linewidth=3)
		
# We add a grid

plt.grid(b=True, which='major', color='#cccccc', linestyle='-', alpha=0.2)

# And place the legend outside of the plotting area 

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

# We save the plot in SVG (editable vectorial graph)
# and PNG formats

plt.savefig(cwd + '/Iberia_in_Coronavirusland.svg', bbox_inches='tight')
plt.savefig(cwd + '/Iberia_in_Coronavirusland.png', dpi=300, bbox_inches='tight')

#plt.show()
plt.close()
