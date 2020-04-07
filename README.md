# galiciaincoronavirusland

Python scripts to analyse current COVID-19 data

This Python script downloads COVID-19 data from two different sources (labelled as "raw"):
    + Information about the Spanish Autonomous Communities from the Spanish Ministry of Health
    + Worldwide information from the European Centre for Disease Prevention and Control (ECDC)
The data is only updated once per day, so there is no need in rerunning this more often
It formats and merges both sources
It generates CSV files and images in PNG and SVG formats
The script is self-explanatory. Each subsection is illuminated
It intends to be a minimalistic template that can be easily modified and recycled
In its current state in enables comparing data from my country (Galicia)
and the rest of the world. It gives some peace of mind to my friends who live abroad...

REQUIREMENTS: Python 3 along with the following modules/libraries:
    + Pandas, wget, datetime, matplotlib

For sample images see:
https://sentidinho.eu/sentidinho/galicia-in-coronavirusland/

Differences between version 1 and 2:

- In version one the master script does some basic plotting. In version two it does not. Only the plot script plots.
- Version two creates two sets of CSV files and images: One for absolute data and the other for cumulative data (default).
- The plot script has been modified to expect no display. This was required in order to call the script from crontab.

What is new in version 3:

- Just one do-it-all script: It downloads, it parses, it plots.
- Now it plots cumulative and non-cumulative data for all countries with a death per million rate superior to Germany (included).
