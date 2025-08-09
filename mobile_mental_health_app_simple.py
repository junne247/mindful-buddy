# Mental Health Bot - MOBILE APP VERSION (No QR dependency)!
import streamlit as st
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import base64
from io import BytesIO

# Mobile-optimized page config
st.set_page_config(
    page_title="Mental Health Buddy 📱",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Mobile-first CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
    }
    
    .mobile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 20px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .quick-action {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .mood-emoji {
        font-size: 3rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .notification-box {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    
    .app-install {
        background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 2rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def load_mobile_data():
    try:
        with open('mobile_app_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            'users': {},
            'app_settings': {
                'notifications_enabled': True,
                'daily_reminder_time': '20:00',
                'app_version': '1.0.0'
            }
        }

def save_mobile_data(data):
    with open('mobile_app_data.json', 'w') as file:
        json.dump(data, file, indent=2)

def get_mood_emoji(mood_score):
    if mood_score <= 2:
        return "😢"
    elif mood_score <= 4:
        return "😕"
    elif mood_score <= 6:
        return "😐"
    elif mood_score <= 8:
        return "🙂"
    else:
        return "😄"

def create_mobile_mood_chart(mood_history):
    if len(mood_history) < 2:
        return None
    
    recent_data = mood_history[-30:]
    dates = [entry['date'].split()[0] for entry in recent_data]
    moods = [entry['mood'] for entry in recent_data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=moods,
        mode='lines+markers',
        fill='tonexty',
        name='Your Mood',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=8),
        fillcolor='rgba(76, 175, 80, 0.2)'
    ))
    
    fig.update_layout(
        title="📱 Your Mood Journey",
        xaxis_title="",
        yaxis_title="Mood",
        yaxis=dict(range=[0, 11]),
        template="plotly_white",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def export_user_data(user_data):
    export_data = {
        'name': user_data.get('name', ''),
        'mood_history': user_data.get('mood_history', []),
        'export_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'total_checkins': len(user_data.get('mood_history', [])),
        'app_version': '1.0.0'
    }
    
    return json.dumps(export_data, indent=2)

# Load data
app_data = load_mobile_data()

# Mobile header
st.markdown('<h1 class="main-header">📱 Mental Health Buddy</h1>', unsafe_allow_html=True)

# Initialize session state
if 'nav_override' not in st.session_state:
    st.session_state.nav_override = None

# Quick stats bar
if 'current_user' in st.session_state:
    user_data = app_data['users'].get(st.session_state.current_user, {})
    if user_data.get('mood_history'):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Check-ins", len(user_data['mood_history']))
        with col2:
            recent_moods = [entry['mood'] for entry in user_data['mood_history'][-7:]]
            avg_mood = sum(recent_moods) / len(recent_moods) if recent_moods else 0
            st.metric("Week Avg", f"{avg_mood:.1f}")
        with col3:
            streak = 0
            if user_data['mood_history'] and user_data['mood_history'][-1]['mood'] >= 6:
                streak = 1
                for i in range(len(user_data['mood_history'])-2, -1, -1):
                    if user_data['mood_history'][i]['mood'] >= 6:
                        streak += 1
                    else:
                        break
            st.metric("Streak", f"{streak} days")

# Main mobile interface
if 'current_user' not in st.session_state:
    # User login/registration
    st.markdown("""
    <div class="mobile-card">
        <h2>👋 Welcome to Your Mental Health Companion</h2>
        <p>Track your mood, get insights, and improve your mental wellbeing - all from your phone!</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "➕ Sign Up"])
    
    with tab1:
        login_name = st.text_input("Your name:", key="login_name")
        if st.button("📱 Login", type="primary", use_container_width=True):
            if login_name and login_name in app_data['users']:
                st.session_state.current_user = login_name
                st.success(f"Welcome back, {login_name}! 📱")
                st.rerun()
            else:
                st.error("User not found! Please sign up first.")
    
    with tab2:
        signup_name = st.text_input("Choose your name:", key="signup_name")
        age_group = st.selectbox("Age group:", ["13-17", "18-24", "25-34", "35+"])
        
        if st.button("🚀 Create Account", type="primary", use_container_width=True):
            if signup_name and signup_name not in app_data['users']:
                app_data['users'][signup_name] = {
                    'age_group': age_group,
                    'mood_history': [],
                    'created_date': datetime.now().strftime("%Y-%m-%d"),
                    'notifications_enabled': True
                }
                save_mobile_data(app_data)
                st.session_state.current_user = signup_name
                st.success(f"Account created! Welcome, {signup_name}! 🎉")
                st.rerun()
            else:
                st.error("Name already taken or empty!")

else:
    # Main app for logged-in users
    user_data = app_data['users'][st.session_state.current_user]
    
    # Mobile navigation
    nav_choice = st.radio(
        "📱 Navigation:",
        ["🏠 Home", "📊 Check-in", "📈 Insights", "⚙️ Settings"],
        horizontal=True
    )
    
    if nav_choice == "🏠 Home":
        st.markdown(f"""
        <div class="mobile-card">
            <h2>Hi {st.session_state.current_user}! 👋</h2>
            <p>Ready for your daily mental health check-in?</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick mood check
        if user_data.get('mood_history'):
            last_entry = user_data['mood_history'][-1]
            last_mood = last_entry['mood']
            last_date = last_entry['date'].split()[0]
            
            st.markdown(f"""
            <div class="mood-emoji">
                {get_mood_emoji(last_mood)}
            </div>
            <p style="text-align: center;">Last check-in: {last_date} - Mood: {last_mood}/10</p>
            """, unsafe_allow_html=True)
        
        # Quick actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Quick Check-in", use_container_width=True):
                st.session_state.nav_override = "📊 Check-in"
                st.rerun()
        with col2:
            if st.button("📈 View Insights", use_container_width=True):
                st.session_state.nav_override = "📈 Insights"
                st.rerun()
        
        # Daily motivation
        motivations = [
            "🌟 You're stronger than you think!",
            "💪 Every day is a fresh start!",
            "🌈 Your mental health matters!",
            "❤️ You deserve happiness and peace!",
            "🚀 Small steps lead to big changes!"
        ]
        daily_motivation = motivations[datetime.now().day % len(motivations)]
        
        st.markdown(f"""
        <div class="notification-box">
            <h4>💝 Daily Motivation</h4>
            <p>{daily_motivation}</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif nav_choice == "📊 Check-in" or st.session_state.get('nav_override') == "📊 Check-in":
        st.session_state.nav_override = None
        
        st.header("📊 Daily Check-in")
        
        # Mood slider with emojis
        mood_score = st.slider(
            "How are you feeling right now?",
            min_value=1,
            max_value=10,
            value=5,
            help="Slide to match your current mood"
        )
        
        # Show emoji for current selection
        st.markdown(f"""
        <div class="mood-emoji">
            {get_mood_emoji(mood_score)}
        </div>
        """, unsafe_allow_html=True)
        
        # Optional note
        note = st.text_area("What's on your mind? (optional)", height=80, placeholder="Share your thoughts...")
        
        # Submit button
        if st.button("✅ Submit Check-in", type="primary", use_container_width=True):
            today = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            entry = {
                'date': today,
                'mood': mood_score,
                'platform': 'mobile'
            }
            if note:
                entry['note'] = note
            
            app_data['users'][st.session_state.current_user]['mood_history'].append(entry)
            save_mobile_data(app_data)
            
            # Response
            if mood_score <= 3:
                st.error(f"💙 I'm sorry you're struggling today. Remember, these feelings are temporary and you're not alone.")
            elif mood_score >= 8:
                st.success(f"🎉 Amazing! I love seeing you happy. Keep up whatever you're doing!")
            else:
                st.info(f"💚 Thanks for checking in! Every feeling is valid and important.")
            
            st.balloons()
            st.success("📱 Check-in saved!")
    
    elif nav_choice == "📈 Insights" or st.session_state.get('nav_override') == "📈 Insights":
        st.session_state.nav_override = None
        
        st.header("📈 Your Mental Health Insights")
        
        if user_data.get('mood_history'):
            # Mobile mood chart
            fig = create_mobile_mood_chart(user_data['mood_history'])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Mobile insights
            moods = [entry['mood'] for entry in user_data['mood_history']]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📊 Average Mood", f"{sum(moods)/len(moods):.1f}/10")
                st.metric("📈 Best Day", f"{max(moods)}/10")
            with col2:
                st.metric("📱 Total Check-ins", len(moods))
                recent_avg = sum(moods[-7:]) / min(7, len(moods))
                st.metric("🗓️ This Week", f"{recent_avg:.1f}/10")
            
            # Patterns
            st.subheader("🔍 Patterns I Notice")
            
            if len(moods) >= 7:
                trend = sum(moods[-3:]) / 3 - sum(moods[-7:-4]) / 3
                if trend > 0.5:
                    st.success("📈 Your mood has been improving lately!")
                elif trend < -0.5:
                    st.warning("📉 You've had some challenging days recently")
                else:
                    st.info("📊 Your mood has been relatively stable")
        else:
            st.info("📱 Complete a few check-ins to see your insights!")
    
    elif nav_choice == "⚙️ Settings":
        st.header("⚙️ App Settings")
        
        # App installation info
        st.markdown("""
        <div class="app-install">
            <h3>📱 Install This App</h3>
            <p>Add to your home screen for quick access!</p>
            <p><strong>📋 Share link:</strong> Copy the URL from your browser to share with friends!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Data export
        st.subheader("💾 Backup Your Data")
        if st.button("📤 Export My Data", use_container_width=True):
            export_data = export_user_data(user_data)
            st.download_button(
                label="💾 Download Backup",
                data=export_data,
                file_name=f"{st.session_state.current_user}_mental_health_backup.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Notifications
        st.subheader("🔔 Settings")
        notifications = st.toggle("Daily reminder notifications", value=user_data.get('notifications_enabled', True))
        
        if notifications != user_data.get('notifications_enabled', True):
            app_data['users'][st.session_state.current_user]['notifications_enabled'] = notifications
            save_mobile_data(app_data)
            st.success("✅ Settings updated!")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            del st.session_state.current_user
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666; font-size: 0.8rem;">📱 Mental Health Buddy Mobile • Your wellbeing, anywhere 💙</p>',
    unsafe_allow_html=True
)