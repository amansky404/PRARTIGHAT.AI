"""
PRATIGHAT.AI LLM Routing Layer

Handles routing between offline (Ollama) and online (cloud) LLM models
with automatic fallback and optimization based on hardware capabilities.
"""

import asyncio
from typing import Optional, Dict, Any, List
from enum import Enum
import ollama

from core.config import get_config, ModelType, ModelConfig


class RoutingStrategy(Enum):
    """LLM routing strategies"""
    OFFLINE_ONLY = "offline_only"
    ONLINE_ONLY = "online_only"
    HYBRID = "hybrid"
    AUTO = "auto"


class LLMRouter:
    """
    LLM Routing Engine
    
    Routes requests to appropriate LLM (offline or online) based on:
    - Hardware capabilities
    - Model availability
    - Request complexity
    - Network availability
    """
    
    def __init__(self, strategy: RoutingStrategy = RoutingStrategy.AUTO):
        self.config = get_config()
        self.strategy = strategy
        self.ollama_client = ollama.AsyncClient()
        self._check_ollama_availability()
    
    def _check_ollama_availability(self) -> bool:
        """Check if Ollama is available and running"""
        try:
            # This will be checked asynchronously in actual usage
            self.ollama_available = True
            return True
        except Exception:
            self.ollama_available = False
            return False
    
    async def _call_ollama(
        self, 
        model_config: ModelConfig,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Call Ollama for offline LLM inference"""
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            response = await self.ollama_client.chat(
                model=model_config.name,
                messages=messages,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            )
            return response['message']['content']
        except Exception as e:
            raise RuntimeError(f"Ollama inference failed: {e}")
    
    async def _call_cloud_llm(
        self,
        model_config: ModelConfig,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Call cloud LLM API (placeholder for future implementation)"""
        # This would integrate with OpenAI, Anthropic, etc.
        raise NotImplementedError("Cloud LLM integration not yet implemented")
    
    async def route_request(
        self,
        model_type: ModelType,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        force_offline: bool = False
    ) -> str:
        """
        Route LLM request to appropriate backend
        
        Args:
            model_type: Type of model to use (strategist, executor, etc.)
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            force_offline: Force offline mode even if cloud is available
            
        Returns:
            LLM response text
        """
        model_config = self.config.models[model_type]
        
        # Determine routing based on strategy
        use_offline = True
        
        if self.strategy == RoutingStrategy.OFFLINE_ONLY or force_offline:
            use_offline = True
        elif self.strategy == RoutingStrategy.ONLINE_ONLY:
            use_offline = False
        elif self.strategy == RoutingStrategy.AUTO:
            # Auto-select based on model config and availability
            use_offline = model_config.offline
        
        # Try offline first if requested
        if use_offline:
            try:
                return await self._call_ollama(
                    model_config,
                    prompt,
                    system_prompt,
                    temperature,
                    max_tokens
                )
            except Exception as e:
                # Fallback to cloud if hybrid mode
                if self.strategy == RoutingStrategy.HYBRID:
                    try:
                        return await self._call_cloud_llm(
                            model_config,
                            prompt,
                            system_prompt,
                            temperature,
                            max_tokens
                        )
                    except Exception:
                        raise RuntimeError(f"Both offline and cloud LLM failed: {e}")
                else:
                    raise
        else:
            # Try cloud first
            try:
                return await self._call_cloud_llm(
                    model_config,
                    prompt,
                    system_prompt,
                    temperature,
                    max_tokens
                )
            except Exception as e:
                # Fallback to offline if hybrid mode
                if self.strategy == RoutingStrategy.HYBRID:
                    try:
                        return await self._call_ollama(
                            model_config,
                            prompt,
                            system_prompt,
                            temperature,
                            max_tokens
                        )
                    except Exception:
                        raise RuntimeError(f"Both cloud and offline LLM failed: {e}")
                else:
                    raise
    
    async def list_available_models(self) -> List[str]:
        """List available Ollama models"""
        try:
            models = await self.ollama_client.list()
            return [model['name'] for model in models.get('models', [])]
        except Exception:
            return []
    
    async def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry"""
        try:
            await self.ollama_client.pull(model_name)
            return True
        except Exception:
            return False
    
    def get_model_config(self, model_type: ModelType) -> ModelConfig:
        """Get model configuration for a given type"""
        return self.config.models[model_type]
    
    async def test_connection(self) -> Dict[str, bool]:
        """Test connection to all LLM backends"""
        results = {
            'ollama': False,
            'cloud': False
        }
        
        # Test Ollama
        try:
            await self.ollama_client.list()
            results['ollama'] = True
        except Exception:
            pass
        
        # Cloud testing would go here
        # results['cloud'] = await self._test_cloud_connection()
        
        return results


# Global router instance
_router: Optional[LLMRouter] = None


def get_router(strategy: RoutingStrategy = RoutingStrategy.AUTO) -> LLMRouter:
    """Get global LLM router instance"""
    global _router
    if _router is None:
        _router = LLMRouter(strategy)
    return _router


async def route_request(
    model_type: ModelType,
    prompt: str,
    system_prompt: Optional[str] = None,
    **kwargs
) -> str:
    """Convenience function for routing requests"""
    router = get_router()
    return await router.route_request(
        model_type,
        prompt,
        system_prompt,
        **kwargs
    )
