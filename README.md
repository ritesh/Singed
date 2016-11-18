# Proxy Singed

![Singed](https://ddragon.leagueoflegends.com/cdn/6.22.1/img/champion/Singed.png)

Python web service (super basic), to act as middleware between riot games and RiotKit. 

## Use case:
Requests come in like so:
`https://<your_domain>/<some_api_domain/<query_string>`

This will then be transformed into:
`https://<riotgames_api_domain>/<query_string>&api_key=<KEY>`<br />

The response will then be delivered to the original requester (I.e. the [RiotKit](https://git.hexplo.it/RiotKit/RiotKit) library).

Once you host Proxy Singed somewhere, you'll need to set the URL in the [RiotKit](https://git.hexplo.it/RiotKit/RiotKit) config.

## Usage
1. Rename [`config.example.ini`](config.example.ini) to `config.ini` and set your Riot Games API key.
2. Now run Singed like shown below: 
```
$ export FLASK_APP=Singed.py
$ python3.5 -m flask run
```
3. You will then need to set up nginx or Apache2 as the reverse proxy to handle port redirection/SSL etc.
