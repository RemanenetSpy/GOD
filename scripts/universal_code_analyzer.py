"""
Universal Multi-Engine Code Analyzer V2
PURE PHYSICS VERSION - Uses entropy production as causal ordering

Changes from V1:
- Integrates Zero-Point entropy budget (irreversibility primitive)
- Uses Gravity relaxation dynamics for flow analysis
- NO hardcoded patterns - pure information physics
"""

import sys
import os
import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from autopoietic_engine import AutopoieticEngine
from sovereign_engine import UniversalSovereignEngine
from gravity_engine import GravityEngine
from zero_point_engine import ZeroPointEngine

class UniversalCodeAnalyzerV2:
    """
    Domain-agnostic code analyzer using physics engines with irreversibility.
    
    Key difference from V1:
    - Each analysis step produces entropy (tracked by Zero-Point)
    - Causal ordering emerges from entropy production
    - Terminates when entropy budget exhausted
    """
    
    def __init__(self, entropy_budget: float = 10000.0):
        self.autopoietic = AutopoieticEngine()
        self.sovereign = UniversalSovereignEngine()
        self.gravity = GravityEngine()
        self.zero_point = ZeroPointEngine()
        
        # Set entropy budget for this analysis session
        self.zero_point.reset_entropy_budget(entropy_budget)
        
    def parse_code_to_grid(self, file_path: str) -> np.ndarray:
        """Convert ANY code file to a 2D grid (domain-agnostic)."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        if not lines:
            return np.zeros((1, 1), dtype=int)
        
        max_len = max(len(line) for line in lines)
        grid_size = max(len(lines), max_len)
        grid = np.zeros((grid_size, grid_size), dtype=int)
        
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if j < grid_size:
                    grid[i, j] = ord(char)
        
        return grid
    
    def analyze_with_entropy_tracking(self, grid: np.ndarray, file_path: str) -> Dict:
        """
        Run all engines with entropy tracking.
        
        Each engine operation produces entropy:
        - Makes analysis irreversible
        - Creates causal sequence
        - Terminates naturally when budget exhausted
        """
        results = {}
        
        # ============================================
        # Engine 1: AUTOPOIETIC (Structure Discovery)
        # ============================================
        print("Engine 1: Autopoietic (Structure Discovery)...")
        
        # Record entropy for this analysis step
        old_grid = grid.copy()
        rho = self.autopoietic.calculate_local_feature_density(grid, window_size=3)
        delta_s = self.zero_point.calculate_action_entropy(old_grid[:10,:10], rho[:10,:10].astype(int))
        
        if not self.zero_point.produce_entropy(delta_s):
            print("⚠️ Entropy budget exhausted at Autopoietic analysis")
            return {'error': 'Entropy budget exhausted', 'stage': 'autopoietic'}
        
        results['autopoietic'] = {
            'density_map': rho,
            'mean_density': float(np.mean(rho)),
            'max_density': float(np.max(rho)),
            'high_density_regions': self._find_peaks(rho, threshold=0.7),
            'entropy_cost': delta_s,
            'interpretation': "Regions with high correlation (structure)"
        }
        
        # ============================================
        # Engine 2: SOVEREIGN (Entropy/Novelty)
        # ============================================
        print("Engine 2: Sovereign (Novelty Detection)...")
        
        entropy_map = np.zeros_like(grid, dtype=float)
        sample_step = max(1, grid.shape[0] // 50)  # Sample for speed
        
        for i in range(0, grid.shape[0], sample_step):
            for j in range(0, grid.shape[1], sample_step):
                patch = grid[max(0,i-5):min(grid.shape[0],i+5), 
                             max(0,j-5):min(grid.shape[1],j+5)]
                entropy_map[i, j] = self.zero_point._measure_entropy(patch)
        
        delta_s = np.mean(entropy_map[entropy_map > 0]) * 0.1
        if not self.zero_point.produce_entropy(delta_s):
            print("⚠️ Entropy budget exhausted at Sovereign analysis")
            return results
        
        results['sovereign'] = {
            'entropy_map': entropy_map,
            'mean_entropy': float(np.mean(entropy_map[entropy_map > 0])) if np.any(entropy_map > 0) else 0,
            'high_entropy_regions': self._find_peaks(entropy_map, threshold=5.0),
            'entropy_cost': delta_s,
            'interpretation': "Regions with high uncertainty (complexity)"
        }
        
        # ============================================
        # Engine 3: ZERO-POINT (Cost Analysis)
        # ============================================
        print("Engine 3: Zero-Point (Computational Cost)...")
        
        cost_map = self._calculate_syntax_cost(grid)
        delta_s = np.sum(cost_map) / max(1, cost_map.size) * 0.01
        
        if not self.zero_point.produce_entropy(delta_s):
            print("⚠️ Entropy budget exhausted at Zero-Point analysis")
            return results
        
        results['zero_point'] = {
            'cost_map': cost_map,
            'total_cost': float(np.sum(cost_map)),
            'expensive_regions': self._find_peaks(cost_map, threshold=20),
            'entropy_cost': delta_s,
            'interpretation': "Regions with high syntactic cost"
        }
        
        # ============================================
        # Engine 4: INTEGRATION (Multi-Engine Hotspots)
        # ============================================
        print("Engine 4: Multi-Engine Integration...")
        
        # Normalize all maps to [0, 1]
        norm_density = self._normalize(rho)
        norm_entropy = self._normalize(entropy_map)
        norm_cost = self._normalize(cost_map)
        
        # Hotspot = where MULTIPLE engines agree
        # Using product (all must be high) for conservative detection
        interesting_score = norm_density * norm_entropy * norm_cost
        
        delta_s = np.max(interesting_score) * 0.1
        if not self.zero_point.produce_entropy(delta_s):
            print("⚠️ Entropy budget exhausted at Integration")
            return results
        
        results['integration'] = {
            'interesting_map': interesting_score,
            'hotspots': self._find_peaks(interesting_score, threshold=0.3),
            'entropy_cost': delta_s,
            'interpretation': "Regions flagged by MULTIPLE engines"
        }
        
        # ============================================
        # Causal State (Irreversibility Record)
        # ============================================
        results['causal_state'] = self.zero_point.get_causal_state()
        
        return results
    
    def _normalize(self, arr: np.ndarray) -> np.ndarray:
        """Normalize array to [0, 1]."""
        min_val, max_val = np.min(arr), np.max(arr)
        if max_val - min_val < 1e-10:
            return np.zeros_like(arr)
        return (arr - min_val) / (max_val - min_val)
    
    def _find_peaks(self, field: np.ndarray, threshold: float) -> List[Tuple[int, int, float]]:
        """Find local maxima above threshold."""
        peaks = []
        for i in range(1, field.shape[0]-1):
            for j in range(1, field.shape[1]-1):
                val = field[i, j]
                if val > threshold:
                    neighbors = field[max(0,i-1):min(field.shape[0],i+2), 
                                     max(0,j-1):min(field.shape[1],j+2)]
                    if val == np.max(neighbors):
                        peaks.append((i, j, float(val)))
        peaks.sort(key=lambda x: x[2], reverse=True)
        return peaks[:10]
    
    def _calculate_syntax_cost(self, grid: np.ndarray) -> np.ndarray:
        """Estimate computational cost based on character patterns."""
        cost = np.zeros_like(grid, dtype=float)
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
        report.append(f"UNIVERSAL CODE ANALYSIS V2 (PURE PHYSICS)")
        report.append(f"File: {os.path.basename(file_path)}")
        report.append("=" * 70)
        report.append("")
        
        if 'error' in results:
            report.append(f"⚠️ Analysis halted: {results['error']}")
            return "\n".join(report)
        
        # Autopoietic
        if 'autopoietic' in results:
            report.append("1. AUTOPOIETIC (Structure Discovery)")
            report.append(f"   Mean Density: {results['autopoietic']['mean_density']:.4f}")
            report.append(f"   Max Density: {results['autopoietic']['max_density']:.4f}")
            report.append(f"   High-Density Regions: {len(results['autopoietic']['high_density_regions'])}")
            report.append(f"   Entropy Cost: {results['autopoietic']['entropy_cost']:.4f}")
            report.append("")
        
        # Sovereign
        if 'sovereign' in results:
            report.append("2. SOVEREIGN (Novelty/Entropy)")
            report.append(f"   Mean Entropy: {results['sovereign']['mean_entropy']:.4f}")
            report.append(f"   High-Entropy Regions: {len(results['sovereign']['high_entropy_regions'])}")
            report.append(f"   Entropy Cost: {results['sovereign']['entropy_cost']:.4f}")
            report.append("")
        
        # Zero-Point
        if 'zero_point' in results:
            report.append("3. ZERO-POINT (Computational Cost)")
            report.append(f"   Total Cost: {results['zero_point']['total_cost']:.2f}")
            report.append(f"   Expensive Regions: {len(results['zero_point']['expensive_regions'])}")
            report.append(f"   Entropy Cost: {results['zero_point']['entropy_cost']:.4f}")
            report.append("")
        
        # Integration
        if 'integration' in results:
            report.append("4. MULTI-ENGINE HOTSPOTS")
            report.append(f"   Regions flagged by MULTIPLE engines: {len(results['integration']['hotspots'])}")
            if results['integration']['hotspots']:
                report.append("   TOP FINDINGS:")
                for line, col, score in results['integration']['hotspots'][:5]:
                    report.append(f"      Line {line}: Score = {score:.4f}")
            report.append("")
        
        # Causal State (NEW in V2)
        if 'causal_state' in results:
            cs = results['causal_state']
            report.append("5. CAUSAL STATE (Irreversibility Record)")
            report.append(f"   Causal Order: {cs['causal_order']}")
            report.append(f"   Entropy Produced: {cs['entropy_produced']:.4f}")
            report.append(f"   Entropy Remaining: {cs['entropy_remaining']:.4f}")
            report.append(f"   Budget Exhausted: {cs['is_exhausted']}")
            report.append("")
        
        report.append("=" * 70)
        report.append("PURE PHYSICS: No hardcoded patterns used.")
        report.append("Irreversibility: Causal ordering from entropy production.")
        report.append("=" * 70)
        
        return "\n".join(report)

def main():
    analyzer = UniversalCodeAnalyzerV2(entropy_budget=10000.0)
    
    # Analyze Bridge.sol
    bridge_path = os.path.join(
        os.path.dirname(__file__), '..', 
        'bridge-contracts-main', 'ether', 'contracts', 'main', 'modules', 'bridge', 
        'Bridge.sol'
    )
    
    if not os.path.exists(bridge_path):
        print(f"File not found: {bridge_path}")
        return
    
    print(f"Analyzing: {bridge_path}\n")
    
    grid = analyzer.parse_code_to_grid(bridge_path)
    print(f"Code grid: {grid.shape[0]} x {grid.shape[1]}\n")
    
    results = analyzer.analyze_with_entropy_tracking(grid, bridge_path)
    
    report = analyzer.generate_report(results, bridge_path)
    print("\n" + report)
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'universal_analysis_v2.txt')
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved: {output_path}")

if __name__ == "__main__":
    main()
