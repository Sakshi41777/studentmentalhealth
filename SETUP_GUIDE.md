# MindCare - Student Mental Health Assessment App

## Features Implemented ✅

### 1. **One-by-One Question Display**
- Questions appear one at a time for better UX
- Automatic progression to next question after selection
- Users can go back and change answers
- Progress bar shows current position (e.g., 5/21)

### 2. **Progress Bar**
- Visual indicator of quiz completion
- Real-time updates as user progresses
- Shows current question number and total

### 3. **LLM Integration for Smart Suggestions**
- Automatically generates personalized relaxation activities
- Supports multiple LLM providers:
  - **Groq** (Free, fastest) - Recommended for testing
  - **Anthropic Claude** (requires paid API key)
  - **OpenAI** (requires paid API key)
- Gracefully falls back to hardcoded suggestions if no API is available

### 4. **Engaging Activity Cards with Images**
- Each activity has a beautiful image from Unsplash
- Hover effects for interactivity
- Responsive grid layout
- AI-generated descriptions and image search terms

---

## Setup Instructions

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd c:\Users\saksh_dd86j1h\OneDrive\Documents\studentmentalhealth

# Install requirements
pip install -r requirements.txt
```

### 2. Optional: Set Up LLM APIs

Choose ONE of the following options:

#### **Option A: Groq (FREE - Recommended for Testing)**
```bash
pip install groq httpx==0.27.2

# Get free API key from: https://console.groq.com
# Set environment variable (Windows):
set GROQ_API_KEY=your_api_key_here

# Or in PowerShell:
$env:GROQ_API_KEY = "your_api_key_here"
```

#### **Option B: Anthropic Claude**
```bash
pip install anthropic

# Get API key from: https://console.anthropic.com
# Set environment variable:
set ANTHROPIC_API_KEY=your_api_key_here
```

#### **Option C: OpenAI**
```bash
pip install openai

# Get API key from: https://platform.openai.com/api-keys
# Set environment variable:
set OPENAI_API_KEY=your_api_key_here
```

### 3. Run the Application

```bash
cd mental
python manage.py runserver
```

Open browser to: `http://127.0.0.1:8000/`

---

## User Flow

1. **Home Page** (`http://127.0.0.1:8000/`)
   - Click "Check My Wellness" button

2. **Assessment Form** (`http://127.0.0.1:8000/form/`)
   - Answer 21 DASS-21 questions
   - One question appears at a time
   - Progress bar shows completion status
   - Auto-advance to next question after selection
   - Click "View My Wellness Summary" when done

3. **Results Page** (`/form/` with POST)
   - Shows wellness level (Stable/Moderate/Elevated)
   - Overall wellness percentage with circular progress
   - Stress, Anxiety, and Depression breakdowns
   - **4 Personalized Activities** with:
     - Activity name and description
     - Beautiful calming images from Unsplash
     - AI-generated (if LLM available) or curated suggestions
   - Guided relaxation video
   - Back to home button

---

## Technical Stack

- **Backend**: Django 5.2.10
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Images**: Unsplash API (free, no API key needed)
- **LLM Integration**: 
  - Groq (Default)
  - Anthropic Claude
  - OpenAI
- **Assessment**: DASS-21 Questionnaire

---

## File Structure

```
mental/
├── manage.py
├── db.sqlite3
├── mental/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── home/
│   ├── views.py              # Main logic
│   ├── templates/
│   │   ├── form.html         # New: Interactive form with one-by-one Q&A
│   │   ├── result.html       # Updated: Activity cards with images
│   │   ├── home.html
│   │   ├── login.html
│   │   └── register.html
│   ├── static/
│   │   └── style.css         # Updated: Better activity card styling
│   └── ml/
│       ├── suggestions.py    # Updated: LLM integration
│       └── predictor.py
└── requirements.txt          # New: Project dependencies
```

---

## API Responses Format

The LLM will generate activities in this format:

```json
[
  {
    "title": "Guided Meditation",
    "desc": "Find a quiet space and follow a 10-minute guided meditation to calm your mind.",
    "image_term": "person meditating peaceful"
  },
  ...
]
```

---

## Environment Variables

If using LLM APIs, set environment variables:

```powershell
# PowerShell
$env:GROQ_API_KEY = "your_key"
$env:ANTHROPIC_API_KEY = "your_key"
$env:OPENAI_API_KEY = "your_key"
```

---

## Fallback Behavior

If no LLM API is available or configured:
- App automatically uses hardcoded, curated suggestions
- Activities still display with beautiful Unsplash images
- User experience remains smooth and engaging

---

## Next Steps

1. ✅ Test the form navigation (one-by-one questions)
2. ✅ Test progress bar functionality
3. ✅ Configure LLM API of your choice
4. ✅ Submit a test assessment
5. ✅ Verify activity cards display correctly

---

## Troubleshooting

**Question: I see hardcoded suggestions, not LLM-generated ones**
- Solution: Set up an LLM API (Groq is free and easiest)
- Check environment variables are set correctly

**Question: Groq client crashes with "Client.__init__() got an unexpected keyword argument 'proxies'"**
- Solution: Pin httpx to a compatible version
- Run: `pip install httpx==0.27.2`

**Question: Images aren't loading**
- Solution: This is normal - Unsplash API returns random images
- Refresh page to get different images
- Check browser console for errors

**Question: Form not advancing to next question**
- Solution: JavaScript might be disabled
- Check browser console (F12) for errors
- Ensure JavaScript is enabled

---

## Support

For issues or questions, check:
1. Browser console (F12) for JavaScript errors
2. Django server logs
3. Environment variables are properly set
4. All dependencies installed: `pip list | grep -E "django|groq|anthropic|openai"`
