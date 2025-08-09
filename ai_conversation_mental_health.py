# MindfulBuddy - AI CONVERSATION VERSION v5.0
import streamlit as st
import json
import hashlib
from datetime import datetime
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="MindfulBuddy - AI Conversation Platform",
    page_icon="🤖",
    layout="wide"
)

# CSS for chat interface
st.markdown("""
<style>
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background: #f8f9fa;
        margin: 1rem 0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0;
        margin-left: 20%;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .ai-message {
        background: white;
        color: #333;
        padding: 0.8rem 1.2rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 0;
        margin-right: 20%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
    }
    
    .typing-indicator {
        background: #e9ecef;
        padding: 0.8rem 1.2rem;
        border-radius: 18px;
        margin: 0.5rem 0;
        margin-right: 20%;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .mood-badge {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# AI Response Functions
def generate_ai_response(user_message, conversation_history, user_mood=None):
    """Generate contextual AI responses based on conversation and mood"""
    
    user_message_lower = user_message.lower()
    
    # Mood-based responses
    if user_mood:
        if user_mood <= 3:
            return generate_supportive_response(user_message, conversation_history)
        elif user_mood >= 8:
            return generate_encouraging_response(user_message, conversation_history)
    
    # Context-aware responses based on keywords
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
    """Responses for low mood situations"""
    responses = [
        "I can hear that you're going through a really tough time right now. That takes courage to share. What's been the hardest part of your day?",
        "Thank you for trusting me with how you're feeling. When you're feeling this low, sometimes just getting through the day is an achievement. What's one small thing that might help you feel even slightly better?",
        "I'm sorry you're struggling so much today. Your feelings are completely valid. Have you been able to talk to anyone else about this, or would you like some suggestions for support?",
        "It sounds like today has been really challenging. Sometimes when we feel this low, it helps to remember that feelings change, even when it doesn't feel like they will. What usually helps you when you're feeling down?",
        "I want you to know that reaching out when you feel this way shows real strength. You don't have to go through this alone. Is there anything specific that's been weighing on your mind?"
    ]
    
    # Consider conversation history for more context
    if len(history) > 2:
        if any('school' in msg['message'].lower() for msg in history[-3:]):
            return "I remember you mentioned school earlier. Academic pressure can really weigh us down. It's okay to feel overwhelmed - you're dealing with a lot. What's the biggest source of stress for you right now?"
    
    import random
    return random.choice(responses)

def generate_empathetic_response(message, history):
    """Responses for sadness and depression"""
    responses = [
        "I hear the sadness in your words, and I want you to know that what you're feeling matters. Sadness can feel so heavy sometimes. Can you tell me more about what's contributing to these feelings?",
        "Thank you for sharing something so personal with me. Depression and sadness can make everything feel more difficult. Have you noticed if there are certain times of day or situations that feel particularly hard?",
        "When we're feeling depressed, it can seem like the sadness will never end. But feelings do change, even when we can't see it. What's one thing that has helped you feel even a little bit better in the past?",
        "I can sense how much pain you're in right now. Sometimes when we're sad, it helps to just acknowledge the feeling instead of fighting it. What do you think your sadness is trying to tell you?",
        "Feeling this low is exhausting, isn't it? You're being incredibly brave by talking about it. Is this something you've been dealing with for a while, or is this a newer feeling?"
    ]
    
    import random
    return random.choice(responses)

def generate_calming_response(message, history):
    """Responses for anxiety and stress"""
    responses = [
        "I can sense the anxiety in what you're sharing. Anxiety can make our minds race and our bodies feel tense. Let's take this one step at a time. What's the main thing that's making you feel anxious right now?",
        "Anxiety can be so overwhelming, can't it? Your nervous system is trying to protect you, but sometimes it can feel like too much. Have you tried any breathing exercises, or would you like me to guide you through one?",
        "When we're stressed, everything can feel urgent and overwhelming. It's okay to feel this way - you're dealing with real pressures. What would it look like to tackle just one small thing today?",
        "I hear how worried you are. Sometimes anxiety makes us imagine worst-case scenarios. Can we talk about what's actually happening right now versus what you're worried might happen?",
        "Stress has a way of making everything feel more intense, doesn't it? You're not alone in feeling this way. What's been your biggest source of stress lately?"
    ]
    
    # Add breathing exercise offer
    if 'panic' in message.lower() or 'can\'t breathe' in message.lower():
        return "It sounds like you might be having a panic attack. That's really scary, but you're going to be okay. Try breathing with me: breathe in for 4 counts, hold for 4, breathe out for 6. Would you like me to guide you through this?"
    
    import random
    return random.choice(responses)

def generate_understanding_response(message, history):
    """Responses for anger and frustration"""
    responses = [
        "I can hear the frustration in your words. Anger often shows up when we feel like things are unfair or out of our control. What's making you feel most frustrated right now?",
        "It sounds like you're really angry about something, and that's completely understandable. Anger is often a signal that something important to us has been threatened or hurt. Can you help me understand what's behind these feelings?",
        "Frustration can be so intense, especially when we feel like we're not being heard or understood. Your anger makes sense. What would you need to feel more in control of this situation?",
        "When we're mad, it can feel like everything is wrong at once. Sometimes anger is protecting other feelings underneath. Besides the anger, what else might you be feeling?",
        "I hear how upset you are. Anger can actually be really useful information about what matters to us. What do you think your anger is trying to tell you?"
    ]
    
    import random
    return random.choice(responses)

def generate_positive_response(message, history):
    """Responses for good moods"""
    responses = [
        "I love hearing the joy in your words! It's wonderful when we have these good moments. What's been the highlight of your day?",
        "You sound really happy, and that just brightens my day too! Good moods can be so energizing. What's contributing to you feeling so good?",
        "It's beautiful to hear you feeling so positive! These good feelings are worth celebrating. What would you like to do with this positive energy?",
        "Your happiness is contagious! It's amazing how good moods can make everything seem more possible. What's been going particularly well for you?",
        "I can feel the positivity radiating from your message! When we feel this good, it's worth taking a moment to really appreciate it. What are you most grateful for today?"
    ]
    
    import random
    return random.choice(responses)

def generate_academic_support_response(message, history):
    """Responses for school/work stress"""
    responses = [
        "School stress is so real and valid. Academic pressure can feel overwhelming, especially when it feels like there's always more to do. What's your biggest challenge with school right now?",
        "Work and study stress can really take a toll on our mental health. It sounds like you're carrying a heavy load. What would it look like to make things feel more manageable?",
        "I hear you're dealing with academic pressure. It's tough when it feels like there's so much riding on your performance. How are you taking care of yourself during this stressful time?",
        "School can be incredibly demanding, can't it? Sometimes we put so much pressure on ourselves to be perfect. What would 'good enough' look like for you right now?",
        "Academic stress affects so many people, and it's completely understandable. What's the most overwhelming part - the workload, the pressure, or something else?"
    ]
    
    import random
    return random.choice(responses)

def generate_family_support_response(message, history):
    """Responses for family issues"""
    responses = [
        "Family relationships can be some of the most complicated and emotionally charged relationships we have. It sounds like there's something difficult happening with your family. Can you tell me more?",
        "Family dynamics can be really challenging, especially when we're trying to figure out our own identity and independence. What's been the most difficult part about your family situation?",
        "I hear that something's going on with your family. Family stress can feel particularly intense because these are people we love and live with. How has this been affecting you?",
        "Family relationships have such a big impact on how we feel, don't they? It's okay if things are complicated or difficult right now. What would support look like for you in this situation?",
        "Family issues can feel so personal and overwhelming. You're not alone in struggling with family dynamics. What's been weighing on you most about your family lately?"
    ]
    
    import random
    return random.choice(responses)

def generate_social_support_response(message, history):
    """Responses for friendship and social issues"""
    responses = [
        "Social connections are so important for our wellbeing, and it sounds like you're dealing with something challenging in that area. Friendship issues can be really painful. What's been going on?",
        "I hear you're struggling with something social. Whether it's feeling lonely or having friend drama, these kinds of issues can really affect our mood. Can you tell me more about what's happening?",
        "Social situations can be so complex, can't they? It sounds like there's something weighing on you about your relationships or social life. What's been the hardest part?",
        "Feeling lonely or having friendship problems can be incredibly isolating. Your feelings about this are completely valid. What kind of social connection are you most missing right now?",
        "Social stress can be just as real as any other kind of stress. It sounds like something's been difficult for you socially. How has this been affecting your day-to-day life?"
    ]
    
    import random
    return random.choice(responses)

def generate_advice_response(message, history):
    """Responses when user asks for advice"""
    responses = [
        "I'm honored that you're asking for my perspective. Before I share some thoughts, can you tell me more about the specific situation? The more I understand, the better I can help.",
        "I'd love to help you think through this. Sometimes it helps to start by clarifying what outcome you're hoping for. What would 'success' look like in this situation?",
        "That's a really thoughtful question. I find that the best advice is usually collaborative - what have you already tried, and what are you thinking might help?",
        "I appreciate you trusting me with this question. Let me ask you something first: what does your gut instinct tell you about this situation?",
        "I'm glad you're reaching out for support with this. Sometimes talking through the situation can help us see new possibilities. Can you walk me through what's been happening?"
    ]
    
    import random
    return random.choice(responses)

def generate_general_response(message, history):
    """General conversational responses"""
    responses = [
        "I'm listening and I'm here with you. Can you tell me more about what's on your mind today?",
        "Thank you for sharing that with me. I can sense there's more to the story. What else would you like to talk about?",
        "I hear you. Sometimes it helps just to have someone listen. What's been the most significant thing that's happened to you lately?",
        "I'm glad you're taking the time to check in with yourself and talk about how you're feeling. What's been occupying your thoughts recently?",
        "It sounds like you have a lot going on. I'm here to listen and support you however I can. What feels most important to talk about right now?"
    ]
    
    import random
    return random.choice(responses)

# Data functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_conversation_data():
    try:
        with open('conversation_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            'users': {},
            'conversations': {}
        }

def save_conversation_data(data):
    with open('conversation_data.json', 'w') as file:
        json.dump(data, file, indent=2)

# Main app
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; margin: -1rem -1rem 2rem -1rem; text-align: center; color: white;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
    <h1 style="margin: 0; font-size: 2.5rem;">MindfulBuddy AI Conversations</h1>
    <p style="margin: 0.5rem 0; font-size: 1.1rem;">Have real conversations about your mental health with AI</p>
</div>
""", unsafe_allow_html=True)

