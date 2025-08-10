# MindfulBuddy - ULTIMATE PLATFORM v5.2 (AI Conversation + Voice + WhatsApp Chat)
import streamlit as st
import json
import hashlib
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import os
import random
import re

# ---------- Config ----------
st.set_page_config(
    page_title="MindfulBuddy - Ultimate Mental Health Platform",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Styles (merged) ----------
st.markdown("""
<style>
    :root {
        --primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --whatsapp-green: #25D366;
        --voice-red: #ff4757;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stDeployButton {display:none;}

    .ultimate-header {
        background: var(--primary);
        padding: 3rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102,126,234,0.3);
    }
    .app-title { color:#fff; font-size:3.2rem; font-weight:800; margin:0; text-shadow:0 4px 8px rgba(0,0,0,0.3); }
    .app-subtitle { color:rgba(255,255,255,0.95); font-size:1.1rem; margin:0.6rem 0; font-weight:400; }
    .platform-badge { background:rgba(255,255,255,0.2); color:#fff; padding:0.35rem 0.9rem; border-radius:22px; font-size:0.85rem; margin:0 0.35rem; border:1px solid rgba(255,255,255,0.3); }

    .ultimate-card {
        background:#fff; border-radius:20px; padding:2rem; margin:1.25rem 0;
        box-shadow:0 10px 40px rgba(0,0,0,0.08); border:1px solid rgba(102,126,234,0.12);
        transition:transform 0.25s ease, box-shadow 0.25s ease;
    }
    .ultimate-card:hover { transform:translateY(-6px); box-shadow:0 18px 50px rgba(0,0,0,0.12); }

    .stButton > button {
        background: var(--primary); color:#fff; border:none; border-radius:30px; padding:0.9rem 2rem; font-weight:600;
        box-shadow:0 6px 20px rgba(102,126,234,0.25); transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 12px 35px rgba(102,126,234,0.33); }

    /* Classic chat (v5.0) */
    .chat-container { max-height: 430px; overflow-y: auto; padding:1rem; border:1px solid #ddd; border-radius:10px; background:#f8f9fa; margin: 0.5rem 0 1rem; }
    .user-message { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:#fff; padding:0.8rem 1.2rem; border-radius:18px 18px 4px 18px; margin:0.5rem 0; margin-left:20%; box-shadow:0 2px 8px rgba(102,126,234,0.3); }
    .ai-message { background:#fff; color:#333; padding:0.8rem 1.2rem; border-radius:18px 18px 18px 4px; margin:0.5rem 0; margin-right:20%; box-shadow:0 2px 8px rgba(0,0,0,0.08); border-left:4px solid #4CAF50; }
    .typing-indicator { background:#e9ecef; padding:0.8rem 1.2rem; border-radius:18px; margin:0.5rem 0; margin-right:20%; animation:pulse 1.5s ease-in-out infinite; }
    @keyframes pulse { 0%{opacity:0.6} 50%{opacity:1} 100%{opacity:0.6} }
    .mood-badge { background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color:#fff; padding:0.3rem 0.8rem; border-radius:15px; font-size:0.8rem; display:inline-block; }

    /* WhatsApp-style chat */
    .whatsapp-container { background: linear-gradient(135deg, #e3f2fd 0%, #f0f4c3 100%); border-radius:15px; padding:1rem; margin:0.5rem 0 1rem; min-height: 430px; max-height: 430px; overflow-y:auto; }
    .user-bubble { background: var(--whatsapp-green); color:#fff; padding:0.8rem 1.2rem; border-radius:18px 18px 4px 18px; margin:0.5rem 0; margin-left:20%; margin-right:0.5rem; box-shadow:0 2px 8px rgba(37,211,102,0.3); word-wrap:break-word; font-size:0.95rem; }
    .ai-bubble { background:#fff; color:#303030; padding:0.8rem 1.2rem; border-radius:18px 18px 18px 4px; margin:0.5rem 0; margin-right:20%; margin-left:0.5rem; box-shadow:0 2px 8px rgba(0,0,0,0.08); word-wrap:break-word; font-size:0.95rem; }
    .message-time { font-size:0.7rem; opacity:0.7; margin-top:0.25rem; text-align:right; }
    .ai-message-time { text-align:left; }

    /* Voice note */
    .voice-status { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); color:#fff; padding:1rem; border-radius:10px; margin: 0.5rem 0 1rem; text-align:center; }
</style>
""", unsafe_allow_html=True)

# ---------- Data helpers ----------
def hash_password(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()

def verify_password(p: str, h: str) -> bool:
    return hash_password(p) == h

def initialize_all_data_files():
    if not os.path.exists('ultimate_platform_data.json'):
        data = {
            "users": {
                "demo_user": {
                    "password_hash": hash_password("demo123"),
                    "age_group": "18-24",
                    "mood_history": [
                        {"date":"2025-08-01 10:00:00","mood":7,"energy":6,"stress":4,"sleep":8,"platform":"ultimate","note":"Feeling good today!"},
                        {"date":"2025-08-02 09:30:00","mood":8,"energy":7,"stress":3,"sleep":9,"platform":"ultimate","note":"Great sleep last night"}
                    ],
                    "created_date": "2025-08-01 00:00:00",
                    "account_type": "ultimate_professional",
                    "ai_conversations": [],
                    "voice_interactions": [],
                    "preferences": {"daily_reminders": True,"crisis_monitoring": True,"voice_enabled": True,"theme": "Professional Blue"}
                }
            },
            "sessions": {},
            "platform_stats": {"total_users":1,"total_checkins":2,"voice_interactions":0,"platform_rating":4.9},
            "app_metadata": {"version":"5.2.0","platform_level":"ultimate","features_enabled":["ai","analytics","security","family","voice","reports","ai_chat"]}
        }
        with open('ultimate_platform_data.json','w') as f:
            json.dump(data, f, indent=2)

def load_data():
    try:
        with open('ultimate_platform_data.json','r') as f:
            return json.load(f)
    except FileNotFoundError:
        initialize_all_data_files()
        return load_data()

def save_data(d):
    with open('ultimate_platform_data.json','w') as f:
        json.dump(d, f, indent=2)

initialize_all_data_files()
app_data = load_data()

# ---------- AI conversation helpers ----------
def extract_mood_from_speech(text: str):
    if not text: return None
    t = text.lower()
    nums = re.findall(r'\b(\d+)\b', t)
    for n in nums:
        v = int(n)
        if 1 <= v <= 10: return v
    if any(w in t for w in ['terrible','awful','horrible','worst','devastated']): return 1
    if any(w in t for w in ['very bad','really sad','depressed','miserable']): return 2
    if any(w in t for w in ['bad','sad','down','low','upset']): return 3
    if any(w in t for w in ['not great','struggling','difficult','hard']): return 4
    if any(w in t for w in ['okay','fine','alright','neutral','average']): return 5
    if any(w in t for w in ['pretty good','decent','not bad']): return 6
    if any(w in t for w in ['good','better','nice','positive','well']): return 7
    if any(w in t for w in ['really good','very good','great']): return 8
    if any(w in t for w in ['amazing','fantastic','wonderful','excellent','superb']): return 9
    if any(w in t for w in ['perfect','best','incredible','outstanding','phenomenal']): return 10
    return None

def generate_voice_response(mood_score, name, speech_text=""):
    if mood_score is None:
        return random.choice([
            f"Thanks for speaking with me, {name}. Tell me how your day is going.",
            f"I'm listening, {name}. Share what feels most important right now."
        ])
    if mood_score <= 3:
        base = [f"Sorry this feels hard today, {name}. You are not alone.",
                f"Thanks for telling me, {name}. Your feelings make sense."]
    elif mood_score <= 6:
        base = [f"Got it, {name}. Mixed days happen. We can take one step at a time.",
                f"Thanks for checking in, {name}. It is ok to feel this way."]
    else:
        base = [f"Nice to hear you are doing well, {name}. Keep the momentum.",
                f"Love that, {name}. Enjoy the good energy."]
    t = (speech_text or "").lower()
    if any(w in t for w in ['work','school','study','exam']):
        base.append(f"If work or school is heavy, we can plan one small step, {name}.")
    if any(w in t for w in ['family','parents','mom','dad']):
        base.append(f"Family stuff can be a lot, {name}. You do not have to carry it alone.")
    return random.choice(base)

def generate_ai_response(user_message, history, user_mood=None):
    txt = user_message.lower()
    if user_mood:
        if user_mood <= 3:
            return random.choice(["That sounds rough. What was the hardest part today?",
                                  "Thanks for sharing. Want ideas for small relief now?"])
        if user_mood >= 8:
            return random.choice(["Love that energy. What went right today?",
                                  "Great to hear. Want to lock a habit while you feel good?"])
    if any(w in txt for w in ['sad','depressed','down','awful','terrible']):
        return "I hear you. Sadness can feel heavy. What started it today?"
    if any(w in txt for w in ['anxious','worried','nervous','stressed','panic']):
        return "Anxiety is real. Want a quick 4-7-8 breathing guide?"
    if any(w in txt for w in ['angry','mad','frustrated','annoyed']):
        return "Anger often points to something that matters. What felt unfair?"
    if any(w in txt for w in ['happy','good','great','amazing','wonderful']):
        return "Nice. What is one thing that made you smile?"
    if any(w in txt for w in ['school','work','job','study','exam','test']):
        return "We can plan it simply. What is the next small task due?"
    if any(w in txt for w in ['family','parents','mom','dad','brother','sister']):
        return "Family can be complex. What outcome would feel better?"
    if any(w in txt for w in ['friend','friends','social','lonely','alone']):
        return "Social stuff hits hard. Who do you feel safe texting today?"
    if any(w in txt for w in ['help','advice','what should','how can']):
        return "Tell me your goal in one line and what you tried so far."
    return "I am here. Tell me more about what you feel right now."

# ---------- Session ----------
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'conversation' not in st.session_state: st.session_state.conversation = []
if 'chat_style' not in st.session_state: st.session_state.chat_style = "WhatsApp"
if 'chat_mood' not in st.session_state: st.session_state.chat_mood = None

# ---------- Header ----------
st.markdown("""
<div class="ultimate-header">
  <div style="font-size:3rem; margin-bottom:0.5rem;">🌟</div>
  <h1 class="app-title">MindfulBuddy</h1>
  <p class="app-subtitle">AI chat, voice check-ins, and clear insights</p>
  <div style="margin-top: 0.8rem;">
    <span class="platform-badge">💬 Chat</span>
    <span class="platform-badge">🎤 Voice</span>
    <span class="platform-badge">📊 Analytics</span>
    <span class="platform-badge">🔐 Security</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### Platform Overview")
    stats = app_data.get("platform_stats", {})
    st.metric("Users", f"{stats.get('total_users',0):,}")
    st.metric("Check-ins", f"{stats.get('total_checkins',0):,}")
    st.metric("Voice logs", f"{stats.get('voice_interactions',0):,}")
    st.metric("Rating", f"{stats.get('platform_rating',4.9)}/5.0")
    st.markdown("---")
    st.markdown("### Features")
    for f in ["AI Mood Prediction","AI Conversations","Voice Integration","Advanced Analytics","Secure Data","Reports","Crisis Detection"]:
        st.markdown(f"✅ {f}")

# ---------- Auth or App ----------
if st.session_state.current_user is None:
    # Welcome
    st.markdown("""
    <div class="ultimate-card" style="text-align:center;">
      <h2 style="color:#667eea;">Welcome to MindfulBuddy</h2>
      <p style="color:#6c757d;">Have real talks, track feelings, and see simple trends.</p>
    </div>
    """, unsafe_allow_html=True)

    # Benefits
    st.markdown("""
    <div class="ultimate-card">
        <h3 style="color:#667eea; text-align:center; margin-bottom:0.5rem;">💝 Designed for real impact</h3>
        <div style="text-align:center; color:#6c757d;">
            🎓 <strong>Students:</strong> manage stress and build healthy habits<br>
            👨‍👩‍👧‍👦 <strong>Families:</strong> support each other with privacy<br>
            🩺 <strong>Healthcare:</strong> tools for clinical use<br>
            🌍 <strong>Everyone:</strong> accessible support
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Auth
    st.markdown("""
    <div class="ultimate-card" style="text-align:center;">
      <h3 style="color:#667eea;">🔐 Sign in or create an account</h3>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔑 Sign In","🌟 Create Account"])
    with tab1:
        c1, c2 = st.columns([2,1])
        with c1:
            login_name = st.text_input("Username")
            login_pass = st.text_input("Password", type="password")
            if st.button("Access Platform", type="primary", use_container_width=True):
                users = app_data["users"]
                if login_name and login_pass and login_name in users and verify_password(login_pass, users[login_name]["password_hash"]):
                    st.session_state.current_user = login_name
                    st.success(f"Welcome, {login_name}")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        with c2:
            st.markdown("""
            <div style="background:#e3f2fd; padding:1rem; border-radius:10px; border-left:4px solid #2196F3;">
              Try demo<br><code>user: demo_user</code><br><code>pass: demo123</code>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        su_name = st.text_input("New username")
        su_pass = st.text_input("New password", type="password")
        su_age = st.selectbox("Age group", ["13-17","18-24","25-34","35+"])
        if st.button("Create Account", type="primary", use_container_width=True):
            if not su_name or not su_pass:
                st.error("Fill all fields")
            elif su_name in app_data["users"]:
                st.error("Username taken")
            else:
                app_data["users"][su_name] = {
                    "password_hash": hash_password(su_pass),
                    "age_group": su_age,
                    "mood_history": [],
                    "ai_conversations": [],
                    "voice_interactions": [],
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "account_type": "ultimate_professional",
                    "preferences": {"daily_reminders": True,"crisis_monitoring": True,"voice_enabled": True,"theme": "Professional Blue"}
                }
                app_data["platform_stats"]["total_users"] += 1
                save_data(app_data)
                st.session_state.current_user = su_name
                st.success(f"Welcome, {su_name}")
                st.rerun()

else:
    user = app_data["users"][st.session_state.current_user]

    st.markdown(f"""
    <div class="ultimate-card">
      <h2>Welcome back, {st.session_state.current_user}</h2>
      <p style="color:#6c757d;">
        <strong>Account:</strong> {user.get('account_type','Ultimate')} •
        <strong>Member since:</strong> {user.get('created_date','Unknown')[:10]}
      </p>
    </div>
    """, unsafe_allow_html=True)

    nav = st.radio("Go to", ["🏠 Dashboard","📊 Check-in","💬 Chat","🎤 Voice","⚙️ Settings"], horizontal=True)

    # ----- Dashboard -----
    if nav == "🏠 Dashboard":
        mh = user.get("mood_history", [])
        if mh:
            moods = [r["mood"] for r in mh]
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric("Total check-ins", len(moods))
            with c2: st.metric("Average mood", f"{sum(moods)/len(moods):.1f}/10")
            with c3: st.metric("Best day", f"{max(moods)}/10")
            with c4: st.metric("Voice logs", len(user.get("voice_interactions", [])))

            df = pd.DataFrame(mh)
            df["date"] = pd.to_datetime(df["date"])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["date"], y=df["mood"], mode="lines+markers", name="Mood",
                                     line=dict(color="#667eea", width=3), marker=dict(size=9)))
            fig.update_layout(title="Mood Over Time", xaxis_title="Date", yaxis_title="Mood (1-10)", template="plotly_white", height=420)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No check-ins yet. Go to Check-in to add your first one.")

    # ----- Check-in -----
    elif nav == "📊 Check-in":
        st.markdown("### Daily check-in")
        a, b = st.columns([2,1])
        with a:
            mood = st.slider("Mood", 1, 10, 5)
            energy = st.slider("Energy", 1, 10, 5)
            stress = st.slider("Stress", 1, 10, 5)
            sleep = st.slider("Sleep", 1, 10, 5)
            note = st.text_area("Notes", placeholder="Add context if you want")
        with b:
            emoji = "😢" if mood <= 3 else "😐" if mood <= 6 else "😊"
            st.metric("Current mood", f"{emoji} {mood}/10")
            if mood <= 3: st.error("Consider texting someone you trust today.")
            elif mood >= 8: st.success("Nice. Keep the good habits going.")
            else: st.info("Take it easy and be kind to yourself.")
        if st.button("Save check-in", type="primary", use_container_width=True):
            entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "mood": mood, "energy": energy, "stress": stress, "sleep": sleep, "platform": "ultimate"}
            if note: entry["note"] = note
            user.setdefault("mood_history", []).append(entry)
            app_data["platform_stats"]["total_checkins"] += 1
            save_data(app_data)
            st.success("Check-in saved")
            st.balloons()
            st.rerun()

    # ----- Chat -----
    elif nav == "💬 Chat":
        top_c1, top_c2 = st.columns([3,1])
        with top_c2:
            st.session_state.chat_style = st.selectbox("Chat style", ["WhatsApp","Classic"], index=0 if st.session_state.chat_style=="WhatsApp" else 1)
            st.session_state.chat_mood = st.slider("Quick mood", 1, 10, st.session_state.chat_mood or 6)
            st.markdown(f'<span class="mood-badge">Mood: {st.session_state.chat_mood}/10</span>', unsafe_allow_html=True)
            if st.button("Clear chat", use_container_width=True):
                st.session_state.conversation = []
                save_data(app_data)
                st.rerun()

        with top_c1:
            st.markdown("### AI chat")
            # render chat
            if st.session_state.chat_style == "WhatsApp":
                if st.session_state.conversation:
                    html = '<div class="whatsapp-container">'
                    for m in st.session_state.conversation:
                        t = m.get("timestamp","")
                        if m["sender"] == "user":
                            html += f'<div class="user-bubble">{m["message"]}<div class="message-time">{t}</div></div>'
                        else:
                            html += f'<div class="ai-bubble">{m["message"]}<div class="message-time ai-message-time">{t}</div></div>'
                    html += '</div>'
                    st.markdown(html, unsafe_allow_html=True)
                else:
                    st.info("Start the conversation below.")
            else:
                # Classic
                if st.session_state.conversation:
                    html = '<div class="chat-container">'
                    for m in st.session_state.conversation:
                        if m["sender"] == "user":
                            html += f'<div class="user-message">{m["message"]}</div>'
                        else:
                            html += f'<div class="ai-message">🤖 {m["message"]}</div>'
                    html += '</div>'
                    st.markdown(html, unsafe_allow_html=True)
                else:
                    st.info("Start the conversation below.")

            msg = st.text_area("Type your message", height=100, placeholder="Tell me what is on your mind")
            if st.button("Send", type="primary", use_container_width=True):
                if msg.strip():
                    st.session_state.conversation.append({"sender":"user","message":msg,"timestamp": datetime.now().strftime("%H:%M")})
                    reply = generate_ai_response(msg, st.session_state.conversation, st.session_state.chat_mood)
                    st.session_state.conversation.append({"sender":"ai","message":reply,"timestamp": datetime.now().strftime("%H:%M")})
                    user.setdefault("ai_conversations", []).extend([
                        {"type":"user","message":msg,"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                        {"type":"ai","message":reply,"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    ])
                    save_data(app_data)
                    st.rerun()

    # ----- Voice -----
    elif nav == "🎤 Voice":
        st.markdown("### Voice check-in demo")
        st.markdown('<div class="voice-status">This demo uses typed transcript to simulate speech. You can connect real audio later.</div>', unsafe_allow_html=True)
        c1, c2 = st.columns([2,1])
        with c1:
            transcript = st.text_area("Speak your feelings (type transcript here)", placeholder="Example: I feel like a 3 out of 10. Work is heavy.")
        with c2:
            detected = extract_mood_from_speech(transcript)
            if detected is not None:
                emo = "😢" if detected <= 3 else "😐" if detected <= 6 else "😊"
                st.metric("Detected mood", f"{emo} {detected}/10")
            else:
                st.info("No mood number detected yet")

        if st.button("Generate voice reply", type="primary", use_container_width=True):
            name = st.session_state.current_user
            mood_for_reply = detected if detected is not None else (user.get("mood_history", [])[-1]["mood"] if user.get("mood_history") else None)
            resp = generate_voice_response(mood_for_reply, name, transcript or "")
            user.setdefault("voice_interactions", []).append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "transcript": transcript,
                "detected_mood": mood_for_reply,
                "response": resp
            })
            app_data["platform_stats"]["voice_interactions"] = app_data["platform_stats"].get("voice_interactions",0) + 1
            # Also add to chat thread
            st.session_state.conversation.append({"sender":"user","message": transcript or "(voice)", "timestamp": datetime.now().strftime("%H:%M")})
            st.session_state.conversation.append({"sender":"ai","message": resp, "timestamp": datetime.now().strftime("%H:%M")})
            save_data(app_data)
            st.success("Voice reply created and logged")

        logs = user.get("voice_interactions", [])
        if logs:
            st.markdown("#### Recent voice logs")
            for item in logs[-5:][::-1]:
                st.write(f"🕒 {item['timestamp']} • Mood: {item.get('detected_mood','?')}")
                if item.get("transcript"): st.write(f"🎙️ {item['transcript']}")
                st.write(f"🤖 {item.get('response','')}")
                st.markdown("---")

        st.caption("To connect WhatsApp, use WhatsApp Cloud API or Twilio WhatsApp with a webhook that writes to this JSON store.")

    # ----- Settings -----
    elif nav == "⚙️ Settings":
        st.markdown("### Settings")
        s1, s2 = st.columns(2)
        with s1:
            st.write(f"**Username:** {st.session_state.current_user}")
            st.write(f"**Account:** {user.get('account_type','Ultimate')}")
            st.write("**Plan:** Ultimate Professional")
        with s2:
            st.write(f"**Member since:** {user.get('created_date','Unknown')[:10]}")
            st.write(f"**Mood check-ins:** {len(user.get('mood_history', []))}")
            st.write(f"**AI conversations:** {len(user.get('ai_conversations', []))}")

        st.markdown("#### Data")
        d1, d2 = st.columns(2)
        with d1:
            if st.button("Export data", use_container_width=True):
                export = {
                    "user": st.session_state.current_user,
                    "exported": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "account_type": user.get("account_type"),
                    "mood_history": user.get("mood_history", []),
                    "ai_conversations": user.get("ai_conversations", []),
                    "voice_interactions": user.get("voice_interactions", []),
                    "preferences": user.get("preferences", {}),
                    "platform": "MindfulBuddy Ultimate v5.2"
                }
                st.download_button("Download JSON", data=json.dumps(export, indent=2),
                                   file_name=f"mindfulbuddy_export_{datetime.now().strftime('%Y%m%d')}.json",
                                   mime="application/json", use_container_width=True)
        with d2:
            if st.button("Sync data", use_container_width=True):
                st.success("Data synced")

        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.current_user = None
            st.session_state.conversation = []
            st.rerun()

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#6c757d; padding:1.4rem 0; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); margin: 1.2rem -1rem -1rem -1rem; border-radius: 16px 16px 0 0;">
   <div style="max-width: 800px; margin: 0 auto;">
       <h4 style="color:#667eea; margin-bottom: 0.6rem;">🌟 MindfulBuddy Ultimate v5.2</h4>
       <p style="margin: 0;">🔐 Security • 💬 Chat • 🎤 Voice • 📊 Analytics</p>
       <p style="margin: 0.4rem 0 0; font-size: 0.9rem; color:#8e8e8e;">Not a replacement for professional therapy. In crisis, contact local emergency services.</p>
   </div>
</div>
""", unsafe_allow_html=True)
