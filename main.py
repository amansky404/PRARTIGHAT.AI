"""
PRATIGHAT.AI - Main Entry Point

Indigenous AI-powered penetration testing and cyber defense platform.
"""

import asyncio
import argparse
import sys
from typing import Optional

from core.config import get_config, OperationalMode
from core.brain import get_core
from agents.recon import ReconAgent
from agents.report import ReportAgent
from ui.terminal import get_ui


async def interactive_mode():
    """Run in interactive mode"""
    ui = get_ui()
    ui.print_banner()
    
    config = get_config()
    ui.print_system_info(config)
    
    # Initialize core and agents
    core = get_core()
    recon_agent = ReconAgent()
    report_agent = ReportAgent()
    
    # Register agents with core
    core.register_agent("recon", recon_agent)
    core.register_agent("report", report_agent)
    
    ui.console.print("[bold green]Interactive Mode Active[/bold green]")
    ui.console.print("[dim]Type 'help' for commands, 'exit' to quit[/dim]\n")
    
    ui.add_log("PRATIGHAT-CORE initialized", "INFO", "core")
    ui.add_log("Agents registered: recon, report", "INFO", "core")
    
    while True:
        try:
            # Get user input
            query = ui.input("[bold cyan]PRATIGHAT>[/bold cyan] ")
            
            if not query.strip():
                continue
            
            # Handle commands
            if query.lower() in ['exit', 'quit', 'q']:
                ui.console.print("[yellow]Shutting down PRATIGHAT-CORE...[/yellow]")
                break
            
            elif query.lower() == 'help':
                ui.show_help()
                continue
            
            elif query.lower() == 'status':
                ui.print_system_info(config)
                continue
            
            elif query.lower() == 'config':
                ui.console.print(f"[bold]Configuration:[/bold]")
                ui.console.print(f"  • Database: {config.sqlite_path}")
                ui.console.print(f"  • Vector DB: {config.chroma_path}")
                ui.console.print(f"  • API: {config.api_host}:{config.api_port}")
                ui.console.print()
                continue
            
            elif query.lower() == 'agents':
                ui.print_agent_status({
                    "recon": "idle",
                    "report": "idle",
                    "core": "active"
                })
                continue
            
            elif query.lower() == 'logs':
                ui.print_logs()
                continue
            
            elif query.lower() == 'clear':
                ui.clear()
                ui.print_banner()
                continue
            
            # Handle agent commands
            elif query.lower().startswith('recon '):
                target = query[6:].strip()
                ui.add_log(f"Starting recon on {target}", "INFO", "recon")
                
                with ui.create_progress() as progress:
                    task = progress.add_task(f"[cyan]Analyzing {target}...", total=None)
                    result = await recon_agent.execute("analyze_target", {"target": target})
                    progress.update(task, completed=True)
                
                ui.print_result(result, "Reconnaissance Result")
                ui.add_log(f"Recon completed for {target}", "INFO", "recon")
                continue
            
            elif query.lower() == 'report':
                ui.add_log("Generating report", "INFO", "report")
                
                with ui.create_progress() as progress:
                    task = progress.add_task("[cyan]Generating report...", total=None)
                    result = await report_agent.execute("generate_executive_summary", {
                        "scope": "General assessment",
                        "findings": []
                    })
                    progress.update(task, completed=True)
                
                ui.print_result(result, "Report Generation")
                ui.add_log("Report generated", "INFO", "report")
                continue
            
            # Process query through PRATIGHAT-CORE
            ui.add_log(f"Processing query: {query[:50]}...", "INFO", "core")
            ui.console.print("[dim]Processing with PRATIGHAT-CORE...[/dim]\n")
            
            response = await core.process_query(query)
            
            ui.print_result(response, "PRATIGHAT-CORE Response")
            ui.add_log("Query processed successfully", "INFO", "core")
            
        except KeyboardInterrupt:
            ui.console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except Exception as e:
            ui.print_error(f"Error: {str(e)}")
            ui.add_log(f"Error: {str(e)}", "ERROR", "core")


async def api_mode(host: str, port: int):
    """Run in API mode"""
    ui = get_ui()
    ui.print_banner()
    ui.console.print(f"[bold yellow]API Server Mode[/bold yellow]\n")
    ui.console.print("[yellow]⚠ API server is not yet fully implemented in this version.[/yellow]")
    ui.console.print()
    ui.console.print("[dim]The API server will be added in a future update.[/dim]")
    ui.console.print("[dim]For now, please use interactive mode: python main.py[/dim]")
    ui.console.print()
    ui.console.print("[bold]Planned API features:[/bold]")
    ui.console.print("  • RESTful endpoints for all agents")
    ui.console.print("  • WebSocket support for real-time updates")
    ui.console.print("  • Authentication and rate limiting")
    ui.console.print("  • OpenAPI documentation")
    ui.console.print()
    ui.console.print("[green]Would you like to start in interactive mode instead? (y/n)[/green]")
    
    try:
        choice = ui.input().lower()
        if choice == 'y':
            await interactive_mode()
    except KeyboardInterrupt:
        ui.console.print("\n[yellow]Exiting...[/yellow]")


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
        ui = get_ui()
        ui.print_banner()
        ui.console.print("[dim]Starting in interactive mode...[/dim]")
        ui.console.print("[dim]Use --help for more options[/dim]\n")
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
