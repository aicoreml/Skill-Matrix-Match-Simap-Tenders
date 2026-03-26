"""
SAP Skill Matrix Match App
Match SAP consultants to project tenders based on skill overlap.
Uses skills.csv (HR resource pool) and tenders_enhanced.csv from docs folder.
Includes Ollama LLM (minimax-m2.7:cloud) for result interpretation.
Supports English and German UI languages.
"""

import json
import streamlit as st
import pandas as pd
from typing import Any
import os
import requests

# =============================================================================
# Translations
# =============================================================================

TRANSLATIONS = {
    "en": {
        "app_title": "🎯 SAP Skill Matrix Match",
        "app_subtitle": "Select a tender to find the best matching consultants from the HR resource pool based on skill overlap.",
        "sidebar": {
            "resource_pool": "✅ Loaded {count} consultants from HR resource pool",
            "tenders_loaded": "📋 Loaded {count} tenders",
            "select_tender": "📋 Select Tender",
            "choose_tender": "Choose a tender:",
            "about_title": "ℹ️ About This App",
            "about_content": """
This app matches SAP consultants from the **HR resource pool** (skills.csv) 
to project **tenders** (tenders_enhanced.csv) based on:

- **🔴 Mandatory skills** (required, weighted 2x)
- **🟢 Optional skills** (bonus skills)

The **Fit Score** is calculated as:
```
(2×mandatory_matched + optional_matched) 
--------------------------------------- × 100
(2×mandatory_total + optional_total)
```

**Color coding:**
- 🟢 Excellent (≥80%): Strong skill coverage
- 🟠 Good (50-79%): Partial match, some gaps
- 🔴 Low (<50%): Significant skill gaps
""",
        },
        "tender_details": "### 📋 Tender Details",
        "industry": "Industry",
        "duration": "Duration",
        "location": "Location",
        "team_size": "Team Size",
        "description": "**Description:**",
        "key_deliverables": "📦 Key Deliverables",
        "success_criteria": "✅ Success Criteria",
        "mandatory_skills": "**🔴 Mandatory Skills:**",
        "optional_skills": "**🟢 Optional Skills:**",
        "additional_info": "ℹ️ Additional Tender Information",
        "client": "Client",
        "contract_type": "Contract Type",
        "seniority": "Seniority",
        "languages": "Languages",
        "budget": "Budget",
        "start_date": "Start Date",
        "matching_results": "### 🎯 Matching Results",
        "find_consultants": "🔍 Find Matching Consultants",
        "analyzing": "Analyzing skill matches...",
        "total_consultants": "Total Consultants",
        "excellent_match": "Excellent Match (≥80%)",
        "good_match": "Good Match (50-79%)",
        "low_match": "Low Match (<50%)",
        "top_consultants": "### 👥 Top Matching Consultants",
        "all_results": "### 📊 All Results Table",
        "download_csv": "📥 Download Results as CSV",
        "ai_interpretation": "### 🤖 AI Interpretation (Ollama)",
        "consulting_ai": "🤖 Consulting AI for analysis...",
        "no_match": "No matching consultants found for this tender.",
        "consultant_table_cols": ["ID", "Name", "Specialization", "Experience", "Fit Score %", "Mandatory %", "Matched Mandatory", "Matched Optional"],
        "exp": "exp.",
        "skills": "**Skills:**",
        "mandatory_skills_label": "**🔴 Mandatory Skills**",
        "optional_skills_label": "**🟢 Optional Skills**",
        "matched": "matched",
        "missing": "Missing:",
        "excellent": "Excellent Match",
        "good": "Good Match",
        "low": "Low Match",
    },
    "de": {
        "app_title": "🎯 SAP Skill Matrix Match",
        "app_subtitle": "Wählen Sie eine Ausschreibung, um die am besten passenden Berater aus dem HR-Ressourcenpool basierend auf der Kompetenzüberschneidung zu finden.",
        "sidebar": {
            "resource_pool": "✅ {count} Berater aus dem HR-Ressourcenpool geladen",
            "tenders_loaded": "📋 {count} Ausschreibungen geladen",
            "select_tender": "📋 Ausschreibung wählen",
            "choose_tender": "Ausschreibung auswählen:",
            "about_title": "ℹ️ Über diese App",
            "about_content": """
Diese App matcht SAP-Berater aus dem **HR-Ressourcenpool** (skills.csv) 
mit Projekt-**Ausschreibungen** (tenders_enhanced.csv) basierend auf:

- **🔴 Pflichtfähigkeiten** (erforderlich, 2-fach gewichtet)
- **🟢 Optionale Fähigkeiten** (Bonusfähigkeiten)

Der **Fit Score** wird berechnet als:
```
(2×gefundene_pflicht + gefundene_optional) 
--------------------------------------- × 100
(2×gesamt_pflicht + gesamt_optional)
```

**Farbcodierung:**
- 🟢 Excellent (≥80%): Starke Kompetenzabdeckung
- 🟠 Good (50-79%): Teilweise Übereinstimmung, einige Lücken
- 🔴 Low (<50%): Erhebliche Kompetenzlücken
""",
        },
        "tender_details": "### 📋 Details zur Ausschreibung",
        "industry": "Branche",
        "duration": "Dauer",
        "location": "Standort",
        "team_size": "Teamgröße",
        "description": "**Beschreibung:**",
        "key_deliverables": "📦 Hauptliefergegenstände",
        "success_criteria": "✅ Erfolgskriterien",
        "mandatory_skills": "**🔴 Pflichtfähigkeiten:**",
        "optional_skills": "**🟢 Optionale Fähigkeiten:**",
        "additional_info": "ℹ️ Zusätzliche Informationen",
        "client": "Kunde",
        "contract_type": "Vertragstyp",
        "seniority": "Erfahrungslevel",
        "languages": "Sprachen",
        "budget": "Budget",
        "start_date": "Startdatum",
        "matching_results": "### 🎯 Matching-Ergebnisse",
        "find_consultants": "🔍 Passende Berater finden",
        "analyzing": "Analysiere Kompetenzüberschneidungen...",
        "total_consultants": "Gesamtberater",
        "excellent_match": "Excellent Match (≥80%)",
        "good_match": "Good Match (50-79%)",
        "low_match": "Low Match (<50%)",
        "top_consultants": "### 👥 Top passende Berater",
        "all_results": "### 📊 Alle Ergebnisse",
        "download_csv": "📥 Ergebnisse als CSV herunterladen",
        "ai_interpretation": "### 🤖 KI-Interpretation (Ollama)",
        "consulting_ai": "🤖 KI-Analyse wird angefordert...",
        "no_match": "Keine passenden Berater für diese Ausschreibung gefunden.",
        "consultant_table_cols": ["ID", "Name", "Spezialisierung", "Erfahrung", "Fit Score %", "Pflicht %", "Gefundene Pflicht", "Gefundene Optional"],
        "exp": "Erf.",
        "skills": "**Fähigkeiten:**",
        "mandatory_skills_label": "**🔴 Pflichtfähigkeiten**",
        "optional_skills_label": "**🟢 Optionale Fähigkeiten**",
        "matched": "gefunden",
        "missing": "Fehlend:",
        "excellent": "Excellent Match",
        "good": "Good Match",
        "low": "Low Match",
    },
}


