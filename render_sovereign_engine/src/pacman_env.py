"""
Pac-Man Environment for Hybrid ToE-Inspired AGI.

This environment implements a simplified Pac-Man game compatible with the 
AGI agent's interface. It supports:
- Grid-based movement
- Partial observability (Fog of War)
- Ghosts with simple AI
- Power pellets and vulnerability mode
- Score tracking
"""

import numpy as np
import random
from typing import Tuple, List, Dict, Set
from environment import CellType, Observation, Action

class PacManWorld:
    """
    Pac-Man environment compatible with AGI system.
    """
    
    def __init__(self, size: int = 20, num_ghosts: int = 4, seed: int = None):
        """Initialize Pac-Man world."""
        self.size = size
        self.num_ghosts_init = num_ghosts
        self.seed = seed
        
        # Only set seed if provided, otherwise let numpy/random be random
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        # Game state
        self.pacman_pos = (1, 1)
        self.ghosts: List[Dict] = []
        self.grid = np.zeros((size, size), dtype=int)
        
        # Scoring
        self.score = 0
        self.steps = 0
        self.power_mode = False
        self.power_timer = 0
        self.lives = 3
        
        # Initialize map
        self.reset()
        
    def reset(self) -> Observation:
        """Reset environment to initial state."""
        self.score = 0
        self.steps = 0
        self.power_mode = False
        self.power_timer = 0
        self.lives = 3
        
        # Clear grid
        self.grid.fill(CellType.EMPTY.value)
        
        # Generate Maze (Simple recursive backtracker or just random walls)
        # Using simple random walls for now, ensuring connectivity
        self._generate_maze()
        
        # Place Pac-Man
        self.pacman_pos = self._find_empty_spot()
        
        # Place Ghosts
        self.ghosts = []
        for _ in range(self.num_ghosts_init):
            self.ghosts.append({
                'pos': self._find_empty_spot(min_dist_from_pacman=5),
                'alive': True,
                'scared': False
            })
            
        # Place Pellets (in all empty spots)
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] == CellType.EMPTY.value and (i, j) != self.pacman_pos:
                    # 5% chance of power pellet, else normal pellet
                    if random.random() < 0.02:
                        self.grid[i, j] = CellType.POWER_PELLET.value
                    else:
                        self.grid[i, j] = CellType.PELLET.value
        
        return self.observe()
    
    def _generate_maze(self):
        """Generate a random maze."""
        # Fill border with walls
        self.grid[0, :] = CellType.OBSTACLE.value
        self.grid[-1, :] = CellType.OBSTACLE.value
        self.grid[:, 0] = CellType.OBSTACLE.value
        self.grid[:, -1] = CellType.OBSTACLE.value
        
        # Add random internal blocks (density 0.2)
        for i in range(2, self.size - 2):
            for j in range(2, self.size - 2):
                if random.random() < 0.2:
                    self.grid[i, j] = CellType.OBSTACLE.value
    
    def _find_empty_spot(self, min_dist_from_pacman: int = 0) -> Tuple[int, int]:
        """Find a random empty spot in the grid."""
        while True:
            x = random.randint(1, self.size - 2)
            y = random.randint(1, self.size - 2)
            
            if self.grid[x, y] != CellType.OBSTACLE.value:
                # Check distance condition
                if min_dist_from_pacman > 0:
                    dist = abs(x - self.pacman_pos[0]) + abs(y - self.pacman_pos[1])
                    if dist < min_dist_from_pacman:
                        continue
                return (x, y)

    def step(self, action: Action) -> Tuple[Observation, float, bool]:
        """Execute one time step."""
        self.steps += 1
        reward = -0.1  # Time penalty
        
        # Move Pac-Man
        new_pos = list(self.pacman_pos)
        if action == Action.MOVE_UP:
            new_pos[0] -= 1
        elif action == Action.MOVE_DOWN:
            new_pos[0] += 1
        elif action == Action.MOVE_LEFT:
            new_pos[1] -= 1
        elif action == Action.MOVE_RIGHT:
            new_pos[1] += 1
            
        new_pos = tuple(new_pos)
        
        # Check wall collision
        if 0 <= new_pos[0] < self.size and 0 <= new_pos[1] < self.size:
            if self.grid[new_pos] != CellType.OBSTACLE.value:
                self.pacman_pos = new_pos
            else:
                reward -= 1.0  # Wall hit penalty
        
        # Handle Interactions
        cell_val = self.grid[self.pacman_pos]
        
        # 1. Eat Pellets
        if cell_val == CellType.PELLET.value:
            self.score += 10
            reward += 10.0
            self.grid[self.pacman_pos] = CellType.EMPTY.value
            
        # 2. Eat Power Pellets
        elif cell_val == CellType.POWER_PELLET.value:
            self.score += 50
            reward += 50.0
            self.power_mode = True
            self.power_timer = 20  # Steps of invulnerability
            self.grid[self.pacman_pos] = CellType.EMPTY.value
            # Scare ghosts
            for ghost in self.ghosts:
                if ghost['alive']:
                    ghost['scared'] = True
        
        # 3. Check Ghost Collisions
        ghost_hit = False
        for ghost in self.ghosts:
            if ghost['alive'] and ghost['pos'] == self.pacman_pos:
                if self.power_mode:
                    # Eat Ghost
                    self.score += 200
                    reward += 200.0
                    ghost['alive'] = False
                    ghost['pos'] = (-1, -1)  # Graveyard
                    # Respawn after delay (simplified: just dead for now)
                else:
                    # Die
                    ghost_hit = True
        
        if ghost_hit:
            self.lives -= 1
            reward -= 1000.0 # BALANCED: Death penalty (was 2000, now 1000 to balance with +5000 win)
            if self.lives <= 0:
                return self.observe(reward), reward, True  # Game Over
            else:
                # Reset positions
                self.pacman_pos = self._find_empty_spot()
                # Reset ghosts
                for g in self.ghosts:
                    if g['pos'] != (-1, -1):
                        g['pos'] = self._find_empty_spot(min_dist_from_pacman=5)
        
        # Move Ghosts
        self._move_ghosts()
        
        # Check interactions AFTER ghost move too (if they ran into us)
        if not ghost_hit:
            for ghost in self.ghosts:
                if ghost['alive'] and ghost['pos'] == self.pacman_pos:
                    if self.power_mode:
                        self.score += 200
                        reward += 200.0
                        ghost['alive'] = False
                    else:
                        self.lives -= 1
                        reward -= 1000.0 # BALANCED: Same as above
                        if self.lives <= 0:
                            return self.observe(reward), reward, True
        
        # Update Power Mode
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
                for g in self.ghosts:
                    g['scared'] = False
        
        # Check Win Condition (No pellets left)
        pellets_exist = False
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i, j] in [CellType.PELLET.value, CellType.POWER_PELLET.value]:
                    pellets_exist = True
                    break
        
        done = not pellets_exist
        if done:
            reward += 5000.0  # INCREASED: Win bonus (was 1000, now 5000)
            
        return self.observe(reward), reward, done
    
    def _move_ghosts(self):
        """Simple Ghost AI."""
        for ghost in self.ghosts:
            if not ghost['alive']:
                continue
                
            # Determine target
            if ghost['scared']:
                # Run away from Pac-Man (Anti-target)
                target = (self.size - self.pacman_pos[0], self.size - self.pacman_pos[1])
            else:
                # Chase Pac-Man
                target = self.pacman_pos
                
            # Randomness (Ghosts are 80% smart, 20% random)
            if random.random() < 0.2:
                # Random move
                moves = [(0,1), (0,-1), (1,0), (-1,0)]
                random.shuffle(moves)
            else:
                # Greedy move towards target
                moves = [(0,1), (0,-1), (1,0), (-1,0)]
                # Sort by distance to target
                g_x, g_y = ghost['pos']
                moves.sort(key=lambda m: abs((g_x+m[0])-target[0]) + abs((g_y+m[1])-target[1]))
            
            # Try moves
            for dx, dy in moves:
                nx, ny = ghost['pos'][0] + dx, ghost['pos'][1] + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.grid[nx, ny] != CellType.OBSTACLE.value:
                        # Don't overlap other ghosts
                        occupied = any(g['pos'] == (nx, ny) for g in self.ghosts if g != ghost)
                        if not occupied:
                            ghost['pos'] = (nx, ny)
                            break
    
    def observe(self, last_reward: float = 0.0) -> Observation:
        """Get observation from Pac-Man's perspective."""
        # Simple visible range (default 2, but agent can improve it)
        visible_range = 2  # This should ideally come from the agent
        # But since observe() calculates what IS visible, we define physics here.
        # Let's say physics allows seeing 2 cells away in Pac-Man world.
        
        visible_cells = np.full((self.size, self.size), CellType.UNKNOWN.value, dtype=int)
        
        # Reveal cells around pacman
        px, py = self.pacman_pos
        vr = visible_range
        
        for i in range(max(0, px - vr), min(self.size, px + vr + 1)):
            for j in range(max(0, py - vr), min(self.size, py + vr + 1)):
                # Manhattan distance check for circle-ish view
                if abs(i - px) + abs(j - py) <= vr:
                    # What is at (i,j)?
                    # Priority: Ghost > Pacman > Static Grid
                    obj_type = self.grid[i, j]
                    
                    # Override with entities
                    for ghost in self.ghosts:
                        if ghost['alive'] and ghost['pos'] == (i, j):
                            if ghost['scared']:
                                obj_type = CellType.GHOST_VULNERABLE.value
                            else:
                                obj_type = CellType.GHOST.value
                            break
                    
                    if (i, j) == self.pacman_pos:
                        obj_type = CellType.PACMAN.value
                        
                    visible_cells[i, j] = obj_type
        
        return Observation(
            visible_cells=visible_cells,
            position=self.pacman_pos,
            reward=last_reward,
            is_noisy=random.random() < 0.05  # 5% sensor noise
        )
    
    def render(self) -> str:
        """Render to ASCII string."""
        chars = {
            CellType.EMPTY.value: ' ',
            CellType.OBSTACLE.value: '#',
            CellType.PELLET.value: '.',
            CellType.POWER_PELLET.value: 'o',
            CellType.UNKNOWN.value: '?',
            CellType.GHOST.value: 'G',
            CellType.GHOST_VULNERABLE.value: 'g',
            CellType.PACMAN.value: 'C'
        }
        
        output = []
        output.append(f"Score: {self.score} | Lives: {self.lives}")
        output.append("+" + "-" * (self.size * 2) + "+")
        
        for i in range(self.size):
            line = "|"
            for j in range(self.size):
                # Determine what to draw
                val = self.grid[i, j]
                
                # Check dynamic entities
                if (i, j) == self.pacman_pos:
                    char = chars[CellType.PACMAN.value]
                else:
                    is_ghost = False
                    for ghost in self.ghosts:
                        if ghost['alive'] and ghost['pos'] == (i, j):
                            char = chars[CellType.GHOST_VULNERABLE.value] if ghost['scared'] else chars[CellType.GHOST.value]
                            is_ghost = True
                            break
                    if not is_ghost:
                        char = chars.get(val, '?')
                
                line += f"{char} "
            line += "|"
            output.append(line)
        
        output.append("+" + "-" * (self.size * 2) + "+")
        return "\n".join(output)

if __name__ == "__main__":
    # Test random play
    env = PacManWorld()
    print(env.render())
