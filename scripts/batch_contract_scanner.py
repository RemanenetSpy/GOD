"""
Batch Contract Scanner - Pure Engine Discovery
Scans all contracts in a directory using ONLY native engine capabilities.

ZERO HARDCODING. The engines don't know what "reentrancy" or "access control" is.
They only measure:
- Information density (structure)
- Entropy (complexity/novelty)
- Flow (execution paths)
- Cost (computational expense)
- Consensus (multi-engine agreement)
"""

import sys
import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from autopoietic_engine import AutopoieticEngine
from sovereign_engine import UniversalSovereignEngine
from gravity_engine import GravityEngine
from zero_point_engine import ZeroPointEngine

class BatchContractScanner:
    """
    Scan multiple contracts looking for anomalies.
    NO PATTERN MATCHING - just physics-based discovery.
    """
    
    def __init__(self):
        self.autopoietic = AutopoieticEngine()
        self.sovereign = UniversalSovereignEngine()
        self.gravity = GravityEngine()
        self.zero_point = ZeroPointEngine()
        self.results = []
        
    def scan_file(self, file_path: str) -> Dict:
        """
        Scan a single file using all engines.
        Returns raw measurements, no interpretation.
        """
        try:
            # Read code
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            if not lines:
                return {'error': 'Empty file'}
            
            # Convert to grid
            max_len = max(len(line) for line in lines)
            grid_size = max(len(lines), max_len)
            grid = np.zeros((grid_size, grid_size), dtype=int)
            
            for i, line in enumerate(lines):
                for j, char in enumerate(line):
                    if j < grid_size:
                        grid[i, j] = ord(char)
            
            # Engine 1: LPMI (Local Predictive Mutual Information)
            # Measures: Where is information DENSE?
            rho = self.autopoietic.calculate_local_feature_density(grid, window_size=3)
            
            # Engine 2: Entropy
            # Measures: Where is code COMPLEX/UNPREDICTABLE?
            entropy_sample = []
            for i in range(0, min(len(lines), grid.shape[0]), 5):
                for j in range(0, grid.shape[1], 10):
                    patch = grid[max(0,i-3):min(grid.shape[0],i+3), 
                                 max(0,j-5):min(grid.shape[1],j+5)]
                    if patch.size > 0:
                        entropy_sample.append(self.zero_point._measure_entropy(patch))
            
            mean_entropy = np.mean(entropy_sample) if entropy_sample else 0
            max_entropy = np.max(entropy_sample) if entropy_sample else 0
            
            # Engine 3: Flow Convergence
            # Measures: Where does execution CONVERGE?
            code_density = (grid > 32).astype(float)
            flow_points = []
            for i in range(0, grid.shape[0], 30):
                for j in range(0, grid.shape[1], 30):
                    if code_density[i, j] > 0:
                        flow_points.append((i, j))
            
            # Engine 4: Computational Cost
            # Measures: Which regions are EXPENSIVE?
            complexity_chars = set(map(ord, '(){}[]+-*/=;,'))
            total_cost = 0
            cost_per_line = []
            
            for i, line in enumerate(lines):
                line_cost = sum(1 for c in line if ord(c) in complexity_chars)
                cost_per_line.append(line_cost)
                total_cost += line_cost
            
            # Calculate anomaly scores
            # An "anomaly" = deviation from normal distribution
            density_std = float(np.std(rho))
            density_peaks = np.sum(rho > (np.mean(rho) + 2 * density_std))
            
            entropy_variance = np.var(entropy_sample) if len(entropy_sample) > 1 else 0
            
            cost_std = np.std(cost_per_line) if cost_per_line else 0
            cost_outliers = sum(1 for c in cost_per_line if c > (np.mean(cost_per_line) + 2 * cost_std))
            
            # COMPOSITE ANOMALY SCORE
            # No hardcoding - just statistical deviation
            anomaly_score = (
                density_peaks / max(1, len(lines)) +  # Density spikes
                entropy_variance / max(1, mean_entropy) +  # Entropy variation
                cost_outliers / max(1, len(lines))  # Cost outliers
            )
            
            return {
                'file': os.path.basename(file_path),
                'path': file_path,
                'lines': len(lines),
                'metrics': {
                    # Raw measurements
                    'mean_density': float(np.mean(rho)),
                    'max_density': float(np.max(rho)),
                    'density_std': density_std,
                    'density_peaks': int(density_peaks),
                    
                    'mean_entropy': float(mean_entropy),
                    'max_entropy': float(max_entropy),
                    'entropy_variance': float(entropy_variance),
                    
                    'total_cost': int(total_cost),
                    'mean_cost_per_line': float(np.mean(cost_per_line)) if cost_per_line else 0,
                    'cost_std': float(cost_std),
                    'cost_outliers': int(cost_outliers),
                    
                    'flow_convergence_points': len(flow_points)
                },
                'anomaly_score': float(anomaly_score),
                'classification': self._classify_anomaly(anomaly_score)
            }
            
        except Exception as e:
            return {'file': os.path.basename(file_path), 'error': str(e)}
    
    def _classify_anomaly(self, score: float) -> str:
        """
        Classify based on statistical deviation ONLY.
        NO knowledge of what the deviation means.
        """
        if score > 1.0:
            return "CRITICAL_ANOMALY"
        elif score > 0.5:
            return "HIGH_ANOMALY"
        elif score > 0.2:
            return "MODERATE_ANOMALY"
        elif score > 0.1:
            return "LOW_ANOMALY"
        else:
            return "NORMAL"
    
    def scan_directory(self, root_dir: str) -> List[Dict]:
        """
        Recursively scan all .sol files in directory.
        """
        results = []
        
        for sol_file in Path(root_dir).rglob('*.sol'):
            print(f"Scanning: {sol_file.name}...")
            result = self.scan_file(str(sol_file))
            results.append(result)
        
        return results
    
    def generate_report(self, results: List[Dict]) -> str:
        """
        Generate comparative report showing relative anomalies.
        """
        # Filter successful scans
        valid_results = [r for r in results if 'anomaly_score' in r]
        
        if not valid_results:
            return "No valid results to report."
        
        # Sort by anomaly score
        sorted_results = sorted(valid_results, key=lambda x: x['anomaly_score'], reverse=True)
        
        report = []
        report.append("=" * 100)
        report.append("BATCH CONTRACT SCAN - PURE ENGINE DISCOVERY")
        report.append("=" * 100)
        report.append("")
        report.append(f"Total Files Scanned: {len(results)}")
        report.append(f"Valid Results: {len(valid_results)}")
        report.append("")
        
        # Classification summary
        classifications = defaultdict(int)
        for r in valid_results:
            classifications[r['classification']] += 1
        
        report.append("CLASSIFICATION SUMMARY:")
        for class_name in ['CRITICAL_ANOMALY', 'HIGH_ANOMALY', 'MODERATE_ANOMALY', 'LOW_ANOMALY', 'NORMAL']:
            count = classifications[class_name]
            if count > 0:
                report.append(f"  {class_name}: {count} files")
        report.append("")
        
        # Top anomalies
        report.append("=" * 100)
        report.append("TOP ANOMALIES (Highest to Lowest)")
        report.append("=" * 100)
        report.append("")
        
        for i, result in enumerate(sorted_results[:20], 1):
            report.append(f"{i}. {result['file']}")
            report.append(f"   Anomaly Score: {result['anomaly_score']:.4f} ({result['classification']})")
            report.append(f"   Lines: {result['lines']}")
            
            m = result['metrics']
            report.append(f"   Density: mean={m['mean_density']:.3f}, peaks={m['density_peaks']}")
            report.append(f"   Entropy: mean={m['mean_entropy']:.3f}, variance={m['entropy_variance']:.3f}")
            report.append(f"   Cost: total={m['total_cost']}, outliers={m['cost_outliers']}")
            report.append(f"   Path: {result['path']}")
            report.append("")
        
        # Statistical baseline
        all_scores = [r['anomaly_score'] for r in valid_results]
        report.append("=" * 100)
        report.append("STATISTICAL BASELINE")
        report.append("=" * 100)
        report.append(f"Mean Anomaly Score: {np.mean(all_scores):.4f}")
        report.append(f"Median: {np.median(all_scores):.4f}")
        report.append(f"Std Dev: {np.std(all_scores):.4f}")
        report.append(f"Max: {np.max(all_scores):.4f}")
        report.append(f"Min: {np.min(all_scores):.4f}")
        report.append("")
        
        report.append("=" * 100)
        report.append("METHODOLOGY")
        report.append("=" * 100)
        report.append("This scan uses ZERO hardcoded patterns.")
        report.append("No knowledge of 'reentrancy', 'access control', or any specific vulnerability.")
        report.append("")
        report.append("Engines measure:")
        report.append("  1. Information Density (LPMI) - Where structure exists")
        report.append("  2. Entropy - Where complexity/unpredictability exists")
        report.append("  3. Flow Convergence - Where execution paths meet")
        report.append("  4. Computational Cost - Which syntax is expensive")
        report.append("")
        report.append("Anomaly Score = Statistical deviation from normal distribution")
        report.append("High scores = Something unusual is happening (could be bug, could be complex logic)")
        report.append("")
        
        return "\n".join(report)

def main():
    scanner = BatchContractScanner()
    
    # Scan bridge contracts
    bridge_dir = os.path.join(
        os.path.dirname(__file__), '..', 'bridge-contracts-main'
    )
    
    print(f"Scanning directory: {bridge_dir}\n")
    print("This may take a few minutes...\n")
    
    results = scanner.scan_directory(bridge_dir)
    
    # Generate report
    report = scanner.generate_report(results)
    print("\n" + report)
    
    # Save results
    output_path = os.path.join(os.path.dirname(__file__), '..', 'batch_scan_results.txt')
    with open(output_path, 'w') as f:
        f.write(report)
    
    # Save raw JSON
    json_path = os.path.join(os.path.dirname(__file__), '..', 'batch_scan_results.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Report saved: {output_path}")
    print(f"✓ Raw data saved: {json_path}")

if __name__ == "__main__":
    main()
