"""
========================================================================================
SOVEREIGN MULTIVERSE 24/7 ENGINE: DUAL-PLATFORM CLOUD & IN-BROWSER ARCHITECTURE
========================================================================================
Platform 1: 🌌 24/7 Live Cloud Multiverse
- 21 Parallel Universes running continuously on Render
- Real-time zero-lock public spectator mode
- Sovereign Master Key Access Control (Owner-exclusive world mutations)

Platform 2: 💻 Local Sandbox Laboratory (In-Browser Web Physics)
- 100% Client-Side Simulation running on the player's own device CPU/GPU at 60 FPS
- Zero server overhead ($0 cost for unlimited simultaneous players)
- Interactive Canvas Painting Tools (Draw chemicals, wire circuits, solitons)
- Local Autonomous Cognitive Agents & Kolmogorov Rule Synthesizer
- "Contribute to Global Vault" button (Syncs rare discoveries to Hugging Face)
========================================================================================
"""

import os
import sys
import time
import json
import threading
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Response, Header
from fastapi.responses import HTMLResponse, JSONResponse

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add src and src/environments to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'environments'))

from environments.registry import SubstrateRegistry
from civilization import (
    SovereignCivilization,
    Observation,
    Action,
    PillarArchetype
)
from hf_dataset_memory import HFDatasetMemoryVault

# Load local gitignored .env if present
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                if k not in os.environ:
                    os.environ[k] = v

HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_REPO = os.environ.get("HF_DATASET_REPO", "Explorerp/sovereign-civilization-memory")
ADMIN_SECRET_KEY = os.environ.get("ADMIN_SECRET_KEY", "sovereign-master-2026")

vault = HFDatasetMemoryVault(repo_id=HF_REPO, token=HF_TOKEN)

# Global Non-Blocking Atomic Payload Cache for instantaneous 0ms responses
CACHED_PAYLOADS: Dict[str, Any] = {}
COMMUNITY_DISCOVERIES: List[Dict[str, Any]] = []
CACHE_LOCK = threading.Lock()


class DiscoverySubmission(BaseModel):
    signature: str
    code_str: str
    description: str
    realm: str
    author: Optional[str] = "Anonymous Pioneer"
    step_discovered: Optional[int] = 0


class UniverseInstance:
    def __init__(
        self,
        universe_id: str,
        mode_name: str,
        substrate_name: str = "lenia",
        enable_pruning: bool = False,
        max_pop: int = 10,
        grid_size: int = 25,
        physics_model: str = "Continuous Physics",
        vault_file: str = "civilization_champion.json"
    ):
        self.universe_id = universe_id
        self.mode_name = mode_name
        self.substrate_name = substrate_name
        self.grid_size = grid_size
        self.grid_shape = (grid_size, grid_size)
        self.physics_model = physics_model
        self.vault_file = vault_file
        
        self.universe = SubstrateRegistry.get_substrate(
            name=substrate_name,
            grid_shape=self.grid_shape
        )
        self.civ = SovereignCivilization(
            grid_shape=self.grid_shape,
            max_population=max_pop,
            enable_cyclic_pruning=enable_pruning
        )
        
        self.positions: Dict[str, Tuple[int, int]] = {
            "classical_prime": (2, 2),
            "quantum_prime": (grid_size - 3, 2),
            "modern_prime": (2, grid_size - 3),
            "string_meta": (grid_size - 3, grid_size - 3),
        }
        self.step_count = 0
        self.last_saved_time = time.time()
        
        self.load_from_cloud()
        self.update_cache()

    def load_from_cloud(self):
        try:
            cloud_data = vault.load_checkpoint(filename=self.vault_file)
            if cloud_data:
                self.step_count = cloud_data.get("step_num", cloud_data.get("stepCount", 0))
                if "subroutines" in cloud_data:
                    raw_subs = cloud_data["subroutines"]
                    clean_subs = {}
                    for sig, code in raw_subs.items():
                        if "laplacian_diff" in sig:
                            clean_subs["prog_laplacian_diffusion"] = code
                        elif "cluster_" in sig:
                            clean_subs["prog_cluster_decomposition"] = code
                        elif "reaction_kinetics" in sig:
                            clean_subs["prog_reaction_kinetics"] = code
                        elif "soliton" in sig:
                            clean_subs["prog_soliton_harmonic"] = code
                        else:
                            clean_subs[sig] = code
                    self.civ.global_subroutine_archive = clean_subs
                print(f"[Render Engine] [{self.mode_name}] Recovered at Step {self.step_count} with {len(self.civ.global_subroutine_archive)} canonical subroutines!")
        except Exception as e:
            print(f"[Render Engine Warning] Recovery error for {self.universe_id}: {e}")

    def step_tick(self):
        try:
            self.step_count += 1
            h, w = self.grid_shape
            
            for aid in list(self.civ.nodes.keys()):
                if aid not in self.positions:
                    self.positions[aid] = (
                        np.random.randint(2, self.grid_size - 2),
                        np.random.randint(2, self.grid_size - 2)
                    )
            
            for pos_id in list(self.positions.keys()):
                if pos_id not in self.civ.nodes:
                    del self.positions[pos_id]
            
            climate = self.universe.get_climate_telemetry()
            rewards = self.universe.step(self.positions)
            
            observations: Dict[str, Observation] = {}
            for aid, node in self.civ.nodes.items():
                py, px = self.positions[aid]
                patch = self.universe.get_observation(py, px, node.aperture)
                rew = rewards.get(aid, 0.0)
                observations[aid] = Observation(
                    visible_cells=patch,
                    position=(py, px),
                    reward=rew
                )
                
            actions = self.civ.step(observations, climate_telemetry=climate)
            
            for aid, act in actions.items():
                if aid not in self.positions:
                    continue
                py, px = self.positions[aid]
                if act == Action.MOVE_UP: py = max(0, py - 1)
                elif act == Action.MOVE_DOWN: py = min(h - 1, py + 1)
                elif act == Action.MOVE_LEFT: px = max(0, px - 1)
                elif act == Action.MOVE_RIGHT: px = min(w - 1, px + 1)
                self.positions[aid] = (py, px)

            self.update_cache(climate=climate)

            now = time.time()
            if now - self.last_saved_time >= 90.0:
                self.last_saved_time = now
                state_dict = {
                    "universe_id": self.universe_id,
                    "mode_name": self.mode_name,
                    "substrate_name": self.substrate_name,
                    "step_num": self.step_count,
                    "physics_model": self.physics_model,
                    "climate": climate,
                    "population": len(self.civ.nodes),
                    "subroutines": self.civ.global_subroutine_archive,
                    "total_subroutines": len(self.civ.global_subroutine_archive)
                }
                vault.save_checkpoint(
                    state_dict,
                    filename=self.vault_file,
                    commit_msg=f"24/7 {self.mode_name} step {self.step_count}",
                    async_upload=True
                )
        except Exception as e:
            print(f"[Render Step Error {self.universe_id}]: {e}")

    def update_cache(self, climate: Any = None):
        if climate is None:
            climate = self.universe.get_climate_telemetry()
            
        grid_list = np.round(self.universe.grid.astype(float), 3).tolist()
        
        nodes_data = []
        for aid, node in self.civ.nodes.items():
            py, px = self.positions.get(aid, (0, 0))
            nodes_data.append({
                "id": aid,
                "pillar": node.pillar.value,
                "pos": [py, px],
                "energy": round(float(node.state.energy), 1),
                "temperature": round(float(node.state.temperature), 2),
                "viscosity": round(float(node.state.viscosity), 2),
                "dh_dt": round(float(node.state.dh_dt), 2),
                "fever": bool(node.state.fever_active),
                "entropy": round(float(node.state.belief_entropy), 3),
                "sub_count": len(node.kolmogorov_engine.program_library),
                "dim_10d": len(node.state.cognitive_10d)
            })
            
        all_subs = list(self.civ.global_subroutine_archive.items())
        recent_subs = [{"signature": sig, "code": code} for sig, code in all_subs[-10:]]

        recent_msgs = [m.summary() for m in self.civ.fabric.history[-8:]]
        
        consensus_tensor = self.civ.synthesize_consensus()
        consciousness_heatmap = np.round(np.mean(consensus_tensor, axis=-1), 3).tolist()

        payload = {
            "universe_id": self.universe_id,
            "mode_name": self.mode_name,
            "substrate_name": self.substrate_name,
            "step": self.step_count,
            "population": len(self.civ.nodes),
            "climate": climate,
            "physics_model": self.physics_model,
            "grid": grid_list,
            "consciousness": consciousness_heatmap,
            "nodes": nodes_data,
            "subroutines": recent_subs,
            "total_laws": len(all_subs),
            "messages": recent_msgs,
            "events": {
                "births": self.civ.mitosis_engine.birth_events[-5:],
                "mergers": self.civ.mitosis_engine.merger_events[-5:],
                "prunings": self.civ.pruning_events[-5:]
            },
            "stagnation_steps": self.civ.steps_since_last_discovery,
            "pruning_enabled": self.civ.enable_cyclic_pruning,
            "total_messages": self.civ.fabric.total_messages_routed,
            "cloud_vault": HF_REPO
        }
        
        with CACHE_LOCK:
            CACHED_PAYLOADS[self.universe_id] = payload

    def trigger_fever(self):
        for n in self.civ.nodes.values():
            n.fever_engine.force_fever()
            n.state.fever_active = True
            n.state.temperature = min(3.0, n.state.temperature + 1.5)
        self.update_cache()

    def reset(self):
        self.universe = SubstrateRegistry.get_substrate(
            name=self.substrate_name,
            grid_shape=self.grid_shape
        )
        self.civ = SovereignCivilization(
            grid_shape=self.grid_shape,
            max_population=self.civ.max_population,
            enable_cyclic_pruning=self.civ.enable_cyclic_pruning
        )
        self.positions = {
            "classical_prime": (2, 2),
            "quantum_prime": (self.grid_size - 3, 2),
            "modern_prime": (2, self.grid_size - 3),
            "string_meta": (self.grid_size - 3, self.grid_size - 3),
        }
        self.step_count = 0
        self.update_cache()


