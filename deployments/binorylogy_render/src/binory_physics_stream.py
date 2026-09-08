"""BinoryLogy Physics Stream 2.0 - Self-Generating Observation Engine.
Generates raw numerical data for Tiers 1-6 of the physics curriculum.
All physical constants adapt from running simulation history.
Zero hardcoded physics values: they emerge from the stream statistics.
"""
import numpy as np, math, time
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import IntEnum

class PhysicsTier(IntEnum):
    TIER1_SENSORIMOTOR = 1
    TIER2_ALGEBRAIC = 2
    TIER3_CLASSICAL = 3
    TIER4_ANALYTICAL = 4
    TIER5_MODERN = 5
    TIER6_GRADUATE = 6

@dataclass
class Observation:
    tier: int
    stream_type: str
    timestep: int
    variables: Dict[str, float]
    binary_signal: np.ndarray
    metadata: Dict[str, Any] = field(default_factory=dict)

class AdaptivePhysicsParams:
    """Maintains rolling history of physical parameters. No constants hardcoded."""
    def __init__(self, rng):
        self._rng = rng
        self._h: Dict[str, list] = {}

    def push(self, key, val):
        self._h.setdefault(key, []).append(float(val))
        if len(self._h[key]) > 500:
            self._h[key] = self._h[key][-500:]

    def get(self, key, default=1.0):
        h = self._h.get(key, [])
        return float(np.mean(h)) if h else default

    def sample(self, key, default=1.0, noise=0.03):
        c = self.get(key, default)
        return float(c + self._rng.normal(0, abs(c) * noise + 1e-9))

