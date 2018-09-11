#!/usr/bin/env python3

import json
import requests
from orm import Database
import os
import time

def update_earnings(username):

    with Database('Terminal.db') as db:
        db.cursor.execute("""SELECT funds FROM users WHERE username='{}';""".format(username))
        funds = db.cursor.fetchone()[0]
        db.cursor.execute("""SELECT shares FROM stocks WHERE username='{}';""".format(username))
        shares = db.cursor.fetchall()
        db.cursor.execute("""SELECT company from stocks WHERE username='{}';""".format(username))
        ticker_symbol = db.cursor.fetchall()
        quotelist = []
        sharelist = []
        share_values = []
        tickerlist = []
        for all in ticker_symbol:
            quotelist.append(get_quote(all[0]))
            tickerlist.append(all[0])
        for all2 in shares:
            sharelist.append(all2[0])
        for x in range(len(quotelist)):
            share_values.append(quotelist[x]*sharelist[x])
        net_worth = funds + sum(share_values)
        earnings = net_worth - 10000.0
        db.cursor.execute("""UPDATE users SET earnings={} WHERE username='{}';""".format(earnings,username))
        print('Earnings have been updated...')
        input('Press any key to continue: ')


def create_login(username,password):
    with Database('Terminal.db') as db:
        password2 = input('Please confirm your password: ')
        if password == password2:
            create_admin = input('Would you like to make this user an admin?(Y/N): ')
            if create_admin.lower() == 'y':
                db.cursor.execute("""INSERT INTO users(username,password,funds, earnings, admin) VALUES('{}','{}', 10000.0, 0.0, {});""".format(username,password,True))
                return (username)
            elif create_admin.lower() == 'n':
                db.cursor.execute("""INSERT INTO users(username,password,funds, earnings, admin) VALUES('{}','{}', 10000.0, 0.0, {});""".format(username,password,False))
                return (username)
            else:
                print('Please enter a Y or N')
                create_login(input('What would you like your username to be?: '),input('Select a password: '))
        else:
            print('Your passwords did not match...please try again.')
            create_login(input('What would you like your username to be?: '),input('Select a password: '))


def login():
    with Database('Terminal.db') as db:
        print('Please Log in')
        username = input('What is your username?: ')
        password = input('What is your password?: ')
        try:
            db.cursor.execute("""SELECT username FROM users WHERE username='{}';""".format(username))
            username2 = db.cursor.fetchone()
            db.cursor.execute("""SELECT password FROM users WHERE username='{}';""".format(username))
            password2 = db.cursor.fetchone()
            if password == password2[0]:
                print('You are logged in.')
                update_earnings(username)
                return(username)
            else:
                print('Username or password is incorrect')
                answer = input('Would you like to create a new user?(Y/N)')
                if answer.lower()=='y':
                    username = create_login(input('What would you like you username to be?: '), input('Select a password: '))
                    return username
                elif answer.lower() =='n':
                    login()
        except:
            print('username or password is incorrect')
            answer = input('Would you like to create a new user?(Y/N): ')
            if answer.lower() == 'y':
                username = create_login(input('What would you like your username to be?: '), input('Select a password: '))
                return username
            elif answer.lower() == 'n':
                login()


def get_quote(ticker_symbol):
    try:
        url = 'http://dev.markitondemand.com/modapis/api/v2/quote/json?symbol={}'.format(ticker_symbol)
        quote = json.loads(requests.get(url).text)
        if quote['LastPrice'] == 'None' or quote['LastPrice'] == []:
            print('No results')
            get_quote(input('Please re-enter ticker symbol: '))
        else:
            return quote['LastPrice']
    except:
        print('Could not find company')
        get_quote(input('Please re-enter ticker symbol: '))

def get_lookup(company_name):
    url = 'http://dev.markitondemand.com/modapis/api/v2/lookup/json?input={}'.format(company_name)
    lookup = json.loads(requests.get(url).text)
    listofnames = []
    for dic in lookup:
        listofnames.append(dic['Symbol'])
        listofnames.append(dic['Name'])
    return ('Here are your results: ' ,listofnames)

