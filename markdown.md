downloader.py:
    originally responsible for scraping data from sipri, but sipri revamped their UI, making the need for the scraper obsolete since I can just input years and get all the data already formatted in csv format now... data.txt has the original file an as far as my research go, the original is no longer accessible as Sipri changed the entire db as of March 2024: "https://armstransfers.sipri.org/ArmsTransfer/".

    the original project was scraping pure HTML static page, and it is locally saved in data.txt


make a data pipline:
    1 api rec get the csv done
    2 rtf done 
    3 clean both
    4 join
    5 create numeric
    6 parse json for the web
    7 build communitty mappings
    8 figure out ML stuff, what is milex data