"""
Phase 17.4: Motif Memory - Transfer Learning
Persistent storage of successful transformation patterns for cross-episode learning.
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import pickle
import os
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class StoredMotif:
    """A successful motif-transformation pair stored in memory"""
    motif_signature: str
    transformation_type: str
    parameters: Dict[str, Any]
    success_count: int = 0
    tasks_used: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    def __repr__(self):
        return f"StoredMotif({self.transformation_type}, success={self.success_count}, conf={self.confidence:.2f})"

class MotifMemory:
    """
    Persistent memory of successful transformation patterns.
    Enables transfer learning - agent remembers what worked before!
    """
    
    def __init__(self, persistence_file: str = "motif_memory.pkl"):
        self.memory_file = persistence_file
        self.successful_motifs: List[StoredMotif] = []
        self.transformation_chains: Dict[str, List[str]] = defaultdict(list)
        self.task_history: Dict[str, Dict] = {}
        
        # Load existing memory if available
        self.load()
    
    def store_success(self, motif: Dict, transformation: Any, task_id: str, confidence: float = 1.0):
        """
        Store a successful motif-transformation pair.
        
        Args:
            motif: Dictionary describing the pattern (from MotifInductor)
            transformation: The AbstractRule that worked
            task_id: Identifier for the task
            confidence: How well it worked (0-1)
        """
        # Create signature for motif
        motif_sig = self._create_signature(motif)
        transform_type = getattr(transformation, 'rule_type', 'UNKNOWN')
        
        # Check if we've seen this pattern before
        existing = None
        for stored in self.successful_motifs:
            if stored.motif_signature == motif_sig and stored.transformation_type == transform_type:
                existing = stored
                break
        
        if existing:
            # Update existing memory
            existing.success_count += 1
            if task_id not in existing.tasks_used:
                existing.tasks_used.append(task_id)
            # Update confidence (running average)
            existing.confidence = (existing.confidence * (existing.success_count - 1) + confidence) / existing.success_count
        else:
            # Create new memory
            new_motif = StoredMotif(
                motif_signature=motif_sig,
                transformation_type=transform_type,
                parameters=getattr(transformation, 'parameters', {}),
                success_count=1,
                tasks_used=[task_id],
                confidence=confidence
            )
            self.successful_motifs.append(new_motif)
        
        # Store in task history
        if task_id not in self.task_history:
            self.task_history[task_id] = {'motifs': [], 'success': False}
        self.task_history[task_id]['motifs'].append(motif_sig)
        
        # Save to disk
        self.save()
    
    def recall_similar(self, current_motif: Dict, top_k: int = 5) -> List[StoredMotif]:
        """
        Retrieve similar successful patterns from memory.
        
        Args:
            current_motif: The pattern we're trying to match
            top_k: Number of top matches to return
            
        Returns:
            List of StoredMotif objects ranked by similarity and confidence
        """
        current_sig = self._create_signature(current_motif)
        
        # Score each stored motif by similarity
        scored = []
        for stored in self.successful_motifs:
            similarity = self._compute_similarity(current_sig, stored.motif_signature)
            # Combined score: similarity × confidence × success_count
            score = similarity * stored.confidence * min(stored.success_count / 10.0, 1.0)
            scored.append((stored, score))
        
        # Sort by score and return top K
        scored.sort(key=lambda x: x[1], reverse=True)
        return [motif for motif, score in scored[:top_k] if score > 0.3]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            'total_motifs': len(self.successful_motifs),
            'total_tasks': len(self.task_history),
            'avg_success_count': np.mean([m.success_count for m in self.successful_motifs]) if self.successful_motifs else 0,
            'transformation_types': list(set(m.transformation_type for m in self.successful_motifs))
        }
    
    def clear(self):
        """Clear all memory (for testing)"""
        self.successful_motifs = []
        self.transformation_chains = defaultdict(list)
        self.task_history = {}
        self.save()
    
    def save(self):
        """Save memory to disk"""
        try:
            with open(self.memory_file, 'wb') as f:
                pickle.dump({
                    'motifs': self.successful_motifs,
                    'chains': dict(self.transformation_chains),
                    'history': self.task_history
                }, f)
        except Exception as e:
            print(f"Warning: Could not save motif memory: {e}")
    
    def load(self):
        """Load memory from disk"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'rb') as f:
                    data = pickle.load(f)
                    self.successful_motifs = data.get('motifs', [])
                    self.transformation_chains = defaultdict(list, data.get('chains', {}))
                    self.task_history = data.get('history', {})
                print(f"[MEMORY] Loaded {len(self.successful_motifs)} stored patterns")
            except Exception as e:
                print(f"Warning: Could not load motif memory: {e}")
    
    # Helper methods
    def _create_signature(self, motif: Dict) -> str:
        """Create a unique signature for a motif"""
        motif_type = motif.get('type', 'unknown')
        
        if motif_type == 'component':
            # Signature based on shape size and color
            size = motif.get('size', 0)
            color = motif.get('color', 0)
            return f"component_{color}_{size}"
        
        elif motif_type == 'rectangle':
            # Signature based on dimensions and color
            bbox = motif.get('bbox', (0,0,0,0))
            h = bbox[2] - bbox[0]
            w = bbox[3] - bbox[1]
            color = motif.get('color', 0)
            return f"rectangle_{color}_{h}x{w}"
        
        elif motif_type == 'fill':
            # Signature based on fill colors
            colors = motif.get('fill_colors', [])
            return f"fill_{'_'.join(map(str, sorted(colors)))}"
        
        else:
            return f"{motif_type}_generic"
    
    def _compute_similarity(self, sig1: str, sig2: str) -> float:
        """Compute similarity between two signatures"""
        # Simple string similarity for now
        if sig1 == sig2:
            return 1.0
        
        # Check if same type
        type1 = sig1.split('_')[0]
        type2 = sig2.split('_')[0]
        
        if type1 == type2:
            return 0.5  # Same type, different parameters
        else:
            return 0.1  # Different types
