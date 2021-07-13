from flask import (
    Flask,
    request,
    Response,
)

from config_parser import (
    token,
)
from requests import request as rt
TOKEN = token
app = Flask(__name__)
VERIFY_TOKEN = 'pegus_200_delay_bot'


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route('/', methods=['GET', 'POST'])
def respond():
    if request.method == 'GET':
        return verify_webhook(request)
    if request.method == 'POST':
        print(request.json)
        # print('smthng')
        # payload = request.json
        # event = payload['entry'][0]['messaging']
        # for x in event:
        #     print(x)
        #     if is_user_message(x):
        #         text = x['message']['text']
        #         sender_id = x['sender']['id']
        #         respond(sender_id, text)
        #
        return "ok"

#
#
# @app.route('/api/sum', methods=['POST'])
# def sum():
#     """
#     Send a POST request to localhost:5000/api/sum with a JSON body with an "a" and "b" key
#     to have the app add those numbers together and return a response string with their sum.
#     """
#     print "Processing request..."
#     payload = parse_request(request)
#     print "Receieved following paylod:"
#     print payload
#
#     print "Adding sum..."
#     summation = payload['a'] + payload['b']
#     print "Found sum: %s" % summation
#
#     print "Creating response string..."
#     resp = '%s + %s = %s' % (payload['a'], payload['b'], summation)
#     print "Sending the following response:"
#     print resp
#
#     return (resp, 200, None)

if __name__ == '__main__':
    app.run(host='localhost', port='8003', debug=True, use_reloader=True)