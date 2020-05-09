#!/usr/bin/env python3

import pandas as pd

import os
cwd = os.getcwd()

# SPAIN

# Corona

link = "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Spain"
df_es = pd.read_html(link, header=0)[3]

df_es = df_es.rename(columns={'Community':'Region'})
df_es = df_es[['Region', 'Deaths']]
df_es.drop(df_es.tail(1).index,inplace=True)

df_es['Region'] = df_es['Region'].str.replace(" \(article\)", "") 
df_es['Region'] = df_es['Region'].str.replace("Castilla–La Mancha", "Castile-La Mancha") 
df_es['Region'] = df_es['Region'].str.replace("Castile and León", "Castile-Leon")
df_es['Region'] = df_es['Region'].str.replace("Community of Madrid", "Madrid")
df_es['Region'] = df_es['Region'].str.replace("Valencian Community", "Valencia")

# Nuts

link = "https://en.wikipedia.org/wiki/NUTS_statistical_regions_of_Spain"
df_nuts = pd.read_html(link, header=0)[1]

df_nuts = df_nuts.iloc[:, [2, 3]]
df_nuts = df_nuts.rename(columns={'NUTS 2':'Region'})

df_nuts['Region'] = df_nuts['Region'].str.replace("Basque Community", "Basque Country") 
df_nuts['Region'] = df_nuts['Region'].str.replace("Principality of Asturias", "Asturias") 
df_nuts['Region'] = df_nuts['Region'].str.replace("Valencian Community", "Valencia") 
df_nuts['Region'] = df_nuts['Region'].str.replace("Region of Murcia", "Murcia") 

df_nuts = df_nuts.drop_duplicates()

# Merge

#df_es = df_es.merge(df_nuts, on=['Region'], how='right')

# Merge

import fuzzymatcher

df_es = fuzzymatcher.fuzzy_left_join(df_nuts, df_es, left_on = "Region", right_on = "Region")
df_es = df_es.rename(columns={'Region_right':'Region'})
df_es = df_es[['Code.1', 'Region', 'Deaths']]

# PORTUGAL

# Corona

link = "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Portugal"
df_pt = pd.read_html(link, header=0)[3]
df_pt.drop(df_pt.tail(1).index,inplace=True)
df_pt = df_pt.tail(2)
df_pt = df_pt.reset_index()

df_pt = df_pt.transpose()

df_pt.drop(df_pt.head(2).index,inplace=True)
df_pt.drop(df_pt.tail(10).index,inplace=True)

df_pt = df_pt[df_pt.columns[::-1]]

df_pt = df_pt.rename(columns={1:'Region', 0:'Deaths'})
df_pt['Region'] = df_pt['Region'].str.replace("Lisbon andTagus Valley", "Lisboa")
df_pt['Region'] = df_pt['Region'].str.replace("North", "Norte")
df_pt['Region'] = df_pt['Region'].str.replace("Center", "Centro")
df_pt['Region'] = df_pt['Region'].str.replace("Azores", "Açores")

#df_pt.to_csv("Portugal.csv", sep=',', index=False)

# Nuts

link = "https://en.wikipedia.org/wiki/NUTS_statistical_regions_of_Portugal"
df_nuts = pd.read_html(link, header=0)[1]

df_nuts = df_nuts.iloc[: , [2, 3]]
df_nuts = df_nuts[df_nuts.columns[::-1]]
df_nuts = df_nuts.rename(columns={'NUTS 2':'Region'})

df_nuts['Region'] = df_nuts['Region'].str.replace("Área Metropolitana de Lisboa", "Lisboa") 
df_nuts['Region'] = df_nuts['Region'].str.replace("Região Autónoma dos Açores", "Açores") 
df_nuts['Region'] = df_nuts['Region'].str.replace("Região Autónoma da Madeira", "Madeira")

df_nuts = df_nuts.drop_duplicates()

# Merge

# df_pt = df_pt.merge(df_nuts, on=['Region'], how='right')

# Merge

import fuzzymatcher

df_pt = fuzzymatcher.fuzzy_left_join(df_nuts, df_pt, left_on = "Region", right_on = "Region")
df_pt = df_pt.rename(columns={'Region_right':'Region'})
df_pt = df_pt[['Code.1', 'Region', 'Deaths']]

# FRANCE

# Corona

import wget
urls = 'https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv'
if os.path.exists(cwd + '/COVID19_France_raw.csv'):
    os.remove(cwd + '/COVID19_France_raw.csv')
wget.download(urls, cwd + '/COVID19_France_raw.csv', bar=None)

df_fr = pd.read_csv(cwd + '/COVID19_France_raw.csv')

df_fr = df_fr.loc[df_fr['source_nom'] == 'Santé publique France Data']

df_fr['date'] = pd.to_datetime(df_fr['date'])
last_day = df_fr['date'].max()
df_fr = df_fr.loc[df_fr['date'] == last_day]
df_fr = df_fr.loc[df_fr['granularite'] == 'departement']

df_fr = df_fr[['maille_nom', 'deces']]

df_fr.columns = ['Departement', 'Dead']

# Nuts

link = "https://en.wikipedia.org/wiki/NUTS_statistical_regions_of_France"
df_nuts = pd.read_html(link, header=0)[2]

