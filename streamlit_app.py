# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import sklearn
import pickle
import streamlit as st

class CustomScaler:
    def __init__(self, columns_to_scale):
        self.columns_to_scale = columns_to_scale
        self.scaler = StandardScaler()

    def fit(self, data):
        selected_columns_data = data[self.columns_to_scale]
        self.scaler.fit(selected_columns_data)

    def transform(self, data):
        scaled_data = data.copy()
        selected_columns_data = data[self.columns_to_scale]
        selected_columns_scaled = self.scaler.transform(selected_columns_data)
        scaled_columns_df = pd.DataFrame(selected_columns_scaled, columns=self.columns_to_scale, index=data.index)
        scaled_data[self.columns_to_scale] = scaled_columns_df
        return scaled_data

loaded_model = pickle.load(open('C:/Users/Joseph/Documents/Prediction_Model/Prediction_Model.pkl', 'rb'))
loaded_scaler = pickle.load(open('C:/Users/Joseph/Documents/Prediction_Model/Prediction_Scaler.pkl', 'rb'))

def append_input_data(data_frame, input_data):
    
    longitude, latitude, housing_median_age, total_rooms, total_bedrooms, population, households, \
    median_income, ocean, inland, island, near_bay, near_ocean, bedroom_ratio, household_rooms = input_data

    
    new_data = {'longitude': [longitude], 'latitude': [latitude], 'housing_median_age': [housing_median_age],
                'total_rooms': [total_rooms], 'total_bedrooms': [total_bedrooms], 'population': [population],
                'households': [households], 'median_income': [median_income], '<1H OCEAN': [ocean], 'INLAND': [inland],
                'ISLAND': [island], 'NEAR BAY': [near_bay], 'NEAR OCEAN': [near_ocean],
                'bedroom_ratio': [bedroom_ratio], 'household_rooms': [household_rooms] }

    new_df = pd.DataFrame(new_data)
    updated_df = pd.concat([data_frame, new_df], ignore_index=True)
    return updated_df

data = {'longitude' : [], 'latitude' : [], 'housing_median_age' : [], 'total_rooms': [],
       'total_bedrooms' : [], 'population' : [], 'households' : [], 'median_income' : [],
       '<1H OCEAN' : [], 'INLAND' : [], 'ISLAND' : [], 'NEAR BAY' : [],
       'NEAR OCEAN' : [], 'bedroom_ratio' : [], 'household_rooms' : []}
df = pd.DataFrame(data)


def House_Price_Prediction(input_data):
    
    dff = append_input_data(df, input_data)

    last_row = dff.tail(1)
    last_row

    input_data = (last_row)

    loaded_scaler.fit(input_data)
    scaled_data = loaded_scaler.transform(input_data)

    prediction = loaded_model.predict(scaled_data)
    predictionn = ', '.join(map(str, prediction))

    additional_text = 'The price is estimated to be around :'
    result = additional_text, predictionn
    
    output = "{} {}".format(result[0], result[1])
    
    return output

def main():
    
    st.title('House Price Prediction Web App')
    
    Longitude = st.text_input('Longitude Coordinate')
    Latitude = st.text_input('Latitude Coordinate')
    HousingMedianAge = st.text_input('Median Age Of Houses In The Area')
    TotalRooms = st.text_input('Total Number Of Rooms In The Area')
    TotalBedrooms = st.text_input('Total Number Of Bedrooms In The Area')
    Population = st.text_input('Total Number Of People Residing In The Area')
    Households = st.text_input('Total Number Of Households In The Area')
    MedianIncome = st.text_input('Median Income Of Residents In the Area')
    LessThanAnHourToTheOcean = st.text_input('Is Building Less Than An Hour To The Ocean')
    INLAND = st.text_input('Is It INLAND? Write (1) if yes or (0) if No')
    ISLAND = st.text_input('Is It On An ISLAND? Write (1) if yes or (0) if No')
    NEARBAY = st.text_input('Is It NEAR A BAY? Write (1) if yes or (0) if No')
    NEAROCEAN = st.text_input('Is It NEAR An OCEAN? Write (1) if yes or (0) if No')
    BedroomRatio = st.text_input('Bedroom Ratio? Total Bedrooms / Total Rooms')
    HouseholdRooms = st.text_input('Total Number Of Household rooms In The Area')
    
    price = ''
    
    if st.button('Check Price'):
        price = House_Price_Prediction([Longitude, Latitude, HousingMedianAge,
                                        TotalRooms, TotalBedrooms, Population, Households, MedianIncome,
                                        LessThanAnHourToTheOcean, INLAND, ISLAND, NEARBAY,
                                        NEAROCEAN, BedroomRatio, HouseholdRooms])
    st.success(price)    


if __name__ == '__main__':
    main()
    
