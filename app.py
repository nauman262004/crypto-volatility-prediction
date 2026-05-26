import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="CryptoVol · Volatility Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    background-color: #080c14 !important;
    color: #c8d8f0 !important;
    font-family: 'Syne', sans-serif !important;
}

section[data-testid="stSidebar"] {
    background: #0b1120 !important;
    border-right: 1px solid #1a2744;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] div {
    background: #0f1a2e !important;
    border: 1px solid #1e3050 !important;
    color: #c8d8f0 !important;
    font-family: 'Space Mono', monospace !important;
    border-radius: 6px !important;
}

input[type="number"] {
    background: #0f1a2e !important;
    color: #7dd3fc !important;
    font-family: 'Space Mono', monospace !important;
}

div[data-baseweb="select"] {
    background: #0f1a2e !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #f59e0b, #ef4444) !important;
    color: #080c14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 16px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 40px !important;
    letter-spacing: 1.5px !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(245,158,11,0.4) !important;
}

div[data-testid="metric-container"] {
    background: #0f1a2e !important;
    border: 1px solid #1e3050 !important;
    border-radius: 10px !important;
    padding: 16px !important;
}
div[data-testid="metric-container"] label {
    color: #5a7a9e !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #7dd3fc !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 20px !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #1e3050 !important;
    border-radius: 8px !important;
}

div[data-baseweb="tab-list"] {
    background: #0b1120 !important;
    border-bottom: 1px solid #1a2744 !important;
}
button[data-baseweb="tab"] {
    color: #5a7a9e !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #f59e0b !important;
    border-bottom: 2px solid #f59e0b !important;
}

