"""
Verify Phase 18: Self-Invented Vocabulary System
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.abstraction import RuleDiscoveryEngine
from src.vocabulary import VocabularyBuilder

def test_vocabulary_learning():
    print("=== Testing Self-Invented Vocabulary ===")
    
    # 1. Create a simple context: 2x2 red square (color 2) implies blue output (color 1)
    context = np.zeros((10, 10), dtype=int)
    # Place a 2x2 red square at (2,2)
    context[2:4, 2:4] = 2
    
    # Training data: positions inside the square -> Blue (1)
    # Positions outside -> Black (0)
    training_data = []
    
    # Positive examples (inside square)
    for r in range(2, 4):
        for c in range(2, 4):
            training_data.append((r, c, 2, 1))
            
    # Negative examples (outside)
    training_data.append((0, 0, 0, 0))
    training_data.append((5, 5, 0, 0))
    
    # 2. Run Discovery
    engine = RuleDiscoveryEngine()
    # Reset vocabulary for clean test
    engine.vocabulary_builder.vocabulary = {}
    
    print("\nRunning discovery...")
    rules = engine.discover_rules(context, training_data, task_id="test_task_001")
    
    # 3. Verify Results
    print(f"\nDiscovered {len(rules)} rules.")
    
    vocab_rules = [r for r in rules if r.rule_type == "VOCABULARY"]
    print(f"Vocabulary rules found: {len(vocab_rules)}")
    
    success = False
    for rule in vocab_rules:
        print(f"  Rule: {rule.name} (Conf: {rule.confidence:.2f})")
        if "rect_2x2_c2" in rule.name:
            success = True
            print("  ✅ Found expected self-invented concept!")
            
    # 4. Verify VocabularyBuilder
    vocab_stats = engine.vocabulary_builder.get_statistics()
    print("\nVocabulary Stats:")
    print(vocab_stats)
    
    if success:
        print("\nSUCCESS: Agent invented 'rect_2x2_c2' and used it to solve the task!")
    else:
        print("\nFAILURE: Did not find expected vocabulary rule.")

if __name__ == "__main__":
    test_vocabulary_learning()