def get_text(key: str, lang: str = "en") -> str:
    """Get translated text."""
    keys = key.split(".")
    value = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, key)
        else:
            return key
    return value


def language_selector():
    """Add language selector to sidebar."""
    st.sidebar.markdown("---")
    lang = st.sidebar.radio(
        "🌐 Sprache / Language",
        options=["en", "de"],
        format_func=lambda x: "🇬🇧 English" if x == "en" else "🇩🇪 Deutsch",
        index=0 if st.session_state.get("language", "en") == "en" else 1,
    )
    st.session_state.language = lang
    return lang


def query_ollama(prompt: str, model: str = "minimax-m2.7:cloud") -> str:
    """Query Ollama LLM for interpretation."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get("response", "No response from LLM")
        elif response.status_code == 404:
            return f"⚠️ Model '{model}' not found. Available models: run 'ollama list' to check."
        else:
            return f"LLM error: HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama is not running. Please start Ollama service."
    except requests.exceptions.Timeout:
        return "⚠️ LLM request timed out. Please try again."
    except Exception as e:
        return f"⚠️ LLM error: {str(e)}"


def generate_llm_interpretation(tender: pd.Series, results: list[dict[str, Any]], lang: str = "en") -> str:
    """Generate LLM interpretation of matching results."""
    top_3 = results[:3]
    
    # Add language instruction to prompt
    lang_instruction = "Please respond in German." if lang == "de" else "Please respond in English."
    
    prompt = f"""
