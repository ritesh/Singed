__author__ = "Grant Douglas"
__credits__ = ["Grant Douglas"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Grant Douglas"
__email__ = "me@hexplo.it"
__status__ = "Production"


#Imports
from flask import Flask, render_template, request, abort, Response, redirect
from urllib.parse import urlsplit
from requests import get
from os.path import exists
import configparser


#Globals
config = None
app = Flask(__name__.split('.')[0])
WHITELIST = [   "euw.api.pvp.net",
                "global.api.pvp.net"
                ]
app.config.update(TEMPLATES_AUTO_RELOAD=True)
API_KEY = None #DO NOT SET API_KEY here. Set it in the config.ini


@app.route('/<path:url>', methods=['GET'])
def proxy_singed(url):
    """
        Receives the incoming requests, and builds the RiotGames URL for the
        outgoing comms.

        Args:
            url: The incoming URL.
        Returns:
            the HTML response from the outgoing request that we issue.
        Raises:
            abort(403): we will issue an HTTP 403 code if appropriate.
    """
    if "favicon.ico" in url:
        abort(403)
    endpoint_url = build_remote_url(url, request.query_string)
    if endpoint_url != "":
        print("Fetching %s" % endpoint_url)
        r = get(endpoint_url, stream=True , params=request.args)
        print("Status: %s" % r.status_code)
        return Response(r, content_type=r.raw.headers['Content-Type'])
    else:
        print("Issue with URL:", endpoint_url)
    abort(403)


@app.route('/', methods=['GET'])
def proxy_root():
    """
        Handles requests for the document root.
        We have a basic README HTML document that we'll serve up.

        Returns:
            the HTML for the index.html template.
    """
    print("Requested root - serving index")
    return render_template('index.html')


def build_remote_url(url, query_string):
    """
        Takes the incoming URL, validates it using the whitelist and then
        constructs the outgoing URL with the API key.

        Args:
            url: The incoming URL to be used for outgoing URL construction.
            query_string: the GET query string. We will use this to build the API
            key parameter in appropriately.
        Returns:
            the riotgames API url for the request
        Raises:
            abort(403): we will issue an HTTP 403 code if appropriate.
    """
    url = 'https://%s' % url
    # Check if the host is whitelisted.
    if is_whitelisted(url):
        query = str(query_string, 'utf-8')
        # Stitch in API key
        if query:
            url = "%s?%s&api_key=%s" % (url, query, API_KEY)
        else:
            url = url + "?api_key=%s" % API_KEY
    else:
        print("URL is not approved: ", url)
        abort(403)
        return ""
    return url


def is_whitelisted(url):
    """
        Deconstructs the URL using `urlsplit` to determine if the domain is in
        our whitelist.

        Args:
            url: The incoming URL to be used for validation
        Returns:
            either `True` or `False`, depending on whether or not `url` is
            whitelisted
    """
    base_url = urlsplit(url).netloc
    return base_url in set(WHITELIST)


if __name__ == 'Singed':
    #Load the config from disk
    config = configparser.ConfigParser()
    if not exists('config.ini'):
        exit("Please make sure you have created the config.ini file")
    config.read('config.ini')
    #Check port is set, otherwise use 9090
    port_number = 9090
    cfg_port = int(config['Singed']['HOST_PORT'])
    if cfg_port:
        port_number = cfg_port
    #Check API_key is set
    API_KEY = config['Singed']['API_KEY']
    if API_KEY and len(API_KEY) > 5:
        print("API Key loaded: %s%s" % ("*" * (len(API_KEY)-7), API_KEY[-6:]))
        app.run(host='127.0.0.1', port=port_number)
    else:
        exit("Please provide your RiotGames API key in the config.ini file")
