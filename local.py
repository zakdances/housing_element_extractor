import json
import os.path
import requests

cities_path_name = "./city json/California_Incorporated_Cities.geojson"
abag_path_name = "./city json/ABAG.json"
scag_path_name = "./city json/SCAG.json"
sandag_path_name = "./city json/SANDAG.json"
sacog_path_name = "./city json/SACOG.json"

def map_cities(city_feature):
    properties =  city_feature["properties"]
    city = properties["CITY"]
    county = properties["COUNTY"]
    # country = "USA"
    # state = "California"

    return {
        "city": city,
        "county": county,
    }



def local():
    # Open the file and load the GeoJSON data
    with open(cities_path_name) as file:
        data = json.load(file)
    
    with open(abag_path_name) as file:
        abag_list = json.load(file)
    
    with open(scag_path_name) as file:
        scag_list = json.load(file)
    
    with open(sandag_path_name) as file:
        sandag_list = json.load(file)

    with open(sacog_path_name) as file:
        sacog_list = json.load(file)

    def map_planning_agencies(city_dict):
        planning_agency = ""
        city = city_dict["city"]
        if city in abag_list:
            planning_agency = "ABAG"
        elif city in scag_list:
            planning_agency = "SCAG"
        elif city in sandag_list:
            planning_agency = "SANDAG"
        elif city in sacog_list:
            planning_agency = "SACOG"
        city_dict["planning_agency"] = planning_agency
        return city_dict
    # Now you can work with the loaded GeoJSON data
    # For example, you can access the features like this:
    city_features = data["features"]
    cities = map(map_cities, city_features)
    cities = map(map_planning_agencies, cities)
    cities = list(cities)

    ABAG_cities = 0
    for city in cities:
        if city["planning_agency"] == "ABAG":
            ABAG_cities = ABAG_cities + 1
    print("ABAG cities: " + str(ABAG_cities))

    SACOG_cities = 0
    for city in cities:
        if city["planning_agency"] == "SACOG":
            SACOG_cities = SACOG_cities + 1
    print("SACOG cities: " + str(SACOG_cities))

    SCAG_cities = 0
    for city in cities:
        if city["planning_agency"] == "SCAG":
            SCAG_cities = SCAG_cities + 1
    print("SCAG cities: " + str(SCAG_cities))

    SANDAG_cities = 0
    for city in cities:
        if city["planning_agency"] == "SANDAG":
            SANDAG_cities = SANDAG_cities + 1
    print("SANDAG cities: " + str(SANDAG_cities))

    with open('./city json/main.json', 'w') as f:
        json.dump(cities, f, indent=4)

    return

if __name__ == '__main__':
    local()