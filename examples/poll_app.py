"""
PH3130 Live Polling System
Streamlit app for creating and running live polls in class
"""

import streamlit as st
import pandas as pd
import json
import qrcode
from io import BytesIO
from datetime import datetime
import plotly.express as px
import base64

# Page config
st.set_page_config(
    page_title="PH3130 Live Polls",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'polls' not in st.session_state:
    st.session_state.polls = {}
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'current_poll' not in st.session_state:
    st.session_state.current_poll = None

# Data persistence helpers
def save_data():
    """Save polls and responses to JSON"""
    with open('polls_data.json', 'w') as f:
        json.dump({
            'polls': st.session_state.polls,
            'responses': st.session_state.responses
        }, f)

def load_data():
    """Load polls and responses from JSON"""
    try:
        with open('polls_data.json', 'r') as f:
            data = json.load(f)
            st.session_state.polls = data.get('polls', {})
            st.session_state.responses = data.get('responses', {})
    except FileNotFoundError:
        pass

# Load data on startup
load_data()

def generate_qr_code(url):
    """Generate QR code for poll URL"""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def get_base_url():
    """Get base URL of the app"""
    try:
        return st.get_option("browser.serverAddress") or "http://localhost:8501"
    except:
        return "http://localhost:8501"

# Sidebar navigation
with st.sidebar:
    st.title("📊 PH3130 Polls")
    page = st.radio("Navigation", ["Admin Panel", "Vote", "Results", "Export Data"])
    
    st.divider()
    st.caption(f"Total polls: {len(st.session_state.polls)}")
    if st.session_state.polls:
        total_responses = sum(len(responses) for responses in st.session_state.responses.values())
        st.caption(f"Total responses: {total_responses}")

# ADMIN PANEL
if page == "Admin Panel":
    st.title("🎛️ Admin Panel")
    st.markdown("Create and manage live polls")
    
    # Create new poll
    with st.expander("➕ Create New Poll", expanded=True):
        with st.form("new_poll_form"):
            poll_id = st.text_input("Poll ID", placeholder="e.g., anxiety, crime, causation")
            poll_title = st.text_input("Poll Title", placeholder="e.g., Statistics Anxiety")
            poll_question = st.text_input("Question", placeholder="How nervous are you about statistics?")
            
            st.markdown("**Options (one per line):**")
            options_text = st.text_area(
                "Options",
                placeholder="A. Very nervous\nB. Somewhat nervous\nC. A little nervous\nD. Not nervous",
                height=150
            )
            
            col1, col2 = st.columns([1, 3])
            with col1:
                submit = st.form_submit_button("Create Poll", type="primary", use_container_width=True)
            with col2:
                if submit:
                    if not poll_id or not poll_question or not options_text:
                        st.error("Please fill all fields")
                    else:
                        options = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
                        st.session_state.polls[poll_id] = {
                            'id': poll_id,
                            'title': poll_title or poll_id,
                            'question': poll_question,
                            'options': options,
                            'created': datetime.now().isoformat(),
                            'active': True
                        }
                        st.session_state.responses[poll_id] = []
                        save_data()
                        st.success(f"✅ Poll '{poll_id}' created!")
                        st.rerun()
    
    st.divider()
    
    # Manage existing polls
    st.subheader("📋 Existing Polls")
    
    if not st.session_state.polls:
        st.info("No polls created yet. Create your first poll above!")
    else:
        for poll_id, poll in st.session_state.polls.items():
            with st.expander(f"**{poll['title']}** ({poll_id})", expanded=False):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Question:** {poll['question']}")
                    st.markdown(f"**Options:**")
                    for opt in poll['options']:
                        st.markdown(f"- {opt}")
                    
                    response_count = len(st.session_state.responses.get(poll_id, []))
                    st.caption(f"📊 {response_count} responses")
                
                with col2:
                    # Generate QR code
                    base_url = get_base_url()
                    vote_url = f"{base_url}?vote={poll_id}"
                    
                    if st.button("Show QR Code", key=f"qr_{poll_id}"):
                        qr_buf = generate_qr_code(vote_url)
                        st.image(qr_buf, caption=f"Scan to vote on {poll_id}", width=200)
                        st.code(vote_url, language=None)
                
                with col3:
                    if st.button("Clear Responses", key=f"clear_{poll_id}"):
                        st.session_state.responses[poll_id] = []
                        save_data()
                        st.success("Responses cleared!")
                        st.rerun()
                    
                    if st.button("Delete Poll", key=f"delete_{poll_id}", type="secondary"):
                        del st.session_state.polls[poll_id]
                        if poll_id in st.session_state.responses:
                            del st.session_state.responses[poll_id]
                        save_data()
                        st.rerun()

# VOTE PAGE
elif page == "Vote":
    st.title("🗳️ Vote on Poll")
    
    # Check for poll ID in URL params
    query_params = st.query_params
    poll_id_from_url = query_params.get("vote", None)
    
    if poll_id_from_url and poll_id_from_url in st.session_state.polls:
        selected_poll = poll_id_from_url
    else:
        # Manual poll selection
        if not st.session_state.polls:
            st.warning("No active polls available")
            st.stop()
        
        poll_options = {f"{p['title']} ({pid})": pid for pid, p in st.session_state.polls.items()}
        selected = st.selectbox("Select a poll:", list(poll_options.keys()))
        selected_poll = poll_options[selected]
    
    poll = st.session_state.polls[selected_poll]
    
    st.markdown(f"### {poll['question']}")
    
    with st.form("vote_form"):
        response = st.radio("Your answer:", poll['options'], index=None)
        
        submitted = st.form_submit_button("Submit Vote", type="primary", use_container_width=True)
        
        if submitted:
            if response is None:
                st.error("Please select an option")
            else:
                # Record response
                st.session_state.responses[selected_poll].append({
                    'response': response,
                    'timestamp': datetime.now().isoformat()
                })
                save_data()
                st.success("✅ Your vote has been recorded!")
                st.balloons()

# RESULTS PAGE
elif page == "Results":
    st.title("📊 Live Results")
    
    if not st.session_state.polls:
        st.warning("No polls available")
        st.stop()
    
    # Auto-refresh toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        poll_options = {f"{p['title']} ({pid})": pid for pid, p in st.session_state.polls.items()}
        selected = st.selectbox("Select poll:", list(poll_options.keys()))
        selected_poll = poll_options[selected]
    
    with col2:
        auto_refresh = st.checkbox("Auto-refresh", value=True)
        if auto_refresh:
            st.caption("Updates every 2s")
    
    poll = st.session_state.polls[selected_poll]
    responses = st.session_state.responses.get(selected_poll, [])
    
    # Display results
    st.markdown(f"### {poll['question']}")
    st.caption(f"Total responses: {len(responses)}")
    
    if not responses:
        st.info("No responses yet. Waiting for votes...")
    else:
        # Count responses
        response_counts = {}
        for opt in poll['options']:
            response_counts[opt] = sum(1 for r in responses if r['response'] == opt)
        
        # Create DataFrame
        df = pd.DataFrame({
            'Option': list(response_counts.keys()),
            'Votes': list(response_counts.values())
        })
        
        # Display bar chart
        fig = px.bar(
            df, 
            x='Option', 
            y='Votes',
            text='Votes',
            title=poll['title'],
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="",
            yaxis_title="Number of Votes"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show percentage breakdown
        total = len(responses)
        st.markdown("#### Response Breakdown")
        for opt, count in response_counts.items():
            percentage = (count / total * 100) if total > 0 else 0
            st.markdown(f"**{opt}:** {count} votes ({percentage:.1f}%)")
    
    # Auto-refresh
    if auto_refresh:
        import time
        time.sleep(2)
        st.rerun()

# EXPORT PAGE
elif page == "Export Data":
    st.title("💾 Export Data")
    
    if not st.session_state.polls:
        st.warning("No data to export")
        st.stop()
    
    st.markdown("Download poll data as CSV for analysis")
    
    for poll_id, poll in st.session_state.polls.items():
        with st.expander(f"{poll['title']} ({poll_id})"):
            responses = st.session_state.responses.get(poll_id, [])
            
            if not responses:
                st.info("No responses to export")
            else:
                # Create DataFrame
                df = pd.DataFrame(responses)
                
                # Display preview
                st.dataframe(df, use_container_width=True)
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"Download {poll_id}.csv",
                    data=csv,
                    file_name=f"{poll_id}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key=f"download_{poll_id}"
                )

# Footer
st.divider()
st.caption("PH3130 Live Polling System | Data Analysis for Public Health")
