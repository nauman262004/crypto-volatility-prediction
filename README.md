# ⚡ CryptoVol — Cryptocurrency Volatility Predictor

> Predict cryptocurrency market volatility in real time using Machine Learning.  
> Built with Random Forest Regression, trained on 70,000+ records across 56 cryptocurrencies.

---

## 📌 Problem Statement

Cryptocurrency markets are among the most volatile financial markets in the world. Prices can swing **20–30% in a single day**, yet most retail investors have no reliable way to measure or anticipate that risk. They rely on gut feeling, news headlines, or basic charts — and often pay the price.

This project addresses that gap by building a Machine Learning model that forecasts volatility from historical OHLCV (Open, High, Low, Close, Volume) data, giving investors a quantified risk signal before they act.

---

## 🎯 Project Highlights

- 📦 **70,000+ records** across **56 real cryptocurrencies** (Bitcoin, Ethereum, Solana & more)
- 🤖 **Random Forest Regression** with engineered market features
- 🟢🟡🔴 **3-tier risk classification** — Low / Medium / High volatility
- 📊 **Interactive Streamlit dashboard** with candlestick charts, volatility trends & feature analysis
- ⚡ **One-click auto-fill** from latest historical data per coin

---

## 📈 Evaluation Metrics

| Metric | Score |
|--------|-------|
| MAE (Mean Absolute Error) | 0.0234 |
| RMSE (Root Mean Square Error) | 0.0459 |
| R² Score | 0.6895 |

---

## 🗂️ Project Structure

```
crypto-volatility-prediction/
│
├── app.py                      # Streamlit web application
├── crypto_volatility_model.pkl # Trained Random Forest model
├── cleaned_crypto_data.csv     # Preprocessed dataset (70K+ rows, 56 coins)
├── ML_Project.ipynb            # Full ML workflow notebook
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🔧 Tech Stack

| Layer | Tools |
|-------|-------|
| Language | Python 3 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Plotly |
| Web App | Streamlit |
| Model Persistence | Joblib |

---

## 🧠 ML Workflow

```
1. Data Collection         →  Historical OHLCV data for 56 cryptocurrencies
2. Data Cleaning           →  Handle missing values, type casting, outlier removal
3. Feature Engineering     →  Daily Return, Rolling Volatility, MA-7, Liquidity Ratio
4. Exploratory Data Analysis → Correlation heatmaps, distribution plots, trend analysis
5. Model Training          →  Random Forest Regressor (scikit-learn)
6. Model Evaluation        →  MAE, RMSE, R² Score
7. Deployment              →  Interactive Streamlit app
```

---

## 🔢 Features Used

| Feature | Description |
|---------|-------------|
| `open` | Opening price of the day |
| `high` | Highest price of the day |
| `low` | Lowest price of the day |
| `close` | Closing price of the day |
| `volume` | Total trading volume |
| `marketCap` | Market capitalization |
| `daily_return` | `(close - open) / open` |
| `ma_7` | 7-day moving average (proxy) |
| `rolling_volatility` | `high - low` intraday spread |
| `liquidity_ratio` | `volume / marketCap` |

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/your-username/crypto-volatility-prediction.git
cd crypto-volatility-prediction
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Launch the Streamlit app**
```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🖥️ App Features

### ⚡ Predict Tab
- Enter OHLCV values manually **or** auto-fill from the latest historical data of any coin
- Instant volatility prediction with a visual gauge chart
- Risk classification with actionable market insight
- Feature strength radar chart
- OHLC price comparison bar chart

### 📊 Market Explorer Tab
- Select any of the 56 supported cryptocurrencies
- Filter by custom date range
- Interactive **candlestick chart** with volume bars
- Historical volatility trend with Low/High threshold lines
- Daily return distribution histogram

### 🧠 Model Insights Tab
- Feature importance rankings from the Random Forest model
- Dataset overview (70K+ records, date range, avg volatility)
- Top 20 coins by average historical volatility
- Pearson correlation heatmap across all features

---

## 📊 Dataset Overview

| Property | Value |
|----------|-------|
| Total Records | 70,465 |
| Unique Cryptocurrencies | 56 |
| Date Range | 2013 – 2024 |
| Target Variable | `volatility` (continuous) |
| Avg Volatility | ~0.05 |

**Supported Coins include:** Bitcoin, Ethereum, Solana, BNB, XRP, Cardano, Dogecoin, Polygon, Avalanche, Chainlink, Uniswap, Shiba Inu, Polkadot, and 43 more.

---

## 🔮 Future Improvements

- [ ] Real-time price API integration
- [ ] LSTM / Transformer-based deep learning model
- [ ] Alert system for high-volatility conditions

---

## 👤 Author

**Mohammed Nauman**  
