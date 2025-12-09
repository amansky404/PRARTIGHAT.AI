# PRATIGHAT.AI Installation Guide

## Prerequisites

- Python 3.12 or higher
- Ollama (for local LLM models)
- 4GB+ RAM (16GB+ recommended)
- Linux (Parrot OS recommended) or compatible system

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or using the project configuration:

```bash
pip install -e .
```

### 2. Install Ollama

Visit [Ollama.ai](https://ollama.ai) and follow installation instructions for your OS.

For Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Pull Required Models

Based on your hardware configuration:

**For Low-End Systems (4GB RAM):**
```bash
ollama pull llama3.2:3b
ollama pull qwen2.5:3b
ollama pull phi3.5:3.8b
```

**For Balanced Systems (4-16GB RAM):**
```bash
ollama pull llama3.1:8b
ollama pull qwen2.5:14b
```

**For High-End Systems (16GB+ RAM):**
```bash
ollama pull llama3.1:70b
ollama pull qwen2.5:32b
ollama pull deepseek-r1:32b
```

### 4. Configuration

Create a `config.yaml` file (optional):

```yaml
operational_mode: assisted
sqlite_path: pratighat.db
chroma_path: chroma_db
api_host: 127.0.0.1
api_port: 8000
tool_timeout: 300
max_recursion_depth: 5
safe_mode: true
simulation_only: true
log_level: INFO
log_file: pratighat.log
```

## Running PRATIGHAT.AI

### Interactive Mode (Default)

```bash
python main.py
```

Or with the installed command:

```bash
pratighat --interactive
```

### API Server Mode

```bash
python main.py --api
```

Or:

```bash
pratighat --api --host 0.0.0.0 --port 8000
```

### With Custom Configuration

```bash
python main.py --config /path/to/config.yaml
```

### Set Operational Mode

```bash
python main.py --mode assisted    # Requires user approval
python main.py --mode autopilot   # Fully autonomous
python main.py --mode manual      # User-driven
```

## Usage Examples

Once in interactive mode:

```
PRATIGHAT> help
PRATIGHAT> status
PRATIGHAT> Explain how SQL injection works for educational purposes
PRATIGHAT> What are the common web vulnerabilities in OWASP Top 10?
```

## Directory Structure

```
pratighat-ai/
├── core/              # Core cognitive engine
├── agents/            # Specialized agents
├── tools/             # Tool integration
├── ui/                # Terminal UI
├── models/            # Model configurations
├── reports/           # Report templates
├── data/              # Sample data
├── docs/              # Documentation
├── main.py            # Entry point
└── requirements.txt   # Dependencies
```

## Safety & Compliance

⚠️ **IMPORTANT**: PRATIGHAT.AI is designed for:
- Educational purposes
- Authorized security research
- Controlled lab environments
- Academic training

**DO NOT** use for:
- Unauthorized testing
- Real attacks
- Malicious purposes
- Illegal activities

All outputs are simulations for learning purposes only.

## Troubleshooting

### Ollama Connection Issues

Ensure Ollama is running:
```bash
ollama serve
```

### Memory Issues

Reduce model size in config or let Adaptive Hardware Mode (AHM) optimize automatically.

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Support

For issues and questions, please refer to the README.md whitebook or create an issue in the repository.

## License

Educational and research use only. See README.md for full terms.
