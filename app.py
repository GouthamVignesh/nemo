from __future__ import print_function
from future.standard_library import install_aliases


install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import webbrowser
import json
import os
import wolframalpha
import wikipedia
import requests
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify,request
import random
from weather import weather
from news import news
from database import database
from doctor_find import doctor_find
from hospitalfind import hospitalfind
from nearby_pharmacy import nearby_pharmacy
from pregnancy import pregnancy
from menstrualcycle import menstrualcycle
from bmi import bmi
import datetime
from datetime import datetime
from pytz import timezone  
import urllib.request
import urllib.parse  
import requests
import re
south_africa = timezone('Asia/Kolkata')
sa_time = datetime.now(south_africa)


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST','GET'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    res = processRequest(req)
    print(res)
    return make_response(jsonify({'fulfillmentText':res}))

def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access.
    speech = ""
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action== "medicalissues.medicalissues-custom":
        my_input = (req.get("queryResult").get("parameters").get("medical")).lower()
        x= database(my_input)
        speech = "" + x + ""
        res = makeWebhookResult(speech)

    elif action =="Diabetes.Diabetes-custom.Diabetes-Type1-no.Diabetes-Type1-no-custom":
        my_input= my_input = req.get('queryResult').get('queryText').lower()
        x= nearby_pharmacy(my_input)
        speech = "" + x + ""
        res = makeWebhookResult(speech)
    
    elif action=="Diabetes.Diabetes-custom.Diabetes-Type1-yes.Diabetes-Type1-yes-custom.Diabetes-Type1-yes-a-no.Diabetes-Type1-yes-a-no-yes.Diabetes-Type1-yes-a-no-yes-custom":
        my_input= my_input = req.get('queryResult').get('queryText').lower()
        x= nearby_pharmacy(my_input)
        speech = "" + x + ""
        res = makeWebhookResult(speech)


    elif action =="Diabetes.Diabetes-custom.Diabetes-Type1-yes.Diabetes-Type1-yes-custom.Diabetes-Type1-yes-a-yes":
        #print (sa_time.strftime('%Y-%m-%d_%H-%M-%S'))
        hour =int(sa_time.strftime('%H'))

        if (7 <= hour < 11):
            greeting = "It's around 9 Am Did you have your Breakfast !"
    
        elif (11<= hour < 18):
            greeting =  "It's around 6 pm"+ " Did you have your lunch !"
        else:
            greeting = "It's around 9 Am Did you have your Dinner !"
        speech =""+greeting+""
        res=makeWebhookResult(speech)

    elif action == "menstrualcycle":
        x=menstrualcycle()
        speech = "" + x + ""
        res = makeWebhookResult(speech)
        
    elif action =="pregnancy.pregnancy-custom":
        data = (req.get("queryResult").get("parameters").get("number"))
        x=pregnancy(data)
        speech = ""+x+""
        res=makeWebhookResult(speech)
    elif action == "pharmacy.pharmacy-custom":
        my_input = req.get('queryResult').get('queryText').lower()
        x= nearby_pharmacy(my_input)
        speech = "" + x + ""
        res = makeWebhookResult(speech)

    elif action == "finddoctor.finddoctor-custom":
        my_input = req.get('queryResult').get('queryText').lower()
        x= doctor_find(my_input)
        speech = "" + x + ""
        res = makeWebhookResult(speech)

    elif action =="findhospital.findhospital-custom":
        my_input = req.get('queryResult').get('queryText').lower()
        x=hospitalfind(my_input)
        speech = "" + x + ""
        res = makeWebhookResult(speech)


    elif action =="fitness.fitness-custom":
        height = req.get('queryResult').get('parameters').get('height')
        weight = req.get('queryResult').get('parameters').get("weight")
        age = req.get('queryResult').get('parameters').get('age').get('amount')
        age=int(age)
        age=str(age)
        gender =req.get('queryResult').get('parameters').get('gender')
        x= bmi(height,weight,gender,age)
        speech="" + x + ""
        res=makeWebhookResult(speech)



    elif action=="weather.weather-custom":
        my_input = req.get('queryResult').get('queryText').lower()
        x = weather(my_input)
        speech = "" + x + ""
        res = makeWebhookResult(speech)
       
            
    elif action== "input.unknown":
        my_input = req.get('queryResult').get('queryText').lower()
        if ("news" in my_input) or ("top headlines" in my_input) or ("headlines" in my_input):
            x = news()
            speech = "" + x + ""
            res = makeWebhookResult(speech)
        elif("open"in my_input):
            keyword=my_input[my_input.find("open")+5:]
            webbrowser.open_new_tab('http://www.google.com/search?q=%s&btnI' %keyword)
            speech=""+keyword+" is Opening in Your Web Browser !"
            res=makeWebhookResult(speech)
        
        elif("play"in my_input):
            search=my_input[my_input.find("play")+5:]
            query_string = urllib.parse.urlencode({"search_query" :search})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            webbrowser.open_new_tab("http://www.youtube.com/watch?v=" + search_results[0])
            speech=""+Search +"is Now playing !"
            res=makeWebhookResult(speech)

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
    return speech
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
