# 🔄 SAP Skill Matrix Match - Technical Flowchart

## System Architecture Flow

```mermaid
graph TB
    User[👤 Project Manager] -->|HTTPS| Nginx[Nginx Proxy :443]
    Nginx -->|/skill-matrix/| Streamlit[Streamlit App :8503]
    
    subgraph "Bottle Dashboard :8000"
        Login[Login Page] --> Auth[Session Auth]
        Auth --> Dashboard[App Dashboard]
        Dashboard -->|Start Button| StartAPI[POST /start-skill-matrix]
        StartAPI -->|Subprocess| Streamlit
    end
    
    subgraph "Skill Matrix App"
        UI[User Interface] --> LoadData[Load CSV Files]
        LoadData --> SelectTender[Select Tender]
        SelectTender --> MatchBtn[Click Match Button]
        MatchBtn --> SkillMatch[Skill Matching Algorithm]
        SkillMatch --> Results[Display Results]
        Results --> LLM[Query Ollama LLM]
        LLM --> Interpretation[Show AI Interpretation]
    end
    
    subgraph "Data Layer"
        SkillsCSV[docs/skills.csv]
        TendersCSV[docs/tenders_enhanced.csv]
    end
    
    LoadData --> SkillsCSV
    LoadData --> TendersCSV
    
    subgraph "External Services"
        Ollama[Ollama LLM :11434<br/>minimax-m2.7:cloud]
    end
    
    LLM -->|HTTP POST| Ollama
    Ollama -->|Response| LLM
```

## Application Flow

```mermaid
flowchart TD
    A[🏁 Start] --> B{App Running?}
    B -->|No| C[502 Bad Gateway]
    B -->|Yes| D[Load UI]
    
    D --> E[Select Language<br/>EN/DE]
    E --> F[Select Tender from Dropdown]
    F --> G[Display Tender Details]
    
    G --> H{Click Match Button?}
    H -->|No| F
    H -->|Yes| I[Load Consultants from CSV]
    
    I --> J[Extract Tender Skills]
    J --> K[Normalize Skills]
    
    K --> L[For Each Consultant]
    L --> M{Extract Skills}
    M --> N[Match Mandatory Skills]
    N --> O[Match Optional Skills]
    O --> P[Calculate Fit Score]
    
    P --> Q{More Consultants?}
    Q -->|Yes| L
    Q -->|No| R[Sort by Fit Score]
    
    R --> S[Display Top 5 Cards]
    S --> T[Display Results Table]
    T --> U[Generate LLM Prompt]
    
    U --> V[Query Ollama API]
    V --> W{Response Received?}
    W -->|Yes| X[Display AI Interpretation]
    W -->|No| Y[Show Error Message]
    
    X --> Z{Download CSV?}
    Y --> Z
    Z -->|Yes| AA[Generate CSV File]
    Z -->|No| AB[🔄 Select Another Tender]
    
    AA --> AC[📥 Download Starts]
    AC --> AB
```

## Skill Matching Algorithm

```mermaid
flowchart TD
    A[Start Matching] --> B[Get Tender Requirements]
    B --> C[Parse Mandatory Skills]
    B --> D[Parse Optional Skills]
    
    C --> E[Normalize to Lowercase]
    D --> E
    
    E --> F[Get Next Consultant]
    F --> G[Extract Consultant Skills]
    G --> H[Normalize Skills]
    
    H --> I{Check Each<br/>Mandatory Skill}
    I --> J{Exact Match?}
    J -->|Yes| K[Add to Matched]
    J -->|No| L{Partial Match?}
    L -->|Contains/Substring| K
    L -->|No Match| M[Add to Missing]
    
    K --> N{More Mandatory?}
    N -->|Yes| I
    N -->|No| O{Check Each<br/>Optional Skill}
    
    O --> P{Exact Match?}
    P -->|Yes| Q[Add to Matched Optional]
    P -->|No| R{Partial Match?}
    R -->|Yes| Q
    R -->|No| S[Skip]
    
    Q --> T{More Optional?}
    T -->|Yes| O
    T -->|No| U[Calculate Fit Score]
    
    U --> V["Score = (2×Mandatory_Matched<br/>+ Optional_Matched) /<br/>(2×Mandatory_Total<br/>+ Optional_Total) × 100"]
    
    V --> W[Store Result]
    W --> X{More Consultants?}
    X -->|Yes| F
    X -->|No| Y[Sort Descending]
    Y --> Z[Return Results]
```

