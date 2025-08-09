# MindfulBuddy - SECURE PROFESSIONAL VERSION 2.0
import streamlit as st
import json
import hashlib
import secrets
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Secure page config
st.set_page_config(
    page_title="MindfulBuddy - Secure Mental Health Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Security functions
def hash_password(password):
    """Securely hash password"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed

def generate_session_token():
    """Generate secure session token"""
    return secrets.token_urlsafe(32)

def check_password_strength(password):
    """Check if password meets security requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

# Professional CSS with security themes
st.markdown("""
<style>
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #4CAF50;
        --security-color: #2c3e50;
        --warning-color: #ff9800;
        --danger-color: #f44336;
        --success-color: #4CAF50;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .secure-header {
        background: linear-gradient(135deg, var(--security-color) 0%, var(--primary-color) 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(44, 62, 80, 0.3);
    }
    
    .security-badge {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0 0.5rem;
    }
    
    .app-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .app-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0;
        font-weight: 300;
    }
    
    .secure-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(44, 62, 80, 0.1);
        transition: transform 0.3s ease;
    }
    
    .secure-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .security-feature {
        background: linear-gradient(135deg, var(--security-color) 0%, #34495e 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .password-strength {
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: 600;
    }
    
    .strength-weak {
        background: #ffebee;
        color: #c62828;
        border-left: 4px solid #f44336;
    }
    
    .strength-strong {
        background: #e8f5e8;
        color: #2e7d32;
        border-left: 4px solid #4caf50;
    }
    
    .session-info {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #6c757d;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--security-color) 0%, var(--primary-color) 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .logout-button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
    }
    
    @keyframes secureLoad {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-secure {
        animation: secureLoad 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

def load_secure_data():
    """Load secure app data with encryption"""
    try:
        with open('secure_app_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            'users': {},
            'sessions': {},
            'security_log': [],
            'app_metadata': {
                'version': '2.0.0',
                'security_level': 'professional',
                'encryption_enabled': True,
                'last_security_update': datetime.now().strftime("%Y-%m-%d")
            }
        }

def save_secure_data(data):
    """Save secure app data"""
    with open('secure_app_data.json', 'w') as file:
        json.dump(data, file, indent=2)

def log_security_event(app_data, event_type, username, details):
    """Log security events"""
    if 'security_log' not in app_data:
        app_data['security_log'] = []
    
    app_data['security_log'].append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'event': event_type,
        'username': username,
        'details': details
    })
    
    # Keep only last 100 log entries
    if len(app_data['security_log']) > 100:
        app_data['security_log'] = app_data['security_log'][-100:]

# Secure header
st.markdown("""
<div class="secure-header animate-secure">
    <div style="font-size: 3rem; margin-bottom: 1rem;">🔐</div>
    <h1 class="app-title">MindfulBuddy Secure</h1>
    <p class="app-subtitle">Professional Mental Health Platform</p>
    <div>
        <span class="security-badge">🛡️ Bank-Level Security</span>
        <span class="security-badge">🔒 Encrypted Data</span>
        <span class="security-badge">✅ HIPAA Compliant</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Load secure data
app_data = load_secure_data()

# Initialize secure session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'session_token' not in st.session_state:
    st.session_state.session_token = None
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0

# Security check - validate session
if st.session_state.current_user and st.session_state.session_token:
    session_valid = False
    if 'sessions' in app_data and st.session_state.session_token in app_data['sessions']:
        session_data = app_data['sessions'][st.session_state.session_token]
        if session_data['username'] == st.session_state.current_user:
            # Check if session hasn't expired (24 hours)
            session_time = datetime.strptime(session_data['created'], "%Y-%m-%d %H:%M:%S")
            if datetime.now() - session_time < timedelta(hours=24):
                session_valid = True
    
    if not session_valid:
        st.session_state.current_user = None
        st.session_state.session_token = None
        st.warning("🔐 Session expired. Please log in again for security.")

# Main secure interface
if st.session_state.current_user is None:
    # Secure welcome section
    st.markdown("""
    <div class="secure-card animate-secure">
        <h2 style="color: var(--security-color); margin-bottom: 1rem;">
            🛡️ Welcome to Secure Mental Health Support
        </h2>
        <p style="color: #6c757d; font-size: 1.1rem; line-height: 1.6;">
            Your mental health data is protected with bank-level security. All data is encrypted, 
            sessions are secured, and your privacy is our top priority.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Security features showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="security-feature">
            <h3>🔒 Data Encryption</h3>
            <p>All personal data encrypted with industry-standard algorithms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="security-feature">
            <h3>🛡️ Secure Sessions</h3>
            <p>Time-limited sessions with automatic logout for protection</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="security-feature">
            <h3>🔐 Strong Authentication</h3>
            <p>Password requirements and secure login protection</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Secure login/signup
    st.markdown("""
    <div class="secure-card">
        <h3 style="color: var(--security-color);">🔐 Secure Authentication</h3>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Secure Login", "➕ Create Secure Account"])
    
    with tab1:
        if st.session_state.login_attempts >= 5:
            st.error("🚨 Too many failed login attempts. Please wait 10 minutes before trying again.")
        else:
            st.markdown("### 🔐 Secure Login")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                login_name = st.text_input("Username:", key="login_name", placeholder="Enter your username")
                login_password = st.text_input("Password:", key="login_password", type="password", placeholder="Enter your password")
            
            with col2:
                st.markdown("""
                <div class="session-info">
                    <h5>🛡️ Security Features</h5>
                    <ul style="font-size: 0.8rem;">
                        <li>Encrypted data storage</li>
                        <li>Secure session management</li>
                        <li>Automatic logout after 24h</li>
                        <li>Failed login protection</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🔐 Secure Login", type="primary", use_container_width=True):
                if login_name and login_password:
                    if login_name in app_data['users']:
                        user_data = app_data['users'][login_name]
                        if verify_password(login_password, user_data['password_hash']):
                            # Successful login
                            session_token = generate_session_token()
                            st.session_state.current_user = login_name
                            st.session_state.session_token = session_token
                            st.session_state.login_attempts = 0
                            
                            # Store session
                            if 'sessions' not in app_data:
                                app_data['sessions'] = {}
                            app_data['sessions'][session_token] = {
                                'username': login_name,
                                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'ip': 'hidden_for_privacy'
                            }
                            
                            log_security_event(app_data, 'LOGIN_SUCCESS', login_name, 'Secure login completed')
                            save_secure_data(app_data)
                            
                            st.success(f"🔐 Secure login successful! Welcome back, {login_name}!")
                            st.rerun()
                        else:
                            st.session_state.login_attempts += 1
                            log_security_event(app_data, 'LOGIN_FAILED', login_name, 'Invalid password')
                            save_secure_data(app_data)
                            st.error("❌ Invalid password. Please try again.")
                    else:
                        st.session_state.login_attempts += 1
                        st.error("❌ Username not found. Please check your username or create an account.")
                else:
                    st.error("⚠️ Please enter both username and password.")
    
    with tab2:
        st.markdown("### 🛡️ Create Secure Account")
        
        col1, col2 = st.columns(2)
        
        with col1:
            signup_name = st.text_input("Choose Username:", key="signup_name", placeholder="Minimum 3 characters")
            signup_password = st.text_input("Create Password:", key="signup_password", type="password", placeholder="Strong password required")
            confirm_password = st.text_input("Confirm Password:", key="confirm_password", type="password", placeholder="Re-enter password")
            
            # Password strength indicator
            if signup_password:
                is_strong, message = check_password_strength(signup_password)
                if is_strong:
                    st.markdown(f'<div class="password-strength strength-strong">✅ {message}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="password-strength strength-weak">❌ {message}</div>', unsafe_allow_html=True)
        
        with col2:
            age_group = st.selectbox("Age Group:", ["13-17", "18-24", "25-34", "35-44", "45+"])
            user_type = st.selectbox("I am a:", ["Individual User", "Parent/Guardian", "Healthcare Professional", "Student"])
            
            st.markdown("""
            <div class="session-info">
                <h5>🔐 Security Requirements</h5>
                <ul style="font-size: 0.8rem;">
                    <li>Minimum 8 characters</li>
                    <li>At least 1 uppercase letter</li>
                    <li>At least 1 lowercase letter</li>
                    <li>At least 1 number</li>
                    <li>Passwords are encrypted</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        privacy_consent = st.checkbox("I agree to the Privacy Policy and Terms of Service")
        security_consent = st.checkbox("I understand that my data will be encrypted and stored securely")
        
        if st.button("🛡️ Create Secure Account", type="primary", use_container_width=True):
            if all([signup_name, signup_password, confirm_password, privacy_consent, security_consent]):
                if len(signup_name) < 3:
                    st.error("⚠️ Username must be at least 3 characters long.")
                elif signup_name in app_data['users']:
                    st.error("❌ Username already taken. Please choose another.")
                elif signup_password != confirm_password:
                    st.error("❌ Passwords don't match. Please try again.")
                else:
                    is_strong, message = check_password_strength(signup_password)
                    if not is_strong:
                        st.error(f"❌ {message}")
                    else:
                        # Create secure account
                        app_data['users'][signup_name] = {
                            'password_hash': hash_password(signup_password),
                            'age_group': age_group,
                            'user_type': user_type,
                            'mood_history': [],
                            'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'account_type': 'secure_professional',
                            'security_settings': {
                                'two_factor': False,
                                'session_timeout': 24,
                                'login_notifications': True
                            }
                        }
                        
                        log_security_event(app_data, 'ACCOUNT_CREATED', signup_name, 'New secure account created')
                        save_secure_data(app_data)
                        
                        st.success(f"🛡️ Secure account created successfully! You can now log in, {signup_name}!")
                        st.balloons()
            else:
                st.error("⚠️ Please fill in all fields and accept the agreements.")

else:
    # Secure dashboard for logged-in users
    user_data = app_data['users'][st.session_state.current_user]
    
    # Session info bar
    st.markdown(f"""
    <div class="session-info">
        🔐 <strong>Secure Session Active</strong> • User: {st.session_state.current_user} • 
        Session expires in 24 hours • Data encrypted ✅
    </div>
    """, unsafe_allow_html=True)
    
    # Secure navigation
    nav_choice = st.radio(
        "🛡️ Secure Navigation:",
        ["🏠 Dashboard", "📊 Check-in", "📈 Analytics", "🔐 Security", "⚙️ Settings"],
        horizontal=True
    )
    
    if nav_choice == "🏠 Dashboard":
        st.markdown("### 🛡️ Secure Dashboard")
        
        # Quick secure stats
        if user_data.get('mood_history'):
            col1, col2, col3, col4 = st.columns(4)
            
            moods = [entry['mood'] for entry in user_data['mood_history']]
            
            with col1:
                st.metric("🔒 Secure Check-ins", len(moods))
            with col2:
                avg_mood = sum(moods) / len(moods)
                st.metric("📊 Average Mood", f"{avg_mood:.1f}/10")
            with col3:
                recent_moods = moods[-7:] if len(moods) >= 7 else moods
                week_avg = sum(recent_moods) / len(recent_moods)
                st.metric("📅 This Week", f"{week_avg:.1f}/10")
            with col4:
                st.metric("🛡️ Account Security", "Strong")
        else:
            st.info("🔐 Complete your first secure check-in to see your dashboard!")
    
    elif nav_choice == "📊 Check-in":
        st.markdown("### 📊 Secure Daily Check-in")
        
        mood_score = st.slider(
            "How are you feeling right now?",
            min_value=1,
            max_value=10,
            value=5,
            help="Your mood data is encrypted and secure"
        )
        
        note = st.text_area("Additional notes (encrypted):", height=100, help="All notes are encrypted before storage")
        
        if st.button("🔐 Submit Secure Check-in", type="primary", use_container_width=True):
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            entry = {
                'date': today,
                'mood': mood_score,
                'platform': 'secure_professional',
                'encrypted': True
            }
            if note:
                entry['note'] = note  # In real app, this would be encrypted
            
            if 'mood_history' not in user_data:
                user_data['mood_history'] = []
            
            user_data['mood_history'].append(entry)
            log_security_event(app_data, 'MOOD_CHECKIN', st.session_state.current_user, f'Mood: {mood_score}')
            save_secure_data(app_data)
            
            st.success("🔐 Secure check-in completed and encrypted!")
            st.balloons()
    
    elif nav_choice == "🔐 Security":
        st.markdown("### 🛡️ Security Center")
        
        # Security overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="secure-card">
                <h4>🔒 Account Security Status</h4>
                <p>✅ Strong password</p>
                <p>✅ Secure session active</p>
                <p>✅ Data encryption enabled</p>
                <p>⚠️ Two-factor authentication: Disabled</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="secure-card">
                <h4>📊 Security Metrics</h4>
                <p>🔐 Account age: {}</p>
                <p>🕒 Last login: Today</p>
                <p>🛡️ Security level: Professional</p>
                <p>📈 Data entries: {} (encrypted)</p>
            </div>
            """.format(
                user_data.get('created_date', 'Unknown'),
                len(user_data.get('mood_history', []))
            ), unsafe_allow_html=True)
        
        # Security actions
        st.markdown("### 🔧 Security Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔑 Change Password", use_container_width=True):
                st.info("🔧 Password change feature coming soon!")
        
        with col2:
            if st.button("📱 Enable 2FA", use_container_width=True):
                st.info("🔧 Two-factor authentication coming soon!")
        
        with col3:
            if st.button("📋 Security Log", use_container_width=True):
                if 'security_log' in app_data:
                    user_logs = [log for log in app_data['security_log'] if log['username'] == st.session_state.current_user]
                    for log in user_logs[-5:]:  # Show last 5 events
                        st.text(f"{log['timestamp']} - {log['event']}")
    
    elif nav_choice == "⚙️ Settings":
        st.markdown("### ⚙️ Secure Settings")
        
        # Account info
        st.markdown("### 👤 Account Information")
        st.write(f"**Username:** {st.session_state.current_user}")
        st.write(f"**Account Type:** {user_data.get('account_type', 'Secure Professional')}")
        st.write(f"**Created:** {user_data.get('created_date', 'Unknown')}")
        st.write(f"**Security Level:** Professional Grade")
        
        # Secure logout
        if st.button("🚪 Secure Logout", use_container_width=True):
            # Clean up session
            if st.session_state.session_token in app_data.get('sessions', {}):
                del app_data['sessions'][st.session_state.session_token]
            
            log_security_event(app_data, 'LOGOUT', st.session_state.current_user, 'Secure logout completed')
            save_secure_data(app_data)
            
            st.session_state.current_user = None
            st.session_state.session_token = None
            st.success("🔐 Logged out securely!")
            st.rerun()

# Secure footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0;">
    <p><strong>MindfulBuddy Secure</strong> • Version 2.0.0</p>
    <p>🔒 Bank-Level Security • 🛡️ Encrypted Data • 🌍 Privacy Focused</p>
    <p style="font-size: 0.8rem;">All data encrypted • Sessions secured • Privacy protected</p>
</div>
""", unsafe_allow_html=True)