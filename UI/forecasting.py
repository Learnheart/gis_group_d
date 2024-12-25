import streamlit as st
import pandas as pd
import joblib
from datetime import datetime, time

model_path = '../model_building/saved_feature/xgb.joblib'
model = joblib.load(model_path)

def convert_datetime(date):
    # convert to pandas dataframe
    date = pd.to_datetime(date)
    df = pd.DataFrame()

    date_series = pd.Series([date])

    df['year'] = date_series.dt.year
    df['month'] = date_series.dt.month
    df['day'] = date_series.dt.day
    df['hour'] = date_series.dt.hour
    df['day_in_week'] = date_series.dt.weekday
    df['is_weekend'] = date_series.dt.weekday.isin([5, 6]).astype(int)

    return df


def convert_temp(temp, scale):
    if scale == 'Celsius (C)':
        K_temp = temp + 273.15
    elif scale == 'Fahrenheit (F)':
        K_temp = ((temp - 32) * 5/9) + 273.15
    return K_temp

# traffic light time
def calculate_traffic_light_times(traffic_volume):
    max_green_time = 70
    max_red_time = 120

    red_time = (traffic_volume / 7000) * max_green_time
    green_time = ((7000 - traffic_volume) / 6000) * max_red_time

    return green_time, red_time

def main():
    st.title('Traffic Volumes Prediction')
    st.markdown("""
        Provide these information to make forecasting
    """)

    # Input fields
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

    cloud_mapping = {
        'Clear': 0,
        'Mostly Cloudy': 1,
        'Overcast': 2,
        'Party Cloudy': 3
    }

    weather_mapping = {
        'Clear': 0,
        'Clouds': 1,
        'Mist': 2,
        'Rain': 3,
        'Snow': 4
    }

    holiday = st.selectbox("Select holiday:", list(holiday_mapping.keys()))
    encoded_holiday = holiday_mapping[holiday]

    temp = st.number_input("Input temperature", step=0.1)
    temp_scale = st.selectbox("Select temperature scale:", ['Celsius (C)', 'Fahrenheit (F)'])
    temp_in_kelvin = convert_temp(temp, temp_scale)  # Convert temperature to Kelvin

    rain = st.selectbox("Select rain condition: ", list(rain_mapping.keys()))
    encoded_rain = rain_mapping[rain]

    snow = st.selectbox("Select snow condition: ", list(snow_mapping.keys()))
    encoded_snow = snow_mapping[snow]

    cloud = st.selectbox("Select cloud condition: ", list(cloud_mapping.keys()))
    encoded_cloud = cloud_mapping[cloud]

    weather = st.selectbox("Select weather condition: ", list(weather_mapping.keys()))
    encoded_weather = weather_mapping[weather]

    date = st.date_input("Select a date: ", value=datetime(2024, 12, 18).date())
    time_input = st.time_input("Select a time", value=time(8, 0))

    datetime_value = datetime.combine(date, time_input)
    datetime_df = convert_datetime(datetime_value)

    # Process after pressing the button
    if st.button("Predict Traffic Volumes"):
        input_data = {
            "holiday": encoded_holiday,
            "temp": temp_in_kelvin,
            "rain_1h": encoded_rain,
            "snow_1h": encoded_snow,
            "clouds_all": encoded_cloud,
            "weather_main": encoded_weather,
            "year": datetime_df['year'].iloc[0],
            "month": datetime_df['month'].iloc[0],
            "day": datetime_df['day'].iloc[0],
            "hour": datetime_df['hour'].iloc[0],
            "day_in_week": datetime_df['day_in_week'].iloc[0],
            "is_weekend": datetime_df['is_weekend'].iloc[0]
        }

        input_df = pd.DataFrame([input_data])
        print(input_data)
        # Make prediction
        prediction = model.predict(input_df)
        predicted_traffic_volume = prediction[0]
        st.success(f"The predicted traffic volume is: {prediction[0]:.0f}")

        # Traffic light time suggestion
        green_time, red_time = calculate_traffic_light_times(
            predicted_traffic_volume)
        st.sidebar.subheader(
            "Suggested Traffic Light Timings")
        st.sidebar.write(
            f"**Green Light Time:** {green_time:.2f} seconds")
        st.sidebar.write(
            f"**Red Light Time:** {red_time:.2f} seconds")

if __name__ == "__main__":
    main()
