import model
import view

def game_loop():
        view.Welcome()
        buy_inputs = ['b','buy']
        sell_inputs = ['s','sell']
        lookup_inputs = ['l','lookup']
        quote_inputs = ['q','quote']
        value_inputs = ['a','add']
        leader_inputs = ['lb','leaderboard']
        balance_inputs = ['c','current balance']
        view_inputs = ['v','view']
        acceptable_inputs = buy_inputs + sell_inputs + lookup_inputs \
        + quote_inputs + value_inputs + leader_inputs + balance_inputs \
        + view_inputs
        user_input = input('What would you like to do:\n[b]uy,\n[s]ell,\n[l]ookup,\n[q]uote,\n[a]dd funds,\n[l]eader[b]oard,\n[c]urrent balance,\n[v]iew portfolio\n: ')

        if user_input in acceptable_inputs:
            if user_input in buy_inputs:
                model.buy(str(input('Ticker Symbol: ')),int(input('Number of Shares to buy: ')))
                input('Press any key to exit: ')
            elif user_input in sell_inputs:
                print(model.sell(input('Ticker Symbol: '),input('Number of Shares to sell: ')))
                input('Press any key to exit: ')
            elif user_input in lookup_inputs:
                print(model.get_lookup(input('Which company would you like to lookup?: ')))
                input('Press any key to exit: ')
            elif user_input in quote_inputs:
                print (model.get_quote(input('Enter ticker symbol of company for quote: ')))
                input('Press any key to exit: ')
            elif user_input in value_inputs:
                print (model.add_value(input('How much would you like to your account balance?: ')))
                input('Press any key to exit: ')
            elif user_input in leader_inputs:
                model.leaderboard()
                input('Press any key to exit: ')
            elif user_input in balance_inputs:
                model.current_balance()
                input('Press any key to exit: ')
            elif user_input in view_inputs:
                model.view_portfolio()
                input('Press any key to exit: ')
            game_loop()
        else:
            print ('incorrect entry')
            input('Press any key to exit: ')
            game_loop()
game_loop()
