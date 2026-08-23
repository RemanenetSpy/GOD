import json

# Load scan results
with open('../batch_scan_results.json', 'r') as f:
    data = json.load(f)

# Find attack/broken contracts
attacks = [r for r in data if 'Reentrancy' in r.get('file', '') or 'Broken' in r.get('file', '')]

# Sort by anomaly score
attacks.sort(key=lambda x: x.get('anomaly_score', 0), reverse=True)

print("=" * 100)
print("VULNERABLE/ATTACK CONTRACTS - PURE ENGINE DETECTION")
print("=" * 100)
print()

for r in attacks:
    print(f"File: {r['file']}")
    print(f"Anomaly Score: {r.get('anomaly_score', 0):.4f} ({r.get('classification', 'N/A')})")
    print(f"Lines: {r.get('lines', 0)}")
    if 'metrics' in r:
        m = r['metrics']
        print(f"Density: mean={m.get('mean_density', 0):.3f}, peaks={m.get('density_peaks', 0)}")
        print(f"Entropy: mean={m.get('mean_entropy', 0):.3f}, variance={m.get('entropy_variance', 0):.3f}")
        print(f"Cost: total={m.get('total_cost', 0)}, outliers={m.get('cost_outliers', 0)}")
    print(f"Path: {r.get('path', 'N/A')}")
    print()

print("=" * 100)
print(f"Total attack/broken contracts found: {len(attacks)}")
print("=" * 100)
