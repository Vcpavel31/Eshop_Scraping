# Scrape from webiste and save to csv
import src.mironet as m
import src.czc as c
import src.items as i
#Imports
import csv
import mysql.connector
import configparser
import json
import os

config = configparser.ConfigParser()
config.read('scrape.conf')

with open(config["Default"]["json"]) as json_file:
    i_data = json.load(json_file)
    print(json.dumps(i_data, indent=4, sort_keys=True))

export_csv = config["Default"]["export_csv"]
export_mysql = config["Default"]["export_mysql"]

datas=[]

for search in i_data["Search Querries"]:
#    print(search)
    if search["Eshop"] == "Mironet":
        datas += m.scrape(search["URL"])
    elif search["Eshop"] == "CZC":
        datas += c.scrape(search["URL"])

for search in i_data["Item Querries"]:
    print(search)
    fucku = i.scrape(search['url'], search['actions'])
    datas.append(fucku) 




print(json.dumps(datas, indent=4, sort_keys=True))
seen = []
new_l = []

for d in datas:
    print(d)
    if d not in seen:
        mezi = {}
        seen.append(d)
        for key, value in d.items():
            mezi[key.lower()] = value
        new_l.append(mezi)
datas = new_l

print(json.dumps(datas, indent=4, sort_keys=True))

#    t = tuple(d.items())
#     
#         seen.add(t)
#         new_l.append(d)

# seen = set()
# new_l = []
# for d in datas:
#     t = tuple(d.items())
#     if t not in seen:
#         seen.add(t)
#         new_l.append(d)

# os.system('clear')
# print(json.dumps(datas, indent=4, sort_keys=True))
# datas = {k.lower(): v for k, v in new_l}

# print(json.dumps(datas, indent=4, sort_keys=True)) 

if(export_csv == "True"):
    #create csv file
    with open('hdd.csv', 'w', newline='') as csvfile:
        #create csv writer
        writer = csv.writer(csvfile, delimiter=';')
        #write header
        writer.writerow(['Nazev', 'Cena [Kč]', 'Kapacita [GB]', 'Kč/TB', 'Popis', 'URL'])
        #write data
        for data in datas:
            #write data to csv
            writer.writerow([data['name'], "{:.2f}".format(data['price']).replace(".",","),
                            "{:.2f}".format(data['capacity']).replace(".",","), "{:.2f}".format(data['divided']).replace(".",","),
                            data['description'], data['address']])
        csvfile.close()

if(export_mysql == "True"):
    mydb = mysql.connector.connect(
        host=config["MySQL"]["host"],
        port=config["MySQL"]["port"],
        user=config["MySQL"]["user"],
        password=config["MySQL"]["password"],
        database="Ceny"
    )

    mycursor = mydb.cursor()

    for data in datas:
        print(data)
        mycursor.execute('SELECT `Item`,`ID`  FROM `URLs` WHERE `URL` = "'+str(data['address'])+'"')
        try:
            myresult = mycursor.fetchone()
            #print(myresult[0])
            sql = "INSERT INTO `Price`(`Item_ID`, `Date`, `Price`, `URL`) VALUES (%s, CURRENT_TIMESTAMP, %s, %s)"
            val = (myresult[0], data['price'], myresult[1])
            mycursor.execute(sql, val)
            mydb.commit()
        # empty response from Mysql
        except Exception as e:
            print("Empty response from Mysql")
            mycursor.execute('SELECT `ID` FROM `Items` WHERE `Name` = "',data['name'],'"')
            try:
                myresult = mycursor.fetchone()
                #print(myresult)
                sql = "INSERT INTO `URLs`(`Item`, `Description`, `URL`, `Name`) VALUES (%s, %s, %s, %s)"
                val = (myresult[0], data['description'], data['address'], data['name'])
                mycursor.execute(sql, val)
                mydb.commit()
                sql = "INSERT INTO `Price`(`Item_ID`, `Date`, `Price`, `URL`) VALUES (%s, CURRENT_TIMESTAMP, %s, %s)"
                val = (myresult[0], data['price'], mycursor.lastrowid)
                mycursor.execute(sql, val)
                mydb.commit()
            except:
                print("Creating new item")
                sql = "INSERT INTO `Items`(`Name`, `Capacity [GB]`) VALUES (%s, %s)"
                val = (data['name'], data['capacity'])
                mycursor.execute(sql, val)
                Item_ID = mycursor.lastrowid
                print("1 record inserted, ID:", Item_ID)
                mydb.commit()
                sql = "INSERT INTO `URLs`(`Item`, `Description`, `URL`, `Name`) VALUES (%s, %s, %s, %s)"
                val = (Item_ID, data['description'], data['address'], data['name'])
                mycursor.execute(sql, val)
                mydb.commit()
                sql = "INSERT INTO `Price`(`Item_ID`, `Date`, `Price`, `URL`) VALUES (%s, CURRENT_TIMESTAMP, %s, %s)"
                val = (Item_ID, data['price'], mycursor.lastrowid)
                mycursor.execute(sql, val)
                mydb.commit()