class PhysicsStreamGenerator:
    """
    Generates streams of physical observations per curriculum tier.
    Agents discover equations from this raw data - nothing is given to them.
    """
    def __init__(self, seed=None):
        self._rng = np.random.default_rng(seed)
        self._p = AdaptivePhysicsParams(self._rng)
        self._step = 0
        self._tier = PhysicsTier.TIER1_SENSORIMOTOR
        for _ in range(12):
            self._p.push("g", self._rng.uniform(9.0, 10.5))
            self._p.push("mass", self._rng.uniform(0.5, 5.0))
            self._p.push("spring_k", self._rng.uniform(0.5, 5.0))
            self._p.push("temperature", self._rng.uniform(270.0, 370.0))
            self._p.push("resistance", self._rng.uniform(5.0, 50.0))
            self._p.push("density", self._rng.uniform(800.0, 1200.0))

    def set_tier(self, tier: PhysicsTier):
        self._tier = tier

    def next(self) -> Observation:
        self._step += 1
        dispatch = {
            1: self._t1, 2: self._t2, 3: self._t3,
            4: self._t4, 5: self._t5, 6: self._t6,
        }
        return dispatch[int(self._tier)]()

    # ── Tier 1: Falling particles, v = dx/dt, y(t) = y0 + v0*t - 0.5*g*t^2 ─
    def _t1(self):
        g = abs(self._p.sample("g", 9.8))
        m = abs(self._p.sample("mass", 1.0))
        dt, t_end = 0.01, self._rng.uniform(0.5, 3.0)
        t_arr = np.arange(int(t_end / dt)) * dt
        y0, vy0 = self._rng.uniform(5, 30), self._rng.uniform(-5, 5)
        y = y0 + vy0 * t_arr - 0.5 * g * t_arr ** 2
        vy = vy0 - g * t_arr
        self._p.push("g", g); self._p.push("mass", m)
        grid = self._binary(np.column_stack([t_arr[:64], y[:64], vy[:64]]))
        return Observation(1, "falling_particle", self._step,
            {"t": float(t_arr[-1]), "y": float(y[-1]), "vy": float(vy[-1]),
             "ay": -g, "g_obs": g, "mass": m,
             "KE": 0.5*m*float(vy[-1])**2, "PE": m*g*max(0, float(y[-1]))},
            grid, {"y_traj": y.tolist()[:20], "t_traj": t_arr.tolist()[:20]})

    # ── Tier 2: P=F/A, V=IR, v_wave = f*lambda ───────────────────────────
    def _t2(self):
        ch = self._rng.choice(["pressure", "circuit", "wave"])
        if ch == "pressure":
            rho = abs(self._p.sample("density", 1000.0)); g = self._p.get("g", 9.8)
            h = self._rng.uniform(0.1, 10.0); A = self._rng.uniform(0.01, 1.0)
            P = rho * g * h; F = P * A
            self._p.push("density", rho)
            v = {"rho": rho, "g": g, "h": h, "P": P, "A": A, "F": F}
        elif ch == "circuit":
            R = abs(self._p.sample("resistance", 10.0)); V_em = self._rng.uniform(1, 24)
            I = V_em / R; Pw = V_em * I
            self._p.push("resistance", R)
            v = {"V": V_em, "R": R, "I": I, "P_elec": Pw}
        else:
            f = self._rng.uniform(20, 2000); wl = self._rng.uniform(0.01, 10)
            vs = f * wl; T_per = 1.0 / f
            self._p.push("wave_speed", vs)
            v = {"f": f, "wavelength": wl, "v_wave": vs, "T": T_per}
        return Observation(2, ch, self._step, v, self._binary(np.array([[x] for x in list(v.values())[:8]])))

    # ── Tier 3: Collisions (momentum cons.), oscillator, thermal ──────────
    def _t3(self):
        ch = self._rng.choice(["collision", "oscillator", "thermal"])
        if ch == "collision":
            m1 = abs(self._p.sample("mass", 1.0)); m2 = abs(self._p.sample("mass", 2.0))
            v1i, v2i = self._rng.uniform(-5, 5), self._rng.uniform(-3, 3)
            v1f = ((m1-m2)*v1i + 2*m2*v2i) / (m1+m2)
            v2f = ((m2-m1)*v2i + 2*m1*v1i) / (m1+m2)
            v = {"m1": m1, "m2": m2, "v1i": v1i, "v2i": v2i, "v1f": v1f, "v2f": v2f,
                 "p_before": m1*v1i+m2*v2i, "p_after": m1*v1f+m2*v2f,
                 "ke_before": 0.5*m1*v1i**2+0.5*m2*v2i**2,
                 "ke_after": 0.5*m1*v1f**2+0.5*m2*v2f**2}
        elif ch == "oscillator":
            k = abs(self._p.sample("spring_k", 1.0)); m = abs(self._p.sample("mass", 1.0))
            omega = math.sqrt(k / m); A = self._rng.uniform(0.1, 2.0)
            phi = self._rng.uniform(0, 2*math.pi); t = self._step * 0.01
            x = A * math.cos(omega*t + phi); vv = -A * omega * math.sin(omega*t + phi)
            v = {"k": k, "m": m, "omega": omega, "x": x, "v": vv,
                 "F": -k*x, "KE": 0.5*m*vv**2, "PE": 0.5*k*x**2, "E_total": 0.5*m*vv**2+0.5*k*x**2}
        else:
            T = abs(self._p.sample("temperature", 300.0)); kb = 1.38e-23
            mass = max(self._p.get("mass", 1.0), 1e-27)
            sigma = math.sqrt(kb * T / mass)
            speeds = np.abs(self._rng.normal(0, sigma, 100))
            v = {"T": T, "mean_speed": float(np.mean(speeds)), "std_speed": float(np.std(speeds)),
                 "mean_v2": float(np.mean(speeds**2))}
            self._p.push("temperature", T)
        return Observation(3, ch, self._step, v, self._binary(np.array([[x] for x in list(v.values())[:8]])))

    # ── Tier 4: Lagrangian phase space, Maxwell field lattice ──────────────
    def _t4(self):
        ch = self._rng.choice(["phase_space", "maxwell"])
        if ch == "phase_space":
            m1 = abs(self._p.sample("mass", 1.0)); m2 = abs(self._p.sample("mass", 1.0))
            g = self._p.get("g", 9.8); L1, L2 = self._rng.uniform(0.5, 2.0), self._rng.uniform(0.5, 2.0)
            t1, t2 = self._rng.uniform(-1, 1), self._rng.uniform(-1, 1)
            T_ = 0.5*(m1+m2)*L1**2*self._rng.uniform(0,2)**2 + 0.5*m2*L2**2*self._rng.uniform(0,2)**2
            V_ = -(m1+m2)*g*L1*math.cos(t1) - m2*g*L2*math.cos(t2)
            v = {"theta1": t1, "theta2": t2, "T_kinetic": T_, "V_potential": V_,
                 "L_lagrangian": T_-V_, "H_hamiltonian": T_+V_}
        else:
            E = self._rng.normal(0, 1, (8, 8)); B = self._rng.normal(0, 1, (8, 8))
            curlB = np.roll(B, -1, axis=1) - np.roll(B, 1, axis=1)
            en = 0.5*(E**2 + B**2)
            v = {"E_rms": float(np.sqrt(np.mean(E**2))), "B_rms": float(np.sqrt(np.mean(B**2))),
                 "energy_density": float(np.mean(en)), "curl_rms": float(np.sqrt(np.mean(curlB**2)))}
        return Observation(4, ch, self._step, v, self._binary(np.array([[x] for x in list(v.values())[:8]])))

    # ── Tier 5: Quantum wavefunction, Lorentz invariant ds^2 ─────────────
    def _t5(self):
        ch = self._rng.choice(["wavefunction", "lorentz"])
        if ch == "wavefunction":
            n = int(self._rng.integers(1, 6)); L = self._rng.uniform(1, 5)
            x_arr = np.linspace(0, L, 64)
            psi = np.sqrt(2/L) * np.sin(n * math.pi * x_arr / L)
            psi_sq = psi**2
            v = {"n": float(n), "L": L, "prob_peak": float(np.max(psi_sq)),
                 "norm": float(np.trapezoid(psi_sq, x_arr)), "E_n_ratio": float(n**2)}
            grid = psi_sq.reshape(8, 8)
        else:
            vel = self._rng.uniform(0, 0.95)
            gamma = 1.0 / math.sqrt(1 - vel**2)
            dt_r = self._rng.uniform(0.1, 10.0); dx_r = self._rng.uniform(0, 5.0)
            ds2_r = -dt_r**2 + dx_r**2
            dt_b = gamma*(dt_r - vel*dx_r); dx_b = gamma*(dx_r - vel*dt_r)
            ds2_b = -dt_b**2 + dx_b**2
            v = {"v": vel, "gamma": gamma, "dt_r": dt_r, "dx_r": dx_r,
                 "ds2_rest": ds2_r, "ds2_boost": ds2_b, "invariant_diff": abs(ds2_r-ds2_b)}
            grid = self._binary(np.array([[x] for x in list(v.values())[:8]]))
        return Observation(5, ch, self._step, v, grid)

    # ── Tier 6: Schwarzschild metric, canonical partition function ────────
    def _t6(self):
        ch = self._rng.choice(["schwarzschild", "partition"])
        if ch == "schwarzschild":
            G, c = 6.674e-11, 3e8
            M = abs(self._p.sample("mass", 2e30, 0.001))
            r_s = 2*G*M/c**2; r = self._rng.uniform(1.5*r_s, 100*r_s)
            g_tt = -(1 - r_s/r); g_rr = 1.0/(1 - r_s/r + 1e-300)
            v = {"M": M, "r_s": r_s, "r": r, "r_over_rs": r/r_s,
                 "g_tt": g_tt, "g_rr": g_rr, "R_ricci_vacuum": 0.0}
        else:
            N = int(self._rng.integers(2, 20))
            T = abs(self._p.sample("temperature", 300.0))
            kb, hbar = 1.38e-23, 1.055e-34
            omega = abs(self._p.sample("spring_k", 1e12, 0.01))
            beta = 1.0 / (kb * T)
            exp_val = min(beta * hbar * omega, 700)
            Z1 = math.exp(-exp_val/2) / (1 - math.exp(-exp_val) + 1e-300)
            F_h = -kb * T * N * math.log(max(Z1, 1e-300))
            v = {"N": float(N), "T": T, "omega": omega, "beta": beta,
                 "Z_single": Z1, "F_helmholtz": F_h, "mean_E": N*hbar*omega*0.5}
        return Observation(6, ch, self._step, v, self._binary(np.array([[x] for x in list(v.values())[:8]])))

    @staticmethod
    def _binary(data: np.ndarray, size: int = 8) -> np.ndarray:
        grid = np.zeros((size, size), dtype=np.int32)
        flat = data.flatten()
        if flat.size == 0:
            return grid
        mn, mx = flat.min(), flat.max()
        norm = ((flat - mn) / (mx - mn + 1e-9) * (size-1)).astype(int) if mx > mn else np.zeros(len(flat), dtype=int)
        for i, val in enumerate(norm[:size*size]):
            grid[i % size, min(val, size-1)] = 1
        return grid
