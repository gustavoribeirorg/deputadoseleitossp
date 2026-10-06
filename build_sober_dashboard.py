import json

with open('dados_estadual.json', 'r', encoding='utf-8') as f:
    estadual = json.load(f)

with open('dados_federal.json', 'r', encoding='utf-8') as f:
    federal = json.load(f)

# Party colors - sober, readable palette for light mode
party_palette = {
    'PL': ('#1e3a8a', '#eff6ff'),
    'PT': ('#b91c1c', '#fef2f2'),
    'PODE': ('#0d9488', '#f0fdfa'),
    'PSOL': ('#b45309', '#fefce8'),
    'PSD': ('#2563eb', '#eff6ff'),
    'REPUBLICANOS': ('#4338ca', '#eef2ff'),
    'MDB': ('#15803d', '#f0fdf4'),
    'PP': ('#0284c7', '#f0f9ff'),
    'PSB': ('#ea580c', '#fff7ed'),
    'UNIÃO': ('#0369a1', '#f0f9ff'),
    'NOVO': ('#c2410c', '#fff7ed'),
    'MISSÃO': ('#6d28d9', '#faf5ff'),
    'PSDB': ('#0284c7', '#f0f9ff'),
    'PRD': ('#475569', '#f8fafc'),
    'CIDADANIA': ('#0284c7', '#f0f9ff')
}