Analyze the following SAP consultant matching results for a tender and provide a brief interpretation.
{lang_instruction}

TENDER: {tender.get('title', 'N/A')}
Industry: {tender.get('industry', 'N/A')}
Location: {tender.get('location', 'N/A')}
Duration: {tender.get('duration', 'N/A')}

Mandatory Skills Required: {tender.get('mandatory_skills', 'N/A')}
Optional Skills Required: {tender.get('optional_skills', 'N/A')}

TOP 3 MATCHING CONSULTANTS:
"""
    
    for i, match in enumerate(top_3, 1):
        prompt += f"""
{i}. {match['consultant_name']} ({match['consultant_id']})
   Specialization: {match['consultant_title']}
   Experience: {match['years_experience']}
   Fit Score: {match['weighted_fit_score']:.1f}%
   Matched Mandatory: {', '.join(match['matched_mandatory_skills']) if match['matched_mandatory_skills'] else 'None'}
   Matched Optional: {', '.join(match['matched_optional_skills']) if match['matched_optional_skills'] else 'None'}
   Missing Mandatory: {', '.join(match['missing_mandatory_skills']) if match['missing_mandatory_skills'] else 'None'}
"""

    prompt += """

Provide a concise interpretation (max 200 words) covering:
1. Overall skill coverage assessment for this tender
2. Strengths of the top candidates
3. Any critical skill gaps in the team
4. Recommendation for team composition
"""

    return query_ollama(prompt)


def load_consultants(file_path: str = "docs/skills.csv") -> pd.DataFrame:
    """Load consultant profiles from CSV file."""
    df = pd.read_csv(file_path)
    # Parse skills into list
    df['skills_list'] = df['Key SAP Modules'].apply(
        lambda x: [s.strip() for s in str(x).split(',')] if pd.notna(x) else []
    )
    return df


def load_tenders(file_path: str = "docs/tenders_enhanced.csv") -> pd.DataFrame:
    """Load tender profiles from CSV file."""
    df = pd.read_csv(file_path)
    # Parse mandatory and optional skills into lists
    df['mandatory_skills_list'] = df['mandatory_skills'].apply(
        lambda x: [s.strip() for s in str(x).split('|')] if pd.notna(x) else []
    )
    df['optional_skills_list'] = df['optional_skills'].apply(
        lambda x: [s.strip() for s in str(x).split('|')] if pd.notna(x) else []
    )
    return df


def normalize_skill(skill: str) -> str:
    """Normalize a skill string for matching."""
    return skill.lower().strip()


def match_skills(
    consultant: pd.Series, tender: pd.Series
) -> dict[str, Any]:
    """
    Match consultant skills against tender requirements.
    Returns match details including percentages and matched skills.
    """
    consultant_skills = set(normalize_skill(s) for s in consultant['skills_list'])

    mandatory_skills = [normalize_skill(s) for s in tender['mandatory_skills_list']]
    optional_skills = [normalize_skill(s) for s in tender['optional_skills_list']]

    # Find matches (exact + partial)
    matched_mandatory = []
    matched_optional = []

    for skill in mandatory_skills:
        # Exact match
        if skill in consultant_skills:
            matched_mandatory.append(skill)
        else:
            # Fuzzy match - check if any consultant skill contains the tender skill
            for c_skill in consultant_skills:
                if skill in c_skill or c_skill in skill:
                    matched_mandatory.append(skill)
                    break

    for skill in optional_skills:
        if skill in consultant_skills:
            matched_optional.append(skill)
        else:
            for c_skill in consultant_skills:
                if skill in c_skill or c_skill in skill:
                    matched_optional.append(skill)
                    break

    # Remove duplicates
    matched_mandatory = list(set(matched_mandatory))
    matched_optional = list(set(matched_optional))

    # Calculate percentages
    mandatory_total = len(mandatory_skills)
    optional_total = len(optional_skills)

    mandatory_match_pct = (
        (len(matched_mandatory) / mandatory_total * 100) if mandatory_total > 0 else 0
    )
    optional_match_pct = (
        (len(matched_optional) / optional_total * 100) if optional_total > 0 else 0
    )

    # Weighted fit score (mandatory skills count double)
    total_weighted = 2 * mandatory_total + optional_total
    matched_weighted = 2 * len(matched_mandatory) + len(matched_optional)
    weighted_fit_score = (
        (matched_weighted / total_weighted * 100) if total_weighted > 0 else 0
    )

    # Get original skill names for display
    matched_mandatory_display = []
    for skill in matched_mandatory:
        for orig_skill in consultant['skills_list']:
            if skill == normalize_skill(orig_skill):
                matched_mandatory_display.append(orig_skill)
                break
        else:
            matched_mandatory_display.append(skill.title())

    matched_optional_display = []
    for skill in matched_optional:
        for orig_skill in consultant['skills_list']:
            if skill == normalize_skill(orig_skill):
                matched_optional_display.append(orig_skill)
                break
        else:
            matched_optional_display.append(skill.title())

    missing_mandatory = [s for s in mandatory_skills if s not in matched_mandatory]
    missing_optional = [s for s in optional_skills if s not in matched_optional]

    return {
        "consultant_id": consultant['ID'],
        "consultant_name": consultant['Name'],
        "consultant_title": consultant['Specialization'],
        "years_experience": consultant['Exp'],
        "skills": consultant['Key SAP Modules'],
        "mandatory_total": mandatory_total,
        "mandatory_matched": len(matched_mandatory),
        "mandatory_match_pct": mandatory_match_pct,
        "optional_total": optional_total,
        "optional_matched": len(matched_optional),
        "optional_match_pct": optional_match_pct,
        "weighted_fit_score": weighted_fit_score,
        "matched_mandatory_skills": matched_mandatory_display,
        "matched_optional_skills": matched_optional_display,
        "missing_mandatory_skills": [s.title() for s in missing_mandatory],
        "missing_optional_skills": [s.title() for s in missing_optional],
    }


def check_language_match(
    consultant_languages: list[str], required_languages: list[str]
) -> bool:
    """Check if consultant speaks at least one required language."""
    if not required_languages:
        return True
    consultant_lang_lower = [lang.lower() for lang in consultant_languages]
    required_lang_lower = [lang.lower() for lang in required_languages]
    return any(lang in consultant_lang_lower for lang in required_lang_lower)


def match_consultants_to_tender(
    consultants_df: pd.DataFrame, tender: pd.Series
) -> list[dict[str, Any]]:
    """Match all consultants to a single tender and return sorted results."""
    results = []

    for _, consultant in consultants_df.iterrows():
        match_result = match_skills(consultant, tender)
        results.append(match_result)

    # Sort by weighted fit score (descending)
    results.sort(key=lambda x: x["weighted_fit_score"], reverse=True)
    return results


def display_consultant_card(match: dict[str, Any], rank: int, lang: str = "en") -> None:
    """Display a consultant match card with styling."""
    score = match["weighted_fit_score"]

    # Determine color based on score
    if score >= 80:
        color = "green"
        emoji = "✅"
        label = get_text("excellent", lang)
    elif score >= 50:
        color = "orange"
        emoji = "⚠️"
        label = get_text("good", lang)
    else:
        color = "red"
        emoji = "❌"
        label = get_text("low", lang)

    # Use Streamlit columns for layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### #{rank} {match['consultant_name']}")
        st.markdown(f"**{match['consultant_title']}**")
        st.markdown(f"⏱️ {match['years_experience']} {get_text('exp', lang)}")
        st.markdown(f"📚 {get_text('skills', lang)} {match['skills']}")
    
    with col2:
        st.markdown(f"## {score:.1f}%")
        st.caption(f"{label} {emoji}")
    
    st.markdown("---")
    
    # Skills breakdown
    col_mand, col_opt = st.columns(2)
    
    with col_mand:
        st.markdown(get_text("mandatory_skills_label", lang))
        st.markdown(f"**{match['mandatory_matched']}/{match['mandatory_total']}** {get_text('matched', lang)} ({match['mandatory_match_pct']:.0f}%)")
        if match['matched_mandatory_skills']:
            st.success(f"✓ {', '.join(match['matched_mandatory_skills'])}")
        if match['missing_mandatory_skills']:
            st.error(f"{get_text('missing', lang)} {', '.join(match['missing_mandatory_skills'])}")
    
    with col_opt:
        st.markdown(get_text("optional_skills_label", lang))
        st.markdown(f"**{match['optional_matched']}/{match['optional_total']}** {get_text('matched', lang)} ({match['optional_match_pct']:.0f}%)")
        if match['matched_optional_skills']:
            st.info(f"+ {', '.join(match['matched_optional_skills'])}")
    
    st.markdown("<br>", unsafe_allow_html=True)


def main():
    # Initialize session state for language
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    st.set_page_config(
        page_title="SAP Skill Matrix Match",
        page_icon="🎯",
        layout="wide",
    )

    # Language selector
    lang = language_selector()
    
    # Get translations
    t = lambda key: get_text(key, lang)

    st.title(t("app_title"))
    st.markdown(t("app_subtitle"))

    # Load data
    skills_file = "docs/skills.csv"
    tenders_file = "docs/tenders_enhanced.csv"

    # Check if files exist
    if not os.path.exists(skills_file):
        st.error(f"❌ Skills file not found: {skills_file}")
        st.stop()
    
    if not os.path.exists(tenders_file):
        st.error(f"❌ Tenders file not found: {tenders_file}")
        st.stop()

    try:
        consultants_df = load_consultants(skills_file)
        st.sidebar.success(t("sidebar.resource_pool").format(count=len(consultants_df)))
    except Exception as e:
        st.error(f"Error loading consultants: {str(e)}")
        st.stop()

    try:
        tenders_df = load_tenders(tenders_file)
        st.sidebar.info(t("sidebar.tenders_loaded").format(count=len(tenders_df)))
    except Exception as e:
        st.error(f"Error loading tenders: {str(e)}")
        st.stop()

    # Tender selection
    st.sidebar.markdown("---")
    st.sidebar.subheader(t("sidebar.select_tender"))

    tender_options = {
        f"{row['id']}: {row['title']}": row
        for _, row in tenders_df.iterrows()
    }

    selected_tender_name = st.sidebar.selectbox(
        t("sidebar.choose_tender"),
        options=list(tender_options.keys()),
    )

    if selected_tender_name:
        selected_tender = tender_options[selected_tender_name]

        # Display tender details
        st.markdown(t("tender_details"))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t("industry"), selected_tender.get("industry", "N/A"))
        with col2:
            st.metric(t("duration"), selected_tender.get("duration", "N/A"))
        with col3:
            st.metric(t("location"), selected_tender.get("location", "N/A"))
        with col4:
            st.metric(t("team_size"), selected_tender.get("team_size", "N/A"))

        # Description
        description = selected_tender.get("description", "No description available.")
        st.markdown(f"{t('description')} {description}")

        # Key deliverables
        deliverables = selected_tender.get("key_deliverables", "N/A")
        with st.expander(t("key_deliverables")):
            st.write(deliverables.replace('|', '\n- '))

        # Success criteria
        success = selected_tender.get("success_criteria", "N/A")
        with st.expander(t("success_criteria")):
            st.write(success.replace('|', '\n- '))

        # Required skills
        col1, col2 = st.columns(2)
        with col1:
            mandatory = selected_tender.get("mandatory_skills", "N/A")
            st.markdown(
                f"""
                {t('mandatory_skills')}
                
                {mandatory.replace('|', '\n- ')}
                """
            )
        with col2:
            optional = selected_tender.get("optional_skills", "N/A")
            st.markdown(
                f"""
                {t('optional_skills')}
                
                {optional.replace('|', '\n- ')}
                """
            )

        # Additional info
        with st.expander(t("additional_info")):
            st.markdown(f"""
            - **{t('client')}:** {selected_tender.get('client', 'N/A')}
            - **{t('contract_type')}:** {selected_tender.get('contract_type', 'N/A')}
            - **{t('seniority')}:** {selected_tender.get('seniority', 'N/A')}
            - **{t('languages')}:** {selected_tender.get('languages', 'N/A')}
            - **{t('budget')}:** {selected_tender.get('budget_range', 'N/A')}
            - **{t('start_date')}:** {selected_tender.get('start_date', 'N/A')}
            """)

        # Perform matching
        st.markdown("---")
        st.markdown(t("matching_results"))

        if st.button(t("find_consultants"), type="primary"):
            with st.spinner(t("analyzing")):
                results = match_consultants_to_tender(consultants_df, selected_tender)

            # Summary metrics
            total_consultants = len(results)
            high_match = sum(1 for r in results if r["weighted_fit_score"] >= 80)
            medium_match = sum(
                1 for r in results if 50 <= r["weighted_fit_score"] < 80
            )
            low_match = sum(1 for r in results if r["weighted_fit_score"] < 50)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(t("total_consultants"), total_consultants)
            with col2:
                st.metric(t("excellent_match"), high_match)
            with col3:
                st.metric(t("good_match"), medium_match)
            with col4:
                st.metric(t("low_match"), low_match)

            st.markdown("---")

            # Show top matches
            st.markdown(t("top_consultants"))

            # Filter to show only consultants with score > 0
            qualified_results = [r for r in results if r["weighted_fit_score"] > 0]

            if qualified_results:
                # Show top 5 in detail
                for i, match in enumerate(qualified_results[:5], 1):
                    display_consultant_card(match, i, lang)

                # Show full table
                st.markdown("---")
                st.markdown(t("all_results"))

                df = pd.DataFrame(results)
                display_df = df[
                    [
                        "consultant_id",
                        "consultant_name",
                        "consultant_title",
                        "years_experience",
                        "weighted_fit_score",
                        "mandatory_match_pct",
                        "matched_mandatory_skills",
                        "matched_optional_skills",
                    ]
                ]
                
                # Rename columns for display
                display_df.columns = t("consultant_table_cols")

                # Format for display - use positional access to avoid column name issues
                display_df.iloc[:, 4] = display_df.iloc[:, 4].round(1)  # Fit Score %
                display_df.iloc[:, 5] = display_df.iloc[:, 5].round(0)  # Mandatory %

                st.dataframe(display_df, use_container_width=True, hide_index=True)

                # LLM Interpretation
                st.markdown("---")
                st.markdown(t("ai_interpretation"))
                
                with st.spinner(t("consulting_ai")):
                    llm_interpretation = generate_llm_interpretation(selected_tender, results, lang)
                
                st.markdown(llm_interpretation)

                # Download option
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label=t("download_csv"),
                    data=csv,
                    file_name=f"match_results_{selected_tender['id']}.csv",
                    mime="text/csv",
                )
            else:
                st.warning(t("no_match"))

    # About section
    st.sidebar.markdown("---")
    st.sidebar.markdown(t("sidebar.about_title"))
    st.sidebar.markdown(t("sidebar.about_content"))


if __name__ == "__main__":
    main()
