"""
Quantum Attack Path Prediction Engine (QHAPE)

Predicts attack paths using graph theory, heuristics, and probability
modeling for educational and defensive planning purposes.
"""

from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math


class NodeType(Enum):
    """Types of nodes in attack graph"""
    EXTERNAL = "external"
    PERIMETER = "perimeter"
    DMZ = "dmz"
    INTERNAL = "internal"
    CRITICAL = "critical"
    USER = "user"
    ADMIN = "admin"


class EdgeType(Enum):
    """Types of connections between nodes"""
    NETWORK = "network"
    APPLICATION = "application"
    CREDENTIAL = "credential"
    PRIVILEGE = "privilege"
    EXPLOIT = "exploit"


@dataclass
class AttackNode:
    """Represents a node in the attack graph"""
    id: str
    type: NodeType
    exposure: float = 0.5  # 0.0 to 1.0
    weakness: float = 0.5  # 0.0 to 1.0
    controls: float = 0.5  # 0.0 to 1.0
    value: float = 0.5  # 0.0 to 1.0 (attacker value)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttackEdge:
    """Represents an edge in the attack graph"""
    source: str
    target: str
    type: EdgeType
    likelihood: float = 0.5  # 0.0 to 1.0
    difficulty: float = 0.5  # 0.0 to 1.0
    detectability: float = 0.5  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttackPath:
    """Represents a complete attack path"""
    nodes: List[str]
    edges: List[Tuple[str, str]]
    probability: float
    impact: float
    detectability: float
    complexity: float
    risk_score: float


