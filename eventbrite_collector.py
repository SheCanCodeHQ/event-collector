import keys # CONTAINS API KEYS
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#for gspread
SCOPES = ["https://spreadsheets.google.com/feeds"]

women_keywords = ["women"]#, "woman", "girl"]
tech_keywords = ["tech"]#, "technology", "code", "programming", "programmer"]
csv_titles = "name, description, host, start_time, end_time, event_type, location, city, country, price, link, tags"

ids = set()
lines = [csv_titles]
rows = [csv_titles.split(', ')]


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

        for event in [event for event in response.json()['events'] if event['id'] not in ids
                    and event['venue'] and event['status']=='live']:
            ids.add(event['id']) #TODO: only do updates

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

            details = [name, description, host, start_time, end_time, event_type, location, city, country, price, link, tags]

            #CSV formatting
            line = [str(item).replace(',', ' ') for item in details]
            line = ", ".join(line)
            lines.append(line)

            #sheets formatting
            rows.append(details)

#CSV
with open("events.csv", 'w') as f:
    f.write('\n'.join(lines))

#sheets
credentials = ServiceAccountCredentials.from_json_keyfile_dict(keys.GOOGLE_SHEETS, SCOPES)
connection = gspread.authorize(credentials)

worksheet = connection.open("Test spreadsheet").sheet1

for row_i in range(len(rows)):
    for cell_i in range(len(rows[0])):
        if rows[row_i][cell_i]:
            worksheet.update_cell(row_i + 1, cell_i + 1, str(rows[row_i][cell_i]))
