"""
Pattern Agent - Vulnerability Pattern Detection and Fingerprinting

This agent detects vulnerability patterns and performs system fingerprinting
for educational and authorized testing purposes.
"""

from typing import Dict, Any, List
from agents.base import BaseAgent, AgentResult
import re


class PatternAgent(BaseAgent):
    """
    Pattern Agent for detecting vulnerability patterns and fingerprinting.
    
    Analyzes patterns to identify potential security issues in an educational context.
    """
    
    def __init__(self):
        super().__init__(
            name="pattern",
            description="Detects vulnerability patterns and performs fingerprinting"
        )
        
        self.supported_tasks = [
            "detect_patterns",
            "fingerprint_service",
            "analyze_configuration",
            "identify_cve_patterns",
            "match_vulnerability_signature",
        ]
        
        # Common vulnerability patterns (educational)
        self.patterns = {
            "sql_injection": [
                r"error in your SQL syntax",
                r"mysql_fetch",
                r"ORA-\d{5}",
                r"Microsoft SQL Server",
                r"SQLSTATE\[\d+\]"
            ],
            "xss": [
                r"<script>",
                r"javascript:",
                r"onerror=",
                r"onload="
            ],
            "path_traversal": [
                r"\.\./",
                r"\.\.\\",
                r"%2e%2e",
                r"..%252f"
            ],
            "command_injection": [
                r";\s*ls\s",
                r"&&\s*dir",
                r"\|\s*cat\s",
                r"`whoami`"
            ],
            "xxe": [
                r"<!ENTITY",
                r"<!DOCTYPE",
                r"SYSTEM\s+[\"']file:///"
            ]
        }
    
    async def execute(self, task: str, params: Dict[str, Any]) -> AgentResult:
        """
        Execute a pattern detection task
        
        Args:
            task: Task name
            params: Task parameters
            
        Returns:
            AgentResult with pattern analysis
        """
        if task == "detect_patterns":
            return await self._detect_patterns(params)
        elif task == "fingerprint_service":
            return await self._fingerprint_service(params)
        elif task == "analyze_configuration":
            return await self._analyze_configuration(params)
        elif task == "identify_cve_patterns":
            return await self._identify_cve_patterns(params)
        elif task == "match_vulnerability_signature":
            return await self._match_vulnerability_signature(params)
        else:
            return AgentResult(
                success=False,
                data={},
                message=f"Unknown task: {task}",
                agent=self.name
            )
    
    async def _detect_patterns(self, params: Dict[str, Any]) -> AgentResult:
        """Detect vulnerability patterns in input"""
        content = params.get("content", "")
        context = params.get("context", "general")
        
        detected = []
        
        # Check each pattern category
        for vuln_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    detected.append({
                        "type": vuln_type,
                        "pattern": pattern,
                        "severity": self._assess_pattern_severity(vuln_type),
                        "recommendation": self._get_recommendation(vuln_type)
                    })
                    break  # Only report once per category
        
        result = {
            "patterns_detected": detected,
            "total_found": len(detected),
            "context": context,
            "is_educational": True,
            "disclaimer": "Pattern detection for educational analysis only"
        }
        
        return AgentResult(
            success=True,
            data=result,
            message=f"Detected {len(detected)} potential patterns",
            agent=self.name
        )
    
    async def _fingerprint_service(self, params: Dict[str, Any]) -> AgentResult:
        """Fingerprint a service based on response characteristics"""
        service_type = params.get("service_type", "unknown")
        banner = params.get("banner", "")
        headers = params.get("headers", {})
        
        fingerprint = {
            "service": service_type,
            "identification": {
                "method": "Banner/Header analysis",
                "confidence": "Educational estimation"
            },
            "characteristics": []
        }
        
        # Web server fingerprinting examples
        if service_type == "http" or service_type == "web":
            server_header = headers.get("Server", banner)
            
            if "Apache" in server_header:
                fingerprint["characteristics"].append({
                    "type": "Web Server",
                    "product": "Apache HTTP Server",
                    "indicators": ["Server: Apache", "Apache modules"],
                    "common_versions": ["2.4.x", "2.2.x"]
                })
            elif "nginx" in server_header:
                fingerprint["characteristics"].append({
                    "type": "Web Server",
                    "product": "nginx",
                    "indicators": ["Server: nginx", "nginx error pages"],
                    "common_versions": ["1.x.x"]
                })
            elif "IIS" in server_header or "Microsoft" in server_header:
                fingerprint["characteristics"].append({
                    "type": "Web Server",
                    "product": "Microsoft IIS",
                    "indicators": ["Server: Microsoft-IIS", "X-Powered-By: ASP.NET"],
                    "common_versions": ["10.0", "8.5", "7.5"]
                })
        
        # SSH fingerprinting example
        elif service_type == "ssh":
            fingerprint["characteristics"].append({
                "type": "SSH Server",
                "analysis": "SSH banner analysis",
                "indicators": ["SSH-2.0-", "Protocol version"],
                "security_note": "SSH version disclosure can aid reconnaissance"
            })
        
        # Database fingerprinting example
        elif "sql" in service_type.lower() or "database" in service_type.lower():
            fingerprint["characteristics"].append({
                "type": "Database Server",
                "analysis": "Database fingerprinting",
                "common_indicators": [
                    "Error messages",
                    "Default ports (3306, 5432, 1433)",
                    "Response characteristics"
                ],
                "security_note": "Database exposure should be minimized"
            })
        
        fingerprint["recommendations"] = [
            "Minimize information disclosure in banners",
            "Use security headers appropriately",
            "Keep services updated",
            "Apply security hardening guidelines"
        ]
        
        return AgentResult(
            success=True,
            data=fingerprint,
            message=f"Fingerprinted {service_type} service",
            agent=self.name
        )
    
    async def _analyze_configuration(self, params: Dict[str, Any]) -> AgentResult:
        """Analyze configuration for security issues"""
        config_type = params.get("config_type", "general")
        config_data = params.get("config_data", {})
        
        analysis = {
            "configuration_type": config_type,
            "security_findings": [],
            "best_practices": []
        }
        
        # Web server configuration analysis
        if config_type == "web_server":
            analysis["security_findings"] = [
                {
                    "finding": "Security Headers",
                    "check": "Verify presence of security headers",
                    "recommended_headers": [
                        "Content-Security-Policy",
                        "X-Frame-Options",
                        "X-Content-Type-Options",
                        "Strict-Transport-Security",
                        "X-XSS-Protection"
                    ]
                },
                {
                    "finding": "Directory Listing",
                    "check": "Ensure directory listing is disabled",
                    "risk": "Information disclosure"
                },
                {
                    "finding": "Default Pages",
                    "check": "Remove default installation pages",
                    "risk": "Version disclosure, reconnaissance aid"
                }
            ]
        
        # SSH configuration analysis
        elif config_type == "ssh":
            analysis["security_findings"] = [
                {
                    "finding": "Root Login",
                    "check": "PermitRootLogin should be 'no'",
                    "risk": "Direct root access"
                },
                {
                    "finding": "Password Authentication",
                    "check": "Consider key-based authentication",
                    "risk": "Brute force attacks"
                },
                {
                    "finding": "Protocol Version",
                    "check": "Use Protocol 2 only",
                    "risk": "Protocol 1 vulnerabilities"
                }
            ]
        
        # Database configuration analysis
        elif "database" in config_type:
            analysis["security_findings"] = [
                {
                    "finding": "Remote Access",
                    "check": "Restrict database remote access",
                    "risk": "Unauthorized access"
                },
                {
                    "finding": "Default Credentials",
                    "check": "Ensure default passwords are changed",
                    "risk": "Trivial compromise"
                },
                {
                    "finding": "Encryption",
                    "check": "Enable TLS/SSL for connections",
                    "risk": "Data interception"
                }
            ]
        
        analysis["best_practices"] = [
            "Follow CIS Benchmarks for your platform",
            "Implement principle of least privilege",
            "Regular security audits",
            "Keep software updated",
            "Enable logging and monitoring"
        ]
        
        return AgentResult(
            success=True,
            data=analysis,
            message=f"Analyzed {config_type} configuration",
            agent=self.name
        )
    
    async def _identify_cve_patterns(self, params: Dict[str, Any]) -> AgentResult:
        """Identify patterns associated with known CVEs (educational)"""
        service = params.get("service", "unknown")
        version = params.get("version", "unknown")
        
        # This is educational - real CVE matching requires CVE databases
        cve_info = {
            "service": service,
            "version": version,
            "analysis_type": "Educational CVE pattern analysis",
            "methodology": [
                "Check service version against CVE databases",
                "Analyze vulnerability patterns",
                "Assess exploitability",
                "Determine patch availability"
            ],
            "data_sources": [
                "NVD (National Vulnerability Database)",
                "CVE.org",
                "Vendor security advisories",
                "Security research publications"
            ],
            "example_cve_structure": {
                "id": "CVE-YYYY-NNNNN",
                "description": "Vulnerability description",
                "cvss_score": "0.0-10.0",
                "affected_versions": "Version range",
                "patches": "Patch information"
            },
            "recommendations": [
                "Subscribe to security mailing lists",
                "Implement vulnerability management program",
                "Regular patching schedule",
                "Use vulnerability scanners",
                "Monitor security advisories"
            ]
        }
        
        return AgentResult(
            success=True,
            data=cve_info,
            message=f"Analyzed CVE patterns for {service}",
            agent=self.name
        )
    
    async def _match_vulnerability_signature(self, params: Dict[str, Any]) -> AgentResult:
        """Match vulnerability signatures (educational)"""
        signature_type = params.get("signature_type", "generic")
        target_data = params.get("target_data", "")
        
        signature_match = {
            "signature_type": signature_type,
            "matching_process": [
                "Collect target characteristics",
                "Compare against known signatures",
                "Assess confidence level",
                "Provide recommendations"
            ],
            "signature_categories": {
                "behavioral": "Anomalous behavior patterns",
                "structural": "Code or configuration patterns",
                "network": "Traffic patterns",
                "cryptographic": "Weak crypto signatures"
            },
            "confidence_levels": {
                "high": "Strong indicators present",
                "medium": "Some indicators match",
                "low": "Weak correlation",
                "unknown": "Insufficient data"
            },
            "next_steps": [
                "Verify findings manually",
                "Consult vulnerability databases",
                "Test in controlled environment",
                "Document findings thoroughly"
            ]
        }
        
        return AgentResult(
            success=True,
            data=signature_match,
            message=f"Analyzed vulnerability signatures for {signature_type}",
            agent=self.name
        )
    
    def _assess_pattern_severity(self, vuln_type: str) -> str:
        """Assess severity of detected pattern"""
        high_severity = ["sql_injection", "command_injection", "xxe"]
        medium_severity = ["xss", "path_traversal"]
        
        if vuln_type in high_severity:
            return "High (potential for significant impact)"
        elif vuln_type in medium_severity:
            return "Medium (requires investigation)"
        else:
            return "Variable (context-dependent)"
    
    def _get_recommendation(self, vuln_type: str) -> str:
        """Get recommendation for vulnerability type"""
        recommendations = {
            "sql_injection": "Use parameterized queries, input validation, ORM frameworks",
            "xss": "Output encoding, Content Security Policy, input validation",
            "path_traversal": "Input validation, whitelist allowed paths, chroot jails",
            "command_injection": "Avoid system commands, use APIs, input sanitization",
            "xxe": "Disable external entities, use safe XML parsers"
        }
        
        return recommendations.get(
            vuln_type,
            "Follow OWASP guidelines and security best practices"
        )


# Singleton instance
_pattern_agent = None


def get_pattern_agent() -> PatternAgent:
    """Get the global Pattern Agent instance"""
    global _pattern_agent
    if _pattern_agent is None:
        _pattern_agent = PatternAgent()
    return _pattern_agent
