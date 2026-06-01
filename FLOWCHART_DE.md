# 🔄 SAP Skill Matrix Match - Technischer Flussplan

## Systemarchitektur-Fluss

```mermaid
graph TB
    User[👤 Projektmanager] -->|HTTPS| Nginx[Nginx Proxy :443]
    Nginx -->|/skill-matrix/| Streamlit[Streamlit App :8503]

    subgraph "Optionaler Auth-Wrapper (Beispiel)"
        Login[Login-Seite] --> Auth[Sitzungs-Auth]
        Auth --> Dashboard[App Dashboard]
        Dashboard -->|Start Button| StartAPI[POST /start-skill-matrix]
        StartAPI -->|Subprozess| Streamlit
    end

    subgraph "Skill Matrix App"
        UI[Benutzeroberfläche] --> LoadData[Daten laden]
        LoadData --> SearchTender[Live simap.ch Ausschreibungen durchsuchen]
        SearchTender --> MatchBtn[Match-Button klicken]
        MatchBtn --> SkillMatch[Kompetenz-Matching-Algorithmus]
        SkillMatch --> Results[Ergebnisse anzeigen]
        Results --> LLM[Ollama LLM abfragen]
        LLM --> Interpretation[KI-Interpretation anzeigen]
    end
    
    subgraph "Datenschicht"
        ConsultantsDB[(SQLite: data/consultants.db)]
        SimapAPI[simap.ch Öffentliche Ausschreibungen]
    end
    
    LoadData --> ConsultantsDB
    LoadData --> SimapAPI
    
    subgraph "Externe Dienste"
        Ollama[Ollama LLM :11434<br/>minimax-m2.7:cloud]
    end
    
    LLM -->|HTTP POST| Ollama
    Ollama -->|Antwort| LLM
```

## Anwendungsablauf

```mermaid
flowchart TD
    A[🏁 Start] --> B{App läuft?}
    B -->|Nein| C[502 Bad Gateway]
    B -->|Ja| D[UI laden]
    
    D --> E[Sprache wählen<br/>EN/DE]
    E --> F[Ausschreibung aus Dropdown wählen]
    F --> G[Ausschreibungsdetails anzeigen]
    
    G --> H{Match-Button klicken?}
    H -->|Nein| F
    H -->|Ja| I[Berater aus CSV laden]
    
    I --> J[Ausschreibungsfähigkeiten extrahieren]
    J --> K[Fähigkeiten normalisieren]
    
    K --> L[Für jeden Berater]
    L --> M{Fähigkeiten extrahieren}
    M --> N[Pflichtfähigkeiten matchen]
    N --> O[Optionale Fähigkeiten matchen]
    O --> P[Fit Score berechnen]
    
    P --> Q{Weitere Berater?}
    Q -->|Ja| L
    Q -->|Nein| R[Nach Fit Score sortieren]
    
    R --> S[Top 5 Karten anzeigen]
    S --> T[Ergebnistabelle anzeigen]
    T --> U[LLM Prompt generieren]
    
    U --> V[Ollama API abfragen]
    V --> W{Antwort erhalten?}
    W -->|Ja| X[KI-Interpretation anzeigen]
    W -->|Nein| Y[Fehlermeldung anzeigen]
    
    X --> Z{CSV herunterladen?}
    Y --> Z
    Z -->|Ja| AA[CSV-Datei generieren]
    Z -->|Nein| AB[🔄 Weitere Ausschreibung wählen]
    
    AA --> AC[📥 Download startet]
    AC --> AB
```

## Kompetenz-Matching-Algorithmus

```mermaid
flowchart TD
    A[Matching starten] --> B[Ausschreibungsanforderungen holen]
    B --> C[Pflichtfähigkeiten parsen]
    B --> D[Optionale Fähigkeiten parsen]
    
    C --> E[In Kleinbuchstaben normalisieren]
    D --> E
    
    E --> F[Nächsten Berater holen]
    F --> G[Beraterfähigkeiten extrahieren]
    G --> H[Fähigkeiten normalisieren]
    
    H --> I{Jede<br/>Pflichtfähigkeit prüfen}
    I --> J{Exakte Übereinstimmung?}
    J -->|Ja| K[Zu Matched hinzufügen]
    J -->|Nein| L{Teilweise Übereinstimmung?}
    L -->|Enthalten/Substring| K
    L -->|Kein Match| M[Zu Missing hinzufügen]
    
    K --> N{Weitere Pflicht?}
    N -->|Ja| I
    N -->|Nein| O{Jede<br/>optionale Fähigkeit prüfen}
    
    O --> P{Exakte Übereinstimmung?}
    P -->|Ja| Q[Zu Matched Optional hinzufügen]
    P -->|Nein| R{Teilweise Übereinstimmung?}
    R -->|Ja| Q
    R -->|Nein| S[Überspringen]
    
    Q --> T{Weitere Optional?}
    T -->|Ja| O
    T -->|Nein| U[Fit Score berechnen]
    
    U --> V["Score = (2×Gefunden_Pflicht<br/>+ Gefunden_Optional) /<br/>(2×Gesamt_Pflicht<br/>+ Gesamt_Optional) × 100"]
    
    V --> W[Ergebnis speichern]
    W --> X{Weitere Berater?}
    X -->|Ja| F
    X -->|Nein| Y[Absteigend sortieren]
    Y --> Z[Ergebnisse zurückgeben]
```

