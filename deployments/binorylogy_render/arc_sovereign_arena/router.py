"""
ARC Sovereign API Router & Live Visual Dashboard
Serves real-time JSON telemetry and the standalone /arc interactive HTML UI.
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from arc_sovereign_arena.coordinator import SovereignArcCoordinator

arc_router = APIRouter(prefix="/api/arc", tags=["ARC-Sovereign-Arena"])

@arc_router.get("/status")
def get_arc_status():
    coordinator = SovereignArcCoordinator()
    return coordinator.get_telemetry()

@arc_router.get("/live")
def get_arc_live():
    coordinator = SovereignArcCoordinator()
    return coordinator.get_live_visual_state()

@arc_router.get("/laws")
def get_arc_laws():
    coordinator = SovereignArcCoordinator()
    return {
        "count": len(coordinator.discoveries),
        "laws": coordinator.discoveries
    }

@arc_router.post("/start")
def start_arc_loop():
    coordinator = SovereignArcCoordinator()
    coordinator.start_background_loop()
    return {"status": "started", "message": "ARC Sovereign Discovery Arena running"}


def generate_arc_html_dashboard() -> str:
    """Generates the full-screen standalone HTML/JS dashboard for /arc."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ARC-AGI Sovereign Arena | Autonomous 4-Pillar Discovery</title>
<style>
  :root {
    --bg-dark: #070b14;
    --card-bg: #0f172a;
    --border: #1e293b;
    --cyan: #00f0ff;
    --green: #10b981;
    --purple: #a855f7;
    --amber: #f59e0b;
    --red: #ef4444;
    --text: #f1f5f9;
    --text-dim: #94a3b8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg-dark);
    color: var(--text);
    font-family: 'JetBrains Mono', 'Segoe UI', monospace;
    padding: 16px;
    font-size: 13px;
  }
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 10px;
  }
  .title-group { display: flex; align-items: center; gap: 12px; }
  h1 { font-size: 18px; color: var(--cyan); letter-spacing: 1px; font-weight: bold; }
  .badge {
    padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; text-transform: uppercase;
  }
  .badge-live { background: rgba(16, 185, 129, 0.2); color: var(--green); border: 1px solid var(--green); animation: pulse 2s infinite; }
  .badge-pass { background: rgba(168, 85, 247, 0.2); color: var(--purple); border: 1px solid var(--purple); }
  .badge-time { background: rgba(0, 240, 255, 0.2); color: var(--cyan); border: 1px solid var(--cyan); }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

  .grid-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    margin-bottom: 16px;
  }
  .stat-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
  }
  .stat-label { font-size: 11px; color: var(--text-dim); text-transform: uppercase; margin-bottom: 4px; }
  .stat-val { font-size: 20px; font-weight: bold; color: var(--cyan); }
  .progress-bar-bg { background: #1e293b; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden; }
  .progress-bar-fill { background: linear-gradient(90deg, var(--cyan), var(--green)); height: 100%; width: 0%; transition: width 0.3s; }

  .main-arena {
    display: grid;
    grid-template-columns: 1fr 1.2fr 1fr;
    gap: 16px;
    margin-bottom: 16px;
  }
  @media (max-width: 1024px) {
    .main-arena { grid-template-columns: 1fr; }
  }
  .panel {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    display: flex;
    flex-direction: column;
  }
  .panel-title { font-size: 12px; color: var(--cyan); font-weight: bold; text-transform: uppercase; margin-bottom: 10px; display: flex; justify-content: space-between; }

  /* 2D Canvas Grid Renderer */
  .grid-canvas-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 220px;
    background: #090e1a;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px;
    margin-bottom: 8px;
  }
  .arc-grid {
    display: grid;
    gap: 1px;
    background: #2d3748;
    border: 2px solid #334155;
    padding: 2px;
  }
  .arc-cell {
    width: 18px;
    height: 18px;
    border-radius: 2px;
  }

  /* Pillar Feed */
  .hyp-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    overflow-y: auto;
    max-height: 250px;
  }
  .hyp-item {
    background: #131d33;
    border-left: 3px solid var(--cyan);
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 11px;
    color: #cbd5e1;
  }
  .hyp-item.Classical { border-left-color: var(--cyan); }
  .hyp-item.Quantum { border-left-color: var(--purple); }
  .hyp-item.Modern { border-left-color: var(--amber); }
  .hyp-item.String { border-left-color: var(--green); }

  /* Leaderboard & Laws */
  .bottom-grid {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 16px;
  }
  @media (max-width: 900px) { .bottom-grid { grid-template-columns: 1fr; } }
  .leaderboard-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 12px;
    background: #131d33;
    border-radius: 6px;
    margin-bottom: 6px;
  }
  .law-feed {
    max-height: 220px;
    overflow-y: auto;
  }
  .law-row {
    padding: 6px 10px;
    background: #131d33;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    font-size: 11px;
  }
  .law-row:last-child { border-bottom: none; }