def buy(ticker,num_shares):
    with Database('Terminal.db') as db:
        username = login()
        price = float(get_quote(ticker)) * num_shares
        db.cursor.execute("""SELECT funds FROM users WHERE username='{}';""".format(username))
        funds = db.cursor.fetchone()[0]
        if float(funds) >= float(price):
            difference_funds = float(funds) - float(price)
            db.cursor.execute("""UPDATE users SET funds={} WHERE username='{username}';""".format(difference_funds,username=username)
                             )
            try:
                db.cursor.execute("""SELECT shares FROM stocks WHERE username='{}' AND company='{}';""".format(username,ticker)
                         )
                old_shares = db.cursor.fetchone()[0]
                sum_shares = int(old_shares) + int(num_shares)
                db.cursor.execute("""UPDATE stocks SET shares={} WHERE username='{}' AND company='{}';""".format(sum_shares,username,ticker)
                                 )
            except:
                db.cursor.execute("""INSERT INTO stocks(username,company,shares) VALUES('{}','{}',{});""".format(username,ticker,num_shares)
                                 )
            print('You have successfully purchased {} stocks of "{}"'.format(str(num_shares),ticker))
        else:
            print('Insufficient Funds')

def sell(ticker,num_shares):
    with Database('Terminal.db') as db:
        username = login()
        price = float(get_quote(ticker))
        num_shares = int(num_shares)
        db.cursor.execute("""SELECT shares FROM stocks WHERE username='{}' AND company='{}';""".format(username,ticker)
                         )
        my_shares = db.cursor.fetchone()[0]
        db.cursor.execute("""SELECT funds FROM users WHERE username='{}';""".format(username)
                         )
        funds = db.cursor.fetchone()[0]
        if int(my_shares) >= num_shares:
            difference_shares = my_shares - num_shares
            sum_funds = funds + (price*num_shares)
            db.cursor.execute("""UPDATE stocks SET shares={} WHERE username='{}' AND company='{}';""".format(difference_shares,username,ticker)
                             )
            db.cursor.execute("""UPDATE users SET funds={} WHERE username='{}';""".format(sum_funds,username)
                             )
            return('You have sold {} shares for {}'.format(num_shares, ticker))
        else:
            return('Insufficient Shares... Please buy more')

def add_value(value):
    with Database('Terminal.db') as db:
        try:
            username = login()
            db.cursor.execute("""SELECT funds FROM users WHERE username='{}';""".format(username)
                          )
            old_val = db.cursor.fetchone()[0]
            new_val = float(value) + float(old_val)
            db.cursor.execute("""UPDATE users SET funds={} WHERE username='{}';""".format(new_val,username)
                         )
            return('Your new balance is {}.\n'.format(new_val))
        except:
            return('Please enter a valid amount. ')

def view_portfolio():
    with Database('Terminal.db') as db:
        try:
            username = login()
            db.cursor.execute("""SELECT * FROM stocks WHERE username='{}';""".format(username)
                             )
            all_table = db.cursor.fetchall()
            db.cursor.execute("""SELECT earnings FROM users WHERE username='{}';""".format(username))
            earnings = db.cursor.fetchone()[0]
            listofinfo = []
            print('\nYour current earnings are ' + str(earnings))
            if len(all_table) == 0:
                print('User does not own any shares')
            else:
                for each in all_table:
                    if each[3] == 0:
                        continue
                    else:
                        print('\nYou own ' + str(each[3]) + ' shares of ' + str(each[2])+ '\n')
        except:
            print('User does not own any shares')


def current_balance():
    with Database('Terminal.db') as db:
        try:
            username = login()
            db.cursor.execute("""SELECT funds FROM users WHERE username='{}';""".format(username)
                             )
            funds = db.cursor.fetchone()
            print('Your balance is currently ' + str(funds[0]))
        except:
            print('Could not find user')

def leaderboard():
    with Database('Terminal.db') as db:
        username = login()
        db.cursor.execute("""SELECT admin FROM users WHERE username='{}';""".format(username))
        admin_status = db.cursor.fetchone()[0]
        if admin_status == True:
            db.cursor.execute("""SELECT earnings FROM users ORDER BY earnings DESC;""")
            leaderearnings = db.cursor.fetchall()
            db.cursor.execute("""SELECT username FROM users ORDER BY earnings DESC;""")
            leaders = db.cursor.fetchall()
            print('The current standings are :')
            time.sleep(1)
            if len(leaders) <= 10:
                for x in range(len(leaders)):
                    print ('Rank:' + str(x+1) + ' is ' + str(leaders[x][0]) + ' with ' + str(leaderearnings[x][0]) + ' in earnings \n')
            else:
                for x in range(10):
                    print ('Rank:' + str(x+1) + ' is ' + str(leaders[x][0]) + ' with ' + str(leaderearnings[x][0]) + ' in earnings \n')
        else:
            print('You do not have admin status')
