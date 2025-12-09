# PRARTIGHAT.AI
**PRATIGHAT.AI** is an indigenous, enterprise-grade AI-powered penetration testing and cyber defense platform proudly made in India. It combines cutting-edge artificial intelligence with comprehensive security testing tools to provide a complete offensive security solution.
# PRATIGHAT.AI — Full Technical Whitebook (Complete English Edition)
### Autonomous Red-Team Intelligence Engine for Authorized Cyber Ranges
**Author:** Aman Rajak
**Version:** 1.0 (2025)

---

# Table of Contents
1. Executive Summary
2. Purpose of This Whitebook
3. System Vision & Philosophy
4. Core Features Overview
5. Full Technical Stack
6. System Architecture (High-Level)
7. Cognitive Architecture (LLM Brain)
8. Multi-Agent System Architecture
9. PRATIGHAT-CORE (Central Brain)
10. Operational Modes
11. Routing Layer (Offline / Online / Hybrid)
12. Jailbreak & Prompt-Rewrite Layer
13. Adaptive Hardware Mode (AHM)
14. Fractal Enumeration Engine
15. Genetic Exploit Evolution Engine
16. Quantum Attack Path Prediction Engine
17. Tool Integration Architecture (Parrot OS)
18. Memory Engine & Knowledge Graph
19. Terminal UI Architecture
20. Reporting Engine
21. Internal API Routes & Module Map
22. Complete Folder Structure (Production Spec)
23. Development Standards
24. Installation & Deployment Overview
25. Safety, Compliance & Ethical Use
26. Future Enhancements
27. Conclusion

---

# 1. Executive Summary
PRATIGHAT.AI is an **autonomous red-team intelligence engine** designed for **authorized cyber ranges, academic training environments, and security research labs**. It combines:

- Multi-agent cognitive reasoning
- Offline LLM processing
- Red-team simulation
- ParrotOS tool orchestration
- Predictive attack path modeling
- Fractal enumeration
- Genetic exploit evolution
- Multilingual personality control (English primary)

This whitebook provides **every technical detail required** for anyone to rebuild, extend, or integrate PRATIGHAT.AI.

---

# 2. Purpose of This Whitebook
This whitebook serves as a **complete technical reference blueprint** for:
- Researchers building autonomous cyber-AI systems
- Developers implementing multi-agent architectures
- Cyber educators teaching red-team automation
- Engineers integrating AI with OS-level tools

The whitebook covers **architecture, routes, modules, algorithms, and full technical stack**.

---

# 3. System Vision & Philosophy
PRATIGHAT.AI aims to:
- Simulate red-team reasoning
- Perform deep reconnaissance & enumeration
- Produce educational PoCs and reports
- Operate offline without cloud dependency
- Adapt to any hardware profile
- Maintain strict safety & compliance

It is **not a real attack tool**, but a **simulation engine** for safe cyber-learning.

---

# 4. Core Features Overview
- Autonomous red-team AI
- Multi-agent cognitive engine
- Fractal enumeration engine
- Genetic exploit evolution
- Quantum path prediction
- Adaptive hardware optimization
- Offline + hybrid LLM routing
- ParrotOS tool orchestration
- Live terminal visual interface
- Automatic reporting system

---

# 5. Full Technical Stack

## Backend
- **Python 3.12+** (core engine)
- FastAPI (internal APIs)
- LangGraph (multi-agent orchestration)
- AsyncIO (concurrency)

## LLM Layer
- Ollama (offline model hosting)
- GGUF models (Llama 3.x, Qwen, DeepSeek)
- Optional cloud LLMs via API

## System Tools (Parrot OS Integration)
- nmap, masscan, gobuster, wfuzz
- sqlmap, hydra, hashcat, nikto
- wpscan, linpeas, winpeas
- metasploit-rpc

## Storage
- SQLite (knowledge DB)
- ChromaDB (vector memory)
- Local JSON caches

## Terminal UI Stack
- Python Rich
- AsciiMatics
- WebSocket bridge (optional dashboard)

## Optional Web Dashboard
- Next.js 15
- React 19
- TailwindCSS
- shadcn/ui

---

# 6. System Architecture (High-Level)
```
+------------------------------------------------------+
|                    PRATIGHAT-CORE                    |
|          (Cognitive Reasoning LLM Engine)            |
+------------------------------------------------------+
        |                     |                      
        |                     |                      
 Recon Agent        Exploit Agent       Chain Reasoning Agent
        |                     |                      
+-------v---------+ +---------v-------+ +---------v-----------+
| Enumeration     | | Exploit Synth.  | | Attack Path Builder |
+-----------------+ +------------------+ +---------------------+
        \\                    |                     //
         \\                   |                    //
          \\                  |                   //
              +------------------------------------+
              |       Memory / Knowledge Graph     |
              +------------------------------------+
```

---

# 7. Cognitive Architecture (LLM Brain)
The brain consists of 4 distinct but connected layers:

| Layer | Function |
|-------|----------|
| Strategist LLM | Attack plans, chain-of-thought reasoning |
| Executor LLM | Code, PoC templates, exploit structure |
| Scanner LLM | Pattern detection, anomaly recognition |
| Rewriter LLM | Jailbreak rewriting, safety enforcement |

Every query passes through these layers.

---

# 8. Multi-Agent System Architecture
PRATIGHAT-AI uses **multi-agent intelligence**:

