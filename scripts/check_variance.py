import csv
import numpy as np

data = {}

with open('data/arena_results.csv', 'r') as f:
    for line in f:
        line = line.strip()
        parts = line.split(',')
        if len(parts) >= 6 and parts[1] != 'Game': # Skip header
             # Format: Timestamp,Game,Agent,Episode,Score,Steps,Memory
             if len(parts) == 7:
                 if parts[4] == 'Score': continue
                 game = parts[1]
                 agent = parts[2]
                 score = float(parts[4])
             elif len(parts) == 6: # Old format
                 if parts[3] == 'Score': continue
                 game = "Standard"
                 agent = parts[1]
                 score = float(parts[3])
             else:
                 continue

             key = f"{game}_{agent}"
             if key not in data: data[key] = []
             data[key].append(score)

print(f"{'GAME_AGENT':<40} | {'RUNS':<5} | {'STD DEV':<10} | {'MEAN':<10} | {'LAST 10'}")
print("-" * 100)

for key, scores in data.items():
    if len(scores) > 5: 
        # Focus on the most recent runs (likely the fixed seed ones)
        recent_scores = scores[-50:] 
        std_dev = np.std(recent_scores)
        mean_score = np.mean(recent_scores)
        last_10 = str(recent_scores[-10:])
        print(f"{key:<40} | {len(recent_scores):<5} | {std_dev:<10.2f} | {mean_score:<10.1f} | {last_10}")
