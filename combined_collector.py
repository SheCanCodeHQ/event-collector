import config # CONTAINS API KEYS
import eventbrite_collector
import get_meetup_data
import requests
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

def main():
    print("Fetching meetup data...")
    get_meetup_data.main()
    print("Fetching eventbrite data...")
    eventbrite_collector.main()
    print("Writing to google sheets...")
    write_to_sheets()

def write_to_sheets():
    SCOPES = ["https://spreadsheets.google.com/feeds"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(config.GOOGLE_SHEETS, SCOPES)
    connection = gspread.authorize(credentials)

    worksheet = connection.open("Test spreadsheet").worksheet("Sheet6")

    ids = set(worksheet.col_values(14))
    first_empty_row = len(ids) + 1
    rows = []

    for csv in ["eventbrite_events.csv", "meetup_events.csv"]:
        with open(csv) as f:
            rows += f.read().split("\n")
    rows = [row.split(",") for row in rows]
    rows = [row for row in rows if row[13] not in ids]

    #TODO: error handling for not enough rows
    for row_i in range(len(rows)):
        for cell_i in range(len(rows[0])):
            if rows[row_i][cell_i]:
                try:
                    worksheet.update_cell(row_i + first_empty_row, cell_i + 1, str(rows[row_i][cell_i]).replace('\n', " "))
                except TypeError as e:
                    print(e)
                    continue
if __name__=="__main__":
        main()
