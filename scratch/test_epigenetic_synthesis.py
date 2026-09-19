import sys
import os
import numpy as np

# Ensure root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.epigenetic_synthesizer import (
    EpigeneticOrgan,
    EpigeneticSandbox,
    EpigeneticProgramSynthesizer
)
from arc_sovereign_arena.ancestral_memory import AncestralCausalMemory
from arc_sovereign_arena.organism import ArcLivingOrganism
from arc_sovereign_arena.autopoietic_world import ArcSurvivalWorld

def test_sandbox_security():
    print("\n--- 1. Testing EpigeneticSandbox Security ---")
    
    # 1. Valid mathematical / numpy code
    valid_code = """
def test_add(grid):
    return np.sum(grid) + 42
"""
    is_valid, msg = EpigeneticSandbox.validate_ast(valid_code)
    assert is_valid, f"Expected valid code to pass, got: {msg}"
    func, c_msg = EpigeneticSandbox.compile_organ(valid_code)
    assert func is not None, f"Failed compilation: {c_msg}"
    res, ok, e_msg = EpigeneticSandbox.execute_safely(func, np.array([[1, 2], [3, 4]]))
    assert ok and res == 52, f"Expected 52, got {res}, err: {e_msg}"
    print("  [PASS] Valid code compilation & execution succeeded.")

    # 2. Block import statements
    bad_code_1 = """
import os
def malicious(grid):
    return os.listdir('.')
"""
    is_valid, msg = EpigeneticSandbox.validate_ast(bad_code_1)
    assert not is_valid and "Imports prohibited" in msg, f"Expected import block, got: {is_valid}, {msg}"
    print("  [PASS] Blocked import statement.")

    # 3. Block open / eval / dangerous builtins
    bad_code_2 = """
def malicious(grid):
    return open('test.txt', 'w')
"""
    is_valid, msg = EpigeneticSandbox.validate_ast(bad_code_2)
    assert not is_valid and "Forbidden function" in msg, f"Expected open block, got: {is_valid}, {msg}"
    print("  [PASS] Blocked dangerous builtin call.")

    # 4. Block system attribute calls
    bad_code_3 = """
def malicious(grid):
    return grid.system('dir')
"""
    is_valid, msg = EpigeneticSandbox.validate_ast(bad_code_3)
    assert not is_valid and "Forbidden attribute call" in msg, f"Expected attribute block, got: {is_valid}, {msg}"
    print("  [PASS] Blocked dangerous attribute call.")

def test_program_synthesis():
    print("\n--- 2. Testing EpigeneticProgramSynthesizer ---")
    synthesizer = EpigeneticProgramSynthesizer()
    
    # Mock train pairs
    in_grid = np.zeros((10, 10), dtype=int)
    in_grid[3:7, 3:7] = 2
    out_grid = np.zeros((10, 10), dtype=int)
    out_grid[2:8, 2:8] = 3
    
    train_pairs = [{"input": in_grid, "output": out_grid}]
    current_canvas = in_grid.copy()
    
    organs = synthesizer.synthesize_candidates(train_pairs, current_canvas, step=10)
    assert len(organs) > 0, "Expected at least 1 candidate organ synthesized"
    for o in organs:
        assert o.callable_func is not None, f"Organ {o.organ_name} has no compiled callable"
        assert o.signature != "", "Organ missing signature"
        print(f"  [PASS] Synthesized & compiled organ: {o.organ_name} (type: {o.organ_type}, sig: {o.signature})")

def test_ancestral_memory_persistence():
    print("\n--- 3. Testing Ancestral Memory Epigenetic Gene Persistence ---")
    mem = AncestralCausalMemory()
    
    dummy_code = "def sample_limb(x):\n    return x * 2"
    organ = EpigeneticOrgan(
        signature="sample_sig_123",
        organ_name="sample_limb",
        organ_type="VECTOR_NAVIGATOR",
        code_str=dummy_code,
        fitness_score=4.5
    )
    mem.record_synthesized_gene(organ.to_dict())
    
    assert "sample_sig_123" in mem.synthesized_genes
    genes = mem.get_inherited_genes()
    assert len(genes) == 1
    assert genes[0]["fitness_score"] == 4.5
    
    # Test dictionary serialization
    serialized = mem.to_dict()
    assert "synthesized_genes" in serialized
    
    mem2 = AncestralCausalMemory()
    mem2.load_dict(serialized)
    assert "sample_sig_123" in mem2.synthesized_genes
    assert mem2.synthesized_genes["sample_sig_123"]["fitness_score"] == 4.5
    print("  [PASS] Epigenetic gene inheritance serialization and reload verified.")

def test_organism_epigenetic_limbs():
    print("\n--- 4. Testing Living Organism Organ Mounting & Generational Inheritance ---")
    mem = AncestralCausalMemory()
    dummy_code = """
def custom_limb(grid):
    return grid + 1
"""
    func, _ = EpigeneticSandbox.compile_organ(dummy_code)
    organ = EpigeneticOrgan(
        signature="test_sig_abc",
        organ_name="custom_limb",
        organ_type="PATTERN_TRANSFORMER",
        code_str=dummy_code,
        fitness_score=5.0,
        callable_func=func
    )
    mem.record_synthesized_gene(organ.to_dict())

    # Create organism with ancestral memory containing gene
    org = ArcLivingOrganism(ancestral_memory=mem, generation=1)
    assert "test_sig_abc" in org.synthesized_organs
    print("  [PASS] Organism loaded and compiled inherited gene from ancestral memory.")

    # Test spawning child generation
    child = org.spawn_next_generation()
    assert "test_sig_abc" in child.synthesized_organs
    print("  [PASS] Child generation inherited epigenetic limbs from parent.")

def test_autopoietic_world_integration():
    print("\n--- 5. Testing Autopoietic World Loop with Epigenetic Engine ---")
    world = ArcSurvivalWorld()
    
    # Force low energy and high deaths to trigger epigenetic pulse
    world.organism.punish(70.0) # Drain energy below 40.0
    world.ancestral_memory.task_deaths[world.current_task_id] = 10
    
    # Tick world
    for _ in range(5):
        world.tick()
        
    state = world.get_state()
    assert "synthesized_organs" in state
    print(f"  [PASS] World ticked successfully. Synthesized organs in telemetry: {len(state['synthesized_organs'])}")

if __name__ == "__main__":
    test_sandbox_security()
    test_program_synthesis()
    test_ancestral_memory_persistence()
    test_organism_epigenetic_limbs()
    test_autopoietic_world_integration()
    print("\n==================================================")
    print("ALL EPIGENETIC SELF-SYNTHESIS TESTS PASSED (5/5)!")
    print("==================================================")