html_code = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Eleições 2026 SP — Apuração Oficial (Estadual e Federal)</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #e2e8f0;
      --border-subtle: #cbd5e1;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --text-sub: #475569;
      --primary: #1e40af;
      --primary-light: #eff6ff;
      --primary-border: #bfdbfe;
      --accent-gray: #f1f5f9;
      --accent-slate: #334155;
      --table-hover: #f8fafc;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      line-height: 1.5;
      padding: 32px 16px;
      -webkit-font-smoothing: antialiased;
    }}

    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}

    /* Switcher */
    .cargo-switcher {{
      display: flex;
      justify-content: center;
      gap: 8px;
      margin-bottom: 24px;
    }}

    .cargo-btn {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text-sub);
      padding: 10px 20px;
      border-radius: 8px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .cargo-btn:hover {{
      border-color: var(--border-subtle);
      color: var(--text-main);
      background: #fafafa;
    }}

    .cargo-btn.active {{
      background: var(--primary);
      border-color: var(--primary);
      color: #ffffff;
    }}

    /* Header */
    header {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px 28px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }}

    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 8px;
    }}

    .badge-status {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #e2e8f0;
      padding: 4px 12px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.2px;
    }}

    .badge-status::before {{
      content: '';
      width: 6px;
      height: 6px;
      background-color: #059669;
      border-radius: 50%;
    }}

    .header-date {{
      color: var(--text-muted);
      font-size: 0.85rem;
    }}

    h1 {{
      font-size: 1.65rem;
      font-weight: 700;
      letter-spacing: -0.4px;
      color: var(--text-main);
      margin-bottom: 4px;
    }}

    .subtitle {{
      color: var(--text-muted);
      font-size: 0.92rem;
    }}

    /* KPI Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px 20px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }}

    .kpi-label {{
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 4px;
      font-weight: 600;
    }}

    .kpi-value {{
      font-size: 1.65rem;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.2;
    }}

    .kpi-desc {{
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-top: 4px;
    }}

    /* Tabs */
    .tabs {{
      display: flex;
      gap: 4px;
      margin-bottom: 18px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
      overflow-x: auto;
    }}

    .tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 16px;
      font-size: 0.9rem;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
    }}

    .tab-btn:hover {{
      color: var(--text-main);
      background-color: #f1f5f9;
    }}

    .tab-btn.active {{
      color: var(--primary);
      background-color: var(--primary-light);
    }}

    /* Tab Content */
    .tab-content {{
      display: none;
    }}

    .tab-content.active {{
      display: block;
    }}

    /* Filter Bar */
    .filter-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 14px;
    }}

    .search-input {{
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 0.88rem;
      width: 100%;
      max-width: 320px;
      outline: none;
      transition: border-color 0.15s;
    }}

    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(30, 64, 175, 0.1);
    }}

    /* Tables */
    .table-container {{
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }}

    .table-responsive {{
      width: 100%;
      overflow-x: auto;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.88rem;
    }}

    th {{
      background-color: #f8fafc;
      padding: 12px 14px;
      color: var(--text-sub);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.72rem;
      letter-spacing: 0.5px;
      border-bottom: 1px solid var(--border);
    }}

    td {{
      padding: 12px 14px;
      border-bottom: 1px solid #f1f5f9;
      color: var(--text-main);
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
      padding: 3px 8px;
      border-radius: 4px;
      font-weight: 600;
      font-size: 0.78rem;
      border: 1px solid rgba(0, 0, 0, 0.08);
    }}

    .badge-vagas {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 24px;
      height: 24px;
      border-radius: 6px;
      background-color: #e0f2fe;
      color: #0369a1;
      font-weight: 700;
      font-size: 0.82rem;
    }}

    .badge-zero {{
      background-color: #f1f5f9;
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
      width: 60px;
      height: 5px;
      background-color: #e2e8f0;
      border-radius: 3px;
      overflow: hidden;
    }}

    .pct-fill {{
      height: 100%;
      background-color: #2563eb;
      border-radius: 3px;
    }}

    /* Card Panels */
    .info-card {{
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px 22px;
      margin-bottom: 18px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }}

    .info-card h3 {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 8px;
    }}

    .info-box {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 14px 16px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.88rem;
      color: #334155;
      margin: 10px 0;
      line-height: 1.6;
    }}

    /* Projections */
    .notice-card {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 20px;
    }}

    .notice-card p {{
      color: var(--text-sub);
      font-size: 0.9rem;
      line-height: 1.5;
    }}

    .projections-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
      margin-bottom: 20px;
    }}

    .status-panel {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 18px;
    }}

    .status-panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}

    .status-panel-tag {{
      font-size: 0.72rem;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.4px;
      padding: 2px 8px;
      border-radius: 4px;
      background: #f1f5f9;
      color: #475569;
    }}

    .cand-name {{
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 4px;
    }}

    .cand-meta {{
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 12px;
    }}

    .calc-row {{
      background: #f8fafc;
      border: 1px solid #f1f5f9;
      border-radius: 6px;
      padding: 10px 12px;
      font-size: 0.84rem;
      color: var(--text-sub);
      font-family: monospace;
    }}

    .duel-item {{
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
      margin-bottom: 10px;
    }}

    /* Plenary Diagram */
    .bancada-chart {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding: 20px;
      background: #f8fafc;
      border-radius: 8px;
      margin-bottom: 18px;
      border: 1px solid var(--border);
      justify-content: center;
    }}

    .cadeira-seat {{
      width: 28px;
      height: 28px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.65rem;
      font-weight: 700;
      cursor: pointer;
      transition: opacity 0.15s, transform 0.15s;
      border: 1px solid rgba(0, 0, 0, 0.08);
    }}

    .cadeira-seat:hover {{
      transform: scale(1.15);
      z-index: 5;
    }}

    footer {{
      text-align: center;
      margin-top: 32px;
      color: var(--text-muted);
      font-size: 0.82rem;
    }}
  </style>