df_nuts = df_nuts.rename(columns={'NUTS 2':'Region'})
df_nuts = df_nuts.rename(columns={'NUTS 3':'Departement'})

df_nuts = df_nuts.iloc[: , [2, 3, 4]]

df_nuts.drop(df_nuts.tail(5).index,inplace=True)

# Merge

import fuzzymatcher

df_fr = fuzzymatcher.fuzzy_left_join(df_nuts, df_fr, left_on = "Departement", right_on = "Departement")

df_fr['Deaths'] = df_fr['Dead'].groupby(df_fr['Region']).transform('sum')
df_fr = df_fr[['Code.1', 'Region', 'Deaths']]
df_fr = df_fr.drop_duplicates()

# ITALY

# Corona

link = "https://it.wikipedia.org/wiki/Pandemia_di_COVID-19_del_2020_in_Italia"
df_it = pd.read_html(link, header=0)[4]

df_it = df_it.rename(columns={'Regione':'Region'})
df_it = df_it.rename(columns={'Decessi':'Deaths'})
df_it = df_it[['Region', 'Deaths']]
df_it.drop(df_it.tail(3).index,inplace=True)

df_it['Deaths'] = df_it['Deaths'].str.replace(' ', '')

# Nuts

link = "https://it.wikipedia.org/wiki/Nomenclatura_delle_unit%C3%A0_territoriali_per_le_statistiche_dell%27Italia"
df_nuts = pd.read_html(link, header=0)[0]

#df_nuts.columns = df_nuts.iloc[1]
df_nuts.drop(df_nuts.head(1).index,inplace=True)

df_nuts = df_nuts.iloc[:, [2, 3]]

df_nuts = df_nuts.rename(columns={'NUTS 2':'Region'})
df_nuts = df_nuts.rename(columns={'NUTS 2.1':'Code.1'})

idx = (df_nuts['Code.1'] == 'ITH10 / ITH20').idxmax()
#df_nuts.loc[df_nuts.idxmin()] = 'ITH10 / ITH20'

df_nuts.loc[idx,'Code.1'] = 'ITH1'
df_nuts['Code.1'] = df_nuts['Code.1'].str.replace('ITH10 / ITH20', 'ITH2')

df_nuts = df_nuts.drop_duplicates()

# Merge

# df_it = df_it.merge(df_nuts, on=['Region'], how='right')
# df_it = df_it[['Code.1', 'Region', 'Deaths']]

# Merge

import fuzzymatcher

df_it = fuzzymatcher.fuzzy_left_join(df_nuts, df_it, left_on = "Region", right_on = "Region")
df_it = df_it.rename(columns={'Region_right':'Region'})
df_it = df_it[['Code.1', 'Region', 'Deaths']]

import re

# GERMANY

# Corona

import wget
urls = 'https://opendata.arcgis.com/agol/arcgis/dd4580c810204019a7b8eb3e0b329dd6/0.csv'
if os.path.exists(cwd + '/COVID19_Germany_raw.csv'):
    os.remove(cwd + '/COVID19_Germany_raw.csv')
wget.download(urls, cwd + '/COVID19_Germany_raw.csv', bar=None)

df_de = pd.read_csv(cwd + '/COVID19_Germany_raw.csv').fillna(0)
df_de = df_de[['Landkreis', 'AnzahlTodesfall']]

df_de['Landkreis'] = df_de['Landkreis'].str.replace("(Berlin).*", "Berlin") 

df_de['AnzahlTodesfall'] = df_de['AnzahlTodesfall'].abs()

df_de['Dead'] = df_de['AnzahlTodesfall'].groupby(df_de['Landkreis']).transform('sum')

df_de = df_de[['Landkreis', 'Dead']]

df_de = df_de.drop_duplicates()

df_de['Landkreis'] = df_de['Landkreis'].str.replace("SK ", "Kreisfreie Stadt ")
df_de['Landkreis'] = df_de['Landkreis'].str.replace("LK ", "Landkreis ")

#df_de.to_csv(cwd + '/germany.csv', index = False)

# Nuts

link = "https://de.wikipedia.org/wiki/NUTS:DE"
df_nuts = pd.read_html(link, header=0)[0]

df_nuts = df_nuts.iloc[: , [2, 3, 5]]
df_nuts = df_nuts[df_nuts.columns[::-1]]

df_nuts.drop(df_nuts.head(1).index,inplace=True)
df_nuts.drop(df_nuts.tail(1).index,inplace=True)
df_nuts = df_nuts.rename(columns={'NUTS 2.1':'Region'})
df_nuts = df_nuts.rename(columns={'NUTS 3.1':'Landkreis'})
df_nuts = df_nuts.rename(columns={'NUTS 2':'Code.1'})

#df_nuts['Landkreis'] = df_nuts['Landkreis'].str.split(',').str[0]

#df_nuts.to_csv(cwd + '/germany_nuts.csv', index = False)

# Merge

import fuzzymatcher

df_mer = fuzzymatcher.fuzzy_left_join(df_nuts, df_de, left_on = "Landkreis", right_on = "Landkreis")

#df_mer.to_csv(cwd + '/germany_merged.csv', index = False)

df_mer['Deaths'] = df_mer['Dead'].groupby(df_mer['Region']).transform('sum')

df_de = df_mer[['Code.1', 'Region', 'Deaths']]

