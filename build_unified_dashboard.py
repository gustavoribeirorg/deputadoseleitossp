import json

with open('dados_estadual.json', 'r', encoding='utf-8') as f:
    estadual = json.load(f)

with open('dados_federal.json', 'r', encoding='utf-8') as f:
    federal = json.load(f)

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

html_code = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Eleições 2026 SP - Apuração Oficial TSE (Estadual & Federal)</title>
  <style>
    :root {{
      --bg-color: #0b1120;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --primary-hover: #0284c7;
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
      max-width: 1260px;
      margin: 0 auto;
    }}

    /* Cargo Selector Switcher */
    .cargo-switcher {{
      display: flex;
      justify-content: center;
      gap: 12px;
      margin-bottom: 24px;
    }}

    .cargo-btn {{
      background: #1e293b;
      border: 2px solid #334155;
      color: var(--text-muted);
      padding: 12px 24px;
      border-radius: 12px;
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: all 0.2s ease;
    }}

    .cargo-btn:hover {{
      border-color: #475569;
      color: #ffffff;
      transform: translateY(-1px);
    }}

    .cargo-btn.active {{
      background: #0284c7;
      border-color: #38bdf8;
      color: #ffffff;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
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
      width: 30px;
      height: 30px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.65rem;
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

    <!-- Switcher -->
    <div class="cargo-switcher">
      <button id="btnCargoEstadual" class="cargo-btn active" onclick="switchCargo('estadual')">
        🏛️ Deputado Estadual (ALESP &bull; 94 Cadeiras)
      </button>
      <button id="btnCargoFederal" class="cargo-btn" onclick="switchCargo('federal')">
        🏛️ Deputado Federal (Câmara &bull; 70 Cadeiras)
      </button>
    </div>

    <!-- Dynamic Container -->
    <div id="cargoContent"></div>

    <footer>
      Tribunal Superior Eleitoral (TSE) &bull; Eleições Gerais 2026 &bull; Estado de São Paulo &bull; Apuração Oficial
    </footer>

  </div>

  <script>
    const dataEstadual = {json.dumps(estadual, ensure_ascii=False)};
    const dataFederal = {json.dumps(federal, ensure_ascii=False)};
    const partyColors = {json.dumps(party_colors, ensure_ascii=False)};

    let currentData = dataEstadual;

    function fmt(n) {{
      return n.toLocaleString('pt-BR');
    }}

    function switchCargo(cargo) {{
      if (cargo === 'estadual') {{
        currentData = dataEstadual;
        document.getElementById('btnCargoEstadual').classList.add('active');
        document.getElementById('btnCargoFederal').classList.remove('active');
      }} else {{
        currentData = dataFederal;
        document.getElementById('btnCargoFederal').classList.add('active');
        document.getElementById('btnCargoEstadual').classList.remove('active');
      }}
      renderDashboard();
    }}

    function renderDashboard() {{
      const d = currentData;
      const g = d.geral;
      const isEstadual = d.cargo_cod === 7;
      const orgaoNome = isEstadual ? 'Assembleia Legislativa de SP (ALESP)' : 'Câmara dos Deputados';

      // Ultima vaga e 1º da fila
      const ultSobra = d.historico_sobras[d.historico_sobras.length - 1];
      const proxFila = d.proximos_fila[0];

      let rowsPartidos = '';
      d.partidos.forEach((p, idx) => {{
        const badgeCls = p.vagas > 0 ? 'badge-vagas' : 'badge-vagas badge-zero';
        const fedLabel = p.fed !== '-' ? p.fed : '<span style="color:#64748b;">Isolado</span>';
        const fillW = Math.min(100, p.pct * 3.5);
        const pctStr = p.pct.toLocaleString('pt-BR', {{minimumFractionDigits: 2}}) + '%';
        rowsPartidos += `
          <tr>
            <td style="color: #94a3b8; font-weight: 600;">${{idx + 1}}º</td>
            <td><strong>${{p.sg}}</strong> &mdash; <span style="color: var(--text-muted); font-size: 0.82rem;">${{p.nm}}</span></td>
            <td style="font-size: 0.85rem;">${{fedLabel}}</td>
            <td class="num-col">${{fmt(p.tvtn)}}</td>
            <td class="num-col" style="color: var(--text-muted);">${{fmt(p.tvtl)}}</td>
            <td class="num-col" style="font-weight: 700; color: #ffffff;">${{fmt(p.tot)}}</td>
            <td class="num-col">
              <div class="pct-bar-wrap">
                <span>${{pctStr}}</span>
                <div class="pct-bar"><div class="pct-fill" style="width: ${{fillW}}%;"></div></div>
              </div>
            </td>
            <td style="text-align: center;"><span class="${{badgeCls}}">${{p.vagas}}</span></td>
          </tr>
        `;
      }});

      let rowsEleitos = '';
      d.eleitos.forEach((c, idx) => {{
        const color = partyColors[c.partido] || ['#334155', '#ffffff'];
        rowsEleitos += `
          <tr>
            <td style="color: #94a3b8; font-weight: 600;">${{idx + 1}}º</td>
            <td><strong style="color: #ffffff;">${{c.nome}}</strong></td>
            <td style="font-family: monospace; color: #38bdf8; font-weight: 600;">${{c.num}}</td>
            <td><span class="party-tag" style="background: ${{color[0]}}; color: ${{color[1]}};">${{c.partido}}</span></td>
            <td class="num-col" style="font-weight: 700; color: #34d399;">${{fmt(c.votos)}}</td>
            <td style="color: var(--text-muted); font-size: 0.82rem;">${{c.agr}}</td>
          </tr>
        `;
      }});

      let cadeirasHtml = '';
      let seatIdx = 1;
      d.partidos.forEach(p => {{
        if (p.vagas > 0) {{
          const color = partyColors[p.sg] || ['#475569', '#ffffff'];
          for (let i = 0; i < p.vagas; i++) {{
            cadeirasHtml += `<div class="cadeira-seat" style="background-color: ${{color[0]}}; color: ${{color[1]}};" title="Cadeira #${{seatIdx}}: ${{p.sg}}">${{p.sg.substring(0,3)}}</div>`;
            seatIdx++;
          }}
        }}
      }});

      let rowsSobrasFila = '';
      d.proximos_fila.slice(0, 6).forEach((p, idx) => {{
        const diffPto = (p.media - ultSobra.media).toFixed(1);
        const color = partyColors[p.cand.partido] || ['#334155', '#ffffff'];
        rowsSobrasFila += `
          <tr>
            <td style="color:#38bdf8; font-weight:800;">${{idx + 1}}º</td>
            <td><strong style="color: #ffffff;">${{p.cand.nome}}</strong></td>
            <td><span class="party-tag" style="background:${{color[0]}}; color:${{color[1]}};">${{p.cand.partido}}</span></td>
            <td class="num-col" style="color:#34d399; font-weight:700;">${{fmt(p.cand.votos)}}</td>
            <td class="num-col" style="font-family:monospace;">${{p.media.toLocaleString('pt-BR', {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}}</td>
            <td class="num-col" style="color:#fbbf24;">${{diffPto}} pts</td>
            <td><span style="color:#38bdf8; font-weight:600;">${{idx === 0 ? 'Disputa direta no fio da navalha' : 'Aguardando urnas finais'}}</span></td>
          </tr>
        `;
      }});

      let duelosHtml = '';
      d.duelos_internos.slice(0, 3).forEach(duel => {{
        const color = partyColors[duel.ultimo.partido] || ['#334155', '#ffffff'];
        duelosHtml += `
          <div class="duel-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span class="party-tag" style="background:${{color[0]}}; color:${{color[1]}};">${{duel.partido.substring(0, 22)}}</span>
              <span style="font-size: 0.8rem; color:${{duel.diff < 200 ? '#f87171' : '#fbbf24'}}; font-weight: 700;">
                Diferença: ${{fmt(duel.diff)}} VOTOS!
              </span>
            </div>
            <div style="font-size: 0.9rem; color:#e2e8f0; margin-bottom: 4px;">
              ✅ <strong>${{duel.ultimo.nome}}:</strong> ${{fmt(duel.ultimo.votos)}} votos <span style="color:#34d399;">(Titular provisório)</span>
            </div>
            <div style="font-size: 0.9rem; color:#94a3b8;">
              ⏳ <strong>${{duel.suplente.nome}}:</strong> ${{fmt(duel.suplente.votos)}} votos <span style="color:#fbbf24;">(1º Suplente)</span>
            </div>
          </div>
        `;
      }});

      let sobrasHistHtml = '';
      d.historico_sobras.forEach(h => {{
        sobrasHistHtml += `${{h.rodada}}ª Sobra: <strong>${{h.partido.substring(0,25)}}</strong> (Média: ${{h.media.toLocaleString('pt-BR', {{minimumFractionDigits:1}})}}) &rarr; ${{h.cand.nome}} (${{h.cand.partido}})<br/>`;
      }});

      const html = `
        <!-- Top Header -->
        <header>
          <div class="header-top">
            <div class="badge-live">APURAÇÃO OFICIAL TSE &bull; ELEIÇÕES GERAIS 2026</div>
            <div style="color: var(--text-muted); font-size: 0.85rem;">
              Atualizado às ${{g.horario}} &bull; ${{g.secoes_pct}}% das seções apuradas
            </div>
          </div>
          <h1>Resultado para ${{d.cargo}} &mdash; São Paulo</h1>
          <p class="subtitle">Painel interativo oficial: Quociente Eleitoral, Distribuição das ${{g.vagas}} Cadeiras na ${{orgaoNome}} e Projeção das Sobras.</p>
        </header>

        <!-- KPI Summary Cards -->
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Quociente Eleitoral (QE)</div>
            <div class="kpi-value" style="color: #38bdf8;">${{fmt(g.qe)}}</div>
            <div class="kpi-desc">Votos necessários para 1 cadeira direta</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Total de Votos Válidos</div>
            <div class="kpi-value" style="color: #34d399;">${{fmt(g.validos)}}</div>
            <div class="kpi-desc">Votos nominais + legenda computados</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Cadeiras em Disputa</div>
            <div class="kpi-value" style="color: #fbbf24;">${{g.vagas}}</div>
            <div class="kpi-desc">Total de vagas na bancada paulista</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Total de Votos Apurados</div>
            <div class="kpi-value" style="color: #f8fafc;">${{fmt(g.total_apurado)}}</div>
            <div class="kpi-desc">Brancos: ${{fmt(g.brancos)}} &bull; Nulos: ${{fmt(g.nulos)}}</div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="tabs">
          <button class="tab-btn active" onclick="openTab('tab-sobras-proj', this)">🎯 Disputa das Sobras & Quem Pode Entrar</button>
          <button class="tab-btn" onclick="openTab('tab-partidos', this)">📊 Tabela por Partidos</button>
          <button class="tab-btn" onclick="openTab('tab-eleitos', this)">👥 ${{g.vagas}} Deputados Eleitos</button>
          <button class="tab-btn" onclick="openTab('tab-calculo', this)">📐 Memória de Cálculo (QE & Médias)</button>
          <button class="tab-btn" onclick="openTab('tab-bancada', this)">🏛️ Plenário (${{g.vagas}} Vagas)</button>
        </div>

        <!-- TAB: SOBRAS & PROJEÇÃO -->
        <div id="tab-sobras-proj" class="tab-content active">
          
          <div class="sobras-alert">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
              <span style="font-size: 1.25rem;">⚠️</span>
              <strong style="color: #f87171; font-size: 1.1rem;">Cenário em Aberto nas Seções Restantes (Art. 109 do Código Eleitoral)</strong>
            </div>
            <p style="color: #e2e8f0; font-size: 0.92rem; line-height: 1.5;">
              Com <strong>${{g.secoes_pct}}%</strong> das urnas totalizadas, a <strong>${{g.vagas}}ª cadeira</strong> (a última vaga de sobra) está sendo decidida por margem estreita de médias, além de disputas internas diretas com diferenças de menos de 100 votos entre titular e primeiro suplente!
            </p>
          </div>

          <!-- Cards Fio da Navalha -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-bottom: 24px;">
            <div class="bubble-card threatened">
              <span class="bubble-rank" style="background: rgba(244, 63, 94, 0.2); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.4);">
                ÚLTIMA CADEIRA CONQUISTADA (#${{g.vagas}})
              </span>
              <div style="font-size: 0.8rem; text-transform: uppercase; color: #f87171; font-weight: 700; margin-bottom: 8px;">
                🚨 No Fio da Navalha (Defendendo a Vaga)
              </div>
              <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">
                ${{ultSobra.cand.nome}}
              </div>
              <div style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 12px;">
                <strong>${{ultSobra.cand.partido}}</strong> &bull; ${{fmt(ultSobra.cand.votos)}} votos nominais
              </div>
              <div class="math-box" style="margin: 0; font-size: 0.85rem; padding: 10px; color: #fca5a5;">
                Média da Bancada (Última Sobra): <strong>${{ultSobra.media.toLocaleString('pt-BR', {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}}</strong>
              </div>
            </div>

            <div class="bubble-card hunting">
              <span class="bubble-rank" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4);">
                1º NA FILA DAS SOBRAS
              </span>
              <div style="font-size: 0.8rem; text-transform: uppercase; color: #38bdf8; font-weight: 700; margin-bottom: 8px;">
                ⚡ Pronto para Entrar (Maior Média Seguinte)
              </div>
              <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-bottom: 4px;">
                ${{proxFila.cand.nome}}
              </div>
              <div style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 12px;">
                <strong>${{proxFila.cand.partido}}</strong> &bull; ${{fmt(proxFila.cand.votos)}} votos nominais
              </div>
              <div class="math-box" style="margin: 0; font-size: 0.85rem; padding: 10px; color: #7dd3fc;">
                Média Necessária: <strong>${{proxFila.media.toLocaleString('pt-BR', {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}}</strong> (Dif: ${{(proxFila.media - ultSobra.media).toFixed(1)}} pts)
              </div>
            </div>
          </div>

          <!-- Tabela Próximos na Fila -->
          <div class="math-card">
            <h3>📋 Ranking dos Próximos na Fila das Sobras (Quem herda a vaga se a média virar)</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 16px;">
              Candidatos que cumprem a cláusula individual de 20% do QE (${{fmt(Math.round(g.qe * 0.2))}} votos) e cujos partidos atingiram mais de 80% do QE:
            </p>
            <div class="table-responsive">
              <table>
                <thead>
                  <tr>
                    <th style="width: 60px;">Fila</th>
                    <th>Candidato (1º Suplente)</th>
                    <th>Partido</th>
                    <th class="num-col">Votos Nominais</th>
                    <th class="num-col">Média da Vaga</th>
                    <th class="num-col">Distância da Vaga #${{g.vagas}}</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  ${{rowsSobrasFila}}
                </tbody>
              </table>
            </div>
          </div>

          <!-- Duelos Internos -->
          <div class="math-card">
            <h3>⚔️ Disputas Internas Acirradas (Menores Diferenças de Votos)</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 16px;">
              Se o suplente ultrapassar o titular dentro da mesma legenda nas urnas restantes, a titularidade se inverte:
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
              ${{duelosHtml}}
            </div>
          </div>

        </div>

        <!-- TAB: PARTIDOS -->
        <div id="tab-partidos" class="tab-content">
          <div class="filter-bar">
            <input type="text" id="partySearch" class="search-input" placeholder="🔍 Filtrar por partido ou sigla..." oninput="filterParties()" />
            <div style="color: var(--text-muted); font-size: 0.85rem;">
              Partidos ordenados pelo total de votos
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
                  ${{rowsPartidos}}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- TAB: ELEITOS -->
        <div id="tab-eleitos" class="tab-content">
          <div class="filter-bar">
            <input type="text" id="candSearch" class="search-input" placeholder="🔍 Buscar por nome do candidato ou partido..." oninput="filterCandidates()" />
            <div style="color: var(--text-muted); font-size: 0.85rem;">
              Os ${{g.vagas}} deputados eleitos para a ${{isEstadual ? '21ª Legislatura da ALESP' : '60ª Legislatura da Câmara'}}
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
                  ${{rowsEleitos}}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- TAB: CALCULO -->
        <div id="tab-calculo" class="tab-content">
          <div class="math-card">
            <h3>1. Quociente Eleitoral (QE) &mdash; Artigo 106 do Código Eleitoral</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem;">
              Votos válidos necessários para conquistar 1 vaga direta:
            </p>
            <div class="math-box">
              QE = Total de Votos Válidos / Número de Cadeiras<br/>
              QE = ${{fmt(g.validos)}} / ${{g.vagas}} = <strong>${{fmt(g.qe)}} votos</strong>
            </div>
          </div>

          <div class="math-card">
            <h3>2. Quociente Partidário (QP) e Trava Individual de 10%</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem;">
              Vagas diretas iniciais por legenda (QP = Votos &divide; QE) com exigência individual de 10% do QE (${{fmt(Math.round(g.qe * 0.1))}} votos):
            </p>
            <div class="math-box">
              ${{d.partidos.filter(p => p.vagas > 0).map(p => `&bull; <strong>${{p.sg}}:</strong> ${{fmt(p.tot)}} votos &rarr; ${{p.vagas}} cadeiras conquistadas`).join('<br/>')}}
            </div>
          </div>

          <div class="math-card">
            <h3>3. Distribuição das ${{d.sobras_tot}} Sobras Rodada a Rodada (Artigo 109)</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem;">
              Sequência de alocação pelas maiores médias:
            </p>
            <div class="math-box">
              ${{sobrasHistHtml}}
            </div>
          </div>
        </div>

        <!-- TAB: BANCADA -->
        <div id="tab-bancada" class="tab-content">
          <div class="math-card">
            <h3>Distribuição Visual das ${{g.vagas}} Cadeiras no Plenário</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 18px;">
              Passe o mouse sobre o assento para ver a legenda partidária:
            </p>
            <div class="bancada-chart">
              ${{cadeirasHtml}}
            </div>
          </div>
        </div>
      `;

      document.getElementById('cargoContent').innerHTML = html;
    }}

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

    // Initial render: Deputado Estadual
    renderDashboard();
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Dashboard unificado (Estadual default + switcher Federal) gerado em index.html com sucesso!")
