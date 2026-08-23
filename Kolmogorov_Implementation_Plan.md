# Implementation Plan: Kolmogorov Complexity Engine

## Objective
Replace the current static concept-based system with a **Recursive Induction Engine** that discovers the shortest program to solve tasks, using Kolmogorov Complexity as the universal filter.

---

## Phase 1: Minimum Description Language (MDL)

### 1.1 Define Grounded Primitives

**Spatial Primitives** (Grounded in perception):
```python
# Position & Movement
position(x, y) -> (int, int)
move(dx, dy) -> transform
rotate(degrees) -> transform
reflect(axis) -> transform
scale(factor) -> transform

# Regions
crop(x1, y1, x2, y2) -> grid
paste(grid, x, y) -> grid
```

**Visual Primitives** (Grounded in perception):
```python
# Color
color(cell) -> int
set_color(cell, value) -> void
swap_colors(c1, c2) -> transform

# Shape
boundary(region) -> list[points]
fill(region, color) -> void
flood_fill(start, color) -> void
```

**Logical Primitives** (Grounded in computation):
```python
# Control flow
if condition: block
for item in collection: block
while condition: block

# Functions
def name(params): block
return value

# Composition
map(function, collection)
filter(predicate, collection)
reduce(function, collection)
```

**Grounding Test**: Each primitive must reduce entropy when applied correctly.

---

### 1.2 MDL Grammar (BNF)

```bnf
<program> ::= <statement>*

<statement> ::= <assignment>
              | <control>
              | <function_def>
              | <return>

<assignment> ::= <var> = <expression>

<control> ::= if <expression>: <block>
            | for <var> in <expression>: <block>
            | while <expression>: <block>

<function_def> ::= def <name>(<params>): <block>

<expression> ::= <primitive>
               | <var>
               | <function_call>
               | <binary_op>

<primitive> ::= position | color | move | rotate | etc.
```

---

## Phase 2: Kolmogorov Engine Core

### 2.1 Program Representation

```python
class Program:
    def __init__(self, code: str, primitives: Dict):
        self.code = code
        self.primitives = primitives
        self.ast = parse(code)
        
    def execute(self, input_grid):
        """Execute program on input"""
        env = Environment(self.primitives)
        return self.ast.eval(env, input_grid)
    
    def length(self) -> int:
        """Kolmogorov Complexity approximation"""
        return len(self.code.replace(' ', '').replace('\n', ''))
    
    def compression_ratio(self, input_grid) -> float:
        """Σ = |Input| / |Program|"""
        input_size = input_grid.size
        program_size = self.length()
        return input_size / max(program_size, 1)
```

---

### 2.2 Program Search (Beam Search)

```python
class KolmogorovEngine:
    def __init__(self, primitives, max_length=100, beam_width=10):
        self.primitives = primitives
        self.max_length = max_length
        self.beam_width = beam_width
        self.subroutine_library = {}
        
    def find_shortest_program(self, train_examples, test_input):
        """
        Find shortest program P where:
        P(train_input_i) = train_output_i for all i
        
        Returns: (program, compression_ratio)
        """
        # Start with empty program
        beam = [Program("", self.primitives)]
        
        for length in range(1, self.max_length):
            # Generate candidates
            candidates = []
            for prog in beam:
                for extension in self._generate_extensions(prog):
                    candidates.append(extension)
            
            # Filter: Keep only programs that fit training data
            valid = []
            for prog in candidates:
                if self._fits_training_data(prog, train_examples):
                    valid.append(prog)
            
            # Prune: Keep top-k by compression ratio
            valid.sort(key=lambda p: p.compression_ratio(test_input), reverse=True)
            beam = valid[:self.beam_width]
            
            # Early stop if perfect compression found
            if beam and beam[0].compression_ratio(test_input) > 10:
                return beam[0]
        
        return beam[0] if beam else None
    
    def _generate_extensions(self, program):
        """Generate all 1-token extensions of program"""
        extensions = []
        
        # Add primitive calls
        for prim_name in self.primitives:
            new_code = program.code + f"\n{prim_name}(...)"
            extensions.append(Program(new_code, self.primitives))
        
        # Add control structures
        for control in ['if', 'for', 'while']:
            new_code = program.code + f"\n{control} ...:"
            extensions.append(Program(new_code, self.primitives))
        
        # Add subroutine calls
        for sub_name in self.subroutine_library:
            new_code = program.code + f"\n{sub_name}(...)"
            extensions.append(Program(new_code, self.primitives))
        
        return extensions
    
    def _fits_training_data(self, program, train_examples):
        """Check if program produces correct output for all training examples"""
        try:
            for example in train_examples:
                output = program.execute(example['input'])
                if not np.array_equal(output, example['output']):
                    return False
            return True
        except:
            return False
```

