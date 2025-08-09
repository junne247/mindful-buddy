# Mental Health Bot - FAMILY VERSION!
import streamlit as st
import json
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Family Mental Health Hub 👨‍👩‍👧‍👦",
    page_icon="🏠",
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
    .family-member-box {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: center;
    }
    .parent-dashboard {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .privacy-box {
        background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .alert-box {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_family_data():
    """Load all family member data"""
    try:
        with open('family_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            'family_members': {},
            'family_settings': {
                'sharing_enabled': False,
                'parent_access': False,
                'emergency_contacts': []
            }
        }

def save_family_data(data):
    """Save family data"""
    with open('family_data.json', 'w') as file:
        json.dump(data, file, indent=2)

def create_family_overview_chart(family_data):
    """Create chart showing all family members' moods"""
    if not family_data['family_members']:
        return None
    
    fig = go.Figure()
    
    colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']
    
    for i, (member_name, member_data) in enumerate(family_data['family_members'].items()):
        if member_data.get('mood_history') and member_data.get('sharing_enabled', False):
            dates = [entry['date'].split()[0] for entry in member_data['mood_history'][-14:]]  # Last 2 weeks
            moods = [entry['mood'] for entry in member_data['mood_history'][-14:]]
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=moods,
                mode='lines+markers',
                name=member_name,
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8)
            ))
    
    fig.update_layout(
        title="🏠 Family Mood Overview (Last 2 Weeks)",
        xaxis_title="Date",
        yaxis_title="Mood (1-10)",
        yaxis=dict(range=[0, 11]),
        template="plotly_white",
        height=400
    )
    
    return fig

def check_family_alerts(family_data):
    """Check for any family members who might need attention"""
    alerts = []
    
    for member_name, member_data in family_data['family_members'].items():
        if not member_data.get('mood_history'):
            continue
            
        recent_moods = [entry['mood'] for entry in member_data['mood_history'][-3:]]
        
        # Check for crisis patterns
        if any(mood <= 2 for mood in recent_moods):
            alerts.append({
                'member': member_name,
                'type': 'crisis',
                'message': f"{member_name} has reported very low moods recently"
            })
        
        # Check for consistent low moods
        elif all(mood <= 4 for mood in recent_moods) and len(recent_moods) >= 3:
            alerts.append({
                'member': member_name,
                'type': 'concern',
                'message': f"{member_name} has been struggling for several days"
            })
        
        # Check for no recent check-ins
        if member_data['mood_history']:
            last_checkin = datetime.strptime(member_data['mood_history'][-1]['date'].split()[0], '%Y-%m-%d')
            if (datetime.now() - last_checkin).days > 7:
                alerts.append({
                    'member': member_name,
                    'type': 'inactive',
                    'message': f"{member_name} hasn't checked in for over a week"
                })
    
    return alerts

def get_family_insights(family_data):
    """Generate insights about family mental health"""
    insights = []
    
    if not family_data['family_members']:
        return ["No family members added yet."]
    
    # Family mood average
    all_moods = []
    active_members = 0
    
    for member_name, member_data in family_data['family_members'].items():
        if member_data.get('mood_history'):
            recent_moods = [entry['mood'] for entry in member_data['mood_history'][-7:]]  # Last week
            if recent_moods:
                all_moods.extend(recent_moods)
                active_members += 1
    
    if all_moods:
        family_avg = sum(all_moods) / len(all_moods)
        insights.append(f"🏠 Family average mood this week: {family_avg:.1f}/10")
        
        if family_avg >= 7:
            insights.append("🌟 Your family is doing great overall!")
        elif family_avg >= 5:
            insights.append("💚 Your family is managing well with some ups and downs.")
        else:
            insights.append("💙 Your family might benefit from some extra support and care.")
    
    insights.append(f"👥 Active family members: {active_members}")
    
    return insights

# Initialize family data
family_data = load_family_data()

# Main header
st.markdown('<h1 class="main-header">🏠 Family Mental Health Hub</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Supporting the mental health of your entire family 👨‍👩‍👧‍👦</p>', unsafe_allow_html=True)

