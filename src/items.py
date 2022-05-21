from re import A
from tkinter.messagebox import NO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

#def If_element_is_here_do_click(browser, xpath_arg):
#        executed = 0
#        while (executed == 0):
#            try:
#                browser.find_element(By.XPATH, xpath_arg).click()
#                executed = 1
#                print("Clicked")
#            except:
#                print("No")
#                time.sleep(0.5)

def scrape(url, actions):
    browser = webdriver.Chrome()
    browser.get(url)

    data = {"Name": None, "Address": url}
    time.sleep(2)
    for action in actions:
        time.sleep(0.5)
        if "hover" in action:
            #hover over element
            element = browser.find_element(By.XPATH, action["hover"])
            print("Hovering over element",element)
            hover = ActionChains(browser).move_to_element(element)
            time.sleep(0.5)
            hover.perform()
    
        if "click" in action:
            browser.find_element(By.XPATH, action['click']).click()

        if "read" in action:
            value = browser.find_element(By.XPATH, action["read"]).text
            for event in action['action']:

                if 'remove' in event:
                    value = value.replace(event['remove'], '')

                if 'split' in event:
                    value = value.split(event['split'])

                if 'to_float' in event:
                    #remove all non-numeric characters
                    value = value.replace(' ', '').replace('\n', '').replace('\t', '')
                    #remove all symbols
                    value = float(value)

                if 'no_digit' in event:
                    value = ''.join([i for i in value if not i.isdigit()])

                if 'set_to' in event:
                    value = event['set_to']
                    
                if 'array_index' in event:
                    value = value[event['array_index']]

            data[action['read_to']] = value
        
    browser.close()
    return (data)
"""
data = scrape(  url = "https://e3d-online.com/products/revo-hemera", 
                actions = [ {'hover':'//*[@id="39800258756667"]/div[2]/div[2]'},
                            {'click':'//*[@id="39800258756667"]/div[2]/div[2]/div/div/button[2]'},
                            {
                                'read':'//*[@id="configurator"]/div/div/div[2]/div[3]/div/div/span',
                                'read_to': 'Price',
                                'action':[
                                    {'remove':' incl. VAT'},
                                    {'remove':'£'},
                                    {'to_float':'1'}
                                ]
                            },
                            {
                                'read':'//*[@id="configurator"]/div/div/div[2]/div[3]/div/div/span',
                                'read_to': 'Currency', 
                                'action':[
                                    {'remove':' incl. VAT'},
                                    {'no_digit':''},
                                    {'remove':'.'}
                                ]
                            }                                                                                    
                        ])

print(data)
"""