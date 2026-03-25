<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Apex Precision | F1 Race Relay Executive Dashboard</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Inter:wght@400;500;600&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<script>
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            colors: {
              "on-surface-variant": "#414751",
              "on-primary": "#ffffff",
              "surface-variant": "#e1e2e4",
              "surface-container-low": "#f2f4f6",
              "on-tertiary": "#ffffff",
              "on-primary-fixed-variant": "#004883",
              "on-secondary-container": "#5e6570",
              "surface-container-high": "#e7e8ea",
              "on-primary-container": "#fdfcff",
              "surface-container-highest": "#e1e2e4",
              "on-surface": "#191c1e",
              "on-tertiary-container": "#fffbff",
              "surface": "#f8f9fb",
              "surface-bright": "#f8f9fb",
              "on-secondary": "#ffffff",
              "surface-container": "#edeef0",
              "primary-fixed": "#d4e3ff",
              "surface-dim": "#d9dadc",
              "tertiary-container": "#a06900",
              "inverse-surface": "#2e3132",
              "secondary": "#585f6a",
              "tertiary-fixed-dim": "#ffb953",
              "surface-tint": "#0060ac",
              "on-secondary-fixed": "#151c25",
              "tertiary-fixed": "#ffddb4",
              "inverse-primary": "#a4c9ff",
              "tertiary": "#7f5300",
              "primary": "#005da7",
              "on-tertiary-fixed": "#291800",
              "surface-container-lowest": "#ffffff",
              "secondary-container": "#dce3f0",
              "on-background": "#191c1e",
              "inverse-on-surface": "#f0f1f3",
              "error-container": "#ffdad6",
              "on-error": "#ffffff",
              "outline-variant": "#c1c7d3",
              "outline": "#717783",
              "background": "#f8f9fb",
              "primary-fixed-dim": "#a4c9ff",
              "on-tertiary-fixed-variant": "#633f00",
              "error": "#ba1a1a",
              "secondary-fixed-dim": "#c0c7d3",
              "secondary-fixed": "#dce3f0",
              "primary-container": "#2976c7",
              "on-error-container": "#93000a",
              "on-secondary-fixed-variant": "#404752",
              "on-primary-fixed": "#001c39"
            },
            fontFamily: {
              "headline": ["Manrope"],
              "body": ["Inter"],
              "label": ["Space Grotesk"]
            },
            borderRadius: {"DEFAULT": "0.125rem", "lg": "0.25rem", "xl": "0.5rem", "full": "0.75rem"},
          },
        },
      }
    </script>
