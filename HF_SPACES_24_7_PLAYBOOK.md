# Hugging Face Spaces 24/7 Continuous Training Playbook

Running a continuous, 24/7 machine learning training pipeline (like a Kaggle self-play bot or sovereign agent society) on a Hugging Face Space requires overcoming several architectural challenges. Because cloud containers can sleep, restart, or crash, you cannot rely on in-memory state or temporary files. 

Here is the definitive guide to building a resilient, 24/7 autonomous agent on Hugging Face Spaces.

---

## 1. Persistent Storage (The `/data` Volume)
By default, any file written inside a Hugging Face Docker Space is temporary and will be permanently deleted when the Space reboots or sleeps. To run 24/7, you **must** configure persistent storage.

**How to do it:**
1. In your Hugging Face Space settings, mount a Persistent Storage volume and map it to a directory like `/data`.
2. Ensure your Python scripts write *all* downloads, datasets, checkpoints, and ML weights to this directory, not the local working directory.

```python
import os
import json

# Fallback to local directory for testing, but use /data in the HF Space
STORAGE_DIR = os.environ.get("STORAGE_DIR", "/data" if os.path.exists("/data") else "./data")
os.makedirs(STORAGE_DIR, exist_ok=True)
WEIGHTS_FILE = os.path.join(STORAGE_DIR, "best_agent_weights.json")

def save_champion(weights):
    with open(WEIGHTS_FILE, 'w') as f:
        json.dump(weights, f, indent=2)
```

---

## 2. Continuing from the Most Recent State (State Management)
Because your Space *will* inevitably reboot, your training loop must be designed to automatically resume exactly where it left off without human intervention.

**How to do it:**
At the start of your main training loop, wrap your initialization in a `try/except` block that explicitly checks for the existence of the persistent weight/state file.

```python
import os
import json
import copy

def main():
    # 1. Start with the baseline default weights
    current_brain = copy.deepcopy(DEFAULT_WEIGHTS)
    
    # 2. Check if a superior brain was already evolving before the reboot
    try:
        if os.path.exists(WEIGHTS_FILE):
            with open(WEIGHTS_FILE, 'r') as f:
                saved_weights = json.load(f)
                current_brain.update(saved_weights)
            print("Successfully restored champion brain from persistent memory!")
    except Exception as e:
        print(f"Starting from scratch with default weights: {e}")
        
    # 3. Begin continuous training loop
    while True:
        current_brain = evolve(current_brain)
        save_champion(current_brain)
```

---

## 3. Managing APIs and Rate Limits (Bulk Data vs. Scraping)
If your continuous training requires fetching live data (e.g., Kaggle replays), standard API scraping loops will quickly hit `HTTP 429: Too Many Requests` when running 24/7.

**The Solution:**
Instead of pulling thousands of files one-by-one, find a way to bulk-download aggregated daily dumps (like Kaggle Datasets).
1. Programmatically calculate the current date.
2. Search the API for the aggregated daily zip file.
3. Download it directly into the persistent `/data` volume.
4. Set a threshold (e.g., `if count < 50000`) so that when the Space reboots, it sees the data is already there and skips the massive 750MB download.

---

## 4. Bypassing the Python GIL for Heavy Compute
Hugging Face Spaces often provide massive multi-core CPUs (e.g., 192 cores). Standard Python `threading` will completely fail to utilize these cores due to the Global Interpreter Lock (GIL). 

**How to utilize 100% of the hardware:**
You must use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`. This creates completely separate Python processes that run in parallel.

```python
import multiprocessing
import concurrent.futures

cores = multiprocessing.cpu_count()

with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:
    # This maps your evaluation function across all cores simultaneously
    results = list(executor.map(evaluate_bot, population))
```
*(Note: Always put `multiprocessing.freeze_support()` inside your `if __name__ == "__main__":` block to prevent catastrophic fork loops in some container environments).*

---

## 5. Visualizing Growth Without Blocking the Pipeline
You need to see what your 24/7 bots are doing, but your UI code cannot block your heavy simulation code.

**The Architecture:**
1. **The Background Threads / Processes:** Launch your Data Miner, Offline Tuner, and Self-Play Tuner as separate `threading.Thread` or background processes running infinite `while True:` loops.
2. **The Log Files:** Have those threads `print()` their progress into a standard log file (e.g., `/data/run.log`), or capture their `stdout`.
3. **The Gradio UI:** Create a Gradio interface using the `gr.Code` or `gr.Textbox` component. Use the `every=` parameter (or Gradio's generator mechanics) to read the last 50 lines of the log file every 2 seconds. 

This creates a real-time scrolling dashboard that operates completely independently of the massive ML workloads churning in the background.
