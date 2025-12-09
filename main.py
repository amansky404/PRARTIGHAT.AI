"""
PRATIGHAT.AI - Main Entry Point

Indigenous AI-powered penetration testing and cyber defense platform.
"""

import asyncio
import argparse
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from core.config import get_config, OperationalMode
from core.brain import get_core


console = Console()


def print_banner():
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
    
    console.print(banner, style="bold cyan")
    console.print()


def print_system_info():
    """Print system information"""
    config = get_config()
    hw = config.hardware
    
    info_text = f"""
[bold]System Configuration:[/bold]
  • Hardware Mode: [cyan]{hw.mode.value.upper()}[/cyan]
  • RAM: [cyan]{hw.ram_gb:.1f} GB[/cyan]
  • CPU Cores: [cyan]{hw.cpu_cores}[/cyan]
  • GPU Available: [cyan]{'Yes' if hw.has_gpu else 'No'}[/cyan]
  • Temperature: [cyan]{hw.temperature:.1f}°C[/cyan]
  • Operational Mode: [cyan]{config.operational_mode.value.upper()}[/cyan]

[bold]LLM Models:[/bold]
  • Strategist: [cyan]{config.models[list(config.models.keys())[0]].name}[/cyan]
  • Executor: [cyan]{config.models[list(config.models.keys())[1]].name if len(config.models) > 1 else 'N/A'}[/cyan]

[bold]Safety:[/bold]
  • Safe Mode: [green]ENABLED[/green]
  • Simulation Only: [green]ENABLED[/green]
"""
    
    console.print(Panel(info_text, title="[bold]PRATIGHAT-CORE Status[/bold]", 
                       border_style="green"))
    console.print()


async def interactive_mode():
    """Run in interactive mode"""
    print_banner()
    print_system_info()
    
    core = get_core()
    
    console.print("[bold green]Interactive Mode Active[/bold green]")
    console.print("[dim]Type 'help' for commands, 'exit' to quit[/dim]\n")
    
    while True:
        try:
            # Get user input
            query = console.input("[bold cyan]PRATIGHAT>[/bold cyan] ")
            
            if not query.strip():
                continue
            
            # Handle commands
            if query.lower() in ['exit', 'quit', 'q']:
                console.print("[yellow]Shutting down PRATIGHAT-CORE...[/yellow]")
                break
            
            elif query.lower() == 'help':
                help_text = """
[bold]Available Commands:[/bold]
  • help          - Show this help message
  • status        - Show system status
  • config        - Show configuration
  • clear         - Clear screen
  • exit/quit/q   - Exit PRATIGHAT.AI

[bold]Usage:[/bold]
  Just type your query and PRATIGHAT-CORE will analyze it.
  Example: "Explain SQL injection for educational purposes"
"""
                console.print(Panel(help_text, title="Help", border_style="blue"))
                continue
            
            elif query.lower() == 'status':
                print_system_info()
                continue
            
            elif query.lower() == 'config':
                config = get_config()
                console.print(f"[bold]Configuration:[/bold]")
                console.print(f"  • Database: {config.sqlite_path}")
                console.print(f"  • Vector DB: {config.chroma_path}")
                console.print(f"  • API: {config.api_host}:{config.api_port}")
                console.print()
                continue
            
            elif query.lower() == 'clear':
                console.clear()
                print_banner()
                continue
            
            # Process query through PRATIGHAT-CORE
            console.print("[dim]Processing with PRATIGHAT-CORE...[/dim]\n")
            
            response = await core.process_query(query)
            
            console.print(Panel(response, title="[bold]PRATIGHAT-CORE Response[/bold]",
                              border_style="green"))
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}\n")


async def api_mode(host: str, port: int):
    """Run in API mode"""
    import uvicorn
    
    print_banner()
    console.print(f"[bold green]Starting API Server on {host}:{port}[/bold green]\n")
    
    # Import FastAPI app
    try:
        from api.server import app
        
        config = uvicorn.Config(app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
    except ImportError:
        console.print("[red]API server not yet implemented[/red]")
        console.print("[dim]Run in interactive mode with: pratighat --interactive[/dim]")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="PRATIGHAT.AI - Indigenous AI-Powered Penetration Testing Platform"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "-a", "--api",
        action="store_true",
        help="Run API server"
    )
    
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="API server host (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API server port (default: 8000)"
    )
    
    parser.add_argument(
        "-m", "--mode",
        choices=["autopilot", "assisted", "manual"],
        help="Operational mode"
    )
    
    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    # Load config if specified
    if args.config:
        import os
        os.environ['PRATIGHAT_CONFIG'] = args.config
    
    # Set operational mode if specified
    if args.mode:
        config = get_config()
        config.operational_mode = OperationalMode(args.mode)
    
    # Determine mode
    if args.api:
        asyncio.run(api_mode(args.host, args.port))
    elif args.interactive:
        asyncio.run(interactive_mode())
    else:
        # Default to interactive
        print_banner()
        console.print("[dim]Starting in interactive mode...[/dim]")
        console.print("[dim]Use --help for more options[/dim]\n")
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
