"""
========================================================================================
HUGGING FACE SPACE: SOVEREIGN CIVILIZATION & CELLULAR AUTOMATA EMERGENCE
========================================================================================
An interactive, browser-based visual laboratory uniting:
1. Dynamic Cellular Automata Living Universes (Conway's Life, HighLife, Seeds, Day & Night)
2. The 4-Pillar Sovereign Civilization (Classical, Quantum, Modern, String Meta-Agents)
3. Relativistic Tensor Messages (M_t^i), Metabolic Vitality (dH/dt), and Fever Phase Shifts
4. 24/7 Persistent Storage Resilience (/data volume state restore across reboots)
========================================================================================
"""

import os
import json
import copy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import gradio as gr
from typing import Tuple, Dict, Any

from ca_universe import CellularAutomataUniverse
from sovereign_civilization import (
    SovereignCivilization,
    Action,
    Observation,
    PillarArchetype
)
from hf_dataset_memory import HFDatasetMemoryVault

STORAGE_DIR = os.environ.get("STORAGE_DIR", "/data" if os.path.exists("/data") else "./data")
os.makedirs(STORAGE_DIR, exist_ok=True)
CHECKPOINT_FILE = os.path.join(STORAGE_DIR, "civilization_checkpoint.json")
LOG_FILE = os.path.join(STORAGE_DIR, "civilization_run.log")

# Cloud Dataset Memory Vault (Free 24/7 Cloud Persistence)
memory_vault = HFDatasetMemoryVault(
    repo_id=os.environ.get("HF_DATASET_REPO", "Explorerp/sovereign-civilization-memory"),
    local_cache_dir=STORAGE_DIR
)


