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
#    https://sentidinho.eu/sentidinho/galicia-in-coronavirusland

###############################
#          READ ME            #
###############################
# This is an auxiliary script of the master script Galicia_in_Coronavirusland.py
# It is intended as a template to play with graphical visualisation optiona
# It is and will always be work in progress
# The idea of providing it as an separate script is to avoid downloading and formating
# the raw data each time that we wish to plot it with different settings
# This script works on the outputa of the master script and expects to find
# two CSV files called Galicia_in_Coronavirusland.csv and Galicia_in_Coronavirusland_noncumulative.csv
# in the same directory 
# REQUIREMENTS: Python 3 along with the following modules/libraries:
#    + Pandas, datetime, matplotlib

import os
cwd = os.getcwd()

import pandas as pd
import datetime

# The following two lines are required for the script to be run from crontab
# Otherwise plot() expects a display to be available

import matplotlib as mpl
mpl.use('Agg')

# Now we import matplotlib as usual

import matplotlib.pyplot as plt

# Read the CSV files

result = pd.read_csv(cwd + '/Galicia_in_Coronavirusland.csv')
result['dateRep'] = pd.to_datetime(result["dateRep"], infer_datetime_format=True)

resultnc = pd.read_csv(cwd + '/Galicia_in_Coronavirusland_absolute.csv')
resultnc['dateRep'] = pd.to_datetime(resultnc["dateRep"], infer_datetime_format=True)


# We remove the first forty days
# Change as appropriate

result.drop(result.head(40).index,inplace=True)

resultnc.drop(resultnc.head(40).index,inplace=True)

# Choose the countries you wish to plot
# Check the CSV files to find out the right names
# As a rule of thumb, replace spaces the English
# name with underscores 

###################
# Cumulative data #
###################

ax = plt.gca()
ax.set_title('COVID-19 pandemic')
ax.set_ylabel('Cumulative deaths per million')

#removing top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

result.plot(kind='line',x='dateRep',y='Galicia',ax=ax,color='#1ce5e3',linewidth=5)
result.plot(kind='line',x='dateRep',y='Spain', color='red',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Portugal',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Germany',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Italy',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='United_Kingdom',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Netherlands',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='France',ax=ax,linewidth=3)

plt.grid(b=True, which='major', color='#cccccc', linestyle='-', alpha=0.2)
plt.legend(frameon=False)

# We save the plot in SVG (editable vectorial graph)
# and PNG formats

plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot.svg')
plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot.png', dpi=300)

#plt.show()
plt.close()

result.drop(result.head(10).index,inplace=True)

ax = plt.gca()
ax.set_title('COVID-19 pandemic')
ax.set_ylabel('Cumulative deaths per million')

#removing top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

result.plot(kind='line',x='dateRep',y='Galicia',ax=ax,color='#1ce5e3',linewidth=5)
result.plot(kind='line',x='dateRep',y='Belgium',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Luxembourg',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Switzerland',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Norway',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Denmark',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Sweden',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Finland',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Iceland',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='Ireland',ax=ax,linewidth=3)
result.plot(kind='line',x='dateRep',y='United_States_of_America',ax=ax,linewidth=3)

plt.grid(b=True, which='major', color='#cccccc', linestyle='-', alpha=0.2)
plt.legend(frameon=False)

# We save the plot in SVG (editable vectorial graph)
# and PNG formats

plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot2.svg')
plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot2.png', dpi=300)

#plt.show()
plt.close()

###################
#  Absolute data  #
###################

ax = plt.gca()
ax.set_title('COVID-19 pandemic')
ax.set_ylabel('Absolute deaths per million')

#removing top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

resultnc.plot(kind='line',x='dateRep',y='Galicia',ax=ax,color='#1ce5e3',linewidth=4)
resultnc.plot(kind='line',x='dateRep',y='Spain', color='red',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Portugal',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Germany',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Italy',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='United_Kingdom',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Netherlands',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='France',ax=ax,linewidth=2)

plt.grid(b=True, which='major', color='#cccccc', linestyle='-', alpha=0.2)
plt.legend(frameon=False)

# We save the plot in SVG (editable vectorial graph)
# and PNG formats

plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot_absolute.svg')
plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot_absolute.png', dpi=300)

#plt.show()
plt.close()

resultnc.drop(resultnc.head(10).index,inplace=True)

ax = plt.gca()
ax.set_title('COVID-19 pandemic')
ax.set_ylabel('Absolute deaths per million')

#removing top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

resultnc.plot(kind='line',x='dateRep',y='Galicia',ax=ax,color='#1ce5e3',linewidth=4)
resultnc.plot(kind='line',x='dateRep',y='Belgium',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Switzerland',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Norway',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Denmark',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Sweden',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Finland',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='Ireland',ax=ax,linewidth=2)
resultnc.plot(kind='line',x='dateRep',y='United_States_of_America',ax=ax,linewidth=2)

plt.grid(b=True, which='major', color='#cccccc', linestyle='-', alpha=0.2)
plt.legend(frameon=False)

# We save the plot in SVG (editable vectorial graph)
# and PNG formats

plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot2_absolute.svg')
plt.savefig(cwd + '/Galicia_in_Coronavirusland_plot2_absolute.png', dpi=300)

#plt.show()
plt.close()
