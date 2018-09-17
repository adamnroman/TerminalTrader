#!/usr/bin/env python3

import json
import requests

def get_quote(ticker_symbol):
    url = 'http://dev.markitondemand.com/modapis/api/v2/quote/json?symbol={}'.format(ticker_symbol)
    quote = json.loads(requests.get(url).text)
    return quote['LastPrice']

def get_lookup(company_name):
    url = 'http://dev.markitondemand.com/modapis/api/v2/lookup/json?input={}'.format(company_name)
    lookup = json.loads(requests.get(url).text)
    for dic in lookup:
        listofnames.append(dic['Symbol'])
        listofnames.append(dic['Name'])
    return listofnames

def buy(ticker,num_shares):
    price = float(get_quote(ticker))
    num_shares = int(num_shares)
    if funds >= (price*num_shares):
        funds = funds - (price*num_shares) #this is subtracting the funds
        # add the shares to the database for the given user
    else:
        ##error not enough funds

def sell(ticker,num_shares):
    price = float(get_quote(ticker))
    num_shares = int(num_shares)
    if my_shares >= num_shares:
        funds = funds + (price*num_shares) ## add the funds to the database for user
        ## shares need to be subtracted from database
