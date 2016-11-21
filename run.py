from app import *
from json import load
from os.path import exists


#Check the config exists
if exists('config.ini'):
    app.config.from_json('../config.ini')

    #Check port is set, otherwise use 9090
    port_number = 9090
    if 'HOST_PORT' in app.config.keys():
        port_number = app.config['HOST_PORT']

    #Check API_key is set
    try:
        print("API Key loaded: %s%s" %
              ("*" * (len(app.config['API_KEY'])-7),
               app.config['API_KEY'][-6:])
              )
        app.run(host='127.0.0.1', port=port_number)
    except Exception:
        exit("Please provide your RiotGames API key in the config.ini file. "
             "See the example config.")
else:
    exit("Please provide your RiotGames API key in the config.ini file. "
         "See the example config.")
