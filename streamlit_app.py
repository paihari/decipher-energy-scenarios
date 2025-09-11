"""
Swiss Energy Scenarios Decipher System - Multilingual Streamlit Web Interface
"""

import streamlit as st
import asyncio
import sys
import os
from typing import Dict, Any
import pandas as pd

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.config import config
from agents.orchestrator_agent import OrchestratorAgent
from agents.data_interpreter_agent import DataInterpreterAgent
from agents.scenario_analyst_agent import ScenarioAnalystAgent
from agents.document_intelligence_agent import DocumentIntelligenceAgent
from agents.policy_context_agent import PolicyContextAgent
from agents.language_translator_agent import LanguageTranslatorAgent

# Language translations
TRANSLATIONS = {
    "en": {
        "title": "🇨🇭 Swiss Energy Scenarios Decipher System",
        "subtitle": "*Making Swiss energy transition data accessible to everyone*",
        "language": "Language",
        "user_profile": "🎯 User Profile",
        "who_are_you": "Who are you?",
        "user_help": "This helps us tailor our responses to your needs",
        "multilingual_note": "💡 You can ask questions in any language - English, German, French, or Italian!",
        "available_agents": "🤖 Available Agents",
        "agents_desc": """
- **📊 Data Interpreter**: Statistics & trends
- **🔮 Scenario Analyst**: Compare pathways  
- **📄 Document Intelligence**: Technical reports
- **🏛️ Policy Context**: Regulations & implementation
        """,
        "example_queries": "💡 Example Queries",
        "try_example": "Try an example:",
        "use_example": "Use Example",
        "ask_question": "💬 Ask Your Question", 
        "enter_question": "Enter your question about Swiss energy scenarios:",
        "placeholder": "e.g., How do emissions change in the ZERO scenario?",
        "analyze": "🔄 Analyze",
        "quick_stats": "📈 Quick Stats",
        "data_files": "Data Files",
        "synthesis_files": "Synthesis Files", 
        "transformation_files": "Transformation Files",
        "data_range": "Data Range",
        "conversation_history": "📝 Conversation History",
        "answer": "**Answer:**",
        "confidence": "Confidence",
        "sources": "**Sources:**",
        "suggestions": "**Suggestions:**",
        "processing": "🔄 Processing your query as {}...",
        "analysis_complete": "✅ Analysis Complete!",
        "response": "🎯 Answer",
        "data_sources": "**📊 Data Sources:**",
        "followup_ideas": "**💡 Follow-up Ideas:**",
        "analysis_details": "🧠 Analysis Details",
        "error_processing": "❌ Error processing query: {}",
        "check_config": "Please check your configuration and try again.",
        "error_loading": "Error loading system info: {}",
        "user_types": {
            "citizen": "Citizen",
            "journalist": "Journalist", 
            "student": "Student",
            "policymaker": "Policymaker"
        },
        "examples": [
            "What are Switzerland's CO2 emissions in 2030?",
            "Compare ZERO vs WWB scenarios",
            "How does transport electrification progress?",
            "What policies support renewable energy?",
            "Explain the methodology used in scenarios"
        ]
    },
    "de": {
        "title": "🇨🇭 Schweizer Energieszenarien Entschlüssler-System",
        "subtitle": "*Schweizer Energiewende-Daten für alle zugänglich machen*",
        "language": "Sprache",
        "user_profile": "🎯 Benutzerprofil",
        "who_are_you": "Wer sind Sie?",
        "user_help": "Dies hilft uns, unsere Antworten auf Ihre Bedürfnisse zuzuschneiden",
        "multilingual_note": "💡 Sie können Fragen in jeder Sprache stellen - Deutsch, Englisch, Französisch oder Italienisch!",
        "available_agents": "🤖 Verfügbare Agenten",
        "agents_desc": """
- **📊 Daten-Interpreter**: Statistiken & Trends
- **🔮 Szenario-Analyst**: Entwicklungspfade vergleichen
- **📄 Dokument-Intelligence**: Technische Berichte
- **🏛️ Policy-Kontext**: Regulierung & Umsetzung
        """,
        "example_queries": "💡 Beispiel-Anfragen",
        "try_example": "Probieren Sie ein Beispiel:",
        "use_example": "Beispiel verwenden",
        "ask_question": "💬 Stellen Sie Ihre Frage",
        "enter_question": "Geben Sie Ihre Frage zu Schweizer Energieszenarien ein:",
        "placeholder": "z.B. Wie entwickeln sich die Emissionen im ZERO-Szenario?",
        "analyze": "🔄 Analysieren",
        "quick_stats": "📈 Schnell-Statistiken",
        "data_files": "Datendateien",
        "synthesis_files": "Synthese-Dateien",
        "transformation_files": "Transformations-Dateien", 
        "data_range": "Datenbereich",
        "conversation_history": "📝 Gesprächsverlauf",
        "answer": "**Antwort:**",
        "confidence": "Vertrauen",
        "sources": "**Quellen:**",
        "suggestions": "**Vorschläge:**",
        "processing": "🔄 Ihre Anfrage wird als {} verarbeitet...",
        "analysis_complete": "✅ Analyse abgeschlossen!",
        "response": "🎯 Antwort",
        "data_sources": "**📊 Datenquellen:**",
        "followup_ideas": "**💡 Weitere Ideen:**",
        "analysis_details": "🧠 Analyse-Details",
        "error_processing": "❌ Fehler bei der Verarbeitung der Anfrage: {}",
        "check_config": "Bitte überprüfen Sie Ihre Konfiguration und versuchen Sie es erneut.",
        "error_loading": "Fehler beim Laden der Systeminfo: {}",
        "user_types": {
            "citizen": "Bürgerin/Bürger",
            "journalist": "Journalistin/Journalist",
            "student": "Studentin/Student", 
            "policymaker": "Politikerin/Politiker"
        },
        "examples": [
            "Wie hoch sind die CO2-Emissionen der Schweiz 2030?",
            "Vergleiche ZERO- mit WWB-Szenario",
            "Wie entwickelt sich die Elektromobilität?",
            "Welche Politiken fördern erneuerbare Energien?",
            "Erkläre die verwendete Methodik in den Szenarien"
        ]
    },
    "fr": {
        "title": "🇨🇭 Système de Décryptage des Scénarios Énergétiques Suisses",
        "subtitle": "*Rendre les données de transition énergétique suisse accessibles à tous*",
        "language": "Langue",
        "user_profile": "🎯 Profil Utilisateur",
        "who_are_you": "Qui êtes-vous ?",
        "user_help": "Cela nous aide à adapter nos réponses à vos besoins",
        "multilingual_note": "💡 Vous pouvez poser des questions dans n'importe quelle langue - français, anglais, allemand ou italien !",
        "available_agents": "🤖 Agents Disponibles",
        "agents_desc": """
- **📊 Interpréteur de Données**: Statistiques & tendances
- **🔮 Analyste de Scénarios**: Comparer les trajectoires
- **📄 Intelligence Documentaire**: Rapports techniques
- **🏛️ Contexte Politique**: Réglementations & mise en œuvre
        """,
        "example_queries": "💡 Exemples de Requêtes",
        "try_example": "Essayez un exemple :",
        "use_example": "Utiliser l'Exemple",
        "ask_question": "💬 Posez Votre Question",
        "enter_question": "Saisissez votre question sur les scénarios énergétiques suisses :",
        "placeholder": "ex. Comment évoluent les émissions dans le scénario ZERO ?",
        "analyze": "🔄 Analyser",
        "quick_stats": "📈 Statistiques Rapides",
        "data_files": "Fichiers de Données",
        "synthesis_files": "Fichiers de Synthèse",
        "transformation_files": "Fichiers de Transformation",
        "data_range": "Plage de Données",
        "conversation_history": "📝 Historique des Conversations",
        "answer": "**Réponse :**",
        "confidence": "Confiance",
        "sources": "**Sources :**",
        "suggestions": "**Suggestions :**",
        "processing": "🔄 Traitement de votre requête en tant que {}...",
        "analysis_complete": "✅ Analyse Terminée !",
        "response": "🎯 Réponse",
        "data_sources": "**📊 Sources de Données :**",
        "followup_ideas": "**💡 Idées de Suite :**",
        "analysis_details": "🧠 Détails de l'Analyse",
        "error_processing": "❌ Erreur lors du traitement de la requête : {}",
        "check_config": "Veuillez vérifier votre configuration et réessayer.",
        "error_loading": "Erreur lors du chargement des informations système : {}",
        "user_types": {
            "citizen": "Citoyen/ne",
            "journalist": "Journaliste",
            "student": "Étudiant/e",
            "policymaker": "Décideur/se Politique"
        },
        "examples": [
            "Quelles sont les émissions de CO2 de la Suisse en 2030 ?",
            "Comparer les scénarios ZERO vs WWB",
            "Comment progresse l'électrification des transports ?",
            "Quelles politiques soutiennent les énergies renouvelables ?",
            "Expliquer la méthodologie utilisée dans les scénarios"
        ]
    },
    "it": {
        "title": "🇨🇭 Sistema di Decrittazione degli Scenari Energetici Svizzeri",
        "subtitle": "*Rendere i dati di transizione energetica svizzera accessibili a tutti*",
        "language": "Lingua",
        "user_profile": "🎯 Profilo Utente",
        "who_are_you": "Chi sei?",
        "user_help": "Questo ci aiuta ad adattare le nostre risposte alle tue esigenze",
        "multilingual_note": "💡 Puoi fare domande in qualsiasi lingua - italiano, inglese, tedesco o francese!",
        "available_agents": "🤖 Agenti Disponibili",
        "agents_desc": """
- **📊 Interprete dei Dati**: Statistiche & tendenze
- **🔮 Analista di Scenari**: Confrontare i percorsi
- **📄 Intelligenza Documentale**: Rapporti tecnici
- **🏛️ Contesto Politico**: Regolamentazioni & implementazione
        """,
        "example_queries": "💡 Esempi di Query",
        "try_example": "Prova un esempio:",
        "use_example": "Usa Esempio",
        "ask_question": "💬 Fai la Tua Domanda",
        "enter_question": "Inserisci la tua domanda sugli scenari energetici svizzeri:",
        "placeholder": "es. Come cambiano le emissioni nello scenario ZERO?",
        "analyze": "🔄 Analizza",
        "quick_stats": "📈 Statistiche Veloci",
        "data_files": "File di Dati",
        "synthesis_files": "File di Sintesi",
        "transformation_files": "File di Trasformazione",
        "data_range": "Intervallo di Dati",
        "conversation_history": "📝 Cronologia Conversazioni",
        "answer": "**Risposta:**",
        "confidence": "Confidenza",
        "sources": "**Fonti:**",
        "suggestions": "**Suggerimenti:**",
        "processing": "🔄 Elaborazione della tua richiesta come {}...",
        "analysis_complete": "✅ Analisi Completata!",
        "response": "🎯 Risposta",
        "data_sources": "**📊 Fonti di Dati:**",
        "followup_ideas": "**💡 Idee di Seguito:**",
        "analysis_details": "🧠 Dettagli dell'Analisi",
        "error_processing": "❌ Errore nell'elaborazione della richiesta: {}",
        "check_config": "Controlla la tua configurazione e riprova.",
        "error_loading": "Errore nel caricamento delle informazioni di sistema: {}",
        "user_types": {
            "citizen": "Cittadino/a",
            "journalist": "Giornalista",
            "student": "Studente/essa",
            "policymaker": "Responsabile Politico/a"
        },
        "examples": [
            "Quali sono le emissioni di CO2 della Svizzera nel 2030?",
            "Confronta gli scenari ZERO vs WWB",
            "Come progredisce l'elettrificazione dei trasporti?",
            "Quali politiche supportano le energie rinnovabili?",
            "Spiega la metodologia utilizzata negli scenari"
        ]
    }
}

