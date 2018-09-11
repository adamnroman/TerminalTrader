""" TerminalTrader
 This file allows you to buy, sell, view portfolio, and view leaderboards of top earners among the users.
 Uses sqlite3 for database and python3 for framework
 There are four main files in use...
   -controller.py runs the application and only holds code that reads the user input and runs the home page.
   -model.py holds most of the functions that make up the application. This doesn't need to be touched, but it is imported         from the controller.py file. 
   -orm.py contains a class that allowed me to make sqlite3 database changes without having to open and close the connection       over and over.
   -view.py is a work in progress. I don't believe I call it in any functions, but the intention was to put all the repetitive     'view' related code in it.
