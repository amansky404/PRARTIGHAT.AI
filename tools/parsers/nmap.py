"""
Nmap Output Parser

Parses nmap scan results into structured data
"""

from typing import Dict, Any, List, Optional
import re
import xml.etree.ElementTree as ET


class NmapParser:
    """Parser for nmap scan output"""
    
    def __init__(self):
        self.scan_info = {}
        self.hosts = []
    
    def parse_text_output(self, output: str) -> Dict[str, Any]:
        """
        Parse nmap text output
        
        Args:
            output: Raw text output from nmap
            
        Returns:
            Structured scan data
        """
        result = {
            "scan_info": {},
            "hosts": [],
            "summary": {}
        }
        
        lines = output.split('\n')
        current_host = None
        
        for line in lines:
            line = line.strip()
            
            # Parse scan info
            if "Nmap scan report for" in line:
                # New host found
                if current_host:
                    result["hosts"].append(current_host)
                
                # Extract hostname/IP
                match = re.search(r'Nmap scan report for (.+?)(?:\s+\((.+?)\))?$', line)
                if match:
                    hostname = match.group(1)
                    ip = match.group(2) if match.group(2) else hostname
                    
                    current_host = {
                        "hostname": hostname,
                        "ip": ip,
                        "ports": [],
                        "os": None,
                        "status": "up"
                    }
            
            # Parse port information
            elif current_host and "/tcp" in line or "/udp" in line:
                port_match = re.match(
                    r'(\d+)/(tcp|udp)\s+(\w+)\s+(\S+)(?:\s+(.+))?',
                    line
                )
                if port_match:
                    port_info = {
                        "port": int(port_match.group(1)),
                        "protocol": port_match.group(2),
                        "state": port_match.group(3),
                        "service": port_match.group(4),
                        "version": port_match.group(5) if port_match.group(5) else ""
                    }
                    current_host["ports"].append(port_info)
            
            # Parse OS detection
            elif current_host and "OS details:" in line:
                os_info = line.split("OS details:", 1)[1].strip()
                current_host["os"] = os_info
            
            # Parse MAC address
            elif current_host and "MAC Address:" in line:
                mac_match = re.search(r'MAC Address: ([0-9A-F:]+)', line)
                if mac_match:
                    current_host["mac"] = mac_match.group(1)
            
            # Parse latency
            elif current_host and "latency" in line.lower():
                latency_match = re.search(r'([\d.]+)\s*ms', line)
                if latency_match:
                    current_host["latency_ms"] = float(latency_match.group(1))
            
            # Parse summary
            elif "Nmap done:" in line:
                summary_match = re.search(
                    r'(\d+) IP address(?:es)? \((\d+) host(?:s)? up\)',
                    line
                )
                if summary_match:
                    result["summary"] = {
                        "total_hosts": int(summary_match.group(1)),
                        "hosts_up": int(summary_match.group(2))
                    }
        
        # Add last host
        if current_host:
            result["hosts"].append(current_host)
        
        return result
    
    def parse_xml_output(self, xml_output: str) -> Dict[str, Any]:
        """
        Parse nmap XML output (-oX)
        
        Args:
            xml_output: Raw XML output from nmap
            
        Returns:
            Structured scan data
        """
        try:
            root = ET.fromstring(xml_output)
            
            result = {
                "scan_info": self._parse_scan_info_xml(root),
                "hosts": [],
                "summary": {}
            }
            
            # Parse each host
            for host in root.findall('host'):
                host_data = self._parse_host_xml(host)
                if host_data:
                    result["hosts"].append(host_data)
            
            # Parse run stats
            runstats = root.find('runstats')
            if runstats is not None:
                hosts = runstats.find('hosts')
                if hosts is not None:
                    result["summary"] = {
                        "total_hosts": int(hosts.get('total', 0)),
                        "hosts_up": int(hosts.get('up', 0)),
                        "hosts_down": int(hosts.get('down', 0))
                    }
            
            return result
            
        except ET.ParseError as e:
            return {
                "error": f"XML parsing failed: {str(e)}",
                "scan_info": {},
                "hosts": [],
                "summary": {}
            }
    
    def _parse_scan_info_xml(self, root: ET.Element) -> Dict[str, Any]:
        """Parse scan information from XML"""
        scan_info = {}
        
        # Get nmaprun attributes
        scan_info["scanner"] = root.get('scanner', 'nmap')
        scan_info["version"] = root.get('version', '')
        scan_info["start_time"] = root.get('start', '')
        
        # Get scaninfo element
        scaninfo = root.find('scaninfo')
        if scaninfo is not None:
            scan_info["type"] = scaninfo.get('type', '')
            scan_info["protocol"] = scaninfo.get('protocol', '')
            scan_info["num_services"] = scaninfo.get('numservices', '')
        
        return scan_info
    
    def _parse_host_xml(self, host: ET.Element) -> Optional[Dict[str, Any]]:
        """Parse individual host from XML"""
        host_data = {
            "hostname": None,
            "ip": None,
            "status": "unknown",
            "ports": [],
            "os": None,
            "mac": None,
            "latency_ms": None
        }
        
        # Get status
        status = host.find('status')
        if status is not None:
            host_data["status"] = status.get('state', 'unknown')
        
        # Get addresses
        for address in host.findall('address'):
            addr_type = address.get('addrtype', '')
            addr = address.get('addr', '')
            
            if addr_type == 'ipv4' or addr_type == 'ipv6':
                host_data["ip"] = addr
            elif addr_type == 'mac':
                host_data["mac"] = addr
        
        # Get hostname
        hostnames = host.find('hostnames')
        if hostnames is not None:
            hostname = hostnames.find('hostname')
            if hostname is not None:
                host_data["hostname"] = hostname.get('name', '')
        
        # Get ports
        ports = host.find('ports')
        if ports is not None:
            for port in ports.findall('port'):
                port_data = self._parse_port_xml(port)
                if port_data:
                    host_data["ports"].append(port_data)
        
        # Get OS
        os_elem = host.find('os')
        if os_elem is not None:
            osmatch = os_elem.find('osmatch')
            if osmatch is not None:
                host_data["os"] = osmatch.get('name', '')
        
        # Get latency
        times = host.find('times')
        if times is not None:
            rtt = times.get('rttvar', '')
            if rtt:
                try:
                    host_data["latency_ms"] = float(rtt) / 1000
                except:
                    pass
        
        return host_data
    
    def _parse_port_xml(self, port: ET.Element) -> Optional[Dict[str, Any]]:
        """Parse port information from XML"""
        port_data = {
            "port": int(port.get('portid', 0)),
            "protocol": port.get('protocol', 'tcp'),
            "state": "unknown",
            "service": "",
            "version": ""
        }
        
        # Get state
        state = port.find('state')
        if state is not None:
            port_data["state"] = state.get('state', 'unknown')
        
        # Get service
        service = port.find('service')
        if service is not None:
            port_data["service"] = service.get('name', '')
            
            # Build version string
            version_parts = []
            if service.get('product'):
                version_parts.append(service.get('product'))
            if service.get('version'):
                version_parts.append(service.get('version'))
            if service.get('extrainfo'):
                version_parts.append(f"({service.get('extrainfo')})")
            
            port_data["version"] = " ".join(version_parts)
        
        return port_data
    
    def get_open_ports(self, parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all open ports from parsed data"""
        open_ports = []
        
        for host in parsed_data.get("hosts", []):
            for port in host.get("ports", []):
                if port.get("state") == "open":
                    open_ports.append({
                        "host": host.get("ip"),
                        "hostname": host.get("hostname"),
                        "port": port.get("port"),
                        "protocol": port.get("protocol"),
                        "service": port.get("service"),
                        "version": port.get("version")
                    })
        
        return open_ports
    
    def get_services_summary(self, parsed_data: Dict[str, Any]) -> Dict[str, int]:
        """Get summary of detected services"""
        services = {}
        
        for host in parsed_data.get("hosts", []):
            for port in host.get("ports", []):
                if port.get("state") == "open":
                    service = port.get("service", "unknown")
                    services[service] = services.get(service, 0) + 1
        
        return services


# Singleton instance
_nmap_parser = None


def get_nmap_parser() -> NmapParser:
    """Get the global NmapParser instance"""
    global _nmap_parser
    if _nmap_parser is None:
        _nmap_parser = NmapParser()
    return _nmap_parser
