#!/usr/bin/env python3

import sqlite3
## class is a programmer defined type
class Database:

    def __init__(self,name_of_db):
        self.connection = sqlite3.connect(name_of_db,check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.connection.close()
