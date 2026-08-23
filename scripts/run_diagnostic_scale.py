"""
Phase 20: Full Scale Diagnostic Run
Scales the agent to 20 diverse tasks to analyze emergent language dynamics.
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

# 20 Diverse Tasks for Stress Testing
DIAGNOSTIC_BATCH = [
    "00d62c1b", "25d8a9c8", "0ca9ddb6", "3aa6fb7a", "1e0a9b12", # The original 5
    "0520fde7", # Boolean logic / masking
    "08ed6ac7", # Color mapping by position
    "0d3d703e", # Simple color substitution
    "10fcaaa3", # Repetition / tiling
    "11852cab", # Pattern completion
    "1caeab9d", # Moving objects
    "1f0c79e5", # Directional shift
    "22168020", # Fill enclosed areas
    "23581191", # Line extension
    "25ff71a9", # Movement
    "28bf18c6", # Pattern expansion
    "3618c87e", # Gravity / stacking
    "3af2c5a8", # Reflected symmetry copies
    "4093f84a", # Noise removal / object filtering
    "4258a5f9"  # Surround shapes
]

def load_task(task_id: str):
    path = os.path.join(TASKS_DIR, f"{task_id}.json")
    if not os.path.exists(path):
        # Fallback to verify path if needed, but assuming valid IDs
        return None
    with open(path, 'r') as f:
        return json.load(f)

def run_diagnostic():
    print("=== Phase 20: Full Scale Diagnostic Run (N=20) ===")
    
    engine = RuleDiscoveryEngine()
    
    # Start fresh for the diagnostic to measure pure growth from zero
    engine.vocabulary_builder.vocabulary = {}
    engine.vocabulary_builder.save()
    
    results = []
    vocab_growth_log = []
    
    print(f"| {'ID':<4} | {'Task':<10} | {'Vocab':<5} | {'New':<3} | {'Reuse':<5} | {'Status':<10} |")
    print(f"|{'-'*6}|{'-'*12}|{'-'*7}|{'-'*5}|{'-'*7}|{'-'*12}|")
    
    for i, task_id in enumerate(DIAGNOSTIC_BATCH):
        task_data = load_task(task_id)
        if not task_data: 
            print(f"| {i+1:<4} | {task_id:<10} | {'SKIP':<5} | {'-':<3} | {'-':<5} | {'NOT FOUND':<10} |")
            continue
            
        train_examples = task_data['train']
        # Use first example for rapid discovery testing
        train_input = np.array(train_examples[0]['input'])
        train_output = np.array(train_examples[0]['output'])
        
        # Prepare basic training tuples
        training_tuples = []
        rows, cols = train_input.shape
        out_rows, out_cols = train_output.shape
        # Only map valid overlapped pixels for this test
        min_r = min(rows, out_rows)
        min_c = min(cols, out_cols)
        for r in range(min_r):
            for c in range(min_c):
                training_tuples.append((r, c, train_input[r, c], train_output[r, c]))
                
        # Metrics Before
        vocab_size_pre = len(engine.vocabulary_builder.vocabulary)
        
        # Run Rule Discovery
        try:
            rules = engine.discover_rules(train_input, training_tuples, task_id=task_id)
        except Exception as e:
            print(f"| {i+1:<4} | {task_id:<10} | {vocab_size_pre:<5} | {'ERR':<3} | {'-':<5} | {'CRASH':<10} |")
            continue
            
        # Metrics After
        vocab_size_post = len(engine.vocabulary_builder.vocabulary)
        new_concepts = vocab_size_post - vocab_size_pre
        
        vocab_based_rules = [r for r in rules if r.rule_type == "VOCABULARY"]
        reused_concepts_set = set()
        for r in vocab_based_rules:
            if 'motif_name' in r.parameters:
                reused_concepts_set.add(r.parameters['motif_name'])
        
        reuse_count = len(reused_concepts_set)
        status = "SOLVED" if len(rules) > 0 else "NO_RULES"
        
        print(f"| {i+1:<4} | {task_id:<10} | {vocab_size_post:<5} | {new_concepts:<3} | {reuse_count:<5} | {status:<10} |")
        
        # Detailed Logging
        results.append({
            "episode": i+1,
            "task_id": task_id,
            "vocab_size": vocab_size_post,
            "new_concepts": new_concepts,
            "reused_count": reuse_count,
            "reused_concepts": list(reused_concepts_set),
            "rule_count": len(rules)
        })
        
        vocab_growth_log.append(vocab_size_post)

    # Save Results
    with open("diagnostic_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"\nDiagnostic Complete. Results saved to diagnostic_results.json")
    
    # Quick Analysis
    if len(vocab_growth_log) > 0:
        total_growth = vocab_growth_log[-1]
        print(f"\nTotal Vocabulary Size: {total_growth}")
        print(f"Avg Concepts/Task: {total_growth/len(DIAGNOSTIC_BATCH):.2f}")

if __name__ == "__main__":
    run_diagnostic()
