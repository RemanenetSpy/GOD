# How to Change Number of Steps in main.py

## Quick Answer

There are **2 places** to change the number of steps:

### 1. Simple Text Demo (Option 1)
**Line 160** in `main.py`:
```python
agent, env = run_episode(num_steps=50, render=True, seed=42)
```

Change `50` to any number you want (e.g., `100`, `200`, `500`)

### 2. Visual Demo (Option 2)
**Line 189** in `main.py`:
```python
visualize_episode(num_steps=100, seed=42, save_animation=True)
```

Change `100` to any number you want

---

## Step-by-Step Instructions

### Option A: Edit Manually

1. Open `main.py` in your editor
2. Find line 160 (for text demo) or line 189 (for visual demo)
3. Change the number
4. Save the file
5. Run `python main.py`

### Option B: I'll Edit It For You

Tell me:
- How many steps do you want? (e.g., 100, 200, 500, 1000)
- For which mode? (text demo, visual demo, or both)

---

## Recommended Values

| Steps | Time | Best For |
|-------|------|----------|
| 50 | ~5 sec | Quick test |
| 100 | ~10 sec | Default demo |
| 200 | ~20 sec | More exploration |
| 500 | ~50 sec | Full map exploration |
| 1000 | ~2 min | Complete mastery |

**Note**: Agent has 100 energy, so it can run ~1000 steps before depleting (each move costs 0.1 energy)

---

## Example: Change to 200 Steps

**Before** (line 160):
```python
agent, env = run_episode(num_steps=50, render=True, seed=42)
```

**After**:
```python
agent, env = run_episode(num_steps=200, render=True, seed=42)
```

---

## Want Me to Change It?

Just tell me the number and I'll update it for you! 

For example:
- "Change to 200 steps"
- "Make it 500 steps for both demos"
- "Set text demo to 100 and visual to 300"