</style>
</head>
<body>

<header>
  <div class="title-group">
    <h1>🌌 ARC-AGI SOVEREIGN DISCOVERY ARENA</h1>
    <span class="badge badge-live">● LIVE 24/7</span>
    <span class="badge badge-pass" id="pass-badge">PASS #1</span>
    <span class="badge badge-time" id="time-badge">00:00:00</span>
    <a href="https://huggingface.co/datasets/Explorerp/binorylogy-physics-memory" target="_blank" style="text-decoration: none;">
      <span class="badge badge-pass" id="vault-badge" style="background: rgba(245, 158, 11, 0.2); color: var(--amber); border: 1px solid var(--amber); cursor: pointer;">🤗 HF VAULT: CONNECTED</span>
    </a>
  </div>
  <div style="color: var(--text-dim); font-size: 11px;">
    Host: <code>god-1d2m.onrender.com</code> | Model: <strong>SovereignCivilization (4 Living Pillars)</strong> | Vault: <a href="https://huggingface.co/datasets/Explorerp/binorylogy-physics-memory" target="_blank" style="color: var(--amber); text-decoration: none;"><strong>Explorerp/binorylogy-physics-memory</strong></a>
  </div>
</header>

<div class="grid-stats">
  <div class="stat-card">
    <div class="stat-label">Total Verified Laws</div>
    <div class="stat-val" id="total-laws" style="color: var(--green);">0</div>
    <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">100% Ground Truth Verified</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">ARC-AGI-1 (Training 400)</div>
    <div class="stat-val" id="agi1-stat">0 / 400 (0.0%)</div>
    <div class="progress-bar-bg"><div class="progress-bar-fill" id="agi1-bar"></div></div>
  </div>
  <div class="stat-card">
    <div class="stat-label">ARC-AGI-2 (Evaluation 400)</div>
    <div class="stat-val" id="agi2-stat">0 / 400 (0.0%)</div>
    <div class="progress-bar-bg"><div class="progress-bar-fill" id="agi2-bar"></div></div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Current Task</div>
    <div class="stat-val" id="current-task-name" style="color: var(--amber);">idle</div>
    <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;" id="current-track-name">Track: -</div>
  </div>
</div>

<div class="main-arena">
  <!-- 1. Input Grid -->
  <div class="panel">
    <div class="panel-title">
      <span>1. Sensory Input Grid</span>
      <span id="input-dims">-</span>
    </div>
    <div class="grid-canvas-container">
      <div id="input-grid-box" class="arc-grid"></div>
    </div>
    <div style="font-size: 11px; color: var(--text-dim); text-align: center;">Raw input matrix fed into 4 Pillars</div>
  </div>

  <!-- 2. 4 Pillars Active Reasoning Stream -->
  <div class="panel">
    <div class="panel-title">
      <span>2. 4 Pillars Deliberation & Hypotheses</span>
      <span style="color: var(--green);" id="task-status-text">Thinking...</span>
    </div>
    <div class="hyp-list" id="hyp-stream">
      <div class="hyp-item">Pillars initializing search tree...</div>
    </div>
    <div style="margin-top: auto; padding-top: 10px; border-top: 1px solid var(--border); font-size: 11px; color: var(--cyan);">
      Winning Law: <strong id="winning-law-text" style="color: var(--green);">-</strong>
    </div>
  </div>

  <!-- 3. Output Comparison (Prediction vs Target) -->
  <div class="panel">
    <div class="panel-title">
      <span>3. Prediction vs ARC Ground Truth</span>
      <span id="output-dims">-</span>
    </div>
    <div class="grid-canvas-container">
      <div id="output-grid-box" class="arc-grid"></div>
    </div>
    <div style="font-size: 11px; color: var(--text-dim); text-align: center;" id="match-verdict">Evaluating...</div>
  </div>