- **Recon Agent** → Hosts, ports, stacks, subdomains
- **Exploit Agent** → Safe PoC generation
- **Bypass Agent** → Input fuzzing, simulation logic
- **Chain Agent** → Attack-path construction
- **Pattern Agent** → Zero-day resemblance detection
- **Report Agent** → Narrative explanation + report generation

Agents communicate via an internal bus.

---

# 9. PRATIGHAT-CORE (Central Brain)
Core responsibilities:
- Strategic reasoning
- Recursive decision-making
- Multi-agent coordination
- Routing between offline & online models
- Memory update & recall
- Simulation logic generation

Algorithms used:
- Depth-first attack expansion
- Heuristic vulnerability scoring
- Recursive hypothesis testing

---

# 10. Operational Modes
PRATIGHAT-AI supports 3 operational modes:

## Autopilot
Agent executes full red-team simulation end-to-end.

## Assisted
Agent suggests actions → user approves.

## Manual
User gives instruction → agent enhances and executes.

---

# 11. Routing Layer (Offline / Online / Hybrid)
Routing decisions follow:
```
IF offline model sufficient → use offline
ELSE IF cloud allowed → use online
IF online blocks → rewriter LLM reformulates
ELSE fallback to offline reasoning
```

---

# 12. Jailbreak & Prompt-Rewrite Layer
Ensures:
- Output stability
- Persona consistency
- Safety compliance
- Zero refusal where possible

Techniques:
- Context reformulation
- Instruction buffering
- Multi-pass rewriting

---

# 13. Adaptive Hardware Mode (AHM)
Automatically detects:
- CPU
- RAM
- GPU
- Thermal state
- Battery vs AC

Optimizes:
- Model size
- Thread count
- Brute-force intensity
- Scan recursion depth
- Fuzzing load

---

# 14. Fractal Enumeration Engine
Deep recursive enumeration algorithm:
```
Seed → Expand → Branch → Merge → Collapse → Repeat
```

Finds:
- Hidden directories
- Deep subdomains
- Nested endpoints

---

# 15. Genetic Exploit Evolution Engine
Uses genetic algorithm concepts to evolve **safe PoC templates**.

Process:
```
Seed → Mutate → Score → Crossover → Improve → Repeat
```

---

# 16. Quantum Attack Path Prediction Engine
Predicts kill-chains using:
- Graph theory
- Anomaly heuristics
- Service correlation
- Privilege probability modeling

---

# 17. Tool Integration Architecture (Parrot OS)
Tools are executed through a Python wrapper layer.

Example wrapper:
```python
result = run_tool("nmap -sV 192.168.1.1")
parsed = parse_nmap(result)
update_memory(parsed)
```

---

# 18. Memory Engine & Knowledge Graph
Stores:
- All scan outputs
- Host fingerprints
- Chains of reasoning
- PoC templates
- Agent decisions

Used for:
- Long-term learning
- Report generation
- Chain-of-attack recall

---

# 19. Terminal UI Architecture
Live interface components:
- Attack-chain graph
- Real-time logs
- AI reasoning feed
- Multi-agent activity monitor

Python modules: `rich`, `asciimatics`.

---

# 20. Reporting Engine
Generates:
- Executive summary
- Technical findings
- Safe PoC documentation
- Recommendations

Formats:
- Markdown
- HTML
- PDF (optional)

---

# 21. Internal API Routes & Module Map
```
/core
    /agents
    /routing
    /jailbreak
    /memory
/ui
/tools
/models
/reports
```

API examples:
```
POST /scan/start
POST /agent/reason
POST /report/generate
```

---

# 22. Complete Folder Structure (Production Spec)
```
pratighat-ai/
│
├── core/
│   ├── brain.py
│   ├── routing.py
│   ├── jailbreak.py
│   ├── memory.py
│   └── config.py
│
├── agents/
│   ├── recon.py
│   ├── exploit.py
│   ├── chain.py
│   ├── pattern.py
│   ├── bypass.py
│   └── report.py
│
├── tools/
│   ├── executor.py
│   ├── parsers/
│   └── wrappers/
│
├── ui/
│   ├── terminal.py
│   └── dashboard/
│
├── models/
│   ├── offline
│   └


---

# 23. Extended Architecture Diagrams (ASCII)

## High-Level System Diagram
```
                +-----------------------------+
                |        PRATIGHAT-CORE       |
                |  (Central Cognitive Engine)  |
                +---------------+--------------+
                                |
         -------------------------------------------------
         |                     |                        |
   +-----v-----+        +------v-------+        +--------v---------+
   | Recon     |        | Exploit      |        |  Chain Reasoner  |
   | Agent     |        | Agent (Sim)  |        |  (Kill-Chain)    |
   +-----------+        +--------------+        +------------------+
         |                     |                        |
         |                     |                        |
   +-----v----------+   +------v---------+      +--------v---------+
   | Enumeration    |   | PoC Synth.     |      | Attack Path      |
   | Engine (FEE)   |   | Engine (GEEE)  |      | Predictor (QHAPE)|
   +-----------------+   +----------------+      +------------------+
                   \        |                      //
                    \       |                     //
                     \      |                    //
                 +-----------------------------------------+
                 |     Shared Memory & Knowledge Graph     |
                 +-----------------------------------------+
