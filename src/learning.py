"""
Phase 4: Advanced Learning and Self-Modification
Implements the learning mechanisms from plan.txt to make the agent smarter.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from core import WorldModel, BeliefState, State
from environment import Observation


class LearningSystem:
    """
    Advanced learning mechanisms for the AGI.
    
    From plan.txt Phase 4:
    - Pattern discovery
    - Model compression
    - Rule learning
    - Self-modification
    - Curiosity-driven exploration
    """
    
    def __init__(self, grid_size: int = 15, vocabulary_builder: Any = None, motif_memory: Any = None):
        self.grid_size = grid_size
        self.learning_rate = 0.1
        self.compression_threshold = 0.8
        self.vocabulary_builder = vocabulary_builder
        self.motif_memory = motif_memory
        
    def discover_patterns(self, world_model: WorldModel, belief_state: BeliefState) -> List[Dict[str, Any]]:
        """
        Discover patterns in the world (Phase 4.1 from plan.txt).
        
        Patterns become candidate laws of the agent's internal physics.
        """
        new_patterns = []
        
        # Pattern 1: High/Low reward cells
        for pos, rewards in world_model.cell_reward_history.items():
            if len(rewards) >= 1:
                avg_reward = np.mean(rewards)
                std_reward = np.std(rewards)
                
                if avg_reward > 0.3 and len(rewards) >= 3:  # Consistently good
                    new_patterns.append({
                        'type': 'high_reward_cell',
                        'position': pos,
                        'avg_reward': float(avg_reward),
                        'confidence': min(len(rewards) / 10.0, 1.0),
                        'consistency': float(1.0 / (1.0 + std_reward))
                    })
                elif avg_reward < -0.5:  # Instant Trauma Learning
                    new_patterns.append({
                        'type': 'danger_zone',
                        'position': pos,
                        'avg_reward': float(avg_reward),
                        'confidence': min(len(rewards) / 10.0, 1.0)
                    })
        
        # Pattern 2: Frequently visited safe areas
        # Refactored for dictionary support
        for pos, count in world_model.cell_visit_counts.items():
            if count > 5:
                if pos in world_model.cell_reward_history:
                    rewards = world_model.cell_reward_history[pos]
                    if len(rewards) > 0 and np.mean(rewards) > -0.2:
                        new_patterns.append({
                            'type': 'safe_zone',
                            'position': pos,
                            'visit_count': int(count),
                            'avg_reward': float(np.mean(rewards))
                        })
        
        # Pattern 3: Unexplored regions (for curiosity)
        # For infinite world, we can't iterate all cells.
        # Instead, check neighbors of visited cells that are NOT in visit_counts
        unexplored = set()
        for pos in world_model.cell_visit_counts.keys():
            x, y = pos
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                neighbor = (x + dx, y + dy)
                if neighbor not in world_model.cell_visit_counts:
                    unexplored.add(neighbor)
        
        # Convert to list and limit
        if unexplored:
            frontier_list = list(unexplored)[:10]
            new_patterns.append({
                'type': 'exploration_frontier',
                'cells': frontier_list,
                'count': len(unexplored)
            })
        
        # Pattern 4: Movement efficiency
        if len(world_model.cell_reward_history) > 10:
            total_visits = sum(world_model.cell_visit_counts.values())
            unique_cells = len(world_model.cell_visit_counts)
            if total_visits > 0:
                efficiency = unique_cells / total_visits
                new_patterns.append({
                    'type': 'movement_efficiency',
                    'efficiency': float(efficiency),
                    'unique_cells': int(unique_cells),
                    'total_visits': int(total_visits)
                })
        
        return new_patterns
    
    def compress_model(self, world_model: WorldModel) -> WorldModel:
        """
        Compress the world model (Phase 4.2 from plan.txt).
        
        Information-theoretic learning:
        - Merge similar states
        - Remove redundant details
        - Cluster similar observations
        """
        # Compress patterns - remove duplicates and low-confidence patterns
        if len(world_model.patterns) > 50:
            # Keep only high-confidence patterns
            world_model.patterns = sorted(
                world_model.patterns,
                key=lambda p: p.get('confidence', 0.5),
                reverse=True
            )[:50]
        
        # Merge similar patterns
        compressed_patterns = []
        for pattern in world_model.patterns:
            # Check if similar pattern already exists
            similar_found = False
            for existing in compressed_patterns:
                if (pattern['type'] == existing['type'] and 
                    pattern.get('position') == existing.get('position')):
                    # Merge by averaging
                    if 'avg_reward' in pattern and 'avg_reward' in existing:
                        existing['avg_reward'] = (existing['avg_reward'] + pattern['avg_reward']) / 2
                        existing['confidence'] = max(existing.get('confidence', 0.5), 
                                                    pattern.get('confidence', 0.5))
                    similar_found = True
                    break
            
            if not similar_found:
                compressed_patterns.append(pattern)
        
        world_model.patterns = compressed_patterns
        
        # Compress visit counts - reduce precision for old data
        # Keep recent visits precise, compress old ones
        # For dictionary:
        for pos in world_model.cell_visit_counts:
            world_model.cell_visit_counts[pos] = int(world_model.cell_visit_counts[pos] * 0.95)
        
        return world_model
    
    def update_rules(self, world_model: WorldModel, patterns: List[Dict[str, Any]]) -> WorldModel:
        """
        Update internal rules based on discovered patterns (Phase 4.3 from plan.txt).
        
        The agent discovers its own laws of physics.
        """
        for pattern in patterns:
            # Convert patterns to rules
            if pattern['type'] == 'high_reward_cell':
                rule = {
                    'type': 'seek_location',
                    'target': pattern['position'],
                    'expected_reward': pattern['avg_reward'],
                    'confidence': pattern['confidence']
                }
                
                # Check if rule already exists
                rule_exists = False
                for existing_rule in world_model.rules:
                    if (existing_rule.get('type') == 'seek_location' and 
                        existing_rule.get('target') == pattern['position']):
                        # Update existing rule
                        existing_rule['expected_reward'] = pattern['avg_reward']
                        existing_rule['confidence'] = pattern['confidence']
                        rule_exists = True
                        break
                
                if not rule_exists and pattern['confidence'] > 0.5:
                    world_model.rules.append(rule)
            
            elif pattern['type'] == 'danger_zone':
                rule = {
                    'type': 'avoid_location',
                    'target': pattern['position'],
                    'expected_penalty': pattern['avg_reward'],
                    'confidence': pattern['confidence']
                }
                
                # Add if doesn't exist
                if not any(r.get('target') == pattern['position'] and r.get('type') == 'avoid_location' 
                          for r in world_model.rules):
                    if pattern['confidence'] > 0.5:
                        world_model.rules.append(rule)
            
            elif pattern['type'] == 'exploration_frontier':
                rule = {
                    'type': 'explore_frontier',
                    'frontier_cells': pattern['cells'],
                    'priority': min(pattern['count'] / 10.0, 1.0)
                }
                
                # Replace old frontier rule
                world_model.rules = [r for r in world_model.rules if r.get('type') != 'explore_frontier']
                world_model.rules.append(rule)
        
        # Limit total rules
        if len(world_model.rules) > world_model.max_rules:
            # Keep highest confidence rules
            world_model.rules = sorted(
                world_model.rules,
                key=lambda r: r.get('confidence', r.get('priority', 0.5)),
                reverse=True
            )[:world_model.max_rules]
        
        return world_model
    
    def self_modify(self, state: State, prediction_error: float, energy_level: float) -> State:
        """
        Self-modification based on performance (Phase 4.4 from plan.txt).
        
        The agent evolves itself:
        - Adjust visible range
        - Tune noise tolerance
        - Change planning depth
        - Modify reward weights
        """
        # Adjust visible range based on prediction error
        if prediction_error > 0.5:  # High error - need more information
            state.frame_of_ref.adjust_visible_range(delta=1)
        elif prediction_error < 0.1 and energy_level > 50:  # Low error - can reduce
            state.frame_of_ref.adjust_visible_range(delta=-1)
            
        # Adjust sensor noise tolerance
        if prediction_error > 0.7:
            # Increase noise tolerance (be more skeptical of observations)
            state.frame_of_ref.sensor_noise_level = min(0.3, state.frame_of_ref.sensor_noise_level * 1.1)
            
        # NEW: Dynamic Planning Depth Adjustment
        # Now modifying planning_depth directly in FrameOfReference
        if prediction_error > 0.5:
            # High error - plan deeper to understand better
            state.frame_of_ref.planning_depth = min(5, state.frame_of_ref.planning_depth + 1)
        elif prediction_error < 0.1 and energy_level > 50:
            # Low error & high energy - can reduce depth to save compute (or increase to optimize)
            # Actually, if error is low, maybe we don't need deep planning? 
            # Or we can explore more. Let's stick to the plan:
            state.frame_of_ref.planning_depth = max(1, state.frame_of_ref.planning_depth - 1)
        
        # Energy-based constraints
        if energy_level < 30:
            # Low energy - conserve cognitive resources
            state.frame_of_ref.planning_depth = max(1, state.frame_of_ref.planning_depth - 1) 
        elif energy_level > 80:
             # Abundance - maximize capabilities
            state.frame_of_ref.planning_depth = min(5, state.frame_of_ref.planning_depth + 1)
        
        # NEW: Dynamic Memory Expansion
        if prediction_error > 0.6 and energy_level > 60:
            # Need more memory to understand complex world
            state.world_model.max_patterns = min(100, state.world_model.max_patterns + 5)
            state.world_model.max_rules = min(40, state.world_model.max_rules + 2)
        elif energy_level < 20:
            # Conserve energy/memory
            state.world_model.max_patterns = max(20, state.world_model.max_patterns - 5)
        
        return state
    
    def compute_curiosity_reward(self, observation: Observation, world_model: WorldModel) -> float:
        """
        Compute curiosity reward (Phase 4.5 from plan.txt).
        
        Novelty-based reward to encourage exploration.
        """
        pos = observation.position
        
        # Base curiosity on visit count
        visit_count = world_model.cell_visit_counts[pos[0], pos[1]]
        
        if visit_count == 0:
            return 1.0  # Never visited - high curiosity
        elif visit_count == 1:
            return 0.5  # Visited once - medium curiosity
        elif visit_count < 5:
            return 0.2  # Visited few times - low curiosity
        else:
            return -0.1  # Visited many times - discourage revisiting
    
    def compute_prediction_error(self, world_model: WorldModel, observation: Observation) -> float:
        """
        Compute how surprised the agent is by the observation.
        
        Used for self-modification.
        """
        pos = observation.position
        
        # If we've been here before, check if reward matches expectation
        if pos in world_model.cell_reward_history:
            past_rewards = world_model.cell_reward_history[pos]
            if len(past_rewards) > 0:
                expected_reward = np.mean(past_rewards)
                actual_reward = observation.reward
                error = abs(expected_reward - actual_reward)
                return min(error, 1.0)
        
        # New location - moderate surprise
        return 0.3
    
    def adjust_rules_on_failure(self, world_model: WorldModel, observation: Observation) -> WorldModel:
        """
        Adjust or remove rules when predictions fail (Phase 4 from plan.txt).
        
        This is the key mechanism for "adjusting laws when predictions fail".
        
        The agent:
        1. Checks if any rules apply to current situation
        2. Compares predicted outcome vs actual outcome
        3. Reduces confidence or removes rules that fail
        4. Strengthens rules that succeed
        """
        pos = observation.position
        actual_reward = observation.reward
        
        rules_to_remove = []
        
        for i, rule in enumerate(world_model.rules):
            # Check if this rule applies to current position
            rule_applies = False
            expected_outcome = None
            
            if rule.get('type') == 'seek_location' and rule.get('target') == pos:
                rule_applies = True
                expected_outcome = rule.get('expected_reward', 0)
            elif rule.get('type') == 'avoid_location' and rule.get('target') == pos:
                rule_applies = True
                expected_outcome = rule.get('expected_penalty', 0)
            
            if rule_applies and expected_outcome is not None:
                # Compare prediction vs reality
                prediction_error = abs(expected_outcome - actual_reward)
                
                # Initialize prediction tracking if not exists
                if 'prediction_errors' not in rule:
                    rule['prediction_errors'] = []
                    rule['prediction_successes'] = 0
                    rule['prediction_failures'] = 0
                
                # Record outcome
                rule['prediction_errors'].append(prediction_error)
                
                # Keep only recent errors (last 10)
                if len(rule['prediction_errors']) > 10:
                    rule['prediction_errors'] = rule['prediction_errors'][-10:]
                
                # Classify as success or failure
                if prediction_error < 0.3:  # Good prediction
                    rule['prediction_successes'] += 1
                    # Strengthen rule
                    rule['confidence'] = min(1.0, rule.get('confidence', 0.5) * 1.1)
                else:  # Bad prediction
                    rule['prediction_failures'] += 1
                    # Weaken rule
                    rule['confidence'] = max(0.1, rule.get('confidence', 0.5) * 0.9)
                
                # Calculate failure rate
                total_predictions = rule['prediction_successes'] + rule['prediction_failures']
                if total_predictions >= 5:  # Need at least 5 samples
                    failure_rate = rule['prediction_failures'] / total_predictions
                    
                    # Remove rule if it fails too often
                    if failure_rate > 0.7:  # 70% failure rate
                        rules_to_remove.append(i)
                        print(f"   ⚠️ Removing failed rule: {rule['type']} at {rule.get('target')} (failure rate: {failure_rate:.1%})")
                    elif failure_rate > 0.5:  # 50% failure rate
                        # Significantly reduce confidence
                        rule['confidence'] = 0.2
                        print(f"   ⚠️ Reducing confidence for rule: {rule['type']} at {rule.get('target')} (failure rate: {failure_rate:.1%})")
        
        # Remove failed rules (in reverse order to maintain indices)
        for i in sorted(rules_to_remove, reverse=True):
            world_model.rules.pop(i)
        
        return world_model


if __name__ == "__main__":
    # Test the learning system
    print("Testing Phase 4 Learning System")
    print("=" * 60)
    
    from environment import GridWorld, Action
    from agent import Agent
    
    # Create environment and agent
    env = GridWorld(size=10, seed=42)
    agent = Agent(grid_size=10)
    learning = LearningSystem(grid_size=10)
    
    # Run a few steps
    obs = env.observe()
    for i in range(30):
        action, state = agent.act(obs)
        obs, reward, done = env.step(action)
    
    # Test pattern discovery
    print("\n1. Pattern Discovery:")
    patterns = learning.discover_patterns(agent.state.world_model, agent.state.belief_state)
    print(f"   Discovered {len(patterns)} patterns:")
    for p in patterns[:5]:
        print(f"   - {p['type']}: {p}")
    
    # Test compression
    print("\n2. Model Compression:")
    before_patterns = len(agent.state.world_model.patterns)
    agent.state.world_model = learning.compress_model(agent.state.world_model)
    after_patterns = len(agent.state.world_model.patterns)
    print(f"   Patterns: {before_patterns} → {after_patterns}")
    
    # Test rule learning
    print("\n3. Rule Learning:")
    before_rules = len(agent.state.world_model.rules)
    agent.state.world_model = learning.update_rules(agent.state.world_model, patterns)
    after_rules = len(agent.state.world_model.rules)
    print(f"   Rules: {before_rules} → {after_rules}")
    for rule in agent.state.world_model.rules[:3]:
        print(f"   - {rule['type']}: {rule}")
    
    # Test curiosity
    print("\n4. Curiosity Reward:")
    curiosity = learning.compute_curiosity_reward(obs, agent.state.world_model)
    print(f"   Current position curiosity: {curiosity:.2f}")
    
    # Test self-modification
    print("\n5. Self-Modification:")
    before_range = agent.state.frame_of_ref.visible_range
    error = learning.compute_prediction_error(agent.state.world_model, obs)
    agent.state = learning.self_modify(agent.state, error, env.agent_energy)
    after_range = agent.state.frame_of_ref.visible_range
    print(f"   Visible range: {before_range} → {after_range}")
    print(f"   Prediction error: {error:.3f}")
    
    print("\n✓ Phase 4 Learning System working!")
