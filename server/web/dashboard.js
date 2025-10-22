async function loadData() {
  try {
    const res = await fetch('/api/results');
    if (!res.ok) {
      document.body.innerHTML = "<h2>Errore nel caricamento dei dati 😢</h2>";
      return;
    }

    const data = await res.json();
    const d = Array.isArray(data) ? data[0] : data;

    document.getElementById("fileName").textContent = d.file_name;
    document.getElementById("total").textContent = d.total_logs;
    document.getElementById("errors").textContent = d.errors;
    document.getElementById("warnings").textContent = d.warnings;
    document.getElementById("criticals").textContent = d.criticals;
    document.getElementById("timestamp").textContent = d.timestamp;

    // Aggiunge il riepilogo AI/ML
    const aiDiv = document.getElementById("aiSummary");
    if (aiDiv) {
      aiDiv.textContent = d.ai_summary || "Nessun riepilogo disponibile.";
    }

    const ctx = document.getElementById('chart');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Errori', 'Warning', 'Critici'],
        datasets: [{
          label: 'Conteggio log',
          data: [Number(d.errors), Number(d.warnings), Number(d.criticals)],
          backgroundColor: ['#e74c3c', '#f1c40f', '#8e44ad'],
          borderColor: ['#c0392b', '#d4ac0d', '#6c3483'],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          tooltip: {
            enabled: true,
            callbacks: {
              label: function(context) {
                return context.dataset.label + ": " + context.raw;
              }
            }
          }
        },
        scales: {
          y: { beginAtZero: true, title: { display: true, text: 'Numero di log' } },
          x: { title: { display: true, text: 'Tipologia' } }
        }
      }
    });

  } catch (err) {
    document.body.innerHTML = "<h2>Errore nel caricamento della dashboard 😢</h2>";
    console.error(err);
  }
}

loadData();
