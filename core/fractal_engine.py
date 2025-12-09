"""
Fractal Enumeration Engine (FEE)

Advanced enumeration using fractal/recursive discovery patterns
for deep reconnaissance and attack surface mapping.
"""

from typing import Dict, Any, List, Set, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import math


class EnumerationStrategy(Enum):
    """Enumeration strategy types"""
    BREADTH_FIRST = "breadth_first"
    DEPTH_FIRST = "depth_first"
    ADAPTIVE = "adaptive"
    PRIORITY_BASED = "priority_based"


@dataclass
class EnumerationNode:
    """Represents a node in the enumeration tree"""
    value: str
    depth: int
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    score: float = 0.0
    visited: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class FractalEnumerationEngine:
    """
    Fractal Enumeration Engine for deep recursive discovery
    
    Uses fractal patterns and adaptive algorithms to discover:
    - Hidden directories
    - Subdomains
    - Endpoints
    - Parameters
    - Attack surface elements
    """
    
    def __init__(self):
        self.max_depth = 10
        self.max_branches = 5
        self.entropy_threshold = 0.3
        self.strategy = EnumerationStrategy.ADAPTIVE
        self.nodes: Dict[str, EnumerationNode] = {}
        self.visited: Set[str] = set()
    
    async def enumerate(
        self,
        seed: str,
        expander: Callable,
        scorer: Optional[Callable] = None,
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Perform fractal enumeration starting from seed
        
        Args:
            seed: Starting point for enumeration
            expander: Function that expands a node to children
            scorer: Optional function to score node importance
            max_depth: Maximum recursion depth
            
        Returns:
            Enumeration results with discovered nodes
        """
        if max_depth:
            self.max_depth = max_depth
        
        # Initialize root node
        root = EnumerationNode(
            value=seed,
            depth=0,
            score=1.0
        )
        self.nodes[seed] = root
        
        # Enumeration queue
        queue = [root]
        results = {
            "seed": seed,
            "discovered": [],
            "tree": {},
            "statistics": {
                "total_nodes": 0,
                "max_depth_reached": 0,
                "branches_explored": 0
            }
        }
        
        while queue:
            # Select next node based on strategy
            current = self._select_next_node(queue)
            
            if not current or current.depth >= self.max_depth:
                continue
            
            # Mark as visited
            current.visited = True
            self.visited.add(current.value)
            
            # Expand node
            try:
                children = await expander(current.value, current.depth)
                
                if not children:
                    continue
                
                # Rank children
                ranked_children = self._rank_children(
                    children,
                    current,
                    scorer
                )
                
                # Select top branches based on adaptive limit
                branch_limit = self._adaptive_branch_limit(
                    current.depth,
                    len(children)
                )
                selected_children = ranked_children[:branch_limit]
                
                # Create child nodes
                for child_value, child_score in selected_children:
                    if child_value not in self.visited:
                        child_node = EnumerationNode(
                            value=child_value,
                            depth=current.depth + 1,
                            parent=current.value,
                            score=child_score
                        )
                        
                        self.nodes[child_value] = child_node
                        current.children.append(child_value)
                        queue.append(child_node)
                        
                        results["discovered"].append({
                            "value": child_value,
                            "depth": child_node.depth,
                            "score": child_score,
                            "parent": current.value
                        })
                
                # Update statistics
                results["statistics"]["branches_explored"] += len(selected_children)
                results["statistics"]["max_depth_reached"] = max(
                    results["statistics"]["max_depth_reached"],
                    current.depth + 1
                )
                
            except Exception as e:
                # Log error but continue enumeration
                current.metadata["error"] = str(e)
        
        results["statistics"]["total_nodes"] = len(self.nodes)
        results["tree"] = self._build_tree()
        
        return results
    
    def _select_next_node(self, queue: List[EnumerationNode]) -> Optional[EnumerationNode]:
        """Select next node to process based on strategy"""
        if not queue:
            return None
        
        if self.strategy == EnumerationStrategy.BREADTH_FIRST:
            return queue.pop(0)
        
        elif self.strategy == EnumerationStrategy.DEPTH_FIRST:
            return queue.pop()
        
        elif self.strategy == EnumerationStrategy.PRIORITY_BASED:
            # Select highest scored node
            queue.sort(key=lambda n: n.score, reverse=True)
            return queue.pop(0)
        
        elif self.strategy == EnumerationStrategy.ADAPTIVE:
            # Adaptive selection based on depth and score
            if len(queue) < 10:
                return queue.pop(0)  # Breadth-first for small queues
            else:
                # Priority-based for large queues
                queue.sort(key=lambda n: n.score * (1.0 / (n.depth + 1)), reverse=True)
                return queue.pop(0)
        
        return queue.pop(0)
    
    def _rank_children(
        self,
        children: List[str],
        parent: EnumerationNode,
        scorer: Optional[Callable]
    ) -> List[tuple]:
        """Rank children by importance/probability"""
        ranked = []
        
        for child in children:
            if scorer:
                score = scorer(child, parent)
            else:
                # Default scoring based on entropy and patterns
                score = self._default_score(child, parent)
            
            ranked.append((child, score))
        
        # Sort by score descending
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        return ranked
    
    def _default_score(self, child: str, parent: EnumerationNode) -> float:
        """Default scoring function"""
        score = 0.5
        
        # Prefer certain patterns
        interesting_patterns = [
            "admin", "api", "v1", "v2", "test", "dev", "staging",
            "backup", "old", "tmp", "config", "user", "account"
        ]
        
        child_lower = child.lower()
        for pattern in interesting_patterns:
            if pattern in child_lower:
                score += 0.2
        
        # Penalize very long or very short names
        if len(child) < 3 or len(child) > 50:
            score -= 0.1
        
        # Consider parent score
        score = score * 0.7 + parent.score * 0.3
        
        return max(0.0, min(1.0, score))
    
    def _adaptive_branch_limit(self, depth: int, num_children: int) -> int:
        """Calculate adaptive branch limit based on depth and children count"""
        # Reduce branches as we go deeper
        base_limit = self.max_branches
        depth_factor = max(0.3, 1.0 - (depth * 0.15))
        adjusted_limit = int(base_limit * depth_factor)
        
        # Ensure at least 1 branch
        return max(1, min(adjusted_limit, num_children))
    
    def _calculate_entropy(self, children: List[str]) -> float:
        """Calculate entropy of child distribution"""
        if not children:
            return 0.0
        
        # Simple entropy calculation
        unique_patterns = len(set(children))
        total = len(children)
        
        if total == 0:
            return 0.0
        
        ratio = unique_patterns / total
        entropy = -ratio * math.log2(ratio) if ratio > 0 else 0.0
        
        return entropy
    
    def _build_tree(self) -> Dict[str, Any]:
        """Build tree representation of enumeration"""
        tree = {}
        
        for value, node in self.nodes.items():
            tree[value] = {
                "depth": node.depth,
                "parent": node.parent,
                "children": node.children,
                "score": node.score,
                "visited": node.visited,
                "metadata": node.metadata
            }
        
        return tree
    
    def get_all_discovered(self) -> List[str]:
        """Get all discovered values"""
        return list(self.nodes.keys())
    
    def get_by_depth(self, depth: int) -> List[str]:
        """Get all nodes at specific depth"""
        return [
            value for value, node in self.nodes.items()
            if node.depth == depth
        ]
    
    def get_leaf_nodes(self) -> List[str]:
        """Get all leaf nodes (no children)"""
        return [
            value for value, node in self.nodes.items()
            if not node.children
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get enumeration statistics"""
        depths = [node.depth for node in self.nodes.values()]
        
        return {
            "total_nodes": len(self.nodes),
            "max_depth": max(depths) if depths else 0,
            "avg_depth": sum(depths) / len(depths) if depths else 0,
            "leaf_nodes": len(self.get_leaf_nodes()),
            "branching_factor": len(self.nodes) / max(1, len(self.visited))
        }
    
    def reset(self):
        """Reset enumeration state"""
        self.nodes.clear()
        self.visited.clear()


# Singleton instance
_fee = None


def get_fractal_engine() -> FractalEnumerationEngine:
    """Get the global Fractal Enumeration Engine instance"""
    global _fee
    if _fee is None:
        _fee = FractalEnumerationEngine()
    return _fee
