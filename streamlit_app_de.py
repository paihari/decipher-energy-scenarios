"""
Swiss Energy Scenarios Decipher System - Deutsche Streamlit Web-Oberfläche
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

# Configure Streamlit page
st.set_page_config(
    page_title="Schweizer Energieszenarien Entschlüssler",
    page_icon="🇨🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def initialize_agents():
    """Alle Agenten initialisieren - gecacht für bessere Performance."""
    config.validate()
    
    # Spezialisierte Agenten initialisieren
    data_interpreter = DataInterpreterAgent(config.openai_api_key, config.data_path)
    scenario_analyst = ScenarioAnalystAgent(config.openai_api_key, config.data_path)
    document_intelligence = DocumentIntelligenceAgent(config.openai_api_key, config.reports_path)
    policy_context = PolicyContextAgent(config.openai_api_key)
    
    # Orchestrator initialisieren
    orchestrator = OrchestratorAgent(config.openai_api_key)
    orchestrator.register_agent(data_interpreter)
    orchestrator.register_agent(scenario_analyst)
    orchestrator.register_agent(document_intelligence)
    orchestrator.register_agent(policy_context)
    
    return orchestrator

def main():
    """Hauptanwendung für Streamlit."""
    
    # Header
    st.title("🇨🇭 Schweizer Energieszenarien Entschlüssler-System")
    st.markdown("*Schweizer Energiewende-Daten für alle zugänglich machen*")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Benutzerprofil")
        user_type_options = {
            "citizen": "Bürgerin/Bürger",
            "journalist": "Journalistin/Journalist", 
            "student": "Studentin/Student",
            "policymaker": "Politikerin/Politiker"
        }
        
        user_type = st.selectbox(
            "Wer sind Sie?",
            list(user_type_options.keys()),
            format_func=lambda x: user_type_options[x],
            index=0,
            help="Dies hilft uns, unsere Antworten auf Ihre Bedürfnisse zuzuschneiden"
        )
        
        st.header("🤖 Verfügbare Agenten")
        st.markdown("""
        - **📊 Daten-Interpreter**: Statistiken & Trends
        - **🔮 Szenario-Analyst**: Entwicklungspfade vergleichen
        - **📄 Dokument-Intelligence**: Technische Berichte
        - **🏛️ Policy-Kontext**: Regulierung & Umsetzung
        """)
        
        st.header("💡 Beispiel-Anfragen")
        example_queries = [
            "Wie hoch sind die CO2-Emissionen der Schweiz 2030?",
            "Vergleiche ZERO- mit WWB-Szenario",
            "Wie entwickelt sich die Elektromobilität?", 
            "Welche Politiken fördern erneuerbare Energien?",
            "Erkläre die verwendete Methodik in den Szenarien"
        ]
        
        selected_example = st.selectbox(
            "Probiere ein Beispiel:",
            [""] + example_queries,
            index=0
        )
        
        if selected_example and st.button("Beispiel verwenden"):
            st.session_state.query_input = selected_example
    
    # Hauptinhalt
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Stellen Sie Ihre Frage")
        
        # Fragefeld
        query = st.text_area(
            "Geben Sie Ihre Frage zu Schweizer Energieszenarien ein:",
            height=100,
            key="query_input",
            placeholder="z.B. Wie entwickeln sich die Emissionen im ZERO-Szenario?"
        )
        
        # Verarbeitung-Button
        if st.button("🔄 Analysieren", disabled=not query.strip()):
            if query.strip():
                process_query(query.strip(), user_type)
    
    with col2:
        st.header("📈 Schnell-Statistiken")
        
        # Versuche einige schnelle Statistiken zu zeigen
        try:
            orchestrator = initialize_agents()
            data_agent = orchestrator.agents_registry.get("DataInterpreter")
            
            if data_agent:
                files = data_agent.csv_processor.get_available_files()
                
                st.metric("Datendateien", 
                         len(files.get("synthesis", [])) + len(files.get("transformation", [])))
                st.metric("Synthese-Dateien", len(files.get("synthesis", [])))
                st.metric("Transformations-Dateien", len(files.get("transformation", [])))
                
                # Versuche einige Beispieldaten zu holen
                try:
                    sample_file = files.get("synthesis", [None])[0]
                    if sample_file:
                        df = data_agent.csv_processor.load_csv(sample_file)
                        if 'year' in df.columns:
                            year_range = f"{int(df['year'].min())} - {int(df['year'].max())}"
                            st.metric("Datenbereich", year_range)
                except:
                    pass
                    
        except Exception as e:
            st.error(f"Fehler beim Laden der Systeminfo: {str(e)}")
    
    # Gesprächsverlauf
    if "conversation_history" in st.session_state and st.session_state.conversation_history:
        st.header("📝 Gesprächsverlauf")
        
        for i, entry in enumerate(reversed(st.session_state.conversation_history[-5:])):  # Zeige letzten 5
            with st.expander(f"F: {entry['query'][:80]}{'...' if len(entry['query']) > 80 else ''}"):
                st.write("**Antwort:**")
                st.write(entry['response']['content'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    confidence = entry['response']['confidence']
                    st.metric("Vertrauen", f"{confidence:.2f}")
                
                if entry['response'].get('data_sources'):
                    with col2:
                        st.write("**Quellen:**")
                        for source in entry['response']['data_sources'][:2]:
                            st.write(f"- {source}")
                
                if entry['response'].get('suggestions'):
                    with col3:
                        st.write("**Vorschläge:**")
                        for suggestion in entry['response']['suggestions'][:2]:
                            st.write(f"• {suggestion}")

def process_query(query: str, user_type: str):
    """Benutzeranfrage asynchron verarbeiten."""
    
    # Session State initialisieren
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    user_type_display = {
        "citizen": "Bürgerin/Bürger",
        "journalist": "Journalistin/Journalist",
        "student": "Studentin/Student", 
        "policymaker": "Politikerin/Politiker"
    }
    
    with st.spinner(f"🔄 Ihre Anfrage wird als {user_type_display[user_type]} verarbeitet..."):
        try:
            # Agenten initialisieren
            orchestrator = initialize_agents()
            
            # Kontext vorbereiten
            context = {"user_type": user_type}
            
            # Anfrage verarbeiten
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                orchestrator.process_query(query, context)
            )
            loop.close()
            
            # Ergebnisse anzeigen
            st.success("✅ Analyse abgeschlossen!")
            
            # Hauptantwort
            st.subheader("🎯 Antwort")
            st.write(response.content)
            
            # Metadaten in Spalten
            col1, col2, col3 = st.columns(3)
            
            with col1:
                confidence_color = "green" if response.confidence > 0.7 else "orange" if response.confidence > 0.4 else "red"
                st.metric(
                    "Vertrauen", 
                    f"{response.confidence:.2f}",
                    help=f"Vertrauensniveau der Analyse"
                )
            
            with col2:
                if response.data_sources:
                    st.write("**📊 Datenquellen:**")
                    for source in response.data_sources[:3]:
                        st.write(f"• {source}")
                    if len(response.data_sources) > 3:
                        st.write(f"... und {len(response.data_sources) - 3} weitere")
            
            with col3:
                if response.suggestions:
                    st.write("**💡 Weitere Ideen:**")
                    for suggestion in response.suggestions:
                        if st.button(f"🔍 {suggestion[:50]}...", key=f"suggestion_{hash(suggestion)}"):
                            st.session_state.query_input = suggestion
                            st.rerun()
            
            # Analyse-Details
            if response.reasoning:
                with st.expander("🧠 Analyse-Details"):
                    st.write(response.reasoning)
            
            # Im Verlauf speichern
            st.session_state.conversation_history.append({
                "query": query,
                "user_type": user_type,
                "response": {
                    "content": response.content,
                    "confidence": response.confidence,
                    "data_sources": response.data_sources or [],
                    "suggestions": response.suggestions or []
                }
            })
            
        except Exception as e:
            st.error(f"❌ Fehler bei der Verarbeitung der Anfrage: {str(e)}")
            st.info("Bitte überprüfen Sie Ihre Konfiguration und versuchen Sie es erneut.")

if __name__ == "__main__":
    main()