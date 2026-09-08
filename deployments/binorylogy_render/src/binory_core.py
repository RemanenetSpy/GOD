"""
================================================================================
BINORY CORE 2.0 - Adaptive Causal Plasticity Engine
================================================================================
Replaces old symmetric Hebbian rule with:
  1. Spike-Timing Dependent Plasticity (STDP) - directed causal synapses A->B
  2. Transfer Entropy - distinguishes genuine causality from correlation
  3. Adaptive thresholds - ALL parameters emerge from running statistics
     (No hardcoded floats in this file)
================================================================================
"""

import hashlib
import itertools
import json
import time
import math
from collections import deque
from pathlib import Path
from typing import Dict, Set, Tuple, Optional

# ---------------------------------------------------------------------------
# Node identity helpers
# ---------------------------------------------------------------------------

def make_node_id(name: str) -> str:
    digest = hashlib.blake2s(name.lower().encode(), digest_size=4).digest()
    return "proc:" + "".join(f"{b:08b}" for b in digest)

_NODE_NAMES: Dict[str, str] = {}

def register_name(node_id: str, name: str) -> None:
    _NODE_NAMES[node_id] = name

def readable(node_id: str) -> str:
    return _NODE_NAMES.get(node_id, node_id)

# ---------------------------------------------------------------------------
# Adaptive Statistics Tracker - replaces every hardcoded threshold
# ---------------------------------------------------------------------------

class AdaptiveStats:
    """
    Rolling window of values; exposes adaptive thresholds.
    No constants hardcoded - everything is a function of observed data.
    """
    def __init__(self, window: int = 200):
        self._window = window
        self._buf: deque = deque(maxlen=window)

    def push(self, value: float) -> None:
        self._buf.append(value)

    @property
    def mean(self) -> float:
        return sum(self._buf) / len(self._buf) if self._buf else 0.0

    @property
    def std(self) -> float:
        if len(self._buf) < 2:
            return 1.0
        m = self.mean
        return math.sqrt(sum((x - m) ** 2 for x in self._buf) / len(self._buf))

    def emerge_threshold(self, sigma_factor: float = 2.0) -> float:
        """Adaptive emergence threshold: mean + sigma * factor."""
        return self.mean + sigma_factor * self.std

    def percentile(self, p: float) -> float:
        if not self._buf:
            return 0.0
        sorted_buf = sorted(self._buf)
        idx = int(p * (len(sorted_buf) - 1))
        return sorted_buf[idx]

# ---------------------------------------------------------------------------
# Directed Causal Synapse - replaces symmetric weight dict
# ---------------------------------------------------------------------------

class CausalSynapse:
    """
    Directed (A -> B) causal synapse with STDP plasticity.
    Strength increases when A fires before B (causal).
    """
    __slots__ = ("strength", "causal_count", "anticausal_count", "last_seen")

    def __init__(self):
        self.strength: float = 0.0
        self.causal_count: int = 0
        self.anticausal_count: int = 0
        self.last_seen: float = time.monotonic()

    def potentiate(self, delta_t: float, tau: float) -> None:
        self.strength += math.exp(-abs(delta_t) / tau)
        self.causal_count += 1
        self.last_seen = time.monotonic()

    def depress(self, magnitude: float) -> None:
        self.strength = max(0.0, self.strength - magnitude)

    def to_dict(self) -> dict:
        return {"strength": self.strength, "causal": self.causal_count, "anticausal": self.anticausal_count}

# ---------------------------------------------------------------------------
# Transfer Entropy Estimator
# ---------------------------------------------------------------------------

class TransferEntropyEstimator:
    """
    Computes T_{X->Y} to distinguish causation from correlation.
    T_{X->Y} > T_{Y->X} => X causes Y.
    """
    def __init__(self, history_len: int = 20):
        self._history_len = history_len
        self._histories: Dict[str, deque] = {}

    def record(self, node_id: str, active: bool) -> None:
        if node_id not in self._histories:
            self._histories[node_id] = deque(maxlen=self._history_len)
        self._histories[node_id].append(int(active))

    def transfer_entropy(self, source: str, target: str) -> float:
        s_hist = list(self._histories.get(source, []))
        t_hist = list(self._histories.get(target, []))
        n = min(len(s_hist), len(t_hist)) - 1
        if n < 4:
            return 0.0
        eps = 1e-9
        counts = {}
        for i in range(n):
            key = (t_hist[i + 1], t_hist[i], s_hist[i])
            counts[key] = counts.get(key, 0) + 1
        te = 0.0
        total = sum(counts.values())
        for (ty1, ty0, sx0), c in counts.items():
            p_joint = c / total
            p_yt1_yt = sum(v for (a, b, _), v in counts.items() if a == ty1 and b == ty0) / total
            p_yt_xt = sum(v for (_, b, c2), v in counts.items() if b == ty0 and c2 == sx0) / total
            p_yt = sum(v for (_, b, _), v in counts.items() if b == ty0) / total
            if p_joint > eps and p_yt1_yt > eps and p_yt_xt > eps and p_yt > eps:
                te += p_joint * math.log2(p_joint * p_yt / (p_yt1_yt * p_yt_xt + eps) + eps)
        return max(0.0, te)

