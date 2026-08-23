"""
Persistent Memory System
Allows agent to save and load learned knowledge across runs.
"""

import pickle
import os
from typing import Optional
from core import State


class MemoryManager:
    """
    Manages persistent storage of agent's learned knowledge.
    
    Saves:
    - Patterns discovered
    - Rules learned
    - Cell visit counts
    - Reward history
    - World model state
    """
    
    def __init__(self, memory_dir: str = "agent_memories"):
        """Initialize memory manager."""
        self.memory_dir = memory_dir
        
        # Create memory directory if it doesn't exist
        if not os.path.exists(memory_dir):
            os.makedirs(memory_dir)
    
    def get_memory_path(self, seed: int) -> str:
        """Get path for memory file for given seed."""
        return os.path.join(self.memory_dir, f"memory_seed_{seed}.pkl")
    
    def save(self, state: State, seed: int, episode_score: float = 0, episode_steps: int = 0) -> bool:
        """
        Save agent's state to persistent memory.
        
        Args:
            state: Agent's current state
            seed: World seed (used as memory identifier)
            episode_score: Final score of this episode
            episode_steps: Steps taken in this episode
            
        Returns:
            True if saved successfully
        """
        try:
            # Load existing memory to append episode history
            path = self.get_memory_path(seed)
            episode_history = []
            if os.path.exists(path):
                try:
                    with open(path, 'rb') as f:
                        old_memory = pickle.load(f)
                        episode_history = old_memory.get('episode_history', [])
                except:
                    pass
            
            # Append this episode's outcome
            episode_history.append({
                'score': episode_score,
                'steps': episode_steps,
                'total_reward': state.total_reward
            })
            
            memory = {
                'patterns': state.world_model.patterns,
                'rules': state.world_model.rules,
                'cell_visit_counts': state.world_model.cell_visit_counts,
                'cell_reward_history': state.world_model.cell_reward_history,
                'total_reward': state.total_reward,
                'step_count': state.step_count,
                'episode_history': episode_history
            }
            
            path = self.get_memory_path(seed)
            with open(path, 'wb') as f:
                pickle.dump(memory, f)
            
            return True
        except Exception as e:
            print(f"Warning: Failed to save memory: {e}")
            return False
    
    def load(self, state: State, seed: int) -> dict:
        """
        Load previously saved memory into agent's state.
        
        Args:
            state: Agent's state to load into
            seed: World seed (memory identifier)
            
        Returns:
            Dictionary with 'loaded' (bool) and 'episode_history' (list)
        """
        path = self.get_memory_path(seed)
        
        if not os.path.exists(path):
            return {'loaded': False, 'episode_history': []}
        
        try:
            with open(path, 'rb') as f:
                memory = pickle.load(f)
            
            # Restore learned knowledge
            state.world_model.patterns = memory['patterns']
            state.world_model.rules = memory['rules']
            state.world_model.cell_visit_counts = memory['cell_visit_counts']
            state.world_model.cell_reward_history = memory['cell_reward_history']
            
            episode_history = memory.get('episode_history', [])
            return {'loaded': True, 'episode_history': episode_history}
        except Exception as e:
            print(f"Warning: Failed to load memory: {e}")
            return False
    
    def has_memory(self, seed: int) -> bool:
        """Check if memory exists for given seed."""
        return os.path.exists(self.get_memory_path(seed))
    
    def clear(self, seed: Optional[int] = None):
        """
        Clear saved memories.
        
        Args:
            seed: If provided, clear only this seed's memory.
                  If None, clear all memories.
        """
        if seed is not None:
            path = self.get_memory_path(seed)
            if os.path.exists(path):
                os.remove(path)
        else:
            # Clear all memories
            for file in os.listdir(self.memory_dir):
                if file.startswith("memory_seed_") and file.endswith(".pkl"):
                    os.remove(os.path.join(self.memory_dir, file))
    
    def list_memories(self) -> list:
        """List all available memories (seeds)."""
        memories = []
        if os.path.exists(self.memory_dir):
            for file in os.listdir(self.memory_dir):
                if file.startswith("memory_seed_") and file.endswith(".pkl"):
                    # Extract seed number
                    seed_str = file.replace("memory_seed_", "").replace(".pkl", "")
                    try:
                        seed = int(seed_str)
                        memories.append(seed)
                    except ValueError:
                        pass
        return sorted(memories)


if __name__ == "__main__":
    # Test memory manager
    print("Testing Persistent Memory System")
    print("=" * 60)
    
    from agent import Agent
    from environment import GridWorld
    
    memory = MemoryManager()
    
    # Test 1: Save memory
    print("\n1. Creating agent and running episode...")
    env = GridWorld(size=10, seed=42)
    agent = Agent(grid_size=10)
    
    obs = env.observe()
    for i in range(20):
        action, state = agent.act(obs)
        obs, reward, done = env.step(action)
    
    print(f"   Patterns: {len(agent.state.world_model.patterns)}")
    print(f"   Rules: {len(agent.state.world_model.rules)}")
    
    # Save
    print("\n2. Saving memory...")
    success = memory.save(agent.state, seed=42)
    print(f"   Saved: {success}")
    
    # Test 2: Load memory
    print("\n3. Creating new agent and loading memory...")
    agent2 = Agent(grid_size=10)
    print(f"   Before load - Patterns: {len(agent2.state.world_model.patterns)}")
    
    loaded = memory.load(agent2.state, seed=42)
    print(f"   Loaded: {loaded}")
    print(f"   After load - Patterns: {len(agent2.state.world_model.patterns)}")
    print(f"   After load - Rules: {len(agent2.state.world_model.rules)}")
    
    # Test 3: List memories
    print("\n4. Available memories:")
    memories = memory.list_memories()
    print(f"   Seeds with saved memory: {memories}")
    
    print("\n✓ Persistent memory system working!")
