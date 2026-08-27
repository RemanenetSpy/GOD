import numpy as np
import json
import os
from typing import Tuple, List, Dict, Optional
from environment import Action, Observation, CellType

class ARCWorld:
    """
    Adapter to run ARC-AGI tasks as a GridWorld environment.
    
    The Agent is placed on the 'Output Grid' (initially blank or filled with 0s).
    The Agent must 'paint' the cells to match the expected Output.
    The 'Input Grid' is provided as context (currently just static context).
    """
    
    def __init__(self, task_file: str, pair_index: int = 0, mode: str = 'train'):
        """
        Initialize ARC environment.
        
        Args:
            task_file: Path to JSON task file.
            pair_index: Which pair to solve (0, 1, 2...)
            mode: 'train' or 'test' pairs.
        """
        with open(task_file, 'r') as f:
            self.task_data = json.load(f)
            
        self.pair = self.task_data[mode][pair_index]
        self.input_grid = np.array(self.pair['input'])
        self.target_grid = np.array(self.pair['output'])
        
        # Load training examples for context-learning
        self.train_examples = []
        for p in self.task_data.get('train', []):
            self.train_examples.append({
                'input': np.array(p['input']),
                'output': np.array(p['output'])
            })
        
        # Dimensions
        self.height, self.width = self.target_grid.shape
        self.size = max(self.height, self.width) # For compatibility with square expectations if any
        
        # Agent State
        self.start_pos = (0, 0)
        self.agent_position = list(self.start_pos)
        self.agent_energy = 1000.0 # High energy for painting
        
        # The Canvas (Agent modifies this)
        self.current_grid = np.zeros_like(self.target_grid)
        
        # Metadata
        self.discovered_cells = set() # For compatibility
        self.step_count = 0
        self.total_reward = 0.0
        
    def reset(self) -> Observation:
        self.current_grid = np.zeros_like(self.target_grid)
        self.agent_position = list(self.start_pos)
        self.step_count = 0
        self.total_reward = 0.0
        self.agent_energy = 1000.0
        return self.observe()
        
    def observe(self, visible_range: int = 5) -> Observation:
        """
        Return observation.
        
        CRITICAL: We must expose both the canvas (current_grid) AND the input (input_grid).
        For now, we return the canvas as the primary 'visible_cells' so the agent knows where it is.
        The agent's visualizer/solver will need to look at 'input_grid' separately.
        """
        # Create a view of the current canvas
        # Pad if necessary or just return full grid if small enough? ARC grids are small (max 30x30).
        # Let's return the full grid properly padded to avoid index errors if we want a sliding window,
        # but for ARC agents usually see the whole thing.
        # Let's stick to the sliding window protocol for consistency with InfiniteMaze agent logic.
        
        padded_grid = np.pad(self.current_grid, visible_range + 1, mode='constant', constant_values=-1) 
        # -1 or similar for out of bounds?
        # InfiniteMaze uses integers. Let's strictly map to Environment CellTypes?
        # ARC colors are 0-9.
        # Environment CellTypes are 0=Empty, 1=Resource, 2=Obstacle.
        # This is a conflict!
        # Context: The Agent logic (Agent.act) interprets values.
        # We need the Agent to see "Colors" not just "Empty/Obstacle".
        # We will pass raw integer values 0-9.
        # The Agent's WorldModel key is just (x,y) -> int.
        # So we just pass the raw integers. The agent will learn 0 is background, 1 is blue, etc.
        
        x, y = self.agent_position
        
        # Extract local view
        view_size = 2 * visible_range + 1
        # Adjust indices for padding
        px, py = x + visible_range + 1, y + visible_range + 1
        
        local_view = padded_grid[px-visible_range:px+visible_range+1, py-visible_range:py+visible_range+1]
        
        # Ensure it matches expected shape
        if local_view.shape != (view_size, view_size):
            # Fallback for edges if padding math is slightly off (it shouldn't be with correct padding)
            local_view = np.zeros((view_size, view_size))
            
        return Observation(
            visible_cells=local_view,
            position=tuple(self.agent_position),
            reward=0.0,
            context=self.input_grid,
            train_examples=self.train_examples
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool]:
        self.step_count += 1
        reward = 0.0
        
        x, y = self.agent_position
        
        # Movement
        new_x, new_y = x, y
        if action == Action.MOVE_UP:
            new_x = max(0, x - 1)
        elif action == Action.MOVE_DOWN:
            new_x = min(self.height - 1, x + 1)
        elif action == Action.MOVE_LEFT:
            new_y = max(0, y - 1)
        elif action == Action.MOVE_RIGHT:
            new_y = min(self.width - 1, y + 1)
            
        if (new_x, new_y) == (x, y) and action in [Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT]:
            reward -= 1.0 # Penalty for hitting boundary
        
        self.agent_position = [new_x, new_y]
        
        # Painting Actions
        # Action.PAINT_0 is 10
        if 10 <= action.value <= 19:
            color = action.value - 10
            
            # Check if this painting action improves the state
            old_val = self.current_grid[x, y]
            target_val = self.target_grid[x, y]
            
            self.current_grid[x, y] = color
            
            if color == target_val:
                if old_val != target_val:
                    reward += 1.0 # Connected a pixel correctly!
                else:
                    reward -= 0.1 # Redundant paint
            else:
                reward -= 1.0 # Wrong color!
                
        # Calculate episode completeness
        # Done if grid matches target exactly
        matches = np.array_equal(self.current_grid, self.target_grid)
        done = matches or self.step_count > 1000
        
        if matches:
            reward += 100.0 # Big finish bonus
            
        self.total_reward += reward
        
        obs = self.observe()
        obs.reward = reward
        return obs, reward, done


def run_agent_with_motion(agent, task_data: Dict):
    """
    Controller loop: adapts grid size and sweeps across the ARC grid.
    Agent logic (paint reflex) stays untouched.
    """
    # Get grid dimensions from first train input
    # Note: Assuming train[0] for demo purposes
    context = np.array(task_data["train"][0]["input"])
    rows, cols = context.shape

    # Initialize agent position
    x, y = 0, 0

    # Copy world (output grid starts blank)
    world_grid = np.zeros_like(context)

    while x < rows:
        while y < cols:
            # Construct observation for the agent at this position
            # We explicitly pass the context (Input Grid)
            obs = Observation(
                visible_cells=np.zeros((3,3)), # Dummy view
                position=(x, y),
                reward=0.0,
                context=context
            )
            
            # Sync Agent's World Model with reality (so Reflex knows current state)
            agent.state.world_model.grid[(x, y)] = world_grid[x, y]
            
            # Ask Agent to Act (Trigger Reflex)
            # "Agent reflex: paint if mismatch"
            action = agent.choose_action(obs)
            
            # Apply Action if it's a PAINT action
            if action.value >= 10:
                color = action.value - 10
                world_grid[x, y] = color # Paint
                
            # Move right until end of row
            y += 1

        # End of row → move down
        x += 1
        y = 0

    return world_grid