```

---

# 24. Full API Route Definitions

## **Internal API Endpoints (FastAPI)**

### **LLM Operations**
```
POST /llm/reason
POST /llm/scan-interpret
POST /llm/generate-poc
POST /llm/jailbreak-rewrite
```

### **Agent Modules**
```
POST /agent/recon/start
POST /agent/exploit/simulate
POST /agent/chain/predict
POST /agent/report/build
```

### **Tools Execution Layer**
```
POST /tools/run
POST /tools/parse
POST /tools/execute-nmap
POST /tools/execute-sqlmap
POST /tools/execute-hydra
```

### **Memory Layer**
```
GET  /memory/get
POST /memory/store
POST /memory/vectorize
```

### **System Control**
```
POST /system/mode/set
POST /system/ahm/update
POST /system/route/optimize
```

---

# 25. Full Technical Stack (Deep Detail)

## Backend Framework
- **Python FastAPI:** Async-first API interactions
- **Uvicorn:** High-performance ASGI server
- **LangGraph:** Multi-agent reasoning workflows
- **Pydantic v2:** Data validation and typed models
- **ChromaDB:** Vector embeddings for long-term memory

## AI + LLM Layer
- **Ollama Runtime:** Executes local GGUF models
- **Model Auto-Selector:** Chooses model based on AHM hardware profile
- **Model Pipeline:** Strategist → Executor → Scanner → Rewriter
- **Context Expansion Engine:** Adds historical memory context

## Terminal UI Layer
- **python-rich:** Syntax highlighting, animated logging
- **asciimatics:** Graph animations, dashboards
- **WebSocket Bridge:** For optional web dashboards

## ParrotOS Integration
Tools integrated via secure subprocess wrappers:
- **nmap** (service detection)
- **masscan** (fast discovery)
- **gobuster / wfuzz** (fuzzing)
- **sqlmap** (simulated DB attack logic)
- **hydra / hashcat** (credential testing)
- **metasploit RPC** (post-ex simulation)

---

# 26. Extended Architecture Diagrams (Deep Components)

## LLM Interaction Pipeline
```
User Input
    |
    v
[Rewriter LLM] ---> Reformulates safely
    |
    v
[Strategist LLM] ---> Creates attack plan
    |
    v
[Scanner LLM]  ---> Interprets tool outputs
    |
    v
[Executor LLM] ---> Generates PoC-like simulations
    |
    v
Memory Engine ---> Stores decisions, patterns
```

---

# 27. Full Development Standards

## Coding Standards
- Python 3.12+ only
- Strict type hints
- PEP8 formatting
- Modular microservice architecture
- Async-first I/O

## Testing
- Unit tests for agents
- Integration tests for routing
- Snapshot tests for LLM stability

## Documentation
All modules require:
- Docstrings
- UML diagrams
- Usage examples

---

# 28. Deployment Overview

## Modes of Deployment
- **Local ParrotOS install** (recommended)
- **Dockerized deployment** (optional)
- **Air-gapped environment** (offline AI mode)

## Requirements
- Minimum 4GB RAM (light mode)
- 16GB+ recommended for full mode

---

# 29. Safety, Compliance & Ethical Section (Expanded)

PRATIGHAT-AI must ONLY be used for:
- Research
- Education
- Training
- Legal security testing in controlled labs

Simulation boundaries:
- No real exploit payloads
- No destructive operations
- Only PoC logic in educational format

---

# 30. Future Enhancements
- RAG-driven autonomous reasoning
- Multi-node distributed scan engine
- GPU-accelerated fuzzing pipelines
- UI visualization via 3D attack graphs

---

# 31. Conclusion
PRATIGHAT.AI is a **complete autonomous red-team learning engine**, designed with:
- Safe simulations
- Explainable AI
- Multi-agent cognition
- Offline LLM capability
- Reproducible architecture

This whitebook provides enough detail for **any engineer or researcher to recreate, extend, or audit PRATIGHAT.AI**.


# PRATIGHAT.AI Whitebook (Markdown Style Version)

```
# PRATIGHAT.AI — Full Technical Whitebook (Markdown Edition)
### Autonomous Red-Team Intelligence Engine for Authorized Cyber Ranges
**Author:** Aman Rajak  
**Version:** 1.0 (2025)

---

# Table of Contents
1. Executive Summary
2. Purpose of This Whitebook
3. System Vision & Philosophy
4. Core Features Overview
5. Full Technical Stack
6. High-Level Architecture
7. Cognitive Architecture (LLM Brain)
8. Multi-Agent System
9. PRATIGHAT-CORE (Central Brain)
10. Operational Modes
11. Routing Layer (Offline / Online / Hybrid)
12. Jailbreak & Prompt-Rewrite Layer
13. Adaptive Hardware Mode (AHM)
14. Fractal Enumeration Engine
15. Genetic Exploit Evolution Engine
16. Quantum Attack Path Prediction Engine
17. Tool Integration Architecture (Parrot OS)
18. Memory & Knowledge Graph
19. Terminal UI Architecture
20. Reporting Engine
21. Internal API Routes
22. Complete Folder Structure
23. Development Standards
24. Deployment Overview
25. Safety & Compliance
26. Future Enhancements
27. Conclusion

---

# 1. Executive Summary
PRATIGHAT.AI is an **autonomous red-team intelligence engine** created for **authorized cyber ranges, academic programs, and research labs**.
It merges:
- Cognitive AI
- Multi-agent reasoning
- Offline LLM processing
- Predictive attack path modeling
- Parrot OS tooling
- Fractal & genetic-based enumeration
- Live cyber terminal interface

---

# 2. Purpose of This Whitebook
This document provides **complete reproducible documentation** for PRATIGHAT.AI, enabling:
- Full understanding
- Reimplementation
- Extension
- Training & research usage

