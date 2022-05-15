# Scrape from webiste and save to csv
import src.mironet as m
import csv

url = "https://www.mironet.cz/pevne-disky-a-ssd/interni-disky/hdd/35-sas+c30318/"

datas = m.Mironet(url)

#create csv file
with open('hdd.csv', 'w', newline='') as csvfile:
    #create csv writer
    writer = csv.writer(csvfile, delimiter=';')
    #write header
    writer.writerow(['Nazev', 'Cena [Kč]', 'Kapacita [GB]', 'Kč/TB', 'Popis', 'URL'])
    #write data
    for data in datas:
        #write data to csv
        writer.writerow([data[0], "{:.2f}".format(data[2]).replace(".",","), "{:.2f}".format(data[3]).replace(".",","), "{:.2f}".format(data[5]).replace(".",","), data[4], data[1]])
    csvfile.close()