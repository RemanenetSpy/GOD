"""
Phase 2: Minimal Simulation Environment
Grid-based world with uncertainty and partial observability.

This implements the "universe" that the AGI agent lives in, following the plan.txt specification.
"""

import numpy as np
from enum import Enum
from typing import Tuple, List, Optional, Set, Dict, Any
from dataclasses import dataclass


class CellType(Enum):
    """Types of cells in the grid world."""
    EMPTY = 0
    RESOURCE = 1
    OBSTACLE = 2
    UNKNOWN = -1  # Changed from 3 to -1 to avoid conflict with ARC color 3
    # Pac-Man extensions
    PELLET = 4
    POWER_PELLET = 5
    GHOST = 6
    GHOST_VULNERABLE = 7
    PACMAN = 8


@dataclass
class Observation:
    """What the agent observes from the environment."""
    visible_cells: np.ndarray  # Grid of visible cells
    position: Tuple[int, int]  # Agent's current position
    reward: float  # Immediate reward received
    is_noisy: bool = False  # Whether observation contains noise
    context: Optional[np.ndarray] = None # Input Grid for ARC
    train_examples: Optional[List[Dict[str, np.ndarray]]] = None # ARC training pairs
    signals: Optional[Dict[Tuple[int, int], List[str]]] = None # Phase 25: Stigmergy signals
    
class Action(Enum):
    """Actions available to the agent."""
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    OBSERVE = 4  # Active sensing - reveals more information
    WAIT = 5
    INTERACT = 6  # Collect resource, push object, etc.
    # Painting Actions (for ARC-AGI)
    PAINT_0 = 10
    PAINT_1 = 11
    PAINT_2 = 12
    PAINT_3 = 13
    PAINT_4 = 14
    PAINT_5 = 15
    PAINT_6 = 16
    PAINT_7 = 17
    PAINT_8 = 18
    PAINT_9 = 19