## LLM Integration Flow

```mermaid
sequenceDiagram
    participant U as User
    participant S as Streamlit App
    participant P as Prompt Builder
    participant O as Ollama API
    participant L as LLM Model
    participant D as Display
    
    U->>S: Click "Find Matching Consultants"
    S->>S: Calculate Skill Matches
    S->>S: Display Results
    
    U->>S: Scroll to AI Interpretation
    S->>P: Build Prompt with Context
    
    Note over P: Include:<br/>- Tender Details<br/>- Top 3 Consultants<br/>- Skill Breakdown<br/>- Language Preference
    
    P->>O: POST /api/generate
    Note over O: Model: minimax-m2.7:cloud<br/>Timeout: 60s
    
    O->>L: Forward Request
    L->>L: Generate Analysis
    
    Note over L: Analyzes:<br/>1. Skill Coverage<br/>2. Candidate Strengths<br/>3. Skill Gaps<br/>4. Team Recommendations
    
    L->>O: Return Response
    O->>S: JSON Response
    
    alt Success
        S->>D: Render Markdown
        D->>U: Show Interpretation
    else Error 404
        S->>D: Show Model Error
        D->>U: "Model not found"
    else Timeout
        S->>D: Show Timeout
        D->>U: "Request timed out"
    else Connection Error
        S->>D: Show Connection Error
        D->>U: "Ollama not running"
    end
```

## Data Flow Diagram

```mermaid
graph LR
    subgraph "Input Layer"
        A[skills.csv]
        B[tenders_enhanced.csv]
    end
    
    subgraph "Processing Layer"
        C[Load Data]
        D[Parse Skills]
        E[Normalize Text]
        F[Match Algorithm]
        G[Score Calculator]
    end
    
    subgraph "Output Layer"
        H[Consultant Cards]
        I[Results Table]
        J[AI Interpretation]
        K[CSV Export]
    end
    
    subgraph "External"
        L[Ollama LLM]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
    J --> L
    G --> K
```

## State Management

```mermaid
stateDiagram-v2
    [*] --> AppLoading
    AppLoading --> DataLoaded: CSV Files Loaded
    DataLoaded --> TenderSelected: User Selects Tender
    TenderSelected --> MatchingReady: Tender Details Displayed
    
    MatchingReady --> MatchingInProgress: Click Match Button
    MatchingInProgress --> ResultsDisplayed: Matching Complete
    
    ResultsDisplayed --> LLMQuerying: Auto-trigger LLM
    LLMQuerying --> LLMResponseReceived: Response Received
    LLMQuerying --> LLMError: Error/Timeout
    
    LLMResponseReceived --> InterpretationDisplayed
    LLMError --> ErrorDisplayed
    
    InterpretationDisplayed --> LanguageSwitched: User Changes Language
    InterpretationDisplayed --> NewTenderSelected: Select Different Tender
    InterpretationDisplayed --> CSVDownloaded: Click Download
    
    LanguageSwitched --> TenderSelected
    NewTenderSelected --> TenderSelected
    CSVDownloaded --> InterpretationDisplayed
    
    ErrorDisplayed --> RetryLLM: Click Retry
    RetryLLM --> LLMQuerying
```

## Component Interaction

