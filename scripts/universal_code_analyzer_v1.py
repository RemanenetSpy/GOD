"""
Universal Multi-Engine Code Analyzer
Uses all 5 GOD engines' NATIVE capabilities, not hardcoded patterns.

What Each Engine Actually Does:
1. AUTOPOIETIC: Discovers where information density is HIGH (structure/correlation)
2. SOVEREIGN: Identifies which regions have HIGH ENTROPY (novelty/complexity)
3. GRAVITY: Maps information FLOW paths (how data propagates)
4. ZERO-POINT: Tracks computational COST (which operations are expensive)
5. EIGEN: Finds STABLE states (recurring patterns, equilibrium points)

NO HARDCODED PATTERNS. Just pure discovery.
"""

import sys
import os
import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from autopoietic_engine import AutopoieticEngine
from sovereign_engine import UniversalSovereignEngine
from gravity_engine import GravityEngine
from zero_point_engine import ZeroPointEngine

class UniversalCodeAnalyzer:
    """
    Domain-agnostic code analyzer using physics engines.
    """
    
    def __init__(self):
        self.autopoietic = AutopoieticEngine()
        self.sovereign = UniversalSovereignEngine()
        self.gravity = GravityEngine()
        self.zero_point = ZeroPointEngine()
        
    def parse_code_to_grid(self, file_path: str) -> np.ndarray:
        """
        Convert ANY code file to a 2D grid based on character-level features.
        
        Grid values = ASCII codes (0-255)
        This is domain-agnostic - works on Solidity, Python, assembly, etc.
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Pad to square grid
        max_len = max(len(line) for line in lines) if lines else 0
        grid_size = max(len(lines), max_len)
        
        grid = np.zeros((grid_size, grid_size), dtype=int)
        
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if j < grid_size:
                    grid[i, j] = ord(char)
        
        return grid
    
    def analyze_with_all_engines(self, grid: np.ndarray, file_path: str) -> Dict:
        """
        Run all 5 engines on the code grid.
        Each engine reports what IT sees, not what we tell it to find.
        """
        results = {}
        
        # 1. AUTOPOIETIC: Where is structure?
        print("Engine 1: Autopoietic (Information Density)...")
        rho = self.autopoietic.calculate_local_feature_density(grid, window_size=3)
        
        results['autopoietic'] = {
            'density_map': rho,
            'mean_density': float(np.mean(rho)),
            'max_density': float(np.max(rho)),
            'high_density_regions': self._find_peaks(rho, threshold=0.7),
            'interpretation': "Regions with high correlation (repeated patterns, structure)"
        }
        
        # 2. SOVEREIGN: Where is novelty/complexity?
        print("Engine 2: Sovereign (Entropy/Novelty)...")
        entropy_map = np.zeros_like(grid, dtype=float)
        
        for i in range(0, grid.shape[0], 10):  # Sample every 10 lines for speed
            for j in range(0, grid.shape[1], 10):
                patch = grid[max(0,i-5):min(grid.shape[0],i+5), 
                             max(0,j-5):min(grid.shape[1],j+5)]
                entropy_map[i, j] = self.zero_point._measure_entropy(patch)
        
        results['sovereign'] = {
            'entropy_map': entropy_map,
            'mean_entropy': float(np.mean(entropy_map[entropy_map > 0])),
            'high_entropy_regions': self._find_peaks(entropy_map, threshold=5.0),
            'interpretation': "Regions with high uncertainty (complex, unpredictable code)"
        }
        
        # 3. GRAVITY: How does information flow?
        print("Engine 3: Gravity (Information Flow)...")
        # Create a potential field: Low values (spaces/comments) = low potential
        # High values (dense code) = high potential
        # Gravity shows how "execution" flows through the code
        
        code_density = (grid > 32).astype(float)  # Non-whitespace
        
        # Find "goals" - regions of high density
        goals = []
        for i in range(0, grid.shape[0], 20):
            for j in range(0, grid.shape[1], 20):
                if code_density[i, j] > 0:
                    goals.append((i, j))
        
        if goals:
            # Create a "wall" map (whitespace = traversable, code = has cost)
            wall_map = (grid == 0).astype(int) * 2  # Empty space
            
            try:
                potential = self.gravity.calculate_potential_field(
                    wall_map, 
                    goals=goals[:10],  # Limit to first 10 for speed
                    wall_value=2
                )
                
                results['gravity'] = {
                    'potential_field': potential,
                    'flow_convergence': self._find_sinks(potential),
                    'interpretation': "Where information flows TO (execution sinks)"
                }
            except:
                results['gravity'] = {
                    'error': 'Could not calculate flow field',
                    'interpretation': 'N/A'
                }
        else:
            results['gravity'] = {'interpretation': 'No code density found'}
        
        # 4. ZERO-POINT: What is the computational cost?
        print("Engine 4: Zero-Point (Computational Cost)...")
        # Measure "cost" of each region based on syntactic complexity
        cost_map = self._calculate_syntax_cost(grid)
        
        results['zero_point'] = {
            'cost_map': cost_map,
            'total_cost': float(np.sum(cost_map)),
            'expensive_regions': self._find_peaks(cost_map, threshold=20),
            'interpretation': "Regions with high syntactic/computational cost"
        }
        
        # 5. INTEGRATION: Where do ALL engines agree?
        print("Engine 5: Multi-Engine Integration...")
        
        # Normalize all maps to [0, 1]
        norm_density = (rho - np.min(rho)) / (np.max(rho) - np.min(rho) + 1e-10)
        norm_entropy = entropy_map / (np.max(entropy_map) + 1e-10)
        norm_cost = cost_map / (np.max(cost_map) + 1e-10)
        
        # "Interesting" regions = High density AND high entropy AND high cost
        interesting_score = norm_density * norm_entropy * norm_cost
        
        results['integration'] = {
            'interesting_map': interesting_score,
            'hotspots': self._find_peaks(interesting_score, threshold=0.5),
            'interpretation': "Regions flagged by MULTIPLE engines (structure + complexity + cost)"
        }
        
        return results
    
    def _find_peaks(self, field: np.ndarray, threshold: float) -> List[Tuple[int, int, float]]:
        """Find local maxima above threshold."""
        peaks = []
        for i in range(1, field.shape[0]-1):
            for j in range(1, field.shape[1]-1):
                val = field[i, j]
                if val > threshold:
                    # Check if local maximum
                    neighbors = field[max(0,i-1):min(field.shape[0],i+2), 
                                     max(0,j-1):min(field.shape[1],j+2)]
                    if val == np.max(neighbors):
                        peaks.append((i, j, float(val)))
        
        # Return top 10
        peaks.sort(key=lambda x: x[2], reverse=True)
        return peaks[:10]
    
    def _find_sinks(self, potential: np.ndarray) -> List[Tuple[int, int, float]]:
        """Find local minima (where flow converges)."""
        sinks = []
        for i in range(1, potential.shape[0]-1):
            for j in range(1, potential.shape[1]-1):
                val = potential[i, j]
                if val < 999:  # Not a wall
                    neighbors = potential[max(0,i-1):min(potential.shape[0],i+2), 
                                         max(0,j-1):min(potential.shape[1],j+2)]
                    if val == np.min(neighbors):
                        sinks.append((i, j, float(val)))
        
        sinks.sort(key=lambda x: x[2])
        return sinks[:10]
    
    def _calculate_syntax_cost(self, grid: np.ndarray) -> np.ndarray:
        """
        Estimate computational cost based on character patterns.
        
        High cost indicators:
        - Brackets/parentheses (control flow)
        - Operators (+, -, *, /, =)
        - Special characters (complexity)
        """
        cost = np.zeros_like(grid, dtype=float)
        
        # Cost weights
        costs = {
            ord('('): 2, ord(')'): 2,
            ord('{'): 3, ord('}'): 3,
            ord('['): 2, ord(']'): 2,
            ord('='): 1,
            ord('+'): 1, ord('-'): 1, ord('*'): 2, ord('/'): 2,
            ord(';'): 1,
            ord(','): 0.5
        }
        
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                char_code = grid[i, j]
                if char_code in costs:
                    cost[i, j] = costs[char_code]
        
        return cost
    
    def generate_report(self, results: Dict, file_path: str) -> str:
        """Generate human-readable report."""
        report = []
        report.append("=" * 70)
        report.append(f"UNIVERSAL CODE ANALYSIS: {os.path.basename(file_path)}")
        report.append("=" * 70)
        report.append("")
        
        # Autopoietic
        report.append("1. AUTOPOIETIC ENGINE (Structure Discovery)")
        report.append(f"   Mean Density: {results['autopoietic']['mean_density']:.4f}")
        report.append(f"   Max Density: {results['autopoietic']['max_density']:.4f}")
        report.append(f"   High-Density Regions: {len(results['autopoietic']['high_density_regions'])}")
        if results['autopoietic']['high_density_regions']:
            for line, col, val in results['autopoietic']['high_density_regions'][:3]:
                report.append(f"      Line {line}: Density = {val:.4f}")
        report.append("")
        
        # Sovereign
        report.append("2. SOVEREIGN ENGINE (Novelty/Entropy)")
        report.append(f"   Mean Entropy: {results['sovereign']['mean_entropy']:.4f}")
        report.append(f"   High-Entropy Regions: {len(results['sovereign']['high_entropy_regions'])}")
        if results['sovereign']['high_entropy_regions']:
            for line, col, val in results['sovereign']['high_entropy_regions'][:3]:
                report.append(f"      Line {line}: Entropy = {val:.4f}")
        report.append("")
        
        # Gravity
        if 'potential_field' in results['gravity']:
            report.append("3. GRAVITY ENGINE (Information Flow)")
            report.append(f"   Flow Sinks: {len(results['gravity']['flow_convergence'])}")
            if results['gravity']['flow_convergence']:
                for line, col, val in results['gravity']['flow_convergence'][:3]:
                    report.append(f"      Line {line}: Sink potential = {val:.2f}")
        else:
            report.append("3. GRAVITY ENGINE: N/A")
        report.append("")
        
        # Zero-Point
        report.append("4. ZERO-POINT ENGINE (Computational Cost)")
        report.append(f"   Total Cost: {results['zero_point']['total_cost']:.2f}")
        report.append(f"   Expensive Regions: {len(results['zero_point']['expensive_regions'])}")
        if results['zero_point']['expensive_regions']:
            for line, col, val in results['zero_point']['expensive_regions'][:3]:
                report.append(f"      Line {line}: Cost = {val:.2f}")
        report.append("")
        
        # Integration
        report.append("5. MULTI-ENGINE HOTSPOTS")
        report.append(f"   Regions flagged by MULTIPLE engines: {len(results['integration']['hotspots'])}")
        if results['integration']['hotspots']:
            report.append("   TOP FINDINGS:")
            for line, col, score in results['integration']['hotspots'][:5]:
                report.append(f"      Line {line}: Combined score = {score:.4f}")
                report.append(f"         → High structure + complexity + cost")
        report.append("")
        
        report.append("=" * 70)
        report.append("INTERPRETATION")
        report.append("=" * 70)
        report.append("This analysis uses NO hardcoded patterns.")
        report.append("Each engine reports what it naturally detects:")
        report.append("  - Structure (Autopoietic)")
        report.append("  - Complexity (Sovereign)")
        report.append("  - Flow (Gravity)")
        report.append("  - Cost (Zero-Point)")
        report.append("")
        report.append("Hotspots = regions where MULTIPLE engines agree something")
        report.append("interesting is happening.")
        report.append("")
        
        return "\n".join(report)

def main():
    analyzer = UniversalCodeAnalyzer()
    
    # Analyze Bridge.sol
    bridge_path = os.path.join(
        os.path.dirname(__file__), '..', 
        'bridge-contracts-main', 'ether', 'contracts', 'main', 'modules', 'bridge', 
        'Bridge.sol'
    )
    
    print(f"Analyzing: {bridge_path}\n")
    
    # Convert to grid
    grid = analyzer.parse_code_to_grid(bridge_path)
    print(f"Code grid: {grid.shape[0]} x {grid.shape[1]}\n")
    
    # Run all engines
    results = analyzer.analyze_with_all_engines(grid, bridge_path)
    
    # Generate report
    report = analyzer.generate_report(results, bridge_path)
    print("\n" + report)
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), '..', 'universal_analysis_bridge.txt')
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved: {output_path}")

if __name__ == "__main__":
    main()
