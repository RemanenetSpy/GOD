"""
========================================================================================
SOVEREIGN MULTIVERSE 21-UNIVERSE TELEMETRY INSPECTOR
========================================================================================
Scrapes live step counts, active populations, and discovered Kolmogorov subroutines
across all 21 parallel universes (7 Realms x 3 Branches) directly from the Cloud Vault.
========================================================================================
"""

import os
import sys
import json
import urllib.request
from typing import Dict, Any

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_env():
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    if k not in os.environ:
                        os.environ[k] = v


load_env()
HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_REPO = os.environ.get("HF_DATASET_REPO", "Explorerp/sovereign-civilization-memory")

BASE_URL = f"https://huggingface.co/datasets/{HF_REPO}/raw/main/"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

REALMS = [
    ("r1", "🏛️ Realm 1: Classic Discrete CA"),
    ("r2", "🍂 Realm 2: Seasonal Scarcity CA"),
    ("r3", "🌊 Realm 3: Continuous Wave Lenia"),
    ("r4", "🧬 Realm 4: Reaction-Diffusion Turing"),
    ("r5", "⚡ Realm 5: Wireworld Digital Circuit"),
    ("r6", "💨 Realm 6: Lattice Gas Hydrodynamics"),
    ("r7", "⚔️ Realm 7: Red Queen Co-Evolution Arena")
]

BRANCHES = [
    ("a", "Univ A (Ancient 10 Pop)"),
    ("b", "Univ B (Pioneers 10 Pop - Pruned)"),
    ("c", "Univ C (Colony 35 Pop)")
]


def inspect_multiverse():
    print("=" * 80)
    print("🌌 SOVEREIGN MULTIVERSE TELEMETRY: 21 LIVING UNIVERSES (STEP 0 FRESH GENESIS)")
    print(f"Vault: https://huggingface.co/datasets/{HF_REPO}")
    print("=" * 80)

    total_steps = 0
    total_laws = 0

    for rid, rname in REALMS:
        print(f"\n{rname}:")
        for bid, bname in BRANCHES:
            fname = f"civilization_{rid}_{bid}.json"
            url = BASE_URL + fname
            try:
                req = urllib.request.Request(url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    steps = data.get("step_num", 0)
                    pop = data.get("population", 0)
                    subs = data.get("subroutines", {})
                    climate = data.get("climate", {})
                    
                    total_steps += steps
                    total_laws += len(subs)
                    
                    icon = climate.get("season_icon", "✨")
                    biomass = climate.get("total_biomass", "N/A")
                    print(f"  [{rid}_{bid}] {bname:<32} | Step: {steps:<7} | Pop: {pop:<2} | Laws: {len(subs):<2} | {icon} Biomass: {biomass}")
            except Exception:
                print(f"  [{rid}_{bid}] {bname:<32} | [Fresh Genesis Starting / Syncing...]")

    print("\n" + "=" * 80)
    print(f"MULTIVERSE AGGREGATE: Total Steps: {total_steps:,} | Total Discovered Laws: {total_laws}")
    print("=" * 80)


if __name__ == "__main__":
    inspect_multiverse()