# --- 21-UNIVERSE MULTIVERSE REGISTRY SETUP ---
REALMS = [
    {"id": "r1", "name": "Realm 1: Classic Discrete CA", "icon": "🏛️", "substrate": "classic_ca", "physics": "Conway Discrete Life (B3/S23)"},
    {"id": "r2", "name": "Realm 2: Seasonal Scarcity CA", "icon": "🍂", "substrate": "seasonal_scarcity", "physics": "4-Season Solar Energy Scarcity & Famine"},
    {"id": "r3", "name": "Realm 3: Continuous Wave Lenia", "icon": "🌊", "substrate": "lenia", "physics": "Continuous Wave Lenia (μ=0.15, σ=0.015)"},
    {"id": "r4", "name": "Realm 4: Reaction-Diffusion", "icon": "🧬", "substrate": "reaction_diffusion", "physics": "Gray-Scott Turing Morphogenesis Field"},
    {"id": "r5", "name": "Realm 5: Wireworld Digital Circuit", "icon": "⚡", "substrate": "wireworld", "physics": "4-State Wireworld Digital Circuit & Logic"},
    {"id": "r6", "name": "Realm 6: Lattice Gas Hydrodynamics", "icon": "💨", "substrate": "lattice_gas", "physics": "FHP Discrete Momentum & Particle Streaming"},
    {"id": "r7", "name": "Realm 7: Red Queen Co-Evolution Arena", "icon": "⚔️", "substrate": "red_queen", "physics": "Co-Evolutionary Predator-Prey Ecological Arms Race"}
]

runners: Dict[str, UniverseInstance] = {}

for r in REALMS:
    rid = r["id"]
    rname = r["name"]
    ricon = r["icon"]
    sub = r["substrate"]
    phys = r["physics"]
    
    runners[f"{rid}_a"] = UniverseInstance(
        universe_id=f"{rid}_a",
        mode_name=f"{ricon} {rname} [Universe A - Ancient Stasis]",
        substrate_name=sub,
        enable_pruning=False,
        max_pop=10,
        physics_model=phys,
        vault_file=f"civilization_{rid}_a.json"
    )
    runners[f"{rid}_b"] = UniverseInstance(
        universe_id=f"{rid}_b",
        mode_name=f"{ricon} {rname} [Universe B - Pioneers (Pruned)]",
        substrate_name=sub,
        enable_pruning=True,
        max_pop=10,
        physics_model=phys,
        vault_file=f"civilization_{rid}_b.json"
    )
    runners[f"{rid}_c"] = UniverseInstance(
        universe_id=f"{rid}_c",
        mode_name=f"{ricon} {rname} [Universe C - Darwinian Colony (35 Pop)]",
        substrate_name=sub,
        enable_pruning=True,
        max_pop=35,
        physics_model=phys,
        vault_file=f"civilization_{rid}_c.json"
    )


# --- HIGH-PERFORMANCE COOPERATIVE MULTIVERSE SCHEDULER ---
RUNNING = True

def _master_multiverse_worker():
    print("[Render Engine] Cooperative 21-Universe Multiverse Master Loop STARTED!")
    tick_delay = float(os.environ.get("TICK_DELAY_SEC", 0.012))
    
    while RUNNING:
        try:
            for uid, runner in runners.items():
                runner.step_tick()
            time.sleep(tick_delay)
        except Exception as e:
            print(f"[Master Multiverse Error]: {e}")
            time.sleep(1.0)

