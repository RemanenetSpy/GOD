"""
ARC Sovereign API Router & Live Visual Dashboard (Survival Ecology Edition)
Serves real-time JSON telemetry and the /arc interactive HTML UI showing the
living organism walking, eating, starving, and surviving in ARC environments.
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
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

@arc_router.post("/start")
def start_arc_loop():
    coordinator = SovereignArcCoordinator()
    coordinator.start_background_loop()
    return {"status": "started", "message": "ARC Autopoietic Survival Ecology active 24/7"}

@arc_router.post("/stop")
def stop_arc_loop():
    coordinator = SovereignArcCoordinator()
    coordinator.stop_background_loop()
    return {"status": "stopped", "message": "ARC Survival loop paused"}


def generate_arc_html_dashboard() -> str:
    """Generates the full-screen standalone HTML/JS dashboard for /arc."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ARC-AGI Sovereign Survival Ecology | Embodied Autopoiesis</title>
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
  .badge-gen { background: rgba(168, 85, 247, 0.2); color: var(--purple); border: 1px solid var(--purple); }
  .badge-time { background: rgba(0, 240, 255, 0.2); color: var(--cyan); border: 1px solid var(--cyan); }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

  .grid-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
  .progress-bar-bg { background: #1e293b; height: 8px; border-radius: 4px; margin-top: 8px; overflow: hidden; }
  .progress-bar-fill { background: linear-gradient(90deg, var(--green), var(--cyan)); height: 100%; width: 100%; transition: width 0.2s, background 0.3s; }

  .main-arena {
    display: grid;
    grid-template-columns: 1fr 1.3fr 1fr;
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
  .panel-title { font-size: 12px; color: var(--cyan); font-weight: bold; text-transform: uppercase; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }

  /* 2D Canvas Grid Renderer */
  .grid-canvas-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 250px;
    background: #090e1a;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px;
    margin-bottom: 8px;
    position: relative;
  }
  .arc-grid {
    display: grid;
    gap: 1px;
    background: #2d3748;
    border: 2px solid #334155;
    padding: 2px;
    position: relative;
  }
  .arc-cell {
    width: 20px;
    height: 20px;
    border-radius: 2px;
    position: relative;
  }

  /* Organism Cursor Avatar */
  .organism-cursor {
    position: absolute;
    inset: 0;
    border: 2px solid #ffffff;
    box-shadow: 0 0 10px #00f0ff, inset 0 0 6px #00f0ff;
    border-radius: 3px;
    animation: cursor-pulse 0.8s infinite alternate;
    pointer-events: none;
    z-index: 10;
  }
  @keyframes cursor-pulse {
    0% { transform: scale(0.95); opacity: 0.8; }
    100% { transform: scale(1.15); opacity: 1.0; }
  }

  /* Event Feed */
  .event-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    overflow-y: auto;
    max-height: 250px;
  }
  .event-item {
    background: #131d33;
    border-left: 3px solid var(--cyan);
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 11px;
    color: #cbd5e1;
    display: flex;
    justify-content: space-between;
  }
  .event-item.nutrition { border-left-color: var(--green); background: rgba(16, 185, 129, 0.08); }
  .event-item.toxic { border-left-color: var(--amber); background: rgba(245, 158, 11, 0.08); }
  .event-item.death { border-left-color: var(--red); background: rgba(239, 68, 68, 0.12); color: #fca5a5; }
  .event-item.clear { border-left-color: #38bdf8; background: rgba(56, 189, 248, 0.15); font-weight: bold; }

  /* Bottom Controls & Info */
  .bottom-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  @media (max-width: 900px) { .bottom-grid { grid-template-columns: 1fr; } }
  .palette-swatch {
    display: inline-block;
    width: 14px;
    height: 14px;
    border-radius: 3px;
    vertical-align: middle;
    margin-right: 6px;
    border: 1px solid #475569;
  }
</style>
</head>
<body>

<header>
  <div class="title-group">
    <h1>🌱 ARC-AGI AUTOPOIETIC SURVIVAL ECOLOGY</h1>
    <span class="badge badge-live">● LIVING ORGANISM</span>
    <span class="badge badge-gen" id="gen-badge">GEN #1</span>
    <span class="badge badge-time" id="time-badge">00:00:00</span>
    <a href="https://huggingface.co/datasets/Explorerp/binorylogy-physics-memory" target="_blank" style="text-decoration: none;">
      <span class="badge badge-gen" id="vault-badge" style="background: rgba(245, 158, 11, 0.2); color: var(--amber); border: 1px solid var(--amber); cursor: pointer;">🤗 HF MEMORY VAULT</span>
    </a>
  </div>
  <div style="color: var(--text-dim); font-size: 11px;">
    Zero pre-coded physics rules. Correct pixels = <strong>Food</strong>. Wrong pixels = <strong>Waste</strong>. Starvation = <strong>Death</strong>.
  </div>
</header>

<div class="grid-stats">
  <div class="stat-card">
    <div class="stat-label">Organism Vitality (Hunger)</div>
    <div class="stat-val" id="organism-vitality" style="color: var(--green);">100.0%</div>
    <div class="progress-bar-bg"><div class="progress-bar-fill" id="vitality-bar"></div></div>
    <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;" id="vitality-status">Well Nourished</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Generations & Lineage</div>
    <div class="stat-val" id="stat-generation">Gen 1</div>
    <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;" id="stat-births-deaths">Births: 1 | Starvations: 0</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Metabolic Food Ingestion</div>
    <div class="stat-val" id="stat-food" style="color: var(--green);">0 px</div>
    <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;" id="stat-puzzles-cleared">0 Puzzles Cleared</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Active Environment Terrain</div>
    <div class="stat-val" id="current-task-name" style="color: var(--amber);">genesis</div>
    <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;" id="stat-organism-pos">Body Pos: (0, 0) | Tool: 1</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Ancestral Causal Memory</div>
    <div class="stat-val" id="stat-ancestral-food" style="color: var(--purple);">0 Food Px</div>
    <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;" id="stat-ancestral-veto">Vetoed Poisons: 0 | Deaths Learned: 0</div>
  </div>
</div>

<div class="main-arena">
  <!-- 1. Input Canvas -->
  <div class="panel">
    <div class="panel-title">
      <span>1. Environmental Input Canvas</span>
      <span id="input-dims">-</span>
    </div>
    <div class="grid-canvas-container">
      <div id="input-grid-box" class="arc-grid"></div>
    </div>
    <div style="font-size: 11px; color: var(--text-dim); text-align: center;">Starting landscape of the puzzle terrain</div>
  </div>

  <!-- 2. Working Canvas (Living Organism Body) -->
  <div class="panel" style="border: 1px solid var(--cyan);">
    <div class="panel-title">
      <span style="color: var(--cyan);">2. Living Canvas (Organism Body)</span>
      <span id="working-dims" style="color: var(--green);">Active</span>
    </div>
    <div class="grid-canvas-container">
      <div id="working-grid-box" class="arc-grid"></div>
    </div>
    <div style="font-size: 11px; color: var(--text-dim); text-align: center;">
      Organism cursor <span style="display:inline-block; width:8px; height:8px; border:2px solid #fff; box-shadow:0 0 4px #00f0ff;"></span> walks & paints pixels to eat
    </div>
  </div>

  <!-- 3. Target Ground Truth -->
  <div class="panel">
    <div class="panel-title">
      <span>3. Target Canvas (Hidden Food Map)</span>
      <span id="target-dims">-</span>
    </div>
    <div class="grid-canvas-container">
      <div id="target-grid-box" class="arc-grid"></div>
    </div>
    <div style="font-size: 11px; color: var(--text-dim); text-align: center;">Environmental ground truth required to feast</div>
  </div>
</div>

<div class="bottom-grid">
  <!-- Live Biological Events Feed -->
  <div class="panel">
    <div class="panel-title">Biological Event & Metabolism Feed</div>
    <div class="event-list" id="event-stream">
      <div class="event-item">Organism initialized on the grid...</div>
    </div>
  </div>

  <!-- Connectome & Physical Memory -->
  <div class="panel">
    <div class="panel-title">Sensory-Motor Connectome & Memory</div>
    <div style="display: flex; flex-direction: column; gap: 8px;">
      <div style="background: #131d33; padding: 10px; border-radius: 6px;">
        <div style="font-size: 11px; color: var(--text-dim);">Selected Color Tool:</div>
        <div style="font-size: 14px; font-weight: bold; margin-top: 4px;" id="selected-color-info">
          <span class="palette-swatch" id="color-swatch" style="background: #1E88E5;"></span> Color 1
        </div>
      </div>
      <div style="background: #131d33; padding: 10px; border-radius: 6px;">
        <div style="font-size: 11px; color: var(--text-dim);">Fittest Ancestor Lifespan:</div>
        <div style="font-size: 14px; font-weight: bold; color: var(--cyan); margin-top: 4px;" id="best-lifespan-info">0 ticks</div>
      </div>
      <div style="background: #131d33; padding: 10px; border-radius: 6px;">
        <div style="font-size: 11px; color: var(--text-dim);">Lineage Memory Storage:</div>
        <div style="font-size: 12px; color: var(--amber); margin-top: 4px;" id="storage-info">HF Vault: Explorerp/binorylogy-physics-memory</div>
      </div>
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

function renderGrid(containerId, matrix, organismPos = null) {
  const container = document.getElementById(containerId);
  if (!container || !matrix || !matrix.length) {
    container.innerHTML = '<div style="color: #64748b; font-size: 11px;">No Data</div>';
    return;
  }
  const rows = matrix.length;
  const cols = matrix[0].length;
  container.style.gridTemplateColumns = `repeat(${cols}, 20px)`;
  container.innerHTML = '';

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const val = matrix[r][c];
      const cell = document.createElement('div');
      cell.className = 'arc-cell';
      cell.style.backgroundColor = ARC_PALETTE[val] || '#000';
      cell.title = `(${r}, ${c}): Color ${val}`;

      if (organismPos && organismPos.r === r && organismPos.c === c) {
        const cursor = document.createElement('div');
        cursor.className = 'organism-cursor';
        cell.appendChild(cursor);
      }
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
    document.getElementById('gen-badge').innerText = `GEN #${d.generation || 1}`;
    document.getElementById('time-badge').innerText = d.elapsed_time_formatted || '00:00:00';

    // Organism Vitality / Hunger
    const org = d.organism || {};
    const vit = org.vitality !== undefined ? org.vitality : 100.0;
    const vitPct = org.vitality_pct !== undefined ? org.vitality_pct : vit;
    document.getElementById('organism-vitality').innerText = `${vit.toFixed(1)}%`;
    const vitBar = document.getElementById('vitality-bar');
    vitBar.style.width = `${Math.max(0, Math.min(100, vitPct))}%`;

    const vitStatus = document.getElementById('vitality-status');
    if (vit > 60) {
      vitBar.style.background = 'linear-gradient(90deg, #10b981, #00f0ff)';
      vitStatus.innerText = 'Well Nourished (Active)';
      vitStatus.style.color = '#10b981';
    } else if (vit > 25) {
      vitBar.style.background = 'linear-gradient(90deg, #f59e0b, #eab308)';
      vitStatus.innerText = 'Hunger Rising (Searching for Food)';
      vitStatus.style.color = '#f59e0b';
    } else {
      vitBar.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
      vitStatus.innerText = 'STARVATION IMMINENT!';
      vitStatus.style.color = '#ef4444';
    }

    // Stats
    document.getElementById('stat-generation').innerText = `Gen ${d.generation || 1}`;
    document.getElementById('stat-births-deaths').innerText = `Births: ${d.total_births || 1} | Deaths: ${d.total_deaths || 0}`;
    document.getElementById('stat-food').innerText = `${d.total_food_eaten || 0} px`;
    document.getElementById('stat-puzzles-cleared').innerText = `${d.puzzles_cleared || 0} Puzzles Cleared`;
    document.getElementById('current-task-name').innerText = d.task_id || d.current_task || 'genesis';
    document.getElementById('stat-organism-pos').innerText = `Body Pos: (${org.r || 0}, ${org.c || 0}) | Color: ${org.selected_color || 0}`;

    // Ancestral Causal Memory
    const mem = d.ancestral_memory || {};
    const nutCount = mem.total_nutrition_discovered !== undefined ? mem.total_nutrition_discovered : (mem.confirmed_nutrition ? Object.keys(mem.confirmed_nutrition).length : 0);
    const toxCount = mem.total_toxic_vetoed !== undefined ? mem.total_toxic_vetoed : (mem.toxic_ledger ? Object.keys(mem.toxic_ledger).length : 0);
    const deathCount = mem.total_deaths_recorded !== undefined ? mem.total_deaths_recorded : (mem.task_deaths ? Object.values(mem.task_deaths).reduce((a, b) => a + b, 0) : 0);
    document.getElementById('stat-ancestral-food').innerText = `${nutCount} Confirmed Food`;
    document.getElementById('stat-ancestral-veto').innerText = `Vetoed Poisons: ${toxCount} | Deaths Learned: ${deathCount}`;

    // Connectome / Selected color info
    const toolCol = org.selected_color || 0;
    document.getElementById('selected-color-info').innerHTML = `
      <span class="palette-swatch" style="background: ${ARC_PALETTE[toolCol] || '#fff'};"></span> Color ${toolCol}
    `;
    document.getElementById('best-lifespan-info').innerText = `${d.best_lifespan || 0} ticks`;

    // Render Grids
    if (d.input_grid && d.input_grid.length) {
      document.getElementById('input-dims').innerText = `${d.input_grid.length}x${d.input_grid[0].length}`;
      renderGrid('input-grid-box', d.input_grid);
    }
    if (d.working_grid && d.working_grid.length) {
      document.getElementById('working-dims').innerText = `${d.working_grid.length}x${d.working_grid[0].length}`;
      renderGrid('working-grid-box', d.working_grid, { r: org.r, c: org.c });
    }
    if (d.target_grid && d.target_grid.length) {
      document.getElementById('target-dims').innerText = `${d.target_grid.length}x${d.target_grid[0].length}`;
      renderGrid('target-grid-box', d.target_grid);
    }

    // Events Feed
    const evBox = document.getElementById('event-stream');
    if (d.recent_events && d.recent_events.length) {
      evBox.innerHTML = d.recent_events.slice().reverse().map(e => {
        let cls = 'event-item';
        if (e.msg.includes('NUTRITION')) cls += ' nutrition';
        else if (e.msg.includes('TOXIC')) cls += ' toxic';
        else if (e.msg.includes('STARVATION')) cls += ' death';
        else if (e.msg.includes('CLEARED')) cls += ' clear';
        return `
          <div class="${cls}">
            <span>${e.msg}</span>
            <span style="color: #64748b;">Tick ${e.tick} | Gen ${e.gen}</span>
          </div>
        `;
      }).join('');
    }
  } catch (e) {
    console.error('Survival Telemetry fetch error:', e);
  }
}

setInterval(fetchLiveTelemetry, 500);
fetchLiveTelemetry();
</script>

</body>
</html>
"""

@arc_router.get("/ui", response_class=HTMLResponse)
def get_arc_ui():
    """Serves the standalone interactive visual UI."""
    return HTMLResponse(content=generate_arc_html_dashboard())