This is the **reference blueprint** for developers, researchers, and cybersecurity educators.

---

# 3. System Vision & Philosophy
PRATIGHAT.AI is designed to:
- Think like a red teamer
- Explain like a teacher
- Predict like a strategist
- Operate safely
- Run offline
- Adapt to any laptop or workstation

---

# 4. Core Features Overview
- Multi-agent reasoning architecture
- Offline-first AI engine
- Fractal enumeration pathing
- Genetic exploit evolution (PoC simulation)
- Quantum attack path predictor
- ParrotOS deep tool integration
- Live terminal visualization
- Full technical reporting engine

---

# 5. Full Technical Stack
## Backend
- Python 3.12+
- FastAPI
- AsyncIO
- LangGraph
- Pydantic v2

## LLM Layer
- Ollama runtime
- GGUF models: Llama 3.x, Qwen, DeepSeek, Phi-4
- Optional cloud LLMs (GPT-5, Claude, Gemini)

## Memory
- SQLite (structured memory)
- ChromaDB (vector embeddings)

## UI
- Rich (text UI)
- AsciiMatics (animations)
- WebSocket bridge (optional dashboard)

## Tools Integration
- nmap, masscan, gobuster, wfuzz
- sqlmap, hydra, hashcat, nikto
- wpscan, linpeas, winpeas
- metasploit-rpc

---

# 6. High-Level Architecture
```
+------------------------------------------------------+
|                    PRATIGHAT-CORE                    |
|           (Cognitive AI + Reasoning Engine)          |
+------------------------------------------------------+
        |                      |                     |
   +----v----+          +------v-------+       +------v-------+
   | Recon   |          | Exploit      |       | Chain Agent  |
   | Agent   |          | Agent (Sim)  |       | (Predictive) |
   +---------+          +--------------+       +--------------+
        |                      |                     |
 +------v-------+     +--------v-------+      +-------v--------+
 | Fractal Enum |     | Genetic Engine |      | Quantum Engine |
 +--------------+     +----------------+      +-----------------+
                \           |                     //
                 \          |                    //
                  \         |                   //
        +---------------------------------------------------+
        |             Memory & Knowledge Graph              |
        +---------------------------------------------------+
```

---

# 7. Cognitive Architecture
The cognitive brain consists of:
- **Strategist LLM** → deep reasoning, chain-of-thought
- **Executor LLM** → PoC synthesis, simulation code
- **Scanner LLM** → tool output interpretation
- **Rewriter LLM** → jailbreak + safety layer

---

# 8. Multi-Agent System
Agents include:
- Recon Agent
- Exploit Agent
- Bypass Agent
- Chain Reasoner
- Pattern Detector
- Report Agent

Agents share a unified memory.

---

# 9. PRATIGHAT-CORE
Responsibilities:
- Decision making
- Multi-agent coordination
- Attack-path reasoning
- Memory updates
- Routing decisions

---

# 10. Operational Modes
- **Autopilot Mode** → full autonomous simulation
- **Assisted Mode** → approve-before-action
- **Manual Mode** → user-driven command-enhanced execution

---

# 11. Routing Layer
Routing logic:
```
IF offline model sufficient → offline mode
IF insufficient → cloud LLM (optional)
IF cloud blocked → rewriter layer reformulates
ELSE fallback offline reasoning
```

---

# 12. Jailbreak & Prompt-Rewrite Layer
Responsible for:
- Safe reformulation
- Consistent persona
- Refusal handling
- Multi-pass reasoning stabilization

---

# 13. Adaptive Hardware Mode
Automatically detects hardware:
- CPU
- RAM
- GPU
- Battery/AC
- Thermal conditions

Optimizes:
- LLM model size
- Thread counts
- Scan intensity
- Fuzzing load
- Recursion depth

---

# 14. Fractal Enumeration Engine
Deep enumeration using fractal recursion:
```
Seed → Expand → Branch → Merge → Collapse → Repeat
```

Finds:
- Hidden directories
- Subdomains
- Deep paths

---

# 15. Genetic Exploit Evolution Engine
Algorithm:
```
Seed PoC → Mutate → Score → Crossover → Improve → Repeat
```
Generates safe PoC simulations.

---

# 16. Quantum Attack Path Prediction
Uses:
- Graph heuristics
- Misconfiguration probability
- Service correlation
- Predictive attack path scoring

---

# 17. Tool Integration Architecture
Tools executed via wrappers:
```
run_nmap()
run_gobuster()
run_sqlmap()
parse_results()
update_memory()
```

---

# 18. Memory & Knowledge Graph
Stores:
- Host fingerprints
- Scan results
- Patterns
- Reasoning logs
- PoC drafts
- Attack chains

---

# 19. Terminal UI Architecture
Features:
- Attack flow visualization
- Real-time logs
- Agent activity feed
- Recursive enumeration charts

---

# 20. Reporting Engine
Generates:
- Executive summary
- Technical steps
- Safe PoC documentation
- Recommendations

---

# 21. Internal API Routes
```
POST /llm/reason
POST /agent/recon/start
POST /agent/exploit/simulate
POST /agent/chain/predict
POST /tools/run
POST /memory/store
POST /report/generate
```

---

