import json

data = {
    'Item Querries' : [
        {
            'url': "https://e3d-online.com/products/revo-hemera", 
            'actions': [    {'hover':'//*[@id="39800258756667"]/div[2]/div[2]'},
                            {'click':'//*[@id="39800258756667"]/div[2]/div[2]/div/div/button[2]'},
                            {
                                'read':'//*[@id="configurator"]/div/div/div[2]/div[3]/div/div/span',
                                'read_to': 'price',
                                'action':[
                                    {'remove':' incl. VAT'},
                                    {'remove':'£'},
                                    {'to_float':'1'}
                                ]
                            },
                            {
                                'read':'//*[@id="configurator"]/div/div/div[2]/div[3]/div/div/span',
                                'read_to': 'currency', 
                                'action':[
                                    {'remove':' incl. VAT'},
                                    {'no_digit':''},
                                    {'remove':'.'}
                                ]
                            }                                                                                    
                        ],
            'Category' : 'Extruders'
        },
        {
            'url': "https://www.i4wifi.cz/cs/232319-ubnt-unifi-switch-usw-flex-mini",
            'actions': [ {
                                'read':'//*[@id="ProductDetailPrices"]/table/tbody[1]/tr[6]/td[2]/strong',
                                'read_to': 'price',
                                'action':[
                                    {'remove':'Kč'},
                                    {'remove':' '},
                                    {'to_float':'1'}
                                ]
                            }
                        ]
        }
    ],
    'Search Querries' : [
        {
            'URL' : 'https://www.mironet.cz/pevne-disky-a-ssd/interni-disky/hdd/35-sas+c30318/',
            'Eshop' : 'Mironet',
            'Category' : 'SAS Drives'
        },
        {
            'URL' : 'https://www.czc.cz/disky/produkty?technologie-pevneho-disku=magneticky&format-disku=3-5_7&rozhrani=sas-12gb-s',
            'Eshop' : 'CZC',
            'Category' : 'SAS Drives'
        }
    ]
}

with open('json_data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4, sort_keys=True)