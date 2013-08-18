#!/usr/bin/python
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
import time
import string
import json

import base58
import coind

COIN = 100000000
PAYOUT_RATE = 1.01

# Config
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://pool:changeme@localhost/pool"
app.config["DEBUG"] = True
db = SQLAlchemy(app)

# Memcached
from werkzeug.contrib.cache import MemcachedCache
cache = MemcachedCache(["127.0.0.1:11211"])

# Logging
import logging
from logging import FileHandler
file_handler = FileHandler("geocash.log")
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

def is_valid_address(addr):
    return base58.get_bcaddress_version(addr) != None

def get_time():
    return int(time.mktime(datetime.datetime.now().timetuple()))

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    name = db.Column(db.String(256))
    btc_addr = db.Column(db.String(64))
    value = db.Column (db.Float())
    claimed = db.Column(db.Boolean)

@app.route("/", methods=['GET'])
def index():
    unclaimed = Location.query.filter(Location.claimed == False).all()
    claimed = Location.query.filter(Location.claimed == True).all()
    return render_template("index.html", unclaimed = unclaimed, claimed = claimed)

@app.route("/add", methods=['POST'])
def add():
    location = Location(latitude=request.form['latitude'], longitude=request.form['longitude'], name=request.form['name'], btc_addr=request.form['btc_addr'], value = 0, claimed = False)
    db.session.add(location)
    db.session.commit()  

    return redirect("/")

@app.route("/api/locations", methods=['GET'])
def api_locations():
    response = []
    locations = Location.query.filter().all()
    for location in locations:
        loc = {}
        loc['name'] = location.name
        loc['lat'] = location.latitude
        loc['lon'] = location.longitude
        loc['value'] = location.value
        loc['claimed'] = location.claimed
        response.append(loc)
    return json.dumps(response)

db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0")

