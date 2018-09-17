#!/flask/bin/python3

from flask import Flask, jsonify
import model

app = Flask(__name__)
    

@app.route('/<apikey>/balance', methods=['GET'])
def current_balance(apikey):
    username = model.api_authenticate(apikey)
    if not username:
        return jsonify({'error': 'could not authenticate'})
    return jsonify({'username': username, 'balance': model.current_balance(username)})
    return('API Trader')

@app.route('/<apikey>/<company_name>', methods=['GET'])

def lookup(apikey, company_name):   
    username = model.api_authenticate(apikey)
    if not username:
        return jsonify({'error': 'could not authenticate'})
    return jsonify({'Username': username, 'balance': model.current_balance(username), 'Results': model.get_lookup(company_name)})

@app.route('/<apikey>/leaderboards', methods=['GET'])
def leaderboards(apikey):
    username = model.api_authenticate(apikey)
    lb = model.leaderboard(username)
    if not username:
        return jsonify({'error': 'could not authenticate'})
    if not lb:
        return jsonify({'error': 'No leaderboards yet...'})
    return jsonify({'leaderboards': lb})
    
if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
