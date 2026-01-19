import streamlit as st
import pandas as pd
import json
import qrcode
from io import BytesIO
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_title="Live Polls",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'polls' not in st.session_state:
    st.session_state.polls = {}
if 'responses' not in st.session_state:
    st.session_state.responses = {}

def save_data():
    with open('polls_data.json', 'w') as f:
        json.dump({
            'polls': st.session_state.polls,
            'responses': st.session_state.responses
        }, f)

def load_data():
    try:
        with open('polls_data.json', 'r') as f:
            data = json.load(f)
            st.session_state.polls = data.get('polls', {})
            st.session_state.responses = data.get('responses', {})
    except FileNotFoundError:
        pass

def load_secrets():
    if 'polls' in st.secrets:
        for poll_id, poll_data in st.secrets['polls'].items():
            if poll_id not in st.session_state.polls:
                st.session_state.polls[poll_id] = {
                    'id': poll_id,
                    'title': poll_data.get('title', poll_id),
                    'question': poll_data.get('question', ''),
                    'options': list(poll_data.get('options', [])),
                    'course': poll_data.get('course', ''),
                    'week': poll_data.get('week', ''),
                    'created': datetime.now().isoformat(),
                    'active': True
                }
                if poll_id not in st.session_state.responses:
                    st.session_state.responses[poll_id] = []

load_data()
load_secrets()

def generate_qr(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def get_base_url():
    try:
        if 'STREAMLIT_SHARING_MODE' in st.secrets or st.runtime.exists():
            return "https://class-polling.streamlit.app"
    except:
        pass
    return "http://localhost:8501"

query_params = st.query_params
vote_poll_id = query_params.get("vote", None)

with st.sidebar:
    st.title("📊 Live Polls")
    if vote_poll_id and vote_poll_id in st.session_state.polls:
        page = "Vote"
        st.info(f"Voting on: {st.session_state.polls[vote_poll_id]['title']}")
    else:
        page = st.radio("Navigation", ["Admin", "Vote", "Results", "Export"])
    st.divider()
    st.caption(f"Polls: {len(st.session_state.polls)}")
    if st.session_state.polls:
        total = sum(len(r) for r in st.session_state.responses.values())
        st.caption(f"Responses: {total}")

if page == "Admin":
    st.title("🎛️ Admin Panel")
    
    with st.expander("➕ Create Poll", expanded=True):
        with st.form("new_poll"):
            poll_id = st.text_input("Poll ID", placeholder="anxiety")
            poll_title = st.text_input("Title", placeholder="Statistics Anxiety")
            poll_question = st.text_input("Question", placeholder="How nervous are you?")
            options = st.text_area("Options (one per line)", height=100)
            
            if st.form_submit_button("Create", type="primary"):
                if poll_id and poll_question and options:
                    opts = [o.strip() for o in options.split('\n') if o.strip()]
                    st.session_state.polls[poll_id] = {
                        'id': poll_id,
                        'title': poll_title or poll_id,
                        'question': poll_question,
                        'options': opts,
                        'created': datetime.now().isoformat(),
                        'active': True
                    }
                    st.session_state.responses[poll_id] = []
                    save_data()
                    st.success(f"✅ Created {poll_id}")
                    st.rerun()
    
    st.divider()
    st.subheader("📋 Polls")
    
    for poll_id, poll in st.session_state.polls.items():
        with st.expander(f"{poll['title']} ({poll_id})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Q:** {poll['question']}")
                for opt in poll['options']:
                    st.markdown(f"- {opt}")
                count = len(st.session_state.responses.get(poll_id, []))
                st.caption(f"📊 {count} responses")
            
            with col2:
                if st.button("QR", key=f"qr_{poll_id}"):
                    url = f"{get_base_url()}?vote={poll_id}"
                    qr = generate_qr(url)
                    st.image(qr, width=200)
                    st.code(url)
                
                if st.button("Clear", key=f"clear_{poll_id}"):
                    st.session_state.responses[poll_id] = []
                    save_data()
                    st.rerun()
                
                if st.button("Delete", key=f"del_{poll_id}"):
                    del st.session_state.polls[poll_id]
                    if poll_id in st.session_state.responses:
                        del st.session_state.responses[poll_id]
                    save_data()
                    st.rerun()

elif page == "Vote":
    st.title("🗳️ Vote")
    
    poll_id = vote_poll_id if vote_poll_id else None
    
    if not poll_id or poll_id not in st.session_state.polls:
        if not st.session_state.polls:
            st.warning("No polls available")
            st.stop()
        if vote_poll_id:
            st.error(f"Poll '{vote_poll_id}' not found")
            st.stop()
        opts = {f"{p['title']} ({pid})": pid for pid, p in st.session_state.polls.items()}
        selected = st.selectbox("Select poll:", list(opts.keys()))
        poll_id = opts[selected]
    
    poll = st.session_state.polls[poll_id]
    st.markdown(f"### {poll['question']}")
    
    with st.form("vote"):
        response = st.radio("Your answer:", poll['options'], index=None)
        
        if st.form_submit_button("Submit", type="primary"):
            if response:
                st.session_state.responses[poll_id].append({
                    'response': response,
                    'timestamp': datetime.now().isoformat()
                })
                save_data()
                st.success("✅ Vote recorded")
                st.balloons()
            else:
                st.error("Select an option")

elif page == "Results":
    st.title("📊 Results")
    
    if not st.session_state.polls:
        st.warning("No polls")
        st.stop()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        opts = {f"{p['title']} ({pid})": pid for pid, p in st.session_state.polls.items()}
        selected = st.selectbox("Poll:", list(opts.keys()))
        poll_id = opts[selected]
    
    with col2:
        auto = st.checkbox("Auto-refresh", value=True)
        if auto:
            st.caption("2s refresh")
    
    poll = st.session_state.polls[poll_id]
    responses = st.session_state.responses.get(poll_id, [])
    
    st.markdown(f"### {poll['question']}")
    st.caption(f"Responses: {len(responses)}")
    
    if not responses:
        st.info("No responses yet")
    else:
        counts = {opt: sum(1 for r in responses if r['response'] == opt) 
                  for opt in poll['options']}
        
        df = pd.DataFrame({
            'Option': list(counts.keys()),
            'Votes': list(counts.values())
        })
        
        fig = px.bar(df, x='Option', y='Votes', text='Votes',
                     title=poll['title'], color_discrete_sequence=['#1f77b4'])
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, height=400, xaxis_title="", yaxis_title="Votes")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Breakdown")
        total = len(responses)
        for opt, count in counts.items():
            pct = (count / total * 100) if total > 0 else 0
            st.markdown(f"**{opt}:** {count} ({pct:.1f}%)")
    
    if auto:
        import time
        time.sleep(2)
        st.rerun()

elif page == "Export":
    st.title("💾 Export")
    
    if not st.session_state.polls:
        st.warning("No data")
        st.stop()
    
    for poll_id, poll in st.session_state.polls.items():
        with st.expander(f"{poll['title']} ({poll_id})"):
            responses = st.session_state.responses.get(poll_id, [])
            
            if not responses:
                st.info("No responses")
            else:
                df = pd.DataFrame(responses)
                st.dataframe(df, use_container_width=True)
                
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"Download {poll_id}.csv",
                    data=csv,
                    file_name=f"{poll_id}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key=f"dl_{poll_id}"
                )

st.divider()
st.caption("Live Polling System")