</div>

<div class="bottom-grid">
  <!-- Pillar Leaderboard -->
  <div class="panel">
    <div class="panel-title">4 Sovereign Pillars Leaderboard</div>
    <div id="pillar-board">
      <div class="leaderboard-row"><span>Classical-Eikonal</span><strong style="color: var(--cyan);" id="score-classical">0</strong></div>
      <div class="leaderboard-row"><span>Quantum-Superposed</span><strong style="color: var(--purple);" id="score-quantum">0</strong></div>
      <div class="leaderboard-row"><span>Modern-Thermodynamic</span><strong style="color: var(--amber);" id="score-modern">0</strong></div>
      <div class="leaderboard-row"><span>String-10D-Topological</span><strong style="color: var(--green);" id="score-string">0</strong></div>
    </div>
  </div>

  <!-- Live Discovered Laws Log -->
  <div class="panel">
    <div class="panel-title">Live Discovered Laws Feed</div>
    <div class="law-feed" id="laws-container">
      <div class="law-row"><span>Waiting for first law...</span></div>
    </div>
  </div>
</div>

<script>
const ARC_PALETTE = [
  '#111111', // 0: Black
  '#1E88E5', // 1: Blue
  '#E53935', // 2: Red
  '#43A047', // 3: Green
  '#FDD835', // 4: Yellow
  '#757575', // 5: Grey
  '#D81B60', // 6: Magenta
  '#FB8C00', // 7: Orange
  '#00ACC1', // 8: Cyan
  '#5D4037'  // 9: Maroon
];

function renderGrid(containerId, matrix) {
  const container = document.getElementById(containerId);
  if (!container || !matrix || !matrix.length) {
    container.innerHTML = '<div style="color: #64748b; font-size: 11px;">No Data</div>';
    return;
  }
  const rows = matrix.length;
  const cols = matrix[0].length;
  container.style.gridTemplateColumns = `repeat(${cols}, 18px)`;
  container.innerHTML = '';
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const val = matrix[r][c];
      const cell = document.createElement('div');
      cell.className = 'arc-cell';
      cell.style.backgroundColor = ARC_PALETTE[val] || '#000';
      cell.title = `(${r}, ${c}): Color ${val}`;
      container.appendChild(cell);
    }
  }
}

