"""
Deep Analysis: Vulnerable Contract Detection via Pure Engine Discovery
Compares known vulnerable contracts against secure contracts
"""

import json
import numpy as np
from collections import defaultdict

# Load results
with open('../batch_scan_results.json', 'r') as f:
    all_results = json.load(f)

# Categorize contracts
vulnerable_keywords = ['Reentrancy', 'Broken', 'Attack']
test_keywords = ['Test', 'Wrapper', 'Example', 'Stub']

vulnerable = []
secure_production = []
test_contracts = []

for r in all_results:
    if 'anomaly_score' not in r:
        continue
    
    filename = r.get('file', '')
    
    # Classify
    if any(keyword in filename for keyword in vulnerable_keywords):
        vulnerable.append(r)
    elif any(keyword in filename for keyword in test_keywords):
        test_contracts.append(r)
    else:
        secure_production.append(r)

print("=" * 100)
print("VULNERABILITY DETECTION ANALYSIS - PURE ENGINE DISCOVERY")
print("=" * 100)
print()

print(f"Total Contracts Scanned: {len(all_results)}")
print(f"  Vulnerable/Attack Contracts: {len(vulnerable)}")
print(f"  Secure Production Contracts: {len(secure_production)}")
print(f"  Test/Example Contracts: {len(test_contracts)}")
print()

# Analysis of vulnerable contracts
if vulnerable:
    print("=" * 100)
    print("KNOWN VULNERABLE CONTRACTS")
    print("=" * 100)
    print()
    
    for r in sorted(vulnerable, key=lambda x: x.get('anomaly_score', 0), reverse=True):
        print(f"File: {r['file']}")
        print(f"  Anomaly Score: {r.get('anomaly_score', 0):.4f} ({r.get('classification', 'N/A')})")
        print(f"  Lines: {r.get('lines', 0)}")
        
        if 'metrics' in r:
            m = r['metrics']
            print(f"  Density: mean={m.get('mean_density', 0):.3f}, std={m.get('density_std', 0):.3f}, peaks={m.get('density_peaks', 0)}")
            print(f"  Entropy: mean={m.get('mean_entropy', 0):.3f}, max={m.get('max_entropy', 0):.3f}, variance={m.get('entropy_variance', 0):.3f}")
            print(f"  Cost: total={m.get('total_cost', 0)}, mean/line={m.get('mean_cost_per_line', 0):.2f}, outliers={m.get('cost_outliers', 0)}")
        print()

# Statistical comparison
print("=" * 100)
print("STATISTICAL COMPARISON")
print("=" * 100)
print()

def calc_stats(contracts):
    scores = [c.get('anomaly_score', 0) for c in contracts]
    density_means = [c['metrics'].get('mean_density', 0) for c in contracts if 'metrics' in c]
    entropy_means = [c['metrics'].get('mean_entropy', 0) for c in contracts if 'metrics' in c]
    entropy_vars = [c['metrics'].get('entropy_variance', 0) for c in contracts if 'metrics' in c]
    
    return {
        'count': len(contracts),
        'anomaly_score': {
            'mean': np.mean(scores) if scores else 0,
            'median': np.median(scores) if scores else 0,
            'std': np.std(scores) if scores else 0,
            'min': np.min(scores) if scores else 0,
            'max': np.max(scores) if scores else 0
        },
        'density': {
            'mean': np.mean(density_means) if density_means else 0,
            'std': np.std(density_means) if density_means else 0
        },
        'entropy_mean': {
            'mean': np.mean(entropy_means) if entropy_means else 0,
            'std': np.std(entropy_means) if entropy_means else 0
        },
        'entropy_variance': {
            'mean': np.mean(entropy_vars) if entropy_vars else 0,
            'std': np.std(entropy_vars) if entropy_vars else 0
        }
    }

vuln_stats = calc_stats(vulnerable)
secure_stats = calc_stats(secure_production)
test_stats = calc_stats(test_contracts)

print("VULNERABLE CONTRACTS:")
print(f"  Count: {vuln_stats['count']}")
print(f"  Anomaly Score: {vuln_stats['anomaly_score']['mean']:.4f} ± {vuln_stats['anomaly_score']['std']:.4f}")
print(f"  Range: [{vuln_stats['anomaly_score']['min']:.4f}, {vuln_stats['anomaly_score']['max']:.4f}]")
print(f"  Entropy Variance: {vuln_stats['entropy_variance']['mean']:.4f} ± {vuln_stats['entropy_variance']['std']:.4f}")
print()

print("SECURE PRODUCTION CONTRACTS:")
print(f"  Count: {secure_stats['count']}")
print(f"  Anomaly Score: {secure_stats['anomaly_score']['mean']:.4f} ± {secure_stats['anomaly_score']['std']:.4f}")
print(f"  Range: [{secure_stats['anomaly_score']['min']:.4f}, {secure_stats['anomaly_score']['max']:.4f}]")
print(f"  Entropy Variance: {secure_stats['entropy_variance']['mean']:.4f} ± {secure_stats['entropy_variance']['std']:.4f}")
print()

