import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import numpy as np
from arc_sovereign_arena.causal_deduction import InverseCausalDeducer, DeducedHypothesis

with open('research_archive/arc_agi/ARC-AGI-master/data/training/025d127b.json') as f:
    task = json.load(f)

train_pairs = [{'input': np.array(p['input']), 'output': np.array(p['output'])} for p in task['train']]
test_pairs = [{'input': np.array(p['input']), 'output': np.array(p['output'])} for p in task['test']]

print("=== 1. Testing Boundary-Anchored Kinematic Shear Invariant ===")

def make_anchored_kinematic_shear(anchor_side: str, shift: tuple):
    dr, dc = shift
    def apply_shear(grid: np.ndarray) -> np.ndarray:
        res = np.zeros_like(grid)
        h, w = grid.shape
        colors = [c for c in np.unique(grid) if c != 0]
        for col in colors:
            coords = np.argwhere(grid == col)
            if len(coords) == 0:
                continue
            r_min, c_min = np.min(coords, axis=0)
            r_max, c_max = np.max(coords, axis=0)
            for r, c in coords:
                is_anchored = False
                if anchor_side == "bottom":
                    # Fixed base: bottom row or corner cell above bottom
                    if r == r_max or (r == r_max - 1 and c == c_max) or (r == r_max - 1 and c == c_min):
                        is_anchored = True
                elif anchor_side == "top":
                    if r == r_min or (r == r_min + 1 and c == c_max) or (r == r_min + 1 and c == c_min):
                        is_anchored = True
                
                if is_anchored:
                    res[r, c] = col
                else:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < h and 0 <= nc < w:
                        res[nr, nc] = col
        return res
    return apply_shear

shear_hyp = DeducedHypothesis(
    "classical_prime",
    "anchored_shear_bottom_right",
    "Classical Kinematics: Boundary-Anchored Base Shear (No-Slip Fixed Foundation + Horizontal Drift)",
    make_anchored_kinematic_shear("bottom", (0, 1)),
    complexity=1.8
)

for idx, p in enumerate(train_pairs):
    pred = shear_hyp.apply(p['input'])
    match = np.array_equal(pred, p['output'])
    print(f"  Train Pair {idx}: Exact Match = {match}")

for idx, p in enumerate(test_pairs):
    pred = shear_hyp.apply(p['input'])
    match = np.array_equal(pred, p['output'])
    print(f"  Test Pair {idx}: Exact Match = {match}")

print("\n=== 2. Simulation of Niche Construction on Death ===")
# Demonstrate that without wiping canvas, generations accumulate correct tiles
input_canvas = train_pairs[0]['input'].copy()
target_canvas = train_pairs[0]['output'].copy()
working = input_canvas.copy()

# Assume Generation 1 finds 5 food pixels
unsolved = np.argwhere((working != target_canvas) & (target_canvas > 0))
print(f"Initial unsolved pixels to paint: {len(unsolved)}")
# Step 1: paint 5 pixels
for r, c in unsolved[:5]:
    working[r, c] = target_canvas[r, c]
print(f"After Gen 1 work, remaining unsolved: {np.sum(working != target_canvas)}")

# If canvas is NOT wiped on death (Niche Construction):
# Gen 2 continues from `working`
unsolved_gen2 = np.argwhere((working != target_canvas) & (target_canvas > 0))
for r, c in unsolved_gen2[:5]:
    working[r, c] = target_canvas[r, c]
print(f"After Gen 2 work, remaining unsolved: {np.sum(working != target_canvas)}")

# Gen 3 finishes
unsolved_gen3 = np.argwhere((working != target_canvas) & (target_canvas > 0))
for r, c in unsolved_gen3:
    working[r, c] = target_canvas[r, c]
# Clear any leftover input pixels that need to be erased (set to 0)
erased = np.argwhere((working != target_canvas) & (target_canvas == 0))
for r, c in erased:
    working[r, c] = 0

print(f"After Gen 3 work, puzzle cleared = {np.array_equal(working, target_canvas)}")
