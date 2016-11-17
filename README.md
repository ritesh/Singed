# Singed

![Singed](https://ddragon.leagueoflegends.com/cdn/6.22.1/img/champion/Singed.png)

Python web service (super basic), to act as middleware between riot games and RiotKit. 

1. At startup, using the API key, fetch and construct all the valid URLS for the riot API.
2. These domains will become whitelisted and will also be used for validation.
	1. `singed.riotkit.xyz/domain_list`
3. The whitelist will be communicated to the library upon request.

Requests will come in like so:
`singed.riotkit.xyz/<some_api_domain/<query_string>`

Singed will be responsible for validation of everything after `.xyz/`.
This will then be transformed into:
`https://<some_api_domain/<query_string>+api_key=<KEY>`
The request will be issued and returned back to the requester (library).

The url in this case is `singed.riotkit.xyz` but will be a configuration value in the library. Singed will be useable for CI testing throughout development with my development API key.

# Usage
1. Place your API key in the source. (TODO - move to config)
2. Run Singed like so:

```
$ export FLASK_APP=Singed.py
$ python3.5 -m flask run
```