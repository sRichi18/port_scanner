#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime
from html import escape

def summarize_results(results):
    counts = {}
    for r in results.get("results", []):
        state = r.get("state", "unknown")
        counts[state] = counts.get(state, 0) + 1
    return counts

#Construcción de un HTML básico
def build_html(results, json_filename):
    target = results.get("target", "desconocido")
    ports_scanned = results.get("ports_scanned", "")
    timestamp = results.get("timestamp", datetime.now().isoformat())
    rows = results.get("results", [])

    counts = summarize_results(results)
    states = list(counts.keys())
    values = [counts[s] for s in states]

    # Salida del nombre del archivo
    base_name = os.path.splitext(os.path.basename(json_filename))[0]
    out_file = f"report_{base_name}.html"

    # Construcción de la tabla
    table_rows = ""
    for r in rows:
        port = r.get("port", "")
        proto = escape(str(r.get("protocol", "")))
        state = escape(str(r.get("state", "")))
        service = escape(str(r.get("service", "")))
        version = escape(str(r.get("version", "")))
        table_rows += f"<tr><td>{port}</td><td>{proto}</td><td>{state}</td><td>{service}</td><td>{version}</td></tr>\n"

    # CSS sencillo
    css = """
    body { font-family: Arial, Helvetica, sans-serif; margin: 20px; color:#222 }
    header { display:flex; justify-content:space-between; align-items:center; }
    h1 { margin:0; font-size:1.4rem; }
    .meta { text-align:right; font-size:0.9rem; color:#555 }
    .card { background:#fff; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.08); padding:16px; margin-top:16px; }
    table { width:100%; border-collapse:collapse; margin-top:12px; }
    th, td { padding:8px 10px; border-bottom:1px solid #eee; text-align:left; }
    th { background:#f7f7f7; font-weight:600; }
    .small { font-size:0.9rem; color:#555; }
    .center { text-align:center; }
    footer { margin-top:18px; font-size:0.85rem; color:#666; }
    @media (max-width:720px){ .meta { text-align:left; margin-top:8px } }
    """

    # Estructura del HTML
    html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Informe de escaneo - {escape(target)}</title>
<link rel="icon" href="data:;base64,=">
<style>{css}</style>
<!-- Chart.js CDN -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<header>
  <div>
    <h1>Informe de escaneo — {escape(target)}</h1>
    <div class="small">Puertos: {escape(str(ports_scanned))}</div>
  </div>
  <div class="meta">
    <div>Generado: {escape(timestamp)}</div>
    <div>Origen JSON: {escape(json_filename)}</div>
  </div>
</header>

<section class="card">
  <h2 class="small">Resumen</h2>
  <p class="small">Total puertos listados: <strong>{len(rows)}</strong></p>

  <canvas id="stateChart" style="max-width:700px;height:280px"></canvas>
</section>

<section class="card">
  <h2 class="small">Detalle por puerto</h2>
  <table>
    <thead>
      <tr><th>Puerto</th><th>Protocolo</th><th>Estado</th><th>Servicio</th><th>Versión</th></tr>
    </thead>
    <tbody>
      {table_rows if table_rows else '<tr><td colspan="5" class="center">No se encontraron puertos</td></tr>'}
    </tbody>
  </table>
</section>

<footer class="card">
  <div>Generado por: <strong>Ricardo Islas</strong></div>
  <div>Proyecto: Port Scanner — resultados procesados</div>
  <div>Nota: Solo para uso autorizado.</div>
</footer>

<script>
const ctx = document.getElementById('stateChart').getContext('2d');
const chart = new Chart(ctx, {{
    type: 'bar',
    data: {{
        labels: {states},
        datasets: [{{
            label: 'Conteo por estado',
            data: {values},
            borderWidth: 1,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)'
        }}]
    }},
    options: {{
        scales: {{
            y: {{
                beginAtZero: true,
                ticks: {{ precision:0 }}
            }}
        }},
        plugins: {{
            legend: {{ display: false }},
            title: {{ display: true, text: 'Estados de puertos' }}
        }}
    }}
}});
</script>

</body>
</html>
"""
    return out_file, html

def main():
    if len(sys.argv) < 2:
        print("Uso: python generate_report.py scan_results_xxx.json")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: archivo JSON no encontrado: {json_path}")
        sys.exit(1)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        print(f"Error leyendo JSON: {e}")
        sys.exit(1)

    out_file, html = build_html(results, json_path)
    try:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Informe generado: {out_file}")
    except Exception as e:
        print(f"Error escribiendo HTML: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