df_de = df_de.drop_duplicates()

# SWITZERLAND

# Corona

import wget
urls = 'https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_fatalities_switzerland_openzh.csv'
if os.path.exists(cwd + '/COVID19_Switzerland_raw.csv'):
    os.remove(cwd + '/COVID19_Switzerland_raw.csv')
wget.download(urls, cwd + '/COVID19_Switzerland_raw.csv', bar=None)

df_ch = pd.read_csv(cwd + '/COVID19_Switzerland_raw.csv').ffill()

df_ch.drop(df_ch.tail(1).index,inplace=True)
df_ch = df_ch.tail(1)

df_ch = df_ch.transpose()

df_ch.drop(df_ch.head(1).index,inplace=True)
df_ch.drop(df_ch.tail(1).index,inplace=True)

df_ch = df_ch.reset_index()
df_ch.columns = ['CantonID', 'Dead']
df_ch = df_ch.fillna(0)

# ID to Canton name

link = "https://de.wikipedia.org/wiki/Kanton_(Schweiz)"
df_id = pd.read_html(link, header=0)[0]

df_id = df_id[['Abk.', 'Kanton']]
df_id.columns = ['CantonID', 'Canton']
df_id.drop(df_id.tail(1).index,inplace=True)

import fuzzymatcher

df_ch = fuzzymatcher.fuzzy_left_join(df_id, df_ch, left_on = "CantonID", right_on = "CantonID")
df_ch = df_ch[['Canton', 'Dead']]

# Nuts

link2 = "https://de.wikipedia.org/wiki/NUTS:CH"
df_nuts = pd.read_html(link2, header=0)[0]

df_nuts = df_nuts[['NUTS-2', 'NUTS-2.1', 'NUTS-3.1']]

df_nuts = df_nuts.rename(columns={'NUTS-2':'Code.1'})
df_nuts = df_nuts.rename(columns={'NUTS-2.1':'Region'})
df_nuts = df_nuts.rename(columns={'NUTS-3.1':'Canton'})

# Merge

df_ch = fuzzymatcher.fuzzy_left_join(df_nuts, df_ch, left_on = "Canton", right_on = "Canton")

df_ch['Deaths'] = df_ch['Dead'].groupby(df_ch['Region']).transform('sum')
df_ch = df_ch[['Code.1', 'Region', 'Deaths']]
df_ch = df_ch.drop_duplicates()

# LUXEMBOURG

import wptools

lux = wptools.page('COVID-19_pandemic_in_Luxembourg').get_parse()
infobox = lux.data['infobox']
dead = infobox['deaths']

data = {'Code.1':  ['LU00'],
        'Region': ['Luxembourg'],
        'Deaths': [dead]
        }

df_lu = pd.DataFrame(data, columns = ['Code.1','Region','Deaths'])

# AUSTRIA

# Corona

import zipfile
import wget

urls = 'https://info.gesundheitsministerium.at/data/data.zip'
if os.path.exists(cwd + '/COVID19_Austria_raw.zip'):
    os.remove(cwd + '/COVID19_Austria_raw.zip')
wget.download(urls, cwd + '/COVID19_Austria_raw.zip', bar=None)

zf = zipfile.ZipFile(cwd + '/COVID19_Austria_raw.zip')
df_at = pd.read_csv(zf.open('GenesenTodesFaelleBL.csv'), sep=';')

df_at = df_at[['Bundesland', 'Todesfälle']]
df_at.columns = ['Region', 'Deaths']

# NUTS

link = "https://de.wikipedia.org/wiki/NUTS:AT"
df_nuts = pd.read_html(link, header=0)[0]

df_nuts = df_nuts[['NUTS-2 Region']]

df_nuts.drop(df_nuts.tail(1).index,inplace=True)

df_nuts['Code.1'] = df_nuts['NUTS-2 Region'].str.slice(0,4)
df_nuts['Region'] = df_nuts['NUTS-2 Region'].str.slice(4,)
df_nuts = df_nuts[['Code.1', 'Region']]
df_nuts = df_nuts.drop_duplicates()

# Merge

import fuzzymatcher

df_at = fuzzymatcher.fuzzy_left_join(df_nuts, df_at, left_on = "Region", right_on = "Region")
df_at = df_at.rename(columns={'Region_right':'Region'})
df_at = df_at[['Code.1', 'Region', 'Deaths']]

# DENMARK

# Corona

link = "https://www.sst.dk/da/corona/tal-og-overvaagning"
df_dk = pd.read_html(link, header=0)[2]

df_dk = df_dk.rename(columns={'Dødsfald✱✱':'Deaths'})
df_dk = df_dk[['Region', 'Deaths']]
df_dk.drop(df_dk.tail(1).index,inplace=True)

# NUTS

link = "https://de.wikipedia.org/wiki/NUTS:DK"
df_nuts = pd.read_html(link, header=0)[0]

df_nuts = df_nuts.iloc[: , [2, 3]]

df_nuts.drop(df_nuts.head(1).index,inplace=True)

df_nuts = df_nuts.rename(columns={'NUTS 2':'Code.1'})
df_nuts = df_nuts.rename(columns={'NUTS 2.1':'Region'})

df_nuts = df_nuts.drop_duplicates()

# Merge

import fuzzymatcher

