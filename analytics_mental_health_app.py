# MindfulBuddy - ADVANCED ANALYTICS VERSION 3.0
import streamlit as st
import json
import hashlib
import secrets
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import calendar

# Advanced page config
st.set_page_config(
    page_title="MindfulBuddy Analytics - Professional Mental Health Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Analytics CSS
st.markdown("""
<style>
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #4CAF50;
        --analytics-color: #2196F3;
        --warning-color: #ff9800;
        --danger-color: #f44336;
        --success-color: #4CAF50;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .analytics-header {
        background: linear-gradient(135deg, var(--analytics-color) 0%, var(--primary-color) 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(33, 150, 243, 0.3);
    }
    
    .analytics-badge {
        background: linear-gradient(135deg, #00bcd4 0%, #0097a7 100%);
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
    
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid var(--analytics-color);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .analytics-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(33, 150, 243, 0.1);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid var(--analytics-color);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .trend-up {
        color: var(--success-color);
        font-weight: bold;
    }
    
    .trend-down {
        color: var(--danger-color);
        font-weight: bold;
    }
    
    .trend-stable {
        color: var(--analytics-color);
        font-weight: bold;
    }
    
    .report-section {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    
    @keyframes analyticsLoad {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .animate-analytics {
        animation: analyticsLoad 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Security functions (from previous version)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def generate_session_token():
    return secrets.token_urlsafe(32)

# Advanced Analytics Functions
def calculate_mood_trends(mood_history):
    """Calculate advanced mood trends and patterns"""
    if len(mood_history) < 2:
        return {}
    
    df = pd.DataFrame(mood_history)
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    df['week'] = df['date'].dt.isocalendar().week
    df['month'] = df['date'].dt.month
    df['hour'] = df['date'].dt.hour
    
    trends = {
        'overall_trend': calculate_overall_trend(df),
        'weekly_pattern': df.groupby('day_of_week')['mood'].mean().to_dict(),
        'monthly_trend': df.groupby('month')['mood'].mean().to_dict(),
        'time_of_day': df.groupby('hour')['mood'].mean().to_dict(),
        'volatility': df['mood'].std(),
        'consistency_score': calculate_consistency_score(df),
        'improvement_rate': calculate_improvement_rate(df),
        'risk_periods': identify_risk_periods(df)
    }
    
    return trends

def calculate_overall_trend(df):
    """Calculate overall mood trend"""
    if len(df) < 2:
        return 0
    
    # Simple linear regression slope
    x = np.arange(len(df))
    y = df['mood'].values
    slope = np.polyfit(x, y, 1)[0]
    
    return slope

def calculate_consistency_score(df):
    """Calculate how consistent mood patterns are (0-100)"""
    std_dev = df['mood'].std()
    # Lower standard deviation = higher consistency
    consistency = max(0, 100 - (std_dev * 10))
    return round(consistency, 1)

def calculate_improvement_rate(df):
    """Calculate rate of improvement over time"""
    if len(df) < 7:
        return 0
    
    recent_avg = df.tail(7)['mood'].mean()
    earlier_avg = df.head(7)['mood'].mean()
    
    return round(((recent_avg - earlier_avg) / earlier_avg) * 100, 1)

def identify_risk_periods(df):
    """Identify periods of concerning mood patterns"""
    risk_periods = []
    
    # Look for consecutive low moods
    low_mood_threshold = 4
    consecutive_low = 0
    
    for _, row in df.iterrows():
        if row['mood'] <= low_mood_threshold:
            consecutive_low += 1
        else:
            if consecutive_low >= 3:
                risk_periods.append({
                    'type': 'consecutive_low',
                    'duration': consecutive_low,
                    'severity': 'high' if consecutive_low >= 5 else 'medium'
                })
            consecutive_low = 0
    
    return risk_periods

def create_advanced_mood_chart(mood_history):
    """Create comprehensive mood visualization"""
    if len(mood_history) < 2:
        return None
    
    df = pd.DataFrame(mood_history)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Mood Over Time', 'Weekly Pattern', 'Monthly Trends', 'Daily Distribution'),
        specs=[[{"secondary_y": True}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "histogram"}]]
    )
    
    # Main mood line chart
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['mood'],
            mode='lines+markers',
            name='Mood',
            line=dict(color='#2196F3', width=3),
            marker=dict(size=8)
        ),
        row=1, col=1
    )
    
    # Add trend line
    x_numeric = np.arange(len(df))
    z = np.polyfit(x_numeric, df['mood'], 1)
    trend_line = np.poly1d(z)(x_numeric)
    
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=trend_line,
            mode='lines',
            name='Trend',
            line=dict(color='#ff9800', width=2, dash='dash')
        ),
        row=1, col=1
    )
    
    # Weekly pattern
    weekly_avg = df.groupby(df['date'].dt.day_name())['mood'].mean()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_ordered = weekly_avg.reindex([day for day in day_order if day in weekly_avg.index])
    
    fig.add_trace(
        go.Bar(
            x=weekly_ordered.index,
            y=weekly_ordered.values,
            name='Weekly Avg',
            marker_color='#4CAF50'
        ),
        row=1, col=2
    )
    
    # Monthly trends
    monthly_avg = df.groupby(df['date'].dt.month)['mood'].mean()
    month_names = [calendar.month_abbr[i] for i in monthly_avg.index]
    
    fig.add_trace(
        go.Bar(
            x=month_names,
            y=monthly_avg.values,
            name='Monthly Avg',
            marker_color='#9C27B0'
        ),
        row=2, col=1
    )
    
    # Mood distribution
    fig.add_trace(
        go.Histogram(
            x=df['mood'],
            nbinsx=10,
            name='Distribution',
            marker_color='#FF5722'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        title_text="📊 Advanced Mood Analytics Dashboard",
        showlegend=True
    )
    
    return fig

def create_insights_report(trends, mood_history):
    """Generate AI-powered insights report"""
    insights = []
    
    # Overall trend analysis
    overall_trend = trends.get('overall_trend', 0)
    if overall_trend > 0.1:
        insights.append("📈 **Positive Trend**: Your mood has been improving over time! Keep up the great work.")
    elif overall_trend < -0.1:
        insights.append("📉 **Attention Needed**: Your mood trend shows a decline. Consider reaching out for support.")
    else:
        insights.append("📊 **Stable Pattern**: Your mood has been relatively stable over time.")
    
    # Consistency analysis
    consistency = trends.get('consistency_score', 0)
    if consistency > 80:
        insights.append(f"🎯 **High Consistency**: Your mood patterns are very consistent ({consistency}% score).")
    elif consistency > 60:
        insights.append(f"⚖️ **Moderate Consistency**: Your mood shows some variation ({consistency}% score).")
    else:
        insights.append(f"🎢 **High Variability**: Your mood varies significantly ({consistency}% score). This is normal but worth monitoring.")
    
    # Weekly pattern insights
    weekly_pattern = trends.get('weekly_pattern', {})
    if weekly_pattern:
        best_day = max(weekly_pattern, key=weekly_pattern.get)
        worst_day = min(weekly_pattern, key=weekly_pattern.get)
        insights.append(f"📅 **Weekly Pattern**: You tend to feel best on {best_day}s and may need extra support on {worst_day}s.")
    
    # Risk assessment
    risk_periods = trends.get('risk_periods', [])
    if risk_periods:
        high_risk = [p for p in risk_periods if p.get('severity') == 'high']
        if high_risk:
            insights.append("🚨 **Important**: Detected periods of extended low mood. Consider professional support.")
    
    # Improvement rate
    improvement_rate = trends.get('improvement_rate', 0)
    if improvement_rate > 10:
        insights.append(f"🌟 **Great Progress**: {improvement_rate:.1f}% improvement in recent weeks!")
    elif improvement_rate < -10:
        insights.append(f"💙 **Gentle Reminder**: Recent weeks show challenges. Remember, ups and downs are normal.")
    
    return insights

def load_analytics_data():
    """Load app data with analytics capabilities"""
    try:
        with open('analytics_app_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            'users': {},
            'sessions': {},
            'analytics': {
                'total_reports_generated': 0,
                'advanced_insights_enabled': True
            },
            'app_metadata': {
                'version': '3.0.0',
                'analytics_level': 'professional',
                'ai_insights': True
            }
        }

def save_analytics_data(data):
    """Save analytics data"""
    with open('analytics_app_data.json', 'w') as file:
        json.dump(data, file, indent=2)

# Analytics header
st.markdown("""
<div class="analytics-header animate-analytics">
    <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
    <h1 class="app-title">MindfulBuddy Analytics</h1>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin: 0.5rem 0;">
        Advanced Mental Health Analytics Platform
    </p>
    <div>
        <span class="analytics-badge">📈 AI Insights</span>
        <span class="analytics-badge">📊 Advanced Charts</span>
        <span class="analytics-badge">🎯 Predictive Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Load data
app_data = load_analytics_data()

# Session management (simplified for analytics focus)
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Main interface
if st.session_state.current_user is None:
    # Login section (simplified)
    st.markdown("""
    <div class="analytics-card animate-analytics">
        <h2 style="color: var(--analytics-color);">📊 Welcome to Advanced Analytics</h2>
        <p style="color: #6c757d; font-size: 1.1rem;">
            Get professional-grade insights into your mental health patterns with AI-powered analytics.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick demo features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Trend Analysis</h3>
            <p>Advanced trend detection with predictive capabilities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🧠 AI Insights</h3>
            <p>Machine learning powered pattern recognition</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📋 Custom Reports</h3>
            <p>Professional reports for personal or clinical use</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Login
    tab1, tab2 = st.tabs(["🔑 Login", "➕ Sign Up"])
    
    with tab1:
        login_name = st.text_input("Username:", key="login_name")
        login_password = st.text_input("Password:", key="login_password", type="password")
        
        if st.button("📊 Access Analytics", type="primary", use_container_width=True):
            if login_name and login_password:
                if login_name in app_data['users'] and verify_password(login_password, app_data['users'][login_name]['password_hash']):
                    st.session_state.current_user = login_name
                    st.success(f"📊 Welcome to Analytics, {login_name}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            else:
                st.error("⚠️ Please enter username and password")
    
    with tab2:
        signup_name = st.text_input("Username:", key="signup_name")
        signup_password = st.text_input("Password:", key="signup_password", type="password")
        
        if st.button("📊 Create Analytics Account", type="primary", use_container_width=True):
            if signup_name and signup_password and signup_name not in app_data['users']:
                app_data['users'][signup_name] = {
                    'password_hash': hash_password(signup_password),
                    'mood_history': [],
                    'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'account_type': 'analytics_professional'
                }
                save_analytics_data(app_data)
                st.session_state.current_user = signup_name
                st.success(f"📊 Analytics account created! Welcome, {signup_name}!")
                st.rerun()
            else:
                st.error("❌ Invalid input or username taken")

else:
    # Analytics dashboard for logged-in users
    user_data = app_data['users'][st.session_state.current_user]
    
    # Navigation
    nav_choice = st.radio(
        "📊 Analytics Navigation:",
        ["📈 Dashboard", "📊 Check-in", "🧠 AI Insights", "📋 Reports", "⚙️ Settings"],
        horizontal=True
    )
    
    if nav_choice == "📈 Dashboard":
        st.markdown("### 📊 Advanced Analytics Dashboard")
        
        if user_data.get('mood_history') and len(user_data['mood_history']) >= 2:
            # Calculate trends
            trends = calculate_mood_trends(user_data['mood_history'])
            
            # Key metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_entries = len(user_data['mood_history'])
                st.metric("📊 Total Entries", total_entries)
            
            with col2:
                avg_mood = sum(entry['mood'] for entry in user_data['mood_history']) / total_entries
                st.metric("📈 Average Mood", f"{avg_mood:.1f}/10")
            
            with col3:
                consistency = trends.get('consistency_score', 0)
                st.metric("🎯 Consistency", f"{consistency}%")
            
            with col4:
                trend_slope = trends.get('overall_trend', 0)
                trend_text = "📈 Improving" if trend_slope > 0.05 else "📉 Declining" if trend_slope < -0.05 else "📊 Stable"
                st.metric("🔄 Trend", trend_text)
            
            # Advanced charts
            fig = create_advanced_mood_chart(user_data['mood_history'])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # AI Insights
            st.markdown("### 🧠 AI-Powered Insights")
            insights = create_insights_report(trends, user_data['mood_history'])
            
            for insight in insights:
                st.markdown(f"""
                <div class="insight-box">
                    {insight}
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("📊 Add more mood entries to unlock advanced analytics!")
    
    elif nav_choice == "📊 Check-in":
        st.markdown("### 📊 Analytics-Enhanced Check-in")
        
        # Enhanced check-in with more data points
        col1, col2 = st.columns([2, 1])
        
        with col1:
            mood_score = st.slider("Overall Mood (1-10):", 1, 10, 5)
            
            # Additional metrics
            energy_level = st.slider("Energy Level (1-10):", 1, 10, 5)
            stress_level = st.slider("Stress Level (1-10):", 1, 10, 5)
            sleep_quality = st.slider("Sleep Quality (1-10):", 1, 10, 5)
            
            # Context
            activities = st.multiselect(
                "Today's Activities:",
                ["Work/School", "Exercise", "Social", "Relaxation", "Creative", "Outdoor", "Learning"]
            )
            
            note = st.text_area("Notes:", height=100)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>📊 Analytics Preview</h4>
                <p>Your data helps generate insights about:</p>
                <ul>
                    <li>Mood patterns</li>
                    <li>Energy correlations</li>
                    <li>Stress triggers</li>
                    <li>Sleep impact</li>
                    <li>Activity effects</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("📊 Submit Analytics Check-in", type="primary", use_container_width=True):
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            entry = {
                'date': today,
                'mood': mood_score,
                'energy': energy_level,
                'stress': stress_level,
                'sleep': sleep_quality,
                'activities': activities,
                'platform': 'analytics_professional'
            }
            if note:
                entry['note'] = note
            
            if 'mood_history' not in user_data:
                user_data['mood_history'] = []
            
            user_data['mood_history'].append(entry)
            save_analytics_data(app_data)
            
            st.success("📊 Enhanced analytics data recorded!")
            st.balloons()
    
    elif nav_choice == "🧠 AI Insights":
        st.markdown("### 🧠 AI-Powered Mental Health Insights")
        
        if user_data.get('mood_history') and len(user_data['mood_history']) >= 5:
            trends = calculate_mood_trends(user_data['mood_history'])
            
            # Detailed insights sections
            st.markdown("#### 📈 Trend Analysis")
            
            overall_trend = trends.get('overall_trend', 0)
            if overall_trend > 0.1:
                st.success("📈 **Positive Trend Detected**: Your mental health shows consistent improvement over time.")
            elif overall_trend < -0.1:
                st.warning("📉 **Declining Trend**: Recent patterns suggest you might benefit from additional support.")
            else:
                st.info("📊 **Stable Pattern**: Your mood remains relatively consistent.")
            
            # Weekly patterns
            st.markdown("#### 📅 Weekly Pattern Analysis")
            weekly_pattern = trends.get('weekly_pattern', {})
            if weekly_pattern:
                df_weekly = pd.DataFrame(list(weekly_pattern.items()), columns=['Day', 'Average Mood'])
                
                fig_weekly = px.bar(
                    df_weekly, 
                    x='Day', 
                    y='Average Mood',
                    title="📅 Average Mood by Day of Week",
                    color='Average Mood',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig_weekly, use_container_width=True)
            
            # Risk assessment
            risk_periods = trends.get('risk_periods', [])
            if risk_periods:
                st.markdown("#### 🚨 Risk Assessment")
                for risk in risk_periods:
                    if risk.get('severity') == 'high':
                        st.error(f"🚨 **High Risk Period**: {risk.get('duration', 0)} consecutive days of low mood detected.")
                    else:
                        st.warning(f"⚠️ **Moderate Risk**: {risk.get('duration', 0)} days of concerning patterns.")
        
        else:
            st.info("🧠 Complete more check-ins to unlock AI insights!")
    
    elif nav_choice == "📋 Reports":
        st.markdown("### 📋 Professional Analytics Reports")
        
        if user_data.get('mood_history'):
            # Report generation
            report_type = st.selectbox(
                "Report Type:",
                ["Weekly Summary", "Monthly Analysis", "Custom Date Range", "Clinical Report"]
            )
            
            if st.button("📋 Generate Professional Report", type="primary"):
                st.markdown("#### 📊 Mental Health Analytics Report")
                st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                st.markdown(f"**User:** {st.session_state.current_user}")
                st.markdown(f"**Report Type:** {report_type}")
                
                # Summary statistics
                moods = [entry['mood'] for entry in user_data['mood_history']]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Total Entries", len(moods))
                with col2:
                    st.metric("📈 Average Mood", f"{sum(moods)/len(moods):.1f}")
                with col3:
                    st.metric("🎯 Highest Mood", max(moods))
                
                # Trend analysis
                trends = calculate_mood_trends(user_data['mood_history'])
                insights = create_insights_report(trends, user_data['mood_history'])
                
                st.markdown("#### 📝 Key Findings")
                for insight in insights:
                    st.markdown(f"• {insight}")
                
                # Export option
                report_data = {
                    'user': st.session_state.current_user,
                    'generated': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'type': report_type,
                    'summary': {
                        'total_entries': len(moods),
                        'average_mood': sum(moods)/len(moods),
                        'highest_mood': max(moods),
                        'lowest_mood': min(moods)
                    },
                    'insights': insights,
                    'raw_data': user_data['mood_history']
                }
                
                st.download_button(
                    "📤 Download Report",
                    data=json.dumps(report_data, indent=2),
                    file_name=f"mindfulbuddy_report_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        else:
            st.info("📋 Complete check-ins to generate reports!")
    
    elif nav_choice == "⚙️ Settings":
        st.markdown("### ⚙️ Analytics Settings")
        
        st.write(f"**Account:** {st.session_state.current_user}")
        st.write(f"**Analytics Level:** Professional")
        st.write(f"**Data Points:** {len(user_data.get('mood_history', []))}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.current_user = None
            st.rerun()

# Analytics footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem 0;">
    <p><strong>MindfulBuddy Analytics</strong> • Version 3.0.0</p>
    <p>📊 Professional Analytics • 🧠 AI Insights • 📈 Predictive Intelligence</p>
</div>
""", unsafe_allow_html=True)