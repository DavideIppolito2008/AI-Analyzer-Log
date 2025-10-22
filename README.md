# AI Log Analyzer

**AI Log Analyzer** è uno strumento di analisi intelligente dei log basato su *Machine Learning* che rileva automaticamente comportamenti anomali nei file di log di sistema, applicazioni o server.  
Il progetto utilizza l’algoritmo **Isolation Forest** per identificare outlier e pattern sospetti, aiutando a individuare errori, intrusioni o anomalie di performance.

---

##  Dashboard

La dashboard interattiva mostra:
- Log grezzi caricati
- Livelli di severità evidenziati
- Segnalazioni automatiche di anomalie
- Grafico dell’andamento temporale

![Dashboard Preview](./Dashboard.png)

---

##  Tecnologie utilizzate

- **Python 3.x**
- **Pandas** – analisi e pulizia dei dati
- **Scikit-learn** – implementazione del modello *IsolationForest*
- **Matplotlib** – visualizzazione grafica dei risultati
- **Streamlit** – dashboard interattiva
- **Joblib** – salvataggio e caricamento del modello AI

---

## Algoritmo: Isolation Forest

L’**Isolation Forest** è un algoritmo di *anomaly detection* che si basa sull’idea che:
> Gli outlier sono più facili da isolare rispetto ai punti normali.

Funziona costruendo molteplici alberi binari casuali, dove:
- I **punti normali** richiedono più partizioni per essere isolati.
- Gli **outlier** vengono isolati rapidamente.

Il punteggio finale (`anomaly_score`) indica quanto un log è anomalo:
- 🔵 **≈ 0.0** → comportamento normale  
- 🔴 **≈ 1.0** → forte anomalia  

Questo approccio è molto efficiente anche su grandi dataset.

---




