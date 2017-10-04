#python3
import config # CONTAINS API KEYS
import requests
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

min_date = datetime.date.today().strftime("%Y-%m-%dT00:00:00")
max_date = (datetime.date.today() + datetime.timedelta(30)).strftime("%Y-%m-%dT00:00:00")

def main():
    diversity_keywords = ["women", "woman", "girl", "lady", "ladies", "diversity", "lgbt", "lgbtq"]
    tech_keywords = ["tech", "technology"]
    keywords = lst = [i + "+" + j for i in diversity_keywords for j in tech_keywords]

    ids = set()
    lines = []

    for keyword in keywords:
        for city in ["san+francisco", "london", "new+york"]:
            response = requests.get(
                ("https://www.eventbriteapi.com/v3/events/search/"
                    "?location.address={}&expand=organizer,venue,format,category&q={}"
                    "&start_date.range_start={}&start_date.range_end={}").format(
                    city, keyword, min_date, max_date),
                headers = {
                    "Authorization": "Bearer " + config.EVENTBRITE_OAUTH,
                },
                verify = True,  # Verify SSL certificate
            )
            if not response: continue

            for event in [event for event in response.json()['events'] if event['id'] not in ids
                        and event['venue'] and event['status']=='live']:
                ids.add(event['id']) #TODO: only do updates but keep tag overlaps!

                name = event['name']['text']
                description = event['description']['text'] if event['description'] else ''
                host = event['organizer']['name']
                start_time = event['start']['local']
                end_time = event['end']['local']
                event_type = event['format']['name'] if event['format'] else ''
                location = event['venue']['address']['localized_address_display']
                city = event['venue']['address']['city']
                country = event['venue']['address']['country']
                price = 'free' if event['is_free'] else 'paid' #TODO: get a general idea of ticket prices
                link = event['url']
                tags = event['category']['name'] if event['category'] else ''
                source = 'eventbrite'
                event_id = event['id']
                keyword = keyword

                details = [name, description, host, start_time, end_time,
                    event_type, location, city, country, price, link, tags, source, event_id, keyword]

                line = [str(item).replace(',', ' ').replace('\n', ' ').replace('\r', '') for item in details]
                line = ",".join(line)
                lines.append(line)

    with open("eventbrite_events.csv", 'w') as f:
        f.write('\n'.join(lines))