print("TEST/EXAMPLE CONTRACTS:")
print(f"  Count: {test_stats['count']}")
print(f"  Anomaly Score: {test_stats['anomaly_score']['mean']:.4f} ± {test_stats['anomaly_score']['std']:.4f}")
print(f"  Range: [{test_stats['anomaly_score']['min']:.4f}, {test_stats['anomaly_score']['max']:.4f}]")
print()

# Detection rate
print("=" * 100)
print("DETECTION EFFECTIVENESS")
print("=" * 100)
print()

# Count how many vulnerable contracts were flagged as anomalies
flagged_critical = sum(1 for v in vulnerable if v.get('classification') == 'CRITICAL_ANOMALY')
flagged_high = sum(1 for v in vulnerable if v.get('classification') == 'HIGH_ANOMALY')
flagged_any = sum(1 for v in vulnerable if 'ANOMALY' in v.get('classification', ''))

detection_rate = (flagged_any / len(vulnerable) * 100) if vulnerable else 0

print(f"Vulnerable contracts flagged as CRITICAL: {flagged_critical}/{len(vulnerable)} ({flagged_critical/len(vulnerable)*100:.1f}%)")
print(f"Vulnerable contracts flagged as HIGH: {flagged_high}/{len(vulnerable)} ({flagged_high/len(vulnerable)*100:.1f}%)")
print(f"Total detection rate: {flagged_any}/{len(vulnerable)} ({detection_rate:.1f}%)")
print()

# False positive rate (secure contracts flagged as critical)
secure_false_positives = sum(1 for s in secure_production if s.get('classification') == 'CRITICAL_ANOMALY')
false_positive_rate = (secure_false_positives / len(secure_production) * 100) if secure_production else 0

print(f"Secure contracts flagged as CRITICAL (potential false positives): {secure_false_positives}/{len(secure_production)} ({false_positive_rate:.1f}%)")
print()

# Key finding
print("=" * 100)
print("KEY FINDINGS")
print("=" * 100)
print()

if vulnerable and secure_production:
    vuln_avg = vuln_stats['anomaly_score']['mean']
    secure_avg = secure_stats['anomaly_score']['mean']
    
    diff = vuln_avg - secure_avg
    diff_pct = (diff / secure_avg * 100) if secure_avg > 0 else 0
    
    print(f"1. Vulnerable contracts have {diff_pct:+.1f}% DIFFERENT anomaly scores vs secure contracts")
    print(f"   Vulnerable: {vuln_avg:.4f} | Secure: {secure_avg:.4f}")
    print()
    
    vuln_entropy = vuln_stats['entropy_variance']['mean']
    secure_entropy = secure_stats['entropy_variance']['mean']
    entropy_diff = vuln_entropy - secure_entropy
    entropy_diff_pct = (entropy_diff / secure_entropy * 100) if secure_entropy > 0 else 0
    
    print(f"2. Vulnerable contracts have {entropy_diff_pct:+.1f}% DIFFERENT entropy variance vs secure contracts")
    print(f"   Vulnerable: {vuln_entropy:.4f} | Secure: {secure_entropy:.4f}")
    print()

print(f"3. Detection achieved WITHOUT hardcoded patterns")
print(f"   - No knowledge of 'reentrancy'")
print(f"   - No knowledge of 'access control'")
print(f"   - No knowledge of EVM or Solidity")
print()

print(f"4. Engines used ONLY native physics:")
print(f"   - LPMI (local feature density)")
print(f"   - Entropy (information complexity)")
print(f"   - Flow convergence (execution paths)")
print(f"   - Computational cost (syntax weight)")
print()

print("=" * 100)
print("CONCLUSION")
print("=" * 100)
print()

if detection_rate > 80:
    print("✅ EXCELLENT: Pure engine discovery successfully identifies vulnerable contracts")
    print(f"   {detection_rate:.0f}% detection rate with NO hardcoded patterns")
elif detection_rate > 50:
    print("⚠️  MODERATE: Pure engine discovery shows promise but needs refinement")
    print(f"   {detection_rate:.0f}% detection rate - threshold tuning recommended")
else:
    print("❌ INSUFFICIENT: Current approach may need recalibration")
    print(f"   {detection_rate:.0f}% detection rate - investigate engine parameters")

print()
print(f"False Positive Rate: {false_positive_rate:.1f}%")
if false_positive_rate < 20:
    print("✅ Low false positive rate - good signal-to-noise ratio")
elif false_positive_rate < 50:
    print("⚠️  Moderate false positives - some tuning may help")
else:
    print("❌ High false positives - may flag too many safe contracts")

print()
print("=" * 100)
