import csv
import numpy as np

results = {}

print(f"{'GAME':<20} | {'AGENT':<15} | {'AVG SCORE':<10} | {'AVG STEPS':<10} | {'EPISODES':<5}")
print("-" * 75)

with open('arena_results.csv', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('Timestamp'):
            continue
            
        parts = line.split(',')
        
        # Heuristic to detect format
        if len(parts) == 7: # New Format: Time, Game, Agent, Ep, Score, Steps, Memory
            game = parts[1]
            agent = parts[2]
            score_idx = 4
            steps_idx = 5
        elif len(parts) == 6: # Old Format: Time, Agent, Ep, Score, Steps, Memory
            game = "Standard"
            agent = parts[1]
            score_idx = 3
            steps_idx = 4
        else:
            continue
            
        try:
            score = float(parts[score_idx])
            steps = float(parts[steps_idx])
        except ValueError:
            continue
            
        if game not in results: results[game] = {}
        if agent not in results[game]: results[game][agent] = {'scores': [], 'steps': []}
        
        results[game][agent]['scores'].append(score)
        results[game][agent]['steps'].append(steps)

for game in sorted(results.keys()):
    best_agent = None
    best_score = -float('inf')
    
    # Filter only the 4 main agents to ignore old test logs if any
    valid_agents = [a for a in results[game].keys() if a in ['QUANTUM', 'RELATIVITY', 'PHYSICS', 'INFORMATION']]
    
    for agent in sorted(valid_agents):
        avg_score = np.mean(results[game][agent]['scores'])
        avg_steps = np.mean(results[game][agent]['steps'])
        episodes = len(results[game][agent]['scores'])
        
        if avg_score > best_score:
            best_score = avg_score
            best_agent = agent
            
        print(f"{game:<20} | {agent:<15} | {avg_score:<10.1f} | {avg_steps:<10.1f} | {episodes:<5}")
    
    if best_agent:
        print(f"   🏆 WINNER: {best_agent} ({best_score:.1f})")
    print("-" * 75)