class SimulationSession:
    """Manages the interactive state of the CA universe and the Sovereign Civilization with 24/7 persistence."""
    def __init__(self, grid_size: int = 25, ca_rule: str = "Conway (B3/S23)"):
        self.grid_shape = (grid_size, grid_size)
        self.ca_rule = ca_rule
        self.universe = CellularAutomataUniverse(grid_shape=self.grid_shape, ca_rule=ca_rule, initial_density=0.22)
        self.civ = SovereignCivilization(grid_shape=self.grid_shape)
        
        # Agent spatial positions
        self.positions: Dict[str, Tuple[int, int]] = {
            "classical_prime": (2, 2),
            "quantum_prime": (grid_size - 3, 2),
            "modern_prime": (2, grid_size - 3),
            "string_meta": (grid_size - 3, grid_size - 3),
        }
        self.step_num: int = 0
        self.log_history: list = []
        
        # Restore checkpoint from Cloud Dataset or local cache upon reboot
        self.load_checkpoint()

    def save_checkpoint(self):
        """Saves current state and discovered subroutines to local storage and syncs to Cloud Dataset repo."""
        try:
            state_data = {
                "step_num": self.step_num,
                "ca_rule": self.ca_rule,
                "grid_shape": list(self.grid_shape),
                "positions": {k: list(v) for k, v in self.positions.items()},
                "subroutines": self.civ.global_subroutine_archive,
                "agent_energies": {k: float(node.state.energy) for k, node in self.civ.nodes.items()},
                "agent_temperatures": {k: float(node.state.temperature) for k, node in self.civ.nodes.items()}
            }
            # Sync to Private Dataset Repository on Hugging Face
            memory_vault.save_checkpoint(state_data, commit_msg=f"Civilization step {self.step_num} update")
        except Exception as e:
            print(f"[Warning] Failed to write checkpoint: {e}")

    def load_checkpoint(self):
        """Restores civilization state from Cloud Dataset Vault upon reboot."""
        try:
            data = memory_vault.load_checkpoint()
            if data:
                self.step_num = data.get("step_num", 0)
                self.ca_rule = data.get("ca_rule", self.ca_rule)
                if "positions" in data:
                    self.positions = {k: tuple(v) for k, v in data["positions"].items()}
                if "subroutines" in data:
                    self.civ.global_subroutine_archive.update(data["subroutines"])
                if "agent_energies" in data:
                    for aid, e in data["agent_energies"].items():
                        if aid in self.civ.nodes:
                            self.civ.nodes[aid].state.energy = float(e)
                self.log_history.append(f"[Reboot Recovery] Successfully restored civilization from step {self.step_num} with {len(self.civ.global_subroutine_archive)} subroutines!")
            else:
                self.log_history.append(f"Initialized fresh Cellular Automata universe ({self.ca_rule}) with 4 Sovereign Pillars.")
        except Exception as e:
            self.log_history.append(f"Starting from default weights (checkpoint load error: {e})")

    def reset(self, grid_size: int, ca_rule: str):
        self.grid_shape = (grid_size, grid_size)
        self.ca_rule = ca_rule
        self.universe = CellularAutomataUniverse(grid_shape=self.grid_shape, ca_rule=ca_rule, initial_density=0.22)
        self.civ = SovereignCivilization(grid_shape=self.grid_shape)
        self.positions = {
            "classical_prime": (2, 2),
            "quantum_prime": (grid_size - 3, 2),
            "modern_prime": (2, grid_size - 3),
            "string_meta": (grid_size - 3, grid_size - 3),
        }
        self.step_num = 0
        self.log_history = [f"Reset Cellular Automata universe ({ca_rule}) with 4 Sovereign Pillars."]
        self.save_checkpoint()

    def step(self) -> Dict[str, Any]:
        self.step_num += 1
        h, w = self.grid_shape
        
        # 1. Step Cellular Automata Physical Substrate
        pos_list = list(self.positions.values())
        rewards = self.universe.step(pos_list)
        
        # 2. Build Relativistic Observations
        observations: Dict[str, Observation] = {}
        for idx, (aid, pos) in enumerate(self.positions.items()):
            r = self.civ.nodes[aid].aperture
            vis = self.universe.get_observation_window(pos, aperture=r)
            rew = rewards.get(f"agent_{idx}", 0.05)
            observations[aid] = Observation(visible_cells=vis, position=pos, reward=rew)
            
        # 3. Step Sovereign Civilization (God Equation + M_t^i Tensor Fabric)
        actions = self.civ.step(observations)
        
        # 4. Apply Spatial Actions
        for aid, act in actions.items():
            cy, cx = self.positions[aid]
            if act == Action.MOVE_UP:
                cy = max(0, cy - 1)
            elif act == Action.MOVE_DOWN:
                cy = min(h - 1, cy + 1)
            elif act == Action.MOVE_LEFT:
                cx = max(0, cx - 1)
            elif act == Action.MOVE_RIGHT:
                cx = min(w - 1, cx + 1)
            self.positions[aid] = (cy, cx)
            self.civ.nodes[aid].state.position = (cy, cx)

        # Log recent messages
        recent_msgs = self.civ.fabric.history[-3:]
        for m in recent_msgs:
            log_line = f"[Step {self.step_num:02d}] {m.summary()}"
            self.log_history.append(log_line)
            try:
                with open(LOG_FILE, 'a') as f:
                    f.write(log_line + "\n")
            except Exception:
                pass
                
        if len(self.log_history) > 30:
            self.log_history = self.log_history[-30:]

        # Auto-persist state periodically
        if self.step_num % 5 == 0:
            self.save_checkpoint()

        return {
            "step": self.step_num,
            "actions": {k: v.name for k, v in actions.items()},
        }


# Global session singleton for Gradio UI
session = SimulationSession(grid_size=25, ca_rule="Conway (B3/S23)")


