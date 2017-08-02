from __future__ import unicode_literals

import requests
import json
import time
import codecs
import sys
import config
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def main():
        categories = ["34"] #34 is the category id for tech; more can be added as deemed fit
        api_key= config.api_key
        for category in categories:
                response=get_results({"category":category,"status":"upcoming","key":api_key}) #only looking at upcoming events
                time.sleep(1)
                for event in response['results']:
                	venue = event.get('venue')
                	city = ""
                	place = ""
                	state = ""
                	country = ""
                	address = ""
                	if venue:
                		city = venue.get('city',"")
                		place = venue.get('name',"")
                		state = venue.get('state',"")
                		country = venue.get('localized_country_name',"")
                		address = venue.get('address_1',"")+' '+venue.get('address_2',"")+' '+venue.get('address_3',"")
                	host = event.get('group')
                	hostname = ""
                	if host:
                		hostname = host.get('name',"")
                	print ",".join([event['name'].replace(","," "), event.get('event_url'), address, place, city, state, country, hostname])


def get_results(params):
	request = requests.get("https://api.meetup.com/2/open_events",params=params)
	data = request.json()
	return data


if __name__=="__main__":
        main()