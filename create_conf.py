import configparser

config = configparser.ConfigParser()

config['Default'] = {   'json': 'json_data.json',
                        'export_csv': 'False',
                        'export_mysql': 'True'}

config['MySQL'] = {     'host': 'x.x.x.x',
                        'port': '3306',
                        'user': 'root',
                        'password': 'password'}
    
with open('scrape.conf', 'w') as configfile:
    config.write(configfile)