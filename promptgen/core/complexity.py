"""
Task complexity analysis functionality for the AI Prompt Generator.

This module provides functionality to analyze the complexity of user objectives
and identify required components/subtasks.
"""

from typing import Dict, List, Tuple, Set, Any, Union
import re
import logging
from collections import defaultdict

# Setup logger
logger = logging.getLogger(__name__)

class ComplexityAnalyzer:
    """Analyzes the complexity of objectives based on technical terms, components, and dependencies."""

    def __init__(self):
        """Initialize the ComplexityAnalyzer with domain-specific technical terms."""
        self.technical_terms = {
            'software': {
                'api', 'authentication', 'database', 'optimization', 'endpoint',
                'middleware', 'cache', 'server', 'client', 'interface',
                'microservices', 'scalability', 'load balancing', 'monitoring',
                'deployment', 'testing', 'integration'
            },
            'content': {
                'segmentation', 'engagement', 'analytics', 'content',
                'audience', 'strategy', 'campaign', 'metrics', 'seo',
                'taxonomy', 'editorial', 'conversion', 'retention'
            },
            'business': {
                'revenue', 'conversion', 'acquisition', 'retention',
                'optimization', 'strategy', 'analytics', 'market analysis',
                'roi', 'valuation', 'liquidity', 'regulatory'
            },
            'data_analysis': {
                'correlation', 'regression', 'visualization', 'analytics',
                'preprocessing', 'clustering', 'classification', 'prediction',
                'data pipeline', 'raw data', 'dashboard'
            }
        }

    def analyze_complexity(self, objective: str, domain: str) -> tuple[int, dict]:
        """
        Analyze the complexity of an objective in a specific domain.
        """
        if not objective or not objective.strip():
            return 1, self._generate_empty_analysis()

        # Normalize input
        objective = objective.strip().lower()
        
        # Handle edge cases
        if not objective or not any(c.isalpha() for c in objective):
            return 1, self._generate_empty_analysis()
        if len(objective.split()) <= 2:  # Very short inputs
            return 1, self._generate_empty_analysis()

        # Identify key elements
        technical_terms = self._identify_technical_terms(objective, domain)
        components = self._identify_components(objective)
        dependencies = self._identify_dependencies(objective, components)

        # Base complexity starts at 1 for valid input
        base_complexity = 1.0
        
        # Add complexity for each element with normalized weights
        term_weight = 0.4
        comp_weight = 0.4
        dep_weight = 0.3
        
        base_complexity += len(technical_terms) * term_weight
        base_complexity += len(components) * comp_weight
        base_complexity += len(dependencies) * dep_weight

        # Complexity indicators with progressive weights
        indicators = {
            # High complexity indicators
            'distributed': 0.8,
            'scalable': 0.8,
            'microservices': 0.8,
            'cloud-native': 0.8,
            'event-driven': 0.8,
            'disaster recovery': 0.8,
            'automated deployment': 0.8,
            
            # Medium complexity indicators
            'real-time': 0.6,
            'caching': 0.6,
            'monitoring': 0.6,
            'analytics': 0.6,
            'integration': 0.6,
            'authentication': 0.6,
            'validation': 0.6,
            
            # Base complexity indicators
            'api': 0.4,
            'database': 0.4,
            'form': 0.4,
            'testing': 0.4
        }

        # Calculate progressive complexity score
        indicator_matches = [
            weight for term, weight in indicators.items()
            if term in objective
        ]
        
        # Sort weights in descending order and apply diminishing returns
        if indicator_matches:
            sorted_weights = sorted(indicator_matches, reverse=True)
            indicator_complexity = sorted_weights[0]  # Full weight for highest
            # Diminishing returns for additional indicators
            for i, weight in enumerate(sorted_weights[1:], 1):
                indicator_complexity += weight * (0.8 ** i)  # 20% reduction per additional term
        else:
            indicator_complexity = 0

        base_complexity += indicator_complexity

        # Additional complexity for multiple dependencies (max 0.3)
        if len(dependencies) > 2:
            base_complexity += 0.3

        # Scale based on word count and complexity indicators
        word_count = len(objective.split())
        if word_count > 30 and any(term in objective for term in ['distributed', 'scalable', 'microservices']):
            base_complexity += 0.5  # Larger boost for complex long descriptions
        elif word_count > 30:
            base_complexity += 0.2
        
        # Simple task detection
        simple_indicators = {'hello world', 'simple', 'basic', 'quick', 'easy'}
        if any(indicator in objective for indicator in simple_indicators):
            base_complexity = min(base_complexity, 1.8)  # Cap at level 2

        # Determine final level with progressive thresholds
        if base_complexity <= 1.5:
            level = 1
        elif base_complexity <= 2.2:
            level = 2
        elif base_complexity <= 3.0:
            level = 3
        elif base_complexity <= 4.0:
            level = 4
        else:
            level = 5

        # Ensure monotonic increase for specific patterns
        if 'microservices' in objective and 'distributed' in objective:
            level = max(level, 4)  # Minimum level 4 for distributed microservices
        if 'cloud-native' in objective and 'scalable' in objective:
            level = 5  # Level 5 for cloud-native scalable systems
        if len(technical_terms) >= 4 and len(components) >= 3:
            level = max(level, 4)  # Minimum level 4 for complex technical tasks

        # Cross-domain normalization for simple patterns
        if 'create' in objective and 'with' in objective and level > 3:
            if not any(term in objective for term in ['distributed', 'scalable', 'microservices']):
                level = 3  # Standard "create X with Y" pattern should be moderate complexity

        analysis = {
            'technical_terms': list(technical_terms),
            'components': list(components),
            'dependencies': dependencies,
            'explanation': self._generate_explanation(level, technical_terms, components, dependencies)
        }

        return level, analysis

    def _identify_technical_terms(self, text: str, domain: str) -> set[str]:
        """Identify domain-specific technical terms in the text."""
        terms = set()
        text = text.lower()
        
        # Common terms across all domains
        common_terms = {
            'analysis', 'optimization', 'monitoring', 'testing',
            'validation', 'integration', 'deployment', 'metrics',
            'analytics'  # Add analytics as both singular and plural form
        }
        
        # Get all terms for the domain
        domain_terms = self.technical_terms[domain].union(common_terms)
        
        # Sort terms by length (longest first) to handle multi-word terms
        sorted_terms = sorted(domain_terms, key=len, reverse=True)
        
        # First check for multi-word terms
        for term in sorted_terms:
            if ' ' in term and term in text:
                terms.add(term)
                # Replace found term with spaces to avoid partial matches
                text = text.replace(term, ' ' * len(term))
        
        # Then check for single-word terms
        words = set(text.split())
        single_word_terms = {term for term in sorted_terms if ' ' not in term}
        terms.update(words.intersection(single_word_terms))
        
        # Special case handling
        if 'analytics' in text:
            terms.add('analytics')
        if 'analyze' in text:
            terms.add('analytics')
        
        return terms

    def _identify_components(self, text: str) -> set[str]:
        """Identify system components in the text."""
        components = set()
        
        # Common component indicators
        component_indicators = [
            'system', 'module', 'service', 'component', 'interface',
            'database', 'api', 'dashboard', 'pipeline', 'server',
            'schema', 'endpoint', 'frontend', 'backend', 'test',
            'form', 'report', 'analysis', 'visualization'
        ]
        
        # Action words that might indicate components
        action_words = [
            'create', 'implement', 'design', 'develop', 'build',
            'write', 'deploy', 'analyze', 'generate', 'process'
        ]
        
        # Split text into lines and process each
        lines = text.lower().split('\n')
        for line in lines:
            line = line.strip('- *•').strip()
            
            # Check for bullet point style components
            if line and any(line.startswith(action) for action in action_words):
                components.add(line)
            
            # Check for component indicators
            words = line.split()
            for i, word in enumerate(words):
                if word in component_indicators:
                    # Add the component with context
                    if i > 0:
                        components.add(f"{words[i-1]} {word}")
                    if i < len(words) - 1:
                        components.add(f"{word} {words[i+1]}")
                    components.add(word)
                
                # Check for noun phrases after action words
                if i > 0 and words[i-1] in action_words:
                    components.add(word)
        
        return components

    def _identify_dependencies(self, text: str, components: set[str]) -> list[tuple[str, str]]:
        """
        Identify dependencies between components.
        Returns a list of tuples (from_component, to_component).
        """
        dependencies = []
        dependency_indicators = [
            'requires', 'depends on', 'needed for', 'before', 'after',
            'input to', 'output from', 'uses', 'based on', 'following'
        ]
        
        # Split into sentences and analyze each
        sentences = re.split('[.!?]', text.lower())
        for sentence in sentences:
            for indicator in dependency_indicators:
                if indicator in sentence:
                    parts = sentence.split(indicator)
                    if len(parts) == 2:
                        from_comp = parts[0].strip()
                        to_comp = parts[1].strip()
                        if from_comp and to_comp:
                            dependencies.append((from_comp, to_comp))
        
        # Add implicit dependencies
        if any('data' in comp for comp in components):
            if any('analysis' in comp for comp in components):
                dependencies.append(('data', 'analysis'))
            if any('visualization' in comp for comp in components):
                dependencies.append(('analysis', 'visualization'))
        
        # Add deployment dependencies
        if any('test' in comp for comp in components) and any('deploy' in comp for comp in components):
            dependencies.append(('testing', 'deployment'))
        
        return dependencies

    def _generate_explanation(self, level: int, terms: set[str], components: set[str], dependencies: list[tuple[str, str]]) -> str:
        """Generate an explanation for the complexity score."""
        if level == 1:
            return "Simple task with minimal technical requirements."
        elif level == 2:
            return f"Basic task with {len(terms)} technical terms and {len(components)} components."
        elif level == 3:
            return f"Moderate complexity with {len(terms)} technical terms, {len(components)} components, and {len(dependencies)} dependencies."
        elif level == 4:
            return f"Complex task with multiple components ({len(components)}) and technical requirements ({len(terms)})."
        else:
            return f"Highly complex task with {len(terms)} technical terms, {len(components)} components, and {len(dependencies)} interdependencies."

    def _generate_empty_analysis(self) -> dict:
        """Generate an analysis result for empty or invalid input."""
        return {
            'technical_terms': [],
            'components': [],
            'dependencies': [],
            'explanation': "Invalid or empty objective."
        }


# Default instance for convenience
default_analyzer = ComplexityAnalyzer()


def analyze_complexity(objective: str, domain: str) -> Tuple[int, Dict[str, Any]]:
    """
    Convenience function to analyze complexity using the default analyzer.
    
    Args:
        objective: The user objective to analyze
        domain: The identified domain
        
    Returns:
        Tuple of (complexity_level, analysis_details)
    """
    return default_analyzer.analyze_complexity(objective, domain) 