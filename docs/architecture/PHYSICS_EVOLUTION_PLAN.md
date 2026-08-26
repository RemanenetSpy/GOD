# GOD System: Physics Evolution Plan
## Adding Irreversibility (The Missing Primitive)

**Date**: 2026-01-20  
**Objective**: Fix the "causality vacuum" using pure physics (no hardcoding)

---

## The Core Insight (from change.md)

**What we rejected**: Clock-time (`t`, seconds, steps)  
**What we accidentally removed**: Ordering / Direction / Irreversibility

> "Gravity works because the universe has a **direction of relaxation** (entropy gradient), not because it has a clock."

**The Problem**:
- ✅ Fields exist
- ✅ Potentials exist  
- ✅ Gradients exist
- ❌ Nothing answers: "Which update happens before which?"

**Result**: Symmetry never breaks → Motion never commits → System freezes

---

## Audit: What We Got Right vs Wrong

### ✅ CORRECT (Validated by Tests)

| Claim | Evidence | Status |
|-------|----------|--------|
| Gravity (Eikonal) beats local potentials | 260 cells vs 0 (legacy) | **PROVEN** |
| Manifold IS Gravity done right | Both got 260 cells | **PROVEN** |
| Sovereign = Intrinsic Motivation RL | 245 cells, clears fog efficiently | **PROVEN** |
| Zero-Point = Constraint/Survival | 184 cells, stops when "safe" | **PROVEN** |
| Autopoietic = Self-Organization | Sorted colors without rules | **PROVEN** |
| Ontology beats Phenomenology | Manifold > Gravity_Legacy | **PROVEN** |

### ❌ WRONG (What Broke)

| Claim | Reality | Root Cause |
|-------|---------|------------|
| Eigen = Optimal Transport | Actually: Greedy best-first | Never implemented Sinkhorn properly |
| System can "move" autonomously | System is STATIC | No irreversible primitive |
| Pursuit adapts to targets | Pursuit never commits | No causal ordering |
| ARC 99% solvable | Only patterns with known physics | Hardcoded transformation library |

---

## The Fix: Add ONE Irreversible Primitive

**Options** (from change.md):
1. **Relaxation Steps** - Field settles until stable
2. **Entropy Budget** - Each update consumes irreversibility
3. **Event Ordering** - A happens because B already happened
4. **Monotonic Loss** - Something can only decrease

**Recommended**: **Entropy Budget** (fits Zero-Point Engine naturally)

### Why Entropy Budget?

1. **Already have the infrastructure**: Zero-Point tracks "energy"
2. **Pure physics**: Entropy always increases (2nd Law)
3. **No clock needed**: Just track total entropy produced
4. **Natural termination**: When entropy budget exhausted → system stops

---

## Evolution Plan: Pure Physics (No Hardcoding)

### Phase 1: Entropy Budget (Zero-Point Upgrade)

**Current**:
```python
self.energy = 100.0
# Decreases arbitrarily per step
```

**New Physics**:
```python
self.entropy_produced = 0.0
self.entropy_budget = 1000.0  # Total allowed irreversibility

def update(self, action):
    # Each action produces entropy (irreversible)
    delta_S = self._calculate_entropy_production(action)
    self.entropy_produced += delta_S
    
    if self.entropy_produced >= self.entropy_budget:
        return HALT  # System has exhausted its irreversibility
```

**Why this is physics**: 
- Real systems can't run forever
- Each decision has thermodynamic cost
- Not a "rule", it's the 2nd Law

---

### Phase 2: Causal Ordering (Gravity Upgrade)

**Current Problem**: 
- Eikonal calculates potential field
- But which point moves first? All equally valid.

**New Physics** (Relaxation Dynamics):
```python
def evolve_field(self, current_state):
    # Calculate potential
    potential = self.calculate_potential_field(...)
    
    # Relaxation step: Move toward gradient
    gradient = np.gradient(potential)
    
    # IRREVERSIBILITY: Can't undo this step
    new_state = current_state - self.dt * gradient
    
    # Entropy production (tracks irreversibility)
    delta_S = np.sum(np.abs(new_state - current_state))
    
    return new_state, delta_S
```

**Key**: The `delta_S` creates ordering. Steps that produce more entropy are "later" in causality.

---

### Phase 3: Eigen Engine (Actually Implement Optimal Transport)

**Current**: Broken (Greedy best-first)

**Required Physics**: Sinkhorn Algorithm (Wasserstein Distance)

