# Mental Health Bot - AI PREDICTION VERSION!
import streamlit as st
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

# Set page config
st.set_page_config(
    page_title="AI Mental Health Buddy 🧠",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #ffa726 0%, #ff7043 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #26c6da 0%, #00acc1 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_user_data():
    try:
        with open('ai_user_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open('ai_user_data.json', 'w') as file:
        json.dump(data, file, indent=2)

def predict_future_mood(mood_history):
    """AI mood prediction using machine learning"""
    if len(mood_history) < 5:
        return None, "Need more data for predictions"
    
    # Prepare data
    dates = [datetime.strptime(entry['date'].split()[0], '%Y-%m-%d') for entry in mood_history]
    moods = [entry['mood'] for entry in mood_history]
    
    # Convert dates to numbers for ML
    start_date = dates[0]
    X = np.array([(date - start_date).days for date in dates]).reshape(-1, 1)
    y = np.array(moods)
    
    # Train simple AI model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 7 days
    last_day = (dates[-1] - start_date).days
    future_days = np.array([last_day + i for i in range(1, 8)]).reshape(-1, 1)
    predictions = model.predict(future_days)
    
    # Ensure predictions are in valid range
    predictions = np.clip(predictions, 1, 10)
    
    return predictions, "AI predictions ready!"

def analyze_patterns_ai(mood_history):
    """Advanced AI pattern analysis"""
    if len(mood_history) < 7:
        return ["Need more check-ins for AI analysis"]
    
    moods = [entry['mood'] for entry in mood_history]
    dates = [datetime.strptime(entry['date'].split()[0], '%Y-%m-%d') for entry in mood_history]
    
    insights = []
    
    # Day of week analysis
    day_moods = {}
    for mood, date in zip(moods, dates):
        day = date.strftime('%A')
        if day not in day_moods:
            day_moods[day] = []
        day_moods[day].append(mood)
    
    if day_moods:
        avg_by_day = {day: sum(moods)/len(moods) for day, moods in day_moods.items() if len(moods) >= 2}
        if avg_by_day:
            best_day = max(avg_by_day, key=avg_by_day.get)
            worst_day = min(avg_by_day, key=avg_by_day.get)
            insights.append(f"🤖 AI detected: You're happiest on {best_day}s ({avg_by_day[best_day]:.1f}/10)")
            if avg_by_day[worst_day] < avg_by_day[best_day] - 1:
                insights.append(f"⚠️ AI noticed: {worst_day}s tend to be harder ({avg_by_day[worst_day]:.1f}/10)")
    
    # Trend analysis
    if len(moods) >= 10:
        recent_trend = np.mean(moods[-5:]) - np.mean(moods[-10:-5])
        if recent_trend > 0.5:
            insights.append("📈 AI trend: Your mood has been improving lately!")
        elif recent_trend < -0.5:
            insights.append("📉 AI trend: You've had some challenging days recently")
    
    # Volatility analysis
    mood_std = np.std(moods)
    if mood_std > 2.5:
        insights.append("🎢 AI insight: Your mood varies quite a bit - that's normal!")
    elif mood_std < 1:
        insights.append("📊 AI insight: Your mood is very stable - great consistency!")
    
    # Streak detection
    current_streak = 1
    streak_type = "good" if moods[-1] >= 6 else "challenging"
    for i in range(len(moods)-2, -1, -1):
        if (moods[i] >= 6) == (streak_type == "good"):
            current_streak += 1
        else:
            break
    
    if current_streak >= 3:
        if streak_type == "good":
            insights.append(f"🔥 AI detected: {current_streak}-day good mood streak!")
        else:
            insights.append(f"💙 AI noticed: {current_streak} challenging days - this will pass")
    
    return insights

def create_prediction_chart(mood_history, predictions):
    """Create chart with predictions"""
    if predictions is None:
        return None
    
    # Historical data
    hist_dates = [entry['date'].split()[0] for entry in mood_history]
    hist_moods = [entry['mood'] for entry in mood_history]
    
    # Future dates
    last_date = datetime.strptime(hist_dates[-1], '%Y-%m-%d')
    future_dates = [(last_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 8)]
    
    fig = go.Figure()
    
    # Historical line
    fig.add_trace(go.Scatter(
        x=hist_dates,
        y=hist_moods,
        mode='lines+markers',
        name='Your Actual Mood',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=10)
    ))
    
    # Prediction line
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=predictions,
        mode='lines+markers',
        name='AI Prediction',
        line=dict(color='#FF9800', width=3, dash='dash'),
        marker=dict(size=10, symbol='diamond')
    ))
    
    fig.update_layout(
        title="🤖 AI Mood Prediction - Next 7 Days",
        xaxis_title="Date",
        yaxis_title="Mood (1-10)",
        yaxis=dict(range=[0, 11]),
        template="plotly_white",
        height=500
    )
    
    return fig