df_dk = fuzzymatcher.fuzzy_left_join(df_nuts, df_dk, left_on = "Region", right_on = "Region")
df_dk = df_dk.rename(columns={'Region_right':'Region'})
df_dk = df_dk[['Code.1', 'Region', 'Deaths']]

# BELGIUM

# Corona

import wget
urls = 'https://epistat.sciensano.be/Data/COVID19BE_MORT.csv'
if os.path.exists(cwd + '/COVID19_Belgium_raw.csv'):
    os.remove(cwd + '/COVID19_Belgium_raw.csv')
wget.download(urls, cwd + '/COVID19_Belgium_raw.csv', bar=None)

df_be = pd.read_csv(cwd + '/COVID19_Belgium_raw.csv')

df_be['Deaths'] = df_be['DEATHS'].groupby(df_be['REGION']).transform('sum')
df_be = df_be.rename(columns={'REGION':'Region'})
df_be = df_be[['Region', 'Deaths']]
df_be = df_be.drop_duplicates()

# NUTS

link = "https://en.wikipedia.org/wiki/NUTS_statistical_regions_of_Belgium"
df_nuts = pd.read_html(link, header=0)[1]

df_nuts = df_nuts.iloc[: , [0, 2, 3]]

df_nuts = df_nuts.rename(columns={'NUTS 1':'Region'})
df_nuts = df_nuts.rename(columns={'NUTS 2':'Province'})

df_nuts = df_nuts.drop_duplicates()

# Merge

import fuzzymatcher

df_be = fuzzymatcher.fuzzy_left_join(df_nuts, df_be, left_on = "Region", right_on = "Region")
#df_be = df_be.rename(columns={'Region_right':'Region'})
df_be = df_be[['Code.1', 'Province', 'Deaths']]
df_be = df_be.rename(columns={'Province':'Region'})
df_be = df_be.drop_duplicates()

# NETHERLANDS

# Corona

urls = "https://raw.githubusercontent.com/J535D165/CoronaWatchNL/master/data/rivm_NL_covid19_fatalities_municipality.csv"
if os.path.exists(cwd + '/COVID19_Netherlands_raw.csv'):
    os.remove(cwd + '/COVID19_Netherlands_raw.csv')
wget.download(urls, cwd + '/COVID19_Netherlands_raw.csv', bar=None)

df_nl = pd.read_csv(cwd + '/COVID19_Netherlands_raw.csv')
yesterday = pd.Timestamp('today').floor('D') - pd.offsets.Day(1)
df_nl['Datum'] = pd.to_datetime(df_nl['Datum'])
mask = (df_nl['Datum'] >= yesterday) & (df_nl['Datum'] <= yesterday)
df_nl = df_nl.loc[mask]
df_nl = df_nl[['Provincienaam', 'Aantal']]
df_nl.drop(df_nl.head(1).index,inplace=True)
df_nl = df_nl.rename(columns={'Provincienaam':'Region'})
df_nl = df_nl.rename(columns={'Aantal':'Dead'})
df_nl['Deaths'] = df_nl['Dead'].groupby(df_nl['Region']).transform('sum')
df_nl = df_nl[['Region', 'Deaths']]
df_nl = df_nl.drop_duplicates()

# link = "https://www.cbs.nl/en-gb/news/2020/17/lower-mortality-in-third-week-of-april#278d5a0a-3705-4b63-9737-c523ba225e5f"
# df_nl = pd.read_html(link, header=0)[3]
# df_nl.drop(df_nl.tail(1).index,inplace=True)
# df_nl = df_nl.rename(columns={'Unnamed: 0':'Region'})
# df_nl = df_nl.rename(columns={'Week 16 (total)':'Deaths'})
# df_nl = df_nl[['Region', 'Deaths']]

# NUTS

link = "https://de.wikipedia.org/wiki/NUTS:NL"
df_nuts = pd.read_html(link, header=0)[0]
df_nuts = df_nuts.iloc[: , [2, 3]]
df_nuts.drop(df_nuts.head(1).index,inplace=True)
df_nuts = df_nuts.drop_duplicates()
df_nuts = df_nuts.rename(columns={'NUTS 2':'Code.1'})
df_nuts = df_nuts.rename(columns={'NUTS 2.1':'Region'})

# Merge

import fuzzymatcher

df_nl = fuzzymatcher.fuzzy_left_join(df_nuts, df_nl, left_on = "Region", right_on = "Region")
df_nl = df_nl.rename(columns={'Region_right':'Region'})
df_nl = df_nl[['Code.1', 'Region', 'Deaths']]

# NORTHERN IRELAND

# Corona

#import wget 

#url = 'https://www.nisra.gov.uk/sites/nisra.gov.uk/files/publications/Weekly_Deaths.xls'
#if os.path.exists(cwd + '/COVID19_NIR_raw.xlsx'):
#    os.remove(cwd + '/COVID19_NIR_raw.xlsx')
# wget.download(url, cwd + '/COVID19_NIR_raw.xlsx')

#from pandas import read_excel

#file_name = cwd + '/COVID19_NIR_raw.xlsx'
#df_nir = read_excel(file_name, sheet_name='Covid-19 by Date of death')
#df_nir = df_nir[['Unnamed: 3']].dropna()
#dead = int(df_nir[['Unnamed: 3']].iat[-1,0])

