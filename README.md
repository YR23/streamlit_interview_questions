# Interview Questions Streamlit App

A Streamlit web application that displays interview questions and AI-generated answers with company logos.

## Features

- **Dynamic Data Loading**: Automatically downloads today's interview data from Backblaze B2
- **Company Logos**: Fetches company logos from multiple sources (Google Favicons, Clearbit, etc.)
- **Interactive Filtering**: Filter by company and role
- **Expandable Q&A**: Questions and answers in collapsible sections
- **Responsive Design**: Clean, professional interface

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Credentials** (Optional):
   Create `.streamlit/secrets.toml`:
   ```toml
   [backblaze]
   key_id = "your_b2_key_id"
   application_key = "your_b2_application_key"
   bucket_name = "your_bucket_name"
   ```

   Or set environment variables:
   ```bash
   export B2_KEY_ID="your_key_id"
   export B2_APPLICATION_KEY="your_app_key"
   export B2_BUCKET_NAME="your_bucket_name"
   ```

3. **Run the App**:
   ```bash
   streamlit run streamlit_app.py
   ```

## How It Works

1. The app checks for today's JSON file (format: `YYYY-MM-DD.json`)
2. If not found locally, it downloads from Backblaze B2
3. Falls back to the most recent local JSON file if download fails
4. Displays interviews with company logos and filtering options

## File Structure

```
├── streamlit_app.py      # Main Streamlit application
├── logo_fetcher.py       # Company logo fetching logic
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── secrets.toml     # Streamlit secrets (excluded from git)
└── README.md            # This file
```

## Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add secrets in the Streamlit Cloud dashboard

### Local Development
```bash
git clone https://github.com/YR23/streamlit_interview_questions.git
cd streamlit_interview_questions
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Data Format

The app expects JSON files with this structure:
```json
[
  {
    "question": "Interview question text",
    "company": "Company Name",
    "role": "Job Role",
    "location": "Location",
    "company_rating": "Rating",
    "interview_date": "Date",
    "answer": "AI-generated answer",
    "url": "Source URL",
    "scraped_at": "Timestamp",
    "answer_generated_at": "Timestamp"
  }
]
```