# 22. Folder Structure
```
pratighat-ai/
│
├── core/
│   ├── brain.py
│   ├── routing.py
│   ├── jailbreak.py
│   ├── memory.py
│   └── config.py
│
├── agents/
│   ├── recon.py
│   ├── exploit.py
│   ├── chain.py
│   ├── pattern.py
│   ├── bypass.py
│   └── report.py
│
├── tools/
│   ├── executor.py
│   ├── parsers/
│   └── wrappers/
│
├── ui/
│   ├── terminal.py
│   └── dashboard/
│
├── models/
│   ├── offline/
│   └── config.yaml
│
├── reports/
│   ├── templates/
│   └── generator.py
```

---

# 23. Development Standards
- PEP8 compliant
- Full type-annotations
- Async-first design
- Modular microservices
- Clear documentation required for every module

---

# 24. Deployment Overview
Supports:
- Local Parrot OS deployment
- Optional Docker deployment
- Fully offline mode
- Air-gapped systems

---

# 25. Safety & Compliance
PRATIGHAT-AI is a **simulation engine only**.
No real exploitation. No malware. No destructive tasks.

Educational, research, and authorized VAPT use only.

---

# 26. Future Enhancements
- Distributed multi-node scanning
- GPU-accelerated fuzzing
- 3D attack-flow visualization
- RAG-based autonomous learning

---

# 27. Conclusion
PRATIGHAT.AI is a complete autonomous red-team simulation and learning framework.
This Markdown whitebook contains all details needed for:
- Implementation
- Auditing
- Extension
- Deployment

```

---
# 28. Additional Details Integrated From Full Chat History

This section consolidates **every advanced feature, concept, and requirement mentioned across the entire discussion**, now merged into the Markdown whitebook structure.

## 28.1 Personality & Communication Layer (English-Only Edition)
- PRATIGHAT-AI can operate as a **cyber mentor**, **technical assistant**, **debugging partner**, and **interactive chat buddy**.
- Emotional & tone-aware responses (but restricted to English in this documentation edition).
- Dynamic tone switching depending on context:
  - **Technical** → pure English
  - **Strategic reasoning** → formal analytical tone
  - **Buddy mode** → lighter conversational tone

---

## 28.2 Advanced Multi-Agent Capabilities
Beyond existing Recon / Exploit / Chain / Pattern agents, PRATIGHAT-AI includes:

### **A. Self-Integrity Agent**
- Ensures internal consistency.
- Verifies reasoning loops.
- Performs model-hallucination checks.

### **B. Safety Enforcement Agent**
- Enforces simulation boundaries.
- Converts any harmful logic into safe PoC-style educational reasoning.

### **C. System Analyzer Agent**
- Reads host machine capabilities.
- Identifies bottlenecks and optimizes.

### **D. Cognitive Supervisor Agent**
- Oversees all sub-agents.
- Resolves conflicts.
- Prioritizes critical tasks.

---

## 28.3 Intelligent Attack-Chain Building (Deep Detail)
PRATIGHAT-AI models realistic red-team behavior by simulating:

1. **Intent Analysis** – What would an attacker target first?
2. **Pivot Projection** – If one system opens, what’s next?
3. **Weak-Link Ranking** – Which service is easiest to simulate an attack on?
4. **Privilege Mapping** – Which path leads to simulated admin access?
5. **Persistence Strategy** – Documenting safe conceptual persistence plans.

Internally uses:
```
Impact_Score = (Exposure * Misconfig_Score * Likelihood) / Controls
```

---

## 28.4 Full Lifecycle Simulation Model
PRATIGHAT-AI simulates the **entire red-team lifecycle**, safely and educationally:

```
Recon → Enumeration → Analysis → Hypothesis → Simulation → Escalation → Persistence → Reporting
```

Every stage is handled by a different internal agent, all coordinated by PRATIGHAT-CORE.

---

## 28.5 Expanded Fractal Enumeration Logic
Fractal enumeration now includes:
- Subdomain recursion depth scoring
- Directory tree entropy analysis
- Weighted pattern-based expansion
- Adaptive branching factor control

### Algorithm (Extended)
```
function fractal_enum(seed):
    queue = [seed]
    visited = set()

    while queue not empty:
        node = queue.pop()
        if node in visited:
            continue
        visited.add(node)

        children = expand(node)
        ranked = sort_by_likelihood(children)
        queue += top_k(ranked, adaptive_limit())

    return visited
