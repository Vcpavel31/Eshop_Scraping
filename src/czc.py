from re import S
import requests
from bs4 import BeautifulSoup

def CZC_page(url):
    #get data from website
    page = requests.get(url)
    #parse data
    soup = BeautifulSoup(page.content, 'html.parser')
    #get number of pages
    pages = int(soup.find(class_="paging").find(class_="last").get_text())
    #return number of pages
    return pages

def CZC(url):
    #get number of pages
    pages = CZC_page(url)

    data = []
    sites = []

    #iterate from page one to last page (pages)
    for i in range(1, pages+1):
        #get data from website
        page = requests.get(url+'&q-first='+str((i-1)*27))
        #parse data
        soup = BeautifulSoup(page.content, 'html.parser')
        #find all divs with id "tiles"
        sites.append(soup.find("div", {"id": "tiles"}).find_all(class_="new-tile"))
        print(i) #print current page because it is very slow

    for products in sites:
        for product in products:
            #find all elements with class "tile-title"
            name = product.find(class_="tile-title").find('a').get_text()
            #remove new lines, tabs and multiple spaces from name
            name = name.replace('\n', '').replace('\t', '').replace('  ', '')

            #Get URL
            adresa = "https://www.czc.cz"+product.find(class_="tile-title").find('a').get('href')

            #find all elements with class "price-vatin"
            price = product.find(class_="price-vatin").get_text().encode('utf-8')
            #remove HTML spaces and "Kč" from price and convert to float
            price = float(str(price.decode('utf-8')).strip().encode('ascii', 'ignore').decode('ascii').replace('Kč', '').replace('K', '').replace(' ', ''))
            print(price," - ", product.find(class_="price-vatin").get_text())

            #find all elements with class "tile-desc"
            description = product.find(class_="tile-desc").get_text()
            #remove new lines, tabs and multiple spaces from description
            description = description.replace('\n', '').replace('\t', '').replace('  ', '')

            parameters = product.find(class_="tile-params").find_all('p')
            for parameter in parameters:
                if(parameter.find(class_="param-label").get_text().find('Kapacita [GB]:') != -1):
                    capacity = float(str(parameter.find(class_="param-value").get_text().encode('utf-8').decode('utf-8')).strip().encode('ascii', 'ignore').decode('ascii').replace('Kč', '').replace('K', '').replace(' ', '')) 

            divided = price/capacity*1000    

            data.append([name, adresa, price, capacity, description, divided])
    return data


#url_czc = "https://www.czc.cz/disky/produkty?technologie-pevneho-disku=magneticky&format-disku=3-5_7&rozhrani=sas-12gb-s"

#print(CZC(url_czc))