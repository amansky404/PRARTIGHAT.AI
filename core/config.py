"""
PRATIGHAT.AI Configuration Module

This module handles all configuration settings for the PRATIGHAT-AI system,
including hardware detection, LLM routing, and operational modes.
"""

import os
import psutil
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional
import yaml


class OperationalMode(Enum):
    """Operational modes for PRATIGHAT-AI"""
    AUTOPILOT = "autopilot"  # Full autonomous execution
    ASSISTED = "assisted"    # User approval required
    MANUAL = "manual"        # User-driven with AI enhancement


class HardwareMode(Enum):
    """Hardware optimization modes"""
    LOW_END = "low_end"      # 2-4GB RAM, 3B models
    BALANCED = "balanced"    # 4-16GB RAM, 13B models
    HIGH_END = "high_end"    # 16GB+ RAM, 34B-70B models


class ModelType(Enum):
    """LLM model types"""
    STRATEGIST = "strategist"  # Attack planning and reasoning
    EXECUTOR = "executor"      # Code and PoC generation
    SCANNER = "scanner"        # Pattern detection
    REWRITER = "rewriter"      # Jailbreak and safety layer


@dataclass
class HardwareProfile:
    """Hardware capabilities profile"""
    ram_gb: float
    cpu_cores: int
    has_gpu: bool
    temperature: float
    battery: bool
    mode: HardwareMode
    
    @classmethod
    def detect(cls) -> "HardwareProfile":
        """Detect system hardware capabilities"""
        ram_gb = psutil.virtual_memory().total / (1024**3)
        cpu_cores = psutil.cpu_count(logical=True)
        
        # Simplified GPU detection
        has_gpu = False
        try:
            import torch
            has_gpu = torch.cuda.is_available()
        except ImportError:
            pass
        
        # Temperature detection (simplified)
        temperature = 50.0  # Default
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                temperature = list(temps.values())[0][0].current
        except (AttributeError, IndexError):
            pass
        
        # Battery detection
        battery = False
        try:
            battery_info = psutil.sensors_battery()
            battery = battery_info is not None and battery_info.power_plugged is False
        except AttributeError:
            pass
        
        # Determine hardware mode
        if ram_gb < 4:
            mode = HardwareMode.LOW_END
        elif ram_gb < 16:
            mode = HardwareMode.BALANCED
        else:
            mode = HardwareMode.HIGH_END
        
        # Adjust for temperature
        if temperature > 85:
            if mode == HardwareMode.HIGH_END:
                mode = HardwareMode.BALANCED
            elif mode == HardwareMode.BALANCED:
                mode = HardwareMode.LOW_END
        
        return cls(
            ram_gb=ram_gb,
            cpu_cores=cpu_cores,
            has_gpu=has_gpu,
            temperature=temperature,
            battery=battery,
            mode=mode
        )


@dataclass
class ModelConfig:
    """LLM model configuration"""
    name: str
    model_type: ModelType
    size: str  # e.g., "3B", "13B", "70B"
    offline: bool = True
    endpoint: Optional[str] = None
    
    @classmethod
    def get_model_for_hardware(
        cls, 
        model_type: ModelType, 
        hw_mode: HardwareMode
    ) -> "ModelConfig":
        """Select appropriate model based on hardware"""
        model_map = {
            HardwareMode.LOW_END: {
                ModelType.STRATEGIST: ("llama3.2:3b", "3B"),
                ModelType.EXECUTOR: ("qwen2.5:3b", "3B"),
                ModelType.SCANNER: ("phi3.5:3.8b", "3.8B"),
                ModelType.REWRITER: ("llama3.2:3b", "3B"),
            },
            HardwareMode.BALANCED: {
                ModelType.STRATEGIST: ("llama3.1:8b", "8B"),
                ModelType.EXECUTOR: ("qwen2.5:14b", "14B"),
                ModelType.SCANNER: ("llama3.1:8b", "8B"),
                ModelType.REWRITER: ("llama3.1:8b", "8B"),
            },
            HardwareMode.HIGH_END: {
                ModelType.STRATEGIST: ("llama3.1:70b", "70B"),
                ModelType.EXECUTOR: ("qwen2.5:32b", "32B"),
                ModelType.SCANNER: ("deepseek-r1:32b", "32B"),
                ModelType.REWRITER: ("llama3.1:70b", "70B"),
            }
        }
        
        model_name, size = model_map[hw_mode][model_type]
        return cls(
            name=model_name,
            model_type=model_type,
            size=size,
            offline=True
        )


@dataclass
class Config:
    """Main configuration for PRATIGHAT-AI"""
    
    # Operational settings
    operational_mode: OperationalMode = OperationalMode.ASSISTED
    
    # Hardware profile
    hardware: HardwareProfile = field(default_factory=HardwareProfile.detect)
    
    # Model configurations
    models: Dict[ModelType, ModelConfig] = field(default_factory=dict)
    
    # Database settings
    sqlite_path: str = "pratighat.db"
    chroma_path: str = "chroma_db"
    
    # API settings
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    
    # Tool settings
    tool_timeout: int = 300  # seconds
    max_recursion_depth: int = 5
    
    # Safety settings
    safe_mode: bool = True
    simulation_only: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "pratighat.log"
    
    def __post_init__(self):
        """Initialize models based on hardware"""
        if not self.models:
            for model_type in ModelType:
                self.models[model_type] = ModelConfig.get_model_for_hardware(
                    model_type, 
                    self.hardware.mode
                )
    
    @classmethod
    def from_yaml(cls, path: str) -> "Config":
        """Load configuration from YAML file"""
        if not os.path.exists(path):
            return cls()
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Convert enum strings to enums
        if 'operational_mode' in data:
            data['operational_mode'] = OperationalMode(data['operational_mode'])
        
        return cls(**data)
    
    def to_yaml(self, path: str) -> None:
        """Save configuration to YAML file"""
        data = {
            'operational_mode': self.operational_mode.value,
            'sqlite_path': self.sqlite_path,
            'chroma_path': self.chroma_path,
            'api_host': self.api_host,
            'api_port': self.api_port,
            'tool_timeout': self.tool_timeout,
            'max_recursion_depth': self.max_recursion_depth,
            'safe_mode': self.safe_mode,
            'simulation_only': self.simulation_only,
            'log_level': self.log_level,
            'log_file': self.log_file,
        }
        
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    
    def update_hardware_profile(self) -> None:
        """Re-detect hardware and update models"""
        self.hardware = HardwareProfile.detect()
        for model_type in ModelType:
            self.models[model_type] = ModelConfig.get_model_for_hardware(
                model_type,
                self.hardware.mode
            )


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance"""
    global _config
    if _config is None:
        config_path = os.environ.get('PRATIGHAT_CONFIG', 'config.yaml')
        _config = Config.from_yaml(config_path)
    return _config


def reload_config() -> Config:
    """Reload configuration"""
    global _config
    _config = None
    return get_config()
