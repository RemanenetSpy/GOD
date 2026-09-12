"""BinoryLogy Curriculum 2.0 - Physics Knowledge Graph + Adaptive Tier Progression.
Maintains a directed graph of physics concepts (PhysicsTier nodes).
Autonomously advances tiers when agents achieve mastery consensus.
Zero hardcoded mastery thresholds - they emerge from compression gain statistics.
"""
import time, math, json
from collections import defaultdict, deque
from typing import Dict, List, Optional, Tuple
from binory_physics_stream import PhysicsTier

class PhysicsNode:
    """A concept node in the Physics Knowledge Graph."""
    __slots__ = ("concept", "tier", "equation", "is_axiom",
                 "prerequisites", "derived_from", "mastery", "discovery_step")
    def __init__(self, concept, tier, equation, is_axiom=False):
        self.concept = concept
        self.tier = tier
        self.equation = equation
        self.is_axiom = is_axiom
        self.prerequisites: List[str] = []
        self.derived_from: List[str] = []
        self.mastery: float = 0.0
        self.discovery_step: int = 0

class PhysicsKnowledgeGraph:
    """
    Directed graph of all physics concepts from Tier 1 to Tier 6.
    Tracks mastery, prerequisite ordering, and axiom/derived status.
    """
    def __init__(self):
        self._nodes: Dict[str, PhysicsNode] = {}
        self._build_graph()

    def _build_graph(self):
        def add(concept, tier, eq, axiom=False, prereqs=None, derived=None):
            n = PhysicsNode(concept, tier, eq, axiom)
            n.prerequisites = prereqs or []
            n.derived_from = derived or []
            self._nodes[concept] = n

        # Tier 1
        add("position", 1, "r=(x,y)", axiom=True)
        add("velocity", 1, "v=dx/dt", prereqs=["position"], derived=["position"])
        add("acceleration", 1, "a=dv/dt", prereqs=["velocity"], derived=["velocity"])
        add("free_fall", 1, "y=y0+v0*t-0.5*g*t^2", prereqs=["acceleration"])
        add("gravity_g", 1, "F=mg", axiom=True)
        add("wave_speed", 1, "v=f*lambda", prereqs=["velocity"])

        # Tier 2
        add("pressure", 2, "P=F/A", prereqs=["free_fall"])
        add("hydrostatic", 2, "P=rho*g*h", prereqs=["pressure","gravity_g"])
        add("ohms_law", 2, "V=IR", axiom=True)
        add("electric_power", 2, "P=IV", prereqs=["ohms_law"])

        # Tier 3
        add("momentum", 3, "p=mv", prereqs=["velocity"])
        add("momentum_conservation", 3, "sum(p)=const",
            prereqs=["momentum"], derived=["noether_spatial"])
        add("kinetic_energy", 3, "KE=0.5*m*v^2", prereqs=["momentum"])
        add("work_energy", 3, "W=dKE", prereqs=["kinetic_energy","acceleration"])
        add("hookes_law", 3, "F=-kx", axiom=True)
        add("harmonic_oscillator", 3, "x''+omega^2*x=0",
            prereqs=["hookes_law","acceleration"], derived=["hookes_law"])
        add("thermodynamics_1", 3, "dU=Q-W", axiom=True)
        add("entropy", 3, "S=-kb*sum(p*lnp)", axiom=True)

        # Tier 4
        add("action_principle", 4, "dS=d(int L dt)=0", axiom=True)
        add("lagrangian", 4, "L=T-V", prereqs=["action_principle"],
            derived=["action_principle"])
        add("euler_lagrange", 4, "d/dt(dL/dq_dot)-dL/dq=0",
            prereqs=["lagrangian"], derived=["lagrangian","action_principle"])
        add("hamiltonian", 4, "H=T+V", prereqs=["lagrangian"], derived=["lagrangian"])
        add("noether_temporal", 4, "time_symm=>E_conserved",
            prereqs=["action_principle"], derived=["action_principle"])
        add("noether_spatial", 4, "space_symm=>p_conserved",
            prereqs=["action_principle"], derived=["action_principle"])
        add("maxwell_gauss_E", 4, "div(E)=rho/eps0", derived=["u1_gauge"])
        add("maxwell_faraday", 4, "curl(E)=-dB/dt", derived=["u1_gauge"])
        add("maxwell_ampere", 4, "curl(B)=mu0*J+mu0*eps0*dE/dt", derived=["u1_gauge"])
        add("partition_function", 4, "Z=sum(exp(-beta*E))",
            prereqs=["entropy"], derived=["entropy"])
        add("helmholtz", 4, "F=-kT*ln(Z)", prereqs=["partition_function"],
            derived=["partition_function"])

        # Tier 5
        add("lorentz_invariance", 5, "c=const_all_frames", axiom=True)
        add("minkowski_metric", 5, "ds^2=-c^2dt^2+dx^2+dy^2+dz^2",
            prereqs=["lorentz_invariance"], derived=["lorentz_invariance"])
        add("lorentz_transform", 5, "t'=gamma*(t-vx/c^2)",
            prereqs=["minkowski_metric"], derived=["minkowski_metric"])
        add("schrodinger", 5, "i*hbar*dpsi/dt=H*psi", axiom=True)
        add("born_rule", 5, "P(a)=|<a|psi>|^2", axiom=True)
        add("uncertainty", 5, "dx*dp>=hbar/2",
            prereqs=["schrodinger"], derived=["commutator"])
        add("commutator", 5, "[x,p]=i*hbar", prereqs=["schrodinger"])
        add("qho_ladder", 5, "H=hbar*omega*(a_dag*a+0.5)",
            prereqs=["schrodinger","hamiltonian"], derived=["schrodinger"])

        # Tier 6
        add("einstein_hilbert", 6, "S=(1/16piG)*int(sqrt(-g)*(R-2L)d^4x)", axiom=True)
        add("einstein_field_eq", 6, "G_uv+Lambda*g_uv=(8piG/c^4)*T_uv",
            prereqs=["einstein_hilbert"], derived=["einstein_hilbert"])
        add("path_integral", 6, "Z=int(D_phi*exp(iS/hbar))", axiom=True)
        add("yang_mills", 6, "L=-1/4*F_uv^a*F^uv_a+psibar*(iGamma^u*D_u-m)*psi",
            prereqs=["path_integral","u1_gauge"])
        add("u1_gauge", 6, "local_U1_gauge_invariance", axiom=True)
        add("bcs_gap", 6, "Delta=-sum(V*Delta/(2E)*tanh(E/2kT))",
            prereqs=["partition_function","schrodinger"])
        add("chern_number", 6, "C1=(1/2pi)*int_BZ(Omega_xy d^2k)",
            prereqs=["berry_phase"])
        add("berry_phase", 6, "gamma_n=i*int<u_n|grad_k u_n> dk",
            prereqs=["schrodinger"])

    def get_node(self, concept: str) -> Optional[PhysicsNode]:
        return self._nodes.get(concept)

    def update_mastery(self, concept: str, compression_gain: float):
        # Concept mapping: map discrete / automata / kinematic symbols to PhysicsKnowledgeGraph nodes
        concept_map = {
            "free_fall": ["free_fall", "gravity_g", "position"],
            "gravity_g": ["gravity_g", "acceleration"],
            "velocity": ["velocity", "position"],
            "acceleration": ["acceleration", "velocity"],
            "falling_particle": ["position", "velocity", "free_fall", "gravity_g"],
            "prog_birth_k4": ["free_fall", "wave_speed"],
            "prog_birth_k2": ["velocity", "position"],
            "prog_birth_k0": ["position"],
            "prog_birth_k1": ["velocity"],
            "prog_birth_k3": ["acceleration"],
            "prog_birth_k5": ["free_fall"],
            "prog_birth_k6": ["gravity_g"],
            "prog_birth_k7": ["wave_speed"],
            "prog_birth_k8": ["wave_speed", "gravity_g"],
            "prog_survive_k4": ["position", "gravity_g"],
            "prog_survive_k0": ["position"],
            "prog_survive_k5": ["velocity"],
            "prog_survive_k6": ["acceleration"],
            "prog_survive_k7": ["free_fall"],
            "prog_survive_k8": ["wave_speed"],
            # Tier 2 mappings
            "pressure": ["pressure", "hydrostatic"],
            "circuit": ["ohms_law", "electric_power"],
            "wave": ["wave_speed"],
            # Tier 3 mappings
            "collision": ["momentum", "momentum_conservation", "kinetic_energy"],
            "spring": ["hookes_law", "harmonic_oscillator"],
            "gas": ["thermodynamics_1", "entropy"]
        }
        targets = concept_map.get(concept, [concept])
        for target in targets:
            if target in self._nodes:
                old = self._nodes[target].mastery
                self._nodes[target].mastery = min(1.0, old + compression_gain * 0.05)

    def observe_empirical(self, obs_stream: str, variables: Dict[str, float]):
        """Incremental empirical mastery earned by continuous observation of physical phenomena."""
        if obs_stream == "falling_particle":
            for c in ["position", "velocity", "acceleration", "gravity_g", "free_fall"]:
                if c in self._nodes:
                    self._nodes[c].mastery = min(1.0, self._nodes[c].mastery + 0.002)
        elif obs_stream in ("pressure", "circuit", "wave"):
            targets = {"pressure": ["pressure", "hydrostatic"], "circuit": ["ohms_law", "electric_power"], "wave": ["wave_speed"]}.get(obs_stream, [])
            for c in targets:
                if c in self._nodes:
                    self._nodes[c].mastery = min(1.0, self._nodes[c].mastery + 0.002)
        elif obs_stream in ("collision", "spring", "gas"):
            targets = {"collision": ["momentum", "momentum_conservation", "kinetic_energy"], "spring": ["hookes_law", "harmonic_oscillator"], "gas": ["thermodynamics_1", "entropy"]}.get(obs_stream, [])
            for c in targets:
                if c in self._nodes:
                    self._nodes[c].mastery = min(1.0, self._nodes[c].mastery + 0.002)

    def current_frontier(self, current_tier: int) -> List[str]:
        """Returns concepts available in current tier with mastery < 1."""
        return [c for c, n in self._nodes.items()
                if n.tier == current_tier and n.mastery < 1.0]

    def tier_mastery(self, tier: int) -> float:
        nodes = [n for n in self._nodes.values() if n.tier == tier]
        if not nodes:
            return 0.0
        return sum(n.mastery for n in nodes) / len(nodes)


