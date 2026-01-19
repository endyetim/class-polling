# Streamlit Secrets Setup

Automate poll loading using Streamlit Secrets - no manual poll creation needed.

## Benefits

✅ Define polls once in Streamlit Cloud  
✅ Polls load automatically on app start  
✅ No manual Admin UI setup  
✅ Keep poll content private  
✅ Easy to update polls

## Setup

### 1. Deploy App to Streamlit Cloud

Follow main README deployment steps.

### 2. Add Secrets

In Streamlit Cloud dashboard:
1. Click your app
2. Settings → Secrets
3. Paste poll definitions (TOML format)
4. Save

### 3. Secret Format

```toml
[polls.anxiety]
title = "Statistics Anxiety"
question = "How nervous are you about statistics?"
options = ["A. Very nervous", "B. Somewhat nervous", "C. A little nervous", "D. Not nervous"]
course = "Data Analysis"
week = 1

[polls.crime]
title = "Crime Perception"
question = "In the last 30 years, has U.S. violent crime:"
options = ["A. Increased", "B. Decreased", "C. Stayed the same"]
course = "Data Analysis"
week = 1

[polls.causation]
title = "Causation Question"
question = "Does the PURE study prove saturated fat causes longer life?"
options = ["A. Yes, definitely", "B. No, definitely not", "C. Maybe - need more info", "D. Study proves causation"]
course = "Data Analysis"
week = 1
```

### 4. Restart App

Click "Reboot app" in Streamlit Cloud dashboard.

Polls load automatically.

## How It Works

App checks `st.secrets['polls']` on startup and creates polls automatically.

## Updating Polls

1. Edit secrets in Streamlit Cloud dashboard
2. Reboot app
3. New polls appear immediately

## Local Testing

Create `.streamlit/secrets.toml` (gitignored):

```toml
[polls.test]
title = "Test Poll"
question = "Test question?"
options = ["A. Yes", "B. No"]
course = "Test"
week = 1
```

Run locally - polls load from secrets.

## Private vs Public Repo

### Public Repo (Current)
- ✅ Code is public
- ✅ Polls stay private (in secrets)
- ✅ Free Streamlit Cloud
- ✅ Anyone can see code structure
- ❌ Repo is visible

### Private Repo
- ✅ Code is private
- ✅ Polls stay private
- ✅ Free Streamlit Cloud (with GitHub Pro/Team)
- ❌ Need GitHub Pro ($4/mo) or GitHub Team

**To make repo private:**
1. Go to github.com/endyetim/class-polling
2. Settings → Danger Zone → Change visibility
3. Make private
4. Streamlit Cloud still works (if you have GitHub Pro)

## Recommendation

**Keep repo public, use secrets for polls:**
- Code is generic (no sensitive info)
- Polls stay private in secrets
- Free everything
- Easy collaboration

**Only make private if:**
- You have GitHub Pro/Team
- You want code structure hidden
- Institutional requirement
