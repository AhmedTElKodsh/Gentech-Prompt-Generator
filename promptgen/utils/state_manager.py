"""State management utility for the AI Prompt Generator."""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os
from dataclasses import dataclass, asdict
from ..config import get_config

@dataclass
class PromptHistory:
    """Represents a single prompt generation history item."""
    timestamp: str
    objective: str
    generated_prompt: str
    domain: str
    techniques_used: List[str]
    quality_score: float
    metadata: Dict[str, Any]

class StateManager:
    """Manages application state and history."""
    
    def __init__(self):
        """Initialize the state manager."""
        self.config = get_config()
        self.history: List[PromptHistory] = []
        self._load_history()
    
    def add_to_history(
        self,
        objective: str,
        generated_prompt: str,
        domain: str,
        techniques_used: List[str],
        quality_score: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a new prompt generation to history.
        
        Args:
            objective: The original user objective
            generated_prompt: The generated prompt
            domain: The domain of the prompt
            techniques_used: List of techniques used
            quality_score: Quality score of the prompt
            metadata: Additional metadata about the generation
        """
        history_item = PromptHistory(
            timestamp=datetime.now().isoformat(),
            objective=objective,
            generated_prompt=generated_prompt,
            domain=domain,
            techniques_used=techniques_used,
            quality_score=quality_score,
            metadata=metadata or {}
        )
        
        self.history.append(history_item)
        
        # Trim history if it exceeds max items
        if len(self.history) > self.config.max_history_items:
            self.history = self.history[-self.config.max_history_items:]
        
        self._save_history()
    
    def get_history(
        self,
        limit: Optional[int] = None,
        domain: Optional[str] = None,
        min_quality: Optional[float] = None
    ) -> List[PromptHistory]:
        """Get prompt generation history with optional filtering.
        
        Args:
            limit: Maximum number of items to return
            domain: Filter by domain
            min_quality: Minimum quality score
            
        Returns:
            List of history items matching the criteria
        """
        filtered_history = self.history
        
        if domain:
            filtered_history = [h for h in filtered_history if h.domain == domain]
        
        if min_quality is not None:
            filtered_history = [h for h in filtered_history if h.quality_score >= min_quality]
        
        if limit:
            filtered_history = filtered_history[-limit:]
        
        return filtered_history
    
    def clear_history(self) -> None:
        """Clear all history."""
        self.history = []
        self._save_history()
    
    def get_best_prompts(self, limit: int = 5) -> List[PromptHistory]:
        """Get the highest quality prompts from history.
        
        Args:
            limit: Maximum number of prompts to return
            
        Returns:
            List of best performing prompts
        """
        sorted_history = sorted(
            self.history,
            key=lambda x: x.quality_score,
            reverse=True
        )
        return sorted_history[:limit]
    
    def get_domain_statistics(self) -> Dict[str, Any]:
        """Get statistics about prompt generation by domain.
        
        Returns:
            Dictionary containing domain statistics
        """
        stats = {}
        for item in self.history:
            if item.domain not in stats:
                stats[item.domain] = {
                    'count': 0,
                    'avg_quality': 0.0,
                    'techniques_used': {}
                }
            
            domain_stats = stats[item.domain]
            domain_stats['count'] += 1
            domain_stats['avg_quality'] = (
                (domain_stats['avg_quality'] * (domain_stats['count'] - 1) + item.quality_score)
                / domain_stats['count']
            )
            
            for technique in item.techniques_used:
                if technique not in domain_stats['techniques_used']:
                    domain_stats['techniques_used'][technique] = 0
                domain_stats['techniques_used'][technique] += 1
        
        return stats
    
    def _get_history_file_path(self) -> str:
        """Get the path to the history file."""
        if not os.path.exists(self.config.cache_dir):
            os.makedirs(self.config.cache_dir)
        return os.path.join(self.config.cache_dir, 'prompt_history.json')
    
    def _save_history(self) -> None:
        """Save history to file."""
        if not self.config.cache_responses:
            return
            
        history_data = [asdict(item) for item in self.history]
        with open(self._get_history_file_path(), 'w') as f:
            json.dump(history_data, f, indent=2)
    
    def _load_history(self) -> None:
        """Load history from file."""
        if not self.config.cache_responses:
            return
            
        try:
            history_path = self._get_history_file_path()
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    history_data = json.load(f)
                self.history = [PromptHistory(**item) for item in history_data]
        except Exception as e:
            print(f"Error loading history: {e}")
            self.history = []

# Create global state manager instance
state_manager = StateManager()

def get_state_manager() -> StateManager:
    """Get the global state manager instance."""
    return state_manager 