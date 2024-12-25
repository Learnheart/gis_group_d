import streamlit as st
import os

def main():
    page = st.sidebar.radio("Select a page", ["Visualize data dashboard", "Forecasting traffic volume"])

    if page == "Visualize data dashboard":
        import dashboard
        dashboard.main()

    elif page == "Forecasting traffic volume":
        import forecasting
        forecasting.main()


if __name__ == "__main__":
    main()
