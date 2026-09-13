"""
Student Mental Health Score Predictor — Streamlit Frontend
Talks to the FastAPI backend defined in main.py (the /predict endpoint).
"""

import requests
import streamlit as st
import plotly.graph_objects as go

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Mental Health Score Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Custom CSS
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(180deg, #0f1117 0%, #161a23 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
        }
        .hero {
            text-align: center;
            padding: 1.5rem 0 0.5rem 0;
        }
        .hero h1 {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(90deg, #7C3AED, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
        }
        .hero p {
            color: #9CA3AF;
            font-size: 1.05rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            font-weight: 700;
            font-size: 1.05rem;
            background: linear-gradient(90deg, #7C3AED, #06B6D4);
            color: white;
            border: none;
            transition: transform 0.15s ease;
        }
        .stButton>button:hover {
            transform: scale(1.02);
        }
        .result-card {
            background: #1B1F2A;
            border-radius: 16px;
            padding: 1.5rem 2rem;
            border: 1px solid #2A2F3D;
        }
        .metric-pill {
            background: #1B1F2A;
            border-radius: 12px;
            padding: 0.8rem 1rem;
            border: 1px solid #2A2F3D;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🧠 Student Mental Health Score Predictor</h1>
        <p>Enter lifestyle & social media habits to estimate a student's mental health score</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Sidebar — API config
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    api_url = st.text_input(
        "FastAPI endpoint",
        value="http://127.0.0.1:8000/predict",
        help="URL of your running FastAPI /predict endpoint",
    )
    st.markdown("---")
    st.caption(
        "Make sure your FastAPI server is running "
        "(`uvicorn main:app --reload`) before predicting."
    )
    st.markdown("---")
    st.markdown("**Built for:** Sheryians AI School")

TOP_COUNTRIES = ['Other', 'India', 'USA', 'Canada', 'Australia', 'UK',
                  'Germany', 'Mexico', 'Turkey', 'France']

# ----------------------------------------------------------------------
# Input form
# ----------------------------------------------------------------------
st.subheader("📋 Student Profile")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Age", min_value=10, max_value=100, value=21)
    gender = st.selectbox("Gender", ["Male", "Female"])
    country = st.selectbox(
        "Country",
        TOP_COUNTRIES + ["China", "Brazil", "Nigeria", "Other (type below)"],
        index=1,
    )
    if country == "Other (type below)":
        country = st.text_input("Type your country", value="Bangladesh")
    academic_level = st.selectbox(
        "Academic Level", ["Undergraduate", "Graduate", "High School"]
    )

with col2:
    most_used_platform = st.selectbox(
        "Most Used Platform",
        ['Facebook', 'LinkedIn', 'Instagram', 'Snapchat', 'Twitter',
         'YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte',
         'WhatsApp', 'WeChat'],
    )
    purpose_of_use = st.selectbox(
        "Purpose of Use", ["Networking", "Education", "Entertainment", "News"]
    )
    avg_daily_usage_hours = st.slider(
        "Avg Daily Social Media Usage (hrs)", 0.0, 24.0, 3.5, 0.1
    )
    daily_unlocks = st.number_input("Daily Phone Unlocks", min_value=0, value=60)

with col3:
    study_hours = st.slider("Study Hours / Day", 0.0, 24.0, 4.0, 0.1)
    physical_activity_hours = st.slider(
        "Physical Activity Hours / Day", 0.0, 24.0, 1.0, 0.1
    )
    sleep_hours_per_night = st.slider("Sleep Hours / Night", 0.0, 24.0, 7.0, 0.1)
    stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High", "Very High"])

st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🔮 Predict Mental Health Score")

# ----------------------------------------------------------------------
# Gauge chart helper
# ----------------------------------------------------------------------
def make_gauge(score: float) -> go.Figure:
    if score >= 7:
        color = "#22C55E"
        band = "Good"
    elif score >= 4:
        color = "#F59E0B"
        band = "Moderate"
    else:
        color = "#EF4444"
        band = "Needs Attention"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " / 10", "font": {"size": 40, "color": "white"}},
            title={"text": f"Predicted Score — {band}", "font": {"size": 18, "color": "white"}},
            gauge={
                "axis": {"range": [0, 10], "tickcolor": "white"},
                "bar": {"color": color, "thickness": 0.3},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 4], "color": "#3f1d1d"},
                    {"range": [4, 7], "color": "#3f321d"},
                    {"range": [7, 10], "color": "#1d3f24"},
                ],
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        height=320,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


TIPS = {
    "Good": [
        "Keep up your current sleep and study balance.",
        "Maintain regular physical activity — it's clearly working.",
    ],
    "Moderate": [
        "Consider trimming daily screen time by even 30–60 minutes.",
        "A consistent sleep schedule can meaningfully improve this score.",
    ],
    "Needs Attention": [
        "High stress combined with low sleep is a strong risk pattern — prioritize rest.",
        "Consider talking to a counselor or trusted mentor.",
        "Try reducing unlocks/notifications to lower compulsive phone checking.",
    ],
}

# ----------------------------------------------------------------------
# Predict
# ----------------------------------------------------------------------
if predict_btn:
    payload = {
        "age": age,
        "gender": gender,
        "country": country,
        "academic_level": academic_level,
        "most_used_platform": most_used_platform,
        "purpose_of_use": purpose_of_use,
        "avg_daily_usage_hours": avg_daily_usage_hours,
        "daily_unlocks": daily_unlocks,
        "study_hours": study_hours,
        "physical_activity_hours": physical_activity_hours,
        "sleep_hours_per_night": sleep_hours_per_night,
        "stress_level": stress_level,
    }

    with st.spinner("Contacting model API..."):
        try:
            resp = requests.post(api_url, json=payload, timeout=15)
            resp.raise_for_status()
            score = resp.json()["predicted_mental_health_score"]

            st.markdown("---")
            left, right = st.columns([1, 1.3])

            with left:
                st.plotly_chart(make_gauge(score), use_container_width=True)

            with right:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown("### 📊 Summary")

                band = "Good" if score >= 7 else "Moderate" if score >= 4 else "Needs Attention"
                c1, c2, c3 = st.columns(3)
                c1.markdown(
                    f'<div class="metric-pill"><h3>{score}</h3>Score</div>',
                    unsafe_allow_html=True,
                )
                c2.markdown(
                    f'<div class="metric-pill"><h3>{band}</h3>Status</div>',
                    unsafe_allow_html=True,
                )
                c3.markdown(
                    f'<div class="metric-pill"><h3>{sleep_hours_per_night}h</h3>Sleep</div>',
                    unsafe_allow_html=True,
                )

                st.markdown("#### 💡 Suggestions")
                for tip in TIPS[band]:
                    st.write(f"- {tip}")
                st.markdown("</div>", unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.error(
                "⚠️ Couldn't reach the FastAPI server. "
                "Make sure it's running and the URL in the sidebar is correct."
            )
        except requests.exceptions.HTTPError as e:
            st.error(f"⚠️ API returned an error: {e}\n\n{resp.text}")
        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")

st.markdown("---")
st.caption("This tool provides an estimate only and is not a substitute for professional mental health advice.")