import requests

import datetime
import locale
locale.setlocale(locale.LC_TIME, "en_US.utf8")

day_delta = datetime.timedelta(days=1)
start_date = datetime.date.today()
end_date = start_date - 31 * day_delta

for i in range((start_date - end_date).days):
	day = (start_date - i * day_delta).strftime('%d-%B-%Y')
	response = requests.get('https://www.health-ni.gov.uk/news/daily-covid-19-figures-' + day)
	url = 'https://www.health-ni.gov.uk/news/daily-covid-19-figures-' + day
	if response.status_code == 200:
		df_nir = pd.read_html(url, header=0)[0]
		idx = (df_nir.iloc[:, 0] == 'Cumulative total').idxmax()
		dead = df_nir.iloc[idx]['Deaths']
		break

data = {'Code.1':  ['UKN0'],
        'Region': ['Northern Ireland'],
        'Deaths': [dead]
        }

df_nir = pd.DataFrame(data, columns = ['Code.1','Region','Deaths'])

#IRELAND

# Corona

import wget
urls = 'https://opendata-geohive.hub.arcgis.com/datasets/d8eb52d56273413b84b0187a4e9117be_0.csv'
if os.path.exists(cwd + '/COVID19_Ireland_raw.csv'):
    os.remove(cwd + '/COVID19_Ireland_raw.csv')
wget.download(urls, cwd + '/COVID19_Ireland_raw.csv', bar=None)

df_ie = pd.read_csv(cwd + '/COVID19_Ireland_raw.csv')
df_ie = df_ie[['TotalCovidDeaths']]
dead = int(df_ie[['TotalCovidDeaths']].iat[-1,0])

# NUTS

link = "https://en.wikipedia.org/wiki/NUTS_statistical_regions_of_Ireland"
df_nuts = pd.read_html(link, header=0)[1]
df_nuts = df_nuts.iloc[: , [2, 3]]
df_nuts = df_nuts.drop_duplicates()
df_nuts = df_nuts.rename(columns={'NUTS 2':'Region'})
df_nuts = df_nuts[df_nuts.columns[::-1]]

# Merge

df_nuts['Deaths']= dead

df_ie = df_nuts

# NORWAY

# Corona

import urllib3
import re

url = 'https://www.fhi.no/en/id/infectious-diseases/coronavirus/daily-reports/daily-reports-COVID19/'

http_pool = urllib3.connection_from_url(url)
site = http_pool.urlopen('GET',url).data.decode('utf-8')

for line in site.split("\n"):
	if "deaths have been notified to the NIPH" in line:
		dead = re.findall(r'\d+', line)[0]

# NUTS

link = "https://de.wikipedia.org/wiki/NUTS:NO"
df_nuts = pd.read_html(link, header=0)[1]
df_nuts = df_nuts.iloc[: , [2, 3]]
df_nuts = df_nuts.drop_duplicates()
df_nuts = df_nuts.rename(columns={'NUTS 2':'Code.1'})
df_nuts = df_nuts.rename(columns={'NUTS 2.1':'Region'})
df_nuts.drop(df_nuts.tail(1).index,inplace=True)

# Merge

df_nuts['Deaths']= dead
df_no = df_nuts

# SWEDEN

# Corona

import wget
urls = 'https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data'
if os.path.exists(cwd + '/COVID19_Sweden_raw.xlsx'):
    os.remove(cwd + '/COVID19_Sweden_raw.xlsx')
wget.download(urls, cwd + '/COVID19_Sweden_raw.xlsx', bar=None)

df_se = pd.read_excel(cwd + '/COVID19_Sweden_raw.xlsx', sheet_name='Totalt antal per region')

df_se.drop(df_se.columns.difference(['Region','Totalt_antal_avlidna']), 1, inplace=True)

df_se = df_se.rename(columns={'Totalt_antal_avlidna':'Dead'})
df_se = df_se.rename(columns={'Region':'County'})
df_se['County'] = df_se['County'].str.replace("Sörmland", "Södermanland")

# NUTS

link = "https://en.wikipedia.org/wiki/NUTS_statistical_regions_of_Sweden"
df_nuts = pd.read_html(link, header=0)[2]

df_nuts = df_nuts.iloc[: , [2, 3, 4]]

df_nuts = df_nuts.rename(columns={'NUTS 3':'County'})
df_nuts = df_nuts.rename(columns={'Code':'Code.1'})
df_nuts = df_nuts.rename(columns={'NUTS 2':'Region'})

df_nuts['Code.1'] = df_nuts['Code.1'].str.replace('SE01', 'SE11')
df_nuts['Code.1'] = df_nuts['Code.1'].str.replace('SE02', 'SE12')
df_nuts['Code.1'] = df_nuts['Code.1'].str.replace('SE09', 'SE21')
df_nuts['Code.1'] = df_nuts['Code.1'].str.replace('SE04', 'SE22')
df_nuts['Code.1'] = df_nuts['Code.1'].str.replace('SE0A', 'SE23')
df_nuts['Code.1'] = df_nuts['Code.1'].str.replace('SE06', 'SE31')
df_nuts['Code.1'] = df_nuts['Code.1'].str.replace('SE07', 'SE32')
df_nuts['Code.1'] = df_nuts['Code.1'].str.replace('SE08', 'SE33')

# Merge

