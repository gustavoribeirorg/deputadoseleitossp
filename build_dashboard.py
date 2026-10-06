import json

with open('dados_eleicao.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Format integer with dots
def fmt(num):
    return f"{num:,}".replace(',', '.')

party_colors = {
    'PL': ('#1e3a8a', '#93c5fd'),
    'PT': ('#b91c1c', '#fca5a5'),
    'PODE': ('#0f766e', '#5eead4'),
    'PSOL': ('#b45309', '#fde047'),
    'PSD': ('#1d4ed8', '#93c5fd'),
    'REPUBLICANOS': ('#3730a3', '#c7d2fe'),
    'MDB': ('#15803d', '#86efac'),
    'PP': ('#0369a1', '#7dd3fc'),
    'PSB': ('#c2410c', '#fdba74'),
    'UNIÃO': ('#0284c7', '#bae6fd'),
    'NOVO': ('#ea580c', '#fed7aa'),
    'MISSÃO': ('#6d28d9', '#d8b4fe'),
    'PSDB': ('#0284c7', '#93c5fd'),
    'PRD': ('#475569', '#cbd5e1'),
    'CIDADANIA': ('#0284c7', '#93c5fd')
}

rows_partidos = []
for idx, p in enumerate(data['partidos']):
    badge_cls = 'badge-vagas' if p['vagas'] > 0 else 'badge-vagas badge-zero'
    fed_label = p['fed'] if p['fed'] != '-' else '<span style="color:#64748b;">Isolado</span>'
    fill_w = min(100, p['pct'] * 3.5)
    pct_str = f"{p['pct']:.2f}%".replace('.', ',')
    rows_partidos.append(f"""
              <tr>
                <td style="color: #94a3b8; font-weight: 600;">{idx + 1}º</td>
                <td>
                  <strong>{p['sg']}</strong> &mdash; <span style="color: var(--text-muted); font-size: 0.82rem;">{p['nm']}</span>
                </td>
                <td style="font-size: 0.85rem;">{fed_label}</td>
                <td class="num-col">{fmt(p['tvtn'])}</td>
                <td class="num-col" style="color: var(--text-muted);">{fmt(p['tvtl'])}</td>
                <td class="num-col" style="font-weight: 700; color: #ffffff;">{fmt(p['tot'])}</td>
                <td class="num-col">
                  <div class="pct-bar-wrap">
                    <span>{pct_str}</span>
                    <div class="pct-bar"><div class="pct-fill" style="width: {fill_w}%;"></div></div>
                  </div>
                </td>
                <td style="text-align: center;">
                  <span class="{badge_cls}">{p['vagas']}</span>
                </td>
              </tr>""")

rows_eleitos = []
for idx, c in enumerate(data['eleitos']):
    bg_col, txt_col = party_colors.get(c['partido'], ('#334155', '#ffffff'))
    badge_style = f"background: {bg_col}; color: {txt_col};"
    rows_eleitos.append(f"""
              <tr>
                <td style="color: #94a3b8; font-weight: 600;">{idx + 1}º</td>
                <td><strong style="color: #ffffff;">{c['nome']}</strong></td>
                <td style="font-family: monospace; color: #38bdf8; font-weight: 600;">{c['num']}</td>
                <td><span class="party-tag" style="{badge_style}">{c['partido']}</span></td>
                <td class="num-col" style="font-weight: 700; color: #34d399;">{fmt(c['votos'])}</td>
                <td style="color: var(--text-muted); font-size: 0.82rem;">{c['agr']}</td>
              </tr>""")

cadeiras_html = []
seat_idx = 1
for p in data['partidos']:
    if p['vagas'] > 0:
        bg_col, txt_col = party_colors.get(p['sg'], ('#475569', '#ffffff'))
        for _ in range(p['vagas']):
            cadeiras_html.append(f"""<div class="cadeira-seat" style="background-color: {bg_col}; color: {txt_col};" title="Cadeira #{seat_idx}: {p['sg']}">{p['sg'][:3]}</div>""")
            seat_idx += 1

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Eleições 2026 - Deputado Federal SP (Resultados Oficiais & Sobras)</title>
  <style>
    :root {{
      --bg-color: #0b1120;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --accent-green: #34d399;
      --accent-yellow: #fbbf24;
      --accent-rose: #f43f5e;
      --table-hover: #263349;
      --pill-bg: #334155;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-color);
      color: var(--text-main);
      line-height: 1.5;
      padding: 24px 16px;
    }}

    .container {{
      max-width: 1240px;
      margin: 0 auto;
    }}

    /* Header */
    header {{
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 28px 24px;
      margin-bottom: 24px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }}

    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 12px;
    }}

    .badge-live {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      letter-spacing: 0.5px;
    }}

    .badge-live::before {{
      content: '';
      width: 8px;
      height: 8px;
      background-color: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 1.8s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}

    h1 {{
      font-size: 1.95rem;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: #ffffff;
      margin-bottom: 6px;
    }}

    .subtitle {{
      color: var(--text-muted);
      font-size: 0.95rem;
    }}

    /* KPI Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      background-color: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
      transition: transform 0.2s, border-color 0.2s;
    }}

    .kpi-card:hover {{
      transform: translateY(-2px);
      border-color: #475569;
    }}

    .kpi-label {{
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.75px;
      color: var(--text-muted);
      margin-bottom: 6px;
      font-weight: 600;
    }}

    .kpi-value {{
      font-size: 1.85rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
    }}

    .kpi-desc {{
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-top: 6px;
    }}

    /* Tabs */
    .tabs {{
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--card-border);
      padding-bottom: 12px;
      overflow-x: auto;
    }}

    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 10px 18px;
      font-size: 0.95rem;
      font-weight: 600;
      border-radius: 8px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }}

    .tab-btn:hover {{
      color: var(--text-main);
      background-color: var(--pill-bg);
    }}

    .tab-btn.active {{
      color: #0b1120;
      background-color: var(--primary);
    }}

    /* Panels */
    .tab-content {{
      display: none;
    }}

    .tab-content.active {{
      display: block;
    }}

    /* Search & Filter Bar */
    .filter-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 16px;
    }}

    .search-input {{
      background-color: var(--card-bg);
      border: 1px solid var(--card-border);
      color: #ffffff;
      padding: 10px 16px;
      border-radius: 8px;
      font-size: 0.9rem;
      width: 100%;
      max-width: 380px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.18);
    }}

    /* Table Styles */
    .table-container {{
      background-color: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }}

    .table-responsive {{
      width: 100%;
      overflow-x: auto;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.9rem;
    }}

    th {{
      background-color: #162032;
      padding: 14px 16px;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.6px;
      border-bottom: 1px solid var(--card-border);
    }}

    td {{
      padding: 14px 16px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.6);
      color: #e2e8f0;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    tbody tr:hover {{
      background-color: var(--table-hover);
    }}

    .num-col {{
      text-align: right;
      font-variant-numeric: tabular-nums;
    }}

    .party-tag {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.8rem;
    }}

    .badge-vagas {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 28px;
      height: 28px;
      border-radius: 9999px;
      background-color: #38bdf8;
      color: #0b1120;
      font-weight: 800;
      font-size: 0.85rem;
    }}

    .badge-zero {{
      background-color: #334155;
      color: #94a3b8;
    }}

    /* Progress bar */
    .pct-bar-wrap {{
      display: flex;
      align-items: center;
      gap: 8px;
      justify-content: flex-end;
    }}

    .pct-bar {{
      width: 70px;
      height: 6px;
      background-color: #334155;
      border-radius: 4px;
      overflow: hidden;
    }}

    .pct-fill {{
      height: 100%;
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      border-radius: 4px;
    }}

    /* Math Card */
    .math-card {{
      background-color: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 20px;
    }}

    .math-card h3 {{
      font-size: 1.15rem;
      color: #38bdf8;
      margin-bottom: 12px;
    }}

    .math-box {{
      background: #0b1120;
      border: 1px dashed #475569;
      border-radius: 8px;
      padding: 16px;
      font-family: monospace;
      font-size: 0.95rem;
      color: #34d399;
      margin: 12px 0;
      line-height: 1.6;
    }}

    /* Sobras & Bubble Cards */
    .sobras-alert {{
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(245, 158, 11, 0.15) 100%);
      border: 1px solid rgba(239, 68, 68, 0.35);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
    }}

    .sobras-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }}

    .bubble-card {{
      background: #111a2e;
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 18px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.25);
      position: relative;
    }}

    .bubble-card.threatened {{
      border-color: rgba(244, 63, 94, 0.5);
      background: linear-gradient(180deg, rgba(244, 63, 94, 0.08) 0%, #111a2e 100%);
    }}

    .bubble-card.hunting {{
      border-color: rgba(56, 189, 248, 0.5);
      background: linear-gradient(180deg, rgba(56, 189, 248, 0.08) 0%, #111a2e 100%);
    }}

    .bubble-rank {{
      position: absolute;
      top: 14px;
      right: 14px;
      font-size: 0.75rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
    }}

    .duel-card {{
      background: #162032;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 12px;
    }}

    /* Plenary Diagram */
    .bancada-chart {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding: 24px;
      background: #0b1120;
      border-radius: 12px;
      margin-bottom: 20px;
      border: 1px solid var(--card-border);
      justify-content: center;
    }}

    .cadeira-seat {{
      width: 32px;
      height: 32px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.68rem;
      font-weight: 700;
      cursor: pointer;
      transition: transform 0.15s, box-shadow 0.15s;
    }}

    .cadeira-seat:hover {{
      transform: scale(1.3);
      box-shadow: 0 0 12px rgba(255, 255, 255, 0.4);
      z-index: 10;
    }}

    footer {{
      text-align: center;
      margin-top: 36px;
      color: var(--text-muted);
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <!-- Top Header -->
    <header>
      <div class="header-top">
        <div class="badge-live">APURAÇÃO OFICIAL TSE &bull; ELEIÇÕES GERAIS 2026</div>
        <div style="color: var(--text-muted); font-size: 0.85rem;">
          Atualizado às {data['geral']['horario']} &bull; {data['geral']['secoes_pct']}% das seções apuradas
        </div>
      </div>
      <h1>Resultado para Deputado Federal &mdash; São Paulo</h1>
      <p class="subtitle">Painel interativo com os resultados oficiais do Tribunal Superior Eleitoral, quocientes, distribuição das 70 cadeiras e projeção das sobras.</p>
    </header>

    <!-- KPI Summary Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Quociente Eleitoral (QE)</div>
        <div class="kpi-value" style="color: #38bdf8;">{fmt(data['geral']['qe'])}</div>
        <div class="kpi-desc">Votos necessários para 1 cadeira direta</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Total de Votos Válidos</div>
        <div class="kpi-value" style="color: #34d399;">{fmt(data['geral']['validos'])}</div>
        <div class="kpi-desc">Nominais (21,57 mi) + Legenda (642 mil)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Cadeiras em Disputa</div>
        <div class="kpi-value" style="color: #fbbf24;">{data['geral']['vagas']}</div>
        <div class="kpi-desc">Total de vagas da bancada paulista</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Total de Votos Apurados</div>
        <div class="kpi-value" style="color: #f8fafc;">{fmt(data['geral']['total_apurado'])}</div>
        <div class="kpi-desc">Brancos: 1,45 mi &bull; Nulos: 1,05 mi</div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs">
      <button class="tab-btn active" onclick="openTab('tab-sobras-proj', this)">🎯 Disputa das Sobras & Quem Pode Entrar</button>
      <button class="tab-btn" onclick="openTab('tab-partidos', this)">📊 Tabela por Partidos</button>
      <button class="tab-btn" onclick="openTab('tab-eleitos', this)">👥 70 Deputados Eleitos</button>
      <button class="tab-btn" onclick="openTab('tab-calculo', this)">📐 Memória de Cálculo (QE & Médias)</button>
      <button class="tab-btn" onclick="openTab('tab-bancada', this)">🏛️ Plenário da Bancada (70 Vagas)</button>
    </div>

    <!-- TAB: SOBRAS & PROJEÇÃO -->
    <div id="tab-sobras-proj" class="tab-content active">
      
      <div class="sobras-alert">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
          <span style="font-size: 1.25rem;">⚠️</span>
          <strong style="color: #f87171; font-size: 1.1rem;">Cenário Aberto nos ~6% de Urnas Finais (Art. 109 do Código Eleitoral)</strong>
        </div>
        <p style="color: #e2e8f0; font-size: 0.92rem; line-height: 1.5;">
          Com <strong>94,01%</strong> das urnas totalizadas, restam cerca de <strong>1,4 milhão de votos</strong> a serem apurados em São Paulo. A <strong>70ª cadeira</strong> (a 11ª vaga de sobra) está sendo disputada voto a voto entre as bancadas do <strong>Republicanos</strong> e do <strong>MDB</strong>, além de disputas internas acirradas onde a diferença entre o eleito e o primeiro suplente é de menos de 150 votos!
        </p>
      </div>

      <!-- Vaga Mais Ameaçada vs 1º na Fila -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-bottom: 24px;">
        
        <div class="bubble-card threatened">
          <span class="bubble-rank" style="background: rgba(244, 63, 94, 0.2); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.4);">
            ÚLTIMA CADEIRA CONQUISTADA (#70)
          </span>
          <div style="font-size: 0.8rem; text-transform: uppercase; color: #f87171; font-weight: 700; margin-bottom: 8px;">
            🚨 No Fio da Navalha (Defendendo a Cadeira)
          </div>
          <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">
            MARIA ROSAS
          </div>
          <div style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 12px;">
            <strong>Republicanos</strong> &bull; 83.928 votos nominais &bull; 6ª vaga do partido
          </div>
          <div class="math-box" style="margin: 0; font-size: 0.85rem; padding: 10px; color: #fca5a5;">
            Média da Bancada (11ª sobra): <strong>237.415,3</strong><br/>
            (Cálculo: 1.420.963 votos &divide; 6 vagas)
          </div>
          <p style="color: var(--text-muted); font-size: 0.82rem; margin-top: 10px;">
            Se o MDB ou o Podemos acelerarem a votação nas seções restantes e ultrapassarem essa média, o Republicanos perde essa cadeira.
          </p>
        </div>

        <div class="bubble-card hunting">
          <span class="bubble-rank" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4);">
            1º NA FILA DAS SOBRAS
          </span>
          <div style="font-size: 0.8rem; text-transform: uppercase; color: #38bdf8; font-weight: 700; margin-bottom: 8px;">
            ⚡ Pronto para Entrar (Maior Média Seguinte)
          </div>
          <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">
            ORLANDO MORANDO
          </div>
          <div style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 12px;">
            <strong>MDB</strong> &bull; 97.088 votos nominais &bull; Seria a 5ª vaga do MDB
          </div>
          <div class="math-box" style="margin: 0; font-size: 0.85rem; padding: 10px; color: #7dd3fc;">
            Média Atual da 5ª vaga: <strong>227.582,0</strong> (Dif: -9.833)<br/>
            (Faltam ~49.167 votos de bancada para o MDB virar a média)
          </div>
          <p style="color: var(--text-muted); font-size: 0.82rem; margin-top: 10px;">
            Orlando Morando supera amplamente a cláusula individual de 20% do QE (63.472 votos) e assume imediatamente se o MDB conquistar a 5ª vaga!
          </p>
        </div>

      </div>

      <!-- Tabela dos Primeiros da Fila -->
      <div class="math-card">
        <h3>📋 Ranking dos Próximos na Fila das Sobras (Quem herda a vaga se a média subir)</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 16px;">
          Todos os candidatos abaixo já cumpriram o requisito individual de ter mais de <strong>20% do QE (63.472 votos)</strong> e seus partidos atingiram mais de <strong>80% do QE</strong>. Se a média da bancada subir nas últimas urnas, eles tomam a cadeira:
        </p>

        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th style="width: 60px;">Fila</th>
                <th>Candidato (1º Suplente)</th>
                <th>Partido / Federação</th>
                <th class="num-col">Votação Nominal</th>
                <th class="num-col">Média da Vaga</th>
                <th class="num-col">Distância da Vaga 70</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="color:#38bdf8; font-weight:800;">1º</td>
                <td><strong style="color: #ffffff;">ORLANDO MORANDO</strong></td>
                <td><span class="party-tag" style="background:#15803d; color:#86efac;">MDB</span></td>
                <td class="num-col" style="color:#34d399; font-weight:700;">97.088</td>
                <td class="num-col" style="font-family:monospace;">227.582,0</td>
                <td class="num-col" style="color:#fbbf24;">-9.833 pontos</td>
                <td><span style="color:#34d399; font-weight:600;">Altíssima chance de virada</span></td>
              </tr>
              <tr>
                <td style="color:#38bdf8; font-weight:800;">2º</td>
                <td><strong style="color: #ffffff;">ANTONIO CARLOS RODRIGUES</strong></td>
                <td><span class="party-tag" style="background:#0f766e; color:#5eead4;">PODE</span></td>
                <td class="num-col" style="color:#34d399; font-weight:700;">64.450</td>
                <td class="num-col" style="font-family:monospace;">225.837,4</td>
                <td class="num-col" style="color:#fbbf24;">-11.578 pontos</td>
                <td><span style="color:#38bdf8; font-weight:600;">Disputa direta com MDB</span></td>
              </tr>
              <tr>
                <td style="color:#38bdf8; font-weight:800;">3º</td>
                <td><strong style="color: #ffffff;">RUI FALCÃO</strong></td>
                <td><span class="party-tag" style="background:#b91c1c; color:#fca5a5;">PT (FE Brasil)</span></td>
                <td class="num-col" style="color:#34d399; font-weight:700;">100.259</td>
                <td class="num-col" style="font-family:monospace;">222.280,8</td>
                <td class="num-col" style="color:#fbbf24;">-15.134 pontos</td>
                <td><span style="color:#94a3b8;">Em espera (precisa +181k votos)</span></td>
              </tr>
              <tr>
                <td style="color:#38bdf8; font-weight:800;">4º</td>
                <td><strong style="color: #ffffff;">VITOR LIPPI</strong></td>
                <td><span class="party-tag" style="background:#1d4ed8; color:#93c5fd;">PSD</span></td>
                <td class="num-col" style="color:#34d399; font-weight:700;">78.448</td>
                <td class="num-col" style="font-family:monospace;">206.624,7</td>
                <td class="num-col" style="color:#fbbf24;">-30.791 pontos</td>
                <td><span style="color:#94a3b8;">Depende de forte arrancada</span></td>
              </tr>
              <tr>
                <td style="color:#38bdf8; font-weight:800;">5º</td>
                <td><strong style="color: #ffffff;">MARCO VINHOLI</strong></td>
                <td><span class="party-tag" style="background:#3730a3; color:#c7d2fe;">REPUBLICANOS</span></td>
                <td class="num-col" style="color:#34d399; font-weight:700;">79.526</td>
                <td class="num-col" style="font-family:monospace;">203.498,9</td>
                <td class="num-col" style="color:#fbbf24;">-33.916 pontos</td>
                <td><span style="color:#94a3b8;">Necessita da 7ª vaga do partido</span></td>
              </tr>
              <tr>
                <td style="color:#38bdf8; font-weight:800;">6º</td>
                <td><strong style="color: #ffffff;">ALEX MANENTE</strong></td>
                <td><span class="party-tag" style="background:#0284c7; color:#bae6fd;">CIDADANIA</span></td>
                <td class="num-col" style="color:#34d399; font-weight:700;">96.538</td>
                <td class="num-col" style="font-family:monospace;">182.687,5</td>
                <td class="num-col" style="color:#fbbf24;">-54.728 pontos</td>
                <td><span style="color:#94a3b8;">Candidato forte, mas federação baixa</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Duelos Internos de Votos -->
      <div class="math-card">
        <h3>⚔️ Disputas Internas no Fio da Navalha (Votos entre Companheiros de Partido)</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 16px;">
          Mesmo que a legenda mantenha o mesmo número de cadeiras, a ordem dos eleitos pode mudar se o suplente ultrapassar o titular nas urnas restantes:
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
          
          <div class="duel-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span class="party-tag" style="background:#0f766e; color:#5eead4;">PODEMOS</span>
              <span style="font-size: 0.8rem; color:#f87171; font-weight: 700;">Diferença: APENAS 142 VOTOS!</span>
            </div>
            <div style="font-size: 0.9rem; color:#e2e8f0; margin-bottom: 4px;">
              ✅ <strong>Marangoni:</strong> 64.592 votos <span style="color:#34d399;">(Eleito provisório)</span>
            </div>
            <div style="font-size: 0.9rem; color:#94a3b8;">
              ⏳ <strong>Antonio Carlos Rodrigues:</strong> 64.450 votos <span style="color:#fbbf24;">(1º Suplente)</span>
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">
              Basta uma urna favorável na capital para Antonio Carlos tomar a cadeira de Marangoni diretamente!
            </div>
          </div>

          <div class="duel-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span class="party-tag" style="background:#b91c1c; color:#fca5a5;">PT / FE BRASIL</span>
              <span style="font-size: 0.8rem; color:#fbbf24; font-weight: 700;">Diferença: 1.185 VOTOS</span>
            </div>
            <div style="font-size: 0.9rem; color:#e2e8f0; margin-bottom: 4px;">
              ✅ <strong>Paulo Teixeira:</strong> 101.444 votos <span style="color:#34d399;">(11º da federação)</span>
            </div>
            <div style="font-size: 0.9rem; color:#94a3b8;">
              ⏳ <strong>Rui Falcão:</strong> 100.259 votos <span style="color:#fbbf24;">(12º da federação)</span>
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">
              Disputa direta histórica entre dois nomes de peso do PT pela última vaga da federação.
            </div>
          </div>

          <div class="duel-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span class="party-tag" style="background:#15803d; color:#86efac;">MDB</span>
              <span style="font-size: 0.8rem; color:#fbbf24; font-weight: 700;">Diferença: 2.685 VOTOS</span>
            </div>
            <div style="font-size: 0.9rem; color:#e2e8f0; margin-bottom: 4px;">
              ✅ <strong>Enrico Misasi:</strong> 99.773 votos <span style="color:#34d399;">(4º do MDB)</span>
            </div>
            <div style="font-size: 0.9rem; color:#94a3b8;">
              ⏳ <strong>Orlando Morando:</strong> 97.088 votos <span style="color:#fbbf24;">(5º do MDB)</span>
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">
              Morando pode entrar tanto se o MDB ganhar a 5ª vaga por média, quanto se ultrapassar Misasi individualmente.
            </div>
          </div>

        </div>
      </div>

    </div>

    <!-- TAB 1: PARTIDOS -->
    <div id="tab-partidos" class="tab-content">
      <div class="filter-bar">
        <input type="text" id="partySearch" class="search-input" placeholder="🔍 Filtrar por partido ou sigla..." oninput="filterParties()" />
        <div style="color: var(--text-muted); font-size: 0.85rem;">
          26 partidos políticos ordenados pelo total de votos
        </div>
      </div>

      <div class="table-container">
        <div class="table-responsive">
          <table id="partiesTable">
            <thead>
              <tr>
                <th style="width: 50px;">Pos.</th>
                <th>Partido / Sigla</th>
                <th>Federação</th>
                <th class="num-col">Votos Nominais</th>
                <th class="num-col">Votos Legenda</th>
                <th class="num-col">Total de Votos</th>
                <th class="num-col">% Votos Válidos</th>
                <th style="text-align: center; width: 100px;">Cadeiras</th>
              </tr>
            </thead>
            <tbody>
              {''.join(rows_partidos)}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 2: ELEITOS -->
    <div id="tab-eleitos" class="tab-content">
      <div class="filter-bar">
        <input type="text" id="candSearch" class="search-input" placeholder="🔍 Buscar por nome do candidato ou partido..." oninput="filterCandidates()" />
        <div style="color: var(--text-muted); font-size: 0.85rem;">
          Os 70 deputados federais eleitos para a 60ª Legislatura
        </div>
      </div>

      <div class="table-container">
        <div class="table-responsive">
          <table id="candTable">
            <thead>
              <tr>
                <th style="width: 50px;">Pos.</th>
                <th>Nome na Urna</th>
                <th>Número</th>
                <th>Partido</th>
                <th class="num-col">Votação Nominal</th>
                <th>Coligação / Federação</th>
              </tr>
            </thead>
            <tbody>
              {''.join(rows_eleitos)}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: CALCULO -->
    <div id="tab-calculo" class="tab-content">
      <div class="math-card">
        <h3>1. Quociente Eleitoral (QE) &mdash; Artigo 106 do Código Eleitoral</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">
          O Quociente Eleitoral representa o volume mínimo de votos válidos para que uma legenda ou federação alcance diretamente 1 cadeira:
        </p>
        <div class="math-box">
          QE = Total de Votos Válidos / Número de Cadeiras<br/>
          QE = 22.215.010 / 70 = 317.357,28... &rarr; <strong>317.357 votos</strong>
        </div>
      </div>

      <div class="math-card">
        <h3>2. Quociente Partidário (QP) e Trava Individual de 10%</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">
          O QP inicial de cada bancada é obtido pela divisão dos seus votos válidos pelo QE:
        </p>
        <div class="math-box">
          QP = Votos Totais da Bancada / QE (desprezada a fração)<br/><br/>
          &bull; <strong>PL:</strong> 6.024.614 / 317.357 = 18 vagas diretas<br/>
          &bull; <strong>Fed. PSOL/REDE:</strong> 2.882.001 / 317.357 = 9 vagas calculadas<br/>
          &bull; <strong>FE Brasil (PT/PCdoB/PV):</strong> 2.659.641 / 317.357 = 8 vagas diretas<br/>
          &bull; <strong>Podemos:</strong> 1.801.045 / 317.357 = 5 vagas diretas<br/>
          &bull; <strong>Fed. União Progressista (PP/UNIÃO):</strong> 1.692.403 / 317.357 = 5 vagas diretas<br/>
          &bull; <strong>PSD:</strong> 1.440.839 / 317.357 = 4 vagas diretas<br/>
          &bull; <strong>Republicanos:</strong> 1.420.963 / 317.357 = 4 vagas diretas<br/>
          &bull; <strong>MDB:</strong> 1.135.357 / 317.357 = 3 vagas diretas<br/>
          &bull; <strong>PSB:</strong> 893.250 / 317.357 = 2 vagas diretas<br/>
          &bull; <strong>Missão:</strong> 616.922 / 317.357 = 1 vaga direta<br/>
          &bull; <strong>NOVO:</strong> 567.219 / 317.357 = 1 vaga direta<br/>
          &bull; <strong>Fed. PSDB/Cidadania:</strong> 364.751 / 317.357 = 1 vaga direta<br/>
          &bull; <strong>Fed. Renovação Solidária (SD/PRD):</strong> 335.995 / 317.357 = 1 vaga direta
        </div>
        <p style="color: #fbbf24; font-size: 0.9rem; margin-top: 10px;">
          ⚠️ <strong>Caso Técnico de Destaque (Art. 108 do Código Eleitoral):</strong><br/>
          Para tomar posse da vaga pelo QP, o candidato precisa ter votação nominal mínima de <strong>10% do QE (31.736 votos)</strong>. A Federação PSOL/REDE obteve quociente para 9 vagas, mas contava com apenas 6 candidatos com votação $\ge$ 31.736. As 3 vagas não preenchidas foram destinadas à distribuição das <strong>Sobras (Médias)</strong>.
        </p>
      </div>

      <div class="math-card">
        <h3>3. Distribuição das 11 Sobras Rodada a Rodada (Art. 109)</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">
          Veja a sequência oficial de distribuição das 11 cadeiras por maiores médias:
        </p>
        <div class="math-box">
          1ª Sobra: <strong>Podemos</strong> (Média: 301.116,5) &rarr; Rodrigo Gambale<br/>
          2ª Sobra: <strong>FE Brasil / PT</strong> (Média: 296.374,3) &rarr; Kiko Celeguim<br/>
          3ª Sobra: <strong>PSD</strong> (Média: 289.274,6) &rarr; Eleuses Paiva<br/>
          4ª Sobra: <strong>Republicanos</strong> (Média: 284.898,4) &rarr; Altair Moraes<br/>
          5ª Sobra: <strong>MDB</strong> (Média: 284.477,5) &rarr; Enrico Misasi<br/>
          6ª Sobra: <strong>NOVO</strong> (Média: 284.255,0) &rarr; Adriana Ventura<br/>
          7ª Sobra: <strong>FE Brasil / PT</strong> (Média: 266.736,9) &rarr; Juliana Cardoso<br/>
          8ª Sobra: <strong>Podemos</strong> (Média: 258.099,9) &rarr; Marangoni<br/>
          9ª Sobra: <strong>FE Brasil / PT</strong> (Média: 242.488,1) &rarr; Paulo Teixeira<br/>
          10ª Sobra: <strong>PSD</strong> (Média: 241.062,2) &rarr; Carlos Bezerra Jr.<br/>
          11ª Sobra (#70): <strong>Republicanos</strong> (Média: 237.415,3) &rarr; Maria Rosas
        </div>
      </div>
    </div>

    <!-- TAB 4: BANCADA -->
    <div id="tab-bancada" class="tab-content">
      <div class="math-card">
        <h3>Distribuição Visual das 70 Cadeiras no Plenário Paulista</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 18px;">
          Representação gráfica das 70 vagas por partido. Passe o mouse sobre a cadeira para identificar a legenda:
        </p>

        <div class="bancada-chart">
          {''.join(cadeiras_html)}
        </div>

        <div style="display: flex; flex-wrap: wrap; gap: 14px; margin-top: 14px; font-size: 0.85rem; justify-content: center;">
          <span><strong style="color:#93c5fd;">■ PL:</strong> 18 vagas (25,7%)</span>
          <span><strong style="color:#fca5a5;">■ PT:</strong> 11 vagas (15,7%)</span>
          <span><strong style="color:#5eead4;">■ PODE:</strong> 7 vagas (10,0%)</span>
          <span><strong style="color:#fde047;">■ PSOL:</strong> 6 vagas (8,6%)</span>
          <span><strong style="color:#93c5fd;">■ PSD:</strong> 6 vagas (8,6%)</span>
          <span><strong style="color:#c7d2fe;">■ Republicanos:</strong> 6 vagas (8,6%)</span>
          <span><strong style="color:#86efac;">■ MDB:</strong> 4 vagas (5,7%)</span>
          <span><strong style="color:#7dd3fc;">■ PP:</strong> 3 vagas (4,3%)</span>
          <span><strong style="color:#fdba74;">■ PSB:</strong> 2 vagas (2,9%)</span>
          <span><strong style="color:#bae6fd;">■ UNIÃO:</strong> 2 vagas (2,9%)</span>
          <span><strong style="color:#fed7aa;">■ NOVO:</strong> 2 vagas (2,9%)</span>
          <span><strong style="color:#d8b4fe;">■ MISSÃO:</strong> 1 vaga (1,4%)</span>
          <span><strong style="color:#93c5fd;">■ PSDB:</strong> 1 vaga (1,4%)</span>
          <span><strong style="color:#cbd5e1;">■ PRD:</strong> 1 vaga (1,4%)</span>
        </div>
      </div>
    </div>

    <footer>
      Tribunal Superior Eleitoral (TSE) &bull; Eleições Gerais 2026 &bull; Cargo de Deputado Federal (SP) &bull; Processamento em Tempo Real
    </footer>

  </div>

  <script>
    function openTab(tabId, btn) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      btn.classList.add('active');
    }}

    function filterParties() {{
      const q = document.getElementById('partySearch').value.toLowerCase();
      const rows = document.querySelectorAll('#partiesTable tbody tr');
      rows.forEach(r => {{
        const text = r.innerText.toLowerCase();
        r.style.display = text.includes(q) ? '' : 'none';
      }});
    }}

    function filterCandidates() {{
      const q = document.getElementById('candSearch').value.toLowerCase();
      const rows = document.querySelectorAll('#candTable tbody tr');
      rows.forEach(r => {{
        const text = r.innerText.toLowerCase();
        r.style.display = text.includes(q) ? '' : 'none';
      }});
    }}
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Dashboard index.html atualizado com aba de Sobras com sucesso!")
