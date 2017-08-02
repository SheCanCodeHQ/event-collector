import keys # CONTAINS API KEYS
import requests

women_keywords = ["women"]#, "woman", "girl"]
tech_keywords = ["tech"]#, "technology", "code", "programming", "programmer"]

ids = set()
lines = []

csv_titles = "name, description, host, start_time, end_time, event_type, location, city, country, price, link, tags"

for i in women_keywords:
    for j in tech_keywords:
        keyword = i + "+" + j

        response = requests.get(
            "https://www.eventbriteapi.com/v3/events/search/?expand=organizer,venue,format,category&q=" + keyword,
            headers = {
                "Authorization": "Bearer " + keys.EVENTBRITE_OAUTH,
            },
            verify = True,  # Verify SSL certificate
        )

        # make sure status is live

        for event in [event for event in response.json()['events'] if event['id'] not in ids and event['venue']]:
            ids.add(event['id'])

            name = event['name']['text']
            description = ''#TODO: clean this event['description']['text'] if event['description'] else ''
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

            line = [name, description, host, start_time, end_time, event_type, location, city, country, price, link, tags]
            line = [str(item).replace(',', ' ') for item in line]
            line = ", ".join(line)
            lines.append(line)

with open("events.csv", 'w') as f:
    f.write(csv_titles + '\n')
    f.write('\n'.join(lines))
