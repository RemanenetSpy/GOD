"""
Infinite Deterministic Maze Environment

A procedurally-generated, infinite maze that tests AGI capabilities:
- Exploration (infinite space)
- Prediction (infer generation rules)
- Compression (store infinite maze in finite memory)
- Planning (navigate without full map)
"""

import numpy as np
from typing import Tuple, Dict, Set
from enum import Enum

# Handle imports from both src/ and scripts/
from environment import Observation

class CellType(Enum):
    """Cell types in the maze"""
    WALL = 0
    PATH = 1
    VISITED = 2
    GOAL = 3
    START = 4

class InfiniteMaze:
    """
    Infinite procedurally-generated maze environment.
    
    Uses chunk-based generation with deterministic seeding.
    Each chunk is 16×16 cells, generated on-demand.
    """
    
    def __init__(self, seed: int = 42, chunk_size: int = 32, visible_range: int = 5):
        """
        Initialize infinite maze.
        
        Args:
            seed: World seed for deterministic generation
            chunk_size: Size of each chunk (default 32x32 for better mazes)
            visible_range: How far agent can see
        """
        self.seed = seed
        self.chunk_size = chunk_size
        self.visible_range = visible_range
        
        # Chunk cache: {(chunk_x, chunk_y): np.ndarray}
        self.chunks: Dict[Tuple[int, int], np.ndarray] = {}
        
        # Agent state
        self.agent_pos = (0, 0)  # Start at origin
        self.visited_cells: Set[Tuple[int, int]] = {(0, 0)}
        
        # Metrics
        self.steps = 0
        self.total_reward = 0.0
        self.cells_explored = 1
        
        # Phase 25: Signal Layer (Stigmergy)
        # Map: (x, y) -> List[str] (list of symbols dropped at this cell)
        self.signals: Dict[Tuple[int, int], list] = {}
        
        # Treasures (deterministic large rewards)
        self.treasures_collected: Set[Tuple[int, int]] = set()

        # Goals (legacy support for tests, mapped to treasures)
        self.goals: Set[Tuple[int, int]] = set()
        
        # Ensure spawn point is navigable
        self._ensure_spawn_accessible()

    def _get_doors(self, chunk_x: int, chunk_y: int) -> Dict[str, bool]:
        """
        Determine which walls have doors using deterministic hashing.
        Returns dict with 'N', 'S', 'E', 'W' booleans.
        """
        doors = {}
        # Hash including direction ensures consistency between adjacent chunks
        # e.g. Chunk(0,0) East door MUST match Chunk(1,0) West door
        
        # North door (y-1) <-> South door of chunk above
        doors['N'] = hash((self.seed, chunk_x, chunk_y, 'N')) % 2 == 0
        
        # South door (y+1) <-> North door of chunk below
        doors['S'] = hash((self.seed, chunk_x, chunk_y + 1, 'N')) % 2 == 0
        
        # West door (x-1) <-> East door of chunk left
        doors['W'] = hash((self.seed, chunk_x, chunk_y, 'W')) % 2 == 0
        
        # East door (x+1) <-> West door of chunk right
        doors['E'] = hash((self.seed, chunk_x + 1, chunk_y, 'W')) % 2 == 0
        
        # Ensure origin chunk always has at least one door to avoid getting stuck immediately
        if chunk_x == 0 and chunk_y == 0 and not any(doors.values()):
            doors['E'] = True 
            
        return doors

    def _generate_chunk(self, seed: int, chunk_x: int, chunk_y: int) -> np.ndarray:
        """
        Generate a maze chunk with connectivity doors.
        """
        rng = np.random.RandomState(seed)
        size = self.chunk_size
        
        # Start with all walls
        maze = np.full((size, size), CellType.WALL.value, dtype=int)
        
        # Determine doors
        doors = self._get_doors(chunk_x, chunk_y)
        
        # Carve doors and add them to generation stack
        stack = []
        mid = size // 2
        
        # Always carve a clear center area to ensure paths can connect
        # This acts as a "hub" for the recursive backtracker
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if 0 <= mid+dx < size and 0 <= mid+dy < size:
                    maze[mid+dx, mid+dy] = CellType.PATH.value
        stack.append((mid, mid))

        # Carve doors
        if doors['N']:
            # Top middle
            maze[mid, 0] = CellType.PATH.value
            stack.append((mid, 0))
        if doors['S']:
            # Bottom middle
            maze[mid, size-1] = CellType.PATH.value
            stack.append((mid, size-1))
        if doors['W']:
            # Left middle
            maze[0, mid] = CellType.PATH.value
            stack.append((0, mid))
        if doors['E']:
            # Right middle
            maze[size-1, mid] = CellType.PATH.value
            stack.append((size-1, mid))

        # Recursive backtracking
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while stack:
            # Pop random element for more "organic" maze, or end for "long corridors"
            # Using -1 makes it Depth-First (long corridors)
            # Using random makes it Prim-like (sprawling)
            # Let's mix it up deterministically
            if rng.rand() < 0.5:
                idx = -1
            else:
                idx = rng.randint(0, len(stack))
                
            x, y = stack[idx]
            
            # Find neighbors that are walls (candidates to carve to)
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + (dx*2), y + (dy*2) # Jump 2 for walls
                
                if 0 <= nx < size and 0 <= ny < size:
                    if maze[nx, ny] == CellType.WALL.value:
                        neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                # Choose random neighbor
                n_idx = rng.randint(len(neighbors))
                nx, ny, dx, dy = neighbors[n_idx]
                
                # Carve path to neighbor (remove wall in between)
                maze[x+dx, y+dy] = CellType.PATH.value
                maze[nx, ny] = CellType.PATH.value
                
                stack.append((nx, ny))
            else:
                stack.pop(idx)
                
        # Post-processing: Make sure doors are actually open!
        # Sometimes backtracker might isolate them if we're not careful.
        # Force carve path from door to nearest open space if needed.
        if doors['N']: maze[mid, 0] = CellType.PATH.value
        if doors['S']: maze[mid, size-1] = CellType.PATH.value
        if doors['W']: maze[0, mid] = CellType.PATH.value
        if doors['E']: maze[size-1, mid] = CellType.PATH.value

        # Place Treasure? (Deterministic: every 5th chunk diagonally)
        if (chunk_x + chunk_y) % 5 == 0 and (chunk_x != 0 or chunk_y != 0):
             # Find a random path spot
             path_cells = np.argwhere(maze == CellType.PATH.value)
             if len(path_cells) > 0:
                 tx, ty = path_cells[rng.randint(len(path_cells))]
                 maze[tx, ty] = CellType.GOAL.value

        return maze
    
    def _chunk_coords(self, x: int, y: int) -> Tuple[int, int]:
        """Convert absolute coordinates to chunk coordinates"""
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        return (chunk_x, chunk_y)
    
    def _local_coords(self, x: int, y: int) -> Tuple[int, int]:
        """Convert absolute coordinates to local chunk coordinates"""
        local_x = x % self.chunk_size
        local_y = y % self.chunk_size
        return (local_x, local_y)

    def get_chunk(self, chunk_x: int, chunk_y: int) -> np.ndarray:
        """Get or generate a chunk."""
        key = (chunk_x, chunk_y)
        if key not in self.chunks:
            chunk_seed = hash((self.seed, chunk_x, chunk_y)) % (2**32)
            self.chunks[key] = self._generate_chunk(chunk_seed, chunk_x, chunk_y)
        return self.chunks[key]

    def _ensure_spawn_accessible(self):
        """Ensure spawn point is clear."""
        chunk = self.get_chunk(0, 0)
        # Clear 3x3 at 0,0 (inside the 0,0 chunk, which is local coords)
        # Assuming 0,0 is center of universe, map it to middle of chunk 0,0?
        # Actually user spec says 0,0 is origin.
        # Local coords of (0,0) depends on how we map global to local.
        # Impl: 0,0 global -> chunk 0,0 -> local 0,0.
        # So we clear top-left of chunk 0,0. 
        # But wait, our generation uses 'mid' as hub. 
        # Let's just force clear 0,0 to 2,2.
        for x in range(3):
            for y in range(3):
                chunk[x, y] = CellType.PATH.value
                
    def get_cell(self, x: int, y: int) -> CellType:
        """
        Get cell type at absolute coordinates.
        
        Args:
            x: Absolute X coordinate
            y: Absolute Y coordinate
            
        Returns:
            CellType at that location
        """
        chunk_x, chunk_y = self._chunk_coords(x, y)
        local_x, local_y = self._local_coords(x, y)
        
        chunk = self.get_chunk(chunk_x, chunk_y)
        cell_value = chunk[local_x, local_y]
        
        return CellType(cell_value)

    def drop_signal(self, x: int, y: int, symbol: str):
        """Phase 25: Stigmergy - Drop a signal at location."""
        if (x, y) not in self.signals:
            self.signals[(x, y)] = []
        if symbol not in self.signals[(x, y)]:
            self.signals[(x, y)].append(symbol)
            # Limit signals per cell to prevent spam
            if len(self.signals[(x, y)]) > 5:
                self.signals[(x, y)].pop(0)

    def observe(self, agent_pos=None) -> Observation:
        """
        Generate observation for current agent position.
        Args:
            agent_pos: Optional override for multi-agent support
        Returns:
            Observation with visible area
        """
        x, y = agent_pos if agent_pos else self.agent_pos
        size = 2 * self.visible_range + 1
        
        # Build visible grid
        visible_grid = np.zeros((size, size), dtype=float)
        visible_signals = {}
        
        for i in range(size):
            for j in range(size):
                world_x = x + i - self.visible_range
                world_y = y + j - self.visible_range
                
                # Get Cell Data
                cell = self.get_cell(world_x, world_y)
                
                # Get Signal Data
                if (world_x, world_y) in self.signals:
                     visible_signals[(i, j)] = self.signals[(world_x, world_y)]
                
                # Remap Logic (Same as before)
                if cell == CellType.WALL:
                    visible_grid[i, j] = 2 # OBSTACLE
                elif cell == CellType.PATH or cell == CellType.VISITED:
                    visible_grid[i, j] = 0 # EMPTY
                elif cell == CellType.GOAL:
                    visible_grid[i, j] = 1 # RESOURCE (Treasure)
                elif cell == CellType.START:
                    visible_grid[i, j] = 0 # EMPTY
                else:
                    visible_grid[i, j] = 3 # UNKNOWN
        
        return Observation(
            visible_cells=visible_grid,
            position=(x, y),
            reward=0.0,
            context=visible_grid, # Reverted: context is just grid for RuleEngine
            signals=visible_signals # New: explicit signals channel
        )

    def step(self, action) -> Tuple[Observation, float, bool]:
        """Execute action with parameters from design doc."""
        from environment import Action
        
        x, y = self.agent_pos
        dx, dy = 0, 0
        if action == Action.MOVE_UP: dx = -1
        elif action == Action.MOVE_DOWN: dx = 1
        elif action == Action.MOVE_LEFT: dy = -1
        elif action == Action.MOVE_RIGHT: dy = 1
        
        new_pos = (x + dx, y + dy)
        cell = self.get_cell(new_pos[0], new_pos[1])
        
        reward = -0.01 # Lower time penalty as per design
        
        if cell == CellType.WALL:
            reward -= 1.0 # Lower wall penalty (physics agent hates, quantum might try)
            # Stay in place
        else:
            self.agent_pos = new_pos
            
            # Discovery bonus
            if new_pos not in self.visited_cells:
                self.visited_cells.add(new_pos)
                self.cells_explored += 1
                reward += 1.0
            
            # Treasure?
            if cell == CellType.GOAL:
                if new_pos not in self.treasures_collected:
                    reward += 50.0
                    self.treasures_collected.add(new_pos)
                    # Note: we don't remove the goal from the map (it's part of the maze)
                    # but we only reward once.
        
        self.steps += 1
        self.total_reward += reward
        
        obs = self.observe()
        obs.reward = reward
        return obs, reward, False
    
    def render(self) -> str:
        """Render visible area as ASCII"""
        x, y = self.agent_pos
        size = 2 * self.visible_range + 1
        
        lines = []
        for i in range(size):
            row = []
            for j in range(size):
                world_x = x + i - self.visible_range
                world_y = y + j - self.visible_range
                
                if (world_x, world_y) == self.agent_pos:
                    row.append('@')
                elif (world_x, world_y) in self.goals:
                    row.append('G')
                else:
                    cell = self.get_cell(world_x, world_y)
                    if cell == CellType.WALL:
                        row.append('█')
                    elif cell == CellType.PATH:
                        if (world_x, world_y) in self.visited_cells:
                            row.append('·')
                        else:
                            row.append(' ')
                    else:
                        row.append('?')
            lines.append(''.join(row))
        
        return '\n'.join(lines)
    
    def get_stats(self) -> dict:
        """Get environment statistics"""
        return {
            'steps': self.steps,
            'total_reward': self.total_reward,
            'cells_explored': self.cells_explored,
            'chunks_generated': len(self.chunks),
            'goals_remaining': len(self.goals),
            'agent_position': self.agent_pos
        }


if __name__ == "__main__":
    # Quick test
    maze = InfiniteMaze(seed=999, visible_range=7)
    
    print("Infinite Maze Test")
    print("=" * 50)
    print(maze.render())
    print("\nStats:", maze.get_stats())
    
    # Test movement
    from src.core import Action
    for _ in range(10):
        obs, reward, done = maze.step(Action.MOVE_RIGHT)
        print(f"\nStep {maze.steps}: Reward={reward:.1f}")
        print(maze.render())
