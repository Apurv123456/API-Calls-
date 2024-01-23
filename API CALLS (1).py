#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import json
import time
import requests
from datetime import datetime


df = pd.DataFrame()

def make_api_call(target_date):
    api_url = f""  # use your URl between " "

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            api_data = response.json()
            update_dataframe(api_data)

        else:
            print(f"API request failed with status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def update_dataframe(api_data):

    vehicle_data = api_data.get("root", {}).get("Vehicle_No", [])

    if vehicle_data:

        first_vehicle = vehicle_data[0]

     # you can write your column name as per use  
        relevant_columns = [                
            "Latitude",
            "Longitude",
            "GPSActualTime",
            "Power",
            "Speed",
            "IGN",
            "Vehicle_No"
        ]


        global df
        new_df = pd.DataFrame({key: first_vehicle.get(key, None) for key in relevant_columns}, index=[0])
        df = pd.concat([new_df, df]).reset_index(drop=True)
        print("Updated Dataframe:")
        print(df)


current_date = datetime.now().strftime("%Y-%m-%d")


num_api_calls = 24 * 120


for i in range(num_api_calls):
    print(f"Making API call {i + 1} for date {current_date}")
    make_api_call(current_date)

  
    if i < num_api_calls - 1:
        print("Waiting for 2 minutes...")
        time.sleep(120)

        

