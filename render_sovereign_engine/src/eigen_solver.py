"""
The Sovereign Eigenstate (Phase 20: Geodesic Flow)

"Gravity is the Local Limit of Optimal Transport."

This module implements the ARC task as a Single Tensor Operation.
V5: Uses Optimal Transport (Wasserstein Geodesics) to learn the Flow Field.
"""

import numpy as np
from typing import List, Tuple, Any, Dict

try:
    from scipy.optimize import linear_sum_assignment
    from scipy.spatial.distance import cdist
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

class EigenSolver:
    def __init__(self):
        self.epsilon = 1e-9
        self.target_size = (30, 30)

    def solve(self, test_input: np.ndarray, train_pairs: List[Tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
        """
        The Zero-Time Solver.
        Equation: Y_test = X_test + Flow(X) where Flow is learned via Optimal Transport.
        """
        if not train_pairs:
            return test_input
        
        if not SCIPY_AVAILABLE:
            print("Warning: Scipy not available. Optimal Transport disabled.")
            return test_input

        # 1. Learn Transport Fields from Training Data
        # We assume the "Task" is a Vector Field V(x, y).
        # We want to estimate V from the Training Flows.
        
        Flow_fields = []
        Shape_deltas = []
        X_train_vecs = []
        
        for xin, yout in train_pairs:
            # 1.1 Embed for Resonance (Phase 18 Thermodynamics is good for finding matches)
            # Use simple Flatten for now as Phase 18 failed to Project.
            # But here we use it only for Weighting.
            # Let's use simple Flatten for speed/robustness.
            x_vec = self._embed_simple(xin)
            X_train_vecs.append(x_vec)
            
            # 1.2 Calculate FLOW (Vector Field)
            # Find which pixel in Input went to which pixel in Output.
            # This is the Monge-Kantorovich Problem.
            # Cost = Distance^2 + ColorDifference^2 (Gravity Potential!)
            
            flow_y, flow_x = self._calculate_transport_field(xin, yout)
            
            # Flatten the field to vector [900*2]
            field_flat = np.concatenate([flow_y.flatten(), flow_x.flatten()])
            Flow_fields.append(field_flat)
            
            Shape_deltas.append(np.array(yout.shape) - np.array(xin.shape))
            
        X_train_matrix = np.array(X_train_vecs)
        Flow_matrix = np.array(Flow_fields)
        
        # 2. Embed Test Input
        x_test_vec = self._embed_simple(test_input)
        
        # 3. Calculate Resonance
        # Which training example is most similar to Test?
        norm_test = np.linalg.norm(x_test_vec) + self.epsilon
        x_test_unit = x_test_vec / norm_test
        norms_train = np.linalg.norm(X_train_matrix, axis=1, keepdims=True) + self.epsilon
        X_train_unit = X_train_matrix / norms_train
        similarity = np.dot(X_train_unit, x_test_unit)
        
        beta = 5.0 
        exp_sim = np.exp(beta * similarity)
        attention = exp_sim / np.sum(exp_sim)
        
        print(f"Geodesic Resonance: {attention}")
        
        # 4. Project Manifold (Average the Flows)
        expected_flow_flat = np.dot(attention, Flow_matrix)
        expected_shape_delta = np.dot(attention, np.array(Shape_deltas))
        
        # Unpack Flow
        mid = len(expected_flow_flat) // 2
        flow_y = expected_flow_flat[:mid].reshape(self.target_size)
        flow_x = expected_flow_flat[mid:].reshape(self.target_size)
        
        # 5. Collapse (Apply Flow)
        output_grid = self._apply_transport_field(test_input, flow_y, flow_x, expected_shape_delta)
        
        return output_grid

    def _embed_simple(self, grid: np.ndarray) -> np.ndarray:
        padded = self._pad_centered(grid, self.target_size)
        return padded.flatten()
        
    def _pad_centered(self, grid: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
        h, w = grid.shape
        th, tw = target_shape
        pad_h, pad_w = max(0, th - h), max(0, tw - w)
        top = pad_h // 2
        left = pad_w // 2
        padded = np.pad(grid, ((top, pad_h-top), (left, pad_w-left)), mode='constant', constant_values=0)
        # Crop if needed
        if padded.shape[0] > th: padded = padded[:th, :]
        if padded.shape[1] > tw: padded = padded[:, :tw]
        return padded

    def _calculate_transport_field(self, grid_a: np.ndarray, grid_b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate Optimal Transport Plan.
        Returns Dy, Dx fields (30x30).
        """
        # 1. Get Points (Mass)
        # A: Source, B: Dest
        # We map PIXELS from A to B.
        # Problem: Unequal mass?
        # We assume Mass Conservation or handle via dummy nodes.
        # Simplified: We treat 30x30 grid as fixed lattice.
        # We want to map pixel (r, c) in A to (r', c') in B.
        # BUT standard ARC is discrete colors.
        
        # Constraint: Only map color C to color C. (Mass Conservation of Species).
        # Gravity Engine Logic: Colors don't transmute easily.
        
        # Initialize Field (0 displacement)
        dy_field = np.zeros(self.target_size)
        dx_field = np.zeros(self.target_size)
        
        # Resize to Target for coordinate consistency
        a_pad = self._pad_centered(grid_a, self.target_size)
        b_pad = self._pad_centered(grid_b, self.target_size)
        
        active_colors = np.unique(a_pad)
        active_colors = active_colors[active_colors != 0] # Ignore background for flow?
        
        for c in active_colors:
            # Source points
            y_a, x_a = np.where(a_pad == c)
            # Dest points
            y_b, x_b = np.where(b_pad == c)
            
            if len(y_a) == 0 or len(y_b) == 0:
                continue
                
            # Compute Cost Matrix (Euclidean Distance^2)
            # C_ij = ||p_a_i - p_b_j||^2
            points_a = np.column_stack((y_a, x_a))
            points_b = np.column_stack((y_b, x_b))
            
            cost_matrix = cdist(points_a, points_b, metric='sqeuclidean')
            
            # Hungarian Algorithm (Linear Sum Assignment)
            # Handles unequal sizes by picking subset?
            # linear_sum_assignment solves min cost for square or rect matrix.
            # If A > B, some A unassigned? No, scipy handles it (rows assigned to cols).
            # If N_a != N_b, we can't fully map.
            # Gravity Logic: We map to NEAREST.
            
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            
            # Record Displacement
            # For each assignment (i -> j)
            # Displacement = p_b_j - p_a_i
            
            for r, c_idx in zip(row_ind, col_ind):
                # Point A index r
                # Point B index c_idx
                pa = points_a[r]
                pb = points_b[c_idx]
                
                # Assign displacement to the Source Pixel location
                dy_field[pa[0], pa[1]] = pb[0] - pa[0]
                dx_field[pa[0], pa[1]] = pb[1] - pa[1]
                
        return dy_field, dx_field

    def _apply_transport_field(self, grid: np.ndarray, dy: np.ndarray, dx: np.ndarray, shape_delta: np.ndarray) -> np.ndarray:
        """
        Advect the grid using the learned velocity field.
        """
        # New grid
        # Output shape
        pred_shape_float = np.array(grid.shape) + shape_delta
        pred_shape = np.round(pred_shape_float).astype(int)
        pred_shape = np.clip(pred_shape, 1, 30)
        
        # Initialize canvas 30x30
        output_pad = np.zeros(self.target_size)
        
        input_pad = self._pad_centered(grid, self.target_size)
        h, w = self.target_size
        
        # Forward Mapping (Splatting)
        # Iterate over all source pixels
        # New Pos = Old Pos + Flow(Old Pos)
        
        # Vectorized Advection
        rows, cols = np.indices((h, w))
        
        # Get flow at each pixel
        # Flow is smooth? In our code it is sparse (only at color locations).
        # But `expected_flow` is an Average of Flows. It wraps the whole object.
        # If the flow is a Vortex, every pixel has a vector.
        
        # Apply Flow
        new_rows = rows + dy
        new_cols = cols + dx
        
        # Round to nearest integer pixel
        new_rows_int = np.round(new_rows).astype(int)
        new_cols_int = np.round(new_cols).astype(int)
        
        # Bounds check
        mask = (new_rows_int >= 0) & (new_rows_int < h) & (new_cols_int >= 0) & (new_cols_int < w)
        
        # Splat
        # For conflicting targets? We assume "Last Write Wins" or "Max Mass".
        # Or just loop.
        
        # We only move NON-ZERO pixels.
        # Background doesn't flow (it's the medium).
        
        non_zero = input_pad != 0
        valid = mask & non_zero
        
        # Extract valid source colors
        colors = input_pad[valid]
        dest_r = new_rows_int[valid]
        dest_c = new_cols_int[valid]
        
        output_pad[dest_r, dest_c] = colors
        
        # Crop to predicted shape
        out_h, out_w = pred_shape
        start_h = (30 - out_h) // 2
        start_w = (30 - out_w) // 2
        
        output_crop = output_pad[start_h:start_h+out_h, start_w:start_w+out_w]
        
        return np.clip(output_crop, 0, 9).astype(int)

    def update(self, observation, action, reward):
        pass  # Dummy update for compatibility

    # ===========================================
    # OPTIMAL TRANSPORT NAVIGATION
    # ===========================================
    
    # ===========================================
    # OPTIMAL TRANSPORT NAVIGATION (SINKHORN)
    # ===========================================
    
    def navigate_via_flow_field(self,
                                current_pos: Tuple[int, int],
                                goal_pos: Tuple[int, int],
                                maze_state: np.ndarray,
                                visit_history: Dict[Tuple[int, int], int],
                                valid_neighbors: List[Tuple[int, int, int]],
                                wall_value: int = 1) -> int:
        """
        Navigate using the Optimal Transport Plan (Wasserstein Geodesic).
        We calculate the 'Transport Plan' gamma from Current(Dirac) to Goal(Dirac).
        The flow through obstacles is penalized but not impossible (Tunneling).
        """
        # 1. Setup Distributions (Inputs)
        h, w = maze_state.shape
        size = h * w
        
        # Flattened indices
        source_idx = current_pos[0] * w + current_pos[1]
        target_idx = goal_pos[0] * w + goal_pos[1]
        
        # Distributions P and Q (Dirac deltas)
        P = np.zeros(size)
        P[source_idx] = 1.0
        
        Q = np.zeros(size)
        Q[target_idx] = 1.0
        
        # 2. Compute Cost Matrix C (N x N)
        # Defines the 'Topology' of the space.
        # Cost = Euclidean Distance + Wall Penalty
        # We compute this on the fly. For larger grids, caching is needed.
        # Vectorized grid generation
        Y, X = np.indices((h, w))
        coords = np.stack([Y.flatten(), X.flatten()], axis=1) # (N, 2)
        
        # Pairwise euclidean distance
        # cdist is efficient
        if SCIPY_AVAILABLE:
            C = cdist(coords, coords, metric='euclidean')
        else:
            # Fallback (slower)
             # x^2 + y^2 - 2xy logic or just loops
             diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
             C = np.sqrt(np.sum(diff**2, axis=-1))
             
        # Wall Penalty (The "Potential Barrier")
        # If a pixel is a wall, moving TO it or FROM it costs extra.
        # We assume maze_state 1 = Wall.
        flat_maze = maze_state.flatten()
        walls = np.where(flat_maze == wall_value)[0]
        
        # Add barrier potential
        # "Tunneling Cost"
        BARRIER_HEIGHT = 100.0 
        
        # We add cost to rows/cols associated with walls
        # C_ij += Wall(j) * penalty
        if len(walls) > 0:
            C[:, walls] += BARRIER_HEIGHT
            C[walls, :] += BARRIER_HEIGHT
            
        # 3. Sinkhorn-Knopp Algorithm
        # Solve for Transport Plan gamma
        # K = exp(-C / epsilon)
        epsilon = 0.5 # Entropy regularization parameter (Temperature)
        K = np.exp(-C / epsilon)
        
        # Iteration
        # u = P / (K @ v)
        # v = Q / (K.T @ u)
        u = np.ones(size)
        v = np.ones(size)
        
        MAX_ITER = 50 # Convergence is usually fast
        for _ in range(MAX_ITER):
            v = Q / (np.dot(K.T, u) + 1e-9)
            u = P / (np.dot(K, v) + 1e-9)
            
        # Transport Plan gamma = diag(u) @ K @ diag(v)
        # We only need the row corresponding to source_idx to see where mass goes!
        # gamma_source = u[source_idx] * K[source_idx, :] * v
        
        # Flow from Source
        # Which 'j' (neighbor) receives the most mass?
        flow_vector = u[source_idx] * K[source_idx, :] * v
        
        # 4. Choose Action
        # We look at valid neighbors and pick the one with highest flow mass
        
        best_action = 4 # Wait
        max_flow = -1.0
        
        for action_idx, nx, ny in valid_neighbors:
            n_idx = nx * w + ny
            mass_transfer = flow_vector[n_idx]
            
            if mass_transfer > max_flow:
                max_flow = mass_transfer
                best_action = action_idx
                
        return best_action
