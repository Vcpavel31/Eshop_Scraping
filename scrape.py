# Scrape from webiste and save to csv
import src.mironet as m
import src.czc as c

import csv
import urllib

url_mironet = "https://www.mironet.cz/pevne-disky-a-ssd/interni-disky/hdd/35-sas+c30318/"
url_czc = "https://www.czc.cz/disky/produkty?technologie-pevneho-disku=magneticky&format-disku=3-5_7&rozhrani=sas-12gb-s"

datas = m.Mironet(url_mironet)
datas += c.CZC(url_czc)


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