worker_thread = threading.Thread(target=_master_multiverse_worker, daemon=True)
worker_thread.start()


# --- FASTAPI WEB INTERFACE ---
app = FastAPI(title="Sovereign Multiverse Dual-Platform Engine")


@app.api_route("/ping", methods=["GET", "HEAD"])
@app.api_route("/health", methods=["GET", "HEAD"])
def ping_health():
    return JSONResponse(
        content={
            "status": "ok",
            "service": "sovereign-multiverse-24-7",
            "active_realms": 7,
            "active_universes": len(runners),
            "cloud_vault": HF_REPO
        },
        status_code=200
    )


@app.api_route("/api/state", methods=["GET", "HEAD"])
def api_state(u: str = "r3_a"):
    target_key = u.lower()
    with CACHE_LOCK:
        if target_key in CACHED_PAYLOADS:
            return CACHED_PAYLOADS[target_key]
        fallback_key = "r3_a" if "r3_a" in CACHED_PAYLOADS else next(iter(CACHED_PAYLOADS.keys()), None)
        if fallback_key:
            return CACHED_PAYLOADS[fallback_key]
    target_runner = runners.get(target_key, runners.get("r3_a"))
    if target_runner:
        return target_runner.update_cache()
    return {"status": "initializing"}


@app.post("/api/action/verify_admin")
def verify_admin(x_admin_key: Optional[str] = Header(None)):
    admin_secret = os.environ.get("ADMIN_SECRET_KEY", "sovereign-master-2026")
    if x_admin_key and x_admin_key == admin_secret:
        return {"status": "AUTHORIZED", "is_admin": True}
    return JSONResponse(status_code=403, content={"status": "UNAUTHORIZED", "is_admin": False, "error": "Invalid Sovereign Admin Key."})


@app.post("/api/action/fever")
def api_fever(u: str = "r3_a", x_admin_key: Optional[str] = Header(None)):
    admin_secret = os.environ.get("ADMIN_SECRET_KEY", "sovereign-master-2026")
    if not x_admin_key or x_admin_key != admin_secret:
        return JSONResponse(
            status_code=403,
            content={"status": "FORBIDDEN", "error": "Access Locked: God Mode Master Key required to alter the multiverse."}
        )
    target_runner = runners.get(u.lower(), runners.get("r3_a"))
    if target_runner:
        target_runner.trigger_fever()
    return {"status": "FEVER_TRIGGERED", "universe": u}


@app.post("/api/action/reset")
def api_reset(u: str = "r3_a", x_admin_key: Optional[str] = Header(None)):
    admin_secret = os.environ.get("ADMIN_SECRET_KEY", "sovereign-master-2026")
    if not x_admin_key or x_admin_key != admin_secret:
        return JSONResponse(
            status_code=403,
            content={"status": "FORBIDDEN", "error": "Access Locked: God Mode Master Key required to reset the universe."}
        )
    target_runner = runners.get(u.lower(), runners.get("r3_a"))
    if target_runner:
        target_runner.reset()
    return {"status": "UNIVERSE_RESET", "universe": u}


# 5. Smart Telemetry Submission from In-Browser Players
@app.post("/api/submit_discovery")
def submit_discovery(sub: DiscoverySubmission):
    entry = {
        "signature": sub.signature,
        "code_str": sub.code_str,
        "description": sub.description,
        "realm": sub.realm,
        "author": sub.author,
        "timestamp": time.time()
    }
    with CACHE_LOCK:
        COMMUNITY_DISCOVERIES.append(entry)
        if len(COMMUNITY_DISCOVERIES) > 50:
            COMMUNITY_DISCOVERIES.pop(0)
            
    # Asynchronously save to community dataset vault
    vault.save_checkpoint(
        {"discoveries": COMMUNITY_DISCOVERIES, "count": len(COMMUNITY_DISCOVERIES)},
        filename="community_discoveries.json",
        commit_msg=f"Community discovery from {sub.author} in {sub.realm}",
        async_upload=True
    )
    return {"status": "DISCOVERY_RECORDED", "total_community_discoveries": len(COMMUNITY_DISCOVERIES)}


HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sovereign Multiverse — 24/7 Cloud & In-Browser Lab</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: #030712;
      color: #f3f4f6;
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      min-height: 100vh;
    }
    
    /* Master Mode Header Navigation */
    .platform-switcher {
      display: flex;
      gap: 8px;
      background: #0f172a;
      padding: 6px;
      border-radius: 10px;
      border: 1px solid #1e293b;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
    }
    .mode-tab-group { display: flex; gap: 6px; }
    .mode-tab {
      background: #1e293b;
      color: #94a3b8;
      border: 1px solid #334155;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 0.76rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }
    .mode-tab:hover { background: #334155; color: #fff; }
    .mode-tab.active {
      background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%);
      color: #fff;
      border-color: #38bdf8;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }

    header {
      background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
      padding: 10px 16px;
      border-radius: 12px;
      border: 1px solid #374151;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .header-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }
    .title-box h1 {
      font-size: 1.2rem;
      background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc, #f43f5e);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-weight: 800;
    }
    .title-box p { font-size: 0.72rem; color: #9ca3af; }
    
    /* 2-Tier Cloud Selector */
    .selector-container {
      display: flex;
      flex-direction: column;
      gap: 5px;
      margin-top: 2px;
    }
    .realm-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }
    .realm-btn {
      background: #1f2937;
      color: #9ca3af;
      border: 1px solid #374151;
      padding: 4px 9px;
      border-radius: 6px;
      font-size: 0.70rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }
    .realm-btn:hover { background: #374151; color: #fff; }
    .realm-btn.active {
      background: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }
    
    .branch-bar {
      display: flex;
      gap: 5px;
      flex-wrap: wrap;
    }
    .branch-btn {
      background: #111827;
      color: #9ca3af;
      border: 1px solid #374151;
      padding: 3px 10px;
      border-radius: 6px;
      font-size: 0.70rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }
    .branch-btn:hover { background: #1f2937; color: #fff; }
    .branch-btn.active {
      background: #4f46e5;
      color: #ffffff;
      border-color: #818cf8;
      box-shadow: 0 0 8px rgba(129, 140, 248, 0.4);
    }

    .main-grid {
      display: grid;
      grid-template-columns: 330px 1fr;
      gap: 10px;
      align-items: start;
    }
    @media (max-width: 1024px) {
      .main-grid { grid-template-columns: 1fr; }
    }
    .card {
      background-color: #111827;
      border: 1px solid #1f2937;
      border-radius: 10px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .card-title {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #9ca3af;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1f2937;
      padding-bottom: 4px;
    }
    .canvas-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      position: relative;
    }
    canvas {
      image-rendering: pixelated;
      background: #000;
      border-radius: 6px;
      border: 1px solid #374151;
      box-shadow: 0 0 15px rgba(0,0,0,0.8);
      max-width: 100%;
      cursor: crosshair;
    }
    .telemetry-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.70rem;
    }
    .telemetry-table th, .telemetry-table td {
      padding: 3px 5px;
      text-align: left;
      border-bottom: 1px solid #1f2937;
    }
    .telemetry-table th { color: #6b7280; font-weight: 600; }
    .agent-tag {
      padding: 1px 4px;
      border-radius: 3px;
      font-weight: 700;
      font-size: 0.65rem;
    }
    .tag-classical { background: #1e3a8a; color: #93c5fd; }
    .tag-quantum { background: #581c87; color: #d8b4fe; }
    .tag-modern { background: #713f12; color: #fde047; }
    .tag-string { background: #831843; color: #f9a8d4; }
    .tag-hybrid { background: #064e3b; color: #6ee7b7; }
    .fever-badge {
      font-size: 0.62rem;
      padding: 1px 3px;
      border-radius: 3px;
      font-weight: 800;
    }
    .fever-on { background: #dc2626; color: #fff; animation: pulse 1s infinite; }
    .fever-off { background: #1f2937; color: #6b7280; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    
    .stream-box {
      background: #030712;
      border: 1px solid #1f2937;
      border-radius: 6px;
      padding: 5px;
      font-family: 'Fira Code', monospace;
      font-size: 0.66rem;
      height: 110px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .stream-line { border-left: 2px solid #374151; padding-left: 5px; }
    .stream-line.sub { border-left-color: #ec4899; color: #f472b6; }
    .stream-line.fever { border-left-color: #ef4444; color: #f87171; }
    .stream-line.prune { border-left-color: #eab308; color: #fde047; }
    .stream-line.mitosis { border-left-color: #10b981; color: #6ee7b7; }
    .stream-line.grad { border-left-color: #3b82f6; color: #93c5fd; }
    
    .btn-group { display: flex; gap: 6px; align-items: center; }
    .action-btn {
      background: #1f2937;
      border: 1px solid #374151;
      color: #f3f4f6;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 0.70rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }
    .action-btn:hover { background: #374151; border-color: #4b5563; }
    .action-btn.fever-btn { border-color: #dc2626; color: #f87171; }
    .action-btn.fever-btn:hover { background: #7f1d1d; color: #fff; }
    .action-btn.submit-btn { border-color: #10b981; color: #6ee7b7; }
    .action-btn.submit-btn:hover { background: #065f46; color: #fff; }
    .key-btn { border-color: #8b5cf6; color: #c4b5fd; }
    .key-btn:hover { background: #5b21b6; color: #fff; }

    .badge-status {
      font-size: 0.68rem;
      padding: 3px 7px;
      border-radius: 5px;
      font-weight: 700;
    }
    .badge-readonly { background: #1f2937; color: #9ca3af; border: 1px solid #374151; }
    .badge-admin { background: #065f46; color: #34d399; border: 1px solid #059669; }
    
    /* In-Browser Tool Bar */
    .browser-tools {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
      background: #0b0f19;
      padding: 6px 10px;
      border-radius: 8px;
      border: 1px solid #1e293b;
    }
    .tool-select {
      background: #1e293b;
      color: #f3f4f6;
      border: 1px solid #374151;
      padding: 3px 6px;
      border-radius: 4px;
      font-size: 0.70rem;
    }
  </style>
</head>
<body>

  <!-- Master Platform Navigation Switcher -->
  <div class="platform-switcher">
    <div class="mode-tab-group">
      <button id="tab-cloud-mode" class="mode-tab active">🌌 24/7 Live Multiverse (Cloud Spectator)</button>
      <button id="tab-browser-mode" class="mode-tab">💻 In-Browser Sandbox Lab (Your Device CPU/GPU)</button>
    </div>
    <div style="font-size:0.7rem; color:#94a3b8;">
      <span id="platform-status-tag">⚡ Live Synchronized Stream</span>
    </div>
  </div>

  <header id="main-header">
    <div class="header-top">
      <div class="title-box">
        <h1 id="multiverse-title">🌌 Sovereign Multiverse 24/7 — 21 Living Universes</h1>
        <p id="universe-subtitle">7 Physical Substrates x 3 Evolution Branches | Zero-Lock Instantaneous Engine</p>
      </div>
      <div class="btn-group" id="header-action-group">
        <span id="admin-badge" class="badge-status badge-readonly">🔒 Spectator (Read-Only)</span>
        <button id="btn-admin-key" class="action-btn key-btn">🔑 Unlock God Mode</button>
        <button id="btn-fever" class="action-btn fever-btn">🔥 Trigger Fever</button>
        <button id="btn-reset" class="action-btn">🔄 Reset Universe</button>
      </div>
    </div>
    
    <!-- 2-Tier Cloud Selector (Visible in Cloud Mode) -->
    <div class="selector-container" id="cloud-selector">
      <div class="realm-bar">
        <button class="realm-btn" data-realm="r1">🏛️ 1. Classic CA</button>
        <button class="realm-btn" data-realm="r2">🍂 2. Seasonal CA</button>
        <button class="realm-btn active" data-realm="r3">🌊 3. Lenia Waves</button>
        <button class="realm-btn" data-realm="r4">🧬 4. Turing Morph</button>
        <button class="realm-btn" data-realm="r5">⚡ 5. Wireworld</button>
        <button class="realm-btn" data-realm="r6">💨 6. Lattice Gas</button>
        <button class="realm-btn" data-realm="r7">⚔️ 7. Red Queen</button>
      </div>
      <div class="branch-bar">
        <button class="branch-btn active" data-branch="a">🟢 Universe A: Ancient (10 Pop)</button>
        <button class="branch-btn" data-branch="b">🟡 Universe B: Pioneers (Pruned)</button>
        <button class="branch-btn" data-branch="c">🔴 Universe C: Darwinian Colony (35 Pop)</button>
      </div>
    </div>

    <!-- In-Browser Sandbox Tools (Visible in Browser Mode) -->
    <div class="browser-tools" id="browser-tool-bar" style="display: none;">
      <span style="font-size:0.72rem; font-weight:700; color:#38bdf8;">🎨 Physics Substrate:</span>
      <select id="browser-substrate-select" class="tool-select">
        <option value="lenia">🌊 Continuous Lenia Solitons</option>
        <option value="turing">🧬 Gray-Scott Turing Reaction</option>
        <option value="wireworld">⚡ Wireworld Logic Circuits</option>
        <option value="conway">🏛️ Conway Discrete Life</option>
      </select>
      <span style="font-size:0.72rem; font-weight:700; color:#c084fc; margin-left:6px;">🖌️ Brush Tool:</span>
      <select id="browser-brush-select" class="tool-select">
        <option value="inject">✨ Inject Biomass / Catalyst</option>
        <option value="erase">🧹 Erase / Vacuum</option>
        <option value="wire">⚡ Lay Copper Conductor</option>
        <option value="head">🔵 Inject Electron Head</option>
      </select>
      <button id="btn-browser-fever" class="action-btn fever-btn">🔥 Local Fever</button>
      <button id="btn-browser-reset" class="action-btn">🔄 Clear Grid</button>
      <button id="btn-submit-discovery" class="action-btn submit-btn">🚀 Submit Discovered Law to Global Vault</button>
    </div>
  </header>

  <div class="main-grid">
    <!-- Left Column: Canvas & Substrate Telemetry -->
    <div class="card">
      <div class="card-title">
        <span id="canvas-label">🌊 Continuous Physics Canvas (25x25)</span>
        <span id="step-counter" style="color:#38bdf8; font-family:monospace;">Step: 000</span>
      </div>
      <div class="canvas-container">
        <canvas id="substrate-canvas" width="280" height="280"></canvas>
      </div>
      <div id="climate-card" style="font-size:0.68rem; color:#9ca3af; background:#030712; padding:5px; border-radius:5px; border:1px solid #1f2937;">
        <span id="climate-text">Loading telemetry...</span>
      </div>
    </div>

    <!-- Right Column: Agents, Laws & Event Stream -->
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <!-- Agent Telemetry -->
      <div class="card">
        <div class="card-title">
          <span>👥 Living Cognitive Society</span>
          <span id="telemetry-summary" style="color:#a78bfa; font-family:monospace;">Pop: 4</span>
        </div>
        <div style="max-height: 160px; overflow-y: auto;">
          <table class="telemetry-table">
            <thead>
              <tr>
                <th>Agent</th>
                <th>Pillar</th>
                <th>Pos</th>
                <th>Energy (H)</th>
                <th>dH/dt</th>
                <th>Temp</th>
                <th>10D</th>
                <th>Laws</th>
                <th>State</th>
              </tr>
            </thead>
            <tbody id="agent-tbody"></tbody>
          </table>
        </div>
      </div>

      <!-- Discovered Laws Archive -->
      <div class="card">
        <div class="card-title">
          <span>📜 Kolmogorov Discovered Laws (L(S_t^i))</span>
          <span id="sub-count" style="color:#ec4899; font-weight:bold;">0 Unique Laws</span>
        </div>
        <div id="subroutine-box" class="stream-box" style="height: 100px;">
          <div style="color:#6b7280;">Inducing verified causal transition laws from Step 0...</div>
        </div>
      </div>

      <!-- Message & Mitosis Stream -->
      <div class="card">
        <div class="card-title">
          <span>⚡ Relativistic Fabric (M_t^i) & Evolution Stream</span>
          <span id="msg-counter" style="color:#60a5fa;">0 Messages</span>
        </div>
        <div id="message-box" class="stream-box" style="height: 80px;"></div>
      </div>
    </div>
  </div>

  <script>
    let currentPlatformMode = "cloud"; // "cloud" or "browser"
    let activeRealm = "r3";
    let activeBranch = "a";
    let lastSubroutineKeys = "";
    let lastMessageCount = 0;
    let isFetching = false;
    let storedAdminKey = localStorage.getItem("sovereign_admin_key") || "";

    // Platform Mode Tabs
    const tabCloud = document.getElementById("tab-cloud-mode");
    const tabBrowser = document.getElementById("tab-browser-mode");
    const cloudSelector = document.getElementById("cloud-selector");
    const browserToolBar = document.getElementById("browser-tool-bar");
    const headerActionGroup = document.getElementById("header-action-group");
    const statusTag = document.getElementById("platform-status-tag");

    tabCloud.onclick = () => {
      currentPlatformMode = "cloud";
      tabCloud.classList.add("active");
      tabBrowser.classList.remove("active");
      cloudSelector.style.display = "flex";
      browserToolBar.style.display = "none";
      headerActionGroup.style.display = "flex";
      statusTag.innerText = "⚡ Live Synchronized Stream";
      fetchStateImmediate();
    };

    tabBrowser.onclick = () => {
      currentPlatformMode = "browser";
      tabBrowser.classList.add("active");
      tabCloud.classList.remove("active");
      cloudSelector.style.display = "none";
      browserToolBar.style.display = "flex";
      headerActionGroup.style.display = "none";
      statusTag.innerText = "💻 In-Browser 60 FPS Web Engine (Client-Side)";
      initBrowserPhysics();
    };

    // --- CLOUD ENGINE AUTH & SYNC ---
    function updateAdminUI() {
      const badge = document.getElementById("admin-badge");
      const keyBtn = document.getElementById("btn-admin-key");
      if (storedAdminKey) {
        badge.className = "badge-status badge-admin";
        badge.innerText = "👑 GOD MODE (Owner)";
        keyBtn.innerText = "🔒 Lock God Mode";
      } else {
        badge.className = "badge-status badge-readonly";
        badge.innerText = "🔒 Spectator (Read-Only)";
        keyBtn.innerText = "🔑 Unlock God Mode";
      }
    }

    document.getElementById("btn-admin-key").onclick = async () => {
      if (storedAdminKey) {
        storedAdminKey = "";
        localStorage.removeItem("sovereign_admin_key");
        updateAdminUI();
        alert("🔒 God Mode Locked. You are now in Read-Only Spectator Mode.");
      } else {
        const inputKey = prompt("🔑 Enter Sovereign Master Key to unlock God Mode:");
        if (!inputKey) return;
        try {
          const res = await fetch("/api/action/verify_admin", {
            method: "POST",
            headers: { "X-Admin-Key": inputKey.trim() }
          });
          if (res.ok) {
            storedAdminKey = inputKey.trim();
            localStorage.setItem("sovereign_admin_key", storedAdminKey);
            updateAdminUI();
            alert("👑 God Mode Unlocked! You now have exclusive intervention authority.");
          } else {
            alert("❌ Invalid Master Key. Access Denied.");
          }
        } catch (e) {
          alert("Error verifying key: " + e);
        }
      }
    };

    updateAdminUI();

    document.querySelectorAll(".realm-btn").forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll(".realm-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeRealm = btn.getAttribute("data-realm");
        lastSubroutineKeys = "";
        fetchStateImmediate();
      };
    });

    document.querySelectorAll(".branch-btn").forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll(".branch-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeBranch = btn.getAttribute("data-branch");
        lastSubroutineKeys = "";
        fetchStateImmediate();
      };
    });

    function getActiveUniverseKey() {
      return `${activeRealm}_${activeBranch}`;
    }

    async function fetchStateImmediate() {
      isFetching = false;
      await fetchState();
    }

    async function fetchState() {
      if (currentPlatformMode !== "cloud") return;
      if (isFetching) return;
      isFetching = true;
      try {
        const uKey = getActiveUniverseKey();
        const res = await fetch(`/api/state?u=${uKey}`);
        if (!res.ok) return;
        const data = await res.json();
        renderDashboard(data);
      } catch (err) {
        console.error("Fetch error:", err);
      } finally {
        isFetching = false;
      }
    }

    function renderDashboard(data) {
      if (!data || !data.grid) return;
      
      document.getElementById("universe-subtitle").innerText = `${data.mode_name} | ${data.substrate_name} | Vault: ${data.cloud_vault}`;
      document.getElementById("step-counter").innerText = `Step: ${data.step.toLocaleString()}`;
      document.getElementById("canvas-label").innerText = `${data.climate.season_icon || '🌌'} ${data.climate.environment_name}`;
      
      const c = data.climate || {};
      document.getElementById("climate-text").innerHTML = `
        <strong>${c.season_icon || '🌌'} ${c.season || 'Active'}</strong> | 
        Biomass: <span style="color:#38bdf8;">${c.total_biomass || 0}</span> | 
        Ambient Temp: <span style="color:#f87171;">${c.ambient_temp || 1.0}</span> | 
        Max Density: <span>${c.max_density || 1.0}</span>
      `;

      const canvas = document.getElementById("substrate-canvas");
      const ctx = canvas.getContext("2d");
      const grid = data.grid;
      const h = grid.length;
      const w = grid[0].length;
      const cellW = canvas.width / w;
      const cellH = canvas.height / h;

      ctx.fillStyle = "#000000";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      for (let r = 0; r < h; r++) {
        for (let col = 0; col < w; col++) {
          const val = grid[r][col];
          if (val > 0.01) {
            if (activeRealm === "r5") {
              if (val === 1) ctx.fillStyle = "#38bdf8";
              else if (val === 2) ctx.fillStyle = "#ef4444";
              else if (val === 3) ctx.fillStyle = "#eab308";
            } else if (activeRealm === "r4") {
              const g = Math.floor(val * 255);
              ctx.fillStyle = `rgb(${Math.floor(val * 100)}, ${g}, ${255 - g})`;
            } else if (activeRealm === "r7") {
              if (val >= 0.9) ctx.fillStyle = "#ef4444";
              else if (val >= 0.5) ctx.fillStyle = "#38bdf8";
              else ctx.fillStyle = `rgba(34, 197, 94, ${val})`;
            } else if (activeRealm === "r6") {
              ctx.fillStyle = `rgba(56, 189, 248, ${val})`;
            } else if (activeRealm === "r2") {
              ctx.fillStyle = val === 1 ? "#22c55e" : (val === 2 ? "#eab308" : "#a855f7");
            } else {
              const intensity = Math.min(1.0, val);
              const b = Math.floor(intensity * 255);
              const g = Math.floor(intensity * 200);
              ctx.fillStyle = `rgb(0, ${g}, ${b})`;
            }
            ctx.fillRect(col * cellW, r * cellH, cellW, cellH);
          }
        }
      }

      (data.nodes || []).forEach(node => {
        const [py, px] = node.pos;
        const cx = px * cellW + cellW / 2;
        const cy = py * cellH + cellH / 2;

        let col = "#38bdf8";
        if (node.pillar.includes("Quantum")) col = "#c084fc";
        else if (node.pillar.includes("Modern")) col = "#facc15";
        else if (node.pillar.includes("String")) col = "#f43f5e";
        else if (node.pillar.includes("Hybrid")) col = "#34d399";

        ctx.beginPath();
        ctx.arc(cx, cy, cellW * 0.75, 0, Math.PI * 2);
        ctx.fillStyle = col;
        ctx.fill();
        ctx.strokeStyle = node.fever ? "#dc2626" : "#ffffff";
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 9px monospace";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(node.id.substring(0, 2).toUpperCase(), cx, cy);
      });

      const tbody = document.getElementById("agent-tbody");
      tbody.innerHTML = (data.nodes || []).map(node => {
        let tagCls = "tag-classical";
        if (node.pillar.includes("Quantum")) tagCls = "tag-quantum";
        else if (node.pillar.includes("Modern")) tagCls = "tag-modern";
        else if (node.pillar.includes("String")) tagCls = "tag-string";
        else if (node.pillar.includes("Hybrid")) tagCls = "tag-hybrid";

        const feverBadge = node.fever ? `<span class="fever-badge fever-on">🔥 FEVER</span>` : `<span class="fever-badge fever-off">❄️ STABLE</span>`;
        return `
          <tr>
            <td><span class="agent-tag ${tagCls}">${node.id}</span></td>
            <td>${node.pillar}</td>
            <td>(${node.pos[0]}, ${node.pos[1]})</td>
            <td>${node.energy.toFixed(1)}</td>
            <td>${node.dh_dt >= 0 ? '+' : ''}${node.dh_dt.toFixed(2)}</td>
            <td>${node.temperature.toFixed(2)}</td>
            <td>D${node.dim_10d}</td>
            <td>${node.sub_count}</td>
            <td>${feverBadge}</td>
          </tr>
        `;
      }).join("");

      document.getElementById("telemetry-summary").innerText = `Pop: ${data.population}`;

      const subs = data.subroutines || [];
      const currentKeys = subs.map(s => s.signature).join(",");
      if (currentKeys !== lastSubroutineKeys) {
        lastSubroutineKeys = currentKeys;
        const count = data.total_laws !== undefined ? data.total_laws : subs.length;
        document.getElementById("sub-count").innerText = `${count} Discovered Laws`;
        const subBox = document.getElementById("subroutine-box");
        if (subs.length > 0) {
          subBox.innerHTML = subs.map(item => `
            <div class="stream-line sub" style="border-bottom: 1px solid #1f2937; padding-bottom: 3px; margin-bottom: 3px;">
              <span style="font-weight:bold; color:#ec4899;">• [${item.signature}]</span>
              <pre>${item.code}</pre>
            </div>
          `).join("");
        } else {
          subBox.innerHTML = "<div style='color:#6b7280;'>Inducing verified causal transition laws from Step 0...</div>";
        }
      }

      const msgCount = (data.events ? (data.events.prunings?.length || 0) + (data.events.births?.length || 0) : 0) + (data.messages?.length || 0);
      if (msgCount !== lastMessageCount) {
        lastMessageCount = msgCount;
        const msgBox = document.getElementById("message-box");
        let lines = [];
        if (data.events && data.events.prunings) {
          data.events.prunings.forEach(p => lines.push(`<div class="stream-line prune">${p}</div>`));
        }
        if (data.events && data.events.births) {
          data.events.births.forEach(b => lines.push(`<div class="stream-line mitosis">${b}</div>`));
        }
        if (data.messages && data.messages.length > 0) {
          data.messages.forEach(m => {
            const cls = m.includes("fever") ? "fever" : (m.includes("subroutine") ? "sub" : "grad");
            lines.push(`<div class="stream-line ${cls}">[M_t^i] ${m}</div>`);
          });
        }
        msgBox.innerHTML = lines.join("");
      }
    }

    async function sendAdminAction(endpoint) {
      if (!storedAdminKey) {
        alert("⛔ Access Denied: God Mode is locked. Enter your Sovereign Master Key first.");
        return;
      }
      try {
        const res = await fetch(`${endpoint}?u=${getActiveUniverseKey()}`, {
          method: "POST",
          headers: { "X-Admin-Key": storedAdminKey }
        });
        const data = await res.json();
        if (res.status === 403) {
          alert("⛔ Unauthorized: " + (data.error || "Invalid Admin Key"));
        }
      } catch (err) {
        alert("Action Error: " + err);
      }
    }

    document.getElementById("btn-fever").onclick = () => sendAdminAction("/api/action/fever");
    document.getElementById("btn-reset").onclick = () => sendAdminAction("/api/action/reset");

    setInterval(fetchState, 140);
    fetchState();


    // =========================================================================
    // IN-BROWSER CLIENT-SIDE SIMULATION ENGINE (100% LOCAL DEVICE COMPUTATION)
    // =========================================================================
    const B_GRID_SIZE = 25;
    let b_grid = Array.from({ length: B_GRID_SIZE }, () => new Float32Array(B_GRID_SIZE));
    let b_u = Array.from({ length: B_GRID_SIZE }, () => new Float32Array(B_GRID_SIZE).fill(1.0));
    let b_v = Array.from({ length: B_GRID_SIZE }, () => new Float32Array(B_GRID_SIZE));
    let b_step = 0;
    let b_agents = [
      { id: "local_pioneer_1", pillar: "Classical-Eikonal", pos: [5, 5], energy: 100.0, temp: 1.0, laws: [] },
      { id: "local_pioneer_2", pillar: "Quantum-Superposed", pos: [20, 5], energy: 100.0, temp: 1.0, laws: [] },
      { id: "local_pioneer_3", pillar: "Modern-Thermodynamic", pos: [5, 20], energy: 100.0, temp: 1.0, laws: [] },
      { id: "local_pioneer_4", pillar: "String-Topological", pos: [20, 20], energy: 100.0, temp: 1.0, laws: [] }
    ];
    let b_discoveredLaws = {};
    let isPainting = false;

    function initBrowserPhysics() {
      b_step = 0;
      const subType = document.getElementById("browser-substrate-select").value;
      for (let r = 0; r < B_GRID_SIZE; r++) {
        for (let c = 0; c < B_GRID_SIZE; c++) {
          if (subType === "lenia") {
            b_grid[r][c] = (Math.random() < 0.25) ? Math.random() * 0.8 : 0.0;
          } else if (subType === "turing") {
            b_u[r][c] = 1.0;
            b_v[r][c] = (r >= 10 && r <= 14 && c >= 10 && c <= 14) ? 0.35 : 0.0;
            b_grid[r][c] = b_v[r][c];
          } else if (subType === "wireworld") {
            b_grid[r][c] = (r % 4 === 0 || c % 4 === 0) ? 3 : 0;
          } else {
            b_grid[r][c] = (Math.random() < 0.20) ? 1 : 0;
          }
        }
      }
      if (subType === "wireworld") {
        b_grid[4][5] = 1;
        b_grid[4][4] = 2;
      }
      document.getElementById("universe-subtitle").innerText = `💻 Local In-Browser Laboratory | Substrate: ${subType} | Running on your device at 60 FPS`;
    }

    document.getElementById("browser-substrate-select").onchange = initBrowserPhysics;

    document.getElementById("btn-browser-reset").onclick = () => {
      for (let r = 0; r < B_GRID_SIZE; r++) {
        b_grid[r].fill(0);
        b_v[r].fill(0);
        b_u[r].fill(1.0);
      }
      b_step = 0;
    };

    document.getElementById("btn-browser-fever").onclick = () => {
      b_agents.forEach(a => {
        a.temp = 3.0;
        a.energy = Math.min(200, a.energy + 50);
      });
      // Spontaneously inject high-energy reaction spots
      for (let i = 0; i < 5; i++) {
        const ry = Math.floor(Math.random() * B_GRID_SIZE);
        const rx = Math.floor(Math.random() * B_GRID_SIZE);
        b_grid[ry][rx] = 1.0;
        b_v[ry][rx] = 0.8;
      }
    };

    // Canvas Interactive Painting Tool
    const canvas = document.getElementById("substrate-canvas");
    function handleCanvasDraw(e) {
      if (currentPlatformMode !== "browser") return;
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const col = Math.floor((x / canvas.width) * B_GRID_SIZE);
      const row = Math.floor((y / canvas.height) * B_GRID_SIZE);
      if (row < 0 || row >= B_GRID_SIZE || col < 0 || col >= B_GRID_SIZE) return;

      const brush = document.getElementById("browser-brush-select").value;
      if (brush === "inject") {
        b_grid[row][col] = 1.0;
        b_v[row][col] = 0.60;
        b_u[row][col] = 0.40;
      } else if (brush === "erase") {
        b_grid[row][col] = 0.0;
        b_v[row][col] = 0.0;
        b_u[row][col] = 1.0;
      } else if (brush === "wire") {
        b_grid[row][col] = 3.0;
      } else if (brush === "head") {
        b_grid[row][col] = 1.0;
      }
    }

    canvas.onmousedown = (e) => { isPainting = true; handleCanvasDraw(e); };
    window.onmouseup = () => { isPainting = false; };
    canvas.onmousemove = (e) => { if (isPainting) handleCanvasDraw(e); };

    // In-Browser Physics Step Loop (60 FPS)
    function stepBrowserPhysics() {
      if (currentPlatformMode === "browser") {
        b_step++;
        const subType = document.getElementById("browser-substrate-select").value;
        const nextGrid = Array.from({ length: B_GRID_SIZE }, () => new Float32Array(B_GRID_SIZE));

        if (subType === "lenia" || subType === "conway") {
          for (let r = 0; r < B_GRID_SIZE; r++) {
            for (let c = 0; c < B_GRID_SIZE; c++) {
              let neighbors = 0;
              for (let dr = -1; dr <= 1; dr++) {
                for (let dc = -1; dc <= 1; dc++) {
                  if (dr === 0 && dc === 0) continue;
                  const nr = (r + dr + B_GRID_SIZE) % B_GRID_SIZE;
                  const nc = (c + dc + B_GRID_SIZE) % B_GRID_SIZE;
                  neighbors += b_grid[nr][nc] >= 0.25 ? 1 : 0;
                }
              }
              if (b_grid[r][c] >= 0.25) {
                nextGrid[r][c] = (neighbors === 2 || neighbors === 3) ? Math.min(1.0, b_grid[r][c] + 0.02) : 0.0;
              } else {
                nextGrid[r][c] = (neighbors === 3) ? 0.8 : 0.0;
              }
            }
          }
          b_grid = nextGrid;
        } else if (subType === "turing") {
          // Gray Scott continuous PDE
          const Du = 0.16, Dv = 0.08, F = 0.035, k = 0.065;
          const nextU = Array.from({ length: B_GRID_SIZE }, () => new Float32Array(B_GRID_SIZE));
          const nextV = Array.from({ length: B_GRID_SIZE }, () => new Float32Array(B_GRID_SIZE));
          for (let r = 0; r < B_GRID_SIZE; r++) {
            for (let c = 0; c < B_GRID_SIZE; c++) {
              const u = b_u[r][c], v = b_v[r][c];
              const lapU = (b_u[(r+1)%B_GRID_SIZE][c] + b_u[(r-1+B_GRID_SIZE)%B_GRID_SIZE][c] + b_u[r][(c+1)%B_GRID_SIZE] + b_u[r][(c-1+B_GRID_SIZE)%B_GRID_SIZE] - 4*u);
              const lapV = (b_v[(r+1)%B_GRID_SIZE][c] + b_v[(r-1+B_GRID_SIZE)%B_GRID_SIZE][c] + b_v[r][(c+1)%B_GRID_SIZE] + b_v[r][(c-1+B_GRID_SIZE)%B_GRID_SIZE] - 4*v);
              const uvv = u * v * v;
              nextU[r][c] = Math.max(0, Math.min(1, u + (Du * lapU - uvv + F * (1 - u))));
              nextV[r][c] = Math.max(0, Math.min(1, v + (Dv * lapV + uvv - (F + k) * v)));
              b_grid[r][c] = nextV[r][c];
            }
          }
          b_u = nextU;
          b_v = nextV;
        } else if (subType === "wireworld") {
          for (let r = 0; r < B_GRID_SIZE; r++) {
            for (let c = 0; c < B_GRID_SIZE; c++) {
              const state = b_grid[r][c];
              if (state === 1) nextGrid[r][c] = 2; // Head -> Tail
              else if (state === 2) nextGrid[r][c] = 3; // Tail -> Conductor
              else if (state === 3) {
                let headCount = 0;
                for (let dr = -1; dr <= 1; dr++) {
                  for (let dc = -1; dc <= 1; dc++) {
                    if (dr === 0 && dc === 0) continue;
                    const nr = (r + dr + B_GRID_SIZE) % B_GRID_SIZE;
                    const nc = (c + dc + B_GRID_SIZE) % B_GRID_SIZE;
                    if (b_grid[nr][nc] === 1) headCount++;
                  }
                }
                nextGrid[r][c] = (headCount === 1 || headCount === 2) ? 1 : 3;
              } else nextGrid[r][c] = 0;
            }
          }
          b_grid = nextGrid;
        }

        // Local Agent Stepping & Kolmogorov Induction
        b_agents.forEach(a => {
          const [py, px] = a.pos;
          const val = b_grid[py][px];
          a.energy += (val > 0.2 ? val * 4.0 : -0.2);
          a.temp = Math.max(1.0, a.temp - 0.01);
          // Random walk / gradient ascent
          const moves = [[0, 1], [0, -1], [1, 0], [-1, 0]];
          const m = moves[Math.floor(Math.random() * moves.length)];
          a.pos[0] = (py + m[0] + B_GRID_SIZE) % B_GRID_SIZE;
          a.pos[1] = (px + m[1] + B_GRID_SIZE) % B_GRID_SIZE;

          // Local in-browser rule discovery
          if (b_step % 25 === 0 && val > 0.3) {
            const sig = `browser_law_${subType}_${Math.floor(val * 10)}`;
            if (!b_discoveredLaws[sig]) {
              b_discoveredLaws[sig] = `def rule_${subType}_local(field):\n    # Locally synthesized by ${a.id}\n    return field * ${val.toFixed(2)}`;
            }
          }
        });

        // Render In-Browser Dashboard
        const payload = {
          mode_name: `💻 In-Browser Sandbox [${subType.toUpperCase()}]`,
          substrate_name: `Local JS Web Physics (${subType})`,
          cloud_vault: "Local Client Memory (Zero Cloud Load)",
          step: b_step,
          population: b_agents.length,
          climate: {
            season: "Interactive Player Sandbox",
            season_icon: "🎨",
            total_biomass: b_grid.reduce((acc, row) => acc + row.reduce((rAcc, v) => rAcc + v, 0), 0).toFixed(1),
            ambient_temp: 1.0,
            max_density: 1.0
          },
          grid: b_grid.map(row => Array.from(row)),
          nodes: b_agents.map(a => ({
            id: a.id,
            pillar: a.pillar,
            pos: a.pos,
            energy: a.energy,
            temperature: a.temp,
            viscosity: 0.1,
            dh_dt: 0.05,
            fever: a.temp > 1.8,
            entropy: 0.2,
            sub_count: Object.keys(b_discoveredLaws).length,
            dim_10d: 10
          })),
          subroutines: Object.entries(b_discoveredLaws).map(([k, v]) => ({ signature: k, code: v })),
          messages: [`[Local Engine] Step ${b_step} computed on device at 60 FPS`],
          events: { births: [], mergers: [], prunings: [] }
        };
        renderDashboard(payload);
      }
      requestAnimationFrame(stepBrowserPhysics);
    }

    requestAnimationFrame(stepBrowserPhysics);

    // Submit Local Discovery to Global Vault
    document.getElementById("btn-submit-discovery").onclick = async () => {
      const laws = Object.entries(b_discoveredLaws);
      if (laws.length === 0) {
        alert("🔍 No local laws discovered yet. Let your browser sandbox run or paint active spots to discover rules!");
        return;
      }
      const [sig, code] = laws[laws.length - 1];
      const author = prompt("Enter your Pioneer name / alias to sign this discovery:", "Player 1") || "Anonymous Pioneer";
      try {
        const res = await fetch("/api/submit_discovery", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            signature: sig,
            code_str: code,
            description: `In-browser discovery from ${author}`,
            realm: document.getElementById("browser-substrate-select").value,
            author: author,
            step_discovered: b_step
          })
        });
        const data = await res.json();
        alert(`🚀 Discovery [${sig}] successfully synced to Global Cloud Vault!\nTotal Community Discoveries: ${data.total_community_discoveries}`);
      } catch (err) {
        alert("Sync error: " + err);
      }
    };
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=HTML_CONTENT)
