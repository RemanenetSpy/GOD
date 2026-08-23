"""
Test script for the Hugging Face Space application.
Verifies that CA universe, multi-agent civilization, and canvas rendering execute cleanly.
"""

import sys
import os

from ca_universe import CellularAutomataUniverse
from sovereign_civilization import SovereignCivilization
from app import SimulationSession, render_visual_canvas, get_agent_metrics_table, format_subroutine_archive


def test_hf_session():
    print("\n[TEST HF] Testing SimulationSession in Cellular Automata Universe...")
    sess = SimulationSession(grid_size=20, ca_rule="Conway (B3/S23)")
    
    # Run 5 steps
    for s in range(1, 6):
        res = sess.step()
        assert res["step"] == s, f"Step mismatch: expected {s}, got {res['step']}"
        print(f"  Step {s:02d}: Actions = {res['actions']}")
        
    fig = render_visual_canvas(sess)
    assert fig is not None, "Canvas plot generation returned None"
    
    table = get_agent_metrics_table(sess)
    assert len(table) == 4, f"Expected 4 agent rows in table, got {len(table)}"
    
    subs = format_subroutine_archive(sess)
    assert isinstance(subs, str), "Subroutine archive formatting failed"
    
    print("[PASS] Hugging Face Space simulation and visualization verified successfully!")


if __name__ == "__main__":
    test_hf_session()
