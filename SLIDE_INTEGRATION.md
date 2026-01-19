# Embedding Poll Results in Slides

## Two Approaches

### **Option 1: Link to Results (Recommended)**

Open results in separate browser window, screen share during class.

**Slide example:**
```qmd
## Poll Results

**View live results:**

[Open Results →](https://class-polling.streamlit.app?results=anxiety)

::: notes
- Open link in separate window before class
- Results auto-refresh every 2 seconds
- Screen share this window during discussion
:::
```

**Benefits:**
- ✅ Clean, simple
- ✅ Auto-refreshing
- ✅ No iframe issues
- ✅ Easy to manage

---

### **Option 2: Embed Results (Advanced)**

Embed results directly in slide using iframe.

**Slide example:**
```qmd
## Poll Results

<iframe src="https://class-polling.streamlit.app?results=anxiety" 
        width="100%" 
        height="600" 
        style="border:1px solid #ccc;">
</iframe>
```

**Note:** May require CORS configuration in Streamlit.

---

## URL Format

**Vote on specific poll:**
```
https://class-polling.streamlit.app?vote=anxiety
```

**View results for specific poll:**
```
https://class-polling.streamlit.app?results=anxiety
```

---

## Complete Slide Workflow

### **Slide 1: Poll Question**
```qmd
## Statistics Anxiety

**How nervous are you about statistics?**

A. Very nervous  
B. Somewhat nervous  
C. A little nervous  
D. Not nervous

::: {.fragment}
**Scan to vote:**

<img src="assets/poll_qr_anxiety.png" width="250"/>
:::
```

### **Slide 2: Results**
```qmd
## Poll Results

[View Live Results →](https://class-polling.streamlit.app?results=anxiety)

::: notes
**Setup before class:**
1. Open results link in separate browser window
2. Position on second monitor or separate window
3. Results auto-refresh every 2 seconds

**During class:**
1. Show poll question slide
2. Students vote (1-2 min)
3. Advance to results slide
4. Screen share results window
5. Discuss patterns
:::
```

---

## Classroom Setup

### **Before Class:**

1. **Open results windows:**
   - Poll 1: `https://class-polling.streamlit.app?results=anxiety`
   - Poll 2: `https://class-polling.streamlit.app?results=crime`
   - Poll 3: `https://class-polling.streamlit.app?results=causation`

2. **Arrange windows:**
   - Slides on main screen
   - Results windows on second monitor (or separate tabs)

3. **Test:**
   - Vote on each poll from phone
   - Verify results update

### **During Class:**

1. Show poll question slide
2. Students scan QR code and vote
3. Advance to results slide
4. Screen share results window
5. Results auto-refresh live

---

## Benefits of URL Parameters

**Direct links to specific polls:**
- ✅ No manual navigation
- ✅ Auto-refresh enabled
- ✅ Shows only that poll
- ✅ Clean, focused view

**For students (voting):**
```
?vote=anxiety
```

**For instructor (results):**
```
?results=anxiety
```

Both automatically navigate to correct page and show only that poll.

---

## QR Code Generation

**In Admin panel:**
1. Click "QR" button for poll
2. QR code shows vote URL: `?vote=anxiety`
3. Screenshot QR code
4. Save to `assets/poll_qr_anxiety.png`
5. Insert in slide

**Results link:**
- Manually create: `?results=anxiety`
- Use in slides for instructor reference
- Or embed in iframe

---

## Example: Full Session

```qmd
## Poll: Statistics Anxiety

**How nervous are you about statistics?**

<img src="assets/poll_qr_anxiety.png" width="250"/>

---

## Results

[Live Results →](https://class-polling.streamlit.app?results=anxiety)

---

## Poll: Crime Perception

**Has U.S. violent crime increased or decreased?**

<img src="assets/poll_qr_crime.png" width="250"/>

---

## Results

[Live Results →](https://class-polling.streamlit.app?results=crime)
```

---

## Recommendation

**Use Option 1 (Link + Screen Share):**
- Most reliable
- No CORS issues
- Auto-refreshing
- Easy setup

**Workflow:**
1. Create polls via Streamlit Secrets
2. Generate QR codes in Admin panel
3. Add QR codes to question slides
4. Add results links to results slides
5. Open results links before class
6. Screen share during discussion

Simple, effective, works every time.
