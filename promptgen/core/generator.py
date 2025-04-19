"""
Prompt generation functionality for the AI Prompt Generator.

This module provides the core functionality for generating structured prompts
based on user objectives, domains, and templates.
"""

from typing import Dict, List, Tuple, Any, Optional
import logging
from ..templates.loader import PromptTemplate, TemplateLibrary
from ..techniques.library import PromptTechnique, get_technique
from .classifier import classify_domain
from .complexity import analyze_complexity

# Setup logger
logger = logging.getLogger(__name__)


class TemplateFactory:
    """
    Factory class for creating and selecting templates based on requirements.
    
    This class implements the Factory Pattern to create appropriate templates
    based on domain type, complexity, and other factors.
    """
    
    def __init__(self, template_library=None):
        """
        Initialize the factory with a template library.
        
        Args:
            template_library: Library containing available templates
        """
        from ..templates.loader import default_library
        self.template_library = template_library or default_library
        
        # Template scoring weights
        self.scoring_weights = {
            'domain_match': 1.0,  # Exact domain match
            'domain_fallback': 0.5,  # General domain fallback
            'complexity_match': 0.8,  # Complexity within range
            'component_match': 0.6,  # Required components present
            'tag_match': 0.3,  # Matching tags
        }
    
    def score_template(self, template: PromptTemplate, domain: str, complexity: int, 
                      components: List[str] = None, tags: List[str] = None) -> float:
        """
        Score a template based on how well it matches the requirements.
        
        Args:
            template: Template to score
            domain: Required domain
            complexity: Required complexity level
            components: Optional required components
            tags: Optional desired tags
            
        Returns:
            Score between 0 and 1
        """
        score = 0.0
        weights = self.scoring_weights
        
        # Domain match
        if template.domain == domain:
            score += weights['domain_match']
        elif template.domain == 'general':
            score += weights['domain_fallback']
            
        # Complexity match
        min_complexity, max_complexity = template.complexity_range
        if min_complexity <= complexity <= max_complexity:
            score += weights['complexity_match']
        else:
            # Penalty for complexity mismatch
            score -= abs(complexity - (min_complexity + max_complexity) / 2) * 0.1
            
        # Component match
        if components:
            required = set(template.get_required_sections())
            optional = set(template.get_optional_sections())
            all_sections = required.union(optional)
            match_ratio = sum(1 for c in components if c in all_sections) / len(components)
            score += weights['component_match'] * match_ratio
            
        # Tag match
        if tags and template.tags:
            tag_matches = sum(1 for tag in tags if tag in template.tags)
            tag_ratio = tag_matches / len(tags)
            score += weights['tag_match'] * tag_ratio
            
        return max(0.0, min(1.0, score))
    
    def create_template(self, domain_type: str, complexity: int, 
                       components: List[str] = None, tags: List[str] = None) -> PromptTemplate:
        """
        Create a template based on domain type, complexity, and required components.
        
        Args:
            domain_type: The domain of the prompt (e.g., 'software', 'content')
            complexity: The complexity level of the task (1-5)
            components: Optional list of required components/sections
            tags: Optional list of desired tags
            
        Returns:
            A suitable prompt template
            
        Raises:
            ValueError: If no suitable template is found
        """
        # Get all potentially suitable templates
        templates = self.template_library.find_templates(domain_type, complexity)
        general_templates = self.template_library.find_templates("general", complexity)
        
        # Score all templates
        scored_templates = []
        
        # Score domain-specific templates
        for template in templates:
            score = self.score_template(template, domain_type, complexity, components, tags)
            scored_templates.append((score, template))
            
        # Score general templates with a small penalty
        for template in general_templates:
            score = self.score_template(template, domain_type, complexity, components, tags) * 0.9
            scored_templates.append((score, template))
            
        if not scored_templates:
            raise ValueError(f"No templates available for domain '{domain_type}' with complexity {complexity}")
            
        # Sort by score and return the best match
        scored_templates.sort(reverse=True, key=lambda x: x[0])
        best_score, best_template = scored_templates[0]
        
        logger.info(f"Selected template '{best_template.name}' with score {best_score:.2f}")
        return best_template


class PromptGenerator:
    """
    Main class for generating prompts based on user objectives.
    """
    
    def __init__(self, template_factory=None, technique_library=None):
        """
        Initialize the prompt generator with a template factory.
        
        Args:
            template_factory: Factory for creating templates
            technique_library: Library of prompting techniques
        """
        self.template_factory = template_factory or TemplateFactory()
        from ..techniques.library import default_library
        self.technique_library = technique_library or default_library
    
    def generate_prompt(self, 
                       objective: str, 
                       domain: str = None, 
                       complexity: int = None,
                       components: List[str] = None,
                       context: Dict[str, Any] = None) -> str:
        """
        Generate a prompt based on the user objective.
        
        Args:
            objective: The user objective
            domain: The domain (if known, otherwise will be classified)
            complexity: The complexity level (if known, otherwise will be estimated)
            components: Optional list of required components/sections
            context: Additional context for prompt generation
            
        Returns:
            Generated prompt text
        """
        context = context or {}
        context["objective"] = objective
        
        # If domain not provided, classify it
        if not domain:
            domain, confidence = classify_domain(objective)
            context["domain_confidence"] = confidence
        
        context["domain"] = domain
        
        # If complexity not provided, analyze it
        if not complexity:
            complexity, analysis = analyze_complexity(objective, domain)
            context["complexity_analysis"] = analysis
            
            # If components not provided, use identified ones from analysis
            if not components and "components" in analysis:
                components = analysis["components"]
        
        context["complexity"] = complexity
        if components:
            context["components"] = components
        
        # Get appropriate template
        template = self.template_factory.create_template(
            domain_type=domain,
            complexity=complexity,
            components=components
        )
        
        # Generate the prompt using the template
        return template.generate(context)


# Default instance for convenience
default_generator = PromptGenerator()


def generate_prompt(objective: str, 
                   domain: str = None, 
                   complexity: int = None,
                   components: List[str] = None,
                   context: Dict[str, Any] = None) -> str:
    """
    Convenience function to generate a prompt using the default generator.
    
    Args:
        objective: The user objective
        domain: Optional domain classification
        complexity: Optional complexity level
        components: Optional required components
        context: Additional context for generation
        
    Returns:
        Generated prompt text
    """
    return default_generator.generate_prompt(
        objective=objective,
        domain=domain,
        complexity=complexity,
        components=components,
        context=context
    ) 