class GridWorld:
    """
    10×10 grid world with partial observability.
    
    Physics Laws (from plan.txt):
    - Moving costs energy
    - Observing reveals nearby cells
    - Resources increase reward
    - Obstacles block movement
    - Probabilistic events (noise, decay)
    """
    
    def __init__(
        self,
        size: int = 10,
        num_resources: int = 5,
        num_obstacles: int = 9,
        sensor_noise_level: float = 0.1,
        seed: Optional[int] = None
    ):
        """
        Initialize the grid world.
        
        Args:
            size: Grid dimensions (size × size)
            num_resources: Number of resources to place
            num_obstacles: Number of obstacles to place
            sensor_noise_level: Probability of noisy observations
            seed: Random seed for reproducibility
        """
        self.size = size
        self.num_resources = num_resources
        self.num_obstacles = num_obstacles
        self.sensor_noise_level = sensor_noise_level
        
        if seed is not None:
            np.random.seed(seed)
        
        # Initialize grid
        self.grid = np.zeros((size, size), dtype=int)
        
        # Agent state
        self.agent_position = self._get_random_empty_position()
        self.agent_energy = 100.0
        
        # Tracking
        self.discovered_cells: Set[Tuple[int, int]] = set()
        self.discovered_cells.add(self.agent_position)
        self.total_reward = 0.0
        self.step_count = 0
        
        # Place resources and obstacles
        self._place_resources()
        self._place_obstacles()
        
    def _get_random_empty_position(self) -> Tuple[int, int]:
        """Get a random empty position in the grid."""
        while True:
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            if self.grid[x, y] == CellType.EMPTY.value:
                return (x, y)
    
    def _place_resources(self):
        """Place resources randomly in the grid."""
        for _ in range(self.num_resources):
            pos = self._get_random_empty_position()
            self.grid[pos[0], pos[1]] = CellType.RESOURCE.value
    
    def _place_obstacles(self):
        """Place obstacles randomly in the grid."""
        for _ in range(self.num_obstacles):
            pos = self._get_random_empty_position()
            self.grid[pos[0], pos[1]] = CellType.OBSTACLE.value
    
    def _is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """Check if position is within grid bounds."""
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size
    
    def _is_walkable(self, pos: Tuple[int, int]) -> bool:
        """Check if position can be walked on (not an obstacle)."""
        if not self._is_valid_position(pos):
            return False
        return self.grid[pos[0], pos[1]] != CellType.OBSTACLE.value
    
    def _get_new_position(self, action: Action) -> Tuple[int, int]:
        """Calculate new position based on action."""
        x, y = self.agent_position
        
        if action == Action.MOVE_UP:
            return (x - 1, y)
        elif action == Action.MOVE_DOWN:
            return (x + 1, y)
        elif action == Action.MOVE_LEFT:
            return (x, y - 1)
        elif action == Action.MOVE_RIGHT:
            return (x, y + 1)
        else:
            return (x, y)  # No movement for other actions
    
    def _apply_noise(self, cells: np.ndarray) -> np.ndarray:
        """Apply sensor noise to observations."""
        if np.random.random() < self.sensor_noise_level:
            # Add random noise to some cells
            noisy_cells = cells.copy()
            mask = np.random.random(cells.shape) < 0.2
            noisy_cells[mask] = np.random.randint(0, 3, size=np.sum(mask))
            return noisy_cells
        return cells
    
    def observe(self, visible_range: int = 1, apply_noise: bool = True) -> Observation:
        """
        Generate observation from agent's current perspective.
        
        Agent sees only its cell + neighbors within visible_range (partial observability).
        
        Args:
            visible_range: How far the agent can see (Manhattan distance)
            apply_noise: Whether to apply sensor noise
            
        Returns:
            Observation object with visible cells and current state
        """
        x, y = self.agent_position
        
        # Create observation grid (initially all unknown)
        obs_grid = np.full((self.size, self.size), CellType.UNKNOWN.value, dtype=int)
        
        # Reveal cells within visible range
        for i in range(self.size):
            for j in range(self.size):
                manhattan_dist = abs(i - x) + abs(j - y)
                if manhattan_dist <= visible_range:
                    obs_grid[i, j] = self.grid[i, j]
                    self.discovered_cells.add((i, j))
        
        # Apply sensor noise if enabled
        is_noisy = False
        if apply_noise:
            if np.random.random() < self.sensor_noise_level:
                obs_grid = self._apply_noise(obs_grid)
                is_noisy = True
        
        return Observation(
            visible_cells=obs_grid,
            position=self.agent_position,
            reward=0.0,  # Will be set by step()
            is_noisy=is_noisy
        )
    
    def step(self, action: Action) -> Tuple[Observation, float, bool]:
        """
        Execute one step in the environment.
        
        Reward system (from plan.txt):
        - +1 for finding resource
        - -1 for hitting obstacle
        - -0.1 for moving (energy cost)
        - +0.5 for discovering new territory
        
        Args:
            action: Action to execute
            
        Returns:
            (observation, reward, done) tuple
        """
        self.step_count += 1
        reward = 0.0
        
        # Handle different actions
        if action in [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT]:
            new_pos = self._get_new_position(action)
            
            if self._is_walkable(new_pos):
                # Valid move
                old_pos = self.agent_position
                self.agent_position = new_pos
                
                # Energy cost for moving
                self.agent_energy -= 1.0
                reward -= 0.1
                
                # Check if discovered new territory
                if new_pos not in self.discovered_cells:
                    reward += 0.5
                    self.discovered_cells.add(new_pos)
                
                # Check if found resource
                if self.grid[new_pos[0], new_pos[1]] == CellType.RESOURCE.value:
                    reward += 1.0
                    self.grid[new_pos[0], new_pos[1]] = CellType.EMPTY.value  # Collect resource
            else:
                # Hit obstacle or boundary
                reward -= 1.0
        
        elif action == Action.OBSERVE:
            # Active sensing - costs energy but reveals more
            self.agent_energy -= 0.5
            reward -= 0.05
        
        elif action == Action.INTERACT:
            # Interact with current cell
            x, y = self.agent_position
            if self.grid[x, y] == CellType.RESOURCE.value:
                reward += 1.0
                self.grid[x, y] = CellType.EMPTY.value
        
        elif action == Action.WAIT:
            # Waiting costs minimal energy
            self.agent_energy -= 0.1
        
        # Apply world physics rules (probabilistic events)
        self._apply_world_rules()
        
        # Generate observation
        visible_range = 2 if action == Action.OBSERVE else 1
        observation = self.observe(visible_range=visible_range)
        observation.reward = reward
        
        self.total_reward += reward
        
        # Episode ends if energy depleted
        done = self.agent_energy <= 0
        
        return observation, reward, done
    
    def _apply_world_rules(self):
        """
        Apply world physics rules.
        
        Probabilistic events:
        - Small chance resources regenerate
        - Environment slowly changes
        """
        # Small chance of resource regeneration (very rare)
        if np.random.random() < 0.01:
            pos = self._get_random_empty_position()
            self.grid[pos[0], pos[1]] = CellType.RESOURCE.value
    
    def reset(self) -> Observation:
        """Reset the environment to initial state."""
        self.__init__(
            size=self.size,
            num_resources=self.num_resources,
            num_obstacles=self.num_obstacles,
            sensor_noise_level=self.sensor_noise_level
        )
        return self.observe()
    
    def render(self) -> str:
        """
        Render the current state as ASCII art.
        
        Returns:
            String representation of the grid
        """
        symbols = {
            CellType.EMPTY.value: '.',
            CellType.RESOURCE.value: 'R',
            CellType.OBSTACLE.value: '#',
            CellType.UNKNOWN.value: '?'
        }
        
        lines = []
        lines.append(f"Step: {self.step_count} | Energy: {self.agent_energy:.1f} | Reward: {self.total_reward:.2f}")
        lines.append(f"Position: {self.agent_position} | Discovered: {len(self.discovered_cells)}/{self.size*self.size}")
        lines.append("+" + "-" * (self.size * 2) + "+")
        
        for i in range(self.size):
            row = "|"
            for j in range(self.size):
                if (i, j) == self.agent_position:
                    row += "A "  # Agent
                else:
                    cell_type = self.grid[i, j]
                    row += symbols.get(cell_type, '?') + " "
            row += "|"
            lines.append(row)
        
        lines.append("+" + "-" * (self.size * 2) + "+")
        return "\n".join(lines)
    
    def get_state_info(self) -> dict:
        """Get current state information for debugging/analysis."""
        return {
            'position': self.agent_position,
            'energy': self.agent_energy,
            'total_reward': self.total_reward,
            'step_count': self.step_count,
            'discovered_cells': len(self.discovered_cells),
            'total_cells': self.size * self.size,
            'exploration_percentage': len(self.discovered_cells) / (self.size * self.size) * 100
        }


if __name__ == "__main__":
    # Test the environment
    print("Testing GridWorld Environment (Phase 2)")
    print("=" * 50)
    
    env = GridWorld(size=10, num_resources=5, num_obstacles=9, seed=42)
    
    print("\nInitial state:")
    print(env.render())
    
    # Test random actions
    print("\nTesting random actions:")
    for i in range(10):
        action = np.random.choice(list(Action))
        obs, reward, done = env.step(action)
        print(f"\nStep {i+1}: {action.name}")
        print(f"Reward: {reward:.2f}, Done: {done}")
        print(env.render())
        
        if done:
            print("\nEpisode ended (energy depleted)")
            break
    
    print("\nFinal state info:")
    print(env.get_state_info())
