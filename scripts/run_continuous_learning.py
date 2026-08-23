"""
Phase 19: Continuous Learning Experiment Agent
Runs the agent on a sequence of diverse ARC tasks to track vocabulary growth and reuse.
"""

import json
import numpy as np
import sys
import os
import glob
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.abstraction import RuleDiscoveryEngine
from src.vocabulary import VocabularyBuilder

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ARC-AGI-master", "data", "training")

# Diverse set of tasks to test geometric vocabulary scaling
TASK_SEQUENCE = [
    "00d62c1b",  # Fill/Enclosure (detecting boundaries)
    "25d8a9c8",  # Horizontal lines / simple shapes
    "0ca9ddb6",  # Diagonal/Symmetry
    "3aa6fb7a",  # Object/Component extraction
    "1e0a9b12",  # Movement/Gravity (downward shift)
]

def load_task(task_id: str):
    path = os.path.join(TASKS_DIR, f"{task_id}.json")
    if not os.path.exists(path):
        print(f"Warning: Task {task_id} not found at {path}")
        return None
    with open(path, 'r') as f:
        return json.load(f)

def run_experiment():
    print("=== Phase 19: Continuous Learning Experiment ===")
    print(f"Goal: specific emergent vocabulary growth across {len(TASK_SEQUENCE)} tasks.")
    
    # Initialize Engine
    engine = RuleDiscoveryEngine()
    
    # 1. Start Tabula Rasa (Clear previous vocabulary)
    print("\n[INIT] Clearing vocabulary for experiment start...")
    engine.vocabulary_builder.vocabulary = {}
    engine.vocabulary_builder.save() # Save empty state
    
    vocab_history = []
    
    for i, task_id in enumerate(TASK_SEQUENCE):
        print(f"\n----------------------------------------------------------------")
        print(f"EPISODE {i+1}: Task {task_id}")
        
        task_data = load_task(task_id)
        if not task_data:
            continue
            
        train_examples = task_data['train']
        
        # We only look at the first training pair for discovery to keep it fast/focused
        # In a real run we'd use all, but for vocabulary growth checking 1 is enough to find motifs
        train_input = np.array(train_examples[0]['input'])
        train_output = np.array(train_examples[0]['output'])
        
        # Prepare training data format for engine
        training_tuples = []
        rows, cols = train_input.shape
        out_rows, out_cols = train_output.shape
        
        # Standardize sizes (naive, assuming same size for simple verification)
        if (rows, cols) == (out_rows, out_cols):
            for r in range(rows):
                for c in range(cols):
                    training_tuples.append((r, c, train_input[r, c], train_output[r, c]))
        else:
            # For different sizes, just pass empty training data implies no pixel-wise mapping
            # But we still want motif discovery on input!
            # The engine treats training_data primarily for rule verification
            # Let's just create dummy training data for input-only discovery if needed, 
            # OR better: iterate over input pixels and map to themselves 
            # to verify "copy" rules, or just pass input pixels.
            # actually discover_rules needs training data to induce input->output mapping.
            # If shape changes, pixel-wise mapping is hard.
            # For Phase 19 verification, let's focus on tasks where simple mapping might exist
            # OR just utilize the input scanning part.
            
            # Let's map valid indices only
            min_r = min(rows, out_rows)
            min_c = min(cols, out_cols)
            for r in range(min_r):
                for c in range(min_c):
                    training_tuples.append((r, c, train_input[r, c], train_output[r, c]))
        
        # RUN DISCOVERY
        print(f"Running discovery on {rows}x{cols} grid...")
        initial_vocab_size = len(engine.vocabulary_builder.vocabulary)
        
        rules = engine.discover_rules(train_input, training_tuples, task_id=task_id)
        
        # ANALYZE VOCABULARY CHANGES
        final_vocab_size = len(engine.vocabulary_builder.vocabulary)
        new_concepts = final_vocab_size - initial_vocab_size
        
        # Detect Re-use
        vocab_based_rules = [r for r in rules if r.rule_type == "VOCABULARY"]
        reused_concepts = set()
        for r in vocab_based_rules:
            if 'motif_name' in r.parameters:
                reused_concepts.add(r.parameters['motif_name'])
        
        vocab_stats = engine.vocabulary_builder.get_statistics()
        top_concepts = vocab_stats.get('top_concepts', [])
        
        print(f"\n[RESULTS] Episode {i+1} Summary:")
        print(f"  - Rules Discovered: {len(rules)}")
        print(f"  - New Concepts Invented: {new_concepts}")
        print(f"  - Total Vocabulary Size: {final_vocab_size}")
        print(f"  - Concepts Reused: {list(reused_concepts)}")
        print(f"  - Top Concepts now: {top_concepts}")
        
        if new_concepts > 0:
            # List specific new keys
            current_keys = set(engine.vocabulary_builder.vocabulary.keys())
            # We don't have previous keys easily unless we tracked them, 
            # but we can infer from the loop.
            print(f"  - Vocabulary growing... {new_concepts} added.")
            
        vocab_history.append({
            "episode": i+1,
            "task": task_id,
            "size": final_vocab_size,
            "new": new_concepts,
            "reuse": len(reused_concepts)
        })

    print("\n----------------------------------------------------------------")
    print("FINAL ANALYSIS: GROWTH DYNAMICS")
    print("Ep | Task     | Vocab Size | New | Reused")
    print("---|----------|------------|-----|-------")
    for log in vocab_history:
        print(f"{log['episode']:2d} | {log['task']} | {log['size']:10d} | {log['new']:3d} | {log['reuse']:5d}")

    # Check for convergence (reuse > new in later episodes?)
    if vocab_history[-1]['size'] > 0:
        print("\n[SUCCESS] Vocabulary system is active and evolving.")
        if len(vocab_history) >= 2 and vocab_history[-1]['new'] < vocab_history[0]['new']:
             print("[TREND] Concept invention slowing down implies convergence.")
    else:
        print("\n[FAILURE] Vocabulary did not grow.")

if __name__ == "__main__":
    run_experiment()