</head>
<body>
  <div class="container">

    <!-- Switcher -->
    <div class="cargo-switcher">
      <button id="btnCargoEstadual" class="cargo-btn active" onclick="switchCargo('estadual')">
        Deputado Estadual (ALESP &bull; 94 Cadeiras)
      </button>
      <button id="btnCargoFederal" class="cargo-btn" onclick="switchCargo('federal')">
        Deputado Federal (Câmara &bull; 70 Cadeiras)
      </button>
    </div>

    <!-- Content rendered via JS -->
    <div id="cargoContent"></div>

    <footer>
      Tribunal Superior Eleitoral (TSE) &bull; Eleições Gerais 2026 &bull; Estado de São Paulo
    </footer>

  </div>

  <script>
    const dataEstadual = {json.dumps(estadual, ensure_ascii=False)};
    const dataFederal = {json.dumps(federal, ensure_ascii=False)};
    const partyPalette = {json.dumps(party_palette, ensure_ascii=False)};

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
      const orgaoNome = isEstadual ? 'Assembleia Legislativa de São Paulo (ALESP)' : 'Câmara dos Deputados';

      const ultSobra = d.historico_sobras[d.historico_sobras.length - 1];
      const proxFila = d.proximos_fila[0];

      let rowsPartidos = '';
      d.partidos.forEach((p, idx) => {{
        const badgeCls = p.vagas > 0 ? 'badge-vagas' : 'badge-vagas badge-zero';
        const fedLabel = p.fed !== '-' ? p.fed : '<span style="color:#94a3b8;">Isolado</span>';
        const fillW = Math.min(100, p.pct * 3.5);
        const pctStr = p.pct.toLocaleString('pt-BR', {{minimumFractionDigits: 2}}) + '%';
        rowsPartidos += `
          <tr>
            <td style="color: #64748b; font-weight: 600;">${{idx + 1}}º</td>
            <td><strong>${{p.sg}}</strong> &mdash; <span style="color: var(--text-muted); font-size: 0.8rem;">${{p.nm}}</span></td>
            <td style="font-size: 0.82rem; color: #475569;">${{fedLabel}}</td>
            <td class="num-col">${{fmt(p.tvtn)}}</td>
            <td class="num-col" style="color: var(--text-muted);">${{fmt(p.tvtl)}}</td>
            <td class="num-col" style="font-weight: 600;">${{fmt(p.tot)}}</td>
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
        const colors = partyPalette[c.partido] || ['#334155', '#f8fafc'];
        rowsEleitos += `
          <tr>
            <td style="color: #64748b; font-weight: 600;">${{idx + 1}}º</td>
            <td><strong>${{c.nome}}</strong></td>
            <td style="font-family: monospace; color: var(--text-sub);">${{c.num}}</td>
            <td><span class="party-tag" style="color: ${{colors[0]}}; background: ${{colors[1]}};">${{c.partido}}</span></td>
            <td class="num-col" style="font-weight: 600;">${{fmt(c.votos)}}</td>
            <td style="color: var(--text-muted); font-size: 0.82rem;">${{c.agr}}</td>
          </tr>
        `;
      }});

      let cadeirasHtml = '';
      let seatIdx = 1;
      d.partidos.forEach(p => {{
        if (p.vagas > 0) {{
          const colors = partyPalette[p.sg] || ['#334155', '#f8fafc'];
          for (let i = 0; i < p.vagas; i++) {{
            cadeirasHtml += `<div class="cadeira-seat" style="color: ${{colors[0]}}; background-color: ${{colors[1]}};" title="Cadeira #${{seatIdx}}: ${{p.sg}}">${{p.sg.substring(0,3)}}</div>`;
            seatIdx++;
          }}
        }}
      }});

      let rowsSobrasFila = '';
      d.proximos_fila.slice(0, 6).forEach((p, idx) => {{
        const diffPto = (p.media - ultSobra.media).toFixed(1);
        const colors = partyPalette[p.cand.partido] || ['#334155', '#f8fafc'];
        rowsSobrasFila += `
          <tr>
            <td style="font-weight:600; color: #475569;">${{idx + 1}}º</td>
            <td><strong>${{p.cand.nome}}</strong></td>
            <td><span class="party-tag" style="color: ${{colors[0]}}; background: ${{colors[1]}};">${{p.cand.partido}}</span></td>
            <td class="num-col">${{fmt(p.cand.votos)}}</td>
            <td class="num-col" style="font-family: monospace;">${{p.media.toLocaleString('pt-BR', {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}}</td>
            <td class="num-col" style="color: #64748b;">${{diffPto}} pts</td>
            <td><span style="color: var(--text-sub); font-size: 0.84rem;">${{idx === 0 ? 'Maior média subsequente' : 'Suplente na ordem'}}</span></td>
          </tr>
        `;
      }});

      let duelosHtml = '';
      d.duelos_internos.slice(0, 3).forEach(duel => {{
        const colors = partyPalette[duel.ultimo.partido] || ['#334155', '#f8fafc'];
        duelosHtml += `
          <div class="duel-item">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span class="party-tag" style="color: ${{colors[0]}}; background: ${{colors[1]}};">${{duel.partido.substring(0, 26)}}</span>
              <span style="font-size: 0.8rem; color: #475569; font-weight: 600;">
                Diferença: ${{fmt(duel.diff)}} votos nominais
              </span>
            </div>
            <div style="font-size: 0.88rem; color: var(--text-main); margin-bottom: 2px;">
              Titular provisório: <strong>${{duel.ultimo.nome}}</strong> (${{fmt(duel.ultimo.votos)}} votos)
            </div>
            <div style="font-size: 0.88rem; color: var(--text-muted);">
              Primeiro suplente: <strong>${{duel.suplente.nome}}</strong> (${{fmt(duel.suplente.votos)}} votos)
            </div>
          </div>
        `;
      }});

      let sobrasHistHtml = '';
      d.historico_sobras.forEach(h => {{
        sobrasHistHtml += `${{h.rodada}}ª Sobra: <strong>${{h.partido.substring(0,25)}}</strong> (Média: ${{h.media.toLocaleString('pt-BR', {{minimumFractionDigits:1}})}}) &rarr; ${{h.cand.nome}} (${{h.cand.partido}})<br/>`;
      }});

      const html = `
        <header>
          <div class="header-top">
            <div class="badge-status">TSE &bull; Apuração em Andamento</div>
            <div class="header-date">
              Atualizado às ${{g.horario}} &bull; ${{g.secoes_pct}}% das seções totalizadas
            </div>
          </div>
          <h1>${{d.cargo}} &mdash; São Paulo</h1>
          <p class="subtitle">Acompanhamento da apuração oficial, cálculo de quocientes e distribuição das ${{g.vagas}} cadeiras na ${{orgaoNome}}.</p>
        </header>

        <!-- KPI Grid -->
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Quociente Eleitoral (QE)</div>
            <div class="kpi-value">${{fmt(g.qe)}}</div>
            <div class="kpi-desc">Votos necessários para 1 cadeira direta</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Total de Votos Válidos</div>
            <div class="kpi-value">${{fmt(g.validos)}}</div>
            <div class="kpi-desc">Nominais e votos de legenda</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Cadeiras em Disputa</div>
            <div class="kpi-value">${{g.vagas}}</div>
            <div class="kpi-desc">Total de assentos na bancada paulista</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Total de Votos Apurados</div>
            <div class="kpi-value">${{fmt(g.total_apurado)}}</div>
            <div class="kpi-desc">Brancos: ${{fmt(g.brancos)}} &bull; Nulos: ${{fmt(g.nulos)}}</div>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="tabs">
          <button class="tab-btn active" onclick="openTab('tab-partidos', this)">Tabela por Partidos</button>
          <button class="tab-btn" onclick="openTab('tab-eleitos', this)">${{g.vagas}} Deputados Eleitos</button>
          <button class="tab-btn" onclick="openTab('tab-sobras-proj', this)">Distribuição das Sobras</button>
          <button class="tab-btn" onclick="openTab('tab-calculo', this)">Memória de Cálculo (QE)</button>
          <button class="tab-btn" onclick="openTab('tab-bancada', this)">Plenário (${{g.vagas}} Vagas)</button>
        </div>

        <!-- TAB: PARTIDOS -->
        <div id="tab-partidos" class="tab-content active">
          <div class="filter-bar">
            <input type="text" id="partySearch" class="search-input" placeholder="Buscar por partido ou sigla..." oninput="filterParties()" />
            <div style="color: var(--text-muted); font-size: 0.82rem;">
              Lista de partidos ordenada pelo total de votos obtidos
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
                    <th style="text-align: center; width: 90px;">Cadeiras</th>
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
            <input type="text" id="candSearch" class="search-input" placeholder="Buscar por candidato ou partido..." oninput="filterCandidates()" />
            <div style="color: var(--text-muted); font-size: 0.82rem;">
              Os ${{g.vagas}} candidatos mais votados dentro do número de vagas de cada legenda
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

        <!-- TAB: SOBRAS -->
        <div id="tab-sobras-proj" class="tab-content">
          
          <div class="notice-card">
            <p>
              Com ${{g.secoes_pct}}% da apuração totalizada, a alocação da última cadeira remanescente (${{g.vagas}}ª vaga) segue a sistemática de maiores médias estabelecida pelo Artigo 109 do Código Eleitoral. Abaixo constam a legenda atualmente detentora da última vaga e os primeiros suplentes da fila de classificação.
            </p>
          </div>

          <div class="projections-grid">
            <div class="status-panel">
              <div class="status-panel-header">
                <span class="status-panel-tag">Última Vaga Alocada (#${{g.vagas}})</span>
              </div>
              <div class="cand-name">${{ultSobra.cand.nome}}</div>
              <div class="cand-meta">
                ${{ultSobra.cand.partido}} &bull; ${{fmt(ultSobra.cand.votos)}} votos nominais
              </div>
              <div class="calc-row">
                Média da Bancada: <strong>${{ultSobra.media.toLocaleString('pt-BR', {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}}</strong>
              </div>
            </div>

            <div class="status-panel">
              <div class="status-panel-header">
                <span class="status-panel-tag">Primeiro da Fila das Sobras</span>
              </div>
              <div class="cand-name">${{proxFila.cand.nome}}</div>
              <div class="cand-meta">
                ${{proxFila.cand.partido}} &bull; ${{fmt(proxFila.cand.votos)}} votos nominais
              </div>
              <div class="calc-row">
                Média da Bancada: <strong>${{proxFila.media.toLocaleString('pt-BR', {{minimumFractionDigits: 1, maximumFractionDigits: 1}})}}</strong> (Diferença: ${{(proxFila.media - ultSobra.media).toFixed(1)}} pts)
              </div>
            </div>
          </div>

          <div class="info-card">
            <h3>Classificação das Próximas Médias Partidárias</h3>
            <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 14px;">
              Candidatos que atendem aos requisitos legais de 20% do QE (${{fmt(Math.round(g.qe * 0.2))}} votos nominais) em legendas que alcançaram ao menos 80% do QE:
            </p>
            <div class="table-responsive">
              <table>
                <thead>
                  <tr>
                    <th style="width: 50px;">Fila</th>
                    <th>Candidato (Suplente)</th>
                    <th>Partido</th>
                    <th class="num-col">Votação Nominal</th>
                    <th class="num-col">Média Partidária</th>
                    <th class="num-col">Diferença para a Última Vaga</th>
                    <th>Posição</th>
                  </tr>
                </thead>
                <tbody>
                  ${{rowsSobrasFila}}
                </tbody>
              </table>
            </div>
          </div>

          <div class="info-card">
            <h3>Margens Mais Estreitas na Disputa Interna</h3>
            <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 14px;">
              Diferenças nominais entre o último titular provisório e o primeiro suplente dentro da mesma legenda:
            </p>
            ${{duelosHtml}}
          </div>

        </div>

        <!-- TAB: CALCULO -->
        <div id="tab-calculo" class="tab-content">
          <div class="info-card">
            <h3>1. Quociente Eleitoral (QE) &mdash; Artigo 106</h3>
            <p style="color: var(--text-muted); font-size: 0.88rem;">
              Divisão do total de votos válidos pelo número de lugares a preencher:
            </p>
            <div class="info-box">
              QE = Total de Votos Válidos / Número de Cadeiras<br/>
              QE = ${{fmt(g.validos)}} / ${{g.vagas}} = <strong>${{fmt(g.qe)}} votos</strong>
            </div>
          </div>

          <div class="info-card">
            <h3>2. Vagas por Quociente Partidário (QP)</h3>
            <p style="color: var(--text-muted); font-size: 0.88rem;">
              Número inicial de vagas obtido pela divisão da votação de cada partido pelo QE:
            </p>
            <div class="info-box">
              ${{d.partidos.filter(p => p.vagas > 0).map(p => `&bull; <strong>${{p.sg}}:</strong> ${{fmt(p.tot)}} votos &rarr; ${{p.vagas}} cadeiras conquistadas`).join('<br/>')}}
            </div>
          </div>

          <div class="info-card">
            <h3>3. Alocação das Sobras pelas Maiores Médias &mdash; Artigo 109</h3>
            <p style="color: var(--text-muted); font-size: 0.88rem;">
              Sequência de preenchimento das ${{d.sobras_tot}} vagas remanescentes:
            </p>
            <div class="info-box">
              ${{sobrasHistHtml}}
            </div>
          </div>
        </div>

        <!-- TAB: BANCADA -->
        <div id="tab-bancada" class="tab-content">
          <div class="info-card">
            <h3>Composição da Bancada (${{g.vagas}} Cadeiras)</h3>
            <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 14px;">
              Visualização esquemática da distribuição das vagas na ${{orgaoNome}}:
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

    // Default to Deputado Estadual
    renderDashboard();
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Dashboard sóbrio e clean gerado em index.html com sucesso!")
