import streamlit as st
import joblib
import numpy as np

model = joblib.load("crypto_volatility_model.pkl")

st.title("Cryptocurrency Volatility Prediction")

st.write("Enter cryptocurrency market values to predict volatility.")

open_price = st.number_input("Open Price", min_value=0.0)
high_price = st.number_input("High Price", min_value=0.0)
low_price = st.number_input("Low Price", min_value=0.0)
close_price = st.number_input("Close Price", min_value=0.0)
volume = st.number_input("Volume", min_value=0.0)
market_cap = st.number_input("Market Cap", min_value=0.0)

if open_price > 0 and market_cap > 0:
    daily_return = (close_price - open_price) / open_price
    ma_7 = close_price
    rolling_volatility = high_price - low_price
    liquidity_ratio = volume / market_cap
else:
    daily_return = 0
    ma_7 = 0
    rolling_volatility = 0
    liquidity_ratio = 0

if st.button("Predict Volatility"):
    input_data = np.array([[
        open_price,
        high_price,
        low_price,
        close_price,
        volume,
        market_cap,
        daily_return,
        ma_7,
        rolling_volatility,
        liquidity_ratio
    ]])

    prediction = model.predict(input_data)

    st.success(f"Predicted Volatility: {prediction[0]:.4f}")