---

### 2.3 Subroutine Discovery

```python
class SubroutineLibrary:
    def __init__(self):
        self.library = {}
        
    def extract_subroutines(self, program):
        """
        Find repeated code patterns and extract as functions.
        Grounding: A subroutine is grounded if it reduces total entropy.
        """
        # Find repeated substrings
        code = program.code
        patterns = self._find_repeated_patterns(code)
        
        for pattern, count in patterns.items():
            if count >= 2:  # Appears at least twice
                # Calculate compression gain
                original_length = len(code)
                compressed_length = len(code.replace(pattern, f"sub_{hash(pattern)}()"))
                compressed_length += len(f"def sub_{hash(pattern)}(): {pattern}")
                
                if compressed_length < original_length:
                    # Compression gain - add to library
                    self.library[f"sub_{hash(pattern)}"] = pattern
    
    def _find_repeated_patterns(self, code, min_length=10):
        """Find all repeated substrings of minimum length"""
        patterns = {}
        for i in range(len(code)):
            for j in range(i + min_length, len(code)):
                pattern = code[i:j]
                if code.count(pattern) >= 2:
                    patterns[pattern] = code.count(pattern)
        return patterns
```

---

## Phase 3: Sovereign Engine Integration

### 3.1 Revised Equations

**Equation 1: Σ (Filter Efficiency) = Compression Ratio**
```python
def compute_sigma(program, input_grid):
    """
    Σ = |Input| / |Program|
    High Σ: Short program (good filter)
    Low Σ: Long program (poor filter)
    """
    input_entropy = input_grid.size  # Shannon entropy
    program_length = program.length()
    
    sigma = input_entropy / max(program_length, 1)
    return sigma
```

**Equation 2: dH/dt (Metabolism) = Compression Profit**
```python
def compute_metabolism(old_program, new_program):
    """
    dH/dt = |Old_Program| - |New_Program|
    Positive: Found shorter explanation (gains energy)
    Negative: Model became more complex (loses energy)
    """
    old_length = old_program.length() if old_program else float('inf')
    new_length = new_program.length()
    
    dH_dt = old_length - new_length
    return dH_dt
```

**Equation 3: Λ (Friction) = Incompressibility of Error**
```python
def compute_lambda(program, actual_output):
    """
    Λ = Kolmogorov Complexity of residual error
    Low Λ: Errors are compressible (systematic)
    High Λ: Errors are random (irreducible)
    """
    predicted_output = program.execute(input_grid)
    error = actual_output - predicted_output
    
    # Approximate K(error) using compression
    error_compressed = compress(error)  # e.g., zlib
    lambda_ = len(error_compressed) / max(error.size, 1)
    
    return lambda_
```

---

### 3.2 Prescriptive Actions (Revised)

```python
def prescribe_action(sigma, omega, lambda_):
    """
    Prescriptive table based on Σ, Ω, Λ
    """
    # Condition 1: Λ > (Σ × Ω) - System Choked
    if lambda_ > (sigma * omega):
        return "BREACH"  # Program too complex, change approach
    
    # Condition 2: Ω >> Σ - System Flooded
    if omega > 3 * sigma:
        return "REFINERY"  # Compress subroutines
    
    # Condition 3: Σ >> Ω - System Starved
    if sigma > 3 * omega:
        return "INJECTION"  # Import external subroutines
    
    # Condition 4: Program length ≈ minimum - System Solved
    if sigma > 10:  # High compression ratio
        return "DISSOLVE"  # Problem solved
    
    return "CONTINUE"
```

---

## Phase 4: Agent Integration

### 4.1 Replace RuleDiscoveryEngine

**Before** (`src/abstraction.py`):
```python
class RuleDiscoveryEngine:
    def discover_rules(self, input_grid, output_grid):
        # Hardcoded rule templates
        rules = []
        if self._check_rotation(input, output):
            rules.append(RotationRule(...))
        # etc.
```

