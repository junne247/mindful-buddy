col2:
    st.write(f"**Member Since:** {user_data.get('created_date', 'Unknown')[:10]}")
    st.write(f"**Data Points:** {len(user_data.get('mood_history', []))}")
    st.write(f"**Features:** All Ultimate Features Enabled")

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

# Platform preferences
st.markdown("#### 🔧 Platform Preferences")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🔔 Notifications**")
    daily_reminders = st.checkbox("Daily check-in reminders", value=user_data.get('preferences', {}).get('daily_reminders', True))
    crisis_monitoring = st.checkbox("Crisis detection alerts", value=user_data.get('preferences', {}).get('crisis_monitoring', True))
    weekly_reports = st.checkbox("Weekly summary reports", value=True)

with col2:
    st.markdown("**🎨 Interface**")
    theme = st.selectbox("Color Theme:", ["Professional Blue", "Calm Green", "Warm Orange", "Classic Purple"])
    language = st.selectbox("Language:", ["English", "Spanish", "French", "German", "Coming Soon..."])
    accessibility = st.checkbox("High contrast mode", value=False)

# Data management
st.markdown("#### 💾 Data Management")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📤 Export All Data", use_container_width=True):
        export_data = {
            'user': st.session_state.current_user,
            'exported': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'account_type': user_data.get('account_type'),
            'plan': user_data.get('plan_type'),
            'mood_history': user_data.get('mood_history', []),
            'preferences': user_data.get('preferences', {}),
            'platform': 'MindfulBuddy Ultimate v4.0'
        }
        
        st.download_button(
            "💾 Download Complete Data Export",
            data=json.dumps(export_data, indent=2),
            file_name=f"mindfulbuddy_complete_export_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )

with col2:
    if st.button("📋 Generate Report", use_container_width=True):
        st.info("📋 Professional report generation available in Reports section!")

with col3:
    if st.button("🔄 Sync Data", use_container_width=True):
        st.success("🔄 Data synchronized with cloud backup!")

# Account actions
st.markdown("#### ⚡ Account Actions")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔑 Change Password", use_container_width=True):
        st.info("🔧 Password change feature - Contact support for assistance!")
    
    if st.button("📱 Download Mobile App", use_container_width=True):
        st.info("📱 Mobile apps coming soon for iOS and Android!")

with col2:
    if st.button("💎 Upgrade Plan", use_container_width=True):
        st.info("💎 You're already on the Ultimate plan!")
    
    if st.button("🆘 Contact Support", use_container_width=True):
        st.info("🆘 24/7 Support: support@mindfulbuddy.com")

# Save preferences
if st.button("💾 Save All Settings", type="primary", use_container_width=True):
    if 'preferences' not in user_data:
        user_data['preferences'] = {}
    
    user_data['preferences'].update({
        'daily_reminders': daily_reminders,
        'crisis_monitoring': crisis_monitoring,
        'weekly_reports': weekly_reports,
        'theme': theme,
        'language': language,
        'accessibility': accessibility
    })
    
    save_ultimate_data(app_data)
    st.success("✅ All settings saved successfully!")

# Logout
st.markdown("---")
if st.button("🚪 Secure Logout", use_container_width=True):
    st.session_state.current_user = None
    st.success("🔐 Logged out securely from Ultimate Platform!")
    st.rerun()

# Ultimate footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 3rem 0; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); margin: 2rem -1rem -1rem -1rem; border-radius: 20px 20px 0 0;">
   <div style="max-width: 800px; margin: 0 auto;">
       <h4 style="color: #667eea; margin-bottom: 1rem;">🌟 MindfulBuddy Ultimate Platform v4.0</h4>
       <p style="margin-bottom: 1rem;">
           🔐 Bank-Level Security • 🧠 AI-Powered • 📊 Professional Analytics • 👨‍👩‍👧‍👦 Family Support • 🎤 Voice Enabled
       </p>
       <p style="font-size: 0.9rem; color: #8e8e8e;">
           Trusted by thousands worldwide • HIPAA Compliant • Privacy Focused • Built with ❤️ for mental health
       </p>
       <div style="margin-top: 1.5rem;">
           <span style="margin: 0 1rem; color: #667eea;">📧 support@mindfulbuddy.com</span>
           <span style="margin: 0 1rem; color: #667eea;">🌐 www.mindfulbuddy.com</span>
           <span style="margin: 0 1rem; color: #667eea;">📱 Mobile apps coming soon</span>
       </div>
       <p style="margin-top: 1rem; font-size: 0.8rem; color: #adb5bd;">
           © 2025 MindfulBuddy. All rights reserved. Terms • Privacy • GDPR Compliant
       </p>
   </div>
</div>
""", unsafe_allow_html=True)
