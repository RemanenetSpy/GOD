"""
================================================================================
BINORYLOGY 2.0 — 24/7 LIVE RENDER SERVER WITH HUGGING FACE IMMORTAL STORAGE
================================================================================
Sovereign Physics Cognitive Architecture running 24/7 on Render.
- 4 Cognitive Agents with 6-Engine Bodies learning physics Tier 1 -> Tier 6
- Hugging Face Dataset Memory Vault (immortal across Render ephemeral restarts)
- Interactive Live HTML Dashboard with real-time physics telemetry & discovered laws
- Zero-lock high-performance state caching & UptimeRobot /ping support
================================================================================
"""

import os
import sys
import time
import json
import threading
import math
import numpy as np
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Response, Header
from fastapi.responses import HTMLResponse, JSONResponse

# ── Path setup ──────────────────────────────────────────────────────────────
_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_DIR, "src")
for p in [_DIR, _SRC]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ── Load local .env if present ──────────────────────────────────────────────
_env_file = os.path.join(_DIR, ".env")
if os.path.exists(_env_file):
    try:
        with open(_env_file, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    if k not in os.environ:
                        os.environ[k] = v
    except Exception as e:
        print(f"[Env Loader] Warning reading .env: {e}")

HF_TOKEN = os.environ.get("HF_TOKEN", "")
env_repo = os.environ.get("HF_DATASET_REPO", "")
if not env_repo or "sovereign-civilization-memory" in env_repo:
    HF_REPO = "Explorerp/binorylogy-physics-memory"
else:
    HF_REPO = env_repo
ADMIN_KEY = os.environ.get("ADMIN_SECRET_KEY", "sovereign-master-2026")

# ── HF Dataset Vault ────────────────────────────────────────────────────────
from hf_vault import BinoryHFVault
vault = BinoryHFVault(repo_id=HF_REPO, token=HF_TOKEN, local_cache_dir=os.path.join(_DIR, "data"))

# ── Core BinoryLogy Engine Imports ──────────────────────────────────────────
from pathlib import Path
from binory_core import BinoryCore, make_node_id, register_name, readable
from binory_physics_stream import PhysicsStreamGenerator, PhysicsTier
from binory_curriculum import AdaptiveCurriculum
from binory_agents import SovereignCivilization

DATA_DIR = Path(vault.local_cache_dir)
DATA_DIR.mkdir(exist_ok=True)
STATE_PATH = DATA_DIR / "binory_state.json"
LOG_PATH = DATA_DIR / "binory_log.txt"

core = BinoryCore(STATE_PATH, LOG_PATH)
stream_gen = PhysicsStreamGenerator()
curriculum = AdaptiveCurriculum()
civilization = SovereignCivilization(grid_shape=(8, 8))

STATE_LOCK = threading.Lock()
LIVE_STATE: Dict[str, Any] = {}
DISCOVERY_LOG: List[Dict] = []
TOTAL_STEPS = 0

# ── Restore from Hugging Face Cloud Vault on Startup ────────────────────────
def _restore_from_vault():
    global DISCOVERY_LOG, TOTAL_STEPS
    saved = vault.load("binory_checkpoint.json")
    if not saved:
        print("[BinoryVault] Fresh genesis - starting from Tier 1.")
        curriculum._current_tier = PhysicsTier.TIER1_SENSORIMOTOR
        TOTAL_STEPS = 0
        core._step = 0
        return
    try:
        tier_val = saved.get("tier", 1)
        curriculum._current_tier = PhysicsTier(tier_val)
        DISCOVERY_LOG = saved.get("discoveries", [])
        TOTAL_STEPS = saved.get("step", 0)
        core._step = TOTAL_STEPS
        for c, m in saved.get("concept_mastery", {}).items():
            if c in curriculum.pkg._nodes:
                curriculum.pkg._nodes[c].mastery = float(m)
        print(f"[BinoryVault] Restored from HF: Step {TOTAL_STEPS}, Tier {tier_val}, {len(DISCOVERY_LOG)} discoveries")
    except Exception as e:
        print(f"[BinoryVault] Checkpoint restore warning: {e}")

_restore_from_vault()

# ── Engine Loop Background Thread ───────────────────────────────────────────
_sample_interval = 0.5
_last_cloud_save = time.time()
CLOUD_SAVE_INTERVAL = 120.0  # 2 minutes = 30 commits/hour, well within HF 128/hr limit

def _cloud_save(step: int):
    try:
        cur_status = curriculum.status()
        state = {
            "step": step,
            "tier": int(curriculum.tier),
            "tier_name": curriculum.tier.name,
            "tier_mastery": {str(t): round(curriculum.pkg.tier_mastery(t), 4) for t in range(1, 7)},
            "concept_mastery": {c: round(n.mastery, 4) for c, n in curriculum.pkg._nodes.items()},
            "synapse_count": len(core._weights),
            "emerged_count": len(core._emerged),
            "discoveries": DISCOVERY_LOG[-250:],
            "top_synapses": [
                {"from": readable(a), "to": readable(b), "strength": round(w, 2)}
                for a, b, w in core.top_synapses(12)
            ],
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "hf_repo": HF_REPO
        }
        core.save_state()
        vault.save(
            state,
            filename="binory_checkpoint.json",
            commit_msg=f"BinoryLogy 2.0 Step {step} | Tier {int(curriculum.tier)}: {curriculum.tier.name}",
            async_upload=True
        )
        print(f"[BinoryLogy Cloud] Saved Step {step} (Tier {int(curriculum.tier)}) to {HF_REPO}")
    except Exception as e:
        print(f"[BinoryLogy Cloud Save Error]: {e}")

def _engine_loop():
    global _sample_interval, _last_cloud_save, TOTAL_STEPS
    step = core._step
    
    while True:
        try:
            step += 1
            TOTAL_STEPS = step
            
            # 1. Generate observation for current curriculum tier
            stream_gen.set_tier(curriculum.tier)
            obs = stream_gen.next()
            
            # 2. Build active signals from physical quantities
            active_nodes = []
            for var_name, val in obs.variables.items():
                nid = make_node_id(f"phys_{var_name}")
                register_name(nid, f"phys:{var_name}")
                if isinstance(val, (int, float)) and abs(val) > 1e-6:
                    active_nodes.append(nid)
                    
            # 3. Update Adaptive Causal STDP Core
            core_out = core.update(active_nodes, cpu_load=len(active_nodes) * 8.0)
            
            # 4. Sovereign Civilization Step — God Equation on all 4 Pillars
            pillar_snapshots = civilization.step(obs, curriculum)
            
            # 4b. Empirical Knowledge Ingestion & Consensus Tier Advancement
            curriculum.pkg.observe_empirical(obs.stream_type, obs.variables)
            if curriculum.check_advancement(n_agents=4):
                print(f"🎉 [TIER ADVANCEMENT] Sovereign Civilization ascended to Tier {int(curriculum.tier)}: {curriculum.tier.name} at Step {step}!")
                DISCOVERY_LOG.append({
                    "step": step,
                    "type": "tier_advancement",
                    "agent": "Sovereign-Council",
                    "concept": f"ASCENSION_TO_TIER_{int(curriculum.tier)}_{curriculum.tier.name}",
                    "equation": f"ConsensusMastery={curriculum.pkg.tier_mastery(int(curriculum.tier)-1):.2f}",
                    "time": time.strftime("%H:%M:%S")
                })

            # 5. Adapt simulation interval from civilization mean viscosity
            viscosities = [v.get("viscosity", 1.0) for v in pillar_snapshots.values()]
            mean_visc = sum(viscosities) / len(viscosities) if viscosities else 1.0
            _sample_interval = max(0.2, min(2.0, 0.8 / (1.0 + mean_visc)))

            # 6. Record newly emerged causal links
            for (a, b), (strength, te) in core_out.get("newly_emerged", {}).items():
                DISCOVERY_LOG.append({
                    "step": step,
                    "type": "causal_link",
                    "from": readable(a),
                    "to": readable(b),
                    "strength": round(strength, 2),
                    "te": round(te, 4),
                    "tier": int(curriculum.tier),
                    "time": time.strftime("%H:%M:%S")
                })

            # 7. Record curriculum law discoveries
            cur_status = curriculum.status()
            for disc in cur_status.get("recent_discoveries", []):
                if not any(d.get("concept") == disc.get("concept") and d.get("step") == disc.get("step") for d in DISCOVERY_LOG[-30:]):
                    disc["time"] = time.strftime("%H:%M:%S")
                    DISCOVERY_LOG.append(disc)

            # 8. Record Kolmogorov laws discovered by any Pillar node
            for nid, snap in pillar_snapshots.items():
                for law in civilization.nodes[nid]._discoveries:
                    if law["step"] == step:
                        entry = {
                            "step": step,
                            "type": "law",
                            "agent": snap["pillar"],
                            "concept": law.get("law", "unknown"),
                            "equation": f"gain={law.get('gain', 0):.2f}",
                            "time": time.strftime("%H:%M:%S")
                        }
                        if not any(d.get("concept") == entry["concept"] and d.get("step") == step for d in DISCOVERY_LOG[-30:]):
                            DISCOVERY_LOG.append(entry)

            # 9. Build agent cards from pillar snapshots (pillar name as id + role)
            agent_cards = []
            for nid, snap in pillar_snapshots.items():
                agent_cards.append({
                    "id":         snap["pillar"],           # e.g. "Classical-Eikonal"
                    "role":       snap["pillar"],
                    "temperature": snap.get("temperature", 0.1),
                    "energy":      snap.get("energy", 100.0),
                    "fever":       snap.get("fever", False),
                    "new_laws":    snap.get("subroutines", 0),
                    "belief_kl":   snap.get("belief_entropy", 0.0),
                    "dh_dt":       snap.get("dh_dt", 0.0),
                    "action":      snap.get("last_action", "OBSERVE"),
                    "discoveries": snap.get("discoveries", 0),
                    "cognitive_10d": snap.get("cognitive_10d", {}),
                })
                    
            with STATE_LOCK:
                LIVE_STATE.update({
                    "step": step,
                    "tier": int(curriculum.tier),
                    "tier_name": curriculum.tier.name,
                    "tier_mastery": round(cur_status["tier_mastery"], 3),
                    "emerge_threshold": round(core_out["emerge_threshold"], 3),
                    "tau_stdp": round(core_out["tau_stdp"], 4),
                    "decay": round(core_out["decay"], 6),
                    "synapse_count": core_out["synapse_count"],
                    "emerged_count": core_out["emerged_count"],
                    "top_links": [
                        {"from": readable(a), "to": readable(b), "strength": round(w, 2)}
                        for a, b, w in core.top_synapses(10)
                    ],
                    "agents": agent_cards,
                    "total_discoveries": len(DISCOVERY_LOG),
                    "recent_discoveries": DISCOVERY_LOG[-15:],
                    "frontier": cur_status.get("frontier", [])[:8],
                    "obs_stream": obs.stream_type,
                    "obs_tier": obs.tier,
                    "obs_vars": {k: round(float(v), 4) for k, v in list(obs.variables.items())[:6]},
                    "hf_repo": HF_REPO,
                    "connectome": civilization.get_connectome(),
                    "total_messages": civilization.total_messages_routed(),
                    "sample_interval": round(_sample_interval, 3),
                    "last_updated": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                })
                
            # 9. Cloud Periodic Persistence
            now = time.time()
            if now - _last_cloud_save >= CLOUD_SAVE_INTERVAL:
                _last_cloud_save = now
                _cloud_save(step)
                
        except Exception as e:
            print(f"[BinoryLogy Daemon Error at Step {step}]: {e}")
            
        time.sleep(_sample_interval)

_thread = threading.Thread(target=_engine_loop, daemon=True)
_thread.start()
print("[BinoryLogy 2.0] Engine loop initialized and running 24/7.")

# ── FastAPI App & Endpoints ─────────────────────────────────────────────────
app = FastAPI(title="BinoryLogy 2.0 Sovereign Physics Cognitive Architecture")

# ── ARC Sovereign Discovery Arena (Plug-in / Plug-out) ──────────────────────
try:
    from arc_sovereign_arena.router import arc_router, generate_arc_html_dashboard
    from arc_sovereign_arena.coordinator import SovereignArcCoordinator
    app.include_router(arc_router)
    arc_coordinator = SovereignArcCoordinator(civilization=civilization, vault=vault, core=core)
    arc_coordinator.start_background_loop()
    print("[ARC Sovereign Arena] Plugged into living civilization and active 24/7.")

    @app.get("/arc", response_class=HTMLResponse)
    def arc_ui_page():
        return HTMLResponse(content=generate_arc_html_dashboard())
except Exception as e:
    arc_coordinator = None
    print(f"[ARC Sovereign Arena] Plug-in notice: {e}")

@app.api_route("/ping", methods=["GET", "HEAD"])
def ping():
    return Response(content="PONG", media_type="text/plain")

@app.get("/api/health")
def health():
    return {
        "status": "alive",
        "system": "BinoryLogy 2.0 Sovereign Physics Engine",
        "step": TOTAL_STEPS,
        "tier": int(curriculum.tier),
        "cloud_vault": HF_REPO
    }

@app.get("/api/state")
def api_state():
    with STATE_LOCK:
        st = dict(LIVE_STATE)
        if "arc_coordinator" in globals() and arc_coordinator:
            st["arc_arena"] = arc_coordinator.get_telemetry()
        return JSONResponse(content=st)

@app.get("/api/discoveries")
def api_discoveries():
    return JSONResponse(content={"discoveries": DISCOVERY_LOG[-100:]})

@app.post("/api/action/fever")
def api_fever(x_admin_key: Optional[str] = Header(None)):
    if x_admin_key != ADMIN_KEY:
        return JSONResponse(status_code=403, content={"error": "Unauthorized. Master key required."})
    for node in civilization.nodes.values():
        if hasattr(node, "fever_engine") and hasattr(node.fever_engine, "temperature"):
            node.fever_engine.temperature = min(3.0, node.fever_engine.temperature + 1.5)
    return {"status": "FEVER_TRIGGERED_ALL_PILLARS"}

@app.post("/api/action/reset")
def api_reset(x_admin_key: Optional[str] = Header(None)):
    if x_admin_key != ADMIN_KEY:
        return JSONResponse(status_code=403, content={"error": "Unauthorized. Master key required."})
    curriculum._current_tier = PhysicsTier.TIER1_SENSORIMOTOR
    curriculum._agent_votes.clear()
    core._weights.clear()
    core._emerged.clear()
    return {"status": "UNIVERSE_RESET_GENESIS", "tier": 1}

@app.post("/api/admin/save")
def api_save(x_admin_key: Optional[str] = Header(None)):
    if x_admin_key != ADMIN_KEY:
        return JSONResponse(status_code=403, content={"error": "Unauthorized."})
    _cloud_save(TOTAL_STEPS)
    return {"status": "SAVED_TO_CLOUD", "step": TOTAL_STEPS, "repo": HF_REPO}

@app.post("/api/admin/advance-tier")
def api_advance(x_admin_key: Optional[str] = Header(None)):
    if x_admin_key != ADMIN_KEY:
        return JSONResponse(status_code=403, content={"error": "Unauthorized."})
    cur = int(curriculum.tier)
    if cur < 6:
        curriculum._current_tier = PhysicsTier(cur + 1)
        curriculum._agent_votes.clear()
        return {"status": "TIER_ADVANCED", "tier": int(curriculum.tier)}
    return {"status": "ALREADY_MAX_TIER", "tier": 6}

# ── High-Performance Real-Time Web Dashboard ────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def dashboard():
    with STATE_LOCK:
        s = dict(LIVE_STATE)

    tier = s.get("tier", 1)
    tier_name = s.get("tier_name", "TIER1_SENSORIMOTOR")
    mastery = s.get("tier_mastery", 0.0)
    step = s.get("step", 0)
    total_disc = s.get("total_discoveries", 0)
    threshold = s.get("emerge_threshold", 0.0)
    synapse_count = s.get("synapse_count", 0)
    emerged_count = s.get("emerged_count", 0)

    tier_descriptions = {
        1: "Grade 1-5: Sensorimotor Kinematics (v = dx/dt, y = y0 + v0*t - 0.5*g*t^2, F = mg)",
        2: "Grade 6-8: Algebraic Continuum (P = F/A, V = IR, v_wave = f * lambda, P = IV)",
        3: "Grade 9-12: Classical Vectors & Thermodynamics (F = ma, p = mv, Hooke's Law, dU = Q - W)",
        4: "Undergraduate: Analytical Mechanics & Fields (Lagrangian L = T - V, Hamiltonian H, Maxwell, Z)",
        5: "Modern Physics: Quantum Mechanics & Special Relativity (Schrodinger Eq, Born Rule, Lorentz ds^2)",
        6: "MIT Graduate: Field Theories & Gravitation (Einstein Field Eq, Path Integrals, Yang-Mills, BCS)"
    }

    tier_badges_html = ""
    for t in range(1, 7):
        active_cls = "active" if t == tier else ("completed" if t < tier else "locked")
        tier_badges_html += f'<span class="tier-pill {active_cls}">T{t}</span>'

    agents_html = ""
    for ag in s.get("agents", []):
        fever_cls = "fever" if ag.get("fever") else ""
        agents_html += f"""
        <div class="agent-card {fever_cls}">
          <div class="agent-header">
            <span class="agent-id">{ag.get('id', '?')}</span>
            <span class="agent-role">{'🔥 FEVER' if ag.get('fever') else ag.get('action', 'OBSERVE')}</span>
          </div>
          <div class="agent-metrics">
            <div><span class="lbl">Temp:</span> <span class="val">{ag.get('temperature', 0):.3f}</span></div>
            <div><span class="lbl">Energy:</span> <span class="val">{ag.get('energy', 100):.0f}</span></div>
            <div><span class="lbl">dH/dt:</span> <span class="val">{ag.get('dh_dt', 0.0):.4f}</span></div>
            <div><span class="lbl">Belief Entropy:</span> <span class="val">{ag.get('belief_kl', 0):.4f}</span></div>
            <div><span class="lbl">Subroutines:</span> <span class="val highlight">{ag.get('new_laws', 0)}</span></div>
            <div><span class="lbl">Discoveries:</span> <span class="val highlight">{ag.get('discoveries', 0)}</span></div>
          </div>
          {'<div class="fever-alert">🔥 FEVER ACTIVE — Stochastic Brownian Walk</div>' if ag.get('fever') else ''}
        </div>"""

    links_html = ""
    for lk in s.get("top_links", []):
        links_html += f"""
        <div class="link-item">
          <span class="link-node from">{lk['from']}</span>
          <span class="link-arrow">⟶</span>
          <span class="link-node to">{lk['to']}</span>
          <span class="link-weight">+{lk['strength']:.1f}</span>
        </div>"""

    connectome_html = ""
    for edge in s.get("connectome", [])[:10]:
        is_emerged = edge.get("emerged", False)
        status_tag = '<span class="tag link-tag" style="background:#059669;color:#a7f3d0">AXON</span>' if is_emerged else '<span class="tag link-tag" style="background:#1e293b;color:#94a3b8">SYNAPSE</span>'
        src_clean = edge.get('from', '').replace('_prime', '').replace('_meta', '')
        dst_clean = edge.get('to', '').replace('_prime', '').replace('_meta', '')
        connectome_html += f"""
        <div class="link-item">
          {status_tag}
          <span class="link-node from" style="width:80px;">{src_clean}</span>
          <span class="link-arrow">⟶</span>
          <span class="link-node to" style="width:80px;">{dst_clean}</span>
          <span class="link-weight" style="color:var(--accent);">W={edge.get('weight', 0):.1f}</span>
        </div>"""

    disc_html = ""
    for d in reversed(s.get("recent_discoveries", [])):
        dtype = d.get("type", "discovery")
        if dtype == "causal_link":
            disc_html += f"""<div class="disc-item causal">
              <span class="time">[{d.get('time', '')}]</span>
              <span class="tag link-tag">CAUSAL</span>
              <span class="desc">{d.get('from', '')} ⟶ {d.get('to', '')}</span>
              <span class="te">TE={d.get('te', 0):.4f}</span>
            </div>"""
        else:
            disc_html += f"""<div class="disc-item law">
              <span class="time">[{d.get('time', '')}]</span>
              <span class="tag law-tag">LAW</span>
              <span class="agent">[{d.get('agent', '')}]</span>
              <span class="concept">{d.get('concept', '')}</span>
              <span class="eq">{d.get('equation', '')}</span>
            </div>"""

    obs_vars = s.get("obs_vars", {})
    obs_pills = "".join([f'<span class="telemetry-pill"><b>{k}</b>: {v}</span>' for k, v in obs_vars.items()])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="2">
<title>BinoryLogy 2.0 — Sovereign Physics Cognitive Architecture</title>
<style>
  :root {{
    --bg: #07090e;
    --card-bg: #0c1017;
    --border: #1a2333;
    --accent: #00ff88;
    --accent-glow: rgba(0, 255, 136, 0.2);
    --cyan: #00d8ff;
    --warn: #ffaa00;
    --danger: #ff3366;
    --text: #e2e8f0;
    --text-muted: #64748b;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 12px;
    padding: 16px;
    line-height: 1.5;
  }}
  header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
    margin-bottom: 16px;
  }}
  h1 {{
    font-size: 18px;
    color: var(--accent);
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .badge-live {{
    background: #004d2b;
    color: var(--accent);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 10px;
    font-weight: bold;
    animation: blink 2s infinite;
  }}
  @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 16px;
  }}
  .col-4 {{ grid-column: span 4; }}
  .col-8 {{ grid-column: span 8; }}
  .col-6 {{ grid-column: span 6; }}
  .col-12 {{ grid-column: span 12; }}
  @media (max-width: 900px) {{
    .col-4, .col-8, .col-6 {{ grid-column: span 12; }}
  }}
  .card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
  }}
  .card-title {{
    font-size: 12px;
    color: var(--cyan);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .tier-banner {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
  }}
  .tier-pill {{
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: bold;
    background: #1e293b;
    color: #94a3b8;
  }}
  .tier-pill.active {{
    background: var(--accent);
    color: #000;
    box-shadow: 0 0 8px var(--accent-glow);
  }}
  .tier-pill.completed {{
    background: #065f46;
    color: #a7f3d0;
  }}
  .mastery-outer {{
    height: 8px;
    background: #1e293b;
    border-radius: 4px;
    overflow: hidden;
    margin: 8px 0;
  }}
  .mastery-fill {{
    height: 100%;
    background: linear-gradient(90deg, #059669, var(--accent));
    transition: width 0.4s ease;
  }}
  .stat-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-top: 10px;
  }}
  .stat-box {{
    background: #090d14;
    border: 1px solid #141c2b;
    border-radius: 4px;
    padding: 8px;
  }}
  .stat-box .k {{ color: var(--text-muted); font-size: 10px; }}
  .stat-box .v {{ color: var(--text); font-size: 14px; font-weight: bold; }}
  .agent-list {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }}
  .agent-card {{
    background: #090d14;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px;
  }}
  .agent-card.fever {{
    border-color: var(--danger);
    background: rgba(255, 51, 102, 0.05);
  }}
  .agent-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
  }}
  .agent-id {{ color: var(--accent); font-weight: bold; }}
  .agent-role {{ color: var(--text-muted); font-size: 10px; }}
  .agent-metrics {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4px; font-size: 10px; }}
  .agent-metrics .lbl {{ color: var(--text-muted); }}
  .agent-metrics .val {{ color: var(--cyan); }}
  .agent-metrics .val.highlight {{ color: var(--warn); font-weight: bold; }}
  .fever-alert {{
    margin-top: 6px;
    color: var(--danger);
    font-size: 9px;
    font-weight: bold;
    animation: blink 1s infinite;
  }}
  .link-list {{ display: flex; flex-direction: column; gap: 4px; max-height: 220px; overflow-y: auto; }}
  .link-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: #090d14;
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #141c2b;
  }}
  .link-node {{ width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .link-node.from {{ color: #7dd3fc; }}
  .link-node.to {{ color: #f472b6; }}
  .link-arrow {{ color: var(--text-muted); }}
  .link-weight {{ color: var(--warn); margin-left: auto; font-weight: bold; }}
  .disc-list {{ display: flex; flex-direction: column; gap: 4px; max-height: 220px; overflow-y: auto; }}
  .disc-item {{
    display: flex;
    gap: 8px;
    align-items: center;
    background: #090d14;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    border-left: 3px solid transparent;
  }}
  .disc-item.causal {{ border-left-color: var(--cyan); }}
  .disc-item.law {{ border-left-color: var(--accent); }}
  .disc-item .time {{ color: var(--text-muted); font-size: 9px; }}
  .tag {{
    font-size: 9px;
    padding: 1px 4px;
    border-radius: 3px;
    font-weight: bold;
  }}
  .link-tag {{ background: #0369a1; color: #bae6fd; }}
  .law-tag {{ background: #065f46; color: #a7f3d0; }}
  .disc-item .agent {{ color: var(--warn); }}
  .disc-item .concept {{ color: var(--cyan); font-weight: bold; }}
  .disc-item .eq {{ color: var(--accent); }}
  .telemetry-bar {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
  }}
  .telemetry-pill {{
    background: #090d14;
    border: 1px solid #1e293b;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 10px;
    color: var(--cyan);
  }}
  footer {{
    margin-top: 16px;
    border-top: 1px solid var(--border);
    padding-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--text-muted);
    font-size: 10px;
  }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>

<header>
  <h1>
    <span>🔬</span> BinoryLogy 2.0 &mdash; Sovereign Physics Cognitive Architecture
    <span class="badge-live">LIVE 24/7</span>
  </h1>
  <div>
    <span style="color: var(--text-muted)">Step:</span> <b style="color: var(--accent)">{step:,}</b> &nbsp;|&nbsp;
    <span style="color: var(--text-muted)">Vault:</span> <a href="https://huggingface.co/datasets/{HF_REPO}" target="_blank">{HF_REPO}</a>
  </div>
</header>

<div class="grid">

  <!-- Curriculum Card -->
  <div class="card col-4">
    <div class="card-title">
      <span>📚 Physics Curriculum</span>
      <span style="color: var(--accent)">Tier {tier}/6</span>
    </div>
    <div class="tier-banner">
      {tier_badges_html}
    </div>
    <div style="font-size: 11px; color: var(--cyan); font-weight: bold; margin-top: 4px;">
      {tier_name}
    </div>
    <div style="font-size: 10px; color: var(--text-muted); margin-bottom: 6px;">
      {tier_descriptions.get(tier, '')}
    </div>
    <div style="display:flex; justify-content:space-between; font-size: 10px;">
      <span>Mastery</span>
      <span>{mastery:.1%}</span>
    </div>
    <div class="mastery-outer">
      <div class="mastery-fill" style="width: {mastery * 100:.1f}%;"></div>
    </div>
    <div class="stat-grid">
      <div class="stat-box">
        <div class="k">TOTAL DISCOVERIES</div>
        <div class="v" style="color: var(--accent)">{total_disc}</div>
      </div>
      <div class="stat-box">
        <div class="k">EMERGED LINKS</div>
        <div class="v" style="color: var(--cyan)">{emerged_count}</div>
      </div>
      <div class="stat-box">
        <div class="k">ACTIVE SYNAPSES</div>
        <div class="v">{synapse_count}</div>
      </div>
      <div class="stat-box">
        <div class="k">ADAPTIVE THRESHOLD</div>
        <div class="v" style="color: var(--warn)">{threshold:.2f}</div>
      </div>
    </div>
  </div>

  <!-- Cognitive Council Card -->
  <div class="card col-8">
    <div class="card-title">
      <span>⚛️ 4 Sovereign Pillars — God Equation S&#8314;&#8301;&#8314;&#185; = U(S,A,O,M) + L(S)</span>
      <span style="font-size: 10px; color: var(--text-muted)">Heartbeat: {s.get('sample_interval', 0.5):.2f}s</span>
    </div>
    <div class="agent-list">
      {agents_html}
    </div>
    <div style="margin-top: 10px; border-top: 1px solid #141c2b; padding-top: 8px;">
      <span style="font-size: 10px; color: var(--text-muted)">Live Stream [{s.get('obs_stream', '?')}]:</span>
      <div class="telemetry-bar">
        {obs_pills}
      </div>
    </div>
  </div>

  <!-- Causal Synapse Network -->
  <div class="card col-4">
    <div class="card-title">
      <span>⚡ Causal Network (STDP + TE)</span>
      <span style="font-size: 10px; color: var(--cyan)">{emerged_count} links</span>
    </div>
    <div class="link-list">
      {links_html if links_html else '<div style="color: var(--text-muted)">Constructing causal graph from physics streams...</div>'}
    </div>
  </div>

  <!-- 4-Pillar Synaptic Connectome -->
  <div class="card col-4">
    <div class="card-title">
      <span>🧬 4-Pillar Connectome (Zero Broadcast)</span>
      <span style="font-size: 10px; color: var(--accent)">{s.get('total_messages', 0):,} msgs</span>
    </div>
    <div class="link-list">
      {connectome_html if connectome_html else '<div style="color: var(--text-muted)">Evolving synaptic axons between pillars...</div>'}
    </div>
  </div>

  <!-- Discovery Ledger -->
  <div class="card col-4">
    <div class="card-title">
      <span>🔭 Discovered Laws & Invariants</span>
      <span style="font-size: 10px; color: var(--accent)">{total_disc} total</span>
    </div>
    <div class="disc-list">
      {disc_html if disc_html else '<div style="color: var(--text-muted)">Genesis step 0 &mdash; observing stream...</div>'}
    </div>
  </div>

</div>

<footer>
  <div>
    <span>Server: Render Cloud &bull; Persistence: Hugging Face Dataset &bull; Zero Handcrafted Rules</span>
  </div>
  <div>
    <a href="/api/state" target="_blank">JSON State</a> &bull;
    <a href="/api/discoveries" target="_blank">Discoveries API</a> &bull;
    <a href="/ping" target="_blank">Ping</a>
  </div>
</footer>

</body>
</html>
"""
    return HTMLResponse(content=html)