async function fetchLiveTelemetry() {
  try {
    const res = await fetch('/api/arc/live');
    if (!res.ok) return;
    const d = await res.json();

    // Badges & Timer
    document.getElementById('pass-badge').innerText = `PASS #${d.current_pass || 1}`;
    document.getElementById('time-badge').innerText = d.elapsed_time_formatted || '00:00:00';
    document.getElementById('total-laws').innerText = d.total_laws_discovered || 0;

    // Cloud Vault Badge
    if (d.cloud_vault) {
      const vb = document.getElementById('vault-badge');
      if (vb) {
        if (d.cloud_vault.connected) {
          vb.innerText = `🤗 HF VAULT: SYNCED (${d.cloud_vault.last_cloud_sync || 'ACTIVE'})`;
        } else {
          vb.innerText = '🤗 HF VAULT: LOCAL CACHE';
        }
      }
    }

    // Progress
    if (d.agi1_progress) {
      const p1 = d.agi1_progress;
      document.getElementById('agi1-stat').innerText = `${p1.mastered} / ${p1.total_tasks} (${(p1.mastery_rate*100).toFixed(1)}%)`;
      document.getElementById('agi1-bar').style.width = `${(p1.tested / p1.total_tasks)*100}%`;
    }
    if (d.agi2_progress) {
      const p2 = d.agi2_progress;
      document.getElementById('agi2-stat').innerText = `${p2.mastered} / ${p2.total_tasks} (${(p2.mastery_rate*100).toFixed(1)}%)`;
      document.getElementById('agi2-bar').style.width = `${(p2.tested / p2.total_tasks)*100}%`;
    }

    // Current Task
    document.getElementById('current-task-name').innerText = d.task_id || d.current_task || 'idle';
    document.getElementById('current-track-name').innerText = `Track: ${d.track || d.current_track || '-'}`;

    // Render Grids
    if (d.input_grid && d.input_grid.length) {
      document.getElementById('input-dims').innerText = `${d.input_grid.length}x${d.input_grid[0].length}`;
      renderGrid('input-grid-box', d.input_grid);
    }
    if (d.output_grid && d.output_grid.length) {
      document.getElementById('output-dims').innerText = `${d.output_grid.length}x${d.output_grid[0].length}`;
      renderGrid('output-grid-box', d.output_grid);
    }

    // Hypotheses
    const hypBox = document.getElementById('hyp-stream');
    if (d.active_hyps && d.active_hyps.length) {
      hypBox.innerHTML = d.active_hyps.map(h => {
        let cls = 'Classical';
        if (h.includes('quantum')) cls = 'Quantum';
        if (h.includes('modern') || h.includes('diffusion')) cls = 'Modern';
        if (h.includes('string') || h.includes('topological')) cls = 'String';
        return `<div class="hyp-item ${cls}">${h}</div>`;
      }).join('');
    }

    // Verdict
    if (d.solved) {
      document.getElementById('task-status-text').innerText = `SOLVED by ${d.pillar}`;
      document.getElementById('task-status-text').style.color = '#10b981';
      document.getElementById('winning-law-text').innerText = d.law || '-';
      document.getElementById('match-verdict').innerText = '100% Exact Match on Ground Truth';
      document.getElementById('match-verdict').style.color = '#10b981';
    } else {
      document.getElementById('task-status-text').innerText = 'Searching...';
      document.getElementById('task-status-text').style.color = '#00f0ff';
      document.getElementById('winning-law-text').innerText = 'Exploring compound hypotheses';
      document.getElementById('match-verdict').innerText = 'No exact primitive match (Moving to next)';
      document.getElementById('match-verdict').style.color = '#94a3b8';
    }

    // Leaderboard
    if (d.pillar_leaderboard) {
      document.getElementById('score-classical').innerText = d.pillar_leaderboard['Classical-Eikonal'] || 0;
      document.getElementById('score-quantum').innerText = d.pillar_leaderboard['Quantum-Superposed'] || 0;
      document.getElementById('score-modern').innerText = d.pillar_leaderboard['Modern-Thermodynamic'] || 0;
      document.getElementById('score-string').innerText = d.pillar_leaderboard['String-10D-Topological'] || 0;
    }

    // Recent Laws
    if (d.recent_discoveries && d.recent_discoveries.length) {
      const lawsBox = document.getElementById('laws-container');
      lawsBox.innerHTML = d.recent_discoveries.slice().reverse().map(l => `
        <div class="law-row">
          <span><strong>${l.pillar}</strong>: Task <code>${l.task_id}</code> &mdash; ${l.law}</span>
          <span style="color: #64748b;">${l.time_sec}s | ${l.timestamp}</span>
        </div>
      `).join('');
    }
  } catch (e) {
    console.error('ARC Telemetry fetch error:', e);
  }
}

setInterval(fetchLiveTelemetry, 1000);
fetchLiveTelemetry();
</script>

</body>
</html>
"""

@arc_router.get("/ui", response_class=HTMLResponse)
def get_arc_ui():
    """Serves the standalone interactive visual UI."""
    return HTMLResponse(content=generate_arc_html_dashboard())
