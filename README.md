# 🎯 SAP Skill Matrix Match

AI-powered application for matching SAP consultants to project tenders based on skill overlap analysis.

## 📋 Overview

This application helps project managers find the best matching SAP consultants from an HR resource pool by analyzing skill requirements in project tenders. It uses a weighted scoring algorithm and AI interpretation to provide actionable insights.

## ✨ Features

- **Skill-Based Matching**: Automatically match consultants to tenders based on mandatory and optional skills
- **Weighted Scoring**: Mandatory skills count 2x more than optional skills in fit calculation
- **AI Interpretation**: Get AI-powered analysis of top candidates using Ollama LLM (minimax-m2.7:cloud)
- **Bilingual UI**: Switch between English and German interfaces
- **CSV Export**: Download matching results for further analysis
- **20 Pre-loaded Tenders**: Sample SAP project tenders across various industries
- **20 Consultant Profiles**: HR resource pool with diverse SAP specializations

## 🚀 Quick Start

### Access via Dashboard

1. Navigate to **https://gpt.myddns.me/**
2. Login with your credentials
3. Find **SAP Skill Matrix Match** in the "SAP & Enterprise" section
4. Click **Start** to launch the application
5. Access at **https://gpt.myddns.me/skill-matrix/**

### Direct Access

If the app is already running, access directly at: **https://gpt.myddns.me/skill-matrix/**

## 📁 Data Files

### Input Files (in `docs/` folder)

| File | Description |
|------|-------------|
| `skills.csv` | HR resource pool with 20 SAP consultants |
| `tenders_enhanced.csv` | 20 sample SAP project tenders |

### Consultant Data Structure

```csv
ID,Name,Specialization,Exp,Key SAP Modules
CV001,Markus Berger,FICO,12y,"FI, CO, S/4HANA Finance, BPC, FI-AA"
```

### Tender Data Structure

Key columns:
- `mandatory_skills`: Required skills (pipe-separated)
- `optional_skills`: Bonus skills (pipe-separated)
- `matching_profiles`: Pre-defined matching consultant IDs

## 🎯 How It Works

### 1. Select a Tender
Choose from the dropdown menu in the sidebar. View detailed information including:
- Industry, duration, location
- Key deliverables and success criteria
- Mandatory and optional skills

### 2. Find Matching Consultants
Click **"🔍 Find Matching Consultants"** to analyze skill overlap.

### 3. Review Results
- **Summary Metrics**: Total consultants, excellent/good/low matches
- **Top 5 Cards**: Detailed view of best matches with skill breakdown
- **Results Table**: Complete ranking with all consultants
- **AI Interpretation**: LLM analysis of team composition

### 4. Export Results
Download results as CSV for further processing.

## 📊 Fit Score Calculation

```
Fit Score = (2×mandatory_matched + optional_matched) / (2×mandatory_total + optional_total) × 100
```

**Weighting**:
- Mandatory skills: 2x weight
- Optional skills: 1x weight

**Color Coding**:
- 🟢 **Excellent (≥80%)**: Strong skill coverage
- 🟠 **Good (50-79%)**: Partial match, some gaps
- 🔴 **Low (<50%)**: Significant skill gaps

## 🤖 AI Interpretation

The app uses **Ollama** with the `minimax-m2.7:cloud` model to provide:
- Overall skill coverage assessment
- Strengths of top candidates
- Critical skill gaps identification
- Team composition recommendations

**Requirements**: Ollama must be running locally with the model installed:
```bash
ollama pull minimax-m2.7:cloud
ollama serve
```

## 🌐 Language Support

Toggle between languages using the radio button in the sidebar:
- 🇬🇧 **English**: Default interface language
- 🇩🇪 **Deutsch**: German translation available

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Nginx Proxy   │────▶│  Bottle Dashboard│────▶│  Skill Matrix   │
│  :443 (HTTPS)   │     │     :8000        │     │   Streamlit     │
│                 │     │                  │     │     :8503       │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │   Ollama LLM    │
                                                 │    :11434       │
                                                 └─────────────────┘
