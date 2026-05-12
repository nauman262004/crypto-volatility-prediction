# Cryptocurrency Volatility Prediction

## Project Overview
This project predicts cryptocurrency volatility using Machine Learning techniques based on historical cryptocurrency market data such as Open, High, Low, Close prices, Volume, and Market Capitalization.

The project includes:
- Data Preprocessing
- Feature Engineering
- Exploratory Data Analysis (EDA)
- Machine Learning Model Training
- Streamlit Deployment

---

## Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Streamlit

---

## Features
- Predicts cryptocurrency volatility
- Uses Random Forest Regression
- Interactive Streamlit web application
- Visualization of crypto market trends

---

## Machine Learning Workflow
1. Data Collection
2. Data Cleaning
3. Feature Engineering
4. Exploratory Data Analysis
5. Model Training
6. Model Evaluation
7. Streamlit Deployment

---

## Evaluation Metrics
- MAE: 0.0234
- RMSE: 0.0459
- R² Score: 0.6895

---

## Project Structure

```text
crypto-volatility-prediction/
│
├── app.py
├── crypto_volatility_model.pkl
├── cleaned_crypto_data.csv
├── requirements.txt
├── README.md
```

---

## How to Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit app:

```bash
python -m streamlit run app.py
```

---

## Streamlit Application
The Streamlit app allows users to input cryptocurrency market values and predict volatility in real time.

---

## Future Improvements
- Add cryptocurrency selection dropdown
- Add real-time API integration
- Improve UI design
- Use Deep Learning models like LSTM

---

## Author
Mohammed Nauman