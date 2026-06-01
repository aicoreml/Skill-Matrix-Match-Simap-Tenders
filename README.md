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

### Run Locally

```bash
# Clone the repository
git clone https://github.com/aicoreml/Skill-Matrix-Match-Simap-Tenders.git
cd Skill-Matrix-Match-Simap-Tenders

# Install dependencies
pip install -r requirements.txt

# Start the app (binds to all interfaces on port 8503)
streamlit run app.py --server.port=8503 --server.address=0.0.0.0
```

The app will be available at `http://localhost:8503/`.

## 📁 Data Sources

### Consultant Database (`data/consultants.db`)
The HR resource pool is stored in a SQLite database. The schema is created automatically on first run.

| Column | Description |
|--------|-------------|
| `id` | Consultant ID (primary key, e.g. `CV001`) |
| `name` | Full name |
| `title` | Job title |
| `years_experience` | Years of SAP experience |
| `location` | City / country |
| `languages` | Spoken languages |
| `skills_sap_modules` | Comma-separated SAP module skills |
| `skills_technical` | Technical skills |
| `skills_project` | Project / architecture skills |
| `skills_tools` | Tooling skills |
| `certifications` | SAP / other certifications |
| `experience` | Work history |
| `education` | Education background |
| `summary` | Short profile summary |
| `specialization` | Primary specialization |
| `exp_display` | Pre-formatted experience string (e.g. `12y`) |
| `key_sap_modules` | Curated list of key SAP modules |

### Live Tenders
Public tenders are fetched live from **simap.ch** at runtime — no static tender data file is shipped with the app.

## 🎯 How It Works

### 1. Browse Live Tenders
Click **"🌐 Live simap.ch Tenders"** in the sidebar to search public SAP tenders.

### 2. Match Consultants
From a tender result, click **"🎯 Match Consultants"** to analyze skill overlap.

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
│   Nginx Proxy   │────▶│  Auth Wrapper    │────▶│  Skill Matrix   │
│  :443 (HTTPS)   │     │  (optional, :8000)│     │   Streamlit     │
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
└── data/
    └── consultants.db          # SQLite database (HR resource pool)
```

## ⚙️ Deployment

### Nginx Reverse Proxy (example)

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

> **Note:** Replace `proxy_pass` with your own host/port and the `location` prefix with whatever path you want to expose the app under.

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
1. Start the app locally (`streamlit run app.py …`)
2. Open `http://localhost:8503/`
3. Click **"🌐 Live simap.ch Tenders"** in the sidebar
4. Search for a SAP-related term and pick a result
5. Click **"🎯 Match Consultants"** on a tender
6. Verify consultants and AI interpretation display correctly
7. Switch language to German and verify translations

### API Testing
```bash
# Health endpoint (Streamlit)
curl http://localhost:8503/_stcore/health
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

### Connection Refused / 502 Bad Gateway
- **Cause**: Streamlit app is not running
- **Solution**: Start the app:
  ```bash
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
- **Solution**: Hard-refresh the page (Cmd/Ctrl+Shift+R) or use an incognito window.

## 📊 Performance

- **Matching Speed**: < 2 seconds for 20 consultants × 20 tenders
- **AI Interpretation**: 5-15 seconds (depends on LLM response time)
- **Concurrent Users**: Supports 10+ simultaneous users

## 🔐 Security Notes

- This app reads consultant data from a local SQLite database and fetches public tender data from `simap.ch`. No write access to the database is required for the matching workflow.
- When deploying behind a reverse proxy, add authentication (basic auth, OAuth, or a wrapper dashboard) — the app itself has no built-in auth.
- The `data/consultants.db` file contains personal data (names, locations, experience). Do not commit it to a public repo unless that is intentional.
- XSRF protection enabled in Streamlit
- HTTPS encryption via Nginx

## 📄 License

Internal use only - Not for external distribution

## 👥 Authors

Developed for SAP consultant skill matching and tender assignment optimization.

## 📞 Support

For issues or feature requests, contact the development team.