def render_visual_canvas(session: SimulationSession) -> plt.Figure:
    """Renders the dual-panel interactive visual: Left=Living CA Universe, Right=Consensus Mind Field."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=100)
    fig.patch.set_facecolor('#0d1117')
    
    h, w = session.grid_shape
    
    # ----------------------------------------------------
    # PANEL 1: CELLULAR AUTOMATA LIVING UNIVERSE
    # ----------------------------------------------------
    ax1.set_facecolor('#0d1117')
    ca_grid = session.universe.grid
    
    rgb = np.zeros((*session.grid_shape, 3), dtype=np.float32)
    rgb[ca_grid == 0] = [0.06, 0.08, 0.12]  # Deep void
    rgb[ca_grid == 1] = [0.15, 0.85, 0.45]  # Living cell
    rgb[ca_grid == 2] = [0.85, 0.25, 0.35]  # Dense crystalline obstacle
    
    ax1.imshow(rgb, origin='upper', interpolation='nearest')
    
    agent_colors = {
        "classical_prime": ("#38bdf8", "C"),
        "quantum_prime": ("#a855f7", "Q"),
        "modern_prime": ("#f59e0b", "M"),
        "string_meta": ("#ec4899", "S")
    }
    
    for aid, pos in session.positions.items():
        color, symbol = agent_colors[aid]
        py, px = pos
        r = session.civ.nodes[aid].aperture
        
        rect = plt.Rectangle((px - r - 0.5, py - r - 0.5), 2*r + 1, 2*r + 1,
                             fill=False, edgecolor=color, linestyle='--', alpha=0.5, linewidth=1.5)
        ax1.add_patch(rect)
        
        ax1.scatter(px, py, color=color, s=220, edgecolors='white', linewidths=1.5, zorder=5)
        ax1.text(px, py, symbol, color='black', fontweight='bold', fontsize=10, ha='center', va='center', zorder=6)
        
    ax1.set_title(f"Living Cellular Automata Universe (Step {session.step_num})", color='white', fontsize=12, pad=10)
    ax1.axis('off')
    
    # ----------------------------------------------------
    # PANEL 2: COLLECTIVE CONSCIOUSNESS & CONSENSUS FIELD
    # ----------------------------------------------------
    ax2.set_facecolor('#0d1117')
    consensus = session.civ.synthesize_consensus()
    res_density = consensus[:, :, 1] + consensus[:, :, 3] * 0.3
    
    im2 = ax2.imshow(res_density, cmap='magma', origin='upper', interpolation='bicubic')
    ax2.set_title("Multi-Agent Consensus Potential Field Phi(x)", color='white', fontsize=12, pad=10)
    ax2.axis('off')
    
    plt.tight_layout()
    return fig


def get_agent_metrics_table(session: SimulationSession) -> list:
    data = []
    for aid, node in session.civ.nodes.items():
        st = node.state
        fever_status = "FEVER" if node.fever_active else "STABLE"
        data.append([
            aid,
            st.pillar.value,
            f"({st.position[0]}, {st.position[1]})",
            f"{st.energy:.1f}",
            f"{st.dh_dt:+.2f}",
            f"{st.temperature:.2f}",
            f"{st.viscosity:.2f}",
            f"{st.belief_entropy:.2f}",
            fever_status
        ])
    return data


def format_subroutine_archive(session: SimulationSession) -> str:
    archive = session.civ.global_subroutine_archive
    if not archive:
        return "No subroutines compressed yet. Agents are exploring the substrate..."
    lines = []
    for sig, code in archive.items():
        lines.append(f"- [{sig}]: {code}")
    return "\n".join(lines)


# Gradio Event Handlers
def step_simulation():
    session.step()
    fig = render_visual_canvas(session)
    metrics = get_agent_metrics_table(session)
    log_text = "\n".join(reversed(session.log_history[-15:]))
    subs_text = format_subroutine_archive(session)
    tot_e = sum(n.state.energy for n in session.civ.nodes.values())
    msgs_count = session.civ.fabric.total_messages_routed
    status_summary = f"Step: {session.step_num:03d} | Vitality: {tot_e:.1f} | Messages: {msgs_count} | Subroutines: {len(session.civ.global_subroutine_archive)} | Storage: {STORAGE_DIR}"
    return fig, metrics, log_text, subs_text, status_summary


def step_multi(n_steps: int):
    for _ in range(int(n_steps)):
        session.step()
    fig = render_visual_canvas(session)
    metrics = get_agent_metrics_table(session)
    log_text = "\n".join(reversed(session.log_history[-15:]))
    subs_text = format_subroutine_archive(session)
    tot_e = sum(n.state.energy for n in session.civ.nodes.values())
    msgs_count = session.civ.fabric.total_messages_routed
    status_summary = f"Step: {session.step_num:03d} | Vitality: {tot_e:.1f} | Messages: {msgs_count} | Subroutines: {len(session.civ.global_subroutine_archive)} | Storage: {STORAGE_DIR}"
    return fig, metrics, log_text, subs_text, status_summary


def trigger_systemic_fever():
    for node in session.civ.nodes.values():
        node.trigger_fever()
    session.log_history.append(f"[Step {session.step_num:02d}] ⚡ SYSTEMIC FEVER TRIGGERED: Thermal phase transition across all pillars!")
    return step_simulation()


def reset_world(grid_size: int, ca_rule: str):
    session.reset(grid_size=int(grid_size), ca_rule=ca_rule)
    fig = render_visual_canvas(session)
    metrics = get_agent_metrics_table(session)
    log_text = "\n".join(session.log_history)
    subs_text = "Archive reset. Awaiting new compressions..."
    status_summary = f"Universe reset to {ca_rule} (Grid: {grid_size}x{grid_size})"
    return fig, metrics, log_text, subs_text, status_summary


with gr.Blocks(title="Sovereign Civilization & Cellular Automata") as demo:
    gr.Markdown(
        """
        # 🌌 Sovereign Civilization: Cellular Automata & Autonomous Self-Evolution
        ### *Exploring, Learning, and Perceiving Beyond Human Cognitive Limits (24/7 Resilient)*
        
        **Governed by the God Equation:** $S_{t+1}^i = U(S_t^i, A_t^i, O_t^i, M_t^i) + L(S_t^i)$
        
        Watch **Classical (C)**, **Quantum (Q)**, **Modern (M)**, and **String Meta-Agents (S)** inhabit a living **Cellular Automata** universe, communicating through relativistic message tensors $M_t^i$, minting Kolmogorov subroutines, and undergoing thermodynamic fever phase shifts.
        """
    )
    
    with gr.Row():
        status_bar = gr.Textbox(
            value=f"Initialized and ready. Storage mounted at: {STORAGE_DIR}",
            label="Civilization Status & Persistent Volume Telemetry",
            interactive=False
        )

    with gr.Row():
        canvas_plot = gr.Plot(value=render_visual_canvas(session), label="Living Universe Canvas")

    with gr.Row():
        with gr.Column(scale=1):
            btn_step = gr.Button("⚡ Step (Single)", variant="primary", size="lg")
            btn_multi = gr.Button("🚀 Run Epoch (10 Steps)", variant="secondary", size="lg")
            btn_fever = gr.Button("🔥 Trigger Systemic Fever", variant="stop", size="sm")
            
        with gr.Column(scale=1):
            rule_dropdown = gr.Dropdown(
                choices=["Conway (B3/S23)", "HighLife (B36/S23)", "Seeds (B2/S)", "Day & Night (B3678/S34678)"],
                value="Conway (B3/S23)",
                label="Cellular Automata Physics Ruleset"
            )
            grid_slider = gr.Slider(minimum=15, maximum=40, value=25, step=5, label="Universe Dimensionality (N x N)")
            btn_reset = gr.Button("🔄 Reset Universe", variant="secondary", size="sm")

    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("### 📊 Relativistic Agent Telemetry")
            telemetry_table = gr.Dataframe(
                headers=["Agent ID", "Pillar", "Position", "Energy (H)", "dH/dt", "Temp (T)", "Viscosity", "Entropy", "Fever"],
                value=get_agent_metrics_table(session),
                label="Agent Internal States S_t^i"
            )
            
        with gr.Column(scale=2):
            gr.Markdown("### 📜 Discovered Kolmogorov Subroutine Archive")
            subroutine_box = gr.Textbox(
                value=format_subroutine_archive(session),
                lines=8,
                label="Shared Code Subroutines (L(S_t) Compression)",
                interactive=False
            )

    with gr.Row():
        gr.Markdown("### 📡 Relativistic Message Stream ($M_t^i$ Transmissions)")
        message_stream_box = gr.Textbox(
            value="\n".join(session.log_history),
            lines=6,
            label="Live Message Fabric Transmissions",
            interactive=False
        )

    # Event Bindings
    btn_step.click(
        fn=step_simulation,
        inputs=[],
        outputs=[canvas_plot, telemetry_table, message_stream_box, subroutine_box, status_bar]
    )
    btn_multi.click(
        fn=lambda: step_multi(10),
        inputs=[],
        outputs=[canvas_plot, telemetry_table, message_stream_box, subroutine_box, status_bar]
    )
    btn_fever.click(
        fn=trigger_systemic_fever,
        inputs=[],
        outputs=[canvas_plot, telemetry_table, message_stream_box, subroutine_box, status_bar]
    )
    btn_reset.click(
        fn=reset_world,
        inputs=[grid_slider, rule_dropdown],
        outputs=[canvas_plot, telemetry_table, message_stream_box, subroutine_box, status_bar]
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
