# 🎯 SAP Skill Matrix Match

KI-gestützte Anwendung zum Matchen von SAP-Beratern mit Projektausschreibungen basierend auf Kompetenzüberschneidungen.

## 📋 Überblick

Diese Anwendung unterstützt Projektmanager dabei, die am besten passenden SAP-Berater aus einem HR-Ressourcenpool zu finden, indem sie Kompetenzanforderungen in Projektausschreibungen analysiert. Sie verwendet einen gewichteten Scoring-Algorithmus und KI-Interpretation für umsetzbare Erkenntnisse.

## ✨ Funktionen

- **Kompetenzbasiertes Matching**: Automatische Zuordnung von Beratern zu Ausschreibungen basierend auf Pflicht- und Wahrfähigkeiten
- **Gewichtete Bewertung**: Pflichtfähigkeiten zählen 2x mehr als Wahrfähigkeiten bei der Fit-Berechnung
- **KI-Interpretation**: KI-gestützte Analyse der Top-Kandidaten mit Ollama LLM (minimax-m2.7:cloud)
- **Zweisprachige UI**: Wechsel zwischen englischer und deutscher Oberfläche
- **CSV-Export**: Ergebnisse für weitere Analysen herunterladen
- **20 Vorinstallierte Ausschreibungen**: Beispielhafte SAP-Projektausschreibungen aus verschiedenen Branchen
- **20 Beraterprofile**: HR-Ressourcenpool mit diversen SAP-Spezialisierungen

## 🚀 Schnellstart

### Zugriff über Dashboard

1. Navigieren Sie zu **https://gpt.myddns.me/**
2. Melden Sie sich mit Ihren Zugangsdaten an
3. Finden Sie **SAP Skill Matrix Match** im Bereich "SAP & Enterprise"
4. Klicken Sie auf **Start** zum Starten der Anwendung
5. Zugriff unter **https://gpt.myddns.me/skill-matrix/**

### Direkter Zugriff

Wenn die App bereits läuft, direkter Zugriff unter: **https://gpt.myddns.me/skill-matrix/**

## 📁 Datendateien

### Eingabedateien (im `docs/` Ordner)

| Datei | Beschreibung |
|-------|--------------|
| `skills.csv` | HR-Ressourcenpool mit 20 SAP-Beratern |
| `tenders_enhanced.csv` | 20 beispielhafte SAP-Projektausschreibungen |

### Beraterdatenstruktur

```csv
ID,Name,Specialization,Exp,Key SAP Modules
CV001,Markus Berger,FICO,12y,"FI, CO, S/4HANA Finance, BPC, FI-AA"
```

### Ausschreibungsdatenstruktur

Hauptspalten:
- `mandatory_skills`: Erforderliche Fähigkeiten (Pipe-getrennt)
- `optional_skills`: Bonusfähigkeiten (Pipe-getrennt)
- `matching_profiles`: Vordefinierte passende Berater-IDs

## 🎯 Funktionsweise

### 1. Ausschreibung auswählen
Wählen Sie aus dem Dropdown-Menü in der Seitenleiste. Zeigen Sie detaillierte Informationen an:
- Branche, Dauer, Standort
- Hauptliefergegenstände und Erfolgskriterien
- Pflicht- und optionale Fähigkeiten

### 2. Passende Berater finden
Klicken Sie auf **"🔍 Passende Berater finden"** zur Analyse der Kompetenzüberschneidungen.

### 3. Ergebnisse überprüfen
- **Zusammenfassung**: Gesamtberater, Excellent/Good/Low Matches
- **Top 5 Karten**: Detaillierte Ansicht der besten Matches mit Kompetenzübersicht
- **Ergebnistabelle**: Vollständiges Ranking aller Berater
- **KI-Interpretation**: LLM-Analyse der Teamzusammensetzung

### 4. Ergebnisse exportieren
Ergebnisse als CSV für weitere Verarbeitung herunterladen.

## 📊 Fit Score Berechnung

```
Fit Score = (2×gefundene_pflicht + gefundene_optional) / (2×gesamt_pflicht + gesamt_optional) × 100
```

**Gewichtung**:
- Pflichtfähigkeiten: 2x Gewicht
- Optionale Fähigkeiten: 1x Gewicht

**Farbcodierung**:
- 🟢 **Excellent (≥80%)**: Starke Kompetenzabdeckung
- 🟠 **Good (50-79%)**: Teilweise Übereinstimmung, einige Lücken
- 🔴 **Low (<50%)**: Erhebliche Kompetenzlücken

## 🤖 KI-Interpretation

Die App verwendet **Ollama** mit dem `minimax-m2.7:cloud` Modell für:
- Gesamte Kompetenzabdeckungsbewertung
- Stärken der Top-Kandidaten
- Identifikation kritischer Kompetenzlücken
- Empfehlungen zur Teamzusammensetzung

**Voraussetzungen**: Ollama muss lokal laufen mit installiertem Modell:
```bash
ollama pull minimax-m2.7:cloud
ollama serve
```

## 🌐 Sprachunterstützung

Umschalten zwischen Sprachen über den Radio-Button in der Seitenleiste:
- 🇬🇧 **English**: Standard-Oberflächensprache
- 🇩🇪 **Deutsch**: Deutsche Übersetzung verfügbar

