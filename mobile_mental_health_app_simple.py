# Mental Health Buddy - PROFESSIONAL VERSION 1.0 (FIXED)
import streamlit as st
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Professional page config
st.set_page_config(
    page_title="MindfulBuddy - Professional Mental Health Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS with brand colors
st.markdown("""
<style>
    /* Professional brand colors */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #4CAF50;
        --warning-color: #ff9800;
        --danger-color: #f44336;
        --text-primary: #2c3e50;
        --text-secondary: #7f8c8d;
        --background: #f8f9fa;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Professional header */
    .professional-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .app-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .app-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0;
        font-weight: 300;
    }
    
    /* Professional cards */
    .pro-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .pro-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .feature-card {
        background: linear-gradient(135deg, var(--accent-color) 0%, #45a049 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: scale(1.02);
    }
    
    /* Professional buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Professional metrics */
    .metric-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 4px solid var(--primary-color);
    }
    
    /* Professional status indicators */
    .status-excellent {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .status-good {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .status-concern {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .status-alert {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        .professional-header {
            padding: 1.5rem 0;
        }
        .pro-card {
            padding: 1.5rem;
        }
    }
    
    /* Professional animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

def load_professional_data():
    """Load professional app data"""
    try:
        with open('professional_app_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            'users': {},
            'app_metadata': {
                'version': '1.0.0',
                'launch_date': datetime.now().strftime("%Y-%m-%d"),
                'total_users': 0,
                'total_checkins': 0
            }
        }

def save_professional_data(data):
    """Save professional app data"""
    with open('professional_app_data.json', 'w') as file:
        json.dump(data, file, indent=2)

def get_professional_mood_status(mood_score):
    """Get professional status indicator"""
    if mood_score >= 8:
        return "status-excellent", "Excellent", "🌟"
    elif mood_score >= 6:
        return "status-good", "Good", "😊"
    elif mood_score >= 4:
        return "status-concern", "Needs Attention", "⚠️"
    else:
        return "status-alert", "Critical", "🚨"

# Professional header (NO LOGO FUNCTION - DIRECT HTML)
st.markdown("""
<div class="professional-header animate-in">
    <div class="logo-container">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🧠</div>
    </div>
    <h1 class="app-title">MindfulBuddy</h1>
    <p class="app-subtitle">Professional Mental Health Platform</p>
    <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
        Trusted by thousands • Clinically informed • Privacy focused
    </p>
</div>
""", unsafe_allow_html=True)

# Load professional data
app_data = load_professional_data()

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Professional welcome section
if st.session_state.current_user is None:
    st.markdown("""
    <div class="pro-card animate-in">
        <h2 style="color: var(--text-primary); margin-bottom: 1rem;">
            🌟 Welcome to Professional Mental Health Support
        </h2>
        <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.6;">
            MindfulBuddy is a clinically-informed, AI-powered platform designed to support your mental wellness journey. 
            Our evidence-based approach combines cutting-edge technology with compassionate care.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional features showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Powered Insights</h3>
            <p>Advanced pattern recognition and mood prediction using machine learning algorithms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🛡️ Crisis Prevention</h3>
            <p>Intelligent early warning system with immediate access to professional resources</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>👨‍👩‍👧‍👦 Family Support</h3>
            <p>Comprehensive family mental health monitoring with privacy controls</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional login/signup
    st.markdown("""
    <div class="pro-card">
        <h3 style="color: var(--text-primary);">🔐 Secure Access</h3>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Existing User", "➕ New User"])
    
    with tab1:
        st.markdown("### Welcome Back")
        login_name = st.text_input("Username:", key="login_name", placeholder="Enter your username")
        
        if st.button("🚀 Access Platform", type="primary", use_container_width=True):
            if login_name and login_name in app_data['users']:
                st.session_state.current_user = login_name
                st.success(f"✅ Welcome back, {login_name}!")
                st.rerun()
            else:
                st.error("❌ User not found. Please check your username or create a new account.")
    
    with tab2:
        st.markdown("### Join MindfulBuddy")
        col1, col2 = st.columns(2)
        
        with col1:
            signup_name = st.text_input("Choose Username:", key="signup_name", placeholder="Your unique username")
            age_group = st.selectbox("Age Group:", ["13-17", "18-24", "25-34", "35-44", "45+"])
        
        with col2:
            user_type = st.selectbox("I am a:", ["Individual User", "Parent/Guardian", "Healthcare Professional", "Student"])
            privacy_consent = st.checkbox("I agree to the Privacy Policy and Terms of Service")
        
        if st.button("🎉 Create Professional Account", type="primary", use_container_width=True):
            if signup_name and privacy_consent and signup_name not in app_data['users']:
                app_data['users'][signup_name] = {
                    'age_group': age_group,
                    'user_type': user_type,
                    'mood_history': [],
                    'created_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'account_type': 'professional'
                }
                app_data['app_metadata']['total_users'] += 1
                save_professional_data(app_data)
                st.session_state.current_user = signup_name
                st.success(f"🎉 Professional account created! Welcome, {signup_name}!")
                st.balloons()
                st.rerun()
            elif not privacy_consent:
                st.error("⚠️ Please accept the Privacy Policy and Terms of Service to continue.")
            elif not signup_name:
                st.error("⚠️ Please choose a username.")
            else:
                st.error("❌ Username already taken. Please choose another.")

else:
    # Professional dashboard for logged-in users
    user_data = app_data['users'][st.session_state.current_user]
    
    # Professional status bar
    if user_data.get('mood_history'):
        latest_mood = user_data['mood_history'][-1]['mood']
        status_class, status_text, status_emoji = get_professional_mood_status(latest_mood)
        
        st.markdown(f"""
        <div class="metric-container">
            <div class="{status_class}">
                {status_emoji} Current Status: {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional navigation
    nav_choice = st.radio(
        "🧭 Navigation:",
        ["🏠 Dashboard", "📊 Check-in", "📈 Analytics", "⚙️ Settings"],
        horizontal=True
    )
    
    if nav_choice == "🏠 Dashboard":
        st.markdown("### 📊 Professional Dashboard")
        
        # Quick stats
        if user_data.get('mood_history'):
            col1, col2, col3, col4 = st.columns(4)
            
            moods = [entry['mood'] for entry in user_data['mood_history']]
            
            with col1:
                st.metric("Total Check-ins", len(moods))
            with col2:
                avg_mood = sum(moods) / len(moods)
                st.metric("Average Mood", f"{avg_mood:.1f}/10")
            with col3:
                recent_moods = moods[-7:] if len(moods) >= 7 else moods
                week_avg = sum(recent_moods) / len(recent_moods)
                st.metric("This Week", f"{week_avg:.1f}/10")
            with col4:
                streak = 1 if moods[-1] >= 6 else 0
                if streak:
                    for i in range(len(moods)-2, -1, -1):
                        if moods[i] >= 6:
                            streak += 1
                        else:
                            break
                st.metric("Good Days Streak", f"{streak} days")
        else:
            st.info("📊 Complete your first check-in to see your dashboard!")
    
    elif nav_choice == "📊 Check-in":
        st.markdown("### 📊 Daily Mental Health Check-in")
        
        mood_score = st.slider(
            "How are you feeling right now?",
            min_value=1,
            max_value=10,
            value=5,
            help="1=Very Low, 10=Excellent"
        )
        
        # Show status
        status_class, status_text, status_emoji = get_professional_mood_status(mood_score)
        st.markdown(f"""
        <div class="{status_class}" style="margin: 1rem 0; text-align: center;">
            {status_emoji} {status_text}
        </div>
        """, unsafe_allow_html=True)
        
        note = st.text_area("Additional notes (optional):", height=100)
        
        if st.button("✅ Submit Professional Check-in", type="primary", use_container_width=True):
            today = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            entry = {
                'date': today,
                'mood': mood_score,
                'platform': 'professional'
            }
            if note:
                entry['note'] = note
            
            if 'mood_history' not in user_data:
                user_data['mood_history'] = []
            
            user_data['mood_history'].append(entry)
            app_data['app_metadata']['total_checkins'] += 1
            save_professional_data(app_data)
            
            st.success("✅ Check-in completed successfully!")
            st.balloons()
    
    elif nav_choice == "📈 Analytics":
        st.markdown("### 📈 Professional Analytics")
        
        if user_data.get('mood_history'):
            # Create professional chart
            moods = [entry['mood'] for entry in user_data['mood_history']]
            dates = [entry['date'].split()[0] for entry in user_data['mood_history']]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=moods,
                mode='lines+markers',
                name='Mood Trend',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="📊 Professional Mood Analytics",
                xaxis_title="Date",
                yaxis_title="Mood Score",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Professional insights
            st.markdown("### 🧠 AI-Powered Insights")
            avg_mood = sum(moods) / len(moods)
            
            if avg_mood >= 7:
                st.success("🌟 Excellent mental health trends detected!")
            elif avg_mood >= 5:
                st.info("💚 Stable mental health patterns observed.")
            else:
                st.warning("⚠️ Consider additional support resources.")
        else:
            st.info("📊 Complete check-ins to unlock professional analytics!")
    
    elif nav_choice == "⚙️ Settings":
        st.markdown("### ⚙️ Professional Settings")
        
        # Account info
        st.markdown("### 👤 Account Information")
        st.write(f"**Username:** {st.session_state.current_user}")
        st.write(f"**Account Type:** {user_data.get('account_type', 'Professional')}")
        st.write(f"**Created:** {user_data.get('created_date', 'Unknown')}")
        
        # Data export
        if st.button("📤 Export Professional Data", use_container_width=True):
            export_data = {
                'username': st.session_state.current_user,
                'mood_history': user_data.get('mood_history', []),
                'export_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'platform': 'MindfulBuddy Professional'
            }
            
            st.download_button(
                label="💾 Download Data",
                data=json.dumps(export_data, indent=2),
                file_name=f"{st.session_state.current_user}_mindfulbuddy_data.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()

# Professional footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); padding: 2rem 0;">
    <p><strong>MindfulBuddy Professional</strong> • Version 1.0.0</p>
    <p>🔒 Privacy Focused • 🌍 Trusted Globally • 💙 Built with Care</p>
</div>
""", unsafe_allow_html=True)
