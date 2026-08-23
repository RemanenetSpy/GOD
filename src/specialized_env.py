"""
Specialized Environments for the Four Pillars Tournament.
"""

import numpy as np
import random
from typing import Tuple, List, Dict
from environment import CellType, Observation, Action
from pacman_env import PacManWorld

class QuantumMaze(PacManWorld):
    """
    The Shifting Maze: Walls appear/disappear randomly.
    Bias: Quantum (Exploration).
    """
    def __init__(self, size=15, num_ghosts=2, seed=None):
        super().__init__(size=size, num_ghosts=num_ghosts, seed=seed)
        self.shift_interval = 10
    
    def step(self, action: Action):
        # Shift walls every N steps
        if self.steps > 0 and self.steps % self.shift_interval == 0:
            self._shift_walls()
            
        return super().step(action)
        
    def _shift_walls(self):
        # Randomly toggle some internal walls
        for i in range(2, self.size - 2):
            for j in range(2, self.size - 2):
                if random.random() < 0.1: # 10% chance to flip state
                    if self.grid[i, j] == CellType.OBSTACLE.value:
                        self.grid[i, j] = CellType.EMPTY.value
                    elif self.grid[i, j] == CellType.EMPTY.value:
                        # Don't spawn on Pacman or Ghost
                        if (i, j) != self.pacman_pos and not any(g['pos'] == (i,j) for g in self.ghosts):
                            self.grid[i, j] = CellType.OBSTACLE.value

class PhysicsMaze(PacManWorld):
    """
    The Clockwork Runners: Timed deterministic hazards.
    Bias: Physics (Precision).
    """
    def __init__(self, size=20, num_ghosts=0, seed=None): # No ghosts, just spikes
        super().__init__(size=size, num_ghosts=0, seed=seed)
        self.spike_interval = 5
        
    def step(self, action: Action):
        obs, reward, done = super().step(action)
        
        # Check spikes
        if self.steps % self.spike_interval == 0:
            # Spikes activate on (even, even) coordinates
            px, py = self.pacman_pos
            if px % 2 == 0 and py % 2 == 0:
                reward -= 500.0 # DEATH
                self.lives -= 1
                if self.lives <= 0:
                    done = True
        
        return obs, reward, done
        
    def observe(self, last_reward=0.0):
        # NO FOG OF WAR (Physics knows all)
        obs = super().observe(last_reward)
        obs.visible_cells = self.grid.copy() # Full visibility
        return obs

class RelativityMaze(PacManWorld):
    """
    Sniper Alley: Fast ghosts, long range vision.
    Bias: Relativity (Prediction).
    """
    def __init__(self, size=20, num_ghosts=2, seed=None):
        super().__init__(size=size, num_ghosts=num_ghosts, seed=seed)
        
    def _move_ghosts(self):
        # Ghosts move TWICE per turn
        super()._move_ghosts()
        super()._move_ghosts()

    def observe(self, last_reward=0.0):
        # Extended Vision (Range 5 instead of 2)
        # We hack this by temporarily modifying the grid or just forcing the observation logic
        # Ideally, Agent controls vision, but here Environment gives "Line of Sight"
        
        # Call super but verify logic allows overrides? 
        # Actually super observe() hardcodes 'visible_range = 2'.
        # We need to reimplement observe() or monkeypatch.
        # Reimplementing for safety:
        
        visible_range = 5 # Sniper vision
        visible_cells = np.full((self.size, self.size), CellType.UNKNOWN.value, dtype=int)
        px, py = self.pacman_pos
        vr = visible_range
        
        for i in range(max(0, px - vr), min(self.size, px + vr + 1)):
            for j in range(max(0, py - vr), min(self.size, py + vr + 1)):
                if abs(i - px) + abs(j - py) <= vr:
                    obj_type = self.grid[i, j]
                    for ghost in self.ghosts:
                        if ghost['alive'] and ghost['pos'] == (i, j):
                            obj_type = CellType.GHOST.value
                            break
                    if (i, j) == self.pacman_pos:
                        obj_type = CellType.PACMAN.value
                    visible_cells[i, j] = obj_type
                    
        return Observation(visible_cells, self.pacman_pos, last_reward, False)

class InformationMaze(PacManWorld):
    """
    The Pattern Trap: Fake pellets with a discoverable rule.
    Bias: Information (Learning).
    """
    def __init__(self, size=15, num_ghosts=1, seed=None):
        super().__init__(size=size, num_ghosts=num_ghosts, seed=seed)
        self._convert_fake_pellets()
        
    def _convert_fake_pellets(self):
        # Rule: True Pellets have a wall to their LEFT (y-1)
        # Fake Pellets do not.
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                if self.grid[i, j] == CellType.PELLET.value:
                    if self.grid[i, j-1] != CellType.OBSTACLE.value:
                        # No wall to left -> FAKE (Poison)
                        # We mark it as valid in GRID so it looks like a pellet,
                        # but we track it internally as poison.
                        pass 
                        
    def step(self, action: Action):
        # Override step to punish fake pellets
        # Need to check BEFORE super().step eats it
        
        # Predict move
        new_pos = list(self.pacman_pos)
        if action == Action.MOVE_UP: new_pos[0] -= 1
        elif action == Action.MOVE_DOWN: new_pos[0] += 1
        elif action == Action.MOVE_LEFT: new_pos[1] -= 1
        elif action == Action.MOVE_RIGHT: new_pos[1] += 1
        new_pos = tuple(new_pos)
        
        is_fake = False
        if 0 <= new_pos[0] < self.size and 0 <= new_pos[1] < self.size:
             if self.grid[new_pos] == CellType.PELLET.value:
                 # Check rule: Is there a wall to the left?
                 # Left of (x,y) is (x, y-1)
                 neighbor = self.grid[new_pos[0], new_pos[1]-1]
                 if neighbor != CellType.OBSTACLE.value:
                     is_fake = True
        
        obs, reward, done = super().step(action)
        
        if is_fake:
            reward -= 60.0 # Negate the +10 and add -50 penalty
            self.score -= 60
            
        return obs, reward, done