# Sidebar - Family Management
with st.sidebar:
    st.header("👥 Family Management")
    
    # Add new family member
    st.subheader("➕ Add Family Member")
    new_member_name = st.text_input("Name:", key="new_member")
    member_role = st.selectbox("Role:", ["Child/Teen", "Parent", "Adult Child", "Other"])
    
    if st.button("Add Member") and new_member_name:
        if new_member_name not in family_data['family_members']:
            family_data['family_members'][new_member_name] = {
                'role': member_role,
                'mood_history': [],
                'sharing_enabled': member_role == "Child/Teen",  # Default sharing for minors
                'created_date': datetime.now().strftime("%Y-%m-%d")
            }
            save_family_data(family_data)
            st.success(f"✅ Added {new_member_name} to family!")
            st.rerun()
    
    # Current family members
    st.subheader("👨‍👩‍👧‍👦 Family Members")
    for member_name, member_data in family_data['family_members'].items():
        checkins = len(member_data.get('mood_history', []))
        st.write(f"• **{member_name}** ({member_data['role']}) - {checkins} check-ins")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Family Overview", "📊 Individual Check-in", "👨‍👩‍👧‍👦 Parent Dashboard", "⚙️ Settings"])

with tab1:
    st.header("🏠 Family Mental Health Overview")
    
    # Family alerts
    alerts = check_family_alerts(family_data)
    if alerts:
        st.markdown("### 🚨 Family Alerts")
        for alert in alerts:
            if alert['type'] == 'crisis':
                st.markdown(f"""
                <div class="alert-box">
                    <h4>🆘 URGENT: {alert['member']}</h4>
                    <p>{alert['message']}</p>
                    <p>Consider reaching out immediately or seeking professional help.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ {alert['message']}")
    
    # Family mood chart
    if family_data['family_members']:
        family_chart = create_family_overview_chart(family_data)
        if family_chart:
            st.plotly_chart(family_chart, use_container_width=True)
        else:
            st.info("📊 Family chart will appear when members enable sharing and have mood data.")
    
    # Family insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Family Insights")
        insights = get_family_insights(family_data)
        for insight in insights:
            st.write(f"• {insight}")
    
    with col2:
        st.subheader("📈 Quick Stats")
        total_checkins = sum(len(member.get('mood_history', [])) for member in family_data['family_members'].values())
        st.metric("Total Family Check-ins", total_checkins)
        st.metric("Family Members", len(family_data['family_members']))
        
        # This week's activity
        week_checkins = 0
        for member_data in family_data['family_members'].values():
            for entry in member_data.get('mood_history', []):
                entry_date = datetime.strptime(entry['date'].split()[0], '%Y-%m-%d')
                if (datetime.now() - entry_date).days <= 7:
                    week_checkins += 1
        st.metric("This Week's Check-ins", week_checkins)

with tab2:
    st.header("📊 Individual Check-in")
    
    # Select family member
    if family_data['family_members']:
        selected_member = st.selectbox("Who is checking in?", list(family_data['family_members'].keys()))
        
        if selected_member:
            member_data = family_data['family_members'][selected_member]
            
            st.markdown(f"""
            <div class="family-member-box">
                <h3>👋 Hi {selected_member}!</h3>
                <p>Role: {member_data['role']}</p>
                <p>Total check-ins: {len(member_data.get('mood_history', []))}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Mood input
            col1, col2 = st.columns([2, 1])
            
            with col1:
                mood_score = st.slider(
                    f"How are you feeling today, {selected_member}?",
                    min_value=1,
                    max_value=10,
                    value=5,
                    help="1=Really struggling, 10=Amazing"
                )
                
                # Optional note
                note = st.text_area("Want to share what's on your mind? (optional)", height=100)
                
                if st.button("Submit Check-in", type="primary"):
                    today = datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    entry = {
                        'date': today,
                        'mood': mood_score
                    }
                    if note:
                        entry['note'] = note
                    
                    family_data['family_members'][selected_member]['mood_history'].append(entry)
                    save_family_data(family_data)
                    
                    # Response based on mood
                    if mood_score <= 3:
                        st.error(f"💙 I'm sorry you're struggling, {selected_member}. Remember, your family cares about you.")
                        if member_data['role'] == "Child/Teen":
                            st.info("🚨 Parent notification: Low mood detected for family member.")
                    elif mood_score >= 8:
                        st.success(f"✨ Great to hear you're doing well, {selected_member}!")
                    else:
                        st.info(f"💚 Thanks for checking in, {selected_member}. Every day is different.")
                    
                    st.success("✅ Check-in saved!")
                    st.rerun()
            
            with col2:
                # Individual stats
                if member_data.get('mood_history'):
                    moods = [entry['mood'] for entry in member_data['mood_history']]
                    st.metric("Average Mood", f"{sum(moods)/len(moods):.1f}/10")
                    st.metric("Best Day", f"{max(moods)}/10")
                    st.metric("Total Check-ins", len(moods))
    else:
        st.info("👈 Add family members in the sidebar to start!")

with tab3:
    st.header("👨‍👩‍👧‍👦 Parent Dashboard")
    
    st.markdown("""
    <div class="parent-dashboard">
        <h3>🔐 Confidential Parent View</h3>
        <p>This dashboard helps parents monitor their children's mental health while respecting privacy.</p>
        <p><strong>Note:</strong> Only data from family members who have enabled sharing is shown.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show children's data
    children_data = {name: data for name, data in family_data['family_members'].items() 
                    if data['role'] == "Child/Teen" and data.get('sharing_enabled', False)}
    
    if children_data:
        for child_name, child_data in children_data.items():
            with st.expander(f"📊 {child_name}'s Mental Health Summary"):
                if child_data.get('mood_history'):
                    moods = [entry['mood'] for entry in child_data['mood_history']]
                    recent_moods = moods[-7:] if len(moods) >= 7 else moods
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Recent Average", f"{sum(recent_moods)/len(recent_moods):.1f}/10")
                    with col2:
                        st.metric("Total Check-ins", len(moods))
                    with col3:
                        last_checkin = child_data['mood_history'][-1]['date'].split()[0]
                        st.metric("Last Check-in", last_checkin)
                    
                    # Trend analysis
                    if len(moods) >= 5:
                        recent_avg = sum(moods[-3:]) / 3
                        overall_avg = sum(moods) / len(moods)
                        
                        if recent_avg < 4:
                            st.error("⚠️ Consider checking in with them - recent moods are concerning.")
                        elif recent_avg > overall_avg + 1:
                            st.success("📈 They seem to be doing better lately!")
                        else:
                            st.info("📊 Mood appears stable.")
                else:
                    st.info("No check-ins yet.")
    else:
        st.info("No children with sharing enabled found.")

with tab4:
    st.header("⚙️ Family Settings")
    
    st.markdown("""
    <div class="privacy-box">
        <h3>🔒 Privacy & Sharing Settings</h3>
        <p>Family mental health requires balancing support with privacy. Configure how data is shared within your family.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Individual member settings
    for member_name, member_data in family_data['family_members'].items():
        with st.expander(f"⚙️ Settings for {member_name}"):
            
            # Sharing settings
            current_sharing = member_data.get('sharing_enabled', False)
            new_sharing = st.checkbox(
                f"Enable family sharing for {member_name}",
                value=current_sharing,
                key=f"sharing_{member_name}",
                help="When enabled, mood data appears in family overview and parent dashboard"
            )
            
            if new_sharing != current_sharing:
                family_data['family_members'][member_name]['sharing_enabled'] = new_sharing
                save_family_data(family_data)
                st.success(f"✅ Updated sharing settings for {member_name}")
                st.rerun()
            
            # Remove member
            if st.button(f"❌ Remove {member_name} from family", key=f"remove_{member_name}"):
                del family_data['family_members'][member_name]
                save_family_data(family_data)
                st.success(f"Removed {member_name} from family")
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">🏠 Family Mental Health Hub • Supporting Every Family Member 💙</p>',
    unsafe_allow_html=True
)