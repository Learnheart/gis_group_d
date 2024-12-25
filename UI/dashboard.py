import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard for analyze traffic pattern")

def display_uploaded_file():
    """
    Handles the file upload, reads the content, and displays the data.
    """
    upload_file = st.sidebar.file_uploader(label="Upload your CSV or Excel file here", type=['csv', 'xlsx'])

    if upload_file is not None:
        try:
            if upload_file.name.endswith('.csv'):
                df = pd.read_csv(upload_file)
            else:
                df = pd.read_excel(upload_file)

            st.write(df)
            return df
        except Exception as e:
            st.error(
                f"An error occurred while reading the file: {e}")
            return None
    return None

def display_top_weather_conditions(df):
    """
    Displays a bar chart for the top 5 weather conditions by average traffic volume.
    """
    if df is not None:
        try:
            # Group the data by weather_main and calculate the mean traffic volume
            grouped_data = df.groupby('weather_main')['traffic_volume'].mean().sort_values(ascending=False)

            # Select the top 5 weather conditions
            top_5_weather = grouped_data.head(5)

            # Create a bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            top_5_weather.plot(kind='bar', color='skyblue', ax=ax)
            ax.set_title('Top 5 Weather Conditions by Traffic Volume')
            ax.set_xlabel('Weather Condition')
            ax.set_ylabel('Average Traffic Volume')
            ax.set_xticks(range(len(top_5_weather)))
            ax.set_xticklabels(top_5_weather.index, rotation=45)

            st.pyplot(fig)
        except KeyError:
            st.error("The dataset does not contain the required columns: 'weather_main' and 'traffic_volume'.")

    else:
        st.warning("No data available. Please upload a valid dataset.")

def traffic_hour(df):
    if df is not None:
        try:
            df['date_time'] = pd.to_datetime(df['date_time'], format='%d-%m-%Y %H:%M', errors='coerce')
            df['hour'] = df['date_time'].dt.hour
            hourly_traffic = df.groupby('hour')['traffic_volume'].mean()

            fig, ax = plt.subplots(figsize=(10, 6))
            hourly_traffic.plot(kind='line', marker='o', color='orange', ax=ax)
            ax.set_title('Hourly Traffic Volume')
            ax.set_xlabel('Hour of the Day')
            ax.set_ylabel('Average Traffic Volume')
            ax.grid(True)

            st.pyplot(fig)
        except KeyError:
            st.error("The dataset does not contain the required columns: 'date_time' in format %d-%m-%Y %H:%M and 'traffic_volume'.")
    else:
        st.warning(
            "No data available. Please upload a valid dataset.")

def traffic_volume_holiday(df):
    if df is not None:
        try:
            holiday_traffic =  df.groupby('holiday')['traffic_volume'].mean().sort_values(ascending=False)

            # Create a bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            holiday_traffic.plot(kind='bar', color='lightgreen', ax=ax)
            ax.set_title('Average Traffic Volume by Holiday')
            ax.set_xlabel('Holiday')
            ax.set_ylabel('Average Traffic Volume')
            ax.set_xticks(range(len(holiday_traffic)))
            ax.set_xticklabels(holiday_traffic.index, rotation=45)

            st.pyplot(fig)
        except KeyError:
            st.error(
                "The dataset does not contain the required columns: 'holiday' and 'traffic_volume'.")

    else:
        st.warning(
            "No data available. Please upload a valid dataset.")

def main():
    df = display_uploaded_file()
    if df is not None:
        chart_select = st.sidebar.selectbox(
            label="Select the chart",
            options=['None', 'Top 5 Weather Conditions by Traffic Volume', 'Hourly Traffic Volume', 'Average Traffic Volume by Holiday'],
            index=0
        )

        if chart_select == 'Top 5 Weather Conditions by Traffic Volume':
            st.subheader('Top 5 Weather Conditions by Traffic Volume')
            display_top_weather_conditions(df)
        elif chart_select == 'Hourly Traffic Volume':
            st.subheader('Hourly Traffic Volume')
            traffic_hour(df)
        elif chart_select == 'Average Traffic Volume by Holiday':
            st.subheader('Average Traffic Volume by Holiday')
            traffic_volume_holiday(df)
        else:
            st.subheader("Please choose a scenario")
    else:
        st.info("Please upload a dataset to proceed.")

if __name__ == "__main__":
    main()
