import csv
import json
import csv
 
def csv_to_json(csv_file_path, json_file_path):
    data_dict = {}
    with open(csv_file_path, encoding = 'utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler) 
        for rows in csv_reader:
            #assuming a column named 'No'
            #to be the primary key
            key = rows['Deal ID']
            data_dict[key] = rows


    with open(json_file_path, 'w', encoding = 'utf-8') as json_file_handler:
        json_file_handler.write(json.dumps(data_dict, indent = 4))

 
#Step 1
csv_file_path = "./data"
json_file_path = "./data"
 
csv_to_json(csv_file_path, json_file_path)