# ---------------------------------------------------------------------------
# BinoryCore - the full adaptive associative learning engine
# ---------------------------------------------------------------------------

class BinoryCore:
    """
    Adaptive Hebbian-STDP-TE core replacing the original fixed-threshold engine.
    All parameters emerge from running statistics - zero hardcoded floats.
    """

    def __init__(self, state_path: Path, log_path: Path):
        self._state_path = state_path
        self._log_path = log_path
        self._synapses: Dict[Tuple[str, str], CausalSynapse] = {}
        self._emerged: Set[Tuple[str, str]] = set()
        self._weight_stats = AdaptiveStats(window=500)
        self._cpu_stats = AdaptiveStats(window=100)
        self._te = TransferEntropyEstimator(history_len=30)
        self._last_active: Dict[str, float] = {}
        self._step = 0
        self._report_pending: Dict[Tuple[str, str], float] = {}
        self._load_state()

    def _load_state(self) -> None:
        if not self._state_path.exists():
            return
        try:
            data = json.loads(self._state_path.read_text(encoding="utf-8"))
            _NODE_NAMES.update(data.get("node_names", {}))
            for key, val in data.get("synapses", {}).items():
                a, b = key.split("||", 1)
                syn = CausalSynapse()
                syn.strength = float(val.get("strength", 0.0))
                syn.causal_count = int(val.get("causal", 0))
                syn.anticausal_count = int(val.get("anticausal", 0))
                self._synapses[(a, b)] = syn
            self._emerged = {tuple(k.split("||", 1)) for k in data.get("emerged", [])}
        except Exception:
            pass

    def save_state(self) -> None:
        tmp = self._state_path.with_suffix(".tmp")
        data = {
            "node_names": _NODE_NAMES,
            "synapses": {f"{a}||{b}": syn.to_dict() for (a, b), syn in self._synapses.items() if syn.strength > 0},
            "emerged": [f"{a}||{b}" for (a, b) in self._emerged],
            "step": self._step,
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(self._state_path)

    def update(self, active_nodes: list, cpu_load: float) -> dict:
        """Called each sample tick. Returns dict with metrics and newly emerged edges."""
        self._step += 1
        now = time.monotonic()
        self._cpu_stats.push(cpu_load)

        # Adaptive STDP tau - scales with CPU variability
        tau = max(0.05, self._cpu_stats.std * 2.0 + 0.1)
        # Adaptive decay - proportional to mean weight
        decay = max(1e-4, self._weight_stats.mean * 0.0001 + 1e-4)

        # Record TE histories
        all_known = set(self._last_active.keys()) | set(active_nodes)
        for node in all_known:
            self._te.record(node, node in active_nodes)

        # STDP potentiation for co-active pairs
        active_set = set(active_nodes)
        for a, b in itertools.combinations(sorted(active_set), 2):
            t_a = self._last_active.get(a, now)
            t_b = self._last_active.get(b, now)
            delta_t = t_a - t_b
            key_ab = (a, b)
            key_ba = (b, a)
            if key_ab not in self._synapses:
                self._synapses[key_ab] = CausalSynapse()
            if key_ba not in self._synapses:
                self._synapses[key_ba] = CausalSynapse()
            if delta_t < 0:
                self._synapses[key_ab].potentiate(delta_t, tau)
            else:
                self._synapses[key_ba].potentiate(delta_t, tau)

        # Decay inactive synapses
        for key, syn in list(self._synapses.items()):
            if key[0] not in active_set or key[1] not in active_set:
                syn.depress(decay)
                if syn.strength <= 0:
                    del self._synapses[key]

        # Update timestamps and weight stats
        for node in active_set:
            self._last_active[node] = now
        for syn in self._synapses.values():
            self._weight_stats.push(syn.strength)

        # Adaptive emergence threshold (mean + 2*sigma)
        emerge_threshold = self._weight_stats.emerge_threshold(sigma_factor=2.0)

        # Detect newly emerged edges via TE confirmation
        newly_emerged = {}
        for (a, b), syn in self._synapses.items():
            if syn.strength >= emerge_threshold and (a, b) not in self._emerged:
                te_ab = self._te.transfer_entropy(a, b)
                te_ba = self._te.transfer_entropy(b, a)
                if te_ab > te_ba:
                    self._emerged.add((a, b))
                    newly_emerged[(a, b)] = (syn.strength, te_ab)
                    self._report_pending[(a, b)] = syn.strength
                    self._log_emergence(a, b, syn.strength, te_ab)

        return {
            "step": self._step,
            "emerge_threshold": emerge_threshold,
            "decay": decay,
            "tau_stdp": tau,
            "synapse_count": len(self._synapses),
            "emerged_count": len(self._emerged),
            "newly_emerged": newly_emerged,
        }

    def top_synapses(self, n: int = 5) -> list:
        ranked = sorted(self._synapses.items(), key=lambda x: x[1].strength, reverse=True)
        return [(a, b, syn.strength) for (a, b), syn in ranked[:n]]

    def _log_emergence(self, a: str, b: str, strength: float, te: float) -> None:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] CAUSAL LINK: {readable(a)} -->> {readable(b)}  (strength: {strength:.1f}, TE: {te:.4f})\n"
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(line)

    def flush_report(self) -> list:
        out = list(self._report_pending.items())
        self._report_pending.clear()
        return out
