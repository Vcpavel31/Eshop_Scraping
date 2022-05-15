
#############################################################################################################
## Alza.cz bot validation -------- Not working yet --------
#############################################################################################################


from re import S
import requests
from bs4 import BeautifulSoup

def Alza(url):

    data = []
    sites = []
    pages = 1
    i = 1

    while(pages):
        #get data from website
        page = requests.get(url.replace("&pg=1&", "&pg="+str(i)+"&"))
        #parse data
        soup = BeautifulSoup(page.content, 'html.parser')
        #find all elements with id "boxc"
        print(soup)
        sites.append(soup.find("div", {"id": "boxc"}))

        print(sites)
        i += 1
        if(soup.find("div", {"id": "boxc"}).find(class_="clear")): #empty
            pages = 0
    
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

print(Alza("https://www.alza.cz/interni-pevne-disky/18851840.htm#f&cst=null&cud=0&pg=1&prod=&sc=755"))#"https://www.alza.cz/harddisky-3-5/18849714.htm#f&cst=null&cud=0&pg=1&prod=&par281=281-1038&sc=1155"))