# Configure Streamlit page
st.set_page_config(
    page_title="Swiss Energy Scenarios Decipher",
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_text(key: str, lang: str = "en") -> str:
    """Get translated text for the given key and language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

@st.cache_resource
def initialize_agents():
    """Initialize all agents - cached for performance."""
    config.validate()
    
    # Initialize specialist agents
    data_interpreter = DataInterpreterAgent(config.openai_api_key, config.data_path)
    scenario_analyst = ScenarioAnalystAgent(config.openai_api_key, config.data_path)
    document_intelligence = DocumentIntelligenceAgent(config.openai_api_key, config.reports_path)
    policy_context = PolicyContextAgent(config.openai_api_key)
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent(config.openai_api_key)
    orchestrator.register_agent(data_interpreter)
    orchestrator.register_agent(scenario_analyst)
    orchestrator.register_agent(document_intelligence)
    orchestrator.register_agent(policy_context)
    
    return orchestrator

def main():
    """Main Streamlit application."""
    
    # Initialize language in session state
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    # Header with logos
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        try:
            st.image("images/enregy-center.jpg", width=150)
        except:
            st.write("⚡")  # Fallback if image not found
    
    with col2:
        st.title(get_text("title", st.session_state.language))
        st.markdown(get_text("subtitle", st.session_state.language))
    
    with col3:
        try:
            st.image("images/ETH-Logo.jpg", width=150)
        except:
            st.write("🏛️")  # Fallback if image not found
    
    # Sidebar
    with st.sidebar:
        st.header(get_text("user_profile", st.session_state.language))
        
        user_types = get_text("user_types", st.session_state.language)
        user_type = st.selectbox(
            get_text("who_are_you", st.session_state.language),
            options=list(user_types.keys()),
            format_func=lambda x: user_types[x],
            index=0,
            help=get_text("user_help", st.session_state.language)
        )
        
        # Multilingual support note
        st.info(get_text("multilingual_note", st.session_state.language))
        
        st.header(get_text("available_agents", st.session_state.language))
        st.markdown(get_text("agents_desc", st.session_state.language))
        
        st.header(get_text("example_queries", st.session_state.language))
        examples = get_text("examples", st.session_state.language)
        
        selected_example = st.selectbox(
            get_text("try_example", st.session_state.language),
            options=[""] + examples,
            index=0
        )
        
        if selected_example and st.button(get_text("use_example", st.session_state.language)):
            st.session_state.query_input = selected_example
        
        # Language selector at bottom of sidebar
        st.markdown("---")
        lang = st.selectbox(
            "🌍 " + get_text("language", st.session_state.language),
            options=["en", "de", "fr", "it"],
            format_func=lambda x: "🇬🇧 English" if x == "en" else "🇩🇪 Deutsch" if x == "de" else "🇫🇷 Français" if x == "fr" else "🇮🇹 Italiano",
            index=0 if st.session_state.language == "en" else (1 if st.session_state.language == "de" else (2 if st.session_state.language == "fr" else 3)),
            key="lang_selector"
        )
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(get_text("ask_question", st.session_state.language))
        
        # Query input
        query = st.text_area(
            get_text("enter_question", st.session_state.language),
            height=100,
            key="query_input",
            placeholder=get_text("placeholder", st.session_state.language)
        )
        
        # Process button
        if st.button(get_text("analyze", st.session_state.language), disabled=not query.strip()):
            if query.strip():
                process_query(query.strip(), user_type, st.session_state.language)
    
    with col2:
        st.header(get_text("quick_stats", st.session_state.language))
        
        # Try to show some quick statistics
        try:
            orchestrator = initialize_agents()
            data_agent = orchestrator.agents_registry.get("DataInterpreter")
            
            if data_agent:
                files = data_agent.csv_processor.get_available_files()
                
                st.metric(get_text("data_files", st.session_state.language), 
                         len(files.get("synthesis", [])) + len(files.get("transformation", [])))
                st.metric(get_text("synthesis_files", st.session_state.language), len(files.get("synthesis", [])))
                st.metric(get_text("transformation_files", st.session_state.language), len(files.get("transformation", [])))
                
                # Try to get some sample data
                try:
                    sample_file = files.get("synthesis", [None])[0]
                    if sample_file:
                        df = data_agent.csv_processor.load_csv(sample_file)
                        if 'year' in df.columns:
                            year_range = f"{int(df['year'].min())} - {int(df['year'].max())}"
                            st.metric(get_text("data_range", st.session_state.language), year_range)
                except:
                    pass
                    
        except Exception as e:
            st.error(get_text("error_loading", st.session_state.language).format(str(e)))
    
    # Conversation history
    if "conversation_history" in st.session_state and st.session_state.conversation_history:
        st.header(get_text("conversation_history", st.session_state.language))
        
        for i, entry in enumerate(reversed(st.session_state.conversation_history[-5:])):  # Show last 5
            with st.expander(f"Q: {entry['query'][:80]}{'...' if len(entry['query']) > 80 else ''}"):
                st.write(get_text("answer", st.session_state.language))
                st.write(entry['response']['content'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    confidence = entry['response']['confidence']
                    st.metric(get_text("confidence", st.session_state.language), f"{confidence:.2f}")
                
                if entry['response'].get('data_sources'):
                    with col2:
                        st.write(get_text("sources", st.session_state.language))
                        for source in entry['response']['data_sources'][:2]:
                            st.write(f"- {source}")
                
                if entry['response'].get('suggestions'):
                    with col3:
                        st.write(get_text("suggestions", st.session_state.language))
                        for suggestion in entry['response']['suggestions'][:2]:
                            st.write(f"• {suggestion}")

def process_query(query: str, user_type: str, language: str):
    """Process a user query asynchronously."""
    
    # Initialize session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    user_types = get_text("user_types", language)
    user_display = user_types.get(user_type, user_type)
    
    with st.spinner(get_text("processing", language).format(user_display)):
        try:
            # Initialize agents
            orchestrator = initialize_agents()
            
            # Prepare context
            context = {"user_type": user_type, "language": language}
            
            # Process query
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                orchestrator.process_query(query, context)
            )
            loop.close()
            
            # Display results
            st.success(get_text("analysis_complete", language))
            
            # Main response
            st.subheader(get_text("response", language))
            st.write(response.content)
            
            # Metadata in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                confidence_color = "green" if response.confidence > 0.7 else "orange" if response.confidence > 0.4 else "red"
                st.metric(
                    get_text("confidence", language), 
                    f"{response.confidence:.2f}",
                    help="Analysis confidence level"
                )
            
            with col2:
                if response.data_sources:
                    st.write(get_text("data_sources", language))
                    for source in response.data_sources[:3]:
                        st.write(f"• {source}")
                    if len(response.data_sources) > 3:
                        remaining = len(response.data_sources) - 3
                        if language == "de":
                            st.write(f"... und {remaining} weitere")
                        elif language == "fr":
                            st.write(f"... et {remaining} de plus")
                        elif language == "it":
                            st.write(f"... e {remaining} di più")
                        else:
                            st.write(f"... and {remaining} more")
            
            with col3:
                if response.suggestions:
                    st.write(get_text("followup_ideas", language))
                    for suggestion in response.suggestions:
                        if st.button(f"🔍 {suggestion[:50]}...", key=f"suggestion_{hash(suggestion)}"):
                            st.session_state.query_input = suggestion
                            st.rerun()
            
            # Analysis details
            if response.reasoning:
                with st.expander(get_text("analysis_details", language)):
                    st.write(response.reasoning)
            
            # Store in history
            st.session_state.conversation_history.append({
                "query": query,
                "user_type": user_type,
                "language": language,
                "response": {
                    "content": response.content,
                    "confidence": response.confidence,
                    "data_sources": response.data_sources or [],
                    "suggestions": response.suggestions or []
                }
            })
            
        except Exception as e:
            st.error(get_text("error_processing", language).format(str(e)))
            st.info(get_text("check_config", language))

if __name__ == "__main__":
    main()