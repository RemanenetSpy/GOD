"""
The Sovereign Test: The Multidimensional Jump (Code Discovery)

Hypothesis:
Legacy Code Analysis uses "Parsers" (Logic).
GOD System uses "Physics" (Information Density).

We treat a binary stream (Assembly) as a physical material.
- Loops/Recursion = High Structure (Crystals).
- Random Data = High Entropy (Gas).

The Autopoietic Engine should 'light up' the logic skeleton without knowing what an Opcode is.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from autopoietic_engine import AutopoieticEngine

def generate_mock_assembly_stream(size=1024):
    """
    Generate a byte stream that mimics a program.
    Contains:
    1. Random 'Data' sections (Noise).
    2. Structured 'Code' sections (Loops/Repeats).
    """
    stream = np.zeros(size, dtype=int)
    
    # 1. Background: Random Data (Heap/Stack noise)
    # High Entropy
    stream[:] = np.random.randint(0, 256, size)
    
    # 2. Inject Code Structure (The "Biology")
    # A Loop is a repeated sequence of instructions.
    # e.g. MOV, ADD, CMP, JNE (4 bytes repeated)
    # Let's create a 'Crystal' of logic in the middle.
    
    loop_opcode = [0x90, 0x89, 0xC3, 0xEB] # NOP, MOV, ADD, JMP (Mock)
    
    # Inject a "Main Loop" at index 200 to 400
    print("Injecting Logic Crystal (Loop) at offset 200-400...")
    for i in range(200, 400, 4):
        stream[i:i+4] = loop_opcode
        
    # Inject a "Recursive Function" at index 600 to 700
    # A recursive pattern might look like: PUSH, CALL, POP, RET
    func_opcode = [0x55, 0xE8, 0x5D, 0xC3]
    print("Injecting Logic Crystal (Recursion) at offset 600-700...")
    for i in range(600, 700, 4):
        stream[i:i+4] = func_opcode
        
    return stream

def run_code_discovery():
    print("Initializing Autopoietic Engine (Code Biology Mode)...")
    engine = AutopoieticEngine()
    
    # 1. Get Data
    stream = generate_mock_assembly_stream(1024)
    
    # 2. Transform to 2D Manifold (Hex Editor View)
    # We wrap the 1D stream into a 2D grid (Width 32)
    # This allows the 'Neighbor' kernel to find local correlations 
    # both spatially (next instruction) and temporally (across loops if stride aligns).
    width = 32
    height = len(stream) // width
    grid = stream.reshape((height, width))
    
    print(f"Mapped {len(stream)} bytes to {height}x{width} Manifold.")
    
    # 3. Calculate Discovery Metric (LPMI)
    print("Calculating Information Density (Rho_D)...")
    rho = engine.calculate_local_feature_density(grid, window_size=3)
    
    # 4. Filter: High Gravity only
    gravity = engine.get_discovery_metric(grid)
    
    # Visualize
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    
    # Raw Data (Bytes)
    axes[0].imshow(grid, cmap='viridis', aspect='auto')
    axes[0].set_title("Raw Memory (Assembly)")
    axes[0].set_ylabel("Memory Address")
    
    # Information Density
    im2 = axes[1].imshow(rho, cmap='magma', aspect='auto')
    axes[1].set_title("Logic Density (Rho_D)")
    plt.colorbar(im2, ax=axes[1])
    
    # Gravity
    im3 = axes[2].imshow(gravity, cmap='gray_r', aspect='auto')
    axes[2].set_title("Gravity Well (Structure)")
    
    plt.savefig("code_biology_proof.png")
    print("Saved code_biology_proof.png")
    
    # Analyze
    # We expect high density in rows corresponding to 200-400 and 600-700
    # 200//32 = Row 6
    # 400//32 = Row 12
    # 600//32 = Row 18
    # 700//32 = Row 21
    
    row_density = np.mean(rho, axis=1)
    
    # Check "Logic" regions vs "Data" regions
    logic_rows = list(range(6, 13)) + list(range(18, 22))
    data_rows = list(range(0, 5)) + list(range(25, 30))
    
    mean_logic = np.mean(row_density[logic_rows])
    mean_data = np.mean(row_density[data_rows])
    
    print(f"Mean Density in LOGIC Regions: {mean_logic:.4f}")
    print(f"Mean Density in DATA Regions:  {mean_data:.4f}")
    
    if mean_logic > mean_data * 1.5:
        print("\n🏆 SUCCESS: The Engine detected the Program Skeleton!")
        print("It separated 'Order' (Code) from 'Entropy' (Data).")
    else:
        print("\nFAILURE: Distinction too weak.")

if __name__ == "__main__":
    run_code_discovery()
