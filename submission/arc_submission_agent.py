"""Submission-ready baseline agent for ARC-AGI-3.

This file is designed as a clean starting point for a Kaggle-style ARC-AGI-3
submission. It exposes a minimal agent interface with:

- is_done(frames, latest_frame)
- choose_action(frames, latest_frame)

and a lightweight local runner that can inspect public environment files.

The goal is not to claim a strong solver, but to make the repo submission-ready
with the correct interface and a standardized agent entry point.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


ACTION_NAMES = [
    "RESET",
    "ACTION1",
    "ACTION2",
    "ACTION3",
    "ACTION4",
    "ACTION5",
    "ACTION6",
    "ACTION7",
]


class ARCAGI3Agent:
    """Baseline ARC-AGI-3 agent.

    This is intentionally simple but valid for submission scaffolding:
    - it respects the lifecycle contract,
    - it recognizes the end-of-game conditions,
    - it picks structured actions using a generic exploration heuristic.
    """

    def __init__(self, max_steps: int = 400):
        self.max_steps = max_steps
        self.step_count = 0
        self.last_action = "RESET"
        self.explore_cycle = ["ACTION1", "ACTION2", "ACTION3", "ACTION4", "ACTION5"]
        self.cycle_index = 0

    def _grid_from_frame(self, frame: Optional[Dict[str, Any]]) -> List[List[int]]:
        if not frame:
            return []
        for key in ("grid", "board", "screen", "cells"):
            data = frame.get(key)
            if isinstance(data, list) and data and isinstance(data[0], list):
                return data
        return []

    def _find_nonzero_cells(self, grid: List[List[int]]) -> List[Tuple[int, int, int]]:
        cells: List[Tuple[int, int, int]] = []
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value != 0:
                    cells.append((x, y, int(value)))
        return cells

    def _centroid(self, cells: List[Tuple[int, int, int]]) -> Optional[Tuple[int, int]]:
        if not cells:
            return None
        xs = [x for x, _, _ in cells]
        ys = [y for _, y, _ in cells]
        return (sum(xs) // len(xs), sum(ys) // len(ys))

    def _direction_toward(self, target: Tuple[int, int], origin: Tuple[int, int]) -> str:
        dx = target[0] - origin[0]
        dy = target[1] - origin[1]
        if abs(dx) >= abs(dy):
            return "ACTION2" if dx > 0 else "ACTION1"
        return "ACTION4" if dy > 0 else "ACTION3"

    def is_done(self, frames: List[Dict[str, Any]], latest_frame: Optional[Dict[str, Any]]) -> bool:
        if latest_frame is None:
            return False

        state = str(latest_frame.get("state", "NOT_FINISHED")).upper()
        if state in {"WIN", "GAME_OVER", "DONE"}:
            return True

        if self.step_count >= self.max_steps:
            return True

        return False

    def choose_action(self, frames: List[Dict[str, Any]], latest_frame: Optional[Dict[str, Any]]) -> str:
        self.step_count += 1

        if latest_frame is None:
            return "RESET"

        state = str(latest_frame.get("state", "NOT_FINISHED")).upper()
        if state in {"WIN", "GAME_OVER", "DONE"}:
            return "RESET"

        if not frames:
            return "RESET"

        grid = self._grid_from_frame(latest_frame)
        if not grid:
            return "RESET"

        nonzero = self._find_nonzero_cells(grid)
        if not nonzero:
            action = self.explore_cycle[self.cycle_index % len(self.explore_cycle)]
            self.cycle_index += 1
            self.last_action = action
            return action

        origin = self._centroid(nonzero)
        if origin is None:
            action = self.explore_cycle[self.cycle_index % len(self.explore_cycle)]
            self.cycle_index += 1
            self.last_action = action
            return action

        # A lightweight heuristic: prefer moving toward the densest cluster.
        # Since ARC-AGI-3 games are interactive and action meanings vary, we avoid
        # trying to be domain-specific. We simply bias toward the object cluster.
        target = origin
        action = self._direction_toward(target, (len(grid[0]) // 2, len(grid) // 2))

        # If the action repeats too much, fall back to a safe exploration cycle.
        if action == self.last_action and self.step_count % 7 == 0:
            action = self.explore_cycle[self.cycle_index % len(self.explore_cycle)]
            self.cycle_index += 1

        self.last_action = action
        return action


def discover_environment_files(base_dir: Path) -> List[Path]:
    if not base_dir.exists():
        return []
    return sorted(p for p in base_dir.rglob("*.json") if p.is_file())


def main() -> None:
    parser = argparse.ArgumentParser(description="ARC-AGI-3 baseline submission agent")
    parser.add_argument(
        "--env-dir",
        type=Path,
        default=Path("./environment_files"),
        help="Directory containing public ARC-AGI-3 environment files.",
    )
    args = parser.parse_args()

    env_dir = args.env_dir
    files = discover_environment_files(env_dir)
    print(f"Found {len(files)} environment files under {env_dir}")
    if files:
        for p in files[:5]:
            print(f" - {p}")
    else:
        print("No environment JSON files were found. This is expected before the Kaggle data bundle is mounted.")

    agent = ARCAGI3Agent()
    print("Agent initialized.")
    print("Expected interface:")
    print("  agent.is_done(frames, latest_frame)")
    print("  agent.choose_action(frames, latest_frame)")


if __name__ == "__main__":
    main()
