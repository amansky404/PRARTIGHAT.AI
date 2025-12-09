"""
Tool Executor - Base framework for executing security tools safely

This module provides the base infrastructure for executing security tools
in a controlled, safe manner for authorized testing only.
"""

from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import asyncio
import subprocess
from dataclasses import dataclass
import time


class ToolStatus(Enum):
    """Tool execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class ToolCategory(Enum):
    """Categories of security tools"""
    SCANNER = "scanner"
    ENUMERATION = "enumeration"
    EXPLOITATION = "exploitation"
    POST_EXPLOITATION = "post_exploitation"
    ANALYSIS = "analysis"
    UTILITY = "utility"


@dataclass
class ToolResult:
    """Result from tool execution"""
    tool_name: str
    status: ToolStatus
    output: str
    error: str
    exit_code: int
    execution_time: float
    metadata: Dict[str, Any]


class ToolExecutor:
    """
    Base class for executing security tools safely
    
    Provides controlled execution environment with:
    - Safety checks
    - Timeout management
    - Output capture
    - Error handling
    - Logging
    """
    
    def __init__(self):
        self.max_timeout = 300  # 5 minutes default
        self.safety_checks_enabled = True
        self.dry_run = False
        self.allowed_tools = self._init_allowed_tools()
    
    def _init_allowed_tools(self) -> Dict[str, Dict[str, Any]]:
        """Initialize list of allowed tools with their configurations"""
        return {
            "nmap": {
                "category": ToolCategory.SCANNER,
                "binary": "nmap",
                "safe_args": ["-sV", "-sC", "-p", "-T", "-A", "-O"],
                "unsafe_args": [],  # Add dangerous args to block
                "requires_root": False,
                "timeout": 300
            },
            "gobuster": {
                "category": ToolCategory.ENUMERATION,
                "binary": "gobuster",
                "safe_args": ["dir", "dns", "vhost", "-u", "-w", "-t"],
                "unsafe_args": [],
                "requires_root": False,
                "timeout": 600
            },
            "nikto": {
                "category": ToolCategory.SCANNER,
                "binary": "nikto",
                "safe_args": ["-h", "-p", "-ssl", "-id"],
                "unsafe_args": [],
                "requires_root": False,
                "timeout": 600
            },
            "sqlmap": {
                "category": ToolCategory.EXPLOITATION,
                "binary": "sqlmap",
                "safe_args": ["-u", "--dbs", "--tables", "--batch", "--level", "--risk"],
                "unsafe_args": ["--os-shell", "--sql-shell"],  # Block dangerous operations
                "requires_root": False,
                "timeout": 300
            },
            "wpscan": {
                "category": ToolCategory.SCANNER,
                "binary": "wpscan",
                "safe_args": ["--url", "--enumerate", "--api-token"],
                "unsafe_args": [],
                "requires_root": False,
                "timeout": 300
            },
            "dig": {
                "category": ToolCategory.ENUMERATION,
                "binary": "dig",
                "safe_args": ["@", "+short", "+trace"],
                "unsafe_args": [],
                "requires_root": False,
                "timeout": 30
            },
            "whois": {
                "category": ToolCategory.ENUMERATION,
                "binary": "whois",
                "safe_args": [],
                "unsafe_args": [],
                "requires_root": False,
                "timeout": 30
            }
        }
    
    async def execute_tool(
        self,
        tool_name: str,
        args: List[str],
        timeout: Optional[int] = None,
        capture_output: bool = True
    ) -> ToolResult:
        """
        Execute a security tool safely
        
        Args:
            tool_name: Name of the tool to execute
            args: Command line arguments
            timeout: Execution timeout in seconds
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            ToolResult with execution details
        """
        start_time = time.time()
        
        # Validate tool
        if tool_name not in self.allowed_tools:
            return ToolResult(
                tool_name=tool_name,
                status=ToolStatus.FAILED,
                output="",
                error=f"Tool '{tool_name}' is not in allowed tools list",
                exit_code=-1,
                execution_time=0,
                metadata={"reason": "tool_not_allowed"}
            )
        
        tool_config = self.allowed_tools[tool_name]
        
        # Safety checks
        if self.safety_checks_enabled:
            safety_check = self._check_safety(tool_name, args, tool_config)
            if not safety_check["safe"]:
                return ToolResult(
                    tool_name=tool_name,
                    status=ToolStatus.FAILED,
                    output="",
                    error=f"Safety check failed: {safety_check['reason']}",
                    exit_code=-1,
                    execution_time=0,
                    metadata={"reason": "safety_check_failed", "details": safety_check}
                )
        
        # Dry run mode
        if self.dry_run:
            return ToolResult(
                tool_name=tool_name,
                status=ToolStatus.COMPLETED,
                output=f"[DRY RUN] Would execute: {tool_config['binary']} {' '.join(args)}",
                error="",
                exit_code=0,
                execution_time=0,
                metadata={"dry_run": True}
            )
        
        # Set timeout
        execution_timeout = timeout or tool_config.get("timeout", self.max_timeout)
        
        # Build command
        cmd = [tool_config["binary"]] + args
        
        # Execute
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE if capture_output else None,
                stderr=asyncio.subprocess.PIPE if capture_output else None
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=execution_timeout
                )
                
                execution_time = time.time() - start_time
                
                return ToolResult(
                    tool_name=tool_name,
                    status=ToolStatus.COMPLETED if process.returncode == 0 else ToolStatus.FAILED,
                    output=stdout.decode() if stdout else "",
                    error=stderr.decode() if stderr else "",
                    exit_code=process.returncode,
                    execution_time=execution_time,
                    metadata={"command": " ".join(cmd)}
                )
                
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                
                execution_time = time.time() - start_time
                
                return ToolResult(
                    tool_name=tool_name,
                    status=ToolStatus.TIMEOUT,
                    output="",
                    error=f"Tool execution exceeded timeout of {execution_timeout} seconds",
                    exit_code=-1,
                    execution_time=execution_time,
                    metadata={"timeout": execution_timeout}
                )
                
        except FileNotFoundError:
            execution_time = time.time() - start_time
            
            return ToolResult(
                tool_name=tool_name,
                status=ToolStatus.FAILED,
                output="",
                error=f"Tool binary '{tool_config['binary']}' not found. Please install {tool_name}.",
                exit_code=-1,
                execution_time=execution_time,
                metadata={"reason": "binary_not_found"}
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return ToolResult(
                tool_name=tool_name,
                status=ToolStatus.FAILED,
                output="",
                error=f"Unexpected error: {str(e)}",
                exit_code=-1,
                execution_time=execution_time,
                metadata={"exception": str(e)}
            )
    
    def _check_safety(
        self,
        tool_name: str,
        args: List[str],
        tool_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform safety checks on tool execution
        
        Returns:
            Dict with 'safe' boolean and 'reason' if unsafe
        """
        # Check for unsafe arguments
        unsafe_args = tool_config.get("unsafe_args", [])
        for arg in args:
            for unsafe in unsafe_args:
                if unsafe in arg:
                    return {
                        "safe": False,
                        "reason": f"Unsafe argument detected: {unsafe}"
                    }
        
        # Check for suspicious patterns
        suspicious_patterns = [
            "--os-",  # OS command execution
            "--sql-shell",  # SQL shell
            "--file-write",  # File writing
            "--file-dest",  # File destination
            "&&",  # Command chaining
            ";",  # Command separator (in certain contexts)
            "|",  # Pipe
        ]
        
        args_str = " ".join(args)
        for pattern in suspicious_patterns:
            if pattern in args_str:
                return {
                    "safe": False,
                    "reason": f"Suspicious pattern detected: {pattern}"
                }
        
        # Additional safety checks can be added here
        
        return {"safe": True, "reason": ""}
    
    def is_tool_available(self, tool_name: str) -> bool:
        """Check if a tool is available in the system"""
        if tool_name not in self.allowed_tools:
            return False
        
        tool_config = self.allowed_tools[tool_name]
        binary = tool_config["binary"]
        
        try:
            result = subprocess.run(
                ["which", binary],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        available = []
        for tool_name in self.allowed_tools:
            if self.is_tool_available(tool_name):
                available.append(tool_name)
        return available
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a tool"""
        if tool_name not in self.allowed_tools:
            return None
        
        config = self.allowed_tools[tool_name].copy()
        config["available"] = self.is_tool_available(tool_name)
        return config


# Singleton instance
_executor = None


def get_executor() -> ToolExecutor:
    """Get the global ToolExecutor instance"""
    global _executor
    if _executor is None:
        _executor = ToolExecutor()
    return _executor
