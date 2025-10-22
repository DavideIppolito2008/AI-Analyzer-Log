# AI-Log-Analyzer

**AI-Log-Analyzer** — un toolkit minimale ma professionale per l'analisi di log (Apache/nginx + syslog) che combina parsing, anomaly detection con Machine Learning e una dashboard web front-end.

> Architettura: Java (static file server) + Python (analisi ML) + Vanilla JS (visualizzazione).
> - Java: serve la dashboard statica e l'API che restituisce il JSON dei risultati.
> - Python: legge i log, esegue parsing, applica un modello di anomaly detection (Isolation Forest) e salva risultati in SQLite / JSON.
> - JS: visualizza grafici (Chart.js) e riepiloghi AI.

---

## Features principali

- Parsing di log HTTP e log di sistema (formati comuni).
- Rilevamento anomalie non supervisionato con **Isolation Forest** (scikit-learn).
- Integrazione Java ↔ Python: il server statico/endpoint rimane stabile; Python non modifica l'API.
- Dashboard vanilla JS con Chart.js per visualizzare conteggi e riepiloghi.
- Salvataggio risultati in `data/results.db` e `analysis_result.json`.

---

## Requisiti

- Python 3.10+ (consigliato 3.11+)
- Java 11+ (JDK)
- `pip` virtualenv (consigliato)
- Rete per installare dipendenze initiali

Esempio ambiente (Unix):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 analyzer/log_analyzer.py analyzer/sample_access.log
javac server/Main.java
java server.Main
# apri http://localhost:8080