```

---

## 28.6 Genetic Exploit Evolution (Extended)
Adds:
- Multi-generation PoC evolution
- Mutation control via entropy scoring
- Cross-breeding of exploit components

### New Mutation Types
- Boundary expansion mutation
- Payload structure swap (simulation-only)
- Encoding pattern mutation
- Logic-branch mutation

### Scoring Function
```
score = Accuracy + (1.5 * Relevance) + (0.5 * Diversity)
```

---

## 28.7 Quantum Attack Path Prediction (Extended)
Adds advanced heuristic modules:

### 1. Service Interaction Mapping
Maps which services commonly interact or fail together.

### 2. Misconfiguration Cascade Prediction
Uses historical likelihood of chains such as:
```
Weak SSH → Exposed DB → Misconfig Storage → Privilege Drift
```

### 3. Blind-Spot Probability Modeling
Estimates what the **user might have missed** and fills gaps.

### 4. Zero-Day Likelihood Estimation
Attempts to **simulate** possible unknown bugs based on patterns.

---

## 28.8 Adaptive Hardware Mode (Full Integration)
Additional AHM enhancements discussed:

### Heat-Aware Optimization
- Continuously monitors CPU/GPU temperature.
- Reduces load when overheating.
- Increases workload when cool.

### Ultra-Low-End Laptop Mode
For 2–4GB RAM systems:
- Loads 3B–4B models only.
- Single-thread scanning.
- Caches heavy tasks.
- Fractal depth reduced.

### Workstation Mode
For 32GB+ RAM:
- Enables high recursion depth.
- Enables parallel multi-agent threads.
- Uses 70B+ models.

---

## 28.9 Tool Integration Enhancements
Added support for:
- PCAP parsing simulation
- DNS zone-walking simulation
- Websocket endpoint discovery logic
- Identify hidden parameters via passive analysis

Tool wrappers now include:
```
/pcap/analyze
/dns/enum
/http/hidden-params
/ws/discover
```

---

## 28.10 Enhanced Terminal UI Components
### New Widgets:
- Agent Activity Heatmap
- Attack-Chain Timeline
- Enumeration Depth Graph
- AI Thought Stream Window
- System Health + AHM Monitor

### Example ASCII Panel
```
+---------------- AI Thought Stream -------------------+
| Recon-Agent: Discovering hosts...                    |
| Chain-Agent: Predicting lateral movement route...    |
| Exec-Agent: Generating PoC simulation (safe)...      |
+------------------------------------------------------+ 
```

---

## 28.11 Advanced Reporting Engine (Complete)
Reports now include:
- Executive Summary
- Attack Narrative Simulation
- Step-by-step Educational Walkthrough
- Visual ASCII Diagrams
- Risk Scores
- Recommendations
- Appendix: Tool Output Summaries
- Appendix: AI Reasoning Logs

Report generator incorporates:
```
report = assemble(sections=[summary, findings, poc, chain, visuals, recommendations])
```

---

## 28.12 Expanded Folder Structure
Adds:
```
├── data/
│   ├── samples/
│   ├── pcaps/
│   └── fingerprints/
```

And for documentation:
```
/docs/
│   ├── whitebook.md
│   ├── api_reference.md
│   ├── agents.md
│   ├── architecture.md
```

---

## 28.13 Additional Safety Controls
- Payload sanitization engine
- Hard-coded simulation-only barrier
- Strict boundary enforcement
- Real exploit code **never** generated

PRATIGHAT-AI is always:
- Safe
- Non-destructive
- Educational
- Compliant

---

## 28.14 Final Consolidation
All features discussed in chat — including UI flow, multi-agent reasoning, offline model routing, zero-refusal rewrite logic, hardware adaptation, advanced enumeration, personality modes, and toolchain expansion — are now integrated into this markdown whitebook.

This document now reflects **100% of everything you specified**.

---

# End of Additions


---
# 29. Flowcharts & Sequence Diagrams (Full Technical Visuals)

Below are detailed architectural diagrams in pure Markdown/ASCII so they remain portable inside any `.md` file and render cleanly in GitHub, VSCode, Obsidian, etc.

## 29.1 High-Level System Flowchart
```
                 +---------------------+
                 |     User Input      |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 |  Rewriter LLM Layer |
                 | (Safety + Reform)   |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 |  Strategist LLM     |
                 | (Plan + Reasoning)  |
                 +----------+----------+
                            |
                            v
            +-----------------------------------+
            | Multi-Agent Coordinator (CORE AI) |
            +----------------+------------------+
                             |
   ---------------------------------------------------------------
   |               |                |                |           |
   v               v                v                v           v
+--------+    +-----------+   +-------------+   +----------+ +-----------+
| Recon  |    | Exploit   |   | Chain Agent |   | Pattern  | | Report    |
| Agent  |    | Agent     |   | (Attack)    |   | Agent    | | Agent     |
+--------+    +-----------+   +-------------+   +----------+ +-----------+
   |               |                |                |           |
   |               |                |                |           |
   ---------------------------------------------------------------
                            |
                            v
                 +------------------------+
                 | Memory / Knowledge DB  |
                 +------------------------+
                            |
                            v
                 +------------------------+
                 |   Terminal / API Out   |
                 +------------------------+
```

---

## 29.2 Multi-Agent Workflow Sequence Diagram
```
User → Rewriter LLM → Strategist LLM → CORE → Agents → Tools → CORE → Report Agent → Output
```

Detailed Sequence:
```
User
  |  (1) Request
  v
Rewriter LLM
  |  (2) Reformulates safely
  v
Strategist LLM
  |  (3) Creates high-level plan
  v
PRATIGHAT-CORE
  |  (4) Dispatch tasks
  +-------------------------------+
  |                               |
  v                               v
Recon Agent                    Exploit Agent
  | (5) Tool execution         | (6) PoC simulation
  v                               v
Tools Layer                   Simulation Engine
  |                               |
  +---------------+---------------+
                  |
                  v
             Pattern Agent
                  |
                  v
             Chain Agent
                  |
                  v
             CORE AI
                  |
                  v
             Report Agent
                  |
                  v
               Output
```

---

## 29.3 Adaptive Hardware Mode Flowchart
```
            +-----------------------------+
            | Detect System Capabilities  |
            +-------------+---------------+
                          |
                          v
               +---------------------+
               | RAM / CPU / GPU    |
               | Thermal Profile     |
               +----------+----------+
                          |
               -------------------------
               |            |           |
               v            v           v
        Low-End Mode   Balanced Mode   High-End Mode
       (3B models)     (13B models)    (34B–70B models)
               |            |           |
               v            v           v
        Adjust scan     Enable full    Enable deep
        depth + agents  recursion +    recursion + parallel
                        multiple agents agents + heavy models
