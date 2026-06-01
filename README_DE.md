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

### Lokal starten

```bash
# Repository klonen
git clone https://github.com/aicoreml/Skill-Matrix-Match-Simap-Tenders.git
cd Skill-Matrix-Match-Simap-Tenders

# Abhängigkeiten installieren
pip install -r requirements.txt

# App starten (lauscht auf allen Interfaces auf Port 8503)
streamlit run app.py --server.port=8503 --server.address=0.0.0.0
```

Die App ist anschließend unter `http://localhost:8503/` erreichbar.

## 📁 Datenquellen

### Beraterdatenbank (`data/consultants.db`)
Der HR-Ressourcenpool wird in einer SQLite-Datenbank gespeichert. Das Schema wird beim ersten Start automatisch angelegt.

| Spalte | Beschreibung |
|--------|--------------|
| `id` | Berater-ID (Primärschlüssel, z. B. `CV001`) |
| `name` | Vollständiger Name |
| `title` | Jobtitel |
| `years_experience` | Jahre SAP-Erfahrung |
| `location` | Stadt / Land |
| `languages` | Gesprochene Sprachen |
| `skills_sap_modules` | Kommagetrennte SAP-Modulkenntnisse |
| `skills_technical` | Technische Fähigkeiten |
| `skills_project` | Projekt- / Architekturkenntnisse |
| `skills_tools` | Tooling-Kenntnisse |
| `certifications` | SAP- / andere Zertifizierungen |
| `experience` | Beruflicher Werdegang |
| `education` | Ausbildung |
| `summary` | Kurzprofil |
| `specialization` | Primäre Spezialisierung |
| `exp_display` | Vorformatierte Erfahrungsangabe (z. B. `12y`) |
| `key_sap_modules` | Kuratierte Liste der wichtigsten SAP-Module |

### Live-Ausschreibungen
Öffentliche Ausschreibungen werden zur Laufzeit live von **simap.ch** abgerufen — es wird keine statische Ausschreibungsdatei mit der App ausgeliefert.

## 🎯 Funktionsweise

### 1. Live-Ausschreibungen durchsuchen
Klicken Sie in der Seitenleiste auf **"🌐 Live simap.ch Tenders"**, um öffentliche SAP-Ausschreibungen zu durchsuchen.

### 2. Berater matchen
Klicken Sie bei einer Ausschreibung auf **"🎯 Match Consultants"**, um die Kompetenzüberschneidung zu analysieren.

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
│   Nginx Proxy   │────▶│  Auth-Wrapper    │────▶│  Skill Matrix   │
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

## 📂 Projektstruktur

```
Skill_Matrix/
├── app.py                      # Hauptanwendung (Streamlit)
├── requirements.txt            # Python-Abhängigkeiten
├── README.md                   # Englische Dokumentation
├── README_DE.md                # Diese Datei (Deutsch)
├── FLOWCHART.md                # Technischer Flussplan (Englisch)
├── FLOWCHART_DE.md             # Deutscher Flussplan
└── data/
    └── consultants.db          # SQLite-Datenbank (HR-Ressourcenpool)
```

## ⚙️ Deployment

### Nginx Reverse Proxy (Beispiel)

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

> **Hinweis:** Passen Sie `proxy_pass` an Ihren eigenen Host/Port und das `location`-Präfix an den gewünschten Pfad an.

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
1. App lokal starten (`streamlit run app.py …`)
2. `http://localhost:8503/` öffnen
3. In der Seitenleiste auf **"🌐 Live simap.ch Tenders"** klicken
4. Nach einem SAP-Begriff suchen und ein Ergebnis auswählen
5. Bei einer Ausschreibung auf **"🎯 Match Consultants"** klicken
6. Überprüfen, ob Berater und KI-Interpretation korrekt angezeigt werden
7. Sprache auf Deutsch umstellen und Übersetzungen prüfen

### API Testing
```bash
# Health-Endpoint (Streamlit)
curl http://localhost:8503/_stcore/health
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

### Verbindung abgelehnt / 502 Bad Gateway
- **Ursache**: Streamlit-App läuft nicht
- **Lösung**: App starten:
  ```bash
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
- **Lösung**: Seite neu laden (Cmd/Ctrl+Shift+R) oder Inkognito-Fenster verwenden.

## 📊 Performance

- **Matching-Geschwindigkeit**: < 2 Sekunden für 20 Berater × 20 Ausschreibungen
- **KI-Interpretation**: 5-15 Sekunden (abhängig von LLM-Antwortzeit)
- **Gleichzeitige Benutzer**: Unterstützt 10+ gleichzeitige Benutzer

## 🔐 Sicherheitshinweise

- Diese App liest Beraterdaten aus einer lokalen SQLite-Datenbank und bezieht öffentliche Ausschreibungsdaten von `simap.ch`. Für den Matching-Workflow sind keine Schreibzugriffe auf die Datenbank erforderlich.
- Beim Deployment hinter einem Reverse-Proxy sollte eine Authentifizierung ergänzt werden (Basic Auth, OAuth oder ein Wrapper-Dashboard) — die App selbst enthält keine eingebaute Authentifizierung.
- Die Datei `data/consultants.db` enthält personenbezogene Daten (Namen, Standorte, Berufserfahrung). Sie sollte nicht ohne Notwendigkeit in ein öffentliches Repository eingecheckt werden.

## 📄 Lizenz

Nur für interne Verwendung - Nicht für externe Verteilung

## 👥 Autoren

Entwickelt für SAP-Berater-Kompetenzmatching und Ausschreibungszuweisungsoptimierung.

## 📞 Support

Bei Problemen oder Feature-Anfragen wenden Sie sich an das Entwicklungsteam.
