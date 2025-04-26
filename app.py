from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = 'Your_Dhan_Access_Token'
CLIENT_ID = 'Your_Dhan_Client_Id'

def place_order(symbol, side, quantity):
    url = "https://api.dhan.co/orders"
    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "clientId": CLIENT_ID,
        "securityId": symbol,
        "orderType": "MARKET",
        "transactionType": side,  # 'BUY' or 'SELL'
        "quantity": quantity,
        "productType": "INTRADAY",
        "exchangeSegment": "NSE_EQ",
        "price": 0,
        "triggerPrice": 0
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received alert:", data)
    if data['action'] == 'buy':
        return place_order(data['symbol'], "BUY", data['qty'])
    elif data['action'] == 'sell':
        return place_order(data['symbol'], "SELL", data['qty'])
    return {"status": "no action"}

@app.route('/')
def home():
    return "Algo Trading Webhook is Running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)