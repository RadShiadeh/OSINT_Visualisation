import os
from typing import List, Optional
import requests
from bs4 import BeautifulSoup as bs
import datetime
from logging import error, info

# years = 'https://armstrade.sipri.org/armstrade/html/tiv/swout.php'
# data = "https://armstrade.sipri.org/armstrade/html/tiv/index.php"

# dates.txt = "./data/date.txt"
# data.txt = "./data/data.txt"


# this is now depricated, since sipri changed their entire UI
def get_data(url_year: str, date_path: str, data_path: str, url_data) -> None:
    today = datetime.datetime.today().strftime('%d-%m-%y')

    latest_year = get_latest_entry(date_path)

    available_data = get_available_year_range(url_year, date_path)
    if not available_data:
        msg = "no new data available"
        error(msg)
        raise Exception(msg)
    elif available_data[-1] <= latest_year:
        msg = f"no new data available, latest entry is {latest_year} is >= available data: {available_data[-1]}"
        error(msg)
        raise Exception(msg)

    
    with open(data_path, 'w') as data_file:
        data_file.write("SIPRI Transfers Database \n\n\n")
        data_file.write(f" Database search results for buyer 'All Countries' and seller  'All Countries' and the years from {available_data[0]} to {available_data[1]} - (created: {today})\n\n")
        data_file.write("Deal ID;Seller;Buyer;Designation;Description;Armament category;Order date;Order date is estimate;Numbers delivered;Numbers delivered is estimate;Delivery year;Delivery year is estimate;Status;SIPRI estimate;TIV deal unit;TIV delivery values;Local production\n")

    for yr in range(available_data[0], available_data[1]+1):
        payload = {'altout':'C', #needs to be C idk why - probs for csv
        'filetype':'DealsAndTIVs.txt', #Name of the file
        'low_year':str(yr), #Start year
        'high_year':str(yr), #End year
        'buyer':'All',
        'seller': 'All'
        }

        try:
            res = requests.post(url_data, data=payload).text.split('\n')

            no_data_res = "No data found"
            if res[0] == no_data_res:
                info(f"no new data or no data for {yr}")
                continue
            
            with open(data_path, 'a') as data_file:
                for i in range(6, len(res)-2):
                    data_file.write(res[i] + '\n')
            
            info(f"data fetched for {yr}")
        except requests.RequestException as e:
            msg = f"failed to post a request to {url_data} for year {yr}\n" + str(e)
            error(msg)
            raise RuntimeError(msg) from e
    

    update_dates(date_path, available_data[-1])

    info("data collected")
    return


def update_dates(dates_path: str, last_entry: int) -> None:
    info("updating dates")

    with open(dates_path, 'w') as dates_file:
        dates_file.write(last_entry)

    info("done")



def get_latest_entry(date_path: str) -> Optional[int]:

    if not os.path.exists(date_path):
        msg = "date.txt path is incorrect or non existant"
        error(msg)
        raise FileNotFoundError(msg)
    
    with open(date_path, 'r') as f:
        return int(f.readline().strip())


def get_available_year_range(url: str, dates_path: str) -> List[str]:
    try:
        html_res = requests.get(url).text
        soup = bs(html_res, 'html.parser')
        years = soup.find_all('select', {'name':'low_year'})[0].find_all('option')

        if not years or len(years) < 1:
            msg = f"no years is empty, sth went wrong gaining making a request to {url}"
            error(msg)
            raise Exception(msg)
        
        year_max = years[1].text
        year_min = years[-1].text
        lines = ""

        with open(dates_path, 'r') as file:
            lines = file.readlines()

        if lines[0] == year_max:
            return []
        
        return [int(year_min), int(year_max)]
    except requests.RequestException as e:
        msg = f"failed to send a get req to {url} and get the year ranges\n" + str(e)
        error(msg)
        raise requests.RequestException(msg)