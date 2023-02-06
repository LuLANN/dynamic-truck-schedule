
from flask import Blueprint, render_template
from flask import Flask, url_for, json, jsonify
from flask_login import login_required, current_user
import os
import datetime
import time

views = Blueprint('views', __name__)


@views.route('/')
# To see home page only when logged in.
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/_updatetruckdata', methods=['GET'])
def updatetruckdata():
    truck_data = json.load(open('website/static/data/truck_data.json'))
    trucks_today = []
    trucks_15 = []
    trucks_30 = []
    now = datetime.datetime.now()
    week = ["S", "M", "T", "W", "T", "F", "S"]

    y = json.dumps(truck_data)
    dict = json.loads(y)
    i = 0
    for truck in truck_data:
        truck_day = dict[i].get("Days")
        arrival = dict[i].get("Arrival")
        departure = dict[i].get("Departure")
        day_index = now.strftime("%w")
        curr_day = week[int(day_index)]

        curr_hour = int(now.strftime("%H"))
        curr_min = int(now.strftime("%M"))
        curr_sec = int(now.strftime("%S"))
        # current time is expressed as the number of seconds that have passed since 12am
        curr_in_sec = curr_hour*3600 + curr_min*60 + curr_sec
        
        
        if arrival[1] == ":":
            arrival_hour = int(arrival[0])
            arrival_min = int(arrival[2:4])
        else:
            arrival_hour = int(arrival[0:2])
            arrival_min = int(arrival[3:5])

        if departure[1] == ":":
            dep_hour = int(departure[0])
            dep_min = int(departure[2:4])
        else:
            dep_hour = int(departure[0:2])
            dep_min = int(departure[3:5])
        
        arrival_sec = int(arrival[-2:])
        # truck arrival and departure time is expressed as the number of seconds that have passed since 12am
        arrival_in_sec = arrival_hour*3600 + arrival_min*60 + arrival_sec

        dep_sec = int(departure[-2:])
        dep_in_sec = dep_hour*3600 + dep_min*60 + dep_sec
        
        current = False
        if day_index == "1" or day_index == "3" or day_index == "5":
            if curr_day in truck_day:
                current = True
        elif day_index == "2":
            if truck_day[1] == "T":
                current = True
        elif day_index == "4":
            if truck_day[3] == "T":
                current = True
        elif day_index == "6":
            if truck_day[5] == "S":
                current = True
        elif day_index == "0":
            if truck_day[6] == "S":
                current = True
        
        to_arrive = False
        to_depart = False
        if current == True:
            # check if a truck's arrival time is within 2 hours (expressed in seconds) of the current time 
            # of if the departure time hasn't passed yet
            if (curr_in_sec <= arrival_in_sec) and (arrival_in_sec <= curr_in_sec + 7200):
                to_arrive = True
            if (curr_in_sec >= arrival_in_sec) and (curr_in_sec < dep_in_sec):
                to_depart = True
            if (to_arrive == True) or (to_depart == True):
                trucks_today.append(dict[i])
                # checking if the truck arrives within 30 min
                if (curr_in_sec <= arrival_in_sec) and (arrival_in_sec <= curr_in_sec + 1800):
                    trucks_30.append(True)
                else:
                    trucks_30.append(False)
                # checking if the truck departs within 15 min
                if (curr_in_sec <= dep_in_sec) and (dep_in_sec <= curr_in_sec + 900):
                    trucks_15.append(True)
                else:
                    trucks_15.append(False)
                
        i += 1
    return jsonify(today = trucks_today, fifteen = trucks_15, thirty = trucks_30)
