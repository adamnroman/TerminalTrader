import sqlite3
from orm import Database

with Database('Terminal.db') as db:
    db.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               pk INTEGER PRIMARY KEY AUTOINCREMENT,
               username VARCHAR,
               password VARCHAR,
               funds FLOAT,
               earnings FLOAT,
               apikey VARCHAR,
               admin BOOL);"""
               )
    db.cursor.execute("""CREATE TABLE IF NOT EXISTS stocks(
               pk INTEGER PRIMARY KEY AUTOINCREMENT,
               username VARCHAR,
               company VARCHAR,
               shares INTEGER
               );"""
               )
