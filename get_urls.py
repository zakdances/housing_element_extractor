import json
import os.path
import requests
from urllib.parse import urlencode

cities_path_name = "./city json/main.json"
SerpApiKey = "7d9613c8d0198e527a50a932e4835c0279f64970ef04c9d9d813a7c5fd6d70c0"

def query(query_param):
    pathname = "http://api.serpstack.com/search"

    params = {
        'access_key': '6f026184a47d4a93d964c57c1212f2b0',
        'query': query_param + ",%22California%22housing%22element",
        'engine': 'google',
        'num': 2,
    }

    query_string = urlencode(params)

    url = pathname + "?" + query_string
    # print(url)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # Assuming the response is in JSON format
        # Process the response data
        # print("keys:")
        # print(list(data.keys()))
        # print(data["organic_results"])
        results = data["organic_results"]
        return results
    else:
        print('Request failed with status code:', response.status_code)

    return None

def main():
    with open(cities_path_name) as file:
        data = json.load(file)

    iteration = 0
    for index, city in enumerate(data):

        results = query(city["city"])

        if len(results) > 0:
            city['result_1'] = results[0]["url"]
        if len(results) > 1:
            city['result_2'] = results[1]["url"]
        with open('./city json/main.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        iteration = iteration + 1
        print(iteration)




if __name__ == '__main__':
    main()