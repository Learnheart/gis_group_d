import streamlit as st
import pickle

with open('xGBoost_best_model .pkl', 'rb') as pickle_file:
    content = pickle.load(pickle_file)

st.title('Traffic volumes prediction')