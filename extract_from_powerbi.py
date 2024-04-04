import os.path
import json
import requests
import re
from urllib.parse import urlencode

cities_path_name = "./city json/California_Incorporated_Cities.geojson"
main_path_name = "./city json/main.json"

def isUrl(val):
    if isinstance(val, str) and ("http:" in val or "https:" in val):
        return True
    return False

def find_unique_elements(array1, array2):
    set1 = set(array1)
    set2 = set(array2)
    
    unique_elements = set1.symmetric_difference(set2)
    
    return unique_elements

def sort_key(x):
    x = os.path.splitext(x)[0]
    x = x[-6:]
    if x.isdigit():
        return (x[4:], x[:2], x[2:4])
    else:
        return ("010101", x[:2], x[2:4])

def remove_third_float(obj, urls):
    if isinstance(obj, list):
        for item in obj:
            remove_third_float(item, urls)
    elif isinstance(obj, dict):
        # rename_key(obj, "MEGA_APN", "APN")
        # rename_key(obj, "Parcel", "APN") # Marin County
        for key in obj:
            val = obj[key]
            remove_third_float(val, urls)
    elif isUrl(obj):
        urls.add(obj)


def main():

    with open(main_path_name) as file:
        main_list = json.load(file)

    # with open(cities_path_name) as file:
    #     cities = json.load(file)

    with open("./city json/elements_1.json") as file:
        data_1 = json.load(file)
    
    with open("./city json/elements_2.json") as file:
        data_2 = json.load(file)
    
    with open("./city json/elements_3.json") as file:
        data_3 = json.load(file)

    urls = set()
    remove_third_float(data_1, urls)
    remove_third_float(data_2, urls)
    remove_third_float(data_3, urls)
    urls = list(urls)
    # print(urls)

    def compare_strings(string1, string2):
        # Remove spaces, hyphens, and numbers from the strings
        pattern = r'[-\s\d_]'
        cleaned_string1 = re.sub(pattern, '', string1).lower()
        cleaned_string2 = re.sub(pattern, '', string2).lower()

        # Compare the cleaned strings (case-insensitive)
        match_1 = cleaned_string1 in cleaned_string2
        match_2 = cleaned_string2 in cleaned_string1
        # is_county = "county" in (cleaned_string1, cleaned_string2)

        return match_1 or match_2
    
    matches_found = set()
    # city_names = list(map(lambda x: x["city"], main_list))
    for city in main_list:
        city["housing_element"] = []

    for url in urls:
        matched_cities = []
        for city in main_list:
            city_name = city["city"]
            if compare_strings(city_name, url) and url not in matches_found and "county" not in url.lower():
                matched_cities.append(city)
        if len(matched_cities) > 0:
            selected_city = sorted(matched_cities, key=lambda x: len(x['city']), reverse=True)[0]
            selected_city["housing_element"].append(url)
            matches_found.add(url)

    for city in main_list:
        city["housing_element"].sort(key=sort_key, reverse=True)


    # print(len(matches))
    # print(len(urls))
    # print(find_unique_elements(matches, urls))

    with open(main_path_name, 'w') as f:
        json.dump(main_list, f, indent=4)

    # date_list = ["120729", "blah", "070523", "070925", "070120"]
    # date_list.sort(key=lambda x: (x[4:] if x.isdigit() else "010101", x[:2], x[2:4]))
    # date_list.reverse()
    # print(date_list)

if __name__ == '__main__':
    main()