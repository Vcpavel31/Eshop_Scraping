import requests
from bs4 import BeautifulSoup

def normalize(text) : 
    return ''.join([i if ord(i) < 128 else ' ' for i in text]).strip().split()

def Mironet_page(url):
    #get data from website
    page = requests.get(url)
    #parse data
    soup = BeautifulSoup(page.content, 'html.parser')
    #get number of pages
    pages = soup.find(class_="pagination").find_all(class_="PageNew")

    numpages = 0

    #iterate through pages
    for page in pages:
        if(int(page.get_text()) > numpages):
            numpages = int(page.get_text())

    return numpages

def Mironet(url):
    #get number of pages
    pages = Mironet_page(url)

    sites = []
    data = []

    #iterate from page one to last page (pages)
    for i in range(1, pages+1):
        #get data from website
        page = requests.get(url+'?PgID='+str(i))
        #parse data
        soup = BeautifulSoup(page.content, 'html.parser')
        #find all elements with class "item_b"
        sites.append(soup.find_all(class_="item_b"))
    for products in sites:
        for product in products:
            #find all elements with class "nazev"
            name = product.find(class_="nazev").get_text()
            #Get URL
            adresa = "https://www.mironet.cz"+product.find(class_="nazev").find('a').get('href')
            #remove new lines, tabs and multiple spaces from name
            name = name.replace('\n', '').replace('\t', '').replace('  ', '')
            #find all elements with class "item_b_cena"
            price = product.find(class_="item_b_cena").get_text()
            #join array of words to string from normalize(price)
            price = ''.join(normalize(price))
            #remove HTML spaces and "Kč" from price and convert to float
            price = float(price.replace('K', '').replace('Kč', '').replace('č', '').replace(' ', ''))
            #find all elements with class "item_b_popis"
            description = product.find(class_="item_b_popis").get_text()
            #remove new lines, tabs and multiple spaces from description
            description = description.replace('\n', '').replace('\t', '').replace('  ', '')
            #split description by '/'
            description_array = description.split('/')               

            capacity = 0
            divided = 99999

            #iterate through description_array
            for i in range(len(description_array)):
                #if description_array[i] is empty, remove it
                if description_array[i] == '':
                    del description_array[i]
                #does "Kapacita" in description_array[i] exist?
                if "Kapacita" in description_array[i]:
                    #if yes, save it withouth "Kapacita", "GB" and without spaces and convert to float
                    capacity = float(description_array[i].replace('Kapacita', '').replace('GB', '').replace(' ', ''))
                    divided = price/capacity*1000    
            data.append([name, adresa, price, capacity, description, divided])
    return data