import fuzzymatcher

df_mer = fuzzymatcher.fuzzy_left_join(df_nuts, df_se, left_on = "County", right_on = "County")
df_mer['Deaths'] = df_mer['Dead'].groupby(df_mer['Region']).transform('sum')
df_se = df_mer[['Code.1', 'Region', 'Deaths']]
df_se = df_se.drop_duplicates()

# WALES

# Corona

import wget 

url = 'https://raw.githubusercontent.com/tomwhite/covid-19-uk-data/master/data/covid-19-totals-wales.csv'
if os.path.exists(cwd + '/COVID19_WLS_raw.csv'):
    os.remove(cwd + '/COVID19_WLS_raw.csv')
wget.download(url, cwd + '/COVID19_WLS_raw.csv', bar=None)

df_wls = pd.read_csv(cwd + '/COVID19_WLS_raw.csv').ffill()
df_wls = df_wls[['Deaths']]
dead = int(df_wls[['Deaths']].iat[-1,0])


data = {'Code.1':  ['UKL1', 'UKL2'],
        'Region': ['Wales', 'Wales'],
        'Deaths': [dead, dead]
        }

df_wls = pd.DataFrame(data, columns = ['Code.1','Region','Deaths'])

# SCOTLAND

# Corona

from datetime import date
week = date.today().isocalendar()[1] + 1

import requests
import wget 

for n in reversed(range(week)):
	response = requests.get('https://www.nrscotland.gov.uk/files//statistics/covid19/covid-deaths-data-week-' + str(n) + '.xlsx')
	url = 'https://www.nrscotland.gov.uk/files//statistics/covid19/covid-deaths-data-week-' + str(n) + '.xlsx'
	if response.status_code == 200:
		if os.path.exists(cwd + '/COVID19_SCT_raw.xlsx'):
			os.remove(cwd + '/COVID19_SCT_raw.xlsx')
		wget.download(url, cwd + '/COVID19_SCT_raw.xlsx')
		break

from pandas import read_excel

file_name = cwd + '/COVID19_SCT_raw.xlsx'
df_sct = read_excel(file_name, sheet_name='Table 3 - deaths by location')
df_sct.columns.values[0] = "NUTS3"
df_sct.columns.values[5] = "Dead"
idx1 = (df_sct['NUTS3'] == 'Aberdeen City').idxmax()
idx2 = (df_sct['NUTS3'] == 'West Lothian').idxmax() + 1
df_sct = df_sct.iloc[idx1:idx2, [0,5]]

# NUTS

sct2nuts = {
    'Code.1': ['UKM5', 'UKM5', 'UKM6', 'UKM6', 'UKM6', 'UKM6', 'UKM6', 'UKM7', 'UKM7', 'UKM7', 'UKM7', 'UKM7', 'UKM7', 'UKM7', 'UKM7', 'UKM7', 'UKM7', 'UKM7', 'UKM8', 'UKM8', 'UKM8', 'UKM8', 'UKM8', 'UKM8', 'UKM8', 'UKM9', 'UKM9', 'UKM9', 'UKM9', 'UKM9', 'UKM9', 'UKM9'], 
    'Region': ['North Eastern Scotland', 'North Eastern Scotland', 'Highlands and Islands', 'Highlands and Islands', 'Highlands and Islands', 'Highlands and Islands', 'Highlands and Islands', 'Eastern Scotland', 'Eastern Scotland', 'Eastern Scotland', 'Eastern Scotland', 'Eastern Scotland', 'Eastern Scotland', 'Eastern Scotland', 'Eastern Scotland', 'Eastern Scotland', 'Eastern Scotland', 'Eastern Scotland', 'West Central Scotland', 'West Central Scotland', 'West Central Scotland', 'West Central Scotland', 'West Central Scotland', 'West Central Scotland', 'West Central Scotland', 'Southern Scotland', 'Southern Scotland', 'Southern Scotland', 'Southern Scotland', 'Southern Scotland', 'Southern Scotland', 'Southern Scotland'], 
    'NUTS3': ['Aberdeen City', 'Aberdeenshire', 'Argyll and Bute', 'Highland', 'Moray', 'Orkney Islands', 'Shetland Islands', 'Angus', 'City of Edinburgh', 'Clackmannanshire', 'Dundee City', 'East Lothian', 'Midlothian', 'West Lothian', 'Falkirk', 'Fife', 'Perth and Kinross', 'Stirling', 'East Dunbartonshire', 'West Dunbartonshire', 'East Renfrewshire', 'Renfrewshire', 'Glasgow City', 'Inverclyde', 'North Lanarkshire', 'Dumfries and Galloway', 'East Ayrshire', 'North Ayrshire', 'South Ayrshire', 'Na h-Eileanan Siar', 'South Lanarkshire', 'Scottish Borders']
}

df_nuts = pd.DataFrame(sct2nuts)

# Merge

import fuzzymatcher

df_mer = fuzzymatcher.fuzzy_left_join(df_nuts, df_sct, left_on = "NUTS3", right_on = "NUTS3")
df_mer['Deaths'] = df_mer['Dead'].groupby(df_mer['Region']).transform('sum')
df_sct = df_mer[['Code.1', 'Region', 'Deaths']]
df_sct = df_sct.drop_duplicates()

# ENGLAND

