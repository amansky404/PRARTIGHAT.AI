"""
PRATIGHAT-CORE (Central Brain)

The cognitive reasoning engine that coordinates all agents,
manages decision-making, and orchestrates the entire system.
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio

from core.config import get_config, ModelType, OperationalMode
from core.routing import route_request, get_router
from core.jailbreak import get_rewriter
from core.memory import get_memory_engine, MemoryEntry


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task:
    """Task representation for agent execution"""
    
    def __init__(
        self,
        task_id: str,
        agent: str,
        action: str,
        params: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL
    ):
        self.task_id = task_id
        self.agent = agent
        self.action = action
        self.params = params
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.result: Optional[Any] = None
        self.error: Optional[str] = None


class PRAtighatCore:
    """
    PRATIGHAT-CORE: Central Cognitive Engine
    
    Responsibilities:
    - Strategic reasoning and decision-making
    - Multi-agent coordination
    - Task scheduling and execution
    - Memory management
    - Recursive hypothesis testing
    """
    
    def __init__(self):
        self.config = get_config()
        self.router = get_router()
        self.rewriter = get_rewriter()
        self.memory = get_memory_engine()
        
        self.agents: Dict[str, Any] = {}
        self.task_queue: List[Task] = []
        self.active_tasks: Dict[str, Task] = {}
    
    def register_agent(self, name: str, agent: Any) -> None:
        """Register an agent with the core"""
        self.agents[name] = agent
    
    async def strategic_reason(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Perform strategic reasoning on a query
        
        Args:
            query: User query or problem
            context: Additional context
            
        Returns:
            Strategic analysis and plan
        """
        # Rewrite for safety
        safe_query = await self.rewriter.rewrite_for_safety(query)
        
        # Build context from memory if needed
        if context:
            relevant_memories = self.memory.get_entries(limit=10)
            context_str = self._build_context_string(relevant_memories)
        else:
            context_str = ""
        
        # System prompt for strategic reasoning
        system_prompt = """You are PRATIGHAT-CORE, the strategic reasoning engine of an 
educational cybersecurity platform. Your role is to:

1. Analyze security scenarios from a red-team perspective (simulation only)
2. Break down complex problems into actionable steps
3. Identify potential attack vectors (for educational purposes)
4. Suggest safe, ethical approaches to testing
5. Provide clear, technical explanations

Always emphasize that this is for authorized testing and learning only.
Focus on conceptual understanding and safe simulation methods."""
        
        full_prompt = f"""{context_str}

Query: {safe_query}

Provide a strategic analysis with:
1. Problem understanding
2. Key considerations
3. Recommended approach (simulation-safe)
4. Potential risks and mitigations
5. Learning objectives
"""
        
        response = await route_request(
            ModelType.STRATEGIST,
            full_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=2000
        )
        
        # Store reasoning in memory
        self.memory.store_entry(MemoryEntry(
            agent="core",
            task="strategic_reasoning",
            data={"query": query, "response": response},
            insights=["Strategic analysis completed"]
        ))
        
        return response
    
    async def decompose_task(
        self,
        objective: str
    ) -> List[Task]:
        """
        Decompose high-level objective into tasks for agents
        
        Args:
            objective: High-level objective
            
        Returns:
            List of tasks for agent execution
            
        Note: This is a placeholder for future LLM-powered task decomposition.
        In production, this would parse LLM output and create Task objects.
        """
        decomposition_prompt = f"""
Objective: {objective}

Break this down into specific tasks that can be executed by specialized agents:
- Recon Agent: Host discovery, port scanning, service enumeration
- Exploit Agent: Safe PoC generation, vulnerability simulation
- Chain Agent: Attack path prediction, lateral movement analysis
- Pattern Agent: Pattern detection, fingerprinting
- Bypass Agent: Fuzzing, bypass strategy simulation
- Report Agent: Documentation, reporting

For each task, specify:
1. Agent name
2. Action to perform
3. Parameters needed
4. Priority (LOW, NORMAL, HIGH, CRITICAL)

Format as JSON list of tasks.
"""
        
        # TODO: Implement JSON parsing and Task object creation
        # This would require LLM to be available and proper JSON parsing
        # For now, return empty list - agents can be called directly
        
        # Example of what this should return:
        # tasks = []
        # response = await route_request(ModelType.STRATEGIST, decomposition_prompt, ...)
        # parsed = json.loads(response)
        # for task_data in parsed:
        #     tasks.append(Task(...))
        # return tasks
        
        return []
    
    def _build_context_string(self, memories: List[MemoryEntry]) -> str:
        """Build context string from memory entries"""
        if not memories:
            return ""
        
        context_parts = ["Recent context from memory:"]
        for entry in memories:
            context_parts.append(
                f"- [{entry.agent}] {entry.task}: {str(entry.data)[:100]}..."
            )
        
        return "\n".join(context_parts)
    
    async def execute_task(self, task: Task) -> Any:
        """
        Execute a task using the appropriate agent
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
        """
        task.status = TaskStatus.RUNNING
        self.active_tasks[task.task_id] = task
        
        try:
            # Get the agent
            agent = self.agents.get(task.agent)
            if not agent:
                raise ValueError(f"Agent '{task.agent}' not found")
            
            # Check operational mode
            if self.config.operational_mode == OperationalMode.ASSISTED:
                # In assisted mode, would ask for user approval
                # For now, proceed automatically
                pass
            
            # Execute the task
            result = await agent.execute(task.action, task.params)
            
            task.status = TaskStatus.COMPLETED
            task.result = result
            
            # Store in memory
            self.memory.store_entry(MemoryEntry(
                agent=task.agent,
                task=task.action,
                data={"params": task.params, "result": result},
                insights=[]
            ))
            
            return result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            raise
        
        finally:
            if task.task_id in self.active_tasks:
                del self.active_tasks[task.task_id]
    
    async def coordinate_agents(
        self,
        objective: str
    ) -> Dict[str, Any]:
        """
        Coordinate multiple agents to achieve an objective
        
        Args:
            objective: High-level objective
            
        Returns:
            Aggregated results from all agents
        """
        # Strategic reasoning first
        strategy = await self.strategic_reason(objective)
        
        # Decompose into tasks
        tasks = await self.decompose_task(objective)
        
        # Sort by priority
        tasks.sort(key=lambda t: t.priority.value, reverse=True)
        
        # Execute tasks
        results = {}
        for task in tasks:
            try:
                result = await self.execute_task(task)
                results[task.task_id] = {
                    "agent": task.agent,
                    "action": task.action,
                    "status": "success",
                    "result": result
                }
            except Exception as e:
                results[task.task_id] = {
                    "agent": task.agent,
                    "action": task.action,
                    "status": "failed",
                    "error": str(e)
                }
        
        return {
            "objective": objective,
            "strategy": strategy,
            "tasks": results
        }
    
    async def recursive_reasoning(
        self,
        hypothesis: str,
        max_depth: int = 3,
        current_depth: int = 0
    ) -> Dict[str, Any]:
        """
        Perform recursive hypothesis testing
        
        Args:
            hypothesis: Initial hypothesis
            max_depth: Maximum recursion depth
            current_depth: Current depth (internal)
            
        Returns:
            Reasoning tree
        """
        if current_depth >= max_depth:
            return {"hypothesis": hypothesis, "depth": current_depth, "children": []}
        
        # Analyze hypothesis
        analysis_prompt = f"""
Hypothesis: {hypothesis}

Analyze this hypothesis and:
1. Validate assumptions
2. Identify sub-hypotheses or questions
3. Suggest next investigation steps

Provide 2-3 specific sub-hypotheses to explore.
"""
        
        response = await route_request(
            ModelType.STRATEGIST,
            analysis_prompt,
            temperature=0.6,
            max_tokens=1000
        )
        
        # In production, would parse sub-hypotheses and recurse
        # For now, return simplified tree
        return {
            "hypothesis": hypothesis,
            "depth": current_depth,
            "analysis": response,
            "children": []
        }
    
    async def process_query(
        self,
        query: str,
        mode: Optional[str] = None
    ) -> str:
        """
        Main entry point for processing user queries
        
        Args:
            query: User query
            mode: Optional processing mode override
            
        Returns:
            Processed response
        """
        # Safety check
        if self.rewriter.detect_harmful_intent(query):
            return (
                "This request appears to have harmful intent. "
                "PRATIGHAT-AI is designed for educational and authorized "
                "research purposes only. Please reformulate your query "
                "with safety and ethics in mind."
            )
        
        # Enforce simulation mode
        query = self.rewriter.enforce_simulation_mode(query)
        
        # Strategic reasoning
        response = await self.strategic_reason(query)
        
        return response


# Global core instance
_core: Optional[PRAtighatCore] = None


def get_core() -> PRAtighatCore:
    """Get global PRATIGHAT-CORE instance"""
    global _core
    if _core is None:
        _core = PRAtighatCore()
    return _core
