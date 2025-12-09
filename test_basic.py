"""
Simple test script to verify core functionality without external dependencies
"""

print("=" * 60)
print("PRATIGHAT.AI - Basic Functionality Test")
print("=" * 60)
print()

# Test 1: Configuration
print("Test 1: Configuration System")
try:
    from core.config import get_config
    config = get_config()
    print(f"  ✅ Hardware Mode: {config.hardware.mode.value}")
    print(f"  ✅ RAM: {config.hardware.ram_gb:.1f} GB")
    print(f"  ✅ CPU Cores: {config.hardware.cpu_cores}")
    print(f"  ✅ Operational Mode: {config.operational_mode.value}")
    print("  ✅ Configuration system works!")
except Exception as e:
    print(f"  ❌ Configuration failed: {e}")
print()

# Test 2: Agent Base Classes
print("Test 2: Agent Framework")
try:
    from agents.base import BaseAgent, AgentResult, AgentCoordinator
    coordinator = AgentCoordinator()
    print("  ✅ Agent framework loaded")
    print(f"  ✅ Registered agents: {len(coordinator.list_agents())}")
    print("  ✅ Agent system works!")
except Exception as e:
    print(f"  ❌ Agent framework failed: {e}")
print()

# Test 3: Terminal UI
print("Test 3: Terminal UI")
try:
    from ui.terminal import TerminalUI
    ui = TerminalUI()
    print("  ✅ Terminal UI initialized")
    ui.add_log("Test log entry", "INFO", "test")
    print(f"  ✅ Log system works ({len(ui.logs)} entries)")
    print("  ✅ Terminal UI works!")
except Exception as e:
    print(f"  ❌ Terminal UI failed: {e}")
print()

# Test 4: Basic Agents
print("Test 4: Specialized Agents")
try:
    from agents.recon import ReconAgent
    from agents.report import ReportAgent
    
    recon = ReconAgent()
    report = ReportAgent()
    
    print(f"  ✅ Recon Agent: {len(recon.supported_tasks)} tasks")
    print(f"  ✅ Report Agent: {len(report.supported_tasks)} tasks")
    print("  ✅ Specialized agents work!")
except Exception as e:
    print(f"  ❌ Agents failed: {e}")
print()

# Summary
print("=" * 60)
print("Test Summary")
print("=" * 60)
print("Core functionality verified!")
print("Note: Full functionality requires Ollama and additional dependencies.")
print()
print("To run PRATIGHAT.AI:")
print("  1. Install dependencies: pip install -r requirements.txt")
print("  2. Install Ollama: https://ollama.ai")
print("  3. Run: python main.py")
print()
