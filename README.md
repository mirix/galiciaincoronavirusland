# galiciaincoronavirusland
Python scripts to analyse current COVID-19 data
###############################
#          READ ME            #
###############################
# This Python script downloads COVID-19 data from two different sources (labelled as "raw"):
#    + Information about the Spanish Autonomous Communities from the Spanish Ministry of Health
#    + Worldwide information from the European Centre for Disease Prevention and Control (ECDC)
# The data is only updated once per day, so there is no need in rerunning this more often
# Should you want to replot the data, please, use the auxiliary plot script
# Which works on the output CSV produced by this script
# It keeps only deceases data
# It converts it to cumulative format (per day)
# And to relative figures (deaths per million inhabitants)
# It formats and merges both sources
# It generates a new CSV file and two image files
# The script is self-explanatory. Each subsection is illuminated
# It intends to be a minimalistic template that can be easily modified and recycled
# In its current state in enables comparing data from my country (Galicia)
# and the rest of the world. It gives some peace of mind to my friends who live abroad...
# REQUIREMENTS: Python 3 along with the following modules/libraries:
#    + Pandas, wget, datetime, matplotlib

For sample images see:
https://sentidinho.eu/sentidinho/galicia-in-coronavirusland/
