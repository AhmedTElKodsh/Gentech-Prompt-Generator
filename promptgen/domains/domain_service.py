"""
Domain service for the AI Prompt Generator.

This module provides a centralized service to coordinate domain-specific
strategies and handle the mapping between domain names and their content strategies.
"""

from typing import Dict, List, Any, Optional, Tuple
import logging
import re

from . import (
    populate_software_section,
    populate_content_section,
    populate_business_section,
    populate_data_analysis_section
)

# Setup logger
logger = logging.getLogger(__name__)


class DomainService:
    """
    Domain service that coordinates domain-specific content strategies.
    
    This class acts as a mediator between the prompt generator and the 
    domain-specific content strategies.
    """
    
    def __init__(self):
        """Initialize the domain service with mappings from domain names to content strategies."""
        self.domain_content_strategies = {
            "software": populate_software_section,
            "content": populate_content_section,
            "business": populate_business_section,
            "data": populate_data_analysis_section
        }
        
        # Define role to domain mappings
        self.role_to_domain = {
            # Software roles
            "software developer": "software",
            "developer": "software",
            "programmer": "software",
            "software engineer": "software",
            "web developer": "software",
            "mobile developer": "software",
            "full stack developer": "software",
            "backend developer": "software",
            "frontend developer": "software",
            "devops engineer": "software",
            
            # Digital Marketing roles
            "digital marketer": "content",
            "marketing specialist": "content",
            "seo specialist": "content",
            "social media manager": "content",
            "digital marketing manager": "content",
            "ppc specialist": "content",
            "email marketer": "content",
            "marketing analyst": "business",
            "growth hacker": "business",
            
            # Content Creation roles
            "content creator": "content",
            "content writer": "content",
            "copywriter": "content",
            "blogger": "content",
            "journalist": "content",
            "editor": "content",
            "content strategist": "content",
            "technical writer": "content",
            
            # Video Editing roles
            "video editor": "content",
            "videographer": "content",
            "film editor": "content",
            "motion graphics designer": "content",
            "video producer": "content",
            
            # Data analysis roles
            "data analyst": "data",
            "data scientist": "data",
            "business analyst": "data",
            "statistician": "data",
            "data engineer": "data",
            "researcher": "data",
            "analyst": "data",
            "bi analyst": "data",
            "business intelligence analyst": "data",
        }
    
    def extract_role_from_objective(self, objective: str) -> Tuple[str, str]:
        """
        Extract the user's role from the beginning of their objective and 
        return the cleaned objective without the role prefix.
        
        Args:
            objective: The user's input message which may start with their role
            
        Returns:
            Tuple of (domain_name, cleaned_objective)
        """
        # Default domain
        domain = "general"
        
        # Try to extract role from beginning of message
        objective_lower = objective.lower().strip()
        
        # Check for "As a [role]" pattern first
        as_a_pattern = re.compile(r'^\s*as\s+a(?:n)?\s+([^,.:;]+)(?:[,.:;]|\s+i\s+)', re.IGNORECASE)
        match = as_a_pattern.search(objective_lower)
        if match:
            role_text = match.group(1).strip()
            # Check if this extracted role is in our mappings
            for role, mapped_domain in self.role_to_domain.items():
                if role in role_text or role_text in role:
                    domain = mapped_domain
                    # Remove the role prefix from the objective
                    clean_objective = objective[match.end():].strip()
                    logger.info(f"Detected 'As a' role pattern '{role_text}', mapped to domain '{domain}'")
                    return domain, clean_objective
        
        # Look for role at the beginning of the message (with various separators)
        for role, mapped_domain in self.role_to_domain.items():
            # Match: "Role: text" or "Role - text" or "Role, text" or "Role text"
            role_pattern = re.compile(r'^\s*(' + re.escape(role) + r')\s*[:,-]?\s+', re.IGNORECASE)
            match = role_pattern.search(objective_lower)
            
            if match:
                domain = mapped_domain
                # Remove the role prefix from the objective
                clean_objective = objective[match.end():].strip()
                logger.info(f"Detected role '{match.group(1)}', mapped to domain '{domain}'")
                return domain, clean_objective
        
        # If no role pattern is found, return the original objective
        return domain, objective
    
    def populate_section(self, section: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Populate a template section using the appropriate domain-specific strategy.
        
        Args:
            section: Template section definition
            context: Content generation context including the domain
            
        Returns:
            Generated content for the section
        """
        domain = context.get("domain", "").lower()
        
        # Extract role-based domain if present in the objective
        objective = context.get("objective", "")
        if objective:
            extracted_domain, clean_objective = self.extract_role_from_objective(objective)
            
            # Only update if we found a role
            if extracted_domain != "general":
                domain = extracted_domain
                # Update the context with cleaned objective and extracted domain
                context["domain"] = domain
                context["original_objective"] = objective
                context["objective"] = clean_objective
        
        # Get the appropriate domain content strategy function
        if domain in self.domain_content_strategies:
            strategy_fn = self.domain_content_strategies[domain]
            logger.info(f"Using {domain} domain strategy to populate section {section.get('name', '')}")
            return strategy_fn(section, context)
        
        # If domain not recognized, use simple template substitution
        logger.warning(f"No strategy found for domain '{domain}', using basic template substitution")
        content_template = section.get("content_template", "")
        try:
            return content_template.format(**context)
        except KeyError as e:
            logger.warning(f"Missing context key for template: {e}")
            return f"{content_template} (Missing context: {e})"
    
    def get_available_domains(self) -> List[str]:
        """Get a list of available domain names."""
        return list(self.domain_content_strategies.keys())
    
    def get_supported_roles(self) -> List[str]:
        """Get a list of supported user roles."""
        return list(self.role_to_domain.keys())
    
    def register_domain_strategy(self, domain: str, strategy_fn) -> None:
        """
        Register a new domain strategy function.
        
        Args:
            domain: Domain name
            strategy_fn: Function to populate sections for this domain
        """
        self.domain_content_strategies[domain] = strategy_fn
        logger.info(f"Registered new domain strategy for '{domain}'")
    
    def register_role_mapping(self, role: str, domain: str) -> None:
        """
        Register a new role to domain mapping.
        
        Args:
            role: User role or job title
            domain: Domain name to map this role to
        """
        if domain not in self.domain_content_strategies:
            logger.warning(f"Mapping role '{role}' to unknown domain '{domain}'")
        
        self.role_to_domain[role.lower()] = domain
        logger.info(f"Registered new role mapping: '{role}' -> '{domain}'")


# Default instance for convenience
default_service = DomainService()


def populate_section(section: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Convenience function to populate a section using the default domain service.
    
    Args:
        section: Section definition
        context: Content generation context
        
    Returns:
        Generated content
    """
    return default_service.populate_section(section, context) 