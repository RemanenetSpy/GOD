"""
Density Void Scanner
"The bug is where the structure isn't."

This scanner uses the Autopoietic Engine's Native Capability (LPMI)
to find "Holes" in the code - regions of Zero Mutual Information (Density ~ 0).

It does NOT look for "vulnerabilities".
It does NOT look for "patterns".
It looks for where the code stops being Autopoietic (self-consistent).
"""

import sys
import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from autopoietic_engine import AutopoieticEngine

class DensityVoidScanner:
    def __init__(self):
        self.engine = AutopoieticEngine()

    def scan_file(self, file_path: str) -> Dict:
        """
        Scan a file for Density Voids (LPMI ~ 0).
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            if not lines:
                return {'error': 'Empty file'}

            # 1. Convert to Grid (State Representation)
            # Consistent with previous approach to allow engine compatibility
            max_len = max(len(line) for line in lines)
            grid_size = max(len(lines), max_len)
            grid = np.zeros((grid_size, grid_size), dtype=int)
            
            for i, line in enumerate(lines):
                for j, char in enumerate(line):
                    if j < grid_size:
                        grid[i, j] = ord(char)

            # 2. Run Autopoietic Engine (Physics Calculation)
            # Calculate Local Predictive Mutual Information (LPMI)
            rho = self.engine.calculate_local_feature_density(grid, window_size=3)
            
            # 3. Find Density Voids
            # A "void" is a region where density drops significantly relative to the file's baseline.
            # We don't set a hard threshold like "0.5".
            # We look for the "lowest energy states" in the density map.
            
            # Line-level density (average density of the line's characters)
            line_densities = []
            for i in range(len(lines)):
                # Only consider the part of the line that has code
                line_len = len(lines[i])
                if line_len > 0:
                    # Get density for this row, up to line length
                    row_density = rho[i, :line_len]
                    # Filter out purely empty space if necessary, or keep it.
                    # Empty space has 0 correlation usually, but we care about CODE density.
                    # Let's filter for non-whitespace density if possible, or just raw average.
                    # Raw average is safer "pure physics".
                    avg_density = np.mean(row_density)
                    line_densities.append(avg_density)
                else:
                    line_densities.append(0.0)

            line_densities = np.array(line_densities)
            
            # Define Voids based on "Hollow Logic" relative to the file's own structure
            
            non_zero_densities = line_densities[line_densities > 0]
            if len(non_zero_densities) == 0:
                 return {'file': os.path.basename(file_path), 'voids': [], 'stats': {}}

            # "Zero Density" is relative. It's the bottom of the well.
            # Use 10th percentile as the "Void Floor"
            threshold = np.percentile(non_zero_densities, 10)
            
            # NOISE FILTER: Ignore boilerplate
            # We only want "Hollow Logic", not "Hollow Braces"
            ignore_starts = ["import ", "pragma ", "//", "/*", "*"]
            ignore_exact = ["}", "{", "};", "});", ");", ""]

            voids = []
            for i, density in enumerate(line_densities):
                content_stripped = lines[i].strip()
                
                # Check for logic density dip
                if density <= threshold and density > 0:
                    
                    # Apply Noise Filter
                    is_noise = False
                    if content_stripped in ignore_exact:
                        is_noise = True
                    for start in ignore_starts:
                        if content_stripped.startswith(start):
                            is_noise = True
                            break
                    
                    if not is_noise:
                        voids.append({
                            'line': i + 1,
                            'density': float(density),
                            'content': content_stripped[:100] # truncated
                        })
            
            # Sort voids by density (lowest first -> deepest holes)
            voids.sort(key=lambda x: x['density'])

            return {
                'file': os.path.basename(file_path),
                'path': file_path,
                'lines': len(lines),
                'voids': voids,
                'stats': {
                    'mean_density': float(np.mean(non_zero_densities)),
                    'min_density': float(np.min(non_zero_densities)),
                    'void_threshold': float(threshold)
                }
            }

        except Exception as e:
            return {'file': os.path.basename(file_path), 'error': str(e)}

    def scan_directory(self, root_dir: str) -> List[Dict]:
        results = []
        # Scan for .sol, .cpp, and .rs (Rust) files
        for ext in ['*.sol', '*.cpp', '*.rs']:
            for file_path in Path(root_dir).rglob(ext):
                print(f"Scanning Physics of: {file_path.name}...")
                result = self.scan_file(str(file_path))
                results.append(result)
        return results

def main():
    scanner = DensityVoidScanner()
    
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        # Default to current directory's parent (GOD root)
        target_dir = os.path.join(os.path.dirname(__file__), '..')
    
    print("Initiating Autopoietic Scan for Density Voids...")
    print(f"Target: {target_dir}\n")
    
    results = scanner.scan_directory(target_dir)
    
    # Analyze alignment with known vulnerabilities
    print("\n" + "="*80)
    print("DENSITY VOID REPORT")
    print("="*80 + "\n")
    
    # Filter for known vulnerable contracts/files
    vuln_keywords = ['Reentrancy', 'Broken', 'Attack', 'vulnerable', 'Vulnerable']
    
    for r in results:
        is_vuln = any(k in r['file'] for k in vuln_keywords)
        # Also report if we found ANY significant voids, regardless of filename
        has_voids = len(r.get('voids', [])) > 0
        
        if is_vuln or has_voids: 
            print(f"File: {r['file']}")
            if 'error' in r:
                print(f"  Error: {r['error']}")
                continue
                
            stats = r.get('stats', {})
            print(f"  Base Density: {stats.get('mean_density', 0):.4f}")
            print(f"  Void Threshold: {stats.get('void_threshold', 0):.4f}")
            print(f"  Detected Voids (Structure Breaks): {len(r['voids'])}")
            
            if r['voids']:
                print("  Top 3 Voids (Lowest Density):")
                for v in r['voids'][:3]:
                    print(f"    Line {v['line']} (rho={v['density']:.4f}): {v['content']}")
            print("-" * 40)

    # Save
    output_path = os.path.join(target_dir, 'density_void_results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()