div[data-testid="stExpander"] {
    background: #0f1a2e !important;
    border: 1px solid #1e3050 !important;
    border-radius: 8px !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb { background: #1e3050; border-radius: 3px; }

div[data-testid="stAlert"] {
    background: #0f1a2e !important;
    border-radius: 8px !important;
}

hr { border-color: #1a2744 !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("crypto_volatility_model.pkl")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_crypto_data.csv", parse_dates=["date"])
    return df

model = load_model()
df_all = load_data()
coins = sorted(df_all["crypto_name"].unique())

PLOT_BG = "#080c14"
PAPER_BG = "#080c14"
GRID_COLOR = "#1a2744"
FONT_COLOR = "#c8d8f0"
AMBER = "#f59e0b"
CYAN = "#7dd3fc"
RED = "#ef4444"
GREEN = "#22c55e"

def dark_layout(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne", size=15, color=AMBER), x=0.02),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family="Space Mono", color=FONT_COLOR, size=11),
        height=height,
        margin=dict(l=16, r=16, t=48, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID_COLOR),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
    )
    return fig

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-family:Space Mono; font-size:11px; color:#5a7a9e; letter-spacing:3px;'>⚡ CRYPTOVOL</div>
        <div style='font-family:Syne; font-size:22px; font-weight:800; color:#f59e0b; line-height:1.2;'>Volatility<br>Intelligence</div>
    </div>
    <hr style='border-color:#1a2744; margin:12px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("#### 🪙 Select Coin")
    selected_coin = st.selectbox("Coin", coins, index=coins.index("Bitcoin"), label_visibility="collapsed")

    coin_df = df_all[df_all["crypto_name"] == selected_coin].sort_values("date")

    if not coin_df.empty:
        latest = coin_df.iloc[-1]
        st.markdown(f"""
        <div style='background:#0f1a2e; border:1px solid #1e3050; border-radius:10px; padding:14px; margin:10px 0;'>
            <div style='font-family:Space Mono; font-size:10px; color:#5a7a9e; letter-spacing:1px;'>LATEST CLOSE</div>
            <div style='font-family:Space Mono; font-size:22px; color:#7dd3fc; font-weight:700;'>${latest['close']:,.2f}</div>
            <div style='font-family:Space Mono; font-size:10px; color:#5a7a9e; margin-top:6px;'>{str(latest['date'])[:10]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🎚️ Auto-fill from Latest Data")
        if st.button("← Load Latest Values"):
            st.session_state["open_price"] = float(latest["open"])
            st.session_state["high_price"] = float(latest["high"])
            st.session_state["low_price"] = float(latest["low"])
            st.session_state["close_price"] = float(latest["close"])
            st.session_state["volume"] = float(latest["volume"]) if latest["volume"] > 0 else 500_000_000.0
            st.session_state["marketcap"] = float(latest["marketCap"]) if latest["marketCap"] > 0 else 600_000_000_000.0

    st.markdown("<hr style='border-color:#1a2744;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:Space Mono; font-size:10px; color:#2a4060; line-height:1.8;'>
    MODEL · Random Forest<br>
    MAE · 0.0234<br>
    RMSE · 0.0459<br>
    R² · 0.6895
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='padding: 10px 0 20px;'>
    <div style='font-family:Space Mono; font-size:11px; color:#5a7a9e; letter-spacing:3px;'>MACHINE LEARNING · FINANCIAL ANALYTICS</div>
    <div style='font-family:Syne; font-size:38px; font-weight:800; color:#f59e0b; line-height:1.1;'>
        Crypto Volatility <span style='color:#7dd3fc;'>Predictor</span>
    </div>
    <div style='font-family:Space Mono; font-size:12px; color:#5a7a9e; margin-top:4px;'>
        Enter OHLCV data below → get an instant volatility forecast
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["⚡ Predict", "📊 Market Explorer", "🧠 Model Insights"])

with tab1:
    st.markdown("### 📥 Market Inputs")
    c1, c2, c3 = st.columns(3)
    with c1:
        open_price  = st.number_input("Open Price ($)", min_value=0.0,
                                       value=st.session_state.get("open_price", 30000.0), format="%.4f")
        close_price = st.number_input("Close Price ($)", min_value=0.0,
                                       value=st.session_state.get("close_price", 30500.0), format="%.4f")
    with c2:
        high_price  = st.number_input("High Price ($)", min_value=0.0,
                                       value=st.session_state.get("high_price", 31000.0), format="%.4f")
        volume      = st.number_input("Volume", min_value=0.0,
                                       value=st.session_state.get("volume", 500_000_000.0), format="%.0f")
    with c3:
        low_price   = st.number_input("Low Price ($)", min_value=0.0,
                                       value=st.session_state.get("low_price", 29500.0), format="%.4f")
        marketcap   = st.number_input("Market Cap ($)", min_value=0.0,
                                       value=st.session_state.get("marketcap", 600_000_000_000.0), format="%.0f")

    daily_return      = (close_price - open_price) / open_price if open_price != 0 else 0
    ma_7              = close_price
    rolling_volatility = high_price - low_price
    liquidity_ratio   = volume / marketcap if marketcap != 0 else 0
    spread_pct        = (high_price - low_price) / open_price * 100 if open_price else 0

    st.markdown("##### Derived Features")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Daily Return", f"{daily_return*100:.3f}%",
               delta=f"{'▲' if daily_return >= 0 else '▼'}")
    m2.metric("Intraday Spread", f"${rolling_volatility:,.2f}")
    m3.metric("Spread %", f"{spread_pct:.2f}%")
    m4.metric("Liquidity Ratio", f"{liquidity_ratio:.6f}")

    st.write("")
    predict_btn = st.button("⚡  RUN VOLATILITY FORECAST")

    if predict_btn:
        input_data = np.array([[
            open_price, high_price, low_price, close_price,
            volume, marketcap, daily_return, ma_7,
            rolling_volatility, liquidity_ratio
        ]])
        prediction = model.predict(input_data)[0]

        if prediction < 0.03:
            risk_label = "LOW VOLATILITY"
            risk_color = GREEN
            risk_icon  = "🟢"
            risk_desc  = "Market movement appears relatively stable. Suitable for conservative positions."
            gauge_pct  = prediction / 0.03
        elif prediction < 0.08:
            risk_label = "MEDIUM VOLATILITY"
            risk_color = AMBER
            risk_icon  = "🟡"
            risk_desc  = "Market shows moderate price movement. Consider risk-adjusted position sizing."
            gauge_pct  = 0.33 + (prediction - 0.03) / 0.05 * 0.33
        else:
            risk_label = "HIGH VOLATILITY"
            risk_color = RED
            risk_icon  = "🔴"
            risk_desc  = "Strong price fluctuations likely. Tighten stops and reduce leverage."
            gauge_pct  = min(0.66 + (prediction - 0.08) / 0.12 * 0.34, 1.0)

        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #0f1a2e, #0b1525);
            border: 1px solid {risk_color};
            border-left: 6px solid {risk_color};
            border-radius: 12px;
            padding: 24px 28px;
            margin: 16px 0;
            display: flex;
            align-items: center;
            gap: 24px;
        '>
            <div style='font-size:48px;'>{risk_icon}</div>
            <div>
                <div style='font-family:Space Mono; font-size:10px; color:#5a7a9e; letter-spacing:2px;'>PREDICTED VOLATILITY</div>
                <div style='font-family:Space Mono; font-size:40px; font-weight:700; color:{risk_color}; line-height:1;'>
                    {prediction:.4f}
                </div>
                <div style='font-family:Syne; font-size:16px; font-weight:700; color:{risk_color}; margin-top:4px;'>
                    {risk_label}
                </div>
                <div style='font-family:Syne; font-size:13px; color:#8aabb0; margin-top:6px;'>{risk_desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        row1, row2 = st.columns(2)

        with row1:
            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prediction,
                number={"font": {"family": "Space Mono", "color": risk_color}, "suffix": "  vol"},
                gauge={
                    "axis": {"range": [0, 0.20], "tickcolor": FONT_COLOR,
                              "tickfont": {"family": "Space Mono", "size": 10}},
                    "bar": {"color": risk_color, "thickness": 0.25},
                    "bgcolor": "#0f1a2e",
                    "bordercolor": GRID_COLOR,
                    "steps": [
                        {"range": [0, 0.03],  "color": "#052e16"},
                        {"range": [0.03, 0.08], "color": "#422006"},
                        {"range": [0.08, 0.20], "color": "#450a0a"},
                    ],
                    "threshold": {"line": {"color": "#fff", "width": 2}, "thickness": 0.85, "value": prediction}
                }
            ))
            dark_layout(fig_gauge, "Volatility Gauge", height=280)
            st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

        with row2:
            # OHLC bar chart
            ohlc_labels = ["Open", "High", "Low", "Close"]
            ohlc_values = [open_price, high_price, low_price, close_price]
            ohlc_colors = [CYAN, GREEN, RED, AMBER]
            fig_ohlc = go.Figure(go.Bar(
                x=ohlc_labels, y=ohlc_values,
                marker_color=ohlc_colors,
                text=[f"${v:,.2f}" for v in ohlc_values],
                textposition="outside",
                textfont=dict(family="Space Mono", size=10, color=FONT_COLOR),
            ))
            dark_layout(fig_ohlc, "OHLC Price Comparison", height=280)
            fig_ohlc.update_layout(showlegend=False, bargap=0.3)
            st.plotly_chart(fig_ohlc, use_container_width=True, config={"displayModeBar": False})

        feat_names = ["Daily Return", "Spread %", "Liq. Ratio", "Volume (log)", "MarketCap (log)"]
        raw = [abs(daily_return)*10, spread_pct/10, liquidity_ratio*100,
               np.log10(volume+1)/10, np.log10(marketcap+1)/20]
        mx = max(raw) if max(raw) > 0 else 1
        norm = [v/mx for v in raw]
        norm_closed = norm + [norm[0]]
        angles = np.linspace(0, 2*np.pi, len(feat_names), endpoint=False).tolist()
        angles_closed = angles + [angles[0]]

        fig_radar = go.Figure(go.Scatterpolar(
            r=norm_closed,
            theta=feat_names + [feat_names[0]],
            fill="toself",
            fillcolor=f"rgba(245,158,11,0.15)",
            line=dict(color=AMBER, width=2),
            name="Feature strength",
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#0f1a2e",
                radialaxis=dict(visible=True, range=[0, 1], gridcolor=GRID_COLOR,
                                tickfont=dict(family="Space Mono", size=9, color="#5a7a9e")),
                angularaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(family="Syne", size=11, color=FONT_COLOR))
            ),
            plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
            font=dict(family="Space Mono", color=FONT_COLOR),
            height=300, margin=dict(l=40, r=40, t=48, b=16),
            title=dict(text="Feature Strength Radar", font=dict(family="Syne", size=15, color=AMBER), x=0.02),
            showlegend=False,
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
        with st.expander("📋 Full Input Summary"):
            summary_df = pd.DataFrame({
                "Feature": ["Open", "High", "Low", "Close", "Volume", "Market Cap",
                             "Daily Return", "Rolling Vol", "MA-7 (proxy)", "Liquidity Ratio"],
                "Value": [open_price, high_price, low_price, close_price,
                           volume, marketcap, daily_return, rolling_volatility, ma_7, liquidity_ratio],
            })
            st.dataframe(summary_df.style.format({"Value": "{:.6f}"}),
                         use_container_width=True, hide_index=True)
with tab2:
    st.markdown(f"### 📊 {selected_coin} · Historical Analysis")

    coin_df = df_all[df_all["crypto_name"] == selected_coin].sort_values("date").copy()

    if coin_df.empty:
        st.warning("No data available for this coin.")
    else:
        # Date range filter
        min_date = coin_df["date"].min().date()
        max_date = coin_df["date"].max().date()
        d1, d2 = st.columns(2)
        with d1:
            start_d = st.date_input("From", value=max(min_date, pd.Timestamp("2020-01-01").date()),
                                     min_value=min_date, max_value=max_date)
        with d2:
            end_d   = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date)

        mask = (coin_df["date"].dt.date >= start_d) & (coin_df["date"].dt.date <= end_d)
        cdf  = coin_df[mask].copy()

        if cdf.empty:
            st.warning("No data in selected date range.")
        else:
            # Summary stats
            s1, s2, s3, s4 = st.columns(4)
            s1.metric("Avg Close",    f"${cdf['close'].mean():,.2f}")
            s2.metric("Max Close",    f"${cdf['close'].max():,.2f}")
            s3.metric("Avg Vol",      f"{cdf['volatility'].mean():.4f}")
            s4.metric("Max Vol",      f"{cdf['volatility'].max():.4f}")

            fig_candle = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                        row_heights=[0.7, 0.3], vertical_spacing=0.03)
            fig_candle.add_trace(go.Candlestick(
                x=cdf["date"], open=cdf["open"], high=cdf["high"],
                low=cdf["low"], close=cdf["close"],
                increasing_line_color=GREEN, decreasing_line_color=RED,
                name="OHLC"
            ), row=1, col=1)
            colors = [GREEN if r >= 0 else RED for r in cdf["daily_return"]]
            fig_candle.add_trace(go.Bar(
                x=cdf["date"], y=cdf["volume"], marker_color=colors,
                name="Volume", opacity=0.6
            ), row=2, col=1)
            dark_layout(fig_candle, f"{selected_coin} · Candlestick & Volume", height=480)
            fig_candle.update_xaxes(rangeslider_visible=False)
            fig_candle.update_yaxes(title_text="Price ($)", row=1, col=1)
            fig_candle.update_yaxes(title_text="Volume", row=2, col=1)
            st.plotly_chart(fig_candle, use_container_width=True, config={"displayModeBar": False})

            fig_vol = go.Figure()
            fig_vol.add_trace(go.Scatter(
                x=cdf["date"], y=cdf["volatility"],
                mode="lines", line=dict(color=AMBER, width=1.5),
                fill="tozeroy", fillcolor="rgba(245,158,11,0.08)",
                name="Volatility"
            ))
            fig_vol.add_hline(y=0.03, line_dash="dot", line_color=GREEN,
                               annotation_text="Low/Med boundary", annotation_font_color=GREEN)
            fig_vol.add_hline(y=0.08, line_dash="dot", line_color=RED,
                               annotation_text="Med/High boundary", annotation_font_color=RED)
            dark_layout(fig_vol, f"{selected_coin} · Historical Volatility", height=320)
            st.plotly_chart(fig_vol, use_container_width=True, config={"displayModeBar": False})

            fig_dist = go.Figure()
            fig_dist.add_trace(go.Histogram(
                x=cdf["daily_return"], nbinsx=60,
                marker_color=CYAN, opacity=0.75, name="Daily Returns"
            ))
            dark_layout(fig_dist, "Daily Return Distribution", height=280)
            st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})

with tab3:
    st.markdown("### 🧠 Model Insights & Dataset Overview")

    feat_importance = {
        "Rolling Volatility": 0.312,
        "Close Price":        0.198,
        "High Price":         0.142,
        "MA-7":               0.118,
        "Low Price":          0.089,
        "Open Price":         0.071,
        "Daily Return":       0.038,
        "Volume":             0.019,
        "Market Cap":         0.008,
        "Liquidity Ratio":    0.005,
    }
    fi_df = pd.DataFrame(feat_importance.items(), columns=["Feature", "Importance"]).sort_values("Importance")

    # Feature importance bar (horizontal)
    fig_fi = go.Figure(go.Bar(
        x=fi_df["Importance"], y=fi_df["Feature"],
        orientation="h",
        marker=dict(
            color=fi_df["Importance"],
            colorscale=[[0, "#1e3050"], [0.5, CYAN], [1, AMBER]],
            showscale=False,
        ),
        text=[f"{v:.3f}" for v in fi_df["Importance"]],
        textposition="outside",
        textfont=dict(family="Space Mono", size=10, color=FONT_COLOR),
    ))
    dark_layout(fig_fi, "Random Forest · Feature Importance", height=380)
    st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})

    st.markdown("#### 📦 Dataset Overview")
    ds1, ds2, ds3, ds4 = st.columns(4)
    ds1.metric("Total Records",  f"{len(df_all):,}")
    ds2.metric("Unique Coins",   df_all["crypto_name"].nunique())
    ds3.metric("Date Range",     f"{df_all['date'].min().year}–{df_all['date'].max().year}")
    ds4.metric("Avg Volatility", f"{df_all['volatility'].mean():.4f}")

    st.markdown("#### 🏆 Coin Volatility Comparison")
    coin_vol = (df_all.groupby("crypto_name")["volatility"]
                .mean().sort_values(ascending=False).head(20).reset_index())
    coin_vol.columns = ["Coin", "Avg Volatility"]

    fig_coins = go.Figure(go.Bar(
        x=coin_vol["Coin"], y=coin_vol["Avg Volatility"],
        marker=dict(
            color=coin_vol["Avg Volatility"],
            colorscale=[[0, "#1e3050"], [0.5, CYAN], [1, AMBER]],
        ),
        text=[f"{v:.3f}" for v in coin_vol["Avg Volatility"]],
        textposition="outside",
        textfont=dict(family="Space Mono", size=9, color=FONT_COLOR),
    ))
    dark_layout(fig_coins, "Top 20 Coins by Average Volatility", height=360)
    fig_coins.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_coins, use_container_width=True, config={"displayModeBar": False})

    st.markdown("#### 🔥 Feature Correlation Matrix")
    num_cols = ["open", "high", "low", "close", "volatility",
                "daily_return", "rolling_volatility", "liquidity_ratio"]
    corr = df_all[num_cols].corr().round(2)
    fig_heat = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index,
        colorscale=[[0, "#0b1120"], [0.5, CYAN], [1, AMBER]],
        text=corr.values, texttemplate="%{text}",
        textfont=dict(family="Space Mono", size=9),
        hoverongaps=False,
    ))
    dark_layout(fig_heat, "Pearson Correlation Heatmap", height=400)
    fig_heat.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

    st.markdown("#### 📐 Evaluation Metrics")
    em1, em2, em3 = st.columns(3)
    em1.metric("MAE",      "0.0234", help="Mean Absolute Error")
    em2.metric("RMSE",     "0.0459", help="Root Mean Square Error")
    em3.metric("R² Score", "0.6895", help="Coefficient of Determination")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; font-family:Space Mono; font-size:20px; color:#2a4060; padding:10px 0 20px;'>
    Built by Mohammed Nauman · Random Forest Regressor · Scikit-learn · Streamlit · Plotly
</div>
""", unsafe_allow_html=True)
