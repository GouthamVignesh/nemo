from __future__ import print_function
from future.standard_library import install_aliases

install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import wolframalpha
import wikipedia
import requests
from flask import Flask
from flask import request
from flask import make_response
import random
from weather import weather
from news import news
from webscrap import webscrap

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access.
    req_dict = json.loads(request.data)
    entity_type = ""
    entity_value = ""
    speech = ""
    # Accessing the fields on the POST request boduy of API.ai invocation of the webhook
    intent = req_dict["result"]["metadata"]["intentName"]

    entity_key_val = req_dict["result"]["parameters"]
    for key in entity_key_val:
        entity_value = entity_key_val[key]
        entity_type = key

        # constructing the resposne string based on intent and the entity.
    if intent == "shopping - custom":
        my_input = (req.get("result").get("resolvedQuery")).lower()
        product_name, price, url = webscrap(my_input)
        res = makeWebhookResult(product_name, price, url)

    elif intent == "Default Fallback Intent":
        my_input = (req.get("result").get("resolvedQuery")).lower()
        if ("weather" in my_input) or ('tell me about weather condition' in my_input) or (
                'tell me about weather' in my_input) or ('whats the climate' in my_input):
            x = weather()
            speech = "" + x + ""
            res = makeWebhookResult(speech)

        elif ("news" in my_input) or ("top headlines" in my_input) or ("headlines" in my_input):
            x = news()
            speech = "" + x + ""
            res = makeWebhookResult(speech)

        else:
            try:
                app_id = "R2LUUJ-QTHXHRHLHK"
                client = wolframalpha.Client(app_id)
                r = client.query(my_input)
                answer = next(r.results).text
                speech = "" + answer + ""
                res = makeWebhookResult(speech)
            except:
                my_input = my_input.split(' ')
                my_input = " ".join(my_input[2:])
                answer = wikipedia.summary(my_input, sentences=2)
                speech = "" + answer + ""
                res = makeWebhookResult(speech)
    else:
        speech = "no input"
        res = makeWebhookResult(speech)

    return res


def makeWebhookResult(speech):
    print("Response:")
    print(speech)

    return {
        "displayText": speech,
        "speech": speech
    }


def makeWebhookResult(product_name, price, url="https://www.ometrics.com/blog/wp-content/uploads/2017/12/chat_bot-01.jpg"):
    return {
        "messages": [
            {
                "type": 1,
                "platform": "facebook",
                "title": product_name,
                "subtitle": price,
                "imageUrl": ""+url+"",
                "buttons": [
                    {
                        "text": "read more about me ?",
                        "postback": "https://medium.com/swlh/what-is-a-chatbot-and-how-to-use-it-for-your-business-976ec2e0a99f"
                    }
                ]

    }
    ]
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
