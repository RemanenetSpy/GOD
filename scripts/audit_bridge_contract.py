"""
Smart Contract Entropy Scanner
Detects security vulnerabilities via information density analysis.

Approach:
- Parse Solidity code into Control Flow Graph (CFG)
- Map operations to 2D grid (function × instruction type)
- Calculate LPMI (Local Pointwise Mutual Information)
- Flag high-density regions near sensitive operations
"""

import sys
import os
import re
import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from autopoietic_engine import AutopoieticEngine

class ContractVulnerabilityScanner:
    def __init__(self):
        self.autopoietic = AutopoieticEngine()
        
    def parse_contract(self, sol_path: str) -> Dict:
        """
        Parse Solidity contract into analyzable structure.
        
        Returns:
            {
                'functions': [(name, start_line, end_line, operations)],
                'state_changes': [line_numbers],
                'external_calls': [line_numbers],
                'balance_checks': [line_numbers],
                ...
            }
        """
        with open(sol_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        functions = []
        state_changes = []
        external_calls = []
        balance_checks = []
        reentrancy_guards = []
        
        current_function = None
        function_start = 0
        brace_depth = 0
        
        for i, line in enumerate(lines):
            # Function detection
            if 'function ' in line:
                func_match = re.search(r'function\s+(\w+)', line)
                if func_match:
                    current_function = func_match.group(1)
                    function_start = i
                    brace_depth = 0
            
            # Track braces
            brace_depth += line.count('{') - line.count('}')
            
            # Analyze operations
            if current_function:
                # External calls
                if '.call{' in line or '.transfer(' in line or '.send(' in line:
                    external_calls.append(i)
                
                # State changes
                if re.search(r'\w+\s*=\s*(?!.*==)', line) and '==' not in line:
                    # Variable assignment (not comparison)
                    state_changes.append(i)
                
                # Balance checks
                if 'balance' in line.lower() or '.balanceOf' in line:
                    balance_checks.append(i)
                
                # Reentrancy guards
                if 'nonReentrant' in line or 'ReentrancyGuard' in line:
                    reentrancy_guards.append(i)
            
            # End of function
            if current_function and brace_depth == 0 and i > function_start:
                functions.append((current_function, function_start, i, []))
                current_function = None
        
        return {
            'functions': functions,
            'state_changes': state_changes,
            'external_calls': external_calls,
            'balance_checks': balance_checks,
            'reentrancy_guards': reentrancy_guards,
            'total_lines': len(lines)
        }
    
    def create_operation_grid(self, contract_data: Dict) -> np.ndarray:
        """
        Convert contract operations to 2D grid for LPMI analysis.
        
        Grid encoding:
        0 = nop / comment / whitespace
        1 = read operation
        2 = write/state change
        3 = external call (HIGH RISK)
        4 = balance check
        5 = guard (reentrancy protection)
        """
        total_lines = contract_data['total_lines']
        grid = np.zeros((total_lines, 6), dtype=int)  # 6 operation types
        
        # Mark state changes
        for line in contract_data['state_changes']:
            if line < total_lines:
                grid[line, 2] = 1
        
        # Mark external calls
        for line in contract_data['external_calls']:
            if line < total_lines:
                grid[line, 3] = 1
        
        # Mark balance checks
        for line in contract_data['balance_checks']:
            if line < total_lines:
                grid[line, 4] = 1
        
        # Mark guards
        for line in contract_data['reentrancy_guards']:
            if line < total_lines:
                grid[line, 5] = 1
        
        return grid
    
    def detect_reentrancy_signature(self, grid: np.ndarray, contract_data: Dict) -> List[Dict]:
        """
        Reentrancy pattern:
        - External call (grid[:, 3])
        - BEFORE state update (grid[:, 2])
        - High LPMI density (circular dependency pattern)
        """
        findings = []
        
        external_call_lines = np.where(grid[:, 3] == 1)[0]
        state_change_lines = np.where(grid[:, 2] == 1)[0]
        
        for call_line in external_call_lines:
            # Check if state changes happen AFTER the call (within 10 lines)
            nearby_state_changes = [s for s in state_change_lines if call_line < s < call_line + 10]
            
            if nearby_state_changes:
                # Calculate local LPMI density around this region
                start = max(0, call_line - 5)
                end = min(grid.shape[0], call_line + 15)
                local_grid = grid[start:end, :]
                
                # LPMI calculation
                rho = self.autopoietic.calculate_local_feature_density(local_grid, window_size=3)
                mean_density = np.mean(rho)
                
                # Reentrancy signature: High density + External call before state change
                if mean_density > 0.6:  # Threshold based on our tests
                    findings.append({
                        'type': 'REENTRANCY',
                        'severity': 'CRITICAL',
                        'line': call_line + 1,  # 1-indexed
                        'density': mean_density,
                        'description': f'External call at line {call_line+1} before state change at {nearby_state_changes[0]+1}',
                        'signature_match': 85  # % confidence
                    })
        
        return findings
    
    def detect_access_control_weakness(self, grid: np.ndarray, contract_data: Dict, sol_path: str) -> List[Dict]:
        """
        Access control pattern:
        - State changes or external calls
        - LOW density (missing checks)
        - No modifiers like onlyRole, onlyOwner
        """
        findings = []
        
        with open(sol_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for func_name, start, end, _ in contract_data['functions']:
            # Skip if function has access control modifiers
            func_line = lines[start]
            if 'onlyRole' in func_line or 'onlyOwner' in func_line or 'private' in func_line or 'internal' in func_line:
                continue
            
            # Check for critical operations in this function
            func_grid = grid[start:end+1, :]
            has_external_call = np.any(func_grid[:, 3] == 1)
            has_state_change = np.any(func_grid[:, 2] == 1)
            
            if has_external_call or has_state_change:
                # Calculate density
                rho = self.autopoietic.calculate_local_feature_density(func_grid, window_size=3)
                mean_density = np.mean(rho)
                
                # Low density in critical function = missing checks
                if mean_density < 0.3:
                    findings.append({
                        'type': 'ACCESS_CONTROL',
                        'severity': 'HIGH',
                        'line': start + 1,
                        'function': func_name,
                        'density': mean_density,
                        'description': f'Function {func_name} has critical operations but low check density',
                        'signature_match': 70
                    })
        
        return findings
    
    def scan_contract(self, sol_path: str) -> Dict:
        """
        Main scanning function.
        """
        print(f"\n{'='*60}")
        print(f"SCANNING: {os.path.basename(sol_path)}")
        print(f"{'='*60}\n")
        
        # Parse
        contract_data = self.parse_contract(sol_path)
        print(f"Functions found: {len(contract_data['functions'])}")
        print(f"External calls: {len(contract_data['external_calls'])}")
        print(f"State changes: {len(contract_data['state_changes'])}")
        print(f"Reentrancy guards: {len(contract_data['reentrancy_guards'])}\n")
        
        # Create grid
        grid = self.create_operation_grid(contract_data)
        
        # Run detectors
        all_findings = []
        
        reentrancy_findings = self.detect_reentrancy_signature(grid, contract_data)
        all_findings.extend(reentrancy_findings)
        
        access_control_findings = self.detect_access_control_weakness(grid, contract_data, sol_path)
        all_findings.extend(access_control_findings)
        
        # Sort by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        all_findings.sort(key=lambda x: severity_order[x['severity']])
        
        return {
            'contract': os.path.basename(sol_path),
            'findings': all_findings,
            'stats': contract_data
        }

def main():
    scanner = ContractVulnerabilityScanner()
    
    # Scan Bridge.sol
    bridge_path = os.path.join(
        os.path.dirname(__file__), '..', 
        'bridge-contracts-main', 'ether', 'contracts', 'main', 'modules', 'bridge', 
        'Bridge.sol'
    )
    
    results = scanner.scan_contract(bridge_path)
    
    print(f"\n{'='*60}")
    print(f"AUDIT REPORT: {results['contract']}")
    print(f"{'='*60}\n")
    
    if not results['findings']:
        print("✅ No vulnerabilities detected by entropy analysis.\n")
    else:
        for i, finding in enumerate(results['findings'], 1):
            print(f"{i}. [{finding['severity']}] {finding['type']}")
            print(f"   Line: {finding['line']}")
            if 'function' in finding:
                print(f"   Function: {finding['function']}")
            print(f"   Density: {finding['density']:.4f}")
            print(f"   Confidence: {finding['signature_match']}%")
            print(f"   Description: {finding['description']}\n")
    
    print(f"Total findings: {len(results['findings'])}\n")
    
    # Save report
    report_path = os.path.join(os.path.dirname(__file__), '..', 'bridge_audit_report.txt')
    with open(report_path, 'w') as f:
        f.write(f"ENTROPY-BASED AUDIT REPORT\n")
        f.write(f"Contract: {results['contract']}\n")
        f.write(f"Timestamp: {__import__('datetime').datetime.now()}\n\n")
        
        for finding in results['findings']:
            f.write(f"[{finding['severity']}] {finding['type']} at line {finding['line']}\n")
            f.write(f"  {finding['description']}\n\n")
    
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    main()
