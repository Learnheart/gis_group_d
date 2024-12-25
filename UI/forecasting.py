import streamlit as st
import pandas as pd
import joblib

model_path = '../model_building/saved_feature/gbr.joblib'
model = joblib.load(model_path)

def convert_datetime(date):
    date = pd.DataFrame(date, format='%d-%m-%Y %H:%M')
    df = pd.DataFrame()

    df['year'] = date.dt.year
    df['month'] = date.dt.month
    df['day'] = date.dt.day
    df['hour'] = date.dt.hour
    df['day_in_week'] = date.dt.weekday
    df['is_weekend'] = df['day_in_week'].isin([5, 6]).astype(int)

    return df

def concat_datetime(df, date, datetime):
    data = pd.concat([df, date], axis=1)
    data = data.drop(columns=datetime)

    return data

def main():
    holiday_mapping = {
        'Christmas Day': 0,
        'Columbus Day': 1,
        'Independence Day': 2,
        'Labor Day': 3,
        'Martin Luther King Jr Day': 4,
        'Memorial Day': 5,
        'New Years Day': 6,
        'Normal Day': 7,
        'State Fair': 8,
        'Thanksgiving Day': 9,
        'Veterans Day': 10,
        'Washingtons Birthday': 11
    }

    rain_mapping = {
        'Have rain': 0,
        'No rain': 1
    }

    snow_mapping = {
        'Have snow': 0,
        'No snow': 1
    }




