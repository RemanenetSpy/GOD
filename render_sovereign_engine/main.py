"""
========================================================================================
SOVEREIGN CIVILIZATION 24/7 CLOUD SERVER & VISUAL LABORATORY
========================================================================================
1. Runs the FULL Real Python Sovereign Civilization Engine (4 Pillars + All Physics).
2. Runs a continuous background simulation loop evolving 24/7.
3. Automatically pushes checkpoints & subroutines to Hugging Face Dataset Vault.
4. Serves a rich, real-time visual dual-canvas laboratory at `/`.
5. Exposes a live HTTP `/ping` endpoint for Keep-Alive bots (UptimeRobot).
========================================================================================
"""

import os
import sys
import time
import json
import threading
import numpy as np
from typing import Dict, Any, List, Tuple
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ca_universe import CellularAutomataUniverse
from civilization import (
    SovereignCivilization,
    Observation,
    Action,
    PillarArchetype
)
from hf_dataset_memory import HFDatasetMemoryVault

# Hugging Face Dataset Cloud Vault configuration
HF_TOKEN = os.environ.get("HF_TOKEN", "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")
HF_REPO = os.environ.get("HF_DATASET_REPO", "Explorerp/sovereign-civilization-memory")

vault = HFDatasetMemoryVault(repo_id=HF_REPO, token=HF_TOKEN)