<style>
      .material-symbols-outlined {
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
      }
      .no-scrollbar::-webkit-scrollbar { display: none; }
      .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
      
      /* Terminal-like output styling */
      .terminal-output {
        font-family: 'Space Grotesk', monospace;
        font-size: 11px;
        line-height: 1.6;
        white-space: pre-wrap;
      }
      .terminal-output .gold { color: #D4A843; }
      .terminal-output .silver { color: #9BA8B0; }
      .terminal-output .bronze { color: #B07D52; }
      .terminal-output .primary { color: #005da7; }
      .terminal-output .success { color: #10b981; }
      .terminal-output .warning { color: #f59e0b; }
      .terminal-output .error { color: #ef4444; }
      
      /* Animation for loading states */
      @keyframes pulse-glow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
      }
      .pulse-glow {
        animation: pulse-glow 1.5s ease-in-out infinite;
      }
      
      /* Table styling */
      .race-table {
        width: 100%;
        font-size: 12px;
      }
      .race-table th {
        text-align: left;
        padding: 12px 8px;
        font-weight: 600;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #585f6a;
        border-bottom: 1px solid #e1e2e4;
      }
      .race-table td {
        padding: 10px 8px;
        border-bottom: 1px solid #edeef0;
      }
      .race-table tr:hover {
        background: #f2f4f6;
      }
      .pos-1 { color: #D4A843; font-weight: 700; }
      .pos-2 { color: #9BA8B0; font-weight: 700; }
      .pos-3 { color: #B07D52; font-weight: 700; }
      
      /* Scrollbar styling */
      ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
      }
      ::-webkit-scrollbar-track {
        background: #e1e2e4;
        border-radius: 4px;
      }
      ::-webkit-scrollbar-thumb {
        background: #005da7;
        border-radius: 4px;
      }
    </style>
</head>
<body class="bg-surface text-on-surface font-body selection:bg-primary-fixed selection:text-on-primary-fixed">

<!-- TopNavBar -->
<header class="fixed top-0 left-0 right-0 z-50 h-16 bg-surface flex justify-between items-center w-full px-6 border-b border-outline-variant/30">
  <div class="flex items-center gap-8">
    <span class="text-xl font-bold tracking-tighter text-on-surface font-headline">F1 RACE RELAY</span>
    <nav class="hidden md:flex items-center gap-6">
      <select id="nav-year" class="bg-transparent font-headline tracking-wide text-sm font-semibold text-primary border-none focus:ring-0 cursor-pointer">
        <option value="2024">2024 Season</option>
        <option value="2023" selected>2023 Season</option>
        <option value="2022">2022 Season</option>
        <option value="2021">2021 Season</option>
      </select>
      <select id="nav-track" class="bg-transparent font-headline tracking-wide text-sm font-semibold text-on-surface-variant border-none focus:ring-0 cursor-pointer">
        <option value="Bahrain">Bahrain GP</option>
        <option value="Monaco" selected>Monaco GP</option>
        <option value="Silverstone">Silverstone GP</option>
        <option value="Spa">Spa GP</option>
        <option value="Monza">Monza GP</option>
        <option value="Hungaroring">Hungaroring GP</option>
        <option value="Suzuka">Suzuka GP</option>
        <option value="Singapore">Singapore GP</option>
      </select>
      <span id="active-driver-display" class="font-headline tracking-wide text-sm font-semibold text-on-surface-variant">Max Verstappen</span>
    </nav>
  </div>
  <div class="flex items-center gap-4">
    <button id="export-data-btn" class="hidden lg:flex px-4 py-2 bg-surface-container-high text-primary rounded-xl font-headline text-sm font-semibold hover:bg-surface-variant transition-all">Export Data</button>
    <button id="live-telemetry-btn" class="px-4 py-2 bg-gradient-to-br from-primary to-primary-container text-on-primary rounded-xl font-headline text-sm font-semibold shadow-sm transition-all hover:scale-105 active:scale-95">Live Telemetry</button>
    <div class="flex items-center gap-2 ml-2">
      <span class="material-symbols-outlined p-2 text-on-surface-variant hover:bg-surface-container-high rounded-full cursor-pointer transition-colors">notifications</span>
      <span class="material-symbols-outlined p-2 text-on-surface-variant hover:bg-surface-container-high rounded-full cursor-pointer transition-colors">settings</span>
      <img alt="Profile" class="w-8 h-8 rounded-full ml-2 object-cover border-2 border-primary" src="https://ui-avatars.com/api/?name=F1&background=005da7&color=fff&bold=true"/>
    </div>
  </div>
</header>

<!-- SideNavBar -->
<aside class="fixed left-0 top-0 h-full w-20 bg-surface-container-low flex flex-col items-center py-8 gap-8 z-40 mt-16">
  <div class="flex flex-col items-center gap-6 w-full px-2">
    <div class="group flex flex-col items-center gap-1 cursor-pointer w-full py-3 bg-white text-primary rounded-xl shadow-sm transition-all" data-tab="dashboard">
      <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">dashboard</span>
      <span class="font-body text-[9px] uppercase tracking-widest font-bold">Dash</span>
    </div>
    <div class="group flex flex-col items-center gap-1 cursor-pointer w-full py-3 text-on-surface-variant hover:text-primary hover:translate-x-1 transition-all duration-300" data-tab="results">
      <span class="material-symbols-outlined">leaderboard</span>
      <span class="font-body text-[9px] uppercase tracking-widest">Results</span>
    </div>
    <div class="group flex flex-col items-center gap-1 cursor-pointer w-full py-3 text-on-surface-variant hover:text-primary hover:translate-x-1 transition-all duration-300" data-tab="compare">
      <span class="material-symbols-outlined">compare_arrows</span>
      <span class="font-body text-[9px] uppercase tracking-widest">Compare</span>
    </div>
    <div class="group flex flex-col items-center gap-1 cursor-pointer w-full py-3 text-on-surface-variant hover:text-primary hover:translate-x-1 transition-all duration-300" data-tab="visuals">
      <span class="material-symbols-outlined">insights</span>
      <span class="font-body text-[9px] uppercase tracking-widest">Visuals</span>
    </div>
  </div>
  <div class="mt-auto flex flex-col items-center gap-6 w-full px-2 mb-20">
    <div class="group flex flex-col items-center gap-1 cursor-pointer w-full py-3 text-on-surface-variant hover:text-primary transition-all" onclick="pingAPI()">
      <span class="material-symbols-outlined">wifi</span>
      <span class="font-body text-[9px] uppercase tracking-widest">Status</span>
    </div>
  </div>
</aside>

<!-- Main Content -->
<main class="ml-20 mt-16 p-8 min-h-screen">
  <div class="max-w-7xl mx-auto">
    
    <!-- Dashboard Header -->
    <div class="mb-10 flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h1 id="dashboard-title" class="font-headline text-3xl font-extrabold tracking-tight text-on-surface">Apex Precision Performance</h1>
        <p id="dashboard-subtitle" class="text-on-surface-variant font-body mt-1">Real-time telemetry and championship projection</p>
      </div>
      <div class="flex items-center gap-3 bg-surface-container px-4 py-2 rounded-xl">
        <div class="flex flex-col items-end">
          <span class="font-label text-xs uppercase tracking-widest text-on-surface-variant">API Status</span>
          <span id="api-status-text" class="font-headline font-bold text-primary">CONNECTING</span>
        </div>
        <div id="api-status-dot" class="w-2 h-2 rounded-full bg-error animate-pulse"></div>
      </div>
    </div>

    <!-- Tab Content: Dashboard View -->
    <div id="dashboard-view" class="grid grid-cols-1 md:grid-cols-12 gap-6">
      <!-- KPI: Winner -->
      <div class="md:col-span-4 bg-surface-container-low rounded-xl p-6 flex flex-col justify-between hover:bg-surface-container-high transition-all">
        <div class="flex justify-between items-start">
          <div>
            <p class="font-label text-xs font-bold uppercase tracking-widest text-secondary mb-1">Race Winner</p>
            <h3 class="font-headline text-lg font-bold">Current Leader</h3>
          </div>
          <span class="material-symbols-outlined text-primary">emoji_events</span>
        </div>
        <div class="mt-8">
          <span id="kpi-winner" class="font-label text-5xl font-bold tracking-tighter">—</span>
        </div>
        <div class="mt-4 flex items-center gap-2 text-xs font-medium text-primary">
          <span class="material-symbols-outlined text-sm">flag</span>
          <span id="kpi-winner-team">—</span>
        </div>
      </div>

      <!-- KPI: Fastest Lap -->
      <div class="md:col-span-4 bg-surface-container-low rounded-xl p-6 flex flex-col justify-between hover:bg-surface-container-high transition-all">
        <div class="flex justify-between items-start">
          <div>
            <p class="font-label text-xs font-bold uppercase tracking-widest text-secondary mb-1">Fastest Lap</p>
            <h3 class="font-headline text-lg font-bold">Purple Sector</h3>
          </div>
          <span class="material-symbols-outlined text-primary">speed</span>
        </div>
        <div class="mt-8">
          <span id="kpi-fastest-time" class="font-label text-3xl font-bold">—</span>
        </div>
        <div class="mt-4 flex items-center gap-2 text-xs font-medium">
          <span class="material-symbols-outlined text-sm text-secondary">person</span>
          <span id="kpi-fastest-driver" class="text-secondary">—</span>
          <span class="text-secondary ml-2">Lap <span id="kpi-fastest-lap">—</span></span>
        </div>
      </div>

      <!-- KPI: Race Info -->
      <div class="md:col-span-4 bg-gradient-to-br from-primary to-primary-container rounded-xl p-6 text-on-primary flex flex-col justify-between relative overflow-hidden">
        <div class="relative z-10">
          <p class="font-label text-xs font-bold uppercase tracking-widest opacity-80 mb-1">Race Information</p>
          <h3 id="kpi-track" class="font-headline text-lg font-bold">—</h3>
          <div class="mt-4">
            <span id="kpi-laps" class="font-label text-4xl font-extrabold tracking-tighter">—</span>
            <span class="font-label text-sm opacity-80 ml-1">laps</span>
          </div>
        </div>
        <div class="relative z-10 mt-4 flex items-center gap-2 text-xs font-semibold">
          <span id="kpi-finishers" class="bg-white/20 px-2 py-1 rounded">— finishers</span>
          <span id="kpi-date" class="bg-white/20 px-2 py-1 rounded">—</span>
        </div>
        <span class="material-symbols-outlined absolute -bottom-4 -right-4 text-white/10 text-9xl rotate-12">flag_circle</span>
      </div>

      <!-- Results Table Preview -->
      <div class="md:col-span-12 bg-surface-container-low rounded-xl p-6 mt-4">
        <div class="flex justify-between items-center mb-6">
          <h3 class="font-headline text-xl font-bold">Race Classification</h3>
          <button id="view-full-results" class="text-primary text-sm font-semibold hover:underline">View Full Results →</button>
        </div>
        <div class="overflow-x-auto">
          <table class="race-table" id="preview-table">
            <thead>
              <tr><th>POS</th><th>DRIVER</th><th>TEAM</th><th>TIME</th><th>GAP</th></tr>
            </thead>
            <tbody id="preview-tbody">
              <tr><td colspan="5" class="text-center py-8 text-on-surface-variant">Load race data to see results</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Tab Content: Results View (Full Table) -->
    <div id="results-view" class="hidden">
      <div class="bg-surface-container-low rounded-xl p-6">
        <div class="flex justify-between items-center mb-6">
          <h3 class="font-headline text-xl font-bold">Full Race Classification</h3>
          <span id="results-event-name" class="text-on-surface-variant text-sm"></span>
        </div>
        <div class="overflow-x-auto max-h-[600px] overflow-y-auto">
          <table class="race-table" id="full-results-table">
            <thead class="sticky top-0 bg-surface-container-low">
              <tr><th>POS</th><th>CODE</th><th>DRIVER</th><th>TEAM</th><th>TIME</th><th>GAP</th></tr>
            </thead>
            <tbody id="full-results-tbody"></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Tab Content: Compare View -->
    <div id="compare-view" class="hidden">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div class="bg-surface-container-low rounded-xl p-6">
          <div class="flex items-center gap-3 mb-4">
            <select id="compare-d1" class="bg-surface-container-highest rounded-lg px-4 py-2 font-bold text-lg border-none focus:ring-2 focus:ring-primary">
              <option>VER</option><option selected>HAM</option><option>LEC</option><option>NOR</option><option>SAI</option><option>RUS</option><option>PER</option><option>ALO</option>
            </select>
            <span class="text-on-surface-variant">vs</span>
            <select id="compare-d2" class="bg-surface-container-highest rounded-lg px-4 py-2 font-bold text-lg border-none focus:ring-2 focus:ring-primary">
              <option selected>VER</option><option>HAM</option><option>LEC</option><option>NOR</option><option>SAI</option><option>RUS</option><option>PER</option><option>ALO</option>
            </select>
          </div>
          <button id="compare-btn" class="w-full bg-primary text-on-primary rounded-xl py-3 font-semibold hover:bg-primary/90 transition-all">Analyze Head-to-Head</button>
        </div>
        <div class="bg-gradient-to-br from-primary/10 to-primary/5 rounded-xl p-6" id="compare-result">
          <p class="text-on-surface-variant text-center py-8">Select two drivers and click analyze</p>
        </div>
      </div>
      <div id="compare-detail" class="grid grid-cols-1 md:grid-cols-2 gap-6 hidden">
        <div id="driver1-card" class="bg-surface-container-low rounded-xl p-6"></div>
        <div id="driver2-card" class="bg-surface-container-low rounded-xl p-6"></div>
      </div>
    </div>

    <!-- Tab Content: Visuals View -->
    <div id="visuals-view" class="hidden">
      <div class="bg-surface-container-low rounded-xl p-6 mb-6">
        <div class="flex gap-4 items-end">
          <div class="flex-1">
            <label class="font-label text-xs uppercase tracking-widest text-secondary block mb-1">Season</label>
            <select id="vis-year" class="w-full bg-surface-container-highest rounded-lg px-4 py-2 border-none">
              <option>2024</option><option selected>2023</option><option>2022</option><option>2021</option>
            </select>
          </div>
          <div class="flex-1">
            <label class="font-label text-xs uppercase tracking-widest text-secondary block mb-1">Grand Prix</label>
            <select id="vis-track" class="w-full bg-surface-container-highest rounded-lg px-4 py-2 border-none">
              <option>Bahrain</option><option selected>Monaco</option><option>Silverstone</option><option>Spa</option><option>Monza</option>
            </select>
          </div>
          <button id="generate-visuals-btn" class="px-6 py-2 bg-primary text-on-primary rounded-xl font-semibold hover:bg-primary/90">Generate Visuals</button>
        </div>
      </div>
      <div id="visuals-output" class="bg-surface-container-low rounded-xl p-6">
        <p class="text-on-surface-variant text-center py-8">Click Generate Visuals to create professional race analysis charts</p>
      </div>
    </div>

    <!-- Terminal Output (Console-like) -->
    <div class="mt-8 bg-surface-container rounded-xl p-4 border border-outline-variant/30">
      <div class="flex items-center gap-2 mb-3">
        <span class="material-symbols-outlined text-primary text-sm">terminal</span>
        <span class="font-label text-xs uppercase tracking-widest text-secondary">Console Output</span>
      </div>
      <div id="terminal-output" class="terminal-output font-mono text-xs text-on-surface-variant h-32 overflow-y-auto">
        <span class="text-secondary">> F1 Race Relay v3.0 · Executive Dashboard</span><br/>
        <span class="text-secondary">> Ready. Select a race and click "Load Race Data" in controls.</span>
      </div>
    </div>
  </div>
</main>

<!-- Control Bar (Floating) -->
<div class="fixed bottom-8 right-8 flex gap-3 z-50">
  <button id="load-race-btn" class="w-14 h-14 bg-primary text-on-primary rounded-full shadow-lg flex items-center justify-center hover:scale-105 transition-all group relative">
    <span class="material-symbols-outlined">play_arrow</span>
    <span class="absolute bottom-full mb-2 right-0 bg-surface-container-highest text-on-surface text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">Load Race</span>
  </button>
  <button id="compare-race-btn" class="w-14 h-14 bg-surface-container-high text-primary rounded-full shadow-lg flex items-center justify-center hover:scale-105 transition-all group relative">
    <span class="material-symbols-outlined">compare_arrows</span>
    <span class="absolute bottom-full mb-2 right-0 bg-surface-container-highest text-on-surface text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">Compare</span>
  </button>
  <button id="visuals-race-btn" class="w-14 h-14 bg-surface-container-high text-primary rounded-full shadow-lg flex items-center justify-center hover:scale-105 transition-all group relative">
    <span class="material-symbols-outlined">insights</span>
    <span class="absolute bottom-full mb-2 right-0 bg-surface-container-highest text-on-surface text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">Visuals</span>
  </button>
</div>

<script>
const API = "http://localhost:5000";
let currentRaceData = null;
let activeTab = "dashboard";

// DOM Elements
const apiDot = document.getElementById('api-status-dot');
const apiText = document.getElementById('api-status-text');

// Tab switching
document.querySelectorAll('[data-tab]').forEach(el => {
  el.addEventListener('click', () => {
    const tab = el.getAttribute('data-tab');
    activeTab = tab;
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('results-view').classList.add('hidden');
    document.getElementById('compare-view').classList.add('hidden');
    document.getElementById('visuals-view').classList.add('hidden');
    document.getElementById(`${tab}-view`).classList.remove('hidden');
    
    // Update active styling
    document.querySelectorAll('[data-tab]').forEach(e => {
      e.classList.remove('bg-white', 'text-primary', 'shadow-sm');
      e.classList.add('text-on-surface-variant');
    });
    el.classList.add('bg-white', 'text-primary', 'shadow-sm');
    el.classList.remove('text-on-surface-variant');
  });
});

// API Functions
async function pingAPI() {
  apiDot.className = "w-2 h-2 rounded-full bg-secondary animate-pulse";
  apiText.textContent = "CONNECTING";
  try {
    const res = await fetch(`${API}/health`, {signal: AbortSignal.timeout(4000)});
    const data = await res.json();
    apiDot.className = "w-2 h-2 rounded-full bg-success";
    apiText.textContent = "ONLINE";
    addToTerminal("✓ API connected successfully", "success");
  } catch(e) {
    apiDot.className = "w-2 h-2 rounded-full bg-error";
    apiText.textContent = "OFFLINE";
    addToTerminal("✗ Cannot reach API. Run: python api.py", "error");
  }
}

function addToTerminal(msg, type = "info") {
  const term = document.getElementById('terminal-output');
  const colors = { success: "text-success", error: "text-error", info: "text-secondary", warning: "text-warning" };
  const span = document.createElement('div');
  span.className = colors[type] || "text-secondary";
  span.innerHTML = `> ${msg}`;
  term.appendChild(span);
  term.scrollTop = term.scrollHeight;
  while(term.children.length > 50) term.removeChild(term.firstChild);
}

async function loadRaceData() {
  const year = document.getElementById('nav-year').value;
  const track = document.getElementById('nav-track').value;
  
  addToTerminal(`Loading ${year} ${track} Grand Prix...`, "info");
  apiDot.className = "w-2 h-2 rounded-full bg-secondary animate-pulse";
  
  try {
    const res = await fetch(`${API}/race?year=${year}&track=${encodeURIComponent(track)}`);
    const data = await res.json();
    
    if (!data.ok) throw new Error(data.error);
    
    currentRaceData = data;
    
    // Update Dashboard KPIs
    document.getElementById('kpi-winner').textContent = data.winnerCode || data.winner || "—";
    document.getElementById('kpi-winner-team').textContent = data.winnerTeam || "—";
    document.getElementById('kpi-fastest-time').textContent = data.fastestLap?.time || "—";
    document.getElementById('kpi-fastest-driver').textContent = data.fastestLap?.driver || "—";
    document.getElementById('kpi-fastest-lap').textContent = data.fastestLap?.lap || "—";
    document.getElementById('kpi-track').textContent = data.eventName || data.track;
    document.getElementById('kpi-laps').textContent = data.totalLaps || "—";
    document.getElementById('kpi-finishers').textContent = `${data.finishers || "—"} finishers`;
    document.getElementById('kpi-date').textContent = data.eventDate || "—";
    document.getElementById('dashboard-title').textContent = `${data.year} ${data.eventName || data.track} Grand Prix`;
    document.getElementById('dashboard-subtitle').textContent = `Winner: ${data.winner} (${data.winnerTeam}) · Fastest Lap: ${data.fastestLap?.time}`;
    document.getElementById('results-event-name').textContent = `${data.year} ${data.eventName}`;
    
    // Update preview table
    const previewBody = document.getElementById('preview-tbody');
    previewBody.innerHTML = '';
    (data.results || []).slice(0, 5).forEach(r => {
      const row = previewBody.insertRow();
      const posClass = r.pos === 1 ? 'pos-1' : r.pos === 2 ? 'pos-2' : r.pos === 3 ? 'pos-3' : '';
      row.innerHTML = `
        <td class="${posClass}">${r.pos}</td>
        <td class="font-semibold">${escapeHtml(r.code)}</td>
        <td>${escapeHtml(r.driver)}</td>
        <td class="text-on-surface-variant">${escapeHtml(r.team)}</td>
        <td class="font-mono">${escapeHtml(r.time)}</td>
        <td class="text-on-surface-variant">${escapeHtml(r.gap)}</td>
      `;
    });
    
    // Update full results table
    const fullBody = document.getElementById('full-results-tbody');
    fullBody.innerHTML = '';
    (data.results || []).forEach(r => {
      const row = fullBody.insertRow();
      const posClass = r.pos === 1 ? 'pos-1' : r.pos === 2 ? 'pos-2' : r.pos === 3 ? 'pos-3' : '';
      row.innerHTML = `
        <td class="${posClass} font-bold">${r.pos}</td>
        <td class="font-mono font-bold">${escapeHtml(r.code)}</td>
        <td>${escapeHtml(r.driver)}</td>
        <td class="text-on-surface-variant">${escapeHtml(r.team)}</td>
        <td class="font-mono">${escapeHtml(r.time)}</td>
        <td class="text-on-surface-variant">${escapeHtml(r.gap)}</td>
      `;
    });
    
    addToTerminal(`✓ Loaded: ${data.finishers} drivers classified · Fastest lap: ${data.fastestLap?.driver} (${data.fastestLap?.time})`, "success");
    apiDot.className = "w-2 h-2 rounded-full bg-success";
    
  } catch(e) {
    addToTerminal(`✗ Error: ${e.message}`, "error");
    apiDot.className = "w-2 h-2 rounded-full bg-error";
  }
}

async function compareDrivers() {
  const year = document.getElementById('nav-year').value;
  const track = document.getElementById('nav-track').value;
  const d1 = document.getElementById('compare-d1').value;
  const d2 = document.getElementById('compare-d2').value;
  
  if (d1 === d2) {
    addToTerminal("Please select two different drivers", "warning");
    return;
  }
  
  addToTerminal(`Comparing ${d1} vs ${d2} at ${year} ${track}...`, "info");
  
  try {
    const res = await fetch(`${API}/compare?year=${year}&track=${encodeURIComponent(track)}&d1=${d1}&d2=${d2}`);
    const data = await res.json();
    
    if (!data.ok) throw new Error(data.error);
    
    const resultDiv = document.getElementById('compare-result');
    resultDiv.innerHTML = `
      <div class="text-center">
        <span class="text-3xl font-bold ${data.faster === d1 ? 'text-primary' : 'text-secondary'}">${data.faster}</span>
        <span class="text-xl mx-2">is faster by</span>
        <span class="text-3xl font-bold text-primary">${data.delta}s</span>
        <p class="text-on-surface-variant mt-2">on fastest lap</p>
      </div>
    `;
    
    const detailDiv = document.getElementById('compare-detail');
    detailDiv.classList.remove('hidden');
    
    const s1 = data.d1, s2 = data.d2;
    
    document.getElementById('driver1-card').innerHTML = `
      <div class="flex items-center gap-3 mb-4 border-b border-outline-variant pb-3">
        <span class="text-4xl font-bold text-primary">${d1}</span>
        <span class="text-on-surface-variant text-sm">${s1.team}</span>
      </div>
      <div class="space-y-3">
        <div class="flex justify-between"><span class="text-on-surface-variant">Position</span><span class="font-bold">P${s1.position}</span></div>
        <div class="flex justify-between"><span class="text-on-surface-variant">Fastest Lap</span><span class="font-mono">${s1.fastest} (Lap ${s1.fastLap})</span></div>
        <div class="flex justify-between"><span class="text-on-surface-variant">Average Lap</span><span class="font-mono">${s1.avgLap}</span></div>
        <div class="flex justify-between"><span class="text-on-surface-variant">Total Laps</span><span>${s1.totalLaps}</span></div>
      </div>
    `;
    
    document.getElementById('driver2-card').innerHTML = `
      <div class="flex items-center gap-3 mb-4 border-b border-outline-variant pb-3">
        <span class="text-4xl font-bold text-secondary">${d2}</span>
        <span class="text-on-surface-variant text-sm">${s2.team}</span>
      </div>
      <div class="space-y-3">
        <div class="flex justify-between"><span class="text-on-surface-variant">Position</span><span class="font-bold">P${s2.position}</span></div>
        <div class="flex justify-between"><span class="text-on-surface-variant">Fastest Lap</span><span class="font-mono">${s2.fastest} (Lap ${s2.fastLap})</span></div>
        <div class="flex justify-between"><span class="text-on-surface-variant">Average Lap</span><span class="font-mono">${s2.avgLap}</span></div>
        <div class="flex justify-between"><span class="text-on-surface-variant">Total Laps</span><span>${s2.totalLaps}</span></div>
      </div>
    `;
    
    addToTerminal(`✓ Comparison complete: ${data.faster} faster by ${data.delta}s`, "success");
    
  } catch(e) {
    addToTerminal(`✗ Compare error: ${e.message}`, "error");
  }
}

async function generateVisuals() {
  const year = document.getElementById('vis-year').value;
  const track = document.getElementById('vis-track').value;
  
  addToTerminal(`Generating visuals for ${year} ${track}... This may take 20-60 seconds`, "info");
  document.getElementById('visuals-output').innerHTML = '<p class="text-center py-8 text-primary animate-pulse">Generating visualizations...</p>';
  
  try {
    const res = await fetch(`${API}/visuals?year=${year}&track=${encodeURIComponent(track)}`);
    const data = await res.json();
    
    if (!data.ok) throw new Error(data.error);
    
    const files = data.files || [];
    let html = '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">';
    files.forEach(f => {
      const name = f.split('/').pop();
      html += `
        <div class="bg-surface-container-highest rounded-lg p-4 flex justify-between items-center">
          <div>
            <span class="material-symbols-outlined text-primary">insert_chart</span>
            <span class="ml-2 text-sm font-mono">${escapeHtml(name)}</span>
          </div>
          <button onclick="window.open('${escapeHtml(f)}', '_blank')" class="text-primary text-sm hover:underline">Open</button>
        </div>
      `;
    });
    html += '</div>';
    document.getElementById('visuals-output').innerHTML = html;
    addToTerminal(`✓ Generated ${files.length} visualizations`, "success");
    
  } catch(e) {
    document.getElementById('visuals-output').innerHTML = `<p class="text-center py-8 text-error">Error: ${escapeHtml(e.message)}</p>`;
    addToTerminal(`✗ Visual generation failed: ${e.message}`, "error");
  }
}

function escapeHtml(str) {
  if (!str) return "—";
  return String(str).replace(/[&<>]/g, function(m) {
    if (m === '&') return '&amp;';
    if (m === '<') return '&lt;';
    if (m === '>') return '&gt;';
    return m;
  });
}

// Event Listeners
document.getElementById('load-race-btn').addEventListener('click', loadRaceData);
document.getElementById('compare-race-btn').addEventListener('click', () => {
  document.querySelector('[data-tab="compare"]').click();
});
document.getElementById('visuals-race-btn').addEventListener('click', () => {
  document.querySelector('[data-tab="visuals"]').click();
});
document.getElementById('compare-btn').addEventListener('click', compareDrivers);
document.getElementById('generate-visuals-btn').addEventListener('click', generateVisuals);
document.getElementById('view-full-results').addEventListener('click', () => {
  document.querySelector('[data-tab="results"]').click();
});
document.getElementById('export-data-btn').addEventListener('click', () => {
  if (currentRaceData) {
    const dataStr = JSON.stringify(currentRaceData, null, 2);
    const blob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `f1_race_${currentRaceData.year}_${currentRaceData.track}.json`;
    a.click();
    URL.revokeObjectURL(url);
    addToTerminal("✓ Race data exported", "success");
  } else {
    addToTerminal("No race data loaded to export", "warning");
  }
});
document.getElementById('live-telemetry-btn').addEventListener('click', () => {
  addToTerminal("Telemetry stream requires FastF1 session with telemetry=True", "info");
});

// Initial ping
pingAPI();

// Update nav selectors to trigger load on change
document.getElementById('nav-year').addEventListener('change', () => {
  if (currentRaceData) loadRaceData();
});
document.getElementById('nav-track').addEventListener('change', () => {
  if (currentRaceData) loadRaceData();
});

addToTerminal("F1 Race Relay Executive Dashboard ready. Click the play button to load race data.", "success");
</script>
</body>
</html>
