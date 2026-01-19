# Live Polling for Classroom

Streamlit app for creating and running live polls during lectures.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

Access at `http://localhost:8501`

## Usage

### Create Polls from YAML

1. Edit `config/polls.yaml`
2. Run `python src/import_polls.py`
3. Restart app

### Create Polls via UI

1. Open app → Admin panel
2. Fill form → Create poll
3. Click "QR" to generate QR code

### Students Vote

Scan QR code or visit: `yourapp.com?vote=poll_id`

### View Results

Results page → Select poll → Enable auto-refresh

## Deploy

**Streamlit Cloud (Free):**
1. Push to GitHub
2. Connect at share.streamlit.io
3. Deploy

**VPS:**
```bash
pip install -r requirements.txt
streamlit run src/app.py --server.port=8501
```

## Structure

```
├── src/
│   ├── app.py           # Main Streamlit app
│   └── import_polls.py  # YAML import script
├── config/
│   └── polls.yaml       # Poll definitions
├── requirements.txt     # Dependencies
└── README.md
```
