# Design Document for Event Web Scraper for She Can Code

## Technologies
Build in python   
bs4 (Beautiful Soup)  
scrapy  
  BaseSpider??  
requests  
Export as csv? can easily be opened in excel  
Google Drive/Sheets API  

## Search Criteria
### Target Websites (MVP)
Meetup _(HAS API!!)_ _(IN python! http://meetup-api.readthedocs.io/en/latest/getting_started.html )_  
Eventbrite _api: https://www.eventbrite.com/developer/v3/ ._  
#### Other (if time)
•	Girls in Technology https://girlsintech.org/#events http://www.womenintechnology.org/event-listing  
•	Women Who Code https://www.womenwhocode.com/events I think these guys are on Meetup though  
•	https://blog.bizzabo.com/women-in-technology-conferences easy to scrape, I think  
•	wearethecity.com https://www.wearethecity.com/events-calendar/ - link to text xml: http://www.wearethecity.com/?plugin=all-in-one-event-calendar&controller=ai1ec_exporter_controller&action=export_events&ai1ec_cat_ids=1094&xml=true  
•	General Assembly https://generalassemb.ly/education?format=events (maybe...)  
Facebook?? (has api)  
### Target Locations (MVP)
London  
SF  
NY  
### Key Words/Tags

## Format
•	Event Name  
•	Short Description / Extract (if any)  
•	Event Author / Organiser / Host  
•	Event Start and End Time (date and time)  
•	Event Type: Conference,  
•	Location (City, Country)  
•	Google Maps Link  
•	Price / Cost of Event (if listed)  
•	Original / Booking Site URL  
•	Logo Image (if any)  
•	Tags (if tagged with anything that would make it more descriptive)  

## Strategy
### Overview
Bit of research on how to build a scraper  
Research layouts of target websites  
Build simple scraper in python - use APIs when possible to increase accuracy (id systems reduce duplicates)  
Make sure to remove duplicates - edit distance? if two platforms, use both links  
Export as csv  
Figure out how to sync with a google doc - entered/not entered attribute on google doc  
Run script on server?? update daily  
Build website for organizing better, or just publish google doc  
Automate squarespace data entry??  


## Questions for Nicole
servers? if not use heroku or someone's machine. only needs to run like once a day  
meetup, eventbrite, fb api key


## Scraping Resources
### General Scraping
http://newcoder.io/scrape/part-2/  
https://blog.hartleybrody.com/web-scraping/
### Google Sheets API
https://developers.google.com/sheets/api/quickstart/python  
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