**After** (`src/kolmogorov_engine.py`):
```python
class KolmogorovRuleEngine:
    def discover_rules(self, train_examples):
        # Find shortest program
        program = self.find_shortest_program(train_examples)
        
        # Program IS the rule
        return program
```

---

### 4.2 Update Agent

```python
# In src/agent.py

class Agent:
    def __init__(self, ...):
        # Replace vocabulary with subroutine library
        self.subroutine_library = SubroutineLibrary()
        
        # Replace rule engine with Kolmogorov engine
        self.kolmogorov_engine = KolmogorovEngine(
            primitives=MDL_PRIMITIVES,
            max_length=100,
            beam_width=10
        )
        
        # Sovereign engine now uses compression-based metrics
        self.sovereign_engine = UniversalSovereignEngine()
    
    def universal_update(self, action, observation):
        # Extract training examples
        if observation.train_examples:
            # Find shortest program
            program = self.kolmogorov_engine.find_shortest_program(
                observation.train_examples,
                observation.context
            )
            
            # Update sovereign engine with compression metrics
            sigma = compute_sigma(program, observation.context)
            omega = compute_omega(observation.context)  # Shannon entropy
            lambda_ = compute_lambda(program, observation.context)
            
            self.sovereign_engine.state.sigma = sigma
            self.sovereign_engine.state.omega = omega
            self.sovereign_engine.state.lambda_ = lambda_
            
            # Compute metabolism
            old_program = self.current_program
            dH_dt = compute_metabolism(old_program, program)
            
            # Extract subroutines if compression gain
            if dH_dt > 0:
                self.subroutine_library.extract_subroutines(program)
            
            # Store current program
            self.current_program = program
        
        # ... rest of update logic
```

---

## Phase 5: Verification

### 5.1 Test on Simple ARC Task

**Task**: Copy input to output
```python
train = [
    {'input': [[1, 2], [3, 4]], 'output': [[1, 2], [3, 4]]}
]

Expected Program:
def solve(grid):
    return grid

Compression Ratio: Σ = 4 pixels / 2 tokens = 2.0
```

### 5.2 Test on Transformation Task

**Task**: Rotate 90° clockwise
```python
train = [
    {'input': [[1, 2], [3, 4]], 'output': [[3, 1], [4, 2]]}
]

Expected Program:
def solve(grid):
    return rotate(grid, 90)

Compression Ratio: Σ = 4 pixels / 3 tokens = 1.33
```

### 5.3 Test on Complex Task

**Task**: Swap red and blue
```python
train = [
    {'input': [[1, 2, 1], [2, 1, 2]], 'output': [[2, 1, 2], [1, 2, 1]]}
]

Expected Program:
def solve(grid):
    for cell in grid:
        if color(cell) == 1:
            set_color(cell, 2)
        elif color(cell) == 2:
            set_color(cell, 1)
    return grid

Compression Ratio: Σ = 6 pixels / 8 tokens = 0.75
```

---

## Implementation Checklist

- [ ] Create `src/mdl.py` - Minimum Description Language primitives
- [ ] Create `src/kolmogorov_engine.py` - Program search and compression
- [ ] Create `src/subroutine_library.py` - Reusable function extraction
- [ ] Update `src/sovereign_engine.py` - Use compression-based Σ/Ω/Λ
- [ ] Update `src/agent.py` - Replace vocabulary with subroutines
- [ ] Create `scripts/test_kolmogorov.py` - Verification tests
- [ ] Run ARC benchmark with Kolmogorov engine
- [ ] Measure compression ratios and solve rates

---

## Expected Outcomes

1. **Σ Stability**: Compression ratio cannot collapse (always positive)
2. **Transfer Learning**: Subroutines reused across tasks
3. **Intrinsic Motivation**: Agent seeks compression, not external rewards
4. **Compositional Reasoning**: Programs can call subroutines (nested)
5. **Sample Efficiency**: Occam's Razor prefers simple explanations
6. **Solve Rate**: > 0% on ARC-AGI (current: 0%)

---

## The "Short Blade" Philosophy

**No Hardcoding**: We don't tell the agent "rotation exists"
**Universal Principle**: We tell it "find the shortest explanation"
**Emergent Discovery**: If rotation is the shortest code, agent discovers it

**This is our own math** - Kolmogorov Complexity as the foundation of intelligence.