# Corona

import requests
import wget

import datetime
import locale
locale.setlocale(locale.LC_TIME, "en_US.utf8")

day_delta = datetime.timedelta(days=1)
start_date = datetime.date.today()
end_date = start_date - 31 * day_delta

for i in range((start_date - end_date).days):
	day = (start_date - i * day_delta).strftime('%d-%B-%Y')
	response = requests.get('https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2020/04/COVID-19-total-announced-deaths-' + day + '.xlsx')
	url = 'https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2020/04/COVID-19-total-announced-deaths-' + day + '.xlsx'
	if response.status_code == 200:
		if os.path.exists(cwd + '/COVID19_ENG_raw.xlsx'):
			os.remove(cwd + '/COVID19_ENG_raw.xlsx')
		wget.download(url, cwd + '/COVID19_ENG_raw.xlsx')
		break

from pandas import read_excel

file_name = cwd + '/COVID19_ENG_raw.xlsx'
df_eng = read_excel(file_name, sheet_name='COVID19 total deaths by region')

df_eng.columns.values[1] = "Region"
df_eng.columns.values[-1] = "Deaths"
idx1 = (df_eng['Region'] == 'East Of England').idxmax()
idx2 = (df_eng['Region'] == 'South West').idxmax() + 1
df_eng = df_eng.iloc[idx1:idx2, [1,-1]]

# NUTS

eng2nuts = {
    'Code.1': ['UKC1', 'UKC2', 'UKD1', 'UKD6', 'UKD3', 'UKD4', 'UKD7', 'UKE1', 'UKE2', 'UKE3', 'UKE4', 'UKF1', 'UKF2', 'UKF3', 'UKG1', 'UKG2', 'UKG3', 'UKH1', 'UKH2', 'UKH3', 'UKI3', 'UKI4', 'UKI5', 'UKI6', 'UKI7', 'UKJ1', 'UKJ2', 'UKJ3', 'UKJ4', 'UKK1', 'UKK2', 'UKK3', 'UKK4'],
    'Region': ['North East And Yorkshire', 'North East And Yorkshire', 'North West', 'North West', 'North West', 'North West', 'North West', 'North East And Yorkshire', 'North East And Yorkshire', 'North East And Yorkshire', 'North East And Yorkshire', 'Midlands', 'Midlands', 'Midlands', 'Midlands', 'Midlands', 'Midlands', 'East of England', 'East of England', 'East of England', 'London', 'London', 'London', 'London', 'London', 'South East', 'South East', 'South East', 'South East', 'South West', 'South West', 'South West', 'South West'], 
    'NUTS2': ['Tees Valley and Durham', 'Northumberland and Tyne and Wear', 'Cumbria', 'Cheshire', 'Greater Manchester', 'Lancashire', 'Merseyside', 'East Riding and North Lincolnshire', 'North Yorkshire', 'South Yorkshire', 'West Yorkshire', 'Derbyshire and Nottinghamshire', 'Leicestershire, Rutland and Northamptonshire', 'Lincolnshire', 'Herefordshire, Worcestershire and Warwickshire', 'Shropshire and Staffordshire', 'West Midlands', 'East Anglia', 'Bedfordshire and Hertfordshire', 'Essex', 'Inner London East', 'Inner London West', 'Outer London South', 'Outer London West and Northwest', 'Outer London East and Norteast', 'Berkshire, Buckinghamshire, and Oxfordshire', 'Surrey, East and West Sussex', 'Hampshire and Isle of Wight', 'Kent', 'Gloucestershire, Wiltshire and Bristol/Bath area', 'Dorset and Somerset', 'Cornwall and Isles of Scilly', 'Devon'], 
}

df_nuts = pd.DataFrame(eng2nuts)

# Merge

import fuzzymatcher

df_mer = fuzzymatcher.fuzzy_left_join(df_nuts, df_eng, left_on = "Region", right_on = "Region")
df_eng = df_mer[['Code.1', 'Region_left', 'Deaths']]
df_eng = df_eng.rename(columns={'Region_left':'Region'})

##########
# CONCAT #
##########

df = pd.concat([df_pt,df_es,df_fr,df_it,df_de,df_ch,df_lu,df_at,df_dk,df_be,df_nl,df_nir,df_ie,df_no,df_se,df_wls,df_sct,df_eng])

df = df.rename(columns={'Code.1':'NUTS2'})
df = df[['NUTS2', 'Region', 'Deaths']]

# POPULATION

import os
cwd = os.getcwd()

import wget

url = 'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/tgs00096.tsv.gz'
if os.path.exists(cwd + '/NUTS2_population_raw.tsv.gz'):
    os.remove(cwd + '/NUTS2_population_raw.tsv.gz')
wget.download(url, cwd + '/NUTS2_population_raw.tsv.gz')

df_pop = pd.read_csv(cwd + '/NUTS2_population_raw.tsv.gz', compression='infer', sep=r'\,|\t', engine='python')

df_pop = df_pop.rename(columns={'geo\\time':'NUTS2'})
df_pop = df_pop.rename(columns={'2019':'Population'})
df_pop = df_pop.replace(to_replace = ': ', value = '')
df_pop = df_pop.replace(to_replace = ':', value = '')
df_pop['Population'] = df_pop['Population'].str.extract('(\d+)', expand=False)
df_pop = df_pop.ffill(axis = 1)  

