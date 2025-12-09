"""
Genetic Exploit Evolution Engine (GEEE)

Uses genetic algorithm concepts to evolve SAFE proof-of-concept
templates for educational purposes only.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import random
import copy


class MutationType(Enum):
    """Types of mutations that can occur"""
    BOUNDARY_EXPANSION = "boundary_expansion"
    ENCODING_VARIATION = "encoding_variation"
    LOGIC_BRANCH = "logic_branch"
    PARAMETER_SWAP = "parameter_swap"
    STRUCTURE_VARIATION = "structure_variation"


@dataclass
class PoCIndividual:
    """Represents a proof-of-concept individual in the population"""
    template: str
    genes: Dict[str, Any]
    fitness: float = 0.0
    generation: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class GeneticExploitEvolutionEngine:
    """
    Genetic Exploit Evolution Engine for safe PoC template generation
    
    IMPORTANT: This engine only creates SAFE, EDUCATIONAL templates.
    No real exploits are generated.
    
    Uses genetic algorithm principles:
    - Selection
    - Crossover
    - Mutation
    - Fitness evaluation
    """
    
    def __init__(self):
        self.population_size = 20
        self.generations = 10
        self.mutation_rate = 0.3
        self.crossover_rate = 0.7
        self.elitism_count = 2
        self.current_generation = 0
    
    async def evolve_poc(
        self,
        seed_template: str,
        fitness_function: Callable,
        target_fitness: float = 0.9,
        max_generations: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Evolve a safe PoC template using genetic algorithms
        
        Args:
            seed_template: Initial template to evolve from
            fitness_function: Function to evaluate fitness (0.0 to 1.0)
            target_fitness: Target fitness to reach
            max_generations: Maximum generations to evolve
            
        Returns:
            Evolution results with best individual
        """
        if max_generations:
            self.generations = max_generations
        
        # Initialize population
        population = self._initialize_population(seed_template)
        
        best_individual = None
        evolution_history = []
        
        for generation in range(self.generations):
            self.current_generation = generation
            
            # Evaluate fitness
            for individual in population:
                individual.fitness = await fitness_function(individual)
            
            # Sort by fitness
            population.sort(key=lambda x: x.fitness, reverse=True)
            
            # Track best
            if not best_individual or population[0].fitness > best_individual.fitness:
                best_individual = copy.deepcopy(population[0])
            
            # Record generation stats
            evolution_history.append({
                "generation": generation,
                "best_fitness": population[0].fitness,
                "avg_fitness": sum(ind.fitness for ind in population) / len(population),
                "worst_fitness": population[-1].fitness
            })
            
            # Check if target reached
            if population[0].fitness >= target_fitness:
                break
            
            # Create next generation
            new_population = []
            
            # Elitism - keep best individuals
            new_population.extend(population[:self.elitism_count])
            
            # Generate rest through selection, crossover, and mutation
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self._select_parent(population)
                parent2 = self._select_parent(population)
                
                # Crossover
                if random.random() < self.crossover_rate:
                    child = self._crossover(parent1, parent2)
                else:
                    child = copy.deepcopy(parent1)
                
                # Mutation
                if random.random() < self.mutation_rate:
                    child = self._mutate(child)
                
                child.generation = generation + 1
                new_population.append(child)
            
            population = new_population
        
        result = {
            "success": True,
            "best_individual": {
                "template": best_individual.template,
                "fitness": best_individual.fitness,
                "generation": best_individual.generation,
                "genes": best_individual.genes
            },
            "evolution_history": evolution_history,
            "final_generation": self.current_generation,
            "convergence_reached": best_individual.fitness >= target_fitness,
            "is_educational": True,
            "disclaimer": "This is a SAFE educational template only"
        }
        
        return result
    
    def _initialize_population(self, seed_template: str) -> List[PoCIndividual]:
        """Initialize population with variations of seed"""
        population = []
        
        # Add seed as-is
        seed_individual = PoCIndividual(
            template=seed_template,
            genes=self._extract_genes(seed_template),
            generation=0
        )
        population.append(seed_individual)
        
        # Create variations
        for i in range(self.population_size - 1):
            variant = copy.deepcopy(seed_individual)
            variant = self._mutate(variant)
            population.append(variant)
        
        return population
    
    def _extract_genes(self, template: str) -> Dict[str, Any]:
        """Extract gene information from template"""
        # Educational genes only
        genes = {
            "structure": "safe_educational",
            "encoding": "standard",
            "complexity": len(template),
            "patterns": [],
            "safety_level": "maximum"
        }
        
        # Identify patterns (educational)
        educational_patterns = [
            "input_validation",
            "output_encoding",
            "parameterized_query",
            "safe_api_call",
            "security_header"
        ]
        
        template_lower = template.lower()
        for pattern in educational_patterns:
            if pattern.replace("_", " ") in template_lower:
                genes["patterns"].append(pattern)
        
        return genes
    
    def _select_parent(self, population: List[PoCIndividual]) -> PoCIndividual:
        """Select parent using tournament selection"""
        tournament_size = 3
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: x.fitness)
    
    def _crossover(
        self,
        parent1: PoCIndividual,
        parent2: PoCIndividual
    ) -> PoCIndividual:
        """Perform crossover between two parents"""
        # Educational crossover - combine best aspects
        child_genes = {}
        
        for key in parent1.genes:
            if random.random() < 0.5:
                child_genes[key] = parent1.genes[key]
            else:
                child_genes[key] = parent2.genes.get(key, parent1.genes[key])
        
        # Combine templates (educational)
        child_template = self._combine_templates(parent1.template, parent2.template)
        
        child = PoCIndividual(
            template=child_template,
            genes=child_genes,
            generation=max(parent1.generation, parent2.generation)
        )
        
        return child
    
    def _combine_templates(self, template1: str, template2: str) -> str:
        """Combine two templates (educational)"""
        # Simple combination - take sections from each
        lines1 = template1.split('\n')
        lines2 = template2.split('\n')
        
        combined = []
        max_len = max(len(lines1), len(lines2))
        
        for i in range(max_len):
            if random.random() < 0.5 and i < len(lines1):
                combined.append(lines1[i])
            elif i < len(lines2):
                combined.append(lines2[i])
        
        return '\n'.join(combined)
    
    def _mutate(self, individual: PoCIndividual) -> PoCIndividual:
        """Apply mutation to individual"""
        # Choose random mutation type
        mutation_types = list(MutationType)
        mutation = random.choice(mutation_types)
        
        mutated = copy.deepcopy(individual)
        
        if mutation == MutationType.BOUNDARY_EXPANSION:
            mutated.template += "\n# Additional boundary check (educational)"
            mutated.genes["complexity"] += 10
        
        elif mutation == MutationType.ENCODING_VARIATION:
            mutated.template += "\n# Encoding variation example (safe)"
            mutated.genes["encoding"] = "varied"
        
        elif mutation == MutationType.LOGIC_BRANCH:
            mutated.template += "\n# Alternative logic branch (educational)"
            mutated.genes["complexity"] += 5
        
        elif mutation == MutationType.PARAMETER_SWAP:
            mutated.template += "\n# Parameter variation (safe)"
            mutated.genes["patterns"].append("parameter_variation")
        
        elif mutation == MutationType.STRUCTURE_VARIATION:
            mutated.template += "\n# Structural variation (educational)"
            mutated.genes["structure"] = "varied_safe"
        
        mutated.metadata["mutation"] = mutation.value
        
        return mutated
    
    async def default_fitness(self, individual: PoCIndividual) -> float:
        """
        Default fitness function for educational PoCs
        
        Args:
            individual: Individual to evaluate
            
        Returns:
            Fitness score (0.0 to 1.0)
        """
        score = 0.0
        
        # Accuracy - check for educational keywords
        educational_keywords = [
            "educational", "safe", "simulation", "example",
            "concept", "learning", "authorized"
        ]
        template_lower = individual.template.lower()
        
        keyword_count = sum(1 for kw in educational_keywords if kw in template_lower)
        score += min(0.4, keyword_count * 0.1)
        
        # Relevance - check for security concepts
        security_concepts = [
            "validation", "encoding", "sanitization", "parameterized",
            "security", "protection", "defense"
        ]
        
        concept_count = sum(1 for concept in security_concepts if concept in template_lower)
        score += min(0.4, concept_count * 0.1)
        
        # Diversity - check gene patterns
        pattern_count = len(individual.genes.get("patterns", []))
        score += min(0.2, pattern_count * 0.05)
        
        return min(1.0, score)
    
    def get_statistics(self, evolution_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get evolution statistics"""
        if not evolution_history:
            return {}
        
        best_fitnesses = [gen["best_fitness"] for gen in evolution_history]
        avg_fitnesses = [gen["avg_fitness"] for gen in evolution_history]
        
        return {
            "total_generations": len(evolution_history),
            "final_best_fitness": best_fitnesses[-1],
            "improvement": best_fitnesses[-1] - best_fitnesses[0],
            "avg_improvement_per_gen": (best_fitnesses[-1] - best_fitnesses[0]) / len(evolution_history),
            "convergence_speed": self._calculate_convergence_speed(best_fitnesses)
        }
    
    def _calculate_convergence_speed(self, fitness_history: List[float]) -> str:
        """Calculate how fast the algorithm converged"""
        if len(fitness_history) < 2:
            return "unknown"
        
        # Calculate rate of improvement
        improvements = [
            fitness_history[i+1] - fitness_history[i]
            for i in range(len(fitness_history) - 1)
        ]
        
        avg_improvement = sum(improvements) / len(improvements)
        
        if avg_improvement > 0.1:
            return "fast"
        elif avg_improvement > 0.05:
            return "moderate"
        else:
            return "slow"


# Singleton instance
_geee = None


def get_genetic_engine() -> GeneticExploitEvolutionEngine:
    """Get the global Genetic Exploit Evolution Engine instance"""
    global _geee
    if _geee is None:
        _geee = GeneticExploitEvolutionEngine()
    return _geee