# Main app
st.markdown('<h1 class="main-header">🤖 AI Mental Health Buddy</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Powered by Artificial Intelligence for smarter mental health insights</p>', unsafe_allow_html=True)

# Load data
user_data = load_user_data()

# Sidebar
with st.sidebar:
    st.header("🤖 AI Dashboard")
    
    if 'name' not in user_data:
        name = st.text_input("What's your name?", key="name_input")
        if name:
            user_data['name'] = name
            user_data['mood_history'] = []
            save_user_data(user_data)
            st.success(f"Nice to meet you, {name}! 🤖")
            st.rerun()
    else:
        st.success(f"Welcome back, {user_data['name']}! 🤖")
        
        if user_data.get('mood_history'):
            st.write(f"📊 Total check-ins: {len(user_data['mood_history'])}")
            
            # AI readiness indicator
            data_count = len(user_data['mood_history'])
            if data_count >= 10:
                st.success("🤖 AI: Fully operational!")
            elif data_count >= 5:
                st.warning("🤖 AI: Learning your patterns...")
            else:
                st.info("🤖 AI: Gathering data...")

# Main content
if 'name' in user_data:
    
    # AI Predictions Section
    if len(user_data.get('mood_history', [])) >= 5:
        st.header("🔮 AI Mood Predictions")
        
        predictions, status = predict_future_mood(user_data['mood_history'])
        
        if predictions is not None:
            # Show prediction chart
            fig = create_prediction_chart(user_data['mood_history'], predictions)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Prediction insights
            avg_prediction = np.mean(predictions)
            if avg_prediction >= 7:
                st.markdown(f"""
                <div class="prediction-box">
                    <h3>🌟 Great News!</h3>
                    <p>AI predicts you'll have a good week ahead! Average predicted mood: {avg_prediction:.1f}/10</p>
                </div>
                """, unsafe_allow_html=True)
            elif avg_prediction <= 4:
                st.markdown(f"""
                <div class="warning-box">
                    <h3>💙 Heads Up</h3>
                    <p>AI suggests some challenging days ahead. Predicted average: {avg_prediction:.1f}/10</p>
                    <p>Consider planning some self-care activities!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="insight-box">
                    <h3>📊 Balanced Week</h3>
                    <p>AI predicts a mixed week ahead. Average: {avg_prediction:.1f}/10</p>
                </div>
                """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Daily check-in
        st.header("🌟 Today's Check-in")
        
        mood_score = st.slider(
            "How are you feeling right now?",
            min_value=1,
            max_value=10,
            value=5,
            help="1=Really struggling, 10=Amazing"
        )
        
        # Optional note
        note = st.text_area("Any thoughts about today? (optional)", height=100)
        
        if st.button("🤖 Submit to AI", type="primary"):
            today = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Add to history
            if 'mood_history' not in user_data:
                user_data['mood_history'] = []
            
            entry = {'date': today, 'mood': mood_score}
            if note:
                entry['note'] = note
            
            user_data['mood_history'].append(entry)
            save_user_data(user_data)
            
            st.success("✅ Data submitted to AI for analysis!")
            st.rerun()
    
    with col2:
        # AI Insights
        if user_data.get('mood_history'):
            st.header("🧠 AI Insights")
            
            insights = analyze_patterns_ai(user_data['mood_history'])
            
            for insight in insights:
                st.write(f"• {insight}")
            
            # Quick stats
            moods = [entry['mood'] for entry in user_data['mood_history']]
            st.metric("AI Confidence", f"{min(len(moods) * 10, 100)}%")
            st.metric("Pattern Strength", f"{min(len(moods) * 15, 100)}%")

else:
    st.info("👈 Enter your name to activate AI features!")

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">🤖 Powered by AI • Built for Mental Health • You Matter! 💙</p>',
    unsafe_allow_html=True
)
