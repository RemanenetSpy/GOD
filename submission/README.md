# ARC-AGI-3 Submission Scaffold

This folder contains a minimal submission-ready agent scaffold for the ARC-AGI-3 competition.

## Files

- `arc_submission_agent.py` — baseline agent implementing the required behavior interface.

## Required interface

The competition expects an agent that can decide when to stop and which action to take:

- `is_done(frames, latest_frame)`
- `choose_action(frames, latest_frame)`

The scaffold in `arc_submission_agent.py` follows that contract.

## How to use

Run the local inspection script:

```bash
python submission/arc_submission_agent.py --env-dir ./environment_files
```

## Submission guidance

1. Replace the default heuristic logic in `ARCAGI3Agent.choose_action` with a stronger game-specific policy.
2. Keep the method names and signatures unchanged.
3. Validate the agent against the public game files before submitting.
4. Keep the agent deterministic and lightweight.

This is a valid starting point for a Kaggle submission structure, but it is intentionally a baseline, not a claim of a solved ARC-AGI-3 agent.
