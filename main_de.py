#!/usr/bin/env python3
"""
Schweizer Energieszenarien Entschlüssler-System
Deutsche Haupteinstiegspunkt für die Multiagenten-Anwendung
"""

import asyncio
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from interfaces.cli_interface_de import EnergieSzenarienCLI

def main():
    """Haupteinstiegspunkt."""
    try:
        cli = EnergieSzenarienCLI()
        asyncio.run(cli.run())
    except KeyboardInterrupt:
        print("\n👋 Auf Wiedersehen!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Anwendungsfehler: {str(e)}")
        print("Bitte überprüfen Sie Ihre Konfiguration und versuchen Sie es erneut.")
        sys.exit(1)

if __name__ == "__main__":
    main()