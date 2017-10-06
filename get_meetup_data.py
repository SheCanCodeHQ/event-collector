#Python version: 2.7.13
import config
import requests
import json
import time
import datetime
import timestring

def main(start, end):
    start_timestamp=int(timestring.Date("{}T00:00:00".format(start)).to_unixtime()*1000)
    end_timestamp=int(timestring.Date("{}T23:59:00".format(end)).to_unixtime()*1000)
    categories = ["34"] #34 is the category id for tech; more can be added as deemed fit
    api_key = config.MEETUP
    headers = ['name', 'description', 'host', 'start_time', 'end_time',
        'event_type', 'location', 'city', 'country', 'price', 'link', 'tags', 'source', 'event_id', 'keyword']
    lines = [','.join(headers)]
    for category in categories:
        for coords in [(37.77397, -122.43129), (51.508530, -0.076132), (40.785091, -73.968285)]:
            lat = coords[0]
            lon = coords[1]
            response= get_results({'lat':lat, 'lon':lon, 'radius':'smart', "category":category,"time": '{},{}'.format(start_timestamp, end_timestamp),
                "key":api_key,"text_format":'plain'}) #only looking at upcoming events
            time.sleep(1)
            for event in response['results']:
                venue = event.get('venue')
                place = ""
                city = ""
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
                description = event.get('description', '')
                host = hostname
                start_time = (datetime.datetime.fromtimestamp(event['time']/1000.0) +
                    datetime.timedelta(milliseconds=event['utc_offset'])).strftime("%Y-%m-%dT%H:%M:%S")
                if event.get('duration', ''):
                    end_time = (datetime.datetime.fromtimestamp(event['time']/1000.0) +
                        datetime.timedelta(milliseconds=event['utc_offset']+event['duration'])).strftime("%Y-%m-%dT00:00:00")
                else:
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
                line = [str(item).replace(',', '').replace('\n', ' ').replace('\r', '') for item in details]
                line = ",".join(line)
                lines.append(line)

    with open("meetup_events_{}_to_{}.csv".format(start,end), 'w') as f:
        f.write('\n'.join(lines))

def get_results(params):
    request = requests.get("https://api.meetup.com/2/open_events",params=params)
    data = request.json()
    return data

if __name__=="__main__":
    start = datetime.date.today().strftime("%Y-%m-%d")
    end = (datetime.date.today() + datetime.timedelta(30)).strftime("%Y-%m-%d")
    main(start, end)
