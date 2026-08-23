import sys
import os

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.abspath("src"))
sys.path.insert(0, os.path.abspath("src/environments"))

from environments.registry import SubstrateRegistry
from civilization import SovereignCivilization

def test_environments():
    print("=================================================================")
    print("TESTING MODULAR PLUG-AND-PLAY SUBSTRATE ARCHITECTURE")
    print("=================================================================")
    
    # 1. Check available substrates
    available = SubstrateRegistry.list_available()
    print(f"Available Substrates: {available}")
    assert "classic_ca" in available
    assert "seasonal_scarcity" in available

    # 2. Test Classic CA (Epoch 1 Baseline)
    u_classic = SubstrateRegistry.get_substrate("classic_ca")
    rewards = u_classic.step({"agent_1": (5, 5)})
    clim_classic = u_classic.get_climate_telemetry()
    print(f"[Classic CA] Step OK! Season: {clim_classic['season']}")
    assert clim_classic["is_famine"] is False

    # 3. Test Seasonal Scarcity CA (Epoch 2 Dynamic Climate)
    u_season = SubstrateRegistry.get_substrate("seasonal_scarcity", season_length=400)
    seasons_observed = set()
    for step in range(400):
        rewards = u_season.step({"pioneer": (10, 10)})
        clim = u_season.get_climate_telemetry()
        seasons_observed.add(clim["season"])
        if step in [20, 120, 220, 320]:
            print(f"Step {step:3d}: [{clim['season']}] | Temp: {clim['ambient_temp']} | Regrowth: {clim['regrowth_rate']} | Famine: {clim['is_famine']}")

    assert seasons_observed == {"Spring", "Summer", "Autumn", "Winter"}
    print("[Seasonal Scarcity CA] Full 4-Season Solar Cycle Verified!")

    # 4. Test Energy Caching (Stigmergy / Storage)
    cache_ok = u_season.deposit_energy_cache(12, 12, amount=15.0)
    assert cache_ok is True
    clim_cache = u_season.get_climate_telemetry()
    assert clim_cache["cache_count"] == 1
    print(f"[Energy Caching] Successfully deposited cache at (12, 12)! Total caches: {clim_cache['cache_count']}")

    # 5. Test Sovereign Civilization with Dynamic Climate
    civ = SovereignCivilization()
    actions = civ.step(climate_telemetry=clim)
    print(f"[Civilization Integration] Step OK with dynamic climate telemetry! Active nodes: {len(civ.nodes)}")
    
    print("\nALL MODULAR SUBSTRATE & SEASONAL ENVIRONMENT TESTS PASSED!")

if __name__ == "__main__":
    test_environments()
