import json
import sys
from datetime import datetime
import os
import re
import pandas as pd
import sqlite3
from sklearn.ensemble import IsolationForest

# === Funzione di estrazione dei dati strutturati dai log ===
def parse_log_line(line):
    """
    Estrae campi utili da una riga di log.
    Supporta sia log HTTP standard che log di sistema.
    """
    http_match = re.match(
        r'(?P<ip>\S+) - - \[(?P<date>.*?)\] "(?P<method>\S+) (?P<url>\S+) .*" (?P<status>\d{3}) (?P<size>\d+)',
        line
    )
    sys_match = re.match(
        r'(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<level>\S+) (?P<msg>.*)',
        line
    )

    if http_match:
        data = http_match.groupdict()
        data["level"] = "INFO" if int(data["status"]) < 400 else (
            "WARNING" if int(data["status"]) < 500 else "ERROR"
        )
        return data
    elif sys_match:
        data = sys_match.groupdict()
        data["status"] = 200 if data["level"] == "INFO" else (
            400 if data["level"] == "WARNING" else (
                500 if data["level"] == "ERROR" else 600
            )
        )
        data["size"] = len(data["msg"])
        data["method"] = "-"
        data["url"] = "-"
        data["ip"] = "-"
        return data
    return None

# === Analisi ML con Isolation Forest ===
def analyze_with_ml(df: pd.DataFrame, db_path: str = "data/results.db") -> pd.DataFrame:
    """Applica modello di anomaly detection ai log e salva i risultati in SQLite."""
    if df.empty:
        raise ValueError("DataFrame vuoto. Nessun log valido trovato.")

    # Feature engineering
    df["url_length"] = df["url"].apply(len)
    df["is_error"] = df["status"].astype(int) >= 400
    features = df[["status", "size", "url_length", "is_error"]].astype(float)

    # Modello Isolation Forest
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(features)  
    df["anomaly_score"] = model.decision_function(features)
    df["is_anomaly_ml"] = model.predict(features) == -1

    # Segnala come anomalia tutte le righe ERROR/CRITICAL
    df["is_anomaly_rule"] = df["level"].isin(["ERROR", "CRITICAL"])

    # Combina ML + regole
    df["is_anomaly"] = df["is_anomaly_ml"] | df["is_anomaly_rule"]

    # Salvataggio in SQLite
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    df.to_sql("logs_analysis", conn, if_exists="replace", index=False)
    conn.close()

    return df

# === Analizzatore principale ===
def analyze_log(file_path):
    total, errors, warnings, criticals = 0, 0, 0, 0
    parsed_data = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            if "ERROR" in line:
                errors += 1
            elif "WARNING" in line:
                warnings += 1
            elif "CRITICAL" in line:
                criticals += 1

            parsed = parse_log_line(line)
            if parsed:
                parsed_data.append(parsed)

    # Converte in DataFrame per il modello ML
    df = pd.DataFrame(parsed_data)
    if not df.empty:
        try:
            df = analyze_with_ml(df)
            anomaly_count = df["is_anomaly"].sum()
            avg_score = df["anomaly_score"].mean()
        except Exception as e:
            print(f"⚠️ Errore durante l'analisi ML: {e}")
            anomaly_count, avg_score = 0, 0
    else:
        anomaly_count, avg_score = 0, 0

    # Genera breve descrizione AI
    if anomaly_count > 0:
        ai_summary = f"Trovate {anomaly_count} anomalie (score medio ML {avg_score:.3f})."
    else:
        ai_summary = "Nessuna anomalia rilevante rilevata. Sistema stabile."

    return {
        "file_name": os.path.basename(file_path),
        "total_logs": total,
        "errors": errors,
        "warnings": warnings,
        "criticals": criticals,
        "ai_summary": ai_summary,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# === Main ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <logfile>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = analyze_log(file_path)

    output_path = os.path.join(os.path.dirname(__file__), "..", "analysis_result.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print(f"✅ AI+ML Analysis complete. Saved to {output_path}")
