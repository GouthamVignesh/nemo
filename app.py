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
    if intent == "Platform exploration help":
	    if entity_type == "features":
		    if entity_value == "sign out":
			    speech = """Here are the steps to update the goals: First, select the project (from the carousel) > click on an objective > update goals"""
     
    elif intent=="Default Fallback Intent":
        my_input=req.get("result").get("resolvedQuery")
        if("weather" in my_input) or ('tell me about weather condition' in my_input) or ('tell me about weather' in my_input) or ('whats the climate' in my_input):
            city="coimbatore"
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=d88ce41afbcf7f04e679e5227db5484a&units=metric'.format(city)
            r = requests.get(url)
            data = r.json()
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            latitude = data['coord']['lat']
            longitude = data['coord']['lon']
            description = data['weather'][0]['description']
            x="The Current condition in coimbatore is Temperature : {} degree celsius \n Wind Speed : {} m/s \n Latitude : {}\n Longitude : {} It's look like some {} in your area".format(temp,wind_speed,latitude,longitude,description)
            speech=""+x+""
        elif("pictures of" in my_input) or ("show me the pictures of" in my_input):
            text=my_input[my_input.find("of")+2:]
            speech='https://www.google.com/search?tbm=isch&source=hp&biw=1240&bih=610&ei=RgUUW-D1JdT5rQHukpWwCQ&q={0}&oq={1}&gs_l=img.3..35i39k1l2j0l8.11757.21299.0.21783.20.19.1.0.0.0.323.1222.0j3j2j1.6.0....0...1ac.1.64.img..14.6.1014.0...0.QyutTOLT3UI'.format(text,text)
        
        elif("how to " in my_input):
            speech="Here is the matching video :"+'www.youtube.com/results?search_query=%s' %my_input
        elif("lets watch movie" in my_input):
            speech="i hope you will find your interesting movie in this link ,  'https://newmoviesonline.tv' have a good time !" 
        elif("news" in my_input)or("top headlines" in my_input) or ("headlines" in my_input):
            y = random.randint(1,6)
            if y == 1:
                r = requests.get('https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=e33b15acbf4c4071bfeb891cd02a99f6')
                j = r.json()
                x = j.get('articles')
                newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
                speech=""+newp+""
            elif y==2:
                r = requests.get('https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=e33b15acbf4c4071bfeb891cd02a99f6')
                j = r.json()
                x = j.get('articles')
                newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
                speech=""+newp+""   
            elif y == 3:
                r = requests.get('https://newsapi.org/v1/articles?source=independent&sortBy=top&apiKey=e33b15acbf4c4071bfeb891cd02a99f6')
                j = r.json()
                x = j.get('articles')
                newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
                speech=""+newp+""
            elif y==4:
                r = requests.get('https://newsapi.org/v1/articles?source=ars-technica&sortBy=top&apiKey=e33b15acbf4c4071bfeb891cd02a99f6')
                j = r.json()
                x = j.get('articles')
                newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
                speech=""+newp+""
            elif y == 5:
                r = requests.get('https://newsapi.org/v1/articles?source=the-hindu&sortBy=top&apiKey=e33b15acbf4c4071bfeb891cd02a99f6')
                j = r.json()
                x = j.get('articles')
                newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
                speech=""+newp+""
            elif y==6:
                r = requests.get('https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=e33b15acbf4c4071bfeb891cd02a99f6')
                j = r.json()
                x = j.get('articles')
                newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
                speech=""+newp+""
        elif("lets watch movie" in my_input) or("movie" in my_input):
            speech="Here is the matching link to find your intrested movie : https://newmoviesonline.tv"
        else:
            try:
                app_id = "R2LUUJ-QTHXHRHLHK"
                client = wolframalpha.Client(app_id)
                r = client.query(my_input)
                answer = next(r.results).text
                speech=""+answer+""
            except:
                my_input = my_input.split(' ')
                my_input = " ".join(my_input[2:])
                answer=wikipedia.summary(my_input,sentences=2)
                speech=""+answer+""
    else:
        speech="no input"
            

    
    res = makeWebhookResult(speech)
    return res

def makeWebhookResult(speech):
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech
	"source": "Build conversational interface for your app in 10 minutes."
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
