"""
    Proxy Singed.

"""
from flask import Flask, render_template, request, abort, Response, redirect
from urllib.parse import urlsplit
from requests import get


app = Flask(__name__.split('.')[0])
WHITELIST = [   "euw.api.pvp.net",
                "global.api.pvp.net"
                ]
app.config.update(TEMPLATES_AUTO_RELOAD=True)
API_KEY = "PLACEHOLDER"


"""
"""
@app.route('/<path:url>', methods=['GET'])
def proxy_singed(url):
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


"""
"""
@app.route('/', methods=['GET'])
def proxy_root():
    print("Requested root - serving index")
    return render_template('index.html')


"""
"""
def build_remote_url(url, query_string):
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


"""
"""
def is_whitelisted(url):
    base_url = urlsplit(url).netloc
    return base_url in set(WHITELIST)

if __name__ == 'Singed':
    app.run(host='127.0.0.1', port=9090)
