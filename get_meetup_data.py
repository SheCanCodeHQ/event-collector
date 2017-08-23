#from __future__ import unicode_literals

import requests
import json
import time
#import codecs
#import sys
import config
import datetime
#UTF8Writer = codecs.getwriter('utf8')
#sys.stdout = UTF8Writer(sys.stdout)

def main():
    categories = ["34"] #34 is the category id for tech; more can be added as deemed fit
    api_key = config.MEETUP
    lines = []
    for category in categories:
            response= get_results({"category":category,"time":",1m","status":"upcoming","key":api_key}) #only looking at upcoming events
            time.sleep(1)
            for event in response['results']:
                venue = event.get('venue')
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

                name = event['name']
                description = ''
                host = hostname
                try:
                    print(event['time'])
                    print(datetime.datetime.fromtimestamp(event['time']))
                    start_time = (datetime.datetime.fromtimestamp(event['time']) +
                        datetime.timedelta(milliseconds=event['utc_offset'])).strftime("%Y-%m-%dT00:00:00")
                    print(start_time)
                    if event[duration]:
                        end_time = (datetime.datetime.fromtimestamp(event['time']) +
                            datetime.timedelta(milliseconds=event['utc_offset']+event['duration'])).strftime("%Y-%m-%dT00:00:00")
                    else:
                        end_time = ''
                    print(end_time)
                except ValueError:
                    print("year is very wrong")
                    start_time = ''
                    end_time = ''
                event_type = ''
                location = address
                price = event.get("fee").get("amount", '') if event.get("fee") else ''
                link = event['event_url']
                tags = ''
                source = "meetup"
                event_id = event["id"]
                keyword = category

                details = [name, description, host, start_time, end_time,
                    event_type, location, city, country, price, link, tags, source, event_id, keyword]
                line = [str(item).replace(',', ' ').replace('\n', ' ') for item in details]
                line = ",".join(line)
                if city in ["San Francisco", "London", "New York"]:
                    lines.append(line)

    with open("meetup_events.csv", 'w') as f:
        f.write('\n'.join(lines))

def get_results(params):
    request = requests.get("https://api.meetup.com/2/open_events",params=params)
    data = request.json()
    return data


if __name__=="__main__":
        main()