# 24/7 Background Evolution Engine
class ContinuousEvolutionRunner:
    def __init__(self, grid_size: int = 25, ca_rule: str = "Conway (B3/S23)"):
        self.grid_size = grid_size
        self.grid_shape = (grid_size, grid_size)
        self.ca_rule = ca_rule
        self.universe = CellularAutomataUniverse(grid_shape=self.grid_shape, ca_rule=ca_rule)
        self.civ = SovereignCivilization(grid_shape=self.grid_shape)
        
        self.positions: Dict[str, Tuple[int, int]] = {
            "classical_prime": (2, 2),
            "quantum_prime": (grid_size - 3, 2),
            "modern_prime": (2, grid_size - 3),
            "string_meta": (grid_size - 3, grid_size - 3),
        }
        self.step_count = 0
        self.running = True
        self.speed_ms = 100
        self.last_saved_step = 0
        self.lock = threading.Lock()
        
        # Recover latest state from cloud
        self.load_from_cloud()
        
        # Start continuous evolution background worker thread
        self.thread = threading.Thread(target=self._evolution_loop, daemon=True)
        self.thread.start()

    def load_from_cloud(self):
        try:
            cloud_data = vault.load_checkpoint()
            if cloud_data:
                self.step_count = cloud_data.get("step_num", cloud_data.get("stepCount", 0))
                if "subroutines" in cloud_data:
                    self.civ.global_subroutine_archive.update(cloud_data["subroutines"])
                print(f"[Render Engine] Recovered from Cloud Vault at Step {self.step_count} with {len(self.civ.global_subroutine_archive)} subroutines!")
        except Exception as e:
            print(f"[Render Engine Warning] Initial recovery error: {e}")

    def _evolution_loop(self):
        print("[Render Engine] 24/7 Sovereign Evolution Loop STARTED in background!")
        while self.running:
            try:
                with self.lock:
                    self.step_count += 1
                    
                    # 1. Step Universe with current agent positions
                    rewards = self.universe.step(self.positions)
                    
                    # 2. Build local sensory observations
                    observations: Dict[str, Observation] = {}
                    h, w = self.grid_shape
                    for aid, node in self.civ.nodes.items():
                        py, px = self.positions[aid]
                        r = node.aperture
                        y_min, y_max = max(0, py - r), min(h, py + r + 1)
                        x_min, x_max = max(0, px - r), min(w, px + r + 1)
                        vis = self.universe.grid[y_min:y_max, x_min:x_max]
                        observations[aid] = Observation(
                            visible_cells=vis,
                            position=(py, px),
                            reward=rewards.get(aid, 0.0)
                        )
                        
                    # 3. Execute true Python physics step & message routing
                    actions = self.civ.step(observations)
                    
                    # 4. Move agents
                    for aid, act in actions.items():
                        py, px = self.positions[aid]
                        if act == Action.MOVE_UP: py = max(0, py - 1)
                        elif act == Action.MOVE_DOWN: py = min(h - 1, py + 1)
                        elif act == Action.MOVE_LEFT: px = max(0, px - 1)
                        elif act == Action.MOVE_RIGHT: px = min(w - 1, px + 1)
                        self.positions[aid] = (py, px)
                    
                    # Auto-commit to Hugging Face Cloud Vault every 25 steps
                    if self.step_count - self.last_saved_step >= 25:
                        self.last_saved_step = self.step_count
                        state_dict = {
                            "step_num": self.step_count,
                            "ca_rule": self.ca_rule,
                            "positions": {k: list(v) for k, v in self.positions.items()},
                            "subroutines": self.civ.global_subroutine_archive,
                            "agent_energies": {k: float(n.state.energy) for k, n in self.civ.nodes.items()},
                            "agent_temperatures": {k: float(n.state.temperature) for k, n in self.civ.nodes.items()},
                            "agent_fever": {k: bool(n.state.fever_active) for k, n in self.civ.nodes.items()},
                            "total_subroutines": len(self.civ.global_subroutine_archive)
                        }
                        vault.save_checkpoint(
                            state_dict,
                            commit_msg=f"Continuous 24/7 evolution step {self.step_count}",
                            async_upload=True
                        )

                # Control tick rate
                time.sleep(self.speed_ms / 1000.0)
            except Exception as e:
                print(f"[Render Evolution Error]: {e}")
                time.sleep(1.0)

    def trigger_fever(self):
        with self.lock:
            for n in self.civ.nodes.values():
                n.fever_active = True
                n.state.fever_active = True
                n.state.temperature = min(3.0, n.state.temperature + 1.0)

    def reset(self, rule: str = "Conway (B3/S23)"):
        with self.lock:
            self.ca_rule = rule
            self.universe = CellularAutomataUniverse(grid_shape=self.grid_shape, ca_rule=rule)
            self.civ = SovereignCivilization(grid_shape=self.grid_shape)
            self.positions = {
                "classical_prime": (2, 2),
                "quantum_prime": (self.grid_size - 3, 2),
                "modern_prime": (2, self.grid_size - 3),
                "string_meta": (self.grid_size - 3, self.grid_size - 3),
            }
            self.step_count = 0

    def get_live_payload(self) -> Dict[str, Any]:
        with self.lock:
            consensus = self.civ.synthesize_consensus()
            # Intensity of mind field
            mind_intensity = (consensus.sum(axis=-1) * 60.0).clip(0, 255).astype(int).tolist()
            
            nodes_data = []
            for aid, n in self.civ.nodes.items():
                nodes_data.append({
                    "id": aid,
                    "pillar": n.pillar.value,
                    "pos": list(self.positions.get(aid, (0, 0))),
                    "energy": float(n.state.energy),
                    "dh_dt": float(n.state.dh_dt),
                    "temperature": float(n.state.temperature),
                    "viscosity": float(n.state.viscosity),
                    "entropy": float(n.state.belief_entropy),
                    "fever": bool(n.state.fever_active)
                })
                
            recent_msgs = [m.summary() for m in self.civ.fabric.history[-25:]]
            recent_msgs.reverse()
            
            return {
                "step": self.step_count,
                "ca_rule": self.ca_rule,
                "grid_size": self.grid_size,
                "grid": self.universe.grid.tolist(),
                "mind_field": mind_intensity,
                "nodes": nodes_data,
                "subroutines": self.civ.global_subroutine_archive,
                "messages": recent_msgs,
                "total_messages": self.civ.fabric.total_messages_routed,
                "cloud_vault": HF_REPO
            }


runner = ContinuousEvolutionRunner()
app = FastAPI(title="Sovereign Civilization 24/7 Cloud Engine")

@app.get("/api/state")
def api_state():
    return runner.get_live_payload()

