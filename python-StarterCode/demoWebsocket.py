# open a websocket connection from the terminal using the command $ python3 demoWebsocket.py.
# NOTE: updates lines 13-15 with the appropriate payload if looking of other events than parking
from cityiq import CityIq
import ssl  # necessary only with line 42
import json
# pip3 install websocket-client
import websocket

with open('../myCredentials.json') as json_file:
    credentials = json.load(json_file)

# # set the zone and websocket url
zone = credentials["id"] + '-IE-TRAFFIC'
wsURL = credentials["websocketService"] + '/events'
payload = '{"bbox": "90:-180,-90:180", "eventTypes":["TFEVT"]}'


def on_message(ws, message):
    print(message)


def on_close(ws):
    print('### closed ###')


def on_error(ws, error):
    print(error)


def on_open(ws):
    print('### connected ###')
    ws.send(payload)


if __name__ == '__main__':
    print("===========Starting================")
    print("Getting the token")
    # getting the token using cityiq.py
    myCIQ = CityIq("City")
    myCIQ.fetchToken()
    token = myCIQ.getToken()

    # setup the websocket
    headers = {'Authorization': 'Bearer '+token, 'Predix-Zone-Id': zone}
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        wsURL, header=headers, on_message=on_message, on_close=on_close, on_error=on_error)
    ws.on_open = on_open
    # lines 41 and 42 are interchangabel - please uncomment one
    # ws.run_forever()
    # requires line 5 import ssl
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
