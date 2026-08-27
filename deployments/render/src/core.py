"""
Phase 3: Core Data Structures
Fundamental objects for the AGI system following the "God Equation" from plan.txt.

State Definition:
    S_t = {W_t, B_t, F_t}
    
Where:
    W_t = world state (agent's internal model of reality)
    B_t = belief state (probabilities over possible worlds)
    F_t = frame of reference (agent's perspective, history, limitations)
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from copy import deepcopy
from environment import CellType, Observation
from abstraction import RuleDiscoveryEngine, AbstractRule


from enum import Enum

class PillarType(Enum):
    """The Four Pillars of the God Equation (Specializations)."""
    QUANTUM = "quantum"        # Uncertainty, Exploration
    RELATIVITY = "relativity"  # Perspective, Empathy
    INFORMATION = "information" # Patterns, Rules
    PHYSICS = "physics"        # Determinism, Efficiency
    GENERAL = "general"        # Balanced (Default)

@dataclass
class FrameOfReference:
    """
    Agent's perspective, history, and limitations (F_t).
    
    Relativity-inspired: All knowledge is relative to the agent's viewpoint.
    """
    agent_id: str  # Unique ID (Phase 5)
    position: Tuple[int, int]  # Current position in the world
    visible_range: int = 1  # How far the agent can see (Manhattan distance)
    planning_depth: int = 3  # How many steps ahead to simulate (dynamic)se 4)
    history: List[Observation] = field(default_factory=list)  # Observation history
    sensor_noise_level: float = 0.1  # Sensor noise probability
    pillar_type: PillarType = PillarType.GENERAL # Specialization of the agent's "mindset"
    
    def update(self, new_position: Tuple[int, int], observation: Observation):
        """Update frame based on action and observation."""
        self.position = new_position
        self.history.append(observation)
        
        # Limit history size to prevent unbounded growth
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def adjust_visible_range(self, delta: int):
        """Dynamically adjust visible range (self-modification)."""
        self.visible_range = max(1, min(10, self.visible_range + delta))

@dataclass
class BeliefState:
    """
    Probabilities over possible worlds (B_t).
    
    Quantum-inspired: Agent maintains superposition of multiple possible world states.
    
    For efficiency, we use a particle filter approach where each "particle" 
    represents a possible world state with an associated probability.
    """
    grid_beliefs: np.ndarray = field(default=None) # Placeholder for type hint

    def __init__(self, height: int = 15, width: int = 15, num_particles: int = 100, grid_beliefs: np.ndarray = None):
        """
        Initialize belief state.
        
        Args:
            height: Height of the grid world
            width: Width of the grid world
            num_particles: Number of particles for belief representation
        """
        self.height = height
        self.width = width
        self.num_particles = num_particles
        
        # If initialized with grid_beliefs (Phase 3 style), use it to seed
        if grid_beliefs is not None:
             self.grid_beliefs = grid_beliefs
        
        # Each particle is a possible world state (grid configuration)
        # For simplicity, we track beliefs about cell types
        self.particles: List[np.ndarray] = []
        self.weights: np.ndarray = np.ones(num_particles) / num_particles
        
        # Initialize particles with uniform prior
        for _ in range(num_particles):
            # Random initial belief about world
            particle = np.random.randint(0, 3, size=(height, width))
            self.particles.append(particle)
    
    def update(self, observation: Observation):
        """
        Update beliefs given new observation (Bayesian-quantum hybrid).
        
        From plan.txt:
            B_{t+1}(s) = Normalize(B_t(s) · P(O_t | s))
        
        This is the quantum-like collapse toward more probable states.
        """
        # Update weights based on likelihood of observation given each particle
        for i, particle in enumerate(self.particles):
            likelihood = self._compute_likelihood(particle, observation)
            self.weights[i] *= likelihood
        
        # Normalize to maintain total probability = 1
        if self.weights.sum() > 0:
            self.weights /= self.weights.sum()
        else:
            # Reset if all weights are zero (shouldn't happen but safety check)
            self.weights = np.ones(self.num_particles) / self.num_particles
        
        # Resample particles if effective sample size is too low
        effective_sample_size = 1.0 / np.sum(self.weights ** 2)
    def resize(self, h: int, w: int):
        """
        Resize the belief state to match new environment dimensions.
        """
        if self.height == h and self.width == w:
            return
            
        self.height = h
        self.width = w
        
        # Re-initialize particles with new size
        self.particles = []
        for _ in range(self.num_particles):
            # Random initial belief about world
            particle = np.random.randint(0, 3, size=(h, w))
            self.particles.append(particle)
            
        # Reset weights
        self.weights = np.ones(self.num_particles) / self.num_particles
        
    def update(self, observation: Observation):
        """
        Update beliefs given new observation (Bayesian-quantum hybrid).
        """
        # Update weights based on likelihood of observation given each particle
        for i, particle in enumerate(self.particles):
            likelihood = self._compute_likelihood(particle, observation)
            self.weights[i] *= likelihood
        
        # Normalize to maintain total probability = 1
        if self.weights.sum() > 0:
            self.weights /= self.weights.sum()
        else:
            self.weights = np.ones(self.num_particles) / self.num_particles
        
        # Resample particles if effective sample size is too low
        effective_sample_size = 1.0 / np.sum(self.weights ** 2)
        if effective_sample_size < self.num_particles / 2:
            self._resample()

    def _compute_likelihood(self, particle: np.ndarray, observation: Observation) -> float:
        """
        Compute P(observation | particle).
        """
        # Compare visible cells in observation with particle's prediction
        # FIX: Observation might be smaller than particle (partial view).
        # We must align them based on observation.position.
        
        obs_h, obs_w = observation.visible_cells.shape
        part_h, part_w = particle.shape
        
        # Assuming observation is square and centered on position
        # radius = (obs_size - 1) // 2
        r_x = (obs_h - 1) // 2
        r_y = (obs_w - 1) // 2
        
        cx, cy = observation.position
        
        # Calculate global bounds of the observation window
        start_x = cx - r_x
        start_y = cy - r_y
        end_x = start_x + obs_h
        end_y = start_y + obs_w
        
        # Calculate valid intersection with particle grid
        p_start_x = max(0, start_x)
        p_start_y = max(0, start_y)
        p_end_x = min(part_h, end_x)
        p_end_y = min(part_w, end_y)
        
        # If no overlap (observation entirely off grid?), return neutral
        if p_start_x >= p_end_x or p_start_y >= p_end_y:
            return 1.0

        # Calculate corresponding offsets in observation grid
        o_start_x = p_start_x - start_x
        o_start_y = p_start_y - start_y
        o_end_x = o_start_x + (p_end_x - p_start_x)
        o_end_y = o_start_y + (p_end_y - p_start_y)
        
        # Extract slices
        obs_slice = observation.visible_cells[o_start_x:o_end_x, o_start_y:o_end_y]
        part_slice = particle[p_start_x:p_end_x, p_start_y:p_end_y]
        
        # Now we can safely mask
        visible_mask = obs_slice != CellType.UNKNOWN.value
        
        # Also ignore padding (-1) if any
        # Assuming CellType.UNKNOWN is not -1. If adapter returns -1, we should treat it as ignore.
        visible_mask &= (obs_slice != -1)
        
        if not np.any(visible_mask):
            return 1.0
            
        # Vectorized matching on the valid slice
        matches = np.sum(part_slice[visible_mask] == obs_slice[visible_mask])
        total_visible = np.sum(visible_mask)
        
        # Likelihood based on match percentage
        match_rate = matches / total_visible if total_visible > 0 else 0.5
        
        # Account for sensor noise
        if observation.is_noisy:
            return max(0.5 + 0.5 * match_rate, 1e-10)
        else:
            return max(match_rate ** 2, 1e-10)
    
    def _resample(self):
        """Resample particles based on weights (particle filter resampling)."""
        indices = np.random.choice(
            self.num_particles,
            size=self.num_particles,
            p=self.weights
        )
        # Deepcopy is slow, but necessary if particles are mutable objects. 
        # Since they are numpy arrays, we can use array copying which is faster.
        # However, indices might pick the same particle multiple times.
        # We'll stick to list comp for safety but optimize if needed.
        self.particles = [self.particles[i].copy() for i in indices]
        self.weights = np.ones(self.num_particles) / self.num_particles
    
    def get_belief_map(self) -> np.ndarray:
        """
        Get the most likely world state (collapse superposition).
        Returns weighted average of all particles.
        """
        if not self.particles:
             return np.zeros((self.grid_size, self.grid_size))
             
        # Vectorized weighted average
        # Stack particles: (num_particles, H, W)
        particles_stack = np.array(self.particles)
        # Weights: (num_particles, 1, 1)
        weights_reshaped = self.weights[:, np.newaxis, np.newaxis]
        
        return np.sum(particles_stack * weights_reshaped, axis=0)
    
    def get_uncertainty_map(self) -> np.ndarray:
        """
        Get uncertainty (entropy) at each cell.
        Vectorized implementation for performance.
        """
        if not self.particles:
             return np.zeros((self.height, self.width))

        # Stack particles: (num_particles, H, W)
        particles_stack = np.array(self.particles)
        
        # We need P(cell_value=k) for each cell (i,j)
        # Max cell value is small (around 7 for Pac-Man types)
        max_val = 8 
        entropy_map = np.zeros((self.height, self.width))
        
        # Iterate through possible values to build probability map
        # This is strictly faster than iterating pixels (10x10=100) if max_val (8) is small
        probs = np.zeros((self.height, self.width, max_val))
        
        for val in range(max_val):
            # Count how many particles have this value at each position
            # (num_particles, H, W) -> (H, W) sum
            matches = (particles_stack == val)
            # Weighted sum of matches
            weighted_matches = np.sum(matches * self.weights[:, np.newaxis, np.newaxis], axis=0)
            probs[:, :, val] = weighted_matches
            
        # Normalize (should already be close to 1 if weights sum to 1)
        prob_sum = np.sum(probs, axis=2, keepdims=True) + 1e-10
        probs = probs / prob_sum
        
        # Calculate Entropy: -sum(p * log2(p))
        # Mask out zero probabilities to avoid log(0)
        valid_mask = probs > 1e-10
        log_probs = np.zeros_like(probs)
        log_probs[valid_mask] = np.log2(probs[valid_mask])
        
        entropy_map = -np.sum(probs * log_probs, axis=2)
        
        return entropy_map


class WorldModel:
    """
    Agent's internal model of reality (W_t).
    
    Computational-physics inspired: The model evolves via explicit rules.
    Information-theoretic: The model compresses and simplifies over time.
    """
    
    def __init__(self, agent_id: str = "agent_0", height: int = 15, width: int = 15, vocabulary_builder: Any = None, motif_memory: Any = None):
        """Initialize world model."""
        self.agent_id = agent_id # Identity (Phase 5)
        self.height = height
        self.width = width
        
        # Internal representation of the world
        # Changed to Dict for infinite world support: (x, y) -> cell_value
        self.grid: Dict[Tuple[int, int], float] = {}
        
        # Learned rules about the world
        self.rules: List[Dict[str, Any]] = []
        
        # Phase 9: Saliency map cache
        self.cached_saliency: Optional[np.ndarray] = None
        self.cached_enclosure: Dict[int, np.ndarray] = None # Phase 10
        self.cached_objects: List['Object'] = [] # Phase 11
        self.learned_transformations: List[Any] = []
        
        # Phase 17: Abstraction Engine
        # Phase 21: Sovereign Memory Injection
        self.abstraction_engine = RuleDiscoveryEngine(
            agent_id=agent_id, 
            vocabulary_builder=vocabulary_builder, 
            motif_memory=motif_memory
        )
        self.discovered_abstract_rules: List[AbstractRule] = []
        
        # Discovered patterns
        self.patterns: List[Dict[str, Any]] = []
        
        # Statistics for learning
        # Changed to Dict for infinite world support: (x, y) -> count
        self.cell_visit_counts: Dict[Tuple[int, int], int] = {}  # Cumulative (all runs)
        self.current_run_visits: Dict[Tuple[int, int], int] = {}  # Current run only
        self.cell_reward_history: Dict[Tuple[int, int], List[float]] = {}
        
        # Dynamic memory limits (Phase 4)
        self.max_patterns = 50
        self.max_rules = 20
        
    def resize(self, h: int, w: int):
        """
        Resize world model to match new environment.
        """
        if self.height == h and self.width == w:
            return
            
        self.height = h
        self.width = w
        # For dictionary-based grid, strictly we don't need to do much unless we want to filter out-of-bounds.
        # But we should clear caches that depend on shape.
        self.cached_saliency = None
        self.cached_enclosure = None
        self.cached_objects = []
        self.grid = {} # Reset grid memory on resize (assuming new task/episode)
        self.cell_visit_counts = {}
        self.current_run_visits = {}
        self.cell_reward_history = {}
        self.cell_reward_history = {}
        
    def update(self, belief_state: BeliefState, observation: Observation):
        """
        Update world model based on beliefs.
        """
        # Update internal grid with belief-weighted information
        # Note: We skip full belief map integration for infinite maze efficiency for now
        # and rely more on direct observation, as belief state is still fixed-grid.
        
        # Merge observation into model
        if observation.visible_cells is not None:
            # Handle standard Observation with numpy array (local view)
            size = observation.visible_cells.shape[0]
            radius = (size - 1) // 2
            agent_x, agent_y = observation.position
            
            for i in range(size):
                for j in range(size):
                    val = observation.visible_cells[i, j]
                    if val != CellType.UNKNOWN.value:
                        # Map local observation coords to global coords
                        # Observation is centered on agent
                        # visible_cells[radius, radius] is at (agent_x, agent_y)
                        world_x = agent_x + (i - radius)
                        world_y = agent_y + (j - radius)
                        self.grid[(world_x, world_y)] = val
        
        # Update statistics
        pos = observation.position
        
        # Initialize if not present
        if pos not in self.cell_visit_counts:
            self.cell_visit_counts[pos] = 0
        if pos not in self.current_run_visits:
            self.current_run_visits[pos] = 0
            
        self.cell_visit_counts[pos] += 1  # Cumulative (all runs)
        self.current_run_visits[pos] += 1  # Current run only
        
        if pos not in self.cell_reward_history:
            self.cell_reward_history[pos] = []
        self.cell_reward_history[pos].append(observation.reward)
    
    def compress(self):
        """
        Compress the model (information-theoretic learning).
        """
        # Limit grid storage if it gets too large?
        # For now, just Limit pattern storage
        if len(self.patterns) > self.max_patterns:
            self.patterns = self.patterns[-self.max_patterns:]
    
    def discover_patterns(self) -> List[Dict[str, Any]]:
        """
        Discover patterns in the world.
        """
        new_patterns = []
        
        # Pattern: High reward cells
        for pos, rewards in self.cell_reward_history.items():
            if len(rewards) >= 3:
                avg_reward = np.mean(rewards)
                if abs(avg_reward) > 0.5: # Track both high positive and negative
                    # 1. Absolute Position Pattern
                    new_patterns.append({
                        'type': 'high_reward_cell' if avg_reward > 0 else 'avoid_cell',
                        'position': pos,
                        'avg_reward': avg_reward,
                        'confidence': min(len(rewards) / 10.0, 1.0)
                    })
                    
                    # 2. Relative Neighbor Pattern (Phase 5.5 Fix)
                    # Check neighbors for consistent features
                    # Directions: Up, Down, Left, Right
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    dir_names = ["UP", "DOWN", "LEFT", "RIGHT"]
                    
                    for d_idx, d in enumerate(directions):
                        n_pos = (pos[0] + d[0], pos[1] + d[1])
                        
                        # Check if we have knowledge of this neighbor
                        if n_pos in self.grid:
                            n_type = self.grid[n_pos]
                            
                            # We found a feature. Is it consistent across ALL history?
                            # For simplicity in this demo, we just log it as a candidate.
                            new_patterns.append({
                                'type': 'neighbor_rule',
                                'direction': dir_names[d_idx],
                                'neighbor_type': n_type,
                                'outcome': 'good' if avg_reward > 0 else 'bad',
                                'confidence': 0.5 
                            })

        # Filter Patterns (Naive: Just keep them for now)
        self.patterns.extend(new_patterns)
        return new_patterns

    def analyze_context(self, context: np.ndarray) -> np.ndarray:
        """
        Phase 9: Intelligent Exploration.
        Generate a 'Saliency Map' from the context (Input Grid).
        High values = Interesting areas (Objects, Edges).
        
        Saliency Heuristics:
        1. Non-background attractor (assuming 0 is bg).
        2. Edge detection (simple gradient).
        """
        # Ensure context is numpy array
        context = np.array(context)
        saliency = np.zeros_like(context, dtype=float)
        
        # 1. Object Saliency (Non-zero pixels attract)
        # We assume 0 is usually background.
        saliency[context != 0] += 1.0
        
        # 2. Edge Detection (Change in color = Information)
        # Vectorized neighbor comparison
        if context.ndim == 2:
            # Vertical edges
            v_diff = (context[:-1, :] != context[1:, :])
            saliency[:-1, :][v_diff] += 0.5
            saliency[1:, :][v_diff] += 0.5
            
            # Horizontal edges
            h_diff = (context[:, :-1] != context[:, 1:])
            saliency[:, :-1][h_diff] += 0.5
            saliency[:, 1:][h_diff] += 0.5
        
        return saliency

    def detect_enclosed_regions(self, context: np.ndarray) -> Dict[int, np.ndarray]:
        """
        Phase 10: Topology.
        Returns masks of areas enclosed by specific colors.
        enclosed_masks[color] = boolean mask of areas inside 'color' loops.
        """
        h, w = context.shape
        enclosed_masks = {}
        
        # For each distinct object color in context
        unique_colors = np.unique(context)
        for outline_color in unique_colors:
            if outline_color == 0: continue # Skip background itself
            
            # Create mask where this color exists
            walls = (context == outline_color)
            
            # Flood fill from outer edges to find "Outside"
            # 0 = Unknown, 1 = Outside, 2 = Inside (Wall)
            # Actually simpler: Mask 0 = Empty/Other, 1 = Wall.
            # We want to find Empty regions NOT reachable from border.
            
            # Start a flood fill from all border pixels that are NOT the outline color
            visited = np.zeros((h, w), dtype=bool)
            queue = []
            
            # Initialize borders
            for r in range(h):
                if not walls[r, 0]: queue.append((r, 0))
                if not walls[r, w-1]: queue.append((r, w-1))
            for c in range(w):
                if not walls[0, c]: queue.append((0, c))
                if not walls[h-1, c]: queue.append((h-1, c))
            
            # Standard BFS
            bg_mask = np.zeros((h, w), dtype=bool)
            for r, c in queue:
                visited[r, c] = True
                bg_mask[r, c] = True
            
            idx = 0
            while idx < len(queue):
                r, c = queue[idx]
                idx += 1
                
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < h and 0 <= nc < w:
                        if not visited[nr, nc] and not walls[nr, nc]:
                            visited[nr, nc] = True
                            bg_mask[nr, nc] = True
                            queue.append((nr, nc))
                            
            # Any non-wall node that was NOT visited is INSIDE the loop
            inside_mask = (~bg_mask) & (~walls)
            if np.any(inside_mask):
                enclosed_masks[outline_color] = inside_mask
                
        return enclosed_masks

    def get_center_of_mass(self, mask: np.ndarray) -> Tuple[int, int]:
        """Phase 13: Compute center of mass for a boolean mask."""
        coords = np.argwhere(mask)
        if len(coords) == 0: return (-1, -1)
        center = coords.mean(axis=0)
        return int(round(center[0])), int(round(center[1]))

    def learn_transformation_rules(self, context: np.ndarray, current_grid: Dict[Tuple[int, int], float]) -> List[Any]:
        """
        Phase 17.2: PURE DISCOVERY - Zero hardcoded rules.
        All patterns discovered through deep search, not pre-written heuristics.
        """
        # Format training data
        training_data = []
        for (x, y), out_val in current_grid.items():
            if 0 <= x < context.shape[0] and 0 <= y < context.shape[1]:
                in_val = context[x, y]
                training_data.append((x, y, int(in_val), int(out_val)))
        
        if not training_data:
            return []
        
        # PURE DISCOVERY: Let abstraction engine find patterns
        abstract_rules = self.abstraction_engine.discover_rules(context, training_data)
        self.discovered_abstract_rules = abstract_rules
        
        # Convert to TransformationRule format
        new_rules = []
        for ar in abstract_rules:
            new_rules.append(TransformationRule(
                input_color=-1,  # Handled by precondition
                output_color=-1,  # Handled by transform
                condition_type="ABSTRACT",
                parameter=ar,  # Store AbstractRule
                confidence=ar.confidence
            ))
        
        if new_rules:
            print(f"[PURE DISCOVERY] Found {len(new_rules)} rules via deep search")
        
        return new_rules

    def find_objects(self, grid: np.ndarray) -> List['Object']:
        """
        Phase 11: Object Abstraction.
        Extracts contiguous regions of the same color as Objects.
        Uses a vectorized-friendly BFS approach.
        """
        h, w = grid.shape
        visited = np.zeros((h, w), dtype=bool)
        objects = []
        
        for r in range(h):
            for c in range(w):
                val = grid[r, c]
                if val != 0 and not visited[r, c]:
                    # Found a new object!
                    obj_pixels = []
                    stack = [(r, c)]
                    visited[r, c] = True
                    
                    while stack:
                        curr_r, curr_c = stack.pop()
                        obj_pixels.append([curr_r, curr_c])
                        
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = curr_r + dr, curr_c + dc
                            if 0 <= nr < h and 0 <= nc < w:
                                if not visited[nr, nc] and grid[nr, nc] == val:
                                    visited[nr, nc] = True
                                    stack.append((nr, nc))
                    
                    # Vectorize the pixels
                    pixel_coords = np.array(obj_pixels)
                    r_min, c_min = np.min(pixel_coords, axis=0)
                    r_max, c_max = np.max(pixel_coords, axis=0)
                    
                    obj = Object(
                        color=int(val),
                        position=np.array([r_min, c_min]),
                        pixels=pixel_coords - np.array([r_min, c_min]), # Relative coords
                        bbox=np.array([r_min, c_min, r_max, c_max])
                    )
                    objects.append(obj)
        return objects

    def rotate_grid(self, grid: np.ndarray, k: int = 1) -> np.ndarray:
        """Vectorized 90-degree rotations."""
        return np.rot90(grid, k)

    def flip_grid(self, grid: np.ndarray, axis: int = 0) -> np.ndarray:
        """Vectorized reflections."""
        return np.flip(grid, axis)

@dataclass
class Object:
    """
    Phase 11: Vectorized object representation.
    """
    color: int
    position: np.ndarray # [row, col] top-left
    pixels: np.ndarray   # Nx2 array of [dr, dc] relative to position
    bbox: np.ndarray     # [r_min, c_min, r_max, c_max]
    
    def get_global_pixels(self) -> np.ndarray:
        return self.pixels + self.position

    def matches_shape(self, other: 'Object') -> bool:
        if len(self.pixels) != len(other.pixels): return False
        # Simple shape match (could be improved with HUD moments or sorting)
        return np.all(self.pixels == other.pixels)

@dataclass
class TransformationRule:
    """
    Phase 9, 10 & 11: Mapping rule with conditions.
    """
    input_color: int
    output_color: int
    condition_type: str = "GLOBAL" # GLOBAL, SPATIAL_X_MOD_2, ENCLOSED_BY, GEOMETRIC
    parameter: Any = None # Remainder, EnclosingColor, or GeomType
    confidence: float = 1.0


@dataclass
class State:
    """
    Complete agent state (S_t).
    
    From plan.txt:
        S_t = {W_t, B_t, F_t}
    
    This is the fundamental object in the AGI universe.
    """
    world_model: WorldModel
    belief_state: BeliefState
    frame_of_ref: FrameOfReference
    step_count: int = 0
    total_reward: float = 0.0
    
    def __post_init__(self, grid_size: int = 15, agent_id: str = "agent_0", pillar_type: PillarType = PillarType.GENERAL):
        """Initialize complex fields after dataclass init."""
        # These fields are initialized here because they depend on grid_size
        # and are not simple default values.
        
        # Check if fields are None (not provided during init)
        if self.world_model is None:
             self.world_model = WorldModel(agent_id=agent_id, grid_size=grid_size)
        if self.belief_state is None:
             self.belief_state = BeliefState(grid_size=grid_size)
        if self.frame_of_ref is None:
             self.frame_of_ref = FrameOfReference(agent_id=agent_id, position=(0, 0), pillar_type=pillar_type)


if __name__ == "__main__":
    # Test core data structures
    print("Testing Core Data Structures (Phase 3)")
    print("=" * 50)
    
    # Create initial state
    state = State(grid_size=10)
    print(f"\nInitialized State:")
    print(f"  World Model grid shape: {state.world_model.grid.shape}")
    print(f"  Belief State particles: {state.belief_state.num_particles}")
    print(f"  Frame position: {state.frame_of_ref.position}")
    
    # Simulate an observation
    from environment import GridWorld, Action
    env = GridWorld(size=10, seed=42)
    obs, reward, done = env.step(Action.MOVE_RIGHT)
    
    print(f"\nSimulated observation:")
    print(f"  Position: {obs.position}")
    print(f"  Reward: {obs.reward}")
    print(f"  Is noisy: {obs.is_noisy}")
    
    # Update belief state
    print(f"\nUpdating belief state...")
    state.belief_state.update(obs)
    belief_map = state.belief_state.get_belief_map()
    print(f"  Belief map shape: {belief_map.shape}")
    print(f"  Belief map mean: {belief_map.mean():.2f}")
    
    # Update world model
    print(f"\nUpdating world model...")
    state.world_model.update(state.belief_state, obs)
    patterns = state.world_model.discover_patterns()
    print(f"  Discovered {len(patterns)} patterns")
    
    # Update frame
    print(f"\nUpdating frame...")
    state.frame_of_ref.update(obs.position, obs)
    print(f"  New position: {state.frame_of_ref.position}")
    print(f"  History length: {len(state.frame_of_ref.history)}")
    
    print("\n✓ Core data structures working correctly!")
