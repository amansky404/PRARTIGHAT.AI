"""
PRATIGHAT.AI Terminal UI

Rich-based terminal interface for PRATIGHAT-AI system.
"""

from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime


class TerminalUI:
    """
    Terminal UI for PRATIGHAT-AI
    
    Provides:
    - Live status display
    - Agent activity monitoring
    - Scan results visualization
    - Log streaming
    """
    
    def __init__(self):
        self.console = Console()
        self.logs: List[Dict[str, Any]] = []
        self.agent_status: Dict[str, str] = {}
    
    def print_banner(self):
        """Print PRATIGHAT.AI banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ██████╗  █████╗ ████████╗██╗ ██████╗ ██╗  ██╗     ║
║   ██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║██╔════╝ ██║  ██║     ║
║   ██████╔╝██████╔╝███████║   ██║   ██║██║  ███╗███████║     ║
║   ██╔═══╝ ██╔══██╗██╔══██║   ██║   ██║██║   ██║██╔══██║     ║
║   ██║     ██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║  ██║     ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═╝     ║
║                         .AI                                   ║
║                                                               ║
║   Indigenous AI-Powered Penetration Testing Platform         ║
║   Autonomous Red-Team Intelligence Engine                    ║
║   For Authorized Cyber Ranges & Security Research            ║
║                                                               ║
║   Version 1.0.0 | Made in India 🇮🇳                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        
        self.console.print(banner, style="bold cyan")
        self.console.print()
    
    def print_system_info(self, config):
        """Print system information"""
        hw = config.hardware
        
        info_text = f"""
[bold]System Configuration:[/bold]
  • Hardware Mode: [cyan]{hw.mode.value.upper()}[/cyan]
  • RAM: [cyan]{hw.ram_gb:.1f} GB[/cyan]
  • CPU Cores: [cyan]{hw.cpu_cores}[/cyan]
  • GPU Available: [cyan]{'Yes' if hw.has_gpu else 'No'}[/cyan]
  • Temperature: [cyan]{hw.temperature:.1f}°C[/cyan]
  • Operational Mode: [cyan]{config.operational_mode.value.upper()}[/cyan]

[bold]Safety:[/bold]
  • Safe Mode: [{'green' if config.safe_mode else 'red'}]{'ENABLED' if config.safe_mode else 'DISABLED'}[/{'green' if config.safe_mode else 'red'}]
  • Simulation Only: [{'green' if config.simulation_only else 'red'}]{'ENABLED' if config.simulation_only else 'DISABLED'}[/{'green' if config.simulation_only else 'red'}]
"""
        
        self.console.print(Panel(info_text, title="[bold]PRATIGHAT-CORE Status[/bold]", 
                                border_style="green"))
        self.console.print()
    
    def add_log(self, message: str, level: str = "INFO", agent: str = "system"):
        """Add log entry"""
        self.logs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "agent": agent,
            "message": message
        })
    
    def print_logs(self, limit: int = 10):
        """Print recent logs"""
        recent_logs = self.logs[-limit:]
        
        table = Table(title="Recent Activity")
        table.add_column("Time", style="dim")
        table.add_column("Agent", style="cyan")
        table.add_column("Level", style="yellow")
        table.add_column("Message")
        
        for log in recent_logs:
            timestamp = log["timestamp"].split("T")[1].split(".")[0]
            level_style = {
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "DEBUG": "dim"
            }.get(log["level"], "white")
            
            table.add_row(
                timestamp,
                log["agent"],
                f"[{level_style}]{log['level']}[/{level_style}]",
                log["message"]
            )
        
        self.console.print(table)
        self.console.print()
    
    def print_agent_status(self, agents: Dict[str, str]):
        """Print agent status"""
        table = Table(title="Agent Status")
        table.add_column("Agent", style="cyan")
        table.add_column("Status")
        
        for agent, status in agents.items():
            status_style = {
                "active": "green",
                "idle": "yellow",
                "busy": "blue",
                "error": "red"
            }.get(status.lower(), "white")
            
            table.add_row(
                agent.upper(),
                f"[{status_style}]{status.upper()}[/{status_style}]"
            )
        
        self.console.print(table)
        self.console.print()
    
    def print_result(self, result: Any, title: str = "Result"):
        """Print result in a panel"""
        if hasattr(result, 'to_dict'):
            result_dict = result.to_dict()
            result_text = self._format_dict(result_dict)
        elif isinstance(result, dict):
            result_text = self._format_dict(result)
        else:
            result_text = str(result)
        
        self.console.print(Panel(result_text, title=f"[bold]{title}[/bold]",
                                border_style="green"))
        self.console.print()
    
    def _format_dict(self, d: Dict[str, Any], indent: int = 0) -> str:
        """Format dictionary for display"""
        lines = []
        prefix = "  " * indent
        
        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}[cyan]{key}:[/cyan]")
                lines.append(self._format_dict(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}[cyan]{key}:[/cyan]")
                for item in value:
                    if isinstance(item, dict):
                        lines.append(self._format_dict(item, indent + 1))
                    else:
                        lines.append(f"{prefix}  • {item}")
            else:
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 200:
                    value_str = value_str[:200] + "..."
                lines.append(f"{prefix}[cyan]{key}:[/cyan] {value_str}")
        
        return "\n".join(lines)
    
    def show_help(self):
        """Show help message"""
        help_text = """
[bold]Available Commands:[/bold]
  • help          - Show this help message
  • status        - Show system status
  • config        - Show configuration
  • agents        - Show agent status
  • logs          - Show recent logs
  • clear         - Clear screen
  • exit/quit/q   - Exit PRATIGHAT.AI

[bold]Agent Commands:[/bold]
  • recon <target>              - Run reconnaissance on target
  • report                      - Generate report
  
[bold]Usage:[/bold]
  Just type your query and PRATIGHAT-CORE will analyze it.
  
[bold]Examples:[/bold]
  • "Explain SQL injection for educational purposes"
  • "What is XSS and how to prevent it?"
  • "recon example.com"
"""
        self.console.print(Panel(help_text, title="Help", border_style="blue"))
    
    def create_progress(self, description: str = "Processing..."):
        """Create a progress indicator"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        )
    
    def print_success(self, message: str):
        """Print success message"""
        self.console.print(f"[green]✓[/green] {message}")
    
    def print_error(self, message: str):
        """Print error message"""
        self.console.print(f"[red]✗[/red] {message}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        self.console.print(f"[yellow]⚠[/yellow] {message}")
    
    def print_info(self, message: str):
        """Print info message"""
        self.console.print(f"[blue]ℹ[/blue] {message}")
    
    def input(self, prompt: str = "") -> str:
        """Get user input"""
        return self.console.input(prompt)
    
    def clear(self):
        """Clear console"""
        self.console.clear()


# Global UI instance
_ui: Optional[TerminalUI] = None


def get_ui() -> TerminalUI:
    """Get global terminal UI instance"""
    global _ui
    if _ui is None:
        _ui = TerminalUI()
    return _ui
