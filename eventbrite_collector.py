#python3
import keys # CONTAINS API KEYS
import requests
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

#TODO: readme for config file

SCOPES = ["https://spreadsheets.google.com/feeds"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(keys.GOOGLE_SHEETS, SCOPES)
connection = gspread.authorize(credentials)

worksheet = connection.open("Test spreadsheet").worksheet("Sheet4")

ids = set(worksheet.col_values(14))
first_empty_row = len(ids) + 1
print(first_empty_row)
rows = []
min_date = datetime.date.today().strftime("%Y-%m-%dT00:00:00")
max_date = (datetime.date.today() + datetime.timedelta(30)).strftime("%Y-%m-%dT00:00:00")

keywords = []
with open('keywords.txt') as f:
    keywords = f.read().split("\n")
keywords = [k.replace(" ", "+").strip() for k in keywords if k]

for keyword in keywords:
    for city in ["san+francisco", "london", "new+york"]:
        print(keyword)
        response = requests.get(
            ("https://www.eventbriteapi.com/v3/events/search/"
                "?location.address={}&expand=organizer,venue,format,category&q={}"
                "&start_date.range_start={}&start_date.range_end={}").format(
                city, keyword, min_date, max_date),
            headers = {
                "Authorization": "Bearer " + keys.EVENTBRITE_OAUTH,
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

            rows.append(details)

#TODO: error handling for not enough rows
for row_i in range(len(rows)):
    print(row_i, "of",len(rows))
    for cell_i in range(len(rows[0])):
        if rows[row_i][cell_i]:
            try:
                worksheet.update_cell(row_i + first_empty_row, cell_i + 1, str(rows[row_i][cell_i]).replace('\n', " "))
            except TypeError as e:
                print(e)
                continue