```

## 📂 Project Structure

```
Skill_Matrix/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file (English)
├── README_DE.md                # German documentation
├── FLOWCHART.md                # Technical flowchart (English)
├── FLOWCHART_DE.md             # German flowchart
├── data/                       # JSON datasets (legacy)
│   ├── consultants.json
│   └── tenders.json
└── docs/                       # CSV data files (active)
    ├── skills.csv              # HR resource pool
    └── tenders_enhanced.csv    # Project tenders
```

## ⚙️ Configuration

### Nginx Proxy (`/opt/homebrew/etc/nginx/servers/gpt.myddns.me.conf`)

```nginx
location /skill-matrix/ {
    proxy_pass http://127.0.0.1:8503/skill-matrix/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### Start Route (Bottle Dashboard)

Endpoint: `POST /start-skill-matrix`
- Authentication required (admin)
- Starts Streamlit app on port 8503
- Health check with 20-second timeout

## 🔧 Dependencies

```txt
streamlit>=1.28.0
pandas>=2.0.0
requests>=2.28.0
```

Install:
```bash
pip install -r requirements.txt
```

## 🧪 Testing

### Manual Testing
1. Open app at https://gpt.myddns.me/skill-matrix/
2. Select tender TND001 (S/4HANA Finance)
3. Click "Find Matching Consultants"
4. Verify CV001 (Markus Berger) appears as top match
5. Check AI interpretation displays correctly
6. Switch language to German and verify translations

### API Testing
```bash
# Check health endpoint
curl http://localhost:8503/skill-matrix/_stcore/health

# Start via dashboard API
curl -X POST https://gpt.myddns.me/start-skill-matrix \
  -H "Cookie: session_id=YOUR_SESSION" \
  -d ""
```

## 📝 Example Use Cases

### Use Case 1: Finance Project
**Tender**: TND001 - S/4HANA Finance Implementation
**Top Match**: CV001 - Markus Berger (FICO Specialist, 12 years)
**Fit Score**: 85-95%

### Use Case 2: Supply Chain Transformation
**Tender**: TND017 - MM/EWM/IBP End-to-End Transformation
**Top Matches**: 
- CV020 - Chen Wei (Supply Chain Architect)
- CV007 - Liam O'Brien (IBP/APO Specialist)
- CV006 - Elena Hoffmann (MM/EWM Specialist)

### Use Case 3: Identity Management
**Tender**: TND004 - SuccessFactors EC & IAS/IPS Setup
**Top Match**: CV002 - Priya Nair (HCM/SuccessFactors, IAS/IPS expert)
**Fit Score**: 90%+

## 🐛 Troubleshooting

### 502 Bad Gateway
- **Cause**: Skill Matrix app not running
- **Solution**: Click "Start" button in dashboard or manually start:
  ```bash
  cd /Users/usermacrtx/Documents/Demos/Skill_Matrix
  streamlit run app.py --server.port=8503 --server.address=0.0.0.0
  ```

### AI Interpretation Shows Error
- **Cause**: Ollama not running or model not installed
- **Solution**:
  ```bash
  ollama pull minimax-m2.7:cloud
  ollama serve
  ```

### Language Not Switching
- **Cause**: Browser cache
- **Solution**: Clear cookies for gpt.myddns.me or use incognito mode

### Start Button Shows JSON Error
- **Cause**: Dashboard app needs restart
- **Solution**: Restart all_demos app:
  ```bash
  lsof -ti:8000 | xargs kill -9
  cd /Users/usermacrtx/Documents/Demos/all_demos
  python3 app.py &
  ```

## 📊 Performance

- **Matching Speed**: < 2 seconds for 20 consultants × 20 tenders
- **AI Interpretation**: 5-15 seconds (depends on LLM response time)
- **Concurrent Users**: Supports 10+ simultaneous users

## 🔐 Security

- Session-based authentication via Bottle dashboard
- Admin-only start/stop functionality
- XSRF protection enabled in Streamlit
- HTTPS encryption via Nginx

## 📄 License

Internal use only - Not for external distribution

## 👥 Authors

Developed for SAP consultant skill matching and tender assignment optimization.

## 📞 Support

For issues or feature requests, contact the development team.