df_pop = df_pop[['NUTS2', 'Population']]

# Sum Trentino

idx1 = (df_pop['NUTS2'] == 'ITH1').idxmax()
idx2 = (df_pop['NUTS2'] == 'ITH2').idxmax()
pop = int(df_pop.loc[idx1,'Population']) + int(df_pop.loc[idx2,'Population'])
df_pop.loc[idx1,'Population'] = pop
df_pop.loc[idx2,'Population'] = pop

# Sum Belgium (Wallonie and Flanders)

for n in range(1, 6):
	n = str(n)
	idxw = (df_pop['NUTS2'] == ('BE3' + n)).idxmax()
	idxf = (df_pop['NUTS2'] == ('BE2' + n)).idxmax()
	df_pop.loc[idxw,'Population'] = '3641748'
	df_pop.loc[idxf,'Population'] = '6623505'

# Sum Ireland

for n in range(4, 7):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('IE0' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '4753886'
	
# Sum Norway

for n in range(1, 8):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('NO0' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '5367580'
	
# Sum Wales

for n in range(1, 3):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKL' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '3138631'
	
# Sum England

for n in range(1, 4):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKH' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '6201214'

for n in range(1, 4):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKF' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '10704906'

for n in range(1, 4):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKG' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '10704906'

for n in range(1, 3):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKC' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '8137524'

for n in range(1, 5):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKE' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '8137524'

for n in [1, 3, 4, 6, 7]:
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKD' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '7292093'

for n in range(1, 5):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKJ' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '9133625'
	
for n in range(1, 5):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKK' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '5599735'

for n in range(3, 8):
	n = str(n)
	idx = (df_pop['NUTS2'] == ('UKI' + n)).idxmax()
	df_pop.loc[idx,'Population'] = '8908081'

# Merge

df = df.merge(df_pop, on=['NUTS2'], how='left')

# Per million

df['Population'] = df['Population'].astype(str).astype(float)
df['Population'] = df['Population'].astype(int).astype(float)
df['Population'] = df['Population'].truediv(1000000)

df['Deaths'] = df['Deaths'].astype(str).astype(float)
df['Deaths'] = df['Deaths'].astype(int).astype(float)
df['Deaths_per_million'] = df['Deaths'] / df['Population']
df.Deaths_per_million = df.Deaths_per_million.round()

df['Deaths_per_million'] = df['Deaths_per_million'].astype(float).astype(int)
df = df[['NUTS2', 'Region', 'Deaths_per_million']]
df = df.rename(columns={'Deaths_per_million':'Deaths'})

# Save

df.to_csv("NUTS2_in_coronavirusland.csv", sep=',', index=False)

# PLOT MAP

df = pd.read_csv(cwd + '/NUTS2_in_coronavirusland.csv')
df = df.rename(columns={'NUTS2':'NUTS_ID'})

url = 'https://gisco-services.ec.europa.eu/distribution/v2/nuts/csv/NUTS_AT_2016.csv'
if os.path.exists(cwd + '/NUTS_AT_2016.csv'):
    os.remove(cwd + '/NUTS_AT_2016.csv')
wget.download(url, cwd + '/NUTS_AT_2016.csv')

df_all = pd.read_csv(cwd + '/NUTS_AT_2016.csv')
df_all = df_all[['NUTS_ID']]

df_mer = df.merge(df_all, on=['NUTS_ID'], how='outer')

df_mer.to_csv("NUTS2_in_coronavirusland_toplot.csv", sep=',', index=False)

import folium

import geopandas as gpd

world_geo = gpd.read_file(cwd + '/NUTS_RG_60M_2016_4326_LEVL_2.geojson')
#world_geo = os.path.join(cwd , 'NUTS_RG_60M_2016_4326_LEVL_2.geojson')
 
world_data = pd.read_csv(cwd + '/NUTS2_in_coronavirusland_toplot.csv')

corona_geo = world_geo.merge(world_data, on='NUTS_ID')
 
# Initialize the map:
m = folium.Map(location=[49, 12], zoom_start=5)
 
# Add the color for the chloropleth:
choropleth = folium.Choropleth(
	geo_data=corona_geo,
	name='choropleth',
	data=world_data,
	columns=['NUTS_ID', 'Deaths'],
	key_on='properties.NUTS_ID',
	nan_fill_color='#F5F5F5',
	fill_color='YlOrRd',
	bins=9,
	fill_opacity=0.8,
	line_opacity=0.2,
	legend_name='COVID-19 Deaths per Million',
	highlight=True,
	tiles="OpenStreetMap"
).add_to(m)

folium.LayerControl(collapsed=True).add_to(m)

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['NUTS_NAME', 'Deaths'],labels=False)
)

today = datetime.date.today()
tdate = today.strftime('%d %B %Y')

title_html = '<h6 align="center" style="font-size:14px";><b>COVID-19 DEATHS PER MILLION &emsp; [ ' + tdate + ' ]</b></h6>'

m.get_root().html.add_child(folium.Element(title_html))

# Save to html
tdate = today.strftime('%d_%B_%Y')
m.save(cwd + '/NUTS2_in_coronavirusland.html')
m.save(cwd + '/screenshots/NUTS2_in_coronavirusland_' + tdate + '.html')