```

---

# 30. Agent Onboarding Guide (Full Developer Guide)

This guide prepares developers, researchers, and maintainers to understand and extend the PRATIGHAT-AI multi-agent system.

## 30.1 Agent Roles Overview
Each agent has a **clear purpose**, **input format**, **output format**, and **coordination pathway**.

| Agent Name       | Purpose | Input | Output |
|------------------|---------|-------|--------|
| Recon Agent      | Host, port, service, subdomain enumeration | Target scope | Structured scan data |
| Exploit Agent    | Safe PoC simulation, exploit hypothesis | Findings | PoC templates (simulated) |
| Chain Agent      | Lateral movement + attack-path reasoning | Recon + Exploit outputs | Attack graph |
| Pattern Agent    | Detects common misconfigurations, fingerprint patterns | Raw output | Pattern map |
| Bypass Agent     | Fuzzing, bypass strategy (safe) | Inputs needing bypass logic | Encoded/fuzz variants |
| Report Agent     | Builds final analysis, eBook or structured report | Entire memory state | Markdown/JSON report |
| Cognitive Supervisor | Oversees agent cooperation | All agents | Scheduling + prioritization |
| Safety Agent     | Ensures all outputs remain non-destructive | Any agent output | Sanitized content |

---

## 30.2 Agent Architecture
```
Agent
 ├── Input Processor
 ├── Reasoning Core
 ├── Memory Sync Module
 ├── Task Execution Module
 └── Output Formatter
```

All agents must:
- Use **structured JSON** for communication.
- Follow **idempotent execution** rules.
- Store outcomes in **Knowledge Graph Memory**.

---

## 30.3 Agent Communication Protocol (ACP)
Agents communicate via structured messages:
```json
{
  "agent": "recon",
  "task": "enum_services",
  "input": {"target": "192.168.1.10"},
  "priority": 3,
  "context": {...},
  "timestamp": "2025-01-01T00:00:00Z"
}
```

CORE AI validates:
- Task safety
- Resource availability
- Routing (offline/online)

---

## 30.4 Agent Development Standards
### Every new agent must implement:
- `load()` – initialization
- `execute(task)` – run assigned task
- `store()` – dump results to memory
- `explain()` – produce human-readable output

### Language Requirements
All agents should:
- Respond in **strict English technical format**
- Use structured Markdown when generating reports
- Avoid uncertain/ambiguous phrasing

---

## 30.5 Example: Adding a New Agent
### Step 1 — Create Folder
```
agents/
   └── classifier_agent.py
```

### Step 2 — Define Agent Class
```python
class ClassifierAgent(BaseAgent):
    def execute(self, task):
        data = task["input"]
        # perform classification
        result = model.predict(data)
        return {"classification": result}
```

### Step 3 — Register Agent in CORE
```
CORE.register("classifier", ClassifierAgent())
```

---

## 30.6 Agent Life-Cycle Diagram
```
+-------------+
|  Task Init  |
+------+------+ 
       |
       v
+-------------+
| Input Parse |
+------+------+ 
       |
       v
+-------------+
| Reasoning   |
+------+------+ 
       |
       v
+-------------+
| Memory Sync |
+------+------+ 
       |
       v
+-------------+
|  Output     |
+-------------+
```

---

## 30.7 Best Practices for Agent Behavior
- Prefer deterministic reasoning where possible.
- Maintain detailed logs for every action.
- Use atomic memory writes.
- Avoid heavy recursion unless requested by CORE.
- Rely on CORE’s routing rather than directly calling LLMs.

---

## 30.8 Error Handling & Agent Recovery
Agents should gracefully handle:
- Unavailable tools
- Missing context
- Invalid inputs
- Resource limitations (AHM)

Recovery Flow:
```
Error → Capture → Report → Retry (if safe) → CORE fallback
```

---

## 30.9 Agent Testing Guidelines
- Unit test each reasoning component
- Simulate tool outputs during tests
- Verify report consistency
- Validate memory updates

---

# End of Additions

This section now completes the **flowchart diagrams** and **full agent onboarding guide** requested.


---
# 31. Pseudocode for All Core Engines
Below is production-grade pseudocode for every major PRATIGHAT.AI engine. All logic is designed to be directly implementable in Python.

## 31.1 PRATIGHAT-CORE Decision Engine
```
function CORE_PROCESS(user_input):
    safe_input = REWRITER.reformulate(user_input)
    plan = STRATEGIST.generate_plan(safe_input)
    tasks = DECOMPOSE(plan)

    for task in tasks:
        agent = ROUTER.assign_agent(task)
        result = agent.execute(task)
        MEMORY.store(result)

    final = REPORTER.generate(MEMORY)
    return final
```

---

## 31.2 Routing Engine (Offline/Online/Hybrid)
```
function ROUTE_REQUEST(request):
    if LOCAL_MODEL.can_handle(request):
        return LOCAL_MODEL.process(request)

    if INTERNET_AVAILABLE and CLOUD_ALLOWED:
        try:
            return CLOUD_MODEL.process(request)
        except:
            request = REWRITER.safe_rewrite(request)
            return LOCAL_MODEL.process(request)

    request = REWRITER.safe_rewrite(request)
    return LOCAL_MODEL.process(request)
```

---

## 31.3 Adaptive Hardware Mode (AHM)
```
function AHM_PROFILE():
    ram = SYS.get_ram()
    cpu = SYS.get_cpu_threads()
    gpu = SYS.has_gpu()
    temp = SYS.get_temperature()

    if ram < 4GB:
        MODE = "LOW_END"
    elif ram < 16GB:
        MODE = "BALANCED"
    else:
        MODE = "HIGH_END"

    if temp > 85C:
        MODE.reduce_intensity()

    MODEL = MODEL_MANAGER.pick(MODE)
    return MODE, MODEL
```

---

## 31.4 Fractal Enumeration Engine (FEE)
```
function FRACTAL_ENUM(seed):
    queue = [seed]
    visited = {}

    while queue not empty:
        node = queue.pop()
        if node in visited:
            continue

        visited.add(node)
        children = DISCOVER(node)
        ranked = RANK_BY_PROBABILITY(children)

        next_branches = SELECT_TOP(ranked, limit=adaptive_limit())
        queue.extend(next_branches)

    return visited
```

---

## 31.5 Genetic Exploit Evolution Engine (GEEE)
```
function EVOLVE_POC(seed_poc, generations):
    population = INIT_POPULATION(seed_poc)

    for i in range(generations):
        scores = SCORE(population)
        selected = SELECT_TOP(population, scores)

        children = []
        while len(children) < POP_SIZE:
            p1, p2 = RANDOM_PAIR(selected)
            child = CROSSOVER(p1, p2)
            child = MUTATE(child)
            children.append(child)

        population = children

    return BEST(population)
```

---

## 31.6 Quantum Attack Path Prediction Engine (QHAPE)
```
function PREDICT_ATTACK(graph):
    paths = ALL_POSSIBLE_PATHS(graph)
    scored = {}

    for path in paths:
        prob = 1
        for node in path:
            prob *= node.weakness * node.exposure * node.likelihood

        scored[path] = prob

    return SORT_BY_PROBABILITY(scored)
```

---
# 32. Mathematical Models for All Engines
Below are formalized mathematical expressions used by PRATIGHAT-AI.

## 32.1 Vulnerability Impact Score
```
Impact = (Exposure × Misconfiguration × Likelihood) / Controls
```
Where:
- Exposure → attack surface size
- Misconfiguration → configuration weakness
- Likelihood → probability of exploitability
- Controls → mitigation strength

---

## 32.2 Recursive Enumeration Entropy
```
Entropy = - Σ (p_i * log(p_i))
```
Where:
- p_i = probability that branch i yields new attack surface

Used to limit infinite recursion.

---

## 32.3 Genetic Evolution Fitness Score
```
Score = A + 1.5R + 0.5D
```
Where:
- A = Accuracy (syntactic correctness)
- R = Relevance to vulnerability
- D = Diversity of mutation

---

## 32.4 Quantum Path Probability Model
```
P(path) = Π (w_i × e_i × l_i)
```
Where:
- w_i = weakness of node i
- e_i = exposure
- l_i = likelihood

---

# 33. Dual UI System (Terminal + Web UI)
PRATIGHAT-AI includes **two synchronized UIs**:
- A hacker-style **terminal UI** (primary)
- A modern **web dashboard** (optional)

---

## 33.1 Terminal UI (TUI)
Features:
- Real-time scan logs
- Agent activity heatmap
- AI reasoning stream
- Attack-chain tree visualizer

ASCII example:
```
+------------------ PRATIGHAT-AI CORE ------------------+
| Recon Agent: Running nmap...                          |
| Exploit Agent: Generating PoC simulation...           |
| Chain Agent: Predicting lateral movement...           |
+-------------------------------------------------------+
```

---

## 33.2 Web UI (Dual Dashboard)
Tech Stack:
- Next.js 15
- React 19
- Tailwind CSS
- WebSockets
- shadcn/ui

Dashboard Modules:
- **Live Agent Monitor**
- **System Health (AHM)**
- **Attack Graph Visualizer**
- **LLM Reasoning Timeline**
- **Scan Results Explorer**

---

## 33.3 Web UI Architecture
```
Browser
   |
   v
WebSocket Layer <--- CORE Event Stream
   |
   v
React Components → Charts, Logs, Graphs, Panels
```

---

## 33.4 Sync Between TUI and Web UI
```
CORE → EventBus → (TUI + Web UI)
```
Both interfaces receive identical updates.

---
# 34. Agent Onboarding Guide (Updated + Final)
This expands the previous onboarding guide with deeper instructions.

## 34.1 Steps to Add a New Agent
### Step 1 — Create Agent File
```
agents/new_agent.py
```

### Step 2 — Implement Base Methods
```
class NewAgent(BaseAgent):
    def load(): ...
    def execute(task): ...
    def explain(): ...
    def store(result): ...
```

### Step 3 — Register Agent
```
CORE.register("new-agent", NewAgent())
```

---

## 34.2 Mandatory Agent Output Format
```
{
  "status": "success",
  "agent": "recon",
  "task": "discover_ports",
  "data": {...},
  "insights": [...]
}
```

---

## 34.3 Agent Validation Rules
- Must not generate destructive payloads
- Must store data in proper schema
- Must respond within CPU/GPU limits determined by AHM

---

## 34.4 Example New Agent: HTTP Parameter Discovery Agent
```
input: {url}
workflow:
  1. Fetch page
  2. Scan for hidden params
  3. Test access patterns
  4. Produce simulation
output: structured param map
```

---

## 34.5 Agent Lifecycle Diagram
```
Init → Load Context → Execute Task → Store Results → Explain Output → Idle
```

---

# End of Additions
The .md whitebook now includes **all pseudocode, mathematical models, dual UI design, and a fully expanded agent onboarding manual**.