@app.post("/api/action/fever")
def api_fever():
    runner.trigger_fever()
    return {"status": "FEVER_TRIGGERED"}

@app.post("/api/action/reset")
def api_reset(rule: str = "Conway (B3/S23)"):
    runner.reset(rule)
    return {"status": "RESET_OK"}

@app.get("/ping")
def ping():
    return JSONResponse(content={"status": "OK", "step": runner.step_count})

@app.get("/", response_class=HTMLResponse)
def visual_dashboard():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>🌌 Sovereign Civilization 24/7 Cloud Engine (Python Core)</title>
  <style>
    :root {
      --bg-main: #0a0e17;
      --bg-panel: #111827;
      --border-color: #1f2937;
      --accent-cyan: #38bdf8;
      --accent-purple: #a855f7;
      --accent-amber: #f59e0b;
      --accent-pink: #ec4899;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-main);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-color);
      flex-wrap: wrap;
      gap: 8px;
    }

    .title-group h1 { font-size: 1.35rem; color: #fff; font-weight: 700; }
    .title-group p { font-size: 0.8rem; color: var(--text-muted); margin-top: 4px; }
    .badge {
      background: rgba(16, 185, 129, 0.2);
      color: #10b981;
      border: 1px solid #10b981;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
    }

    .controls-bar {
      display: flex;
      gap: 10px;
      align-items: center;
      background: var(--bg-panel);
      padding: 10px 16px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      flex-wrap: wrap;
    }

    button {
      background: #1f2937;
      color: #fff;
      border: 1px solid #374151;
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.85rem;
      transition: all 0.2s;
    }
    button:hover { background: #374151; }
    button.fever { background: #7f1d1d; border-color: #ef4444; color: #fca5a5; }
    button.fever:hover { background: #991b1b; }

    .canvas-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    @media (max-width: 850px) {
      .canvas-container { grid-template-columns: 1fr; }
    }

    .panel {
      background: var(--bg-panel);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .panel-title { font-weight: 600; font-size: 0.95rem; }

    .canvas-wrapper {
      position: relative;
      width: 100%;
      aspect-ratio: 1 / 1;
      background: #000;
      border-radius: 6px;
      overflow: hidden;
    }

    canvas {
      width: 100%;
      height: 100%;
      display: block;
      image-rendering: pixelated;
    }

    .telemetry-grid {
      display: grid;
      grid-template-columns: 3fr 2fr;
      gap: 16px;
    }
    @media (max-width: 900px) {
      .telemetry-grid { grid-template-columns: 1fr; }
    }

    table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
    th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border-color); }
    th { color: var(--text-muted); font-weight: 600; }

    .agent-tag { font-weight: 700; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; }
    .tag-classical { background: rgba(56, 189, 248, 0.2); color: var(--accent-cyan); }
    .tag-quantum { background: rgba(168, 85, 247, 0.2); color: var(--accent-purple); }
    .tag-modern { background: rgba(245, 158, 11, 0.2); color: var(--accent-amber); }
    .tag-string { background: rgba(236, 72, 153, 0.2); color: var(--accent-pink); }

    .fever-badge { font-size: 0.7rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; }
    .fever-on { background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid #ef4444; }
    .fever-off { color: #10b981; }

    .stream-box {
      background: #000;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      height: 140px;
      overflow-y: auto;
      padding: 8px;
      font-family: monospace;
      font-size: 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .stream-line.fever { color: #f87171; }
    .stream-line.sub { color: var(--accent-pink); }
    .stream-line.grad { color: var(--accent-cyan); }
  </style>
</head>
<body>

  <header>
    <div class="title-group">
      <h1>🌌 Sovereign Civilization: 24/7 Real Python Cloud Engine</h1>
      <p>Powered by Real Native Python 3.11 Backend | God Equation: <code>S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)</code></p>
    </div>
    <div class="badge" id="phase-badge">● LIVE 24/7 PYTHON RUNTIME</div>
  </header>

  <div class="controls-bar">
    <button class="fever" id="btn-fever">🔥 Trigger Fever</button>
    <button id="btn-reset">🔄 Reset Universe</button>
    <span id="cloud-status" style="font-size: 0.75rem; color: #10b981; margin-left: auto;">☁️ Cloud Vault: Connected (Explorerp/sovereign-civilization-memory)</span>
  </div>

  <div class="canvas-container">
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">🌱 Living Cellular Automata Universe</div>
        <span style="font-size: 0.8rem; color: var(--text-muted);">Green: Life | Red: Barriers | C/Q/M/S: Real Python Agents</span>
      </div>
      <div class="canvas-wrapper">
        <canvas id="ca-canvas" width="400" height="400"></canvas>
      </div>
    </div>

    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">🧠 Collective Consciousness Consensus Field Φ(x)</div>
        <span style="font-size: 0.8rem; color: var(--text-muted);">True Quantum Belief Tensors Synthesized via M_t^i</span>
      </div>
      <div class="canvas-wrapper">
        <canvas id="mind-canvas" width="400" height="400"></canvas>
      </div>
    </div>
  </div>

  <div class="telemetry-grid">
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">📊 Real-Time Relativistic Agent Telemetry (S_t^i)</div>
        <span id="telemetry-summary" style="font-size: 0.8rem; color: var(--text-muted);">Step: 000 | Total Energy: 1200.0</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Agent</th>
            <th>Pillar</th>
            <th>Pos</th>
            <th>Energy (H)</th>
            <th>dH/dt</th>
            <th>Temp (T)</th>
            <th>Viscosity</th>
            <th>Entropy</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody id="telemetry-body"></tbody>
      </table>
    </div>

    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">📜 Kolmogorov Subroutine Archive (L(S_t))</div>
        <span id="sub-count" style="font-size: 0.8rem; color: var(--text-muted);">0 Subroutines</span>
      </div>
      <div class="stream-box" id="subroutine-box"></div>
    </div>
  </div>

  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">📡 Relativistic Message Stream (M_t^i Tensor Fabric)</div>
      <span id="msg-counter" style="font-size: 0.8rem; color: var(--text-muted);">0 Messages Exchanged</span>
    </div>
    <div class="stream-box" id="message-box"></div>
  </div>

  <script>
    const canvasCA = document.getElementById("ca-canvas");
    const ctxCA = canvasCA.getContext("2d");
    const canvasMind = document.getElementById("mind-canvas");
    const ctxMind = canvasMind.getContext("2d");

    const AGENT_COLORS = {
      "classical_prime": "#38bdf8",
      "quantum_prime": "#a855f7",
      "modern_prime": "#f59e0b",
      "string_meta": "#ec4899"
    };

    const AGENT_SYMBOLS = {
      "classical_prime": "C",
      "quantum_prime": "Q",
      "modern_prime": "M",
      "string_meta": "S"
    };

    async function fetchState() {
      try {
        const res = await fetch("/api/state");
        if (!res.ok) return;
        const data = await res.json();
        render(data);
      } catch (e) {}
    }

    function render(data) {
      const s = data.grid_size || 25;
      const w = canvasCA.width;
      const h = canvasCA.height;
      const cellW = w / s;
      const cellH = h / s;

      // 1. Render Living Grid
      ctxCA.fillStyle = "#000000";
      ctxCA.fillRect(0, 0, w, h);

      for (let y = 0; y < s; y++) {
        for (let x = 0; x < s; x++) {
          const val = data.grid[y][x];
          if (val === 1) {
            ctxCA.fillStyle = "#10b981";
            ctxCA.fillRect(x * cellW, y * cellH, cellW - 1, cellH - 1);
          } else if (val === 2) {
            ctxCA.fillStyle = "#ef4444";
            ctxCA.fillRect(x * cellW, y * cellH, cellW - 1, cellH - 1);
          }
        }
      }

      // Render Agents
      data.nodes.forEach(node => {
        const [py_idx, px_idx] = node.pos;
        const color = AGENT_COLORS[node.id] || "#fff";
        const sym = AGENT_SYMBOLS[node.id] || "?";

        // Draw Aperture Box
        ctxCA.strokeStyle = color;
        ctxCA.lineWidth = 1.5;
        const r = 3;
        ctxCA.strokeRect((px_idx - r) * cellW, (py_idx - r) * cellH, (r * 2 + 1) * cellW, (r * 2 + 1) * cellH);

        // Draw Agent Circle
        const px = px_idx * cellW + cellW / 2;
        const py = py_idx * cellH + cellH / 2;
        ctxCA.beginPath();
        ctxCA.arc(px, py, cellW * 0.45, 0, Math.PI * 2);
        ctxCA.fillStyle = color;
        ctxCA.fill();
        ctxCA.strokeStyle = "#fff";
        ctxCA.stroke();

        ctxCA.fillStyle = "#000";
        ctxCA.font = "bold 10px sans-serif";
        ctxCA.textAlign = "center";
        ctxCA.textBaseline = "middle";
        ctxCA.fillText(sym, px, py);
      });

      // 2. Render Consensus Mind Field
      ctxMind.fillStyle = "#0d1117";
      ctxMind.fillRect(0, 0, w, h);

      for (let y = 0; y < s; y++) {
        for (let x = 0; x < s; x++) {
          const intensity = data.mind_field[y][x];
          ctxMind.fillStyle = `rgb(${intensity}, ${Math.floor(intensity * 0.4)}, ${Math.floor(intensity * 0.8)})`;
          ctxMind.fillRect(x * cellW, y * cellH, cellW, cellH);
        }
      }

      // 3. Render Telemetry Table
      const tbody = document.getElementById("telemetry-body");
      tbody.innerHTML = "";
      let totEnergy = 0;

      data.nodes.forEach(node => {
        totEnergy += node.energy;
        const tr = document.createElement("tr");
        const tagClass = `tag-${node.pillar.split("-")[0].toLowerCase()}`;
        const feverBadge = node.fever ? `<span class="fever-badge fever-on">🔥 FEVER</span>` : `<span class="fever-badge fever-off">❄️ STABLE</span>`;

        tr.innerHTML = `
          <td><span class="agent-tag ${tagClass}">${node.id}</span></td>
          <td>${node.pillar}</td>
          <td>(${node.pos[0]}, ${node.pos[1]})</td>
          <td>${node.energy.toFixed(1)}</td>
          <td>${node.dh_dt >= 0 ? '+' : ''}${node.dh_dt.toFixed(2)}</td>
          <td>${node.temperature.toFixed(2)}</td>
          <td>${node.viscosity.toFixed(2)}</td>
          <td>${node.entropy.toFixed(2)}</td>
          <td>${feverBadge}</td>
        `;
        tbody.appendChild(tr);
      });

      document.getElementById("telemetry-summary").innerText = `Step: ${data.step.toString().padStart(3, '0')} | Total Energy: ${totEnergy.toFixed(1)}`;
      document.getElementById("msg-counter").innerText = `${data.total_messages} Messages Exchanged`;

      // 4. Render Subroutines
      const subBox = document.getElementById("subroutine-box");
      const subKeys = Object.keys(data.subroutines || {});
      document.getElementById("sub-count").innerText = `${subKeys.length} Subroutines`;
      if (subKeys.length > 0) {
        subBox.innerHTML = subKeys.map(k => `<div class="stream-line sub">• [${k}]: ${data.subroutines[k]}</div>`).join("");
      }

      // 5. Render Messages
      const msgBox = document.getElementById("message-box");
      if (data.messages && data.messages.length > 0) {
        msgBox.innerHTML = data.messages.map(m => {
          const cls = m.includes("fever") ? "fever" : (m.includes("subroutine") ? "sub" : "grad");
          return `<div class="stream-line ${cls}">[M_t^i] ${m}</div>`;
        }).join("");
      }
    }

    document.getElementById("btn-fever").onclick = () => fetch("/api/action/fever", { method: "POST" });
    document.getElementById("btn-reset").onclick = () => fetch("/api/action/reset", { method: "POST" });

    // Poll live Python server every 120ms
    setInterval(fetchState, 120);
    fetchState();
  </script>
</body>
</html>
"""
