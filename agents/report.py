"""
PRATIGHAT.AI Report Agent

Generates comprehensive reports from reconnaissance and analysis results.
"""

from typing import Dict, Any, List
from datetime import datetime
from agents.base import BaseAgent, AgentResult
from core.routing import route_request
from core.config import ModelType


class ReportAgent(BaseAgent):
    """
    Report Generation Agent
    
    Generates:
    - Executive summaries
    - Technical findings reports
    - Safe PoC documentation
    - Recommendations
    - Educational walkthroughs
    """
    
    def __init__(self):
        super().__init__("report")
        self.supported_tasks = [
            "generate_executive_summary",
            "generate_technical_report",
            "generate_poc_documentation",
            "generate_recommendations",
            "generate_full_report"
        ]
    
    async def execute(self, task: str, params: Dict[str, Any]) -> AgentResult:
        """Execute report generation task"""
        if task not in self.supported_tasks:
            return self.create_result(
                "failed",
                task,
                {},
                [f"Unsupported task: {task}"]
            )
        
        # Route to appropriate method
        if task == "generate_executive_summary":
            result = await self._generate_executive_summary(params)
        elif task == "generate_technical_report":
            result = await self._generate_technical_report(params)
        elif task == "generate_poc_documentation":
            result = await self._generate_poc_documentation(params)
        elif task == "generate_recommendations":
            result = await self._generate_recommendations(params)
        elif task == "generate_full_report":
            result = await self._generate_full_report(params)
        else:
            result = self.create_result("failed", task, {}, ["Unknown task"])
        
        self.store_result(result)
        return result
    
    async def _generate_executive_summary(self, params: Dict[str, Any]) -> AgentResult:
        """Generate executive summary"""
        findings = params.get("findings", [])
        scope = params.get("scope", "")
        
        prompt = f"""
Scope: {scope}
Number of Findings: {len(findings)}

Task: Generate an executive summary for a security assessment report.

Include:
1. Assessment Overview
2. Scope and Methodology
3. Key Findings Summary
4. Risk Assessment
5. High-Level Recommendations
6. Conclusion

Keep it concise, non-technical, suitable for executives.
Educational simulation context.
"""
        
        response = await route_request(
            ModelType.STRATEGIST,
            prompt,
            temperature=0.5,
            max_tokens=1500
        )
        
        return self.create_result(
            "success",
            "generate_executive_summary",
            {
                "summary": response,
                "scope": scope,
                "finding_count": len(findings),
                "generated_at": datetime.utcnow().isoformat()
            },
            ["Executive summary generated"]
        )
    
    async def _generate_technical_report(self, params: Dict[str, Any]) -> AgentResult:
        """Generate detailed technical report"""
        findings = params.get("findings", [])
        methodology = params.get("methodology", "")
        
        prompt = f"""
Methodology: {methodology}
Findings Count: {len(findings)}

Task: Generate a detailed technical security assessment report.

Structure:
1. Introduction
2. Methodology and Approach
3. Detailed Findings
   - For each finding: Description, Impact, Evidence, Recommendation
4. Technical Analysis
5. Risk Matrix
6. Remediation Priority

Technical audience. Educational simulation.
"""
        
        response = await route_request(
            ModelType.EXECUTOR,
            prompt,
            temperature=0.4,
            max_tokens=3000
        )
        
        return self.create_result(
            "success",
            "generate_technical_report",
            {
                "report": response,
                "findings": findings,
                "generated_at": datetime.utcnow().isoformat()
            },
            ["Technical report generated"]
        )
    
    async def _generate_poc_documentation(self, params: Dict[str, Any]) -> AgentResult:
        """Generate PoC documentation"""
        vulnerability = params.get("vulnerability", "")
        description = params.get("description", "")
        
        prompt = f"""
Vulnerability: {vulnerability}
Description: {description}

Task: Generate safe, educational PoC documentation.

Include:
1. Vulnerability Overview
2. Conceptual Proof of Concept (Safe)
3. Step-by-Step Educational Walkthrough
4. Code Snippets (Educational, Non-Exploitative)
5. Detection Methods
6. Mitigation Strategies
7. References

IMPORTANT: Focus on education, not exploitation. Safe simulation only.
"""
        
        response = await route_request(
            ModelType.EXECUTOR,
            prompt,
            temperature=0.3,
            max_tokens=2000
        )
        
        return self.create_result(
            "success",
            "generate_poc_documentation",
            {
                "poc": response,
                "vulnerability": vulnerability,
                "safe": True,
                "generated_at": datetime.utcnow().isoformat()
            },
            ["Safe PoC documentation generated"]
        )
    
    async def _generate_recommendations(self, params: Dict[str, Any]) -> AgentResult:
        """Generate security recommendations"""
        findings = params.get("findings", [])
        priority = params.get("priority", "all")
        
        prompt = f"""
Number of Findings: {len(findings)}
Priority Filter: {priority}

Task: Generate prioritized security recommendations.

Structure:
1. Critical Recommendations (Immediate Action Required)
2. High Priority Recommendations
3. Medium Priority Recommendations
4. Long-term Security Improvements
5. Best Practices

For each recommendation:
- Issue addressed
- Recommended action
- Implementation complexity
- Expected impact

Educational context.
"""
        
        response = await route_request(
            ModelType.STRATEGIST,
            prompt,
            temperature=0.5,
            max_tokens=2000
        )
        
        return self.create_result(
            "success",
            "generate_recommendations",
            {
                "recommendations": response,
                "priority": priority,
                "generated_at": datetime.utcnow().isoformat()
            },
            ["Security recommendations generated"]
        )
    
    async def _generate_full_report(self, params: Dict[str, Any]) -> AgentResult:
        """Generate comprehensive full report"""
        scope = params.get("scope", "")
        findings = params.get("findings", [])
        methodology = params.get("methodology", "")
        
        # Generate all components
        exec_summary = await self._generate_executive_summary(params)
        tech_report = await self._generate_technical_report(params)
        recommendations = await self._generate_recommendations(params)
        
        # Compile full report
        full_report = f"""
# PRATIGHAT.AI Security Assessment Report
**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

---

## Executive Summary

{exec_summary.data.get('summary', '')}

---

## Technical Report

{tech_report.data.get('report', '')}

---

## Recommendations

{recommendations.data.get('recommendations', '')}

---

## Appendix

### Methodology
{methodology}

### Scope
{scope}

### Disclaimer
This report is generated for educational and authorized testing purposes only.
All findings are simulations for learning and training objectives.

---

*Report generated by PRATIGHAT.AI v1.0.0*
*Autonomous Red-Team Intelligence Engine*
*Made in India 🇮🇳*
"""
        
        return self.create_result(
            "success",
            "generate_full_report",
            {
                "full_report": full_report,
                "components": {
                    "executive_summary": exec_summary.data,
                    "technical_report": tech_report.data,
                    "recommendations": recommendations.data
                },
                "generated_at": datetime.utcnow().isoformat()
            },
            ["Full report generated", "All components compiled"]
        )
    
    async def explain(self, result: AgentResult) -> str:
        """Generate human-readable explanation"""
        task = result.task
        data = result.data
        
        explanation = f"""
[Report Agent Result]

Task: {task}
Status: {result.status}
Generated: {data.get('generated_at', 'N/A')}

"""
        
        if task == "generate_full_report":
            explanation += "Full Report Components:\n"
            explanation += "  • Executive Summary\n"
            explanation += "  • Technical Report\n"
            explanation += "  • Recommendations\n\n"
            explanation += "Full report available in data['full_report']"
        else:
            explanation += f"Report component '{task}' generated successfully.\n"
            explanation += f"Available in data['{list(data.keys())[0]}']"
        
        explanation += f"\n\nInsights:\n"
        for insight in result.insights:
            explanation += f"  • {insight}\n"
        
        return explanation