class QuantumAttackPathPredictionEngine:
    """
    Quantum-inspired Attack Path Prediction Engine
    
    Uses:
    - Graph theory for path analysis
    - Heuristic scoring for probability
    - Service correlation analysis
    - Privilege escalation modeling
    
    Educational purposes only - for defensive planning.
    """
    
    def __init__(self):
        self.nodes: Dict[str, AttackNode] = {}
        self.edges: List[AttackEdge] = []
        self.paths: List[AttackPath] = []
    
    def add_node(
        self,
        node_id: str,
        node_type: NodeType,
        exposure: float = 0.5,
        weakness: float = 0.5,
        controls: float = 0.5,
        value: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add a node to the attack graph"""
        node = AttackNode(
            id=node_id,
            type=node_type,
            exposure=exposure,
            weakness=weakness,
            controls=controls,
            value=value,
            metadata=metadata or {}
        )
        self.nodes[node_id] = node
    
    def add_edge(
        self,
        source: str,
        target: str,
        edge_type: EdgeType,
        likelihood: float = 0.5,
        difficulty: float = 0.5,
        detectability: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add an edge to the attack graph"""
        edge = AttackEdge(
            source=source,
            target=target,
            type=edge_type,
            likelihood=likelihood,
            difficulty=difficulty,
            detectability=detectability,
            metadata=metadata or {}
        )
        self.edges.append(edge)
    
    def predict_attack_paths(
        self,
        source_node: str,
        target_node: Optional[str] = None,
        max_paths: int = 10,
        max_depth: int = 10
    ) -> Dict[str, Any]:
        """
        Predict possible attack paths
        
        Args:
            source_node: Starting point (usually external/attacker)
            target_node: Optional target (finds paths to any high-value if None)
            max_paths: Maximum number of paths to return
            max_depth: Maximum path length
            
        Returns:
            Predicted attack paths with risk analysis
        """
        if source_node not in self.nodes:
            return {
                "success": False,
                "error": f"Source node {source_node} not found"
            }
        
        # Find all paths
        if target_node:
            paths = self._find_paths(source_node, target_node, max_depth)
        else:
            # Find paths to high-value targets
            high_value_targets = [
                node_id for node_id, node in self.nodes.items()
                if node.value > 0.7 and node_id != source_node
            ]
            paths = []
            for target in high_value_targets:
                paths.extend(self._find_paths(source_node, target, max_depth))
        
        # Score and rank paths
        scored_paths = []
        for path_nodes in paths:
            attack_path = self._score_path(path_nodes)
            scored_paths.append(attack_path)
        
        # Sort by risk score
        scored_paths.sort(key=lambda p: p.risk_score, reverse=True)
        
        # Limit results
        top_paths = scored_paths[:max_paths]
        
        result = {
            "success": True,
            "source": source_node,
            "target": target_node,
            "paths_found": len(paths),
            "top_paths": [self._path_to_dict(p) for p in top_paths],
            "risk_analysis": self._analyze_risks(top_paths),
            "recommendations": self._generate_recommendations(top_paths),
            "is_educational": True
        }
        
        return result
    
    def _find_paths(
        self,
        source: str,
        target: str,
        max_depth: int,
        current_path: Optional[List[str]] = None,
        visited: Optional[Set[str]] = None
    ) -> List[List[str]]:
        """Find all paths between source and target using DFS"""
        if current_path is None:
            current_path = [source]
        if visited is None:
            visited = {source}
        
        if source == target:
            return [current_path.copy()]
        
        if len(current_path) >= max_depth:
            return []
        
        paths = []
        
        # Find outgoing edges from current node
        for edge in self.edges:
            if edge.source == source and edge.target not in visited:
                visited.add(edge.target)
                current_path.append(edge.target)
                
                # Recursive search
                sub_paths = self._find_paths(
                    edge.target,
                    target,
                    max_depth,
                    current_path,
                    visited
                )
                paths.extend(sub_paths)
                
                # Backtrack
                current_path.pop()
                visited.remove(edge.target)
        
        return paths
    
    def _score_path(self, path_nodes: List[str]) -> AttackPath:
        """Score an attack path"""
        if len(path_nodes) < 2:
            return AttackPath(
                nodes=path_nodes,
                edges=[],
                probability=0.0,
                impact=0.0,
                detectability=0.0,
                complexity=1.0,
                risk_score=0.0
            )
        
        # Calculate path probability
        probability = 1.0
        detectability_sum = 0.0
        path_edges = []
        
        for i in range(len(path_nodes) - 1):
            source = path_nodes[i]
            target = path_nodes[i + 1]
            
            # Find edge
            edge = self._find_edge(source, target)
            if edge:
                # Probability decreases with each step
                node_source = self.nodes[source]
                node_target = self.nodes[target]
                
                # Calculate transition probability
                transition_prob = (
                    node_source.exposure *
                    node_target.weakness *
                    edge.likelihood *
                    (1.0 - node_target.controls)
                )
                
                probability *= transition_prob
                detectability_sum += edge.detectability
                path_edges.append((source, target))
        
        # Calculate impact (value of target node)
        target_node = self.nodes[path_nodes[-1]]
        impact = target_node.value
        
        # Calculate complexity (inverse of path length)
        complexity = 1.0 / len(path_nodes)
        
        # Average detectability
        detectability = detectability_sum / len(path_edges) if path_edges else 0.5
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(
            probability,
            impact,
            detectability,
            complexity
        )
        
        return AttackPath(
            nodes=path_nodes,
            edges=path_edges,
            probability=probability,
            impact=impact,
            detectability=detectability,
            complexity=complexity,
            risk_score=risk_score
        )
    
    def _find_edge(self, source: str, target: str) -> Optional[AttackEdge]:
        """Find edge between two nodes"""
        for edge in self.edges:
            if edge.source == source and edge.target == target:
                return edge
        return None
    
    def _calculate_risk_score(
        self,
        probability: float,
        impact: float,
        detectability: float,
        complexity: float
    ) -> float:
        """Calculate overall risk score"""
        # Risk = Probability * Impact * (1 - Detectability) * (1 + Complexity)
        # Range: 0.0 to ~2.0, normalized to 0.0 to 1.0
        
        risk = (
            probability *
            impact *
            (1.0 - detectability) *
            (1.0 + complexity)
        )
        
        # Normalize to 0-1 range
        normalized_risk = min(1.0, risk / 2.0)
        
        return normalized_risk
    
    def _path_to_dict(self, path: AttackPath) -> Dict[str, Any]:
        """Convert AttackPath to dictionary"""
        return {
            "nodes": path.nodes,
            "path_length": len(path.nodes),
            "probability": round(path.probability, 4),
            "impact": round(path.impact, 4),
            "detectability": round(path.detectability, 4),
            "complexity": round(path.complexity, 4),
            "risk_score": round(path.risk_score, 4),
            "description": self._generate_path_description(path)
        }
    
    def _generate_path_description(self, path: AttackPath) -> str:
        """Generate human-readable path description"""
        if len(path.nodes) < 2:
            return "Invalid path"
        
        descriptions = []
        for i in range(len(path.nodes) - 1):
            source = path.nodes[i]
            target = path.nodes[i + 1]
            edge = self._find_edge(source, target)
            
            descriptions.append(
                f"{source} → {target} (via {edge.type.value if edge else 'unknown'})"
            )
        
        return " → ".join(descriptions)
    
    def _analyze_risks(self, paths: List[AttackPath]) -> Dict[str, Any]:
        """Analyze overall risks from paths"""
        if not paths:
            return {"overall_risk": "low", "analysis": "No paths found"}
        
        avg_probability = sum(p.probability for p in paths) / len(paths)
        max_impact = max(p.impact for p in paths)
        avg_detectability = sum(p.detectability for p in paths) / len(paths)
        
        overall_risk = "low"
        if avg_probability > 0.5 and max_impact > 0.7:
            overall_risk = "critical"
        elif avg_probability > 0.3 or max_impact > 0.6:
            overall_risk = "high"
        elif avg_probability > 0.1 or max_impact > 0.4:
            overall_risk = "medium"
        
        return {
            "overall_risk": overall_risk,
            "avg_probability": round(avg_probability, 4),
            "max_impact": round(max_impact, 4),
            "avg_detectability": round(avg_detectability, 4),
            "total_paths": len(paths)
        }
    
    def _generate_recommendations(self, paths: List[AttackPath]) -> List[str]:
        """Generate security recommendations based on paths"""
        recommendations = []
        
        if not paths:
            return ["No immediate threats identified. Continue monitoring."]
        
        # Analyze common weaknesses
        high_risk_nodes = set()
        for path in paths:
            if path.risk_score > 0.5:
                high_risk_nodes.update(path.nodes)
        
        if high_risk_nodes:
            recommendations.append(
                f"Focus on hardening {len(high_risk_nodes)} high-risk nodes"
            )
        
        # Check detectability
        low_detectability_paths = [p for p in paths if p.detectability < 0.3]
        if low_detectability_paths:
            recommendations.append(
                "Improve detection capabilities - several paths have low detectability"
            )
        
        # Check for common patterns
        recommendations.extend([
            "Implement network segmentation to break attack paths",
            "Apply principle of least privilege",
            "Enable comprehensive logging and monitoring",
            "Conduct regular security assessments",
            "Update and patch all systems regularly"
        ])
        
        return recommendations[:5]  # Limit to top 5
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": self._count_node_types(),
            "edge_types": self._count_edge_types(),
            "avg_node_exposure": self._avg_node_metric("exposure"),
            "avg_node_weakness": self._avg_node_metric("weakness"),
            "avg_node_controls": self._avg_node_metric("controls")
        }
    
    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type"""
        counts = {}
        for node in self.nodes.values():
            type_name = node.type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts
    
    def _count_edge_types(self) -> Dict[str, int]:
        """Count edges by type"""
        counts = {}
        for edge in self.edges:
            type_name = edge.type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts
    
    def _avg_node_metric(self, metric: str) -> float:
        """Calculate average of a node metric"""
        if not self.nodes:
            return 0.0
        
        total = sum(getattr(node, metric) for node in self.nodes.values())
        return total / len(self.nodes)
    
    def reset(self):
        """Reset the engine"""
        self.nodes.clear()
        self.edges.clear()
        self.paths.clear()


# Singleton instance
_qhape = None


def get_quantum_engine() -> QuantumAttackPathPredictionEngine:
    """Get the global Quantum Attack Path Prediction Engine instance"""
    global _qhape
    if _qhape is None:
        _qhape = QuantumAttackPathPredictionEngine()
    return _qhape