## LLM-Integrations-Fluss

```mermaid
sequenceDiagram
    participant U as Benutzer
    participant S as Streamlit App
    participant P as Prompt Builder
    participant O as Ollama API
    participant L as LLM Modell
    participant D as Anzeige
    
    U->>S: Auf "Passende Berater finden" klicken
    S->>S: Kompetenz-Matching berechnen
    S->>S: Ergebnisse anzeigen
    
    U->>S: Zu KI-Interpretation scrollen
    S->>P: Prompt mit Kontext erstellen
    
    Note over P: Beinhaltet:<br/>- Ausschreibungsdetails<br/>- Top 3 Berater<br/>- Fähigkeitsaufschlüsselung<br/>- Sprachpräferenz
    
    P->>O: POST /api/generate
    Note over O: Modell: minimax-m2.7:cloud<br/>Timeout: 60s
    
    O->>L: Anfrage weiterleiten
    L->>L: Analyse generieren
    
    Note over L: Analysiert:<br/>1. Kompetenzabdeckung<br/>2. Kandidatenstärken<br/>3. Kompetenzlücken<br/>4. Team-Empfehlungen
    
    L->>O: Antwort zurückgeben
    O->>S: JSON-Antwort
    
    alt Erfolg
        S->>D: Markdown rendern
        D->>U: Interpretation anzeigen
    else Fehler 404
        S->>D: Modellfehler anzeigen
        D->>U: "Modell nicht gefunden"
    else Timeout
        S->>D: Timeout anzeigen
        D->>U: "Anfrage abgelaufen"
    else Verbindungsfehler
        S->>D: Verbindungsfehler anzeigen
        D->>U: "Ollama läuft nicht"
    end
```

## Datenflussdiagramm

```mermaid
graph LR
    subgraph "Eingabeschicht"
        A[(SQLite: data/consultants.db)]
        B[simap.ch Öffentliche Ausschreibungen]
    end
    
    subgraph "Verarbeitungsschicht"
        C[Daten laden]
        D[Fähigkeiten parsen]
        E[Text normalisieren]
        F[Matching-Algorithmus]
        G[Score-Rechner]
    end
    
    subgraph "Ausgabeschicht"
        H[Berater-Karten]
        I[Ergebnistabelle]
        J[KI-Interpretation]
        K[CSV-Export]
    end
    
    subgraph "Extern"
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

## Zustandsverwaltung

```mermaid
stateDiagram-v2
    [*] --> AppLoading
    AppLoading --> DataLoaded: CSV-Dateien geladen
    DataLoaded --> TenderSelected: Benutzer wählt Ausschreibung
    TenderSelected --> MatchingReady: Ausschreibungsdetails angezeigt
    
    MatchingReady --> MatchingInProgress: Match-Button klicken
    MatchingInProgress --> ResultsDisplayed: Matching abgeschlossen
    
    ResultsDisplayed --> LLMQuerying: LLM automatisch auslösen
    LLMQuerying --> LLMResponseReceived: Antwort erhalten
    LLMQuerying --> LLMError: Fehler/Timeout
    
    LLMResponseReceived --> InterpretationDisplayed
    LLMError --> ErrorDisplayed
    
    InterpretationDisplayed --> LanguageSwitched: Benutzer ändert Sprache
    InterpretationDisplayed --> NewTenderSelected: Andere Ausschreibung wählen
    InterpretationDisplayed --> CSVDownloaded: Auf Download klicken
    
    LanguageSwitched --> TenderSelected
    NewTenderSelected --> TenderSelected
    CSVDownloaded --> InterpretationDisplayed
    
    ErrorDisplayed --> RetryLLM: Auf Retry klicken
    RetryLLM --> LLMQuerying
```

## Komponenten-Interaktion

```mermaid
graph TB
    subgraph "Frontend-Komponenten"
        UI[Sprachauswahl]
        DD[Ausschreibungs-Dropdown]
        MB[Match-Button]
        CC[Berater-Karten]
        RT[Ergebnistabelle]
        AI[KI-Interpretations-Box]
        DB[Download-Button]
    end
    
    subgraph "Backend-Funktionen"
        LC[load_consultants]
        SF[search_simap_tenders]
        MS[match_skills]
        GLM[generate_llm_interpretation]
        QO[query_ollama]
    end
    
    subgraph "Datenspeicher"
        SC[Sitzungsstatus<br/>language, page, selected_simap_tender]
        DB1[(SQLite: data/consultants.db)]
    end
    
    UI --> SC
    SearchBtn --> SF
    MB --> MS
    MS --> LC
    LC --> DB1
    MS --> CC
    MS --> RT
    MS --> GLM
    GLM --> QO
    QO --> AI
    DB --> RT