```mermaid
graph TB
    subgraph "Frontend Components"
        UI[Language Selector]
        DD[Tender Dropdown]
        MB[Match Button]
        CC[Consultant Cards]
        RT[Results Table]
        AI[AI Interpretation Box]
        DB[Download Button]
    end
    
    subgraph "Backend Functions"
        LC[load_consultants]
        LT[load_tenders]
        MS[match_skills]
        GLM[generate_llm_interpretation]
        QO[query_ollama]
    end
    
    subgraph "Data Store"
        SC[Session State<br/>language]
        CSV1[skills.csv]
        CSV2[tenders_enhanced.csv]
    end
    
    UI --> SC
    DD --> LT
    LT --> CSV2
    MB --> MS
    MS --> LC
    LC --> CSV1
    MS --> CC
    MS --> RT
    MS --> GLM
    GLM --> QO
    QO --> AI
    DB --> RT
```

## Error Handling Flow

```mermaid
flowchart TD
    A[Start Operation] --> B{Operation Type?}
    
    B -->|Load CSV| C{File Exists?}
    C -->|Yes| D[Load Successfully]
    C -->|No| E[Show Error<br/>"File not found"]
    
    B -->|Match Skills| F{Data Loaded?}
    F -->|Yes| G[Execute Matching]
    F -->|No| H[Show Error<br/>"Data not loaded"]
    
    B -->|Query LLM| I{Ollama Running?}
    I -->|No| J[Show Error<br/>"Ollama not running"]
    I -->|Yes| K{Model Available?}
    
    K -->|No| L[Show Error<br/>"Model not found"]
    K -->|Yes| M{Response Timeout?}
    
    M -->|Yes| N[Show Error<br/>"Request timed out"]
    M -->|No| O{HTTP Status?}
    
    O -->|200| P[Display Response]
    O -->|404| Q[Show Error<br/>"Model 404"]
    O -->|Other| R[Show Error<br/>"HTTP Error"]
    
    B -->|Download CSV| S{Results Available?}
    S -->|Yes| T[Generate CSV]
    S -->|No| U[Show Error<br/>"No results"]
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Internet"
        User[👤 User Browser]
    end
    
    subgraph "Firewall"
        FW[Port 443 HTTPS]
    end
    
    subgraph "Nginx Reverse Proxy"
        Nginx[Nginx Server<br/>gpt.myddns.me]
        SSL[SSL Certificate<br/>Let's Encrypt]
    end
    
    subgraph "Application Layer"
        Bottle[Bottle Dashboard<br/>Port 8000]
        Streamlit[Streamlit Apps<br/>Various Ports]
        SkillMatrix[Skill Matrix<br/>Port 8503]
    end
    
    subgraph "AI Services"
        Ollama[Ollama LLM<br/>Port 11434]
    end
    
    subgraph "File System"
        DataFiles[CSV Data Files<br/>/docs/]
        Logs[Log Files<br/>*.log]
    end
    
    User -->|HTTPS| FW
    FW --> Nginx
    Nginx --> SSL
    Nginx -->|/| Bottle
    Nginx -->|/skill-matrix/| SkillMatrix
    SkillMatrix -->|HTTP| Ollama
    SkillMatrix --> DataFiles
    SkillMatrix --> Logs
    Bottle -->|Start/Stop| SkillMatrix
```

## Security Flow

```mermaid
sequenceDiagram
    participant U as User
    participant N as Nginx
    participant B as Bottle App
    participant S as Session Store
    participant SM as Skill Matrix
    
    U->>N: HTTPS Request
    N->>B: Forward Request
    
    B->>S: Check Session Cookie
    alt No Session
        S-->>B: Invalid
        B->>U: Redirect to /login
    else Valid Session
        S-->>B: Valid + User Info
        B->>B: Check Admin Rights
        alt Admin User
            B->>SM: Start Command
            SM-->>B: Success
            B->>U: JSON Success
        else Regular User
            B->>U: JSON Error<br/>"Admin required"
        end
    end
    
    Note over N,SM: All communication over HTTPS
    Note over S: Session expires after 1 hour
    Note over SM: XSRF Protection enabled
```

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ▶ | Process Start |
| ◆ | Decision Point |
| ▭ | Process/Action |
| ◯ | Input/Output |
| → | Data Flow |
| ⇢ | Async Flow |
| [ ] | Subsystem |

## Document Info

- **Version**: 1.0
- **Last Updated**: March 2026
- **Author**: Development Team
- **Status**: Production