## 🏗️ Architektur

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

## 📂 Projektstruktur

```
Skill_Matrix/
├── app.py                      # Hauptanwendung (Streamlit)
├── requirements.txt            # Python-Abhängigkeiten
├── README.md                   # Englische Dokumentation
├── README_DE.md                # Diese Datei (Deutsch)
├── FLOWCHART.md                # Technischer Flussplan (Englisch)
├── FLOWCHART_DE.md             # Deutscher Flussplan
├── data/                       # JSON-Datensätze (legacy)
│   ├── consultants.json
│   └── tenders.json
└── docs/                       # CSV-Datendateien (aktiv)
    ├── skills.csv              # HR-Ressourcenpool
    └── tenders_enhanced.csv    # Projektausschreibungen
```

## ⚙️ Konfiguration

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

### Start-Route (Bottle Dashboard)

Endpoint: `POST /start-skill-matrix`
- Authentifizierung erforderlich (Admin)
- Startet Streamlit-App auf Port 8503
- Health-Check mit 20-Sekunden-Timeout

## 🔧 Abhängigkeiten

```txt
streamlit>=1.28.0
pandas>=2.0.0
requests>=2.28.0
```

Installieren:
```bash
pip install -r requirements.txt
```

## 🧪 Testing

### Manuelles Testing
1. App öffnen unter https://gpt.myddns.me/skill-matrix/
2. Ausschreibung TND001 (S/4HANA Finance) auswählen
3. Auf "Passende Berater finden" klicken
4. Überprüfen, ob CV001 (Markus Berger) als Top-Match erscheint
5. KI-Interpretation auf korrekte Anzeige prüfen
6. Sprache auf Deutsch umstellen und Übersetzungen prüfen

### API Testing
```bash
# Health-Endpoint prüfen
curl http://localhost:8503/skill-matrix/_stcore/health

# Start über Dashboard-API
curl -X POST https://gpt.myddns.me/start-skill-matrix \
  -H "Cookie: session_id=IHRE_SESSION" \
  -d ""
```

## 📝 Anwendungsbeispiele

### Anwendungsfall 1: Finance-Projekt
**Ausschreibung**: TND001 - S/4HANA Finance Implementierung
**Top-Match**: CV001 - Markus Berger (FICO-Spezialist, 12 Jahre)
**Fit Score**: 85-95%

### Anwendungsfall 2: Supply Chain Transformation
**Ausschreibung**: TND017 - MM/EWM/IBP End-to-End Transformation
**Top-Matches**: 
- CV020 - Chen Wei (Supply Chain Architekt)
- CV007 - Liam O'Brien (IBP/APO-Spezialist)
- CV006 - Elena Hoffmann (MM/EWM-Spezialist)

### Anwendungsfall 3: Identity Management
**Ausschreibung**: TND004 - SuccessFactors EC & IAS/IPS Setup
**Top-Match**: CV002 - Priya Nair (HCM/SuccessFactors, IAS/IPS-Experte)
**Fit Score**: 90%+

## 🐛 Fehlerbehebung

### 502 Bad Gateway
- **Ursache**: Skill Matrix App läuft nicht
- **Lösung**: "Start"-Button im Dashboard klicken oder manuell starten:
  ```bash
  cd /Users/usermacrtx/Documents/Demos/Skill_Matrix
  streamlit run app.py --server.port=8503 --server.address=0.0.0.0
  ```

### KI-Interpretation zeigt Fehler
- **Ursache**: Ollama läuft nicht oder Modell nicht installiert
- **Lösung**:
  ```bash
  ollama pull minimax-m2.7:cloud
  ollama serve
  ```

### Sprache wechselt nicht
- **Ursache**: Browser-Cache
- **Lösung**: Cookies für gpt.myddns.me löschen oder Inkognito-Modus verwenden

### Start-Button zeigt JSON-Fehler
- **Ursache**: Dashboard-App benötigt Neustart
- **Lösung**: all_demos-App neu starten:
  ```bash
  lsof -ti:8000 | xargs kill -9
  cd /Users/usermacrtx/Documents/Demos/all_demos
  python3 app.py &
  ```

## 📊 Performance

- **Matching-Geschwindigkeit**: < 2 Sekunden für 20 Berater × 20 Ausschreibungen
- **KI-Interpretation**: 5-15 Sekunden (abhängig von LLM-Antwortzeit)
- **Gleichzeitige Benutzer**: Unterstützt 10+ gleichzeitige Benutzer

## 🔐 Sicherheit

- Sitzungsbasierte Authentifizierung über Bottle-Dashboard
- Start/Stopp-Funktionalität nur für Admins
- XSRF-Schutz in Streamlit aktiviert
- HTTPS-Verschlüsselung über Nginx

## 📄 Lizenz

Nur für interne Verwendung - Nicht für externe Verteilung

## 👥 Autoren

Entwickelt für SAP-Berater-Kompetenzmatching und Ausschreibungszuweisungsoptimierung.

## 📞 Support

Bei Problemen oder Feature-Anfragen wenden Sie sich an das Entwicklungsteam.
