from pickle import APPEND
from flask import request, Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html') 
    elif request.method == 'POST':
        city = request.form['city']
        response = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/today?unitGroup=metric&key=R7AJKMMK92F92AU32GWEFQ82M&contentType=json")
        response1 = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next7days?unitGroup=metric&include=days&key=R7AJKMMK92F92AU32GWEFQ82M&contentType=json")
        report = response.json()
        report1 = response1.json()
        next_7_days = []
        at = []
        for days in report1['days']:
            next_7_days.append(days['conditions'])
            tma = days['tempmax']
            tmi = days['tempmin']
            at.append((tma+tmi)/2)
            print(days['conditions'])
            print(at)
        conditions = []
        next_7_days.pop(1)
        at.pop(1)
        ra = report['resolvedAddress'] 
        for days in report['days']:
            c = days['conditions']
            sr = days['sunrise']
            ss = days['sunset']
            mp = days['moonphase']
            tma = days['tempmax']
            tmi = days['tempmin']
            daily=(f"Today is {c}! The sun rises at {sr} and the sun sets at {ss}. The moonphase for today is {mp}. The minimum temperature is {tmi} and the maximum temperature is {tma} in {ra}!")
            for hours in days['hours']:
                icon = hours['icon']
                temp = hours['temp']
                hum = hours['humidity']
                perci = hours['precipprob']
                ws = hours['windspeed']   
                cc = hours['cloudcover'] 
                se = hours['solarenergy']
                conditions.append(f" {icon}, {temp} , {hum}, {perci}%, {ws}, {cc}, {se}")         
        return render_template('home.html', conditions=conditions, daily=daily, next_7_days=next_7_days, at=at, c=c)


if __name__ == '__main__':
    app.run(debug=True)


# def jprint(obj):
#     # create a formatted string of the Python JSON object
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)

# jprint(response.json())