```

## Fehlerbehandlungs-Fluss

```mermaid
flowchart TD
    A[Vorgang starten] --> B{Vorgangstyp?}
    
    B -->|CSV laden| C{Datei existiert?}
    C -->|Ja| D[Erfolgreich laden]
    C -->|Nein| E[Fehler anzeigen<br/>"Datei nicht gefunden"]
    
    B -->|Matching| F{Daten geladen?}
    F -->|Ja| G[Matching ausführen]
    F -->|Nein| H[Fehler anzeigen<br/>"Daten nicht geladen"]
    
    B -->|LLM abfragen| I{Ollama läuft?}
    I -->|Nein| J[Fehler anzeigen<br/>"Ollama läuft nicht"]
    I -->|Ja| K{Modell verfügbar?}
    
    K -->|Nein| L[Fehler anzeigen<br/>"Modell nicht gefunden"]
    K -->|Ja| M{Antwort-Timeout?}
    
    M -->|Ja| N[Fehler anzeigen<br/>"Anfrage abgelaufen"]
    M -->|Nein| O{HTTP-Status?}
    
    O -->|200| P[Antwort anzeigen]
    O -->|404| Q[Fehler anzeigen<br/>"Modell 404"]
    O -->|Andere| R[Fehler anzeigen<br/>"HTTP-Fehler"]
    
    B -->|CSV herunterladen| S{Ergebnisse verfügbar?}
    S -->|Ja| T[CSV generieren]
    S -->|Nein| U[Fehler anzeigen<br/>"Keine Ergebnisse"]
```

## Bereitstellungsarchitektur

```mermaid
graph TB
    subgraph "Internet"
        User[👤 Benutzer-Browser]
    end
    
    subgraph "Firewall"
        FW[Port 443 HTTPS]
    end
    
    subgraph "Nginx Reverse Proxy"
        Nginx[Nginx Server<br/>ihr-host.example.com]
        SSL[SSL-Zertifikat<br/>Let's Encrypt]
    end
    
    subgraph "Anwendungsschicht"
        AuthWrapper[Auth-Wrapper<br/>Port 8000]
        Streamlit[Streamlit Apps<br/>Verschiedene Ports]
        SkillMatrix[Skill Matrix<br/>Port 8503]
    end

    subgraph "KI-Dienste"
        Ollama[Ollama LLM<br/>Port 11434]
    end

    subgraph "Dateisystem"
        DataFiles[(SQLite: data/consultants.db)]
        Logs[Log-Dateien<br/>*.log]
    end
    
    User -->|HTTPS| FW
    FW --> Nginx
    Nginx --> SSL
    Nginx -->|/| Bottle
    Nginx -->|/skill-matrix/| SkillMatrix
    SkillMatrix -->|HTTP| Ollama
    SkillMatrix --> DataFiles
    SkillMatrix --> Logs
    Bottle -->|Start/Stopp| SkillMatrix
```

## Sicherheitsfluss

```mermaid
sequenceDiagram
    participant U as Benutzer
    participant N as Nginx
    participant B as Bottle App
    participant S as Sitzungsspeicher
    participant SM als Skill Matrix
    
    U->>N: HTTPS-Anfrage
    N->>B: Anfrage weiterleiten
    
    B->>S: Sitzungs-Cookie prüfen
    alt Keine Sitzung
        S-->>B: Ungültig
        B->>U: Umleitung zu /login
    else Gültige Sitzung
        S-->>B: Gültig + Benutzerinfo
        B->>B: Admin-Rechte prüfen
        alt Admin-Benutzer
            B->>SM: Start-Befehl
            SM-->>B: Erfolg
            B->>U: JSON Erfolg
        else Normaler Benutzer
            B->>U: JSON Fehler<br/>"Admin erforderlich"
        end
    end
    
    Note over N,SM: Alle Kommunikationen über HTTPS
    Note over S: Sitzung läuft nach 1 Stunde ab
    Note over SM: XSRF-Schutz aktiviert
```

---

## Legende

| Symbol | Bedeutung |
|--------|-----------|
| ▶ | Prozessstart |
| ◆ | Entscheidungspunkt |
| ▭ | Prozess/Aktion |
| ◯ | Eingabe/Ausgabe |
| → | Datenfluss |
| ⇢ | Asynchroner Fluss |
| [ ] | Subsystem |

## Dokumenteninfo

- **Version**: 1.0
- **Zuletzt aktualisiert**: März 2026
- **Autor**: Entwicklungsteam
- **Status**: Produktion
