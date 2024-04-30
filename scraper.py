#!/usr/bin/python3
import urllib3
import sys
import time
import random
import json

if len(sys.argv) < 2:
    print(f"Error! You have to specify the location to search businesses from like:\npython3 {sys.argv[0]} LOCATION")
    sys.exit(-1)
else:
    LOCATION = sys.argv[1]

print(f"Using location {LOCATION}")
pageNumber = 37
html = str(urllib3.request(method='GET', url=f"https://guiaempresas.universia.es/localidad/{LOCATION}/?qPagina={pageNumber}").data)

if not "qPagina=" in html:
    print("Error! We found a bot blocker or an error page:")
    print(html)
    print("Check if the location you used exists in the main page.")
    sys.exit(-1)

# Get number of pages
res = html.split('"')
maxPages = 0
for i in range(len(res)):
    if "?qPagina=" in res[i]:
        maxPages = int(res[i].split('?qPagina=')[1]) if int(res[i].split('?qPagina=')[1]) > maxPages else maxPages
print(f"We have {maxPages} pages")

num = 30 * (pageNumber - 1) + 1
businesses = []
while pageNumber <= maxPages:
    res = html.split('<td class="textleft"><a href="')
    for i in range(1, len(res)):
        row = res[i].split('</td>')[0]
        webpage = "https://guiaempresas.universia.es" + row.split('"')[0]
        business = row.split(">")[1].split("</a")[0]
        print(f"{num}. Business '{business}' with website '{webpage}'")
        businesses.append({'index': num, 'name': business, 'webpage': webpage})
        num += 1

    pageNumber += 1
    # Get another page after waiting between 1 and 60 seconds
    sleep_time = random.randrange(1, 60)
    print(f"Waiting {sleep_time} seconds before requesting page {pageNumber}")
    time.sleep(sleep_time)
    html = str(urllib3.request(method='GET', url=f"https://guiaempresas.universia.es/localidad/{LOCATION}/?qPagina={pageNumber}").data)

# Save the data to a JSON file
with open(f'{LOCATION}.json', 'w') as f:
    json.dump(businesses, f)