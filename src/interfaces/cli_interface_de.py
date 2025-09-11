import asyncio
import sys
import os
from typing import Optional
import json

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.config import config
from agents.orchestrator_agent import OrchestratorAgent
from agents.data_interpreter_agent import DataInterpreterAgent
from agents.scenario_analyst_agent import ScenarioAnalystAgent
from agents.document_intelligence_agent import DocumentIntelligenceAgent
from agents.policy_context_agent import PolicyContextAgent

class EnergieSzenarienCLI:
    def __init__(self):
        config.validate()
        
        # Agenten initialisieren
        self.data_interpreter = DataInterpreterAgent(
            config.openai_api_key, 
            config.data_path
        )
        self.scenario_analyst = ScenarioAnalystAgent(
            config.openai_api_key, 
            config.data_path
        )
        self.document_intelligence = DocumentIntelligenceAgent(
            config.openai_api_key, 
            config.reports_path
        )
        self.policy_context = PolicyContextAgent(
            config.openai_api_key
        )
        
        # Orchestrator initialisieren und Agenten registrieren
        self.orchestrator = OrchestratorAgent(config.openai_api_key)
        self.orchestrator.register_agent(self.data_interpreter)
        self.orchestrator.register_agent(self.scenario_analyst)
        self.orchestrator.register_agent(self.document_intelligence)
        self.orchestrator.register_agent(self.policy_context)
        
        self.conversation_history = []
        
    def display_welcome(self):
        """Willkommensnachricht und Systeminfo anzeigen."""
        print("=" * 80)
        print("🇨🇭 SCHWEIZER ENERGIESZENARIEN ENTSCHLÜSSLER-SYSTEM 🇨🇭")
        print("=" * 80)
        print("Schweizer Energiewende-Daten für alle zugänglich machen!")
        print()
        print("Verfügbare Expertise:")
        print("📊 Datenanalyse - Statistiken, Trends und Vergleiche")
        print("🔮 Szenario-Analyse - Energiepfade vergleichen") 
        print("📄 Dokument-Intelligence - Technische Berichte und Studien")
        print("🏛️ Policy-Kontext - Regulierung und Umsetzung")
        print()
        print("Unterstützte Benutzertypen:")
        print("👥 Bürgerinnen und Bürger - Einfache, praktische Erklärungen")
        print("📰 Journalistinnen und Journalisten - Fakten mit Kontext und Story-Ansätzen") 
        print("🎓 Studierende - Bildungsinhalte mit Erklärungen")
        print("🏢 Politikerinnen und Politiker - Umfassende Analyse mit Implikationen")
        print()
        print("Befehle:")
        print("- Stellen Sie Ihre Frage zu Schweizer Energieszenarien")
        print("- 'hilfe' - Detaillierte Hilfe anzeigen")
        print("- 'agenten' - Verfügbare Agenten auflisten")
        print("- 'verlauf' - Gesprächsverlauf anzeigen")
        print("- 'löschen' - Gesprächsverlauf löschen")
        print("- 'beenden' oder 'exit' - System verlassen")
        print("=" * 80)
        print()
        
    def display_help(self):
        """Detaillierte Hilfeinformationen anzeigen."""
        help_text = """
DETAILLIERTE HILFE - Schweizer Energieszenarien Entschlüssler-System

BEISPIEL-ANFRAGEN:

📊 DATENANALYSE BEISPIELE:
- "Wie hoch sind die CO2-Emissionen der Schweiz 2030 im ZERO-Szenario?"
- "Wie verändert sich der Stromverbrauch nach Sektoren von 2020 bis 2050?"
- "Vergleiche das Wachstum erneuerbarer Energien zwischen den Szenarien"
- "Zeige mir die Trends im Transportenergieverbrauch"

🔮 SZENARIO-ANALYSE BEISPIELE:
- "Was ist der Unterschied zwischen ZERO-Basis und WWB-Szenarien?"
- "Wie unterscheiden sich die Szenarien bei Kernenergie-Annahmen?"
- "Vergleiche die Kosten zwischen Energiewende-Pfaden"
- "Was sind die Auswirkungen verzögerter Klimaschutz-Maßnahmen?"

📄 DOKUMENTENANALYSE BEISPIELE:
- "Welche Methodik wird für die Szenario-Modellierung verwendet?"
- "Erkläre die Annahmen zur Biomasse-Verfügbarkeit"
- "Was sagen die technischen Berichte über Winterstrom?"
- "Finde Informationen über Kohlenstoffabscheidung und -speicherung"

🏛️ POLICY-KONTEXT BEISPIELE:
- "Welche Politiken sind nötig für Netto-Null bis 2050?"
- "Wie unterstützt das CO2-Gesetz die Energiewende?"
- "Was sind die Umsetzungsherausforderungen für erneuerbare Energien?"
- "Erkläre die Klimaverpflichtungen der Schweiz"

TIPPS FÜR BESSERE ERGEBNISSE:
✅ Seien Sie spezifisch bei Zeitperioden (z.B. "bis 2030", "im Jahr 2050")
✅ Erwähnen Sie spezifische Sektoren falls relevant (Verkehr, Gebäude, Industrie)
✅ Fragen Sie nach Vergleichen zwischen Szenarien wenn angebracht
✅ Geben Sie an, ob Sie Policy-Implikationen oder technische Details wollen

BENUTZERTYPEN - Passen Sie Ihre Fragen an:
- Bürger/innen: Stellen Sie praktische Fragen zu Auswirkungen und Veränderungen
- Journalist/innen: Bitten Sie um Fakten, Kontext und Story-Ansätze
- Studierende: Fragen Sie nach Erklärungen von Konzepten und Methodik
- Politiker/innen: Bitten Sie um umfassende Analyse und Empfehlungen
"""
        print(help_text)
        
    def display_agents(self):
        """Verfügbare Agenten und ihre Fähigkeiten anzeigen."""
        print("\n🤖 VERFÜGBARE SPEZIALISIERTE AGENTEN:")
        print("-" * 50)
        
        agents = [
            self.data_interpreter,
            self.scenario_analyst, 
            self.document_intelligence,
            self.policy_context
        ]
        
        agent_names = {
            "DataInterpreter": "Daten-Interpreter",
            "ScenarioAnalyst": "Szenario-Analyst", 
            "DocumentIntelligence": "Dokument-Intelligence",
            "PolicyContext": "Policy-Kontext"
        }
        
        agent_descriptions = {
            "DataInterpreter": "Analysiert Energiedaten, Statistiken, Trends aus CSV-Dateien",
            "ScenarioAnalyst": "Vergleicht Szenarien, analysiert Pfade und Varianten",
            "DocumentIntelligence": "Verarbeitet PDF-Berichte und Dokumente", 
            "PolicyContext": "Bietet Policy-Implikationen und regulatorischen Kontext"
        }
        
        for agent in agents:
            capabilities = agent.get_capabilities()
            german_name = agent_names.get(capabilities['name'], capabilities['name'])
            german_desc = agent_descriptions.get(capabilities['name'], capabilities['description'])
            
            print(f"Agent: {german_name}")
            print(f"Beschreibung: {german_desc}")
            print(f"Modell: {capabilities['model']}")
            print()
            
    def display_history(self):
        """Gesprächsverlauf anzeigen."""
        if not self.conversation_history:
            print("Noch kein Gesprächsverlauf vorhanden.")
            return
            
        print("\n💬 GESPRÄCHSVERLAUF:")
        print("-" * 50)
        
        for i, entry in enumerate(self.conversation_history, 1):
            print(f"{i}. F: {entry['query'][:100]}{'...' if len(entry['query']) > 100 else ''}")
            print(f"   A: {entry['response']['content'][:100]}{'...' if len(entry['response']['content']) > 100 else ''}")
            print(f"   Vertrauen: {entry['response']['confidence']:.2f}")
            print()
            
    async def process_query(self, query: str, user_type: str = "citizen") -> None:
        """Eine Benutzeranfrage verarbeiten."""
        user_type_display = {
            "citizen": "Bürgerin/Bürger",
            "journalist": "Journalistin/Journalist",
            "student": "Studentin/Student",
            "policymaker": "Politikerin/Politiker"
        }
        
        print(f"\n🔄 Ihre Anfrage wird verarbeitet...")
        print(f"Benutzertyp: {user_type_display.get(user_type, user_type)}")
        print("-" * 50)
        
        try:
            # Benutzerkontext hinzufügen
            context = {"user_type": user_type}
            
            # Mit Orchestrator verarbeiten
            response = await self.orchestrator.process_query(query, context)
            
            # Antwort anzeigen
            self._display_response(response)
            
            # Im Verlauf speichern
            self.conversation_history.append({
                "query": query,
                "user_type": user_type,
                "response": {
                    "content": response.content,
                    "confidence": response.confidence,
                    "data_sources": response.data_sources,
                    "suggestions": response.suggestions
                }
            })
            
        except Exception as e:
            print(f"❌ Fehler bei der Verarbeitung der Anfrage: {str(e)}")
            print("Bitte formulieren Sie Ihre Frage neu oder wenden Sie sich an den Support.")
            
    def _display_response(self, response) -> None:
        """Agentenantwort formatiert anzeigen."""
        print("✅ ANTWORT:")
        print("-" * 50)
        print(response.content)
        print()
        
        # Vertrauen und Begründung anzeigen
        confidence_emoji = "🟢" if response.confidence > 0.7 else "🟡" if response.confidence > 0.4 else "🔴"
        print(f"{confidence_emoji} Vertrauen: {response.confidence:.2f}")
        
        if response.reasoning:
            print(f"🧠 Analyse: {response.reasoning}")
        
        # Datenquellen anzeigen
        if response.data_sources:
            print(f"📊 Datenquellen: {', '.join(response.data_sources[:3])}")
            if len(response.data_sources) > 3:
                print(f"    ... und {len(response.data_sources) - 3} weitere")
        
        # Vorschläge anzeigen
        if response.suggestions:
            print("\n💡 Weitere Vorschläge:")
            for i, suggestion in enumerate(response.suggestions, 1):
                print(f"   {i}. {suggestion}")
        
        print("\n" + "=" * 80)
        
    def get_user_type(self) -> str:
        """Benutzertyp aus Eingabe erhalten."""
        print("Wer sind Sie? (hilft uns, Antworten anzupassen)")
        print("1. Bürgerin/Bürger - Praktische, alltägliche Auswirkungen")
        print("2. Journalistin/Journalist - Fakten und Story-Ansätze") 
        print("3. Studentin/Student - Bildungsinhalte mit Erklärungen")
        print("4. Politikerin/Politiker - Umfassende Analyse")
        print("5. Überspringen - Standard verwenden (Bürger/in)")
        
        while True:
            choice = input("Auswahl (1-5): ").strip()
            
            if choice == "1":
                return "citizen"
            elif choice == "2": 
                return "journalist"
            elif choice == "3":
                return "student"
            elif choice == "4":
                return "policymaker"
            elif choice == "5" or choice == "":
                return "citizen"
            else:
                print("Bitte geben Sie 1, 2, 3, 4 oder 5 ein")
                
    async def run(self):
        """Haupt-CLI-Oberfläche ausführen."""
        self.display_welcome()
        
        # Benutzertyp erhalten
        user_type = self.get_user_type()
        user_type_display = {
            "citizen": "Bürgerin/Bürger",
            "journalist": "Journalistin/Journalist",
            "student": "Studentin/Student",
            "policymaker": "Politikerin/Politiker"
        }
        print(f"\n🎯 Modus: {user_type_display[user_type]}")
        print("Stellen Sie Ihre Fragen zu Schweizer Energieszenarien...")
        print()
        
        while True:
            try:
                # Benutzereingabe erhalten
                query = input("💬 Ihre Frage: ").strip()
                
                if not query:
                    continue
                    
                # Befehle behandeln
                if query.lower() in ['beenden', 'exit', 'q']:
                    print("👋 Vielen Dank für die Nutzung des Schweizer Energieszenarien-Systems!")
                    break
                elif query.lower() == 'hilfe':
                    self.display_help()
                    continue
                elif query.lower() == 'agenten':
                    self.display_agents()
                    continue
                elif query.lower() == 'verlauf':
                    self.display_history()
                    continue
                elif query.lower() == 'löschen':
                    self.conversation_history = []
                    print("🗑️ Gesprächsverlauf gelöscht.")
                    continue
                elif query.lower() == 'benutzer':
                    user_type = self.get_user_type()
                    print(f"🎯 Modus geändert zu: {user_type_display[user_type]}")
                    continue
                    
                # Reguläre Anfrage verarbeiten
                await self.process_query(query, user_type)
                
            except KeyboardInterrupt:
                print("\n\n👋 Auf Wiedersehen!")
                break
            except Exception as e:
                print(f"❌ Unerwarteter Fehler: {str(e)}")
                print("Bitte versuchen Sie es erneut oder geben Sie 'beenden' ein.")

if __name__ == "__main__":
    cli = EnergieSzenarienCLI()
    asyncio.run(cli.run())