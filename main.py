from api import IdenaAPI
# Connect to local node with default settings (with no Custom api)
api = IdenaAPI()
api = IdenaAPI(api_key="example")


def get_info():
    myaddr = api.address()["result"]
    mybalance = api.balance(myaddr)["result"]["balance"]
    highestBlock = api.sync_status()["result"]["highestBlock"]
    nodever = api.node_version()["result"]
    print("Address: " + myaddr)
    print("Balance: " + str(mybalance))
    print("Highest Block: " + str(highestBlock))
    print("Node Version: " + nodever)
    stats = {
        "Address": myaddr,
        "Balance": mybalance,
        "Block": highestBlock,
        "Node Version": nodever
    }
    return stats
                
def search_tx(txhash):
    tx = api.transaction(txhash)["result"]
    return tx
def balance_of(addr):
    bal = api.balance(addr)["result"]["balance"]
    return bal

def faucet_send(to):
    myaddr = api.address()["result"]
    result = api.send(myaddr, to, 1)
    return result["result"]


# an object of WSGI application
from flask import Flask, redirect, request
app = Flask(__name__)   # Flask constructor
  
# A decorator used to tell the application
# which URL is associated function

@app.route('/addr/<addr>')
def addr(addr):
    html = "<tr><td><a href='/'>Back</a></td></tr>"
    html += "<table>"
    try:
        bal = balance_of(addr)
        html += "<tr><td>Address</td><td>" + addr + "</td></tr>"
        html += "<tr><td>Balance</td><td>" + str(bal) + "</td></tr>"
    except:
        html += "<tr><td>Balance</td><td>Invalid Address</td></tr>"
    html += "</table>"
    return html
@app.route('/tx/<txhash>')
def tx(txhash):
    tx = search_tx(txhash)
    html = "<table>"
    html += "<tr><td><a href='/'>Back</a></td></tr>"
    for key, value in tx.items():
        html += "<tr><td>" + key + "</td><td>" + str(value) + "</td></tr>"
    html += "</table>"
    return html
@app.route('/block_at/<height>')
def block_at(height):
    try:
        block = api.block_at(int(height))["result"]
        html = "<table>"
        html += "<tr><td><a href='/'>Back</a></td></tr>"
        for key, value in block.items():
            if key == "coinbase":
                value = "<a href='/addr/" + value + "'>" + value + "</a>"
                
            html += "<tr><td>" + key + "</td><td>" + str(value) + "</td></tr>"
        html += "</table>"
        return html
    except Exception as e:
        html = "<tr><td><a href='/'>Back</a></td></tr>" 
        html += "<tr><td> Invalid Block Height" + str(e) + "</td></tr>"
        return html

@app.route('/block/<hash>')
def block(hash):
    try:
        block = api.block(hash)["result"]
        html = "<table>"
        html += "<tr><td><a href='/'>Back</a></td></tr>"
        for key, value in block.items():
            if key == "coinbase":
                value = "<a href='/addr/" + value + "'>" + value + "</a>"
            html += "<tr><td>" + key + "</td><td>" + str(value) + "</td></tr>"
        html += "</table>"
        return html
    except:
        html = "<tr><td><a href='/'>Back</a></td></tr>" 
        html += "<tr><td> Invalid Block Hash</td></tr>"
        return html
@app.route('/faucet')
def faucet():
    ip = request.remote_addr
    # get addr param
    addr = request.args.get('addr')
    print(addr)
    if get_ip(ip):
        html = "<tr><td><a href='/'>Back</a></td></tr>"
        html += "<table>"
        result = faucet_send(addr)
        html += "<tr><td>Transaction Hash</td><td>" + result + "</td></tr>"
        # add ip to db
        add_ip(ip)

        html += "</table>"
        return html
    else:
        html = "<tr><td><a href='/'>Back</a></td></tr>"
        html += "<table>"
        html += "<tr><td>Transaction Hash</td><td> 24 hours have not passed since last request</td></tr>"
        html += "</table>"
        return html

@app.route('/')
def index():
    # center the page but make every element one under the other
    css = "<style>body {display: flex;justify-content: center;align-items: center;flex-direction: column;}</style>"

    html = "Falcon Idena Light Explorer"
    html += css
    # search with dropdown to select type
    html += "<form action='/search' method='get'>"
    html += "<select name='type'>"
    html += "<option value='addr'>Address</option>"
    html += "<option value='tx'>Transaction</option>"
    html += "<option value='block_height'>Block Height</option>"
    html += "<option value='block_hash'>Block Hash</option>"
    html += "</select>"
    html += "<input type='text' name='search'>"
    html += "<input type='submit' value='Search'>"
    html += "</form>"
    # add stats
    stats = get_info()
    html += "<table>"
    html += "<tr><td> Address is faucet address</td></tr>"

    for key, value in stats.items():
        html += "<tr><td>" + key + "</td><td>" + str(value) + "</td></tr>"
    html += "</table>"
    # add faucet
    html += "<tr><td> Input address to send 1 test idena for testing</td></tr>"
    html += "<form action='/faucet' method='get'>"
    html += "<input type='text' name='addr'>"
    html += "<input type='submit' value='Faucet'>"
    html += "</form>"
    # load last 50 blocks and check for txs
    txs = []
    for i in range(stats["Block"] - 50, stats["Block"]):
        block = api.block_at(i)["result"]
        try:
            # transactions check if its none
            for tx in block["transactions"]:
                txs.append(tx)
        except:
            pass
    html += "<table>"
    html += "<tr><td>Lastest Transactions</td></tr>"
    for tx in txs:
        tx = search_tx(tx)
        for key, value in tx.items():
            
            if key == "from":
                value = "<a href='/addr/" + value + "'>" + value + "</a>"
                html += "<tr><td>" + key + "</td><td>" + str(value) + "</td></tr>"
            if key == "to":
                value = "<a href='/addr/" + value + "'>" + value + "</a>"
                html += "<tr><td>" + key + "</td><td>" + str(value) + "</td></tr>"
            if key == "hash":
                value = "<a href='/tx/" + value + "'>" + value + "</a>"
                html += "<tr><td>" + key + "</td><td>" + str(value) + "</td></tr>"
            if key == "amount":
                html += "<tr><td>" + key + "</td><td>" + str(value) + "</td></tr>"
        html += "<tr><td>-------------------</td></tr>"
            
    html += "</table>"


    

    return html
    
@app.route('/search')
def search():
    search = request.args.get('search')
    type = request.args.get('type')
    if search == "":
        return redirect("/")
    if type == "addr":
        return redirect("/addr/" + search)
    elif type == "tx":
        return redirect("/tx/" + search)
    elif type == "block_height":
        return redirect("/block_at/" + search)
    elif type == "block_hash":
        return redirect("/block/" + search)
    else:
        return redirect("/")
    return html


import time
import json
# json db
# check ip if the last faucet request was less than 24 hours ago
def add_ip(ip):
    with open("db.json", "r") as f:
        db = json.load(f)
    db[ip] = time.time()
    with open("db.json", "w") as f:
        json.dump(db, f, indent=4)
def get_ip(ip):
    # check if ip last request was less than 24 hours ago
    with open("db.json", "r") as f:
        db = json.load(f)
    if ip in db:
        if time.time() - db[ip] < 86400:
            return False
        else:
            # remove ip from db
            return True
    else:
        return True
    

            
    
















if __name__=='__main__':
   app.run()