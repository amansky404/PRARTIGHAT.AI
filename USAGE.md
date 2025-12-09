# PRATIGHAT.AI Usage Guide

## Quick Start

### 1. Start PRATIGHAT.AI

```bash
python main.py
```

or

```bash
python main.py --interactive
```

### 2. Using the Interactive Interface

Once started, you'll see the PRATIGHAT.AI banner and system information.

## Available Commands

### System Commands

- `help` - Show help message with all available commands
- `status` - Display current system status and configuration
- `config` - Show configuration details
- `agents` - Show registered agent status
- `logs` - Display recent activity logs
- `clear` - Clear the terminal screen
- `exit`, `quit`, or `q` - Exit PRATIGHAT.AI

### Agent Commands

#### Reconnaissance

```
recon <target>
```

Example:
```
PRATIGHAT> recon example.com
```

This will perform educational reconnaissance analysis on the specified target.

#### Report Generation

```
report
```

Generates a sample executive summary report.

### Query Processing

Simply type your cybersecurity-related query, and PRATIGHAT-CORE will process it:

```
PRATIGHAT> Explain SQL injection for educational purposes
PRATIGHAT> What are the OWASP Top 10 vulnerabilities?
PRATIGHAT> How does XSS work and how to prevent it?
PRATIGHAT> Explain buffer overflow attacks conceptually
```

## Example Session

```
PRATIGHAT> help
[Shows help menu]

PRATIGHAT> status
[Shows system configuration and hardware mode]

PRATIGHAT> recon google.com
[Performs educational reconnaissance analysis]

PRATIGHAT> What is Cross-Site Scripting?
[PRATIGHAT-CORE provides detailed explanation]

PRATIGHAT> report
[Generates sample security report]

PRATIGHAT> exit
[Shuts down PRATIGHAT.AI]
```

## Advanced Usage

### Custom Configuration

Create a `config.yaml` file:

```yaml
operational_mode: assisted
safe_mode: true
simulation_only: true
log_level: INFO
```

Run with custom config:

```bash
python main.py --config config.yaml
```

### Operational Modes

PRATIGHAT.AI supports three operational modes:

1. **Assisted Mode** (Default) - Requires user approval for actions
2. **Autopilot Mode** - Fully autonomous (educational simulation)
3. **Manual Mode** - User-driven with AI enhancement

Set mode via command line:

```bash
python main.py --mode assisted
python main.py --mode autopilot
python main.py --mode manual
```

### Agent Workflow

PRATIGHAT.AI uses specialized agents for different tasks:

- **Recon Agent** - Reconnaissance and enumeration planning
- **Exploit Agent** - Safe PoC generation (coming soon)
- **Chain Agent** - Attack path prediction (coming soon)
- **Pattern Agent** - Pattern detection (coming soon)
- **Bypass Agent** - Fuzzing simulation (coming soon)
- **Report Agent** - Report generation

## Safety Features

PRATIGHAT.AI includes multiple safety layers:

1. **Prompt Rewriting** - All queries are rewritten for safety
2. **Simulation Mode** - All outputs are educational simulations
3. **Safety Enforcement** - Harmful intent detection
4. **Compliance Checks** - Ensures authorized use only

## Educational Features

### Learning Mode

Ask educational questions about:

- Web vulnerabilities (SQL injection, XSS, CSRF, etc.)
- Network security concepts
- Cryptography basics
- Security best practices
- Penetration testing methodologies
- OWASP guidelines
- Secure coding practices

### Example Educational Queries

```
PRATIGHAT> Explain how to detect SQL injection vulnerabilities
PRATIGHAT> What are the phases of penetration testing?
PRATIGHAT> How does TLS/SSL work?
PRATIGHAT> What is the difference between symmetric and asymmetric encryption?
PRATIGHAT> Explain the CIA triad in cybersecurity
```

## Adaptive Hardware Mode

PRATIGHAT.AI automatically detects your hardware and optimizes:

- **Low-End Mode** (2-4GB RAM) - Uses lightweight 3B models
- **Balanced Mode** (4-16GB RAM) - Uses medium 8-14B models
- **High-End Mode** (16GB+ RAM) - Uses powerful 32B-70B models

## Memory & Context

PRATIGHAT.AI maintains memory of your session:

- All queries and responses are stored
- Context is maintained across conversations
- Agent activities are logged
- Results can be retrieved for reporting

## Troubleshooting

### Ollama Not Connected

Ensure Ollama is running:

```bash
ollama serve
```

Pull required models:

```bash
ollama pull llama3.1:8b
```

### Memory Issues

The system will automatically adapt to your hardware. For low-memory systems:

- Smaller models are automatically selected
- Recursion depth is reduced
- Processing is optimized

### Import Errors

Install all dependencies:

```bash
pip install -r requirements.txt
```

## Best Practices

1. **Always use for educational purposes** - PRATIGHAT.AI is designed for learning
2. **Authorized testing only** - Only use on systems you own or have permission to test
3. **Review outputs carefully** - AI-generated content should be verified
4. **Keep models updated** - Regularly update Ollama models
5. **Monitor system resources** - Watch RAM and CPU usage

## Getting Help

Within PRATIGHAT.AI:

```
PRATIGHAT> help
```

For detailed documentation, see:

- `README.md` - Complete technical whitebook
- `INSTALL.md` - Installation instructions
- `USAGE.md` - This file

## Disclaimer

⚠️ **IMPORTANT**: PRATIGHAT.AI is an educational tool for:

- Learning cybersecurity concepts
- Authorized security research
- Academic training
- Controlled lab environments

**DO NOT** use for:

- Unauthorized testing
- Real attacks
- Malicious purposes
- Illegal activities

All outputs are simulations for educational purposes only.

---

Made in India 🇮🇳 | PRATIGHAT.AI v1.0.0
