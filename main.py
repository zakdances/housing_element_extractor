from __future__ import print_function
import json
import os.path
import time
import itertools
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from googlesearch import search

cities_path_name = "./city json/main.json"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_SPREADSHEET_ID = '1_8arPl4aYjq4QwoJbt63YjVuZ_NsSWuKnMMCIKnHcUE'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'
# SAMPLE_RANGE_NAME = 'Sheet1!A1:D5'
SAMPLE_RANGE_NAME = 'A1:H6000'
body = {
    # "range": "Sheet1!A1:D5",
    "range": SAMPLE_RANGE_NAME,
    # "majorDimension": "ROWS",
    "values": [
        ["Item", "Cost", "Stocked", "Ship Date"],
        ["Wheel", "$20.50", "4", "3/1/2016"],
        ["Door", "$15", "2", "3/15/2016"],
        ["Engine", "$100", "1", "3/20/2016"],
        ["Totals", "=SUM(B2:B4)", "=SUM(C2:C4)", "=MAX(D2:D4)"]
    ],
}

def get_cities_list():
    # Specify the path to your GeoJSON file
    file_path = cities_path_name

    # Open the file and load the GeoJSON data
    with open(file_path) as file:
        data = json.load(file)
    
    # Now you can work with the loaded GeoJSON data
    # For example, you can access the features like this:
    # features = data["features"]
    return data

# iteration = 0
def formatDate(x):
    # x = file_name = os.path.splitext(x)[0]
    x = x[-6:]
    if x.isdigit():
        # date_object = datetime.strptime(x, "%d%m%y")
        formatted_date = f"{x[:2]}-{x[2:4]}-{x[-2:]}"
        return formatted_date
    return None
def filter_list(city):
    # properties =  item["properties"]
    city_name = city["city"]
    housing_element_urls = city["housing_element"]
    county_name = city["county"]
    planning_agency = city["planning_agency"]



    # search_results = search(city + ", California", num_results=1, advanced=True)
    # city_website_url = ""
    # for result in list(search_results):
    #    city_website_url = result.url
    #    break
    # time.sleep(0.25)

    # search_results = search(city + ", California housing element", num_results=1, advanced=True)
    # result_1 = ""
    # result_2 = ""
    # for index, result in enumerate(list(search_results)):
    #     if index == 0:
    #         result_1 = result
    #     if index == 1:
    #         result_2 = result
    # time.sleep(0.25)
    rows = []

    # url_string = ""
    for i, url in enumerate(housing_element_urls):
        row = []
        hyperlink = '=HYPERLINK("' + url + '")'
        date_string = formatDate(os.path.splitext(hyperlink)[0])
        if i == 0:
            row = [
                city_name,
                hyperlink,
                date_string if date_string else "",
                planning_agency,
                county_name,
            ]
        else:
            row = [
                "",
                hyperlink,
                date_string if date_string else "",
                "",
                "",
            ]
        rows.append(row)
    
    if len(rows) == 0:
        row = [
            city_name,
            "",
            "",
            planning_agency,
            county_name,
        ]
        rows.append(row)

        # url_string += '=HYPERLINK("' + url + '")'
        # if len(housing_element_urls) > 1 and i != len(housing_element_urls) - 1:
        #     url_string += '\n'

    # iteration = iteration + 1
    # print("start ---------")
    # print(url_string)
    # print("end ---------")
    rows.append([
        "",
        "",
        "",
        "",
        ""
    ])
    return rows

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()

        cities_list = get_cities_list()
        new_List = map(filter_list, cities_list)
        new_List = list(itertools.chain(*new_List))
        body["values"] = list(new_List)

        result = sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
            valueInputOption="USER_ENTERED", body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result

        # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #                             range=SAMPLE_RANGE_NAME).execute()
        # values = result.get('values', [])

        # if not values:
        #     print('No data found.')
        #     return

        # print('Name, Major:')
        # for row in values:
        #     # Print columns A and E, which correspond to indices 0 and 4.
        #     print('%s, %s' % (row[0], row[4]))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()