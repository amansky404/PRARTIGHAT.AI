"""
Nmap Wrapper - High-level interface for nmap scanning

Provides safe, easy-to-use nmap functionality
"""

from typing import Dict, Any, List, Optional
from tools.executor import get_executor, ToolResult
from tools.parsers.nmap import get_nmap_parser


class NmapWrapper:
    """High-level wrapper for nmap operations"""
    
    def __init__(self):
        self.executor = get_executor()
        self.parser = get_nmap_parser()
    
    async def ping_scan(self, targets: str) -> Dict[str, Any]:
        """
        Perform a ping scan to discover live hosts
        
        Args:
            targets: Target hosts/networks (e.g., "192.168.1.0/24")
            
        Returns:
            Parsed scan results
        """
        args = ["-sn", targets]
        result = await self.executor.execute_tool("nmap", args, timeout=60)
        
        if result.status.value == "completed":
            parsed = self.parser.parse_text_output(result.output)
            return {
                "success": True,
                "data": parsed,
                "raw_output": result.output
            }
        else:
            return {
                "success": False,
                "error": result.error,
                "status": result.status.value
            }
    
    async def port_scan(
        self,
        target: str,
        ports: Optional[str] = None,
        scan_type: str = "syn"
    ) -> Dict[str, Any]:
        """
        Perform a port scan
        
        Args:
            target: Target host
            ports: Port specification (e.g., "22,80,443" or "1-1000")
            scan_type: Type of scan (syn, tcp, udp)
            
        Returns:
            Parsed scan results
        """
        args = []
        
        # Scan type
        if scan_type == "syn":
            args.append("-sS")
        elif scan_type == "tcp":
            args.append("-sT")
        elif scan_type == "udp":
            args.append("-sU")
        
        # Ports
        if ports:
            args.extend(["-p", ports])
        
        args.append(target)
        
        result = await self.executor.execute_tool("nmap", args, timeout=300)
        
        if result.status.value == "completed":
            parsed = self.parser.parse_text_output(result.output)
            return {
                "success": True,
                "data": parsed,
                "raw_output": result.output
            }
        else:
            return {
                "success": False,
                "error": result.error,
                "status": result.status.value
            }
    
    async def service_scan(
        self,
        target: str,
        ports: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform service version detection scan
        
        Args:
            target: Target host
            ports: Port specification
            
        Returns:
            Parsed scan results with service versions
        """
        args = ["-sV"]
        
        if ports:
            args.extend(["-p", ports])
        
        args.append(target)
        
        result = await self.executor.execute_tool("nmap", args, timeout=300)
        
        if result.status.value == "completed":
            parsed = self.parser.parse_text_output(result.output)
            return {
                "success": True,
                "data": parsed,
                "open_ports": self.parser.get_open_ports(parsed),
                "services": self.parser.get_services_summary(parsed),
                "raw_output": result.output
            }
        else:
            return {
                "success": False,
                "error": result.error,
                "status": result.status.value
            }
    
    async def os_detection(self, target: str) -> Dict[str, Any]:
        """
        Perform OS detection scan
        
        Args:
            target: Target host
            
        Returns:
            Parsed scan results with OS information
        """
        args = ["-O", target]
        
        result = await self.executor.execute_tool("nmap", args, timeout=180)
        
        if result.status.value == "completed":
            parsed = self.parser.parse_text_output(result.output)
            return {
                "success": True,
                "data": parsed,
                "raw_output": result.output
            }
        else:
            return {
                "success": False,
                "error": result.error,
                "status": result.status.value
            }
    
    async def full_scan(
        self,
        target: str,
        aggressive: bool = False
    ) -> Dict[str, Any]:
        """
        Perform a comprehensive scan
        
        Args:
            target: Target host
            aggressive: Enable aggressive scan options
            
        Returns:
            Complete scan results
        """
        args = ["-sV", "-sC"]
        
        if aggressive:
            args.append("-A")
        
        args.append(target)
        
        result = await self.executor.execute_tool("nmap", args, timeout=600)
        
        if result.status.value == "completed":
            parsed = self.parser.parse_text_output(result.output)
            return {
                "success": True,
                "data": parsed,
                "open_ports": self.parser.get_open_ports(parsed),
                "services": self.parser.get_services_summary(parsed),
                "raw_output": result.output
            }
        else:
            return {
                "success": False,
                "error": result.error,
                "status": result.status.value
            }
    
    async def script_scan(
        self,
        target: str,
        scripts: Optional[List[str]] = None,
        ports: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run NSE scripts against target
        
        Args:
            target: Target host
            scripts: List of script names or categories
            ports: Port specification
            
        Returns:
            Script scan results
        """
        args = []
        
        if scripts:
            args.extend(["--script", ",".join(scripts)])
        else:
            args.append("-sC")  # Default scripts
        
        if ports:
            args.extend(["-p", ports])
        
        args.append(target)
        
        result = await self.executor.execute_tool("nmap", args, timeout=300)
        
        if result.status.value == "completed":
            parsed = self.parser.parse_text_output(result.output)
            return {
                "success": True,
                "data": parsed,
                "raw_output": result.output
            }
        else:
            return {
                "success": False,
                "error": result.error,
                "status": result.status.value
            }
    
    def is_available(self) -> bool:
        """Check if nmap is available"""
        return self.executor.is_tool_available("nmap")


# Singleton instance
_nmap_wrapper = None


def get_nmap_wrapper() -> NmapWrapper:
    """Get the global NmapWrapper instance"""
    global _nmap_wrapper
    if _nmap_wrapper is None:
        _nmap_wrapper = NmapWrapper()
    return _nmap_wrapper