```python
def optimal_transport(self, source, target):
    """
    Find minimum-entropy transport plan from source to target.
    
    This is TRUE "tunneling" - doesn't solve for path,
    solves for probability flow.
    """
    # Cost matrix (how expensive to move mass from i to j)
    C = self._compute_cost_matrix(source, target)
    
    # Sinkhorn iterations (entropy-regularized OT)
    K = np.exp(-C / self.regularization)
    u, v = self._sinkhorn_iterations(K, source, target)
    
    # Transport plan
    P = np.diag(u) @ K @ np.diag(v)
    
    return P
```

**Why this matters**: 
- Gravity finds geodesics (continuous paths)
- Eigen finds teleportation (discontinuous jumps)
- Both are valid physics, different regimes

---

### Phase 4: Autopoietic Discovery (No Transformation Library)

**What we learned**: LPMI (Local Pointwise Mutual Information) finds structure without knowing what to look for.

**New Capability**: Universal Discovery
```python
def discover(self, data_grid):
    """
    Find structure in ANY data without prior knowledge.
    
    Returns: density_map (where structure exists)
    
    NO TRANSFORMATION LIBRARY.
    NO DOMAIN KNOWLEDGE.
    """
    rho = self.calculate_local_feature_density(data_grid)
    
    # High density = structure (correlated)
    # Low density = noise (random)
    
    return rho
```

**The key insight**: 
- Don't ask "is this reentrancy?"
- Ask "where is information density anomalous?"
- Let the PHYSICS tell you what's interesting

---

## Updated Engine Definitions

### 1. Sovereign (The Mind)
- **Physics**: Entropy-seeking (maximizes information gained)
- **Role**: Decides WHERE to look
- **Irreversibility**: Consumes attention budget

### 2. Gravity (The Body)
- **Physics**: Eikonal equation (geodesic flow)
- **Role**: Moves through space
- **Irreversibility**: Each step produces friction entropy

### 3. Zero-Point (The Metabolism)
- **Physics**: 2nd Law thermodynamics
- **Role**: Tracks total entropy produced
- **Irreversibility**: THE PRIMITIVE (entropy budget)

### 4. Eigen (The Quantum Layer)
- **Physics**: Optimal transport (Wasserstein)
- **Role**: Teleportation / discontinuous jumps
- **Irreversibility**: Tunneling has entropy cost

### 5. Autopoietic (The Soul)
- **Physics**: Self-organization (LPMI clustering)
- **Role**: Discovers structure
- **Irreversibility**: Crystallization is one-way

---

## What This Solves

| Problem | Root Cause | Fix |
|---------|------------|-----|
| System freezes | No causal ordering | Entropy budget creates sequence |
| Pursuit never adapts | Symmetry never breaks | Irreversible steps break ties |
| Hardcoded patterns | Domain knowledge baked in | LPMI finds ANY structure |
| Eigen broken | Never implemented | Add Sinkhorn OT |

---

## Validation Plan

### Test 1: Entropy Production Tracking
- **Input**: Simple maze
- **Measure**: Total entropy produced per run
- **Pass if**: Entropy monotonically increases, system halts when budget exhausted

### Test 2: Causal Ordering
- **Input**: Symmetric 4-way maze (like our failure case)
- **Current**: Decision paralysis (all directions equal)
- **Pass if**: System chooses ONE direction (symmetry breaks via entropy)

### Test 3: Eigen Teleportation
- **Input**: Maze with disconnected regions
- **Current**: System stuck
- **Pass if**: Eigen "tunnels" through wall (with entropy cost)

### Test 4: Universal Discovery
- **Input**: Unknown code (new language, new patterns)
- **Pass if**: LPMI finds structure without domain-specific rules

---

## Summary

**What we're adding**: ONE irreversible primitive (entropy budget)

**What we're NOT adding**:
- ❌ Time (no clocks)
- ❌ Hardcoded rules
- ❌ Domain-specific patterns
- ❌ Prediction / future modeling

**Result**: System becomes:
- ✅ Timeless (no `t` variable)
- ✅ Physical (real thermodynamics)
- ✅ Directional (entropy creates causality)
- ✅ Finite (budget creates termination)

**The Final Truth**:
> "Gravity doesn't know time. But it knows direction. That's the missing piece."

---

## Implementation Priority

1. **High**: Zero-Point entropy budget (enables everything else)
2. **High**: Gravity relaxation dynamics (causal ordering)
3. **Medium**: Eigen Sinkhorn implementation (teleportation)
4. **Low**: Autopoietic refinement (already working)

**Timeline**: 1-2 weeks for full implementation

**Status**: Ready to proceed when approved.
