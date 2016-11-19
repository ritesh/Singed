# Proxy Singed

[![Twitter](https://img.shields.io/badge/twitter-@Hexploitable-blue.svg?style=flat)](http://twitter.com/Hexploitable)
[![GitHub version](https://badge.fury.io/gh/RiotKit%2FSinged.svg)](https://badge.fury.io/gh/RiotKit%2FSinged)

![Singed](https://ddragon.leagueoflegends.com/cdn/6.22.1/img/champion/Singed.png)

Python web service (super basic), to act as middleware between riot games and RiotKit. 

## Requirements
There are only a couple of requirements:-
- A flavour of Python 3
- Python `flask` module
- Python `requests` module

## Use case:
Proxy Singed is a super simple and lightweight Python Flask application to run between the RiotGames and RiotKit towers. 

Essentially, Proxy Singed will act as your middle man between the RiotKit framework and the Riot Games API. You'll host Proxy Singed somewhere on the web, provide the URL to RiotKit in your application, and Singed will make sure all traffic lands at Riot with your API key.

## Usage
1. Rename [`config.example.ini`](config.example.ini) to `config.ini` and set your Riot Games API key.
2. Now run Singed like shown below: 
```
$ export FLASK_APP=Singed.py
$ python3.5 -m flask run
```
3. You will then need to set up nginx or Apache2 as the reverse proxy to handle port redirection/SSL etc.