# Load data
app_data = load_conversation_data()

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'current_mood' not in st.session_state:
    st.session_state.current_mood = None

# Authentication
if st.session_state.current_user is None:
    st.markdown("### 🤖 Start Your AI Conversation")
    
    tab1, tab2 = st.tabs(["🔑 Login", "➕ New User"])
    
    with tab1:
        login_name = st.text_input("Username:", key="login")
        login_password = st.text_input("Password:", type="password", key="login_pass")
        
        if st.button("💬 Start Conversation", type="primary"):
            if login_name and login_password:
                if login_name in app_data['users'] and app_data['users'][login_name]['password_hash'] == hash_password(login_password):
                    st.session_state.current_user = login_name
                    if login_name in app_data['conversations']:
                        st.session_state.conversation = app_data['conversations'][login_name]
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with tab2:
        signup_name = st.text_input("Choose Username:", key="signup")
        signup_password = st.text_input("Create Password:", type="password", key="signup_pass")
        
        if st.button("🤖 Create AI Account", type="primary"):
            if signup_name and signup_password and signup_name not in app_data['users']:
                app_data['users'][signup_name] = {
                    'password_hash': hash_password(signup_password),
                    'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                app_data['conversations'][signup_name] = []
                save_conversation_data(app_data)
                st.session_state.current_user = signup_name
                st.session_state.conversation = []
                st.success(f"Welcome, {signup_name}! Let's start talking.")
                st.rerun()

else:
    # Main conversation interface
    user_name = st.session_state.current_user
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### 💬 Conversation with AI - {user_name}")
        
        # Display conversation
        chat_html = '<div class="chat-container">'
        
        for msg in st.session_state.conversation:
            if msg['sender'] == 'user':
                chat_html += f'<div class="user-message">{msg["message"]}</div>'
            else:
                chat_html += f'<div class="ai-message">🤖 {msg["message"]}</div>'
        
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
        
        # Message input
        user_message = st.text_area("💬 Talk to your AI therapist:", height=100, placeholder="Share what's on your mind... I'm here to listen and support you.")
        
        col1_1, col1_2 = st.columns([3, 1])
        
        with col1_1:
            if st.button("📤 Send Message", type="primary", use_container_width=True):
                if user_message:
                    # Add user message
                    st.session_state.conversation.append({
                        'sender': 'user',
                        'message': user_message,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # Generate AI response
                    ai_response = generate_ai_response(user_message, st.session_state.conversation, st.session_state.current_mood)
                    
                    # Add AI response
                    st.session_state.conversation.append({
                        'sender': 'ai',
                        'message': ai_response,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # Save conversation
                    app_data['conversations'][user_name] = st.session_state.conversation
                    save_conversation_data(app_data)
                    
                    st.rerun()
        
        with col1_2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.conversation = []
                app_data['conversations'][user_name] = []
                save_conversation_data(app_data)
                st.rerun()
    
    with col2:
        st.markdown("### 📊 Quick Mood Check")
        
        current_mood = st.slider("How are you feeling?", 1, 10, 5, key="mood_slider")
        
        if current_mood != st.session_state.current_mood:
            st.session_state.current_mood = current_mood
            
            mood_colors = {
                1: "🔴", 2: "🟠", 3: "🟠", 4: "🟡", 5: "🟡",
                6: "🟢", 7: "🟢", 8: "🟢", 9: "🔵", 10: "🟣"
            }
            
            st.markdown(f'<div class="mood-badge">{mood_colors[current_mood]} Mood: {current_mood}/10</div>', unsafe_allow_html=True)
        
        st.markdown("### 🤖 AI Features")
        st.markdown("""
        - 💬 **Natural conversation**
        - 🧠 **Context awareness**
        - 🎯 **Mood-based responses**
        - 💙 **Empathetic listening**
        - 🔗 **Conversation memory**
        - 🆘 **Crisis support**
        """)
        
        st.markdown("### 📋 Conversation Stats")
        if st.session_state.conversation:
            user_messages = len([m for m in st.session_state.conversation if m['sender'] == 'user'])
            ai_messages = len([m for m in st.session_state.conversation if m['sender'] == 'ai'])
            st.metric("Messages Exchanged", user_messages + ai_messages)
            st.metric("Your Messages", user_messages)
            st.metric("AI Responses", ai_messages)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.current_user = None
            st.session_state.conversation = []
            st.session_state.current_mood = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p><strong>🤖 MindfulBuddy AI Conversations</strong></p>
    <p>Powered by advanced conversational AI • Your privacy is protected • Not a replacement for professional therapy</p>
</div>
""", unsafe_allow_html=True)