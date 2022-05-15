# Scrape from webiste and save to csv
import src.mironet as m
import src.czc as c
#Imports
import csv
import mysql.connector
import configparser

export_csv = False
export_mysql = True

url_mironet = "https://www.mironet.cz/pevne-disky-a-ssd/interni-disky/hdd/35-sas+c30318/"
url_czc = "https://www.czc.cz/disky/produkty?technologie-pevneho-disku=magneticky&format-disku=3-5_7&rozhrani=sas-12gb-s"

datas = m.Mironet(url_mironet)
datas += c.CZC(url_czc)

if(export_csv):
    #create csv file
    with open('hdd.csv', 'w', newline='') as csvfile:
        #create csv writer
        writer = csv.writer(csvfile, delimiter=';')
        #write header
        writer.writerow(['Nazev', 'Cena [Kč]', 'Kapacita [GB]', 'Kč/TB', 'Popis', 'URL'])
        #write data
        for data in set(map(tuple, datas)):
            #write data to csv
            writer.writerow([data[0], "{:.2f}".format(data[2]).replace(".",","),
                            "{:.2f}".format(data[3]).replace(".",","), "{:.2f}".format(data[5]).replace(".",","),
                            data[4], data[1]])
        csvfile.close()

if(export_mysql):
    config = configparser.ConfigParser()
    #config['MySQL'] = {'host': 'x.x.x.x',
    #                  'port': '3306',
    #                  'user': 'root',
    #                  'password': 'password'}
    #with open('mysql.conf', 'w') as configfile:
    #    config.write(configfile)
    config.read('mysql.conf')

    mydb = mysql.connector.connect(
        host=config["MySQL"]["host"],
        port=config["MySQL"]["port"],
        user=config["MySQL"]["user"],
        password=config["MySQL"]["password"],
        database="Ceny"
    )

    mycursor = mydb.cursor()

    for data in set(map(tuple, datas)):
        mycursor.execute('SELECT `Item`,`ID`  FROM `URLs` WHERE `URL` = "'+str(data[1])+'"')
        try:
            myresult = mycursor.fetchone()
            print(myresult[0])
            sql = "INSERT INTO `Price`(`Item_ID`, `Date`, `Price`, `URL`) VALUES (%s, CURRENT_TIMESTAMP, %s, %s)"
            val = (myresult[0], data[2], myresult[1])
            mycursor.execute(sql, val)
            mydb.commit()
        # empty response from Mysql
        except Exception as e:
            pass
            print("Empty response from Mysql")
            mycursor.execute('SELECT `ID` FROM `Items` WHERE `Name` = "',data[0],'"')
            try:
                myresult = mycursor.fetchone()
                print(myresult)
                sql = "INSERT INTO `URLs`(`Item`, `Description`, `URL`, `Name`) VALUES (%s, %s, %s, %s)"
                val = (myresult[0], data[4], data[1], data[0])
                mycursor.execute(sql, val)
                mydb.commit()
                sql = "INSERT INTO `Price`(`Item_ID`, `Date`, `Price`, `URL`) VALUES (%s, CURRENT_TIMESTAMP, %s, %s)"
                val = (myresult[0], data[2], mycursor.lastrowid)
                mycursor.execute(sql, val)
                mydb.commit()
            except:
                print("Creating new item")
                sql = "INSERT INTO `Items`(`Name`, `Capacity [GB]`) VALUES (%s, %s)"
                val = (data[0], data[3])
                mycursor.execute(sql, val)
                Item_ID = mycursor.lastrowid
                print("1 record inserted, ID:", Item_ID)
                mydb.commit()
                sql = "INSERT INTO `URLs`(`Item`, `Description`, `URL`, `Name`) VALUES (%s, %s, %s, %s)"
                val = (Item_ID, data[4], data[1], data[0])
                mycursor.execute(sql, val)
                mydb.commit()
                sql = "INSERT INTO `Price`(`Item_ID`, `Date`, `Price`, `URL`) VALUES (%s, CURRENT_TIMESTAMP, %s, %s)"
                val = (Item_ID, data[2], mycursor.lastrowid)
                mycursor.execute(sql, val)
                mydb.commit()