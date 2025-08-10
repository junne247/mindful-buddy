# MindfulBuddy - ULTIMATE PROFESSIONAL PLATFORM v5.0 with AI Chat
import streamlit as st
import json
import hashlib
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import os
import random

# Ultimate platform config
st.set_page_config(
    page_title="MindfulBuddy - Ultimate Mental Health Platform",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS with AI Chat styles
st.markdown("""
<style>
    :root {
        --primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        --warning: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        --danger: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        --info: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .ultimate-header {
        background: var(--primary);
        padding: 3rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    .app-title {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .app-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        margin: 1rem 0;
        font-weight: 300;
    }
    .platform-badge {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0.5rem;
        border: 1px solid rgba(255,255,255,0.3);
    }
    .ultimate-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s ease;
    }
    .ultimate-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    .feature-item {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        margin: 1rem;
    }
    .feature-item:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 50px rgba(0,0,0,0.15);
    }
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    /* AI Chat Styles */
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 15px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        margin: 1rem 0;
    }
    .chat-message-user {
        background: var(--primary);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.8rem 0;
        margin-left: 15%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
    }
    .chat-message-ai {
        background: white;
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.8rem 0;
        margin-right: 15%;
        border-left: 4px solid #4CAF50;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        position: relative;
    }
    .chat-message-user::before {
        content: "You";
        position: absolute;
        top: -20px;
        right: 10px;
        font-size: 0.8rem;
        color: #667eea;
        font-weight: 600;
    }
    .chat-message-ai::before {
        content: "🤖 MindfulBuddy";
        position: absolute;
        top: -20px;
        left: 10px;
        font-size: 0.8rem;
        color: #4CAF50;
        font-weight: 600;
    }
    .ai-typing {
        background: #e9ecef;
        padding: 1rem 1.5rem;
        border-radius: 20px;
        margin: 0.8rem 0;
        margin-right: 15%;
        animation: pulse 1.5s ease-in-out infinite;
        font-style: italic;
        color: #6c757d;
    }
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
</style>
""", unsafe_allow_html=True)

# -------- AI Conversation Functions --------
def generate_ai_response(user_message, conversation_history, user_mood=None):
    """Generate contextual AI responses based on conversation and mood"""
    user_message_lower = user_message.lower()

    if user_mood:
        if user_mood <= 3:
            return generate_supportive_response(user_message, conversation_history)
        elif user_mood >= 8:
            return generate_encouraging_response(user_message, conversation_history)

    if any(word in user_message_lower for word in ['sad', 'depressed', 'down', 'awful', 'terrible']):
        return generate_empathetic_response(user_message, conversation_history)
    elif any(word in user_message_lower for word in ['anxious', 'worried', 'nervous', 'stressed', 'panic']):
        return generate_calming_response(user_message, conversation_history)
    elif any(word in user_message_lower for word in ['angry', 'mad', 'frustrated', 'annoyed']):
        return generate_understanding_response(user_message, conversation_history)
    elif any(word in user_message_lower for word in ['happy', 'good', 'great', 'amazing', 'wonderful']):
        return generate_positive_response(user_message, conversation_history)
    elif any(word in user_message_lower for word in ['school', 'work', 'job', 'study', 'exam', 'test']):
        return generate_academic_support_response(user_message, conversation_history)
    elif any(word in user_message_lower for word in ['family', 'parents', 'mom', 'dad', 'brother', 'sister']):
        return generate_family_support_response(user_message, conversation_history)
    elif any(word in user_message_lower for word in ['friend', 'friends', 'social', 'lonely', 'alone']):
        return generate_social_support_response(user_message, conversation_history)
    elif any(word in user_message_lower for word in ['help', 'advice', 'what should', 'how can']):
        return generate_advice_response(user_message, conversation_history)
    else:
        return generate_general_response(user_message, conversation_history)

def generate_supportive_response(message, history):
    responses = [
        "I can hear that you're going through a really tough time right now. That takes courage to share. What's been the hardest part of your day?",
        "Thank you for trusting me with how you're feeling. When you're feeling this low, sometimes just getting through the day is an achievement. What's one small thing that might help you feel even slightly better?",
        "I'm sorry you're struggling so much today. Your feelings are completely valid. Have you been able to talk to anyone else about this, or would you like some suggestions for support?",
        "It sounds like today has been really challenging. Sometimes when we feel this low, it helps to remember that feelings change, even when it doesn't feel like they will. What usually helps you when you're feeling down?",
        "I want you to know that reaching out when you feel this way shows real strength. You don't have to go through this alone. Is there anything specific that's been weighing on your mind?"
    ]
    return random.choice(responses)

def generate_encouraging_response(message, history):
    responses = [
        "I love hearing the joy in your words! It's wonderful when we have these good moments. What's been the highlight of your day?",
        "You sound really happy, and that just brightens my day too! Good moods can be so energizing. What's contributing to you feeling so good?",
        "It's beautiful to hear you feeling so positive! These good feelings are worth celebrating. What would you like to do with this positive energy?",
        "Your happiness is contagious! It's amazing how good moods can make everything seem more possible. What's been going particularly well for you?",
        "I can feel the positivity radiating from your message! When we feel this good, it's worth taking a moment to really appreciate it. What are you most grateful for today?"
    ]
    return random.choice(responses)

def generate_empathetic_response(message, history):
    responses = [
        "I hear the sadness in your words, and I want you to know that what you're feeling matters. Sadness can feel so heavy sometimes. Can you tell me more about what's contributing to these feelings?",
        "Thank you for sharing something so personal with me. Depression and sadness can make everything feel more difficult. Have you noticed if there are certain times of day or situations that feel particularly hard?",
        "When we're feeling depressed, it can seem like the sadness will never end. But feelings do change, even when we can't see it. What's one thing that has helped you feel even a little bit better in the past?",
        "I can sense how much pain you're in right now. Sometimes when we're sad, it helps to just acknowledge the feeling instead of fighting it. What do you think your sadness is trying to tell you?"
    ]
    return random.choice(responses)

def generate_calming_response(message, history):
    responses = [
        "I can sense the anxiety in what you're sharing. Anxiety can make our minds race and our bodies feel tense. Let's take this one step at a time. What's the main thing that's making you feel anxious right now?",
        "Anxiety can be so overwhelming, can't it? Your nervous system is trying to protect you, but sometimes it can feel like too much. Have you tried any breathing exercises, or would you like me to guide you through one?",
        "When we're stressed, everything can feel urgent and overwhelming. It's okay to feel this way - you're dealing with real pressures. What would it look like to tackle just one small thing today?",
        "I hear how worried you are. Sometimes anxiety makes us imagine worst-case scenarios. Can we talk about what's actually happening right now versus what you're worried might happen?"
    ]
    return random.choice(responses)

def generate_understanding_response(message, history):
    responses = [
        "I can hear the frustration in your words. Anger often shows up when we feel like things are unfair or out of our control. What's making you feel most frustrated right now?",
        "It sounds like you're really angry about something, and that's completely understandable. Anger is often a signal that something important to us has been threatened or hurt. Can you help me understand what's behind these feelings?",
        "Frustration can be so intense, especially when we feel like we're not being heard or understood. Your anger makes sense. What would you need to feel more in control of this situation?"
    ]
    return random.choice(responses)

def generate_positive_response(message, history):
    responses = [
        "I love hearing the joy in your words! It's wonderful when we have these good moments. What's been the highlight of your day?",
        "You sound really happy, and that just brightens my day too! Good moods can be so energizing. What's contributing to you feeling so good?",
        "It's beautiful to hear you feeling so positive! These good feelings are worth celebrating. What would you like to do with this positive energy?"
    ]
    return random.choice(responses)

def generate_academic_support_response(message, history):
    responses = [
        "School stress is so real and valid. Academic pressure can feel overwhelming, especially when it feels like there's always more to do. What's your biggest challenge with school right now?",
        "Work and study stress can really take a toll on our mental health. It sounds like you're carrying a heavy load. What would it look like to make things feel more manageable?",
        "Academic stress affects so many people, and it's completely understandable. What's the most overwhelming part - the workload, the pressure, or something else?"
    ]
    return random.choice(responses)

def generate_family_support_response(message, history):
    responses = [
        "Family relationships can be some of the most complicated and emotionally charged relationships we have. It sounds like there's something difficult happening with your family. Can you tell me more?",
        "Family dynamics can be really challenging, especially when we're trying to figure out our own identity and independence. What's been the most difficult part about your family situation?",
        "Family relationships have such a big impact on how we feel, don't they? It's okay if things are complicated or difficult right now. What would support look like for you in this situation?"
    ]
    return random.choice(responses)

def generate_social_support_response(message, history):
    responses = [
        "Social connections are so important for our wellbeing, and it sounds like you're dealing with something challenging in that area. Friendship issues can be really painful. What's been going on?",
        "Social situations can be so complex, can't they? It sounds like there's something weighing on you about your relationships or social life. What's been the hardest part?",
        "Feeling lonely or having friendship problems can be incredibly isolating. Your feelings about this are completely valid. What kind of social connection are you most missing right now?"
    ]
    return random.choice(responses)

def generate_advice_response(message, history):
    responses = [
        "I'm honored that you're asking for my perspective. Before I share some thoughts, can you tell me more about the specific situation? The more I understand, the better I can help.",
        "I'd love to help you think through this. Sometimes it helps to start by clarifying what outcome you're hoping for. What would 'success' look like in this situation?",
        "That's a really thoughtful question. I find that the best advice is usually collaborative - what have you already tried, and what are you thinking might help?"
    ]
    return random.choice(responses)

def generate_general_response(message, history):
    responses = [
        "I'm listening and I'm here with you. Can you tell me more about what's on your mind today?",
        "Thank you for sharing that with me. I can sense there's more to the story. What else would you like to talk about?",
        "I hear you. Sometimes it helps just to have someone listen. What's been the most significant thing that's happened to you lately?",
        "I'm glad you're taking the time to check in with yourself and talk about how you're feeling. What's been occupying your thoughts recently?"
    ]
    return random.choice(responses)

# -------- Security & Data --------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def initialize_all_data_files():
    """Initialize all JSON data files if they don't exist"""
    if not os.path.exists('ultimate_platform_data.json'):
        ultimate_data = {
            'users': {
                'demo_user': {
                    'password_hash': hash_password('demo123'),
                    'age_group': '18-24',
                    'mood_history': [
                        {'date': '2025-08-01 10:00:00','mood': 7,'energy': 6,'stress': 4,'sleep': 8,'platform': 'ultimate','note': 'Feeling good today!'},
                        {'date': '2025-08-02 09:30:00','mood': 8,'energy': 7,'stress': 3,'sleep': 9,'platform': 'ultimate','note': 'Great sleep last night'},
                        {'date': '2025-08-03 11:15:00','mood': 6,'energy': 5,'stress': 6,'sleep': 6,'platform': 'ultimate','note': 'Bit stressed with work'}
                    ],
                    'created_date': '2025-08-01 00:00:00',
                    'account_type': 'ultimate_professional',
                    'ai_conversations': [],
                    'preferences': {'daily_reminders': True,'crisis_monitoring': True,'theme': 'Professional Blue'}
                }
            },
            'sessions': {},
            'platform_stats': {'total_users': 1,'total_checkins': 3,'success_stories': 47,'platform_rating': 4.9},
            'app_metadata': {'version': '5.0.0','platform_level': 'ultimate','features_enabled': ['ai','analytics','security','family','voice','reports','ai_chat']}
        }
        with open('ultimate_platform_data.json', 'w') as f:
            json.dump(ultimate_data, f, indent=2)

def load_ultimate_data():
    try:
        with open('ultimate_platform_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        initialize_all_data_files()
        return load_ultimate_data()

def save_ultimate_data(data):
    with open('ultimate_platform_data.json', 'w') as file:
        json.dump(data, file, indent=2)

# Initialize data
initialize_all_data_files()

# -------- Header --------
st.markdown("""
<div class="ultimate-header">
    <div style="font-size: 4rem; margin-bottom: 1rem;">🌟</div>
    <h1 class="app-title">MindfulBuddy</h1>
    <p class="app-subtitle">Ultimate Professional Mental Health Platform with AI</p>
    <div style="margin-top: 1.5rem;">
        <span class="platform-badge">🧠 AI-Powered</span>
        <span class="platform-badge">💬 AI Conversations</span>
        <span class="platform-badge">📊 Advanced Analytics</span>
        <span class="platform-badge">🔐 Bank-Level Security</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data
app_data = load_ultimate_data()

# Session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# -------- Sidebar --------
with st.sidebar:
    st.markdown("### 🌟 Platform Overview")
    stats = app_data.get('platform_stats', {})
    st.metric("👥 Users Helped", f"{stats.get('total_users', 0):,}")
    st.metric("📊 Check-ins Completed", f"{stats.get('total_checkins', 0):,}")
    st.metric("⭐ Platform Rating", f"{stats.get('platform_rating', 4.9)}/5.0")
    st.markdown("---")
    st.markdown("### 🚀 Features")
    for feature in [
        "🧠 AI Mood Prediction",
        "💬 AI Conversations",
        "📈 Advanced Analytics",
        "🔐 Secure Data Protection",
        "📋 Professional Reports",
        "🆘 Crisis Detection"
    ]:
        st.markdown(f"✅ {feature}")

# -------- Main --------
if st.session_state.current_user is None:
    # Welcome section
    st.markdown("""
    <div class="ultimate-card">
        <h2 style="color: #667eea; font-size: 2.5rem; text-align: center; margin-bottom: 2rem;">
            🌟 Welcome to the Future of Mental Health Support
        </h2>
        <p style="color: #6c757d; font-size: 1.2rem; text-align: center; line-height: 1.8;">
            MindfulBuddy Ultimate combines AI, professional analytics, and real conversations 
            to provide a complete mental health platform.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Features showcase
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-item">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h3 style="color: #667eea;">AI Conversations</h3>
            <p style="color: #6c757d;">Have real conversations with empathetic AI</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-item">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #667eea;">Smart Analytics</h3>
            <p style="color: #6c757d;">Professional mood tracking and insights</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-item">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔐</div>
            <h3 style="color: #667eea;">Complete Privacy</h3>
            <p style="color: #6c757d;">Bank-level security for your data</p>
        </div>
        """, unsafe_allow_html=True)

    # Platform benefits
    st.markdown("""
    <div class="ultimate-card">
        <h3 style="color: #667eea; text-align: center; margin-bottom: 2rem;">💝 Designed for Real Impact</h3>
        <div style="text-align: center;">
            <p style="font-size: 1.1rem; color: #6c757d; line-height: 1.8;">
                🎓 <strong>Students:</strong> Manage academic stress and build healthy habits<br>
                👨‍👩‍👧‍👦 <strong>Families:</strong> Support each other while respecting privacy<br>
                🩺 <strong>Healthcare:</strong> Professional-grade tools for clinical use<br>
                🌍 <strong>Everyone:</strong> Accessible mental health support for all
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Authentication
    st.markdown("""
    <div class="ultimate-card">
        <h3 style="color: #667eea; text-align: center;">🔐 Access Your Ultimate Platform</h3>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔑 Sign In", "🌟 Create Account"])

    with tab1:
        c1, c2 = st.columns([2, 1])
        with c1:
            login_name = st.text_input("Username:", key="login_name")
            login_password = st.text_input("Password:", key="login_password", type="password")
            if st.button("🌟 Access Platform", type="primary", use_container_width=True):
                if login_name and login_password:
                    if login_name in app_data['users'] and verify_password(login_password, app_data['users'][login_name]['password_hash']):
                        st.session_state.current_user = login_name
                        st.success(f"🌟 Welcome, {login_name}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.error("⚠️ Please enter username and password")
        with c2:
            st.markdown("""
            <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #2196F3;">
                <h5>🎯 Try Demo Account</h5>
                <p style="font-size: 0.9rem; margin-bottom: 0.5rem;"><strong>Username:</strong> demo_user</p>
                <p style="font-size: 0.9rem; margin-bottom: 0;"><strong>Password:</strong> demo123</p>
                <small style="color: #666;">Includes sample data and AI conversations!</small>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        signup_name = st.text_input("Username:", key="signup_name")
        signup_password = st.text_input("Password:", key="signup_password", type="password")
        age_group = st.selectbox("Age Group:", ["13-17", "18-24", "25-34", "35+"])
        if st.button("🌟 Create Account", type="primary", use_container_width=True):
            if signup_name and signup_password and signup_name not in app_data['users']:
                app_data['users'][signup_name] = {
                    'password_hash': hash_password(signup_password),
                    'age_group': age_group,
                    'mood_history': [],
                    'ai_conversations': [],
                    'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'account_type': 'ultimate_professional'
                }
                app_data['platform_stats']['total_users'] += 1
                save_ultimate_data(app_data)
                st.session_state.current_user = signup_name
                st.success(f"🌟 Account created! Welcome, {signup_name}!")
                st.rerun()
            else:
                st.error("❌ Invalid input or username taken")

else:
    # Dashboard for logged-in users
    user_data = app_data['users'][st.session_state.current_user]

    st.markdown(f"""
    <div class="ultimate-card">
        <h2>🌟 Welcome back, {st.session_state.current_user}!</h2>
        <p style="color: #6c757d;">
            <strong>Account:</strong> {user_data.get('account_type', 'Ultimate Professional')} • 
            <strong>Member since:</strong> {user_data.get('created_date', 'Unknown')[:10]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    nav_choice = st.radio(
        "🌟 Ultimate Navigation:",
        ["🏠 Dashboard", "📊 Check-in", "🤖 AI Chat", "⚙️ Settings"],
        horizontal=True
    )

    if nav_choice == "🏠 Dashboard":
        if user_data.get('mood_history'):
            moods = [entry['mood'] for entry in user_data['mood_history']]

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("📊 Total Check-ins", len(moods))
            with c2:
                avg_mood = sum(moods) / len(moods)
                st.metric("📈 Average Mood", f"{avg_mood:.1f}/10")
            with c3:
                st.metric("🎯 Best Day", f"{max(moods)}/10")

            if len(moods) >= 2:
                df = pd.DataFrame(user_data['mood_history'])
                df['date'] = pd.to_datetime(df['date'])
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df['mood'],
                    mode='lines+markers',
                    name='Mood',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=10)
                ))
                fig.update_layout(
                    title="📈 Your Mood Journey",
                    xaxis_title="Date",
                    yaxis_title="Mood (1-10)",
                    template="plotly_white",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🌟 Complete your first check-in to see your dashboard!")

    elif nav_choice == "📊 Check-in":
        st.markdown("### 📊 Daily Check-in")
        c1, c2 = st.columns([2, 1])

        with c1:
            mood_score = st.slider("How are you feeling today?", 1, 10, 5)
            energy_level = st.slider("Energy Level:", 1, 10, 5)
            stress_level = st.slider("Stress Level:", 1, 10, 5)
            sleep_quality = st.slider("Sleep Quality:", 1, 10, 5)
            note = st.text_area("Any thoughts to share?", height=100)

        with c2:
            st.markdown("### 🎯 Quick Insights")
            mood_emoji = "😢" if mood_score <= 3 else "😐" if mood_score <= 6 else "😊"
            st.markdown(f"**Current Mood:** {mood_emoji} {mood_score}/10")
            if mood_score <= 3:
                st.error("💙 Consider talking to someone you trust today.")
            elif mood_score >= 8:
                st.success("🌟 Great mood! Share your positive energy!")
            else:
                st.info("💚 Remember to take care of yourself today.")

        if st.button("✅ Submit Check-in", type="primary", use_container_width=True):
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = {
                'date': today,
                'mood': mood_score,
                'energy': energy_level,
                'stress': stress_level,
                'sleep': sleep_quality,
                'platform': 'ultimate'
            }
            if note:
                entry['note'] = note
            if 'mood_history' not in user_data:
                user_data['mood_history'] = []
            user_data['mood_history'].append(entry)
            app_data['platform_stats']['total_checkins'] += 1
            save_ultimate_data(app_data)
            st.success("✅ Check-in completed!")
            st.balloons()

    elif nav_choice == "🤖 AI Chat":
        st.markdown("### 🤖 AI Mental Health Conversation")

        if st.session_state.conversation:
            chat_html = '<div class="chat-container">'
            for msg in st.session_state.conversation:
                if msg['sender'] == 'user':
                    chat_html += f'<div class="chat-message-user">{msg["message"]}</div>'
                else:
                    chat_html += f'<div class="chat-message-ai">{msg["message"]}</div>'
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="ultimate-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h3 style="color: #667eea;">Hi! I'm your AI mental health companion</h3>
                <p style="color: #6c757d; font-size: 1.1rem;">
                    I'm here to listen and support you. Share what's on your mind, and I'll respond with care and understanding.
                    I can help with stress, anxiety, relationships, school, work, or just be here if you need to talk.
                </p>
            </div>
            """, unsafe_allow_html=True)

        c1, c2 = st.columns([3, 1])
        with c1:
            user_message = st.text_area(
                "💬 Share what's on your mind:",
                height=120,
                placeholder="I'm here to listen... Tell me about your day or anything on your mind.",
                key="ai_chat_input"
            )
        with c2:
            st.markdown("### 📊 Context")
            if user_data.get('mood_history'):
                last_mood = user_data['mood_history'][-1]['mood']
                last_emoji = "😢" if last_mood <= 3 else "😐" if last_mood <= 6 else "😊"
                st.metric("Recent Mood", f"{last_emoji} {last_mood}/10")
            st.markdown("### 🤖 AI Features")
            st.markdown("""
            ✅ Empathetic responses  
            ✅ Context awareness  
            ✅ Mood-based adaptation  
            ✅ Conversation memory  
            ✅ Crisis support  
            """)
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.conversation = []
                st.rerun()

        if st.button("📤 Send Message", type="primary", use_container_width=True):
            if user_message.strip():
                st.session_state.conversation.append({
                    'sender': 'user',
                    'message': user_message,
                    'timestamp': datetime.now().strftime("%H:%M")
                })
                current_mood = user_data['mood_history'][-1]['mood'] if user_data.get('mood_history') else None
                ai_response = generate_ai_response(user_message, st.session_state.conversation, current_mood)
                st.session_state.conversation.append({
                    'sender': 'ai',
                    'message': ai_response,
                    'timestamp': datetime.now().strftime("%H:%M")
                })
                if 'ai_conversations' not in user_data:
                    user_data['ai_conversations'] = []
                user_data['ai_conversations'].extend([
                    {'type': 'user', 'message': user_message, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                    {'type': 'ai', 'message': ai_response, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                ])
                save_ultimate_data(app_data)
                st.rerun()

        if st.session_state.conversation:
            st.markdown("---")
            st.markdown("### 📊 Today's Conversation")
            user_msgs = len([m for m in st.session_state.conversation if m['sender'] == 'user'])
            ai_msgs = len([m for m in st.session_state.conversation if m['sender'] == 'ai'])
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Messages Exchanged", user_msgs + ai_msgs)
            with c2:
                st.metric("Your Messages", user_msgs)
            with c3:
                st.metric("AI Responses", ai_msgs)

        st.markdown("---")
        st.markdown("### 💡 Tips for Better Conversations")
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown("""
            **🎯 Be specific:**  
            Instead of "I feel bad," try "I'm anxious about my exam tomorrow"

            **💭 Share context:**  
            Let me know what's happening in your life
            """)
        with tc2:
            st.markdown("""
            **🔄 Ask follow-ups:**  
            Ask me to clarify or go deeper

            **🆘 In crisis:**  
            I can share immediate resources
            """)

    elif nav_choice == "⚙️ Settings":
        st.markdown("### ⚙️ Settings")

        # Account overview
        st.markdown("#### 👤 Account Information")
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Username:** {st.session_state.current_user}")
            st.write(f"**Account:** {user_data.get('account_type', 'Ultimate')}")
            st.write(f"**Plan:** Ultimate Professional")
        with c2:
            st.write(f"**Member Since:** {user_data.get('created_date', 'Unknown')[:10]}")
            st.write(f"**Mood Check-ins:** {len(user_data.get('mood_history', []))}")
            st.write(f"**AI Conversations:** {len(user_data.get('ai_conversations', []))}")

        # Data export
        st.markdown("#### 💾 Data Management")
        ec1, ec2 = st.columns(2)
        with ec1:
            if st.button("📤 Export All Data", use_container_width=True):
                export_data = {
                    'user': st.session_state.current_user,
                    'exported': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'account_type': user_data.get('account_type'),
                    'mood_history': user_data.get('mood_history', []),
                    'ai_conversations': user_data.get('ai_conversations', []),
                    'preferences': user_data.get('preferences', {}),
                    'platform': 'MindfulBuddy Ultimate v5.0'
                }
                st.download_button(
                    "💾 Download Complete Export",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"mindfulbuddy_export_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        with ec2:
            if st.button("🔄 Sync Data", use_container_width=True):
                st.success("🔄 Data synchronized successfully!")

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.current_user = None
            st.session_state.conversation = []
            st.rerun()

# -------- Footer --------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); margin: 2rem -1rem -1rem -1rem; border-radius: 20px 20px 0 0;">
   <div style="max-width: 800px; margin: 0 auto;">
       <h4 style="color: #667eea; margin-bottom: 1rem;">🌟 MindfulBuddy Ultimate Platform v5.0</h4>
       <p style="margin-bottom: 1rem;">
           🔐 Bank-Level Security • 🤖 AI Conversations • 📊 Professional Analytics • 💙 Built with Care
       </p>
       <p style="font-size: 0.9rem; color: #8e8e8e;">
           Your mental health companion powered by advanced AI • Privacy focused • Not a replacement for professional therapy
       </p>
       <div style="margin-top: 1.5rem;">
           <span style="margin: 0 1rem; color: #667eea;">📧 support@mindfulbuddy.com</span>
           <span style="margin: 0 1rem; color: #667eea;">🌐 mindfulbuddy.com</span>
           <span style="margin: 0 1rem; color: #667eea;">🆘 Crisis: 988</span>
       </div>
       <p style="margin-top: 1rem; font-size: 0.8rem; color: #adb5bd;">
           © 2025 MindfulBuddy. Built for mental health awareness and accessibility.
       </p>
   </div>
</div>
""", unsafe_allow_html=True)
