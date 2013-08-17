#!/usr/bin/python
from flask.ext.script import Manager

import urllib2
import json

from geocash import app
from geocash import Location
from geocash import db
manager = Manager(app)

@manager.command
def update():
    # Check every unclaimed location
    locations = Location.query.filter(Location.claimed == False).all()

    if len(locations) > 0:
        # 500 requests / 5 minutes
        # 10000 requests / 8 hours
        url = "http://blockchain.info/multiaddr?active="
        for location in locations:
            url += location.btc_addr
            url += "|"

        response = urllib2.urlopen(url)
        addresses = json.loads(response.read())['addresses']

        for address in addresses:
            btc_addr = address['address']
            location = Location.query.filter(Location.btc_addr == btc_addr).first()
            location.value = 1.0 * address['final_balance'] / 100000000 

            # If any coins have been spent, then the private key was redeemed
            if address['total_sent'] > 0:
                location = Location.query.filter(Location.btc_addr == btc_addr).first()
                location.claimed = True
                print "Claimed: " + btc_addr
        
        db.session.commit()

    else:
        print "No unclaimed locations"

#    locations[0].claimed = True
#    db.session.commit() 

if __name__ == "__main__":
    manager.run()
