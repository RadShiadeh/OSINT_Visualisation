
ingestion.py:
    This is a comprehensive project, a lot of the scripts written here are one off except the pipline folder, which was initially designed to call the sipri database for new data, to then be used in the trade visualisation website we created

    Sipri changed their UI and API endpoints as of March 2024, making it much simpler to obtain the data (you can get all relevant data already in csv format) so there is no need for that pipline anymore... I included it regardless.

    The website used to be pure html, with no option to download data, which meant making post requests and write the raw data into a text file

    There are two databases... one is trade registers or transfer of major weapon deal (1950 - 2021) and another one being the main database looking at the trade data between countaries from 1950 - 2022

reader.py:
    this was designed to wrangle data, find relative info making data frames and outputting local CSV files to be later used for community detection and ML attempts


map folder:
    we have a list of countries and their borders... this is processing data to later be used in the visualisation website for creating the boarders visually

    the script first gets a list of IDS, stores it in newIDSJson.txt (ik its not JSON, I blame past me, but the format of it is JSON but stored as a txt file for some reason)
    that is then used to create a CSV file of borders of a given country from a given date start to end... if end is 9999 then its till.... running countries.py should give the files... they are not included because Github doesnt like it (too large)