import json
import csv
import sys
csv.field_size_limit(int(sys.maxsize/10000000000))

#Open the txt as 
data = []
with open('idsJson.txt', 'r',encoding="utf-8") as file:
    text = file.read()
    data = json.loads(text)

#get list of countries in the data
with open('countryList.csv', 'w',encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id","name","start","end","polygon","abbr"])

    for i in range(len(data)):
        name = data[i]["title"]
        dateStart = data[i]["from"]
        dateEnd = data[i]["to"]
        polygon = (data[i]["poly"]).replace(",",";")
        id = data[i]["opts"]["id"]
        abbr = data[i]["abbr"]
        typeCheck = data[i]["opts"]["type"]
        if typeCheck == 0:
            print("Skipping " + name + " as it is not a country")
            continue
        writer.writerow([id,name,dateStart,dateEnd,polygon,abbr])