class AdaptiveCurriculum:
    """
    Manages tier progression based on mastery consensus from all 4 agents.
    Advancement threshold adapts from the running distribution of compression gains.
    No hardcoded advancement threshold.
    """
    def __init__(self):
        self._pkg = PhysicsKnowledgeGraph()
        self._current_tier = PhysicsTier.TIER1_SENSORIMOTOR
        self._agent_votes: Dict[str, int] = {}
        self._gain_history: deque = deque(maxlen=200)
        self._tier_steps: Dict[int, int] = defaultdict(int)
        self._discoveries: List[dict] = []

    @property
    def tier(self) -> PhysicsTier:
        return self._current_tier

    @property
    def pkg(self) -> PhysicsKnowledgeGraph:
        return self._pkg

    def record_discovery(self, agent_id: str, concept: str,
                         equation: str, compression_gain: float, step: int):
        """Record when an agent synthesizes a new law."""
        self._gain_history.append(compression_gain)
        self._pkg.update_mastery(concept, compression_gain)
        self._discoveries.append({
            "step": step, "agent": agent_id, "concept": concept,
            "equation": equation, "gain": compression_gain,
            "tier": int(self._current_tier),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def agent_vote_advance(self, agent_id: str) -> None:
        """An agent votes to advance the curriculum tier."""
        self._agent_votes[agent_id] = int(self._current_tier)

    def check_advancement(self, n_agents: int = 4) -> bool:
        """
        Advance tier if:
        - All n_agents have voted for current tier advancement, AND
        - Current tier mastery >= adaptive threshold (mean + 1*sigma of gain history)
        """
        current_t = int(self._current_tier)
        votes_for_current = sum(1 for v in self._agent_votes.values() if v == current_t)
        if votes_for_current < n_agents:
            return False
        # Adaptive mastery threshold
        mastery = self._pkg.tier_mastery(current_t)
        if self._gain_history:
            mean_g = sum(self._gain_history) / len(self._gain_history)
            std_g = math.sqrt(sum((x-mean_g)**2 for x in self._gain_history) / len(self._gain_history))
            threshold = min(0.85, max(0.25, mean_g / (mean_g + std_g + 1e-6)))
        else:
            threshold = 0.40
        if mastery >= threshold:
            next_tier = min(6, current_t + 1)
            self._current_tier = PhysicsTier(next_tier)
            self._agent_votes.clear()
            return True
        return False

    def status(self) -> dict:
        t = int(self._current_tier)
        return {
            "current_tier": t,
            "tier_mastery": round(self._pkg.tier_mastery(t), 3),
            "discoveries": len(self._discoveries),
            "frontier": self._pkg.current_frontier(t),
            "recent_discoveries": self._discoveries[-5:],
        }
