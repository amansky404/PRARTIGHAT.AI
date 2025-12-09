"""
PRATIGHAT.AI Base Agent

Base class for all specialized agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

from core.memory import get_memory_engine, MemoryEntry


@dataclass
class AgentResult:
    """Standardized agent result"""
    status: str  # success, failed, partial
    agent: str
    task: str
    data: Dict[str, Any]
    insights: List[str]
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "status": self.status,
            "agent": self.agent,
            "task": self.task,
            "data": self.data,
            "insights": self.insights,
            "timestamp": self.timestamp
        }


class BaseAgent(ABC):
    """
    Base Agent Class
    
    All specialized agents inherit from this class and implement
    the required methods for task execution, memory storage, and explanation.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.memory = get_memory_engine()
        self.task_history: List[Dict[str, Any]] = []
    
    @abstractmethod
    async def execute(self, task: str, params: Dict[str, Any]) -> AgentResult:
        """
        Execute a task
        
        Args:
            task: Task identifier
            params: Task parameters
            
        Returns:
            Agent result
        """
        pass
    
    def store_result(self, result: AgentResult) -> None:
        """
        Store result in memory
        
        Args:
            result: Result to store
        """
        entry = MemoryEntry(
            agent=result.agent,
            task=result.task,
            data=result.data,
            insights=result.insights
        )
        self.memory.store_entry(entry)
        self.task_history.append(result.to_dict())
    
    @abstractmethod
    async def explain(self, result: AgentResult) -> str:
        """
        Generate human-readable explanation of result
        
        Args:
            result: Result to explain
            
        Returns:
            Human-readable explanation
        """
        pass
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get task history
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of historical results
        """
        return self.task_history[-limit:]
    
    async def validate_params(self, task: str, params: Dict[str, Any]) -> bool:
        """
        Validate task parameters
        
        Args:
            task: Task identifier
            params: Parameters to validate
            
        Returns:
            True if valid
        """
        # Override in subclasses for specific validation
        return True
    
    def create_result(
        self,
        status: str,
        task: str,
        data: Dict[str, Any],
        insights: List[str]
    ) -> AgentResult:
        """
        Create a standardized result
        
        Args:
            status: Result status
            task: Task identifier
            data: Result data
            insights: Key insights
            
        Returns:
            Agent result
        """
        return AgentResult(
            status=status,
            agent=self.name,
            task=task,
            data=data,
            insights=insights
        )


class AgentCoordinator:
    """
    Agent Coordinator
    
    Manages agent lifecycle and inter-agent communication.
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.event_bus: List[Dict[str, Any]] = []
    
    def register(self, agent: BaseAgent) -> None:
        """Register an agent"""
        self.agents[agent.name] = agent
    
    def unregister(self, agent_name: str) -> None:
        """Unregister an agent"""
        if agent_name in self.agents:
            del self.agents[agent_name]
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get an agent by name"""
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[str]:
        """List all registered agents"""
        return list(self.agents.keys())
    
    async def broadcast_event(self, event: Dict[str, Any]) -> None:
        """
        Broadcast event to all agents
        
        Args:
            event: Event data
        """
        self.event_bus.append({
            "timestamp": datetime.utcnow().isoformat(),
            **event
        })
    
    def get_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events from event bus"""
        return self.event_bus[-limit:]


# Global coordinator
_coordinator: Optional[AgentCoordinator] = None


def get_coordinator() -> AgentCoordinator:
    """Get global agent coordinator"""
    global _coordinator
    if _coordinator is None:
        _coordinator = AgentCoordinator()